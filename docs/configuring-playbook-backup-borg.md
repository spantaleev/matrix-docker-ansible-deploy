# Setting up borg backup (optional)

The playbook can install and configure [borgbackup](https://www.borgbackup.org/) with [borgmatic](https://torsion.org/borgmatic/) for you.
BorgBackup is a deduplicating backup program with optional compression and encryption.
That means your daily incremental backups can be stored in a fraction of the space and is safe whether you store it at home or on a cloud service.

The backup will run based on `matrix_backup_borg_schedule` var (systemd timer calendar), default: 4am every day

## Prerequisites

1. Create ssh key on any machine:

```bash
ssh-keygen -t ed25519 -N '' -f matrix-borg-backup -C matrix
```

2. Add public part of that ssh key to your borg provider / server:

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

* USER - ssh user of a provider / server
* HOST - ssh host of a provider / server
* REPO - borg repository name, it will be initialized on backup start, eg: `matrix`
* PASSPHRASE - super-secret borg passphrase, you may generate it with `pwgen -s 64 1` or use any password manager
* PRIVATE KEY - the content of the public part of the ssh key you created before

Check the `roles/matrix-backup-borg/defaults/main.yml` for the full list of available options

## Installing

After configuring the playbook, run the [installation](installing.md) command again:

```
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```
