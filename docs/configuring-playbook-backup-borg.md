# Setting up borg backup (optional)

The playbook can install and configure [borgbackup](https://www.borgbackup.org/) with [borgmatic](https://torsion.org/borgmatic/) for you.
BorgBackup is a deduplicating backup program with optional compression and encryption.
That means your daily incremental backups can be stored in a fraction of the space and is safe whether you store it at home or on a cloud service.

You will need a remote server where borg will store the backups. There are hosted, borg compatible solutions available, such as [BorgBase](https://www.borgbase.com).

The backup will run based on `matrix_backup_borg_schedule` var (systemd timer calendar), default: 4am every day.

By default, if you're using the integrated Postgres database server (as opposed to [an external Postgres server](configuring-playbook-external-postgres.md)), Borg backups will also include dumps of your Postgres database. An alternative solution for backing up the Postgres database is [postgres backup](configuring-playbook-postgres-backup.md). If you decide to go with another solution, you can disable Postgres-backup support for Borg using the `matrix_backup_borg_postgresql_enabled` variable.


## Prerequisites

1. Create a new SSH key:

```bash
ssh-keygen -t ed25519 -N '' -f matrix-borg-backup -C matrix
```

This can be done on any machine and you don't need to place the key in the `.ssh` folder. It will be added to the Ansible config later.

2. Add the **public** part of this SSH key (the `matrix-borg-backup.pub` file) to your borg provider/server:

If you plan to use a hosted solution, follow their instructions. If you have your own server, copy the key over:

```bash
# example to append the new PUBKEY contents, where:
# PUBKEY is path to the public key,
# USER is a ssh user on a provider / server
# HOST is a ssh host of a provider / server
cat PUBKEY | ssh USER@HOST 'dd of=.ssh/authorized_keys oflag=append conv=notrunc'
```

## Adjusting the playbook configuration

Minimal working configuration (`inventory/host_vars/matrix.DOMAIN/vars.yml`) to enable borg backup:

```yaml
matrix_backup_borg_enabled: true
matrix_backup_borg_location_repositories:
 - USER@HOST:REPO
matrix_backup_borg_storage_encryption_passphrase: "PASSPHRASE"
matrix_backup_borg_ssh_key_private: |
	PRIVATE KEY
```

where:

* USER - SSH user of a provider/server
* HOST - SSH host of a provider/server
* REPO - borg repository name, it will be initialized on backup start, eg: `matrix`
* PASSPHRASE - passphrase used for encrypting backups, you may generate it with `pwgen -s 64 1` or use any password manager
* PRIVATE KEY - the content of the **private** part of the SSH key you created before

To backup without encryption, add `matrix_backup_borg_encryption: 'none'` to your vars. This will also enable the `matrix_backup_borg_unknown_unencrypted_repo_access_is_ok` variable.

`matrix_backup_borg_location_source_directories` defines the list of directories to back up: it's set to `{{ matrix_base_data_path }}` by default, which is the base directory for every service's data, such as Synapse, Postgres and the bridges. You might want to exclude certain directories or file patterns from the backup using the `matrix_backup_borg_location_exclude_patterns` variable.

Check the `roles/matrix-backup-borg/defaults/main.yml` file for the full list of available options.

## Installing

After configuring the playbook, run the [installation](installing.md) command again:

```
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```
