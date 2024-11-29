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

The shortcut commands with `just` program are also available: `just run-tags install-all,start` or `just run-tags setup-all,start`

`just run-tags install-all,start` is useful for maintaining your setup quickly when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just run-tags setup-all,start`, or these components will still remain installed. For more information about `just` shortcuts, take a look at this page: [Running `just` commands](just.md)
