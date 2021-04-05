# Setting up postgres backup (optional)

The playbook can install and configure [docker-postgres-backup-local](https://github.com/prodrigestivill/docker-postgres-backup-local) for you.

## Adjusting the playbook configuration

Minimal working configuration (`inventory/host_vars/matrix.DOMAIN/vars.yml`) to enable Postgres backup:

```yaml
matrix_postgres_backup_enabled: true
```

Refer to the table below for additional configuration variables and their default values.


| Name                              | Default value                | Description                                                      |
| :-------------------------------- | :--------------------------- | :--------------------------------------------------------------- |
|`matrix_postgres_backup_enabled`|`false`|Set to true to use [docker-postgres-backup-local](https://github.com/prodrigestivill/docker-postgres-backup-local) to create automatic database backups|
|`matrix_postgres_backup_schedule`| `'@daily'` |Cron-schedule specifying the interval between postgres backups.|
|`matrix_postgres_backup_keep_days`|`7`|Number of daily backups to keep|
|`matrix_postgres_backup_keep_weeks`|`4`|Number of weekly backups to keep|
|`matrix_postgres_backup_keep_months`|`12`|Number of monthly backups to keep|
|`matrix_postgres_backup_path` | `"{{ matrix_base_data_path }}/postgres-backup"` | Storagepath for the database backups|


## Installing

After configuring the playbook, run the [installation](installing.md) command again:

```
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```
