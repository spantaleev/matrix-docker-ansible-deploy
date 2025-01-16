# Setting up BorgBackup (optional)

The playbook can install and configure [BorgBackup](https://www.borgbackup.org/) (short: Borg) with [borgmatic](https://torsion.org/borgmatic/) for you.

BorgBackup is a deduplicating backup program with optional compression and encryption. That means your daily incremental backups can be stored in a fraction of the space and is safe whether you store it at home or on a cloud service.

## Prerequisites

### Set up a remote server for storing backups

You will need a remote server where BorgBackup will store the backups. There are hosted, BorgBackup compatible solutions available, such as [BorgBase](https://www.borgbase.com).

### Check the Postgres version

By default, if you're using the integrated Postgres database server (as opposed to [an external Postgres server](configuring-playbook-external-postgres.md)), backups with BorgBackup will also include dumps of your Postgres database.

Unless you disable the Postgres-backup support, make sure that the Postgres version of your homeserver's database is compatible with borgmatic. You can check the compatible versions [here](https://github.com/mother-of-all-self-hosting/ansible-role-backup_borg/blob/main/defaults/main.yml).

An alternative solution for backing up the Postgres database is [postgres backup](configuring-playbook-postgres-backup.md). If you decide to go with another solution, you can disable Postgres-backup support for BorgBackup using the `backup_borg_postgresql_enabled` variable.

### Create a new SSH key

Run the command below on any machine to create a new SSH key:

```sh
ssh-keygen -t ed25519 -N '' -f matrix-borg-backup -C matrix
```

You don't need to place the key in the `.ssh` folder.

### Add the public key

Next, add the **public** part of this SSH key (the `matrix-borg-backup.pub` file) to your BorgBackup provider/server.

If you are using a hosted solution, follow their instructions. If you have your own server, copy the key to it with the command like below:

```sh
# Example to append the new PUBKEY contents, where:
# - PUBKEY is path to the public key
# - USER is a ssh user on a provider / server
# - HOST is a ssh host of a provider / server
cat PUBKEY | ssh USER@HOST 'dd of=.ssh/authorized_keys oflag=append conv=notrunc'
```

The **private** key needs to be added to `backup_borg_ssh_key_private` on your `inventory/host_vars/matrix.example.com/vars.yml` file as below.

## Adjusting the playbook configuration

To enable BorgBackup, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
backup_borg_enabled: true

# Set the repository location, where:
# - USER is a ssh user on a provider / server
# - HOST is a ssh host of a provider / server
# - REPO is a BorgBackup repository name
backup_borg_location_repositories:
 - ssh://USER@HOST/./REPO

# Generate a strong password used for encrypting backups. You can create one with a command like `pwgen -s 64 1`.
backup_borg_storage_encryption_passphrase: "PASSPHRASE"

# Add the content of the **private** part of the SSH key you have created.
# Note: the whole key (all of its belonging lines) under the variable needs to be indented with 2 spaces.
backup_borg_ssh_key_private: |
  -----BEGIN OPENSSH PRIVATE KEY-----
  TG9yZW0gaXBzdW0gZG9sb3Igc2l0IGFtZXQsIGNvbnNlY3RldHVyIGFkaXBpc2NpbmcgZW
  xpdCwgc2VkIGRvIGVpdXNtb2QgdGVtcG9yIGluY2lkaWR1bnQgdXQgbGFib3JlIGV0IGRv
  bG9yZSBtYWduYSBhbGlxdWEuIFV0IGVuaW0gYWQgbWluaW0gdmVuaWFtLCBxdWlzIG5vc3
  RydWQgZXhlcmNpdGF0aW9uIHVsbGFtY28gbGFib3JpcyBuaXNpIHV0IGFsaXF1aXAgZXgg
  ZWEgY29tbW9kbyBjb25zZXF1YXQuIA==
  -----END OPENSSH PRIVATE KEY-----
```

**Note**: `REPO` will be initialized on backup start, for example: `matrix`. See [Remote repositories](https://borgbackup.readthedocs.io/en/stable/usage/general.html#repository-urls) for the syntax.

### Set backup archive name (optional)

You can specify the backup archive name format. To set it, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
backup_borg_storage_archive_name_format: matrix-{now:%Y-%m-%d-%H%M%S}
```

### Configure retention policy (optional)

It is also possible to configure a retention strategy. To configure it, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
backup_borg_retention_keep_hourly: 0
backup_borg_retention_keep_daily: 7
backup_borg_retention_keep_weekly: 4
backup_borg_retention_keep_monthly: 12
backup_borg_retention_keep_yearly: 2
```

### Edit the backup schedule (optional)

By default the backup will run 4 a.m. every day based on the `backup_borg_schedule` variable. It is defined in the format of systemd timer calendar.

To edit the schedule, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
backup_borg_schedule: "*-*-* 04:00:00"
```

**Note**: the actual job may run with a delay. See `backup_borg_schedule_randomized_delay_sec` [here](https://github.com/mother-of-all-self-hosting/ansible-role-backup_borg/blob/f5d5b473d48c6504be10b3d946255ef5c186c2a6/defaults/main.yml#L50) for its default value.

### Set include and/or exclude directories (optional)

`backup_borg_location_source_directories` defines the list of directories to back up. It's set to `{{ matrix_base_data_path }}` by default, which is the base directory for every service's data, such as Synapse, Postgres and the bridges.

You might also want to exclude certain directories or file patterns from the backup using the `backup_borg_location_exclude_patterns` variable.

### Extending the configuration

There are some additional things you may wish to configure about the component.

Take a look at:

- [backup_borg role](https://github.com/mother-of-all-self-hosting/ansible-role-backup_borg)'s [`defaults/main.yml`](https://github.com/mother-of-all-self-hosting/ansible-role-backup_borg/blob/main/defaults/main.yml) for some variables that you can customize via your `vars.yml` file. You can override settings (even those that don't have dedicated playbook variables) using the `backup_borg_configuration_extension_yaml` variable

## Installing

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

## Manually start a backup

Sometimes it can be helpful to run the backup as you'd like, avoiding to wait until 4 a.m., like when you test your configuration.

If you want to run the backup immediately, log in to the server with SSH and run `systemctl start matrix-backup-borg`.

This will not return until the backup is done, so it can possibly take a long time. Consider using [tmux](https://en.wikipedia.org/wiki/Tmux) if your SSH connection is unstable.
