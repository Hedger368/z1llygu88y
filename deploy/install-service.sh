#!/usr/bin/env bash
# Run once as root: sudo bash deploy/install-service.sh gha-runner
set -euo pipefail

if [[ $EUID -ne 0 || $# -ne 1 ]]; then
    echo "Usage: sudo bash deploy/install-service.sh RUNNER_USER" >&2
    exit 1
fi
runner_user=$1
if [[ ! $runner_user =~ ^[a-z_][a-z0-9_-]*\$?$ ]] || ! id "$runner_user" >/dev/null 2>&1; then
    echo "Provide the existing Linux account running the GitHub runner." >&2
    exit 1
fi
if [[ $(id -u "$runner_user") == 0 ]]; then
    echo "The GitHub runner must run as a non-root user." >&2
    exit 1
fi
python3 -c 'import sys; assert sys.version_info >= (3, 10), "Python 3.10+ required"'
for tool in systemctl visudo git flock; do
    command -v "$tool" >/dev/null
done
script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
systemctl_bin=$(command -v systemctl)

if ! id z1llygu88y >/dev/null 2>&1; then
    useradd --system --user-group --home-dir /var/lib/z1llygu88y --shell /usr/sbin/nologin z1llygu88y
fi
install -d -m 0755 -o "$runner_user" -g "$(id -gn "$runner_user")" /opt/z1llygu88y
install -d -m 0755 -o "$runner_user" -g "$(id -gn "$runner_user")" /opt/z1llygu88y/releases
install -m 0644 "$script_dir/z1llygu88y.service" /etc/systemd/system/z1llygu88y.service
if [[ ! -e /etc/z1llygu88y.env ]]; then
    install -m 0600 "$script_dir/../.env.example" /etc/z1llygu88y.env
fi

# Limit service control to this bot; the runner does not need general sudo access.
sudoers_tmp=$(mktemp)
trap 'rm -f "$sudoers_tmp"' EXIT
printf '%s ALL=(root) NOPASSWD: %s restart z1llygu88y.service, %s stop z1llygu88y.service\n' \
    "$runner_user" "$systemctl_bin" "$systemctl_bin" > "$sudoers_tmp"
visudo -cf "$sudoers_tmp"
install -m 0440 "$sudoers_tmp" /etc/sudoers.d/z1llygu88y
"$systemctl_bin" daemon-reload
"$systemctl_bin" enable z1llygu88y.service

echo "Installed. Set DISCORD_TOKEN with: sudoedit /etc/z1llygu88y.env"
echo "Then push the latest tag. The deployment will start the bot."
