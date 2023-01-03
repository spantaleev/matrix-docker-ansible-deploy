# Setting up postgres backup (optional)

The playbook can install and configure [docker-postgres-backup-local](https://github.com/prodrigestivill/docker-postgres-backup-local) for you via the [com.devture.ansible.role.postgres_backup](https://github.com/devture/com.devture.ansible.role.postgres_backup) Ansible role.

For a more complete backup solution (one that includes not only Postgres, but also other configuration/data files), you may wish to look into [borg backup](configuring-playbook-backup-borg.md) instead.


## Adjusting the playbook configuration

Minimal working configuration (`inventory/host_vars/matrix.DOMAIN/vars.yml`) to enable Postgres backup:

```yaml
devture_postgres_backup_enabled: true
```

Refer to the table below for additional configuration variables and their default values.


| Name                              | Default value                | Description                                                      |
| :-------------------------------- | :--------------------------- | :--------------------------------------------------------------- |
|`devture_postgres_backup_enabled`|`false`|Set to true to use [docker-postgres-backup-local](https://github.com/prodrigestivill/docker-postgres-backup-local) to create automatic database backups|
|`devture_postgres_backup_schedule`| `'@daily'` |Cron-schedule specifying the interval between postgres backups.|
|`devture_postgres_backup_keep_days`|`7`|Number of daily backups to keep|
|`devture_postgres_backup_keep_weeks`|`4`|Number of weekly backups to keep|
|`devture_postgres_backup_keep_months`|`12`|Number of monthly backups to keep|
|`devture_postgres_base_path` | `"{{ matrix_base_data_path }}/postgres-backup"` | Base path for postgres-backup. Also see `devture_postgres_data_path` |
|`devture_postgres_data_path` | `"{{ devture_postgres_base_path }}/data"` | Storage path for postgres-backup database backups |


## Installing

After configuring the playbook, run the [installation](installing.md) command again:

```
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```
