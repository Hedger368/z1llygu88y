#!/usr/bin/env bash
set -euo pipefail
umask 022

app_root=/opt/z1llygu88y
service=z1llygu88y.service
systemctl_bin=$(command -v systemctl)
repo_root=$(git rev-parse --show-toplevel)
cd "$repo_root"

if [[ ! -d $app_root/releases || ! -w $app_root/releases ]]; then
    echo "Run deploy/install-service.sh once as root for this runner account first." >&2
    exit 1
fi
# Also protect against simultaneous manual invocations on the server.
exec 9>"$app_root/deploy.lock"
flock 9

sha=$(git rev-parse HEAD)
release=$(mktemp -d "$app_root/releases/${sha}.XXXXXX")
previous=""
if [[ -e $app_root/current ]]; then
    previous=$(readlink -f "$app_root/current")
fi
switched=false
finished=false

switch_to() {
    ln -s "$1" "$app_root/current.next"
    mv -Tf "$app_root/current.next" "$app_root/current"
}

cleanup() {
    local status=$?
    trap - EXIT INT TERM
    rm -f "$app_root/current.next"
    if [[ $finished == false ]]; then
        if [[ $switched == true ]]; then
            if [[ -n $previous && -d $previous ]]; then
                echo "Deployment failed; restoring $previous" >&2
                switch_to "$previous"
                if ! sudo -n "$systemctl_bin" restart "$service"; then
                    echo "Rollback restart failed. Check: sudo journalctl -u $service" >&2
                fi
                # Keep the failed release for diagnosis; a failed rollback may still use it.
            else
                sudo -n "$systemctl_bin" stop "$service" || true
                rm -f "$app_root/current"
                echo "First deployment failed. Check: sudo journalctl -u $service" >&2
            fi
        else
            rm -rf -- "$release"
        fi
    fi
    exit "$status"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

# Export tracked files only. The running bot is independent of the Actions workspace.
git archive HEAD | tar -x -C "$release"
chmod 0755 "$release" # mktemp defaults to 0700; the separate bot user needs access.
python3 -m venv "$release/.venv"
"$release/.venv/bin/python" -m pip install --disable-pip-version-check -r "$release/requirements.txt"
"$release/.venv/bin/python" -m pip check
"$release/.venv/bin/python" -m py_compile "$release/bot.py"
# Import without logging in to catch missing dependencies and startup errors.
(cd "$release" && "$release/.venv/bin/python" -c 'import bot')
printf '%s\n' "$sha" > "$release/REVISION"

switch_to "$release"
switched=true
# Type=notify waits for bot.on_ready(), so a bad token or connection fails deployment.
sudo -n "$systemctl_bin" restart "$service"
"$systemctl_bin" is-active --quiet "$service"
finished=true
echo "Deployed $sha; bot connected to Discord."
