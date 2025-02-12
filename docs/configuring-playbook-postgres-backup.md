<!--
SPDX-FileCopyrightText: 2021 foxcris
SPDX-FileCopyrightText: 2021 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up postgres backup (optional)

The playbook can install and configure [docker-postgres-backup-local](https://github.com/prodrigestivill/docker-postgres-backup-local) for you via the [ansible-role-postgres-backup](https://github.com/mother-of-all-self-hosting/ansible-role-postgres-backup) Ansible role.

For a more complete backup solution (one that includes not only Postgres, but also other configuration/data files), you may wish to look into [BorgBackup](configuring-playbook-backup-borg.md) instead.

## Adjusting the playbook configuration

To enable Postgres backup, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
postgres_backup_enabled: true
```

Refer to the table below for additional configuration variables and their default values.

| Name                              | Default value                | Description                                                      |
| :-------------------------------- | :--------------------------- | :--------------------------------------------------------------- |
|`postgres_backup_enabled`|`false`|Set to true to use [docker-postgres-backup-local](https://github.com/prodrigestivill/docker-postgres-backup-local) to create automatic database backups|
|`postgres_backup_schedule`| `'@daily'` |Cron-schedule specifying the interval between postgres backups.|
|`postgres_backup_keep_days`|`7`|Number of daily backups to keep|
|`postgres_backup_keep_weeks`|`4`|Number of weekly backups to keep|
|`postgres_backup_keep_months`|`12`|Number of monthly backups to keep|
|`postgres_backup_base_path` | `"{{ matrix_base_data_path }}/postgres-backup"` | Base path for postgres-backup. Also see `postgres_backup_data_path` |
|`postgres_backup_data_path` | `"{{ postgres_backup_base_path }}/data"` | Storage path for postgres-backup database backups |

## Installing

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-postgres-backup`.
