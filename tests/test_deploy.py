"""Exercise real deployment shell logic with isolated files and fake service/venv commands."""
import os
import shlex
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class DeploymentTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.app = self.base / "app"
        (self.app / "releases").mkdir(parents=True)
        self.repo = self.base / "repo"
        self.repo.mkdir()
        self.bin = self.base / "bin"
        self.bin.mkdir()
        self.log = self.base / "service.log"
        self.env = dict(os.environ, PATH=f"{self.bin}:{os.environ['PATH']}",
                        TEST_APP=str(self.app), TEST_LOG=str(self.log))
        # Relocate the production constant, so tests never touch /opt or root services.
        self.script = self.base / "deploy.sh"
        source = (ROOT / "deploy/deploy.sh").read_text()
        self.script.write_text(source.replace("app_root=/opt/z1llygu88y", f"app_root={shlex.quote(str(self.app))}"))
        self.write_command("sudo", '#!/bin/bash\n[[ $1 == -n ]] && shift\nexec "$@"\n')
        self.write_command("systemctl", """#!/bin/bash
set -eu
if [[ $1 == restart ]]; then
    target=$(readlink -f "$TEST_APP/current")
    echo "$target" >> "$TEST_LOG"
    if [[ ${FAIL_START:-0} == 1 && $target != */previous ]]; then exit 1; fi
    if [[ ${FAIL_ROLLBACK:-0} == 1 ]]; then exit 1; fi
fi
""")
        self.write_command("python3", """#!/bin/bash
set -eu
[[ $1 == -m && $2 == venv ]]
mkdir -p "$3/bin"
cat > "$3/bin/python" <<'PYTHON'
#!/bin/bash
if [[ ${FAIL_INSTALL:-0} == 1 && $* == *'pip install'* ]]; then exit 1; fi
exit 0
PYTHON
chmod +x "$3/bin/python"
""")
        self.git("init", "-q")
        (self.repo / "bot.py").write_text("# deployment fixture\n")
        (self.repo / "requirements.txt").write_text("")
        self.git("add", ".")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-qm", "fixture")
        (self.repo / ".env").write_text("DISCORD_TOKEN=not-for-release\n")

    def write_command(self, name, source):
        path = self.bin / name
        path.write_text(source)
        path.chmod(0o755)

    def git(self, *args):
        return subprocess.check_output([shutil.which("git"), *args], cwd=self.repo, text=True).strip()

    def previous_release(self):
        previous = self.app / "releases/previous"
        previous.mkdir()
        (self.app / "current").symlink_to(previous)
        return previous

    def deploy(self, **env):
        return subprocess.run(["bash", str(self.script)], cwd=self.repo,
                              env=dict(self.env, **env), text=True, capture_output=True)

    def test_success_exports_only_tracked_files_and_records_revision(self):
        result = self.deploy()
        self.assertEqual(result.returncode, 0, result.stderr)
        current = (self.app / "current").resolve()
        self.assertEqual(current.stat().st_mode & 0o777, 0o755)
        self.assertTrue((current / "bot.py").exists())
        self.assertFalse((current / ".env").exists())
        self.assertEqual((current / "REVISION").read_text().strip(), self.git("rev-parse", "HEAD"))

    def test_dependency_failure_leaves_running_release_untouched(self):
        previous = self.previous_release()
        result = self.deploy(FAIL_INSTALL="1")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual((self.app / "current").resolve(), previous)
        self.assertFalse(self.log.exists())
        self.assertEqual(list((self.app / "releases").iterdir()), [previous])

    def test_startup_failure_restores_and_restarts_previous_release(self):
        previous = self.previous_release()
        result = self.deploy(FAIL_START="1")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual((self.app / "current").resolve(), previous)
        starts = self.log.read_text().splitlines()
        self.assertEqual(len(starts), 2)
        self.assertEqual(starts[-1], str(previous))

    def test_first_deployment_failure_removes_current_pointer(self):
        result = self.deploy(FAIL_START="1")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.app / "current").is_symlink())
        self.assertIn("First deployment failed", result.stderr)

    def test_rollback_failure_is_reported(self):
        self.previous_release()
        result = self.deploy(FAIL_START="1", FAIL_ROLLBACK="1")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Rollback restart failed", result.stderr)
