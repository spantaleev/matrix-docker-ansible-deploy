<!--
SPDX-FileCopyrightText: 2026 Slavi Pantaleev

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up system cleanup (optional)

The playbook can do some housekeeping on the server: removing Docker leftovers, old logs and arbitrary paths, and (on Debian-based distributions) upgrading packages and purging old kernels. Everything is off by default.

The [Ansible role for system cleanup](https://github.com/mother-of-all-self-hosting/ansible-role-cleanup) is developed and maintained by [the MASH (mother-of-all-self-hosting) project](https://github.com/mother-of-all-self-hosting). For all options, see the role's [`defaults/main.yml`](https://github.com/mother-of-all-self-hosting/ansible-role-cleanup/blob/main/defaults/main.yml).

## Adjusting the playbook configuration

To enable the cleanup tasks you'd like, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
# Removes stopped containers and Docker images which a newer image of the same repository superseded
# at least 3 days ago (and which no container uses). Unlike `docker image prune -a`, unused images
# without a newer version (e.g. of services you have stopped) are kept.
system_cleanup_docker: true

# Installs a systemd timer which runs `journalctl --vacuum-time=7d` daily.
# journald already limits the space logs take up on its own, so this is only needed for keeping logs for a shorter time.
system_cleanup_logs: true

# Absolute paths to remove on each run
system_cleanup_paths: []

# The following options only have an effect on Debian-based distributions.

# Runs a safe upgrade, `apt-get autoremove`, `apt-get clean`, etc.
system_cleanup_apt: true

# WARNING: very dangerous! Purges old Linux kernels, and their modules
system_cleanup_kernels: false
```

The Docker cleanup runs when the playbook is run with the `start` tag (e.g. `just install-all` or `just setup-all`), after all services have been started. To also run it daily via a systemd timer (useful for removing superseded images without re-running the playbook), add `system_cleanup_docker_timer_enabled: true`.

## Installing

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just setup-all`

## Usage

The Docker cleanup is done by a script, which you can also run by hand on the server. Pass `--dry-run` to only see what it would remove:

```sh
/matrix/system-cleanup/bin/cleanup-docker --dry-run
```
