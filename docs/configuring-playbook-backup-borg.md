# Setting up BorgBackup (optional)

The playbook can install and configure [BorgBackup](https://www.borgbackup.org/) (short: Borg) with [borgmatic](https://torsion.org/borgmatic/) for you.

BorgBackup is a deduplicating backup program with optional compression and encryption. That means your daily incremental backups can be stored in a fraction of the space and is safe whether you store it at home or on a cloud service.

You will need a remote server where BorgBackup will store the backups. There are hosted, BorgBackup compatible solutions available, such as [BorgBase](https://www.borgbase.com).

The backup will run based on `backup_borg_schedule` var (systemd timer calendar), default: 4am every day.

By default, if you're using the integrated Postgres database server (as opposed to [an external Postgres server](configuring-playbook-external-postgres.md)), backups with BorgBackup will also include dumps of your Postgres database. An alternative solution for backing up the Postgres database is [postgres backup](configuring-playbook-postgres-backup.md). If you decide to go with another solution, you can disable Postgres-backup support for BorgBackup using the `backup_borg_postgresql_enabled` variable.

**Note**: the component is not managed by this repository but its [own repository](https://github.com/mother-of-all-self-hosting/ansible-role-backup_borg).

## Prerequisites

1. If you do not disable Postgres-backup support, make sure that the Postgres version of your homeserver's database is compatible with borgmatic.

2. Create a new SSH key:

    ```sh
    ssh-keygen -t ed25519 -N '' -f matrix-borg-backup -C matrix
    ```

    This can be done on any machine and you don't need to place the key in the `.ssh` folder. It will be added to the Ansible config later.

3. Add the **public** part of this SSH key (the `matrix-borg-backup.pub` file) to your BorgBackup provider/server:

    If you plan to use a hosted solution, follow their instructions. If you have your own server, copy the key over:

    ```sh
    # example to append the new PUBKEY contents, where:
    # PUBKEY is path to the public key,
    # USER is a ssh user on a provider / server
    # HOST is a ssh host of a provider / server
    cat PUBKEY | ssh USER@HOST 'dd of=.ssh/authorized_keys oflag=append conv=notrunc'
    ```

## Adjusting the playbook configuration

Minimal working configuration (`inventory/host_vars/matrix.example.com/vars.yml`) to enable BorgBackup:

```yaml
backup_borg_enabled: true
backup_borg_location_repositories:
 - ssh://USER@HOST/./REPO
backup_borg_storage_encryption_passphrase: "PASSPHRASE"
backup_borg_ssh_key_private: |
  -----BEGIN OPENSSH PRIVATE KEY-----
  TG9yZW0gaXBzdW0gZG9sb3Igc2l0IGFtZXQsIGNvbnNlY3RldHVyIGFkaXBpc2NpbmcgZW
  xpdCwgc2VkIGRvIGVpdXNtb2QgdGVtcG9yIGluY2lkaWR1bnQgdXQgbGFib3JlIGV0IGRv
  bG9yZSBtYWduYSBhbGlxdWEuIFV0IGVuaW0gYWQgbWluaW0gdmVuaWFtLCBxdWlzIG5vc3
  RydWQgZXhlcmNpdGF0aW9uIHVsbGFtY28gbGFib3JpcyBuaXNpIHV0IGFsaXF1aXAgZXgg
  ZWEgY29tbW9kbyBjb25zZXF1YXQuIA==
  -----END OPENSSH PRIVATE KEY-----
```

where:

* USER - SSH user of a provider/server
* HOST - SSH host of a provider/server
* REPO - BorgBackup repository name, it will be initialized on backup start, eg: `matrix`, regarding Syntax see [Remote repositories](https://borgbackup.readthedocs.io/en/stable/usage/general.html#repository-urls)
* PASSPHRASE - passphrase used for encrypting backups, you may generate it with `pwgen -s 64 1` or use any password manager
* PRIVATE KEY - the content of the **private** part of the SSH key you created before. The whole key (all of its belonging lines) under `backup_borg_ssh_key_private` needs to be indented with 2 spaces

To backup without encryption, add `backup_borg_encryption: 'none'` to your vars. This will also enable the `backup_borg_unknown_unencrypted_repo_access_is_ok` variable.

`backup_borg_location_source_directories` defines the list of directories to back up: it's set to `{{ matrix_base_data_path }}` by default, which is the base directory for every service's data, such as Synapse, Postgres and the bridges. You might want to exclude certain directories or file patterns from the backup using the `backup_borg_location_exclude_patterns` variable.

Check the [backup_borg role](https://github.com/mother-of-all-self-hosting/ansible-role-backup_borg)'s [defaults/main.yml](https://github.com/mother-of-all-self-hosting/ansible-role-backup_borg/blob/main/defaults/main.yml) file for the full list of available options.

## Installing

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with `just` program are also available: `just run-tags install-all,start` or `just run-tags setup-all,start`

`just run-tags install-all,start` is useful for maintaining your setup quickly when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just run-tags setup-all,start`, or these components will still remain installed. For more information about `just` shortcuts, take a look at this page: [Running `just` commands](just.md)

## Manually start a backup

For testing your setup it can be helpful to not wait until 4am. If you want to run the backup immediately, log onto the server and run `systemctl start matrix-backup-borg`. This will not return until the backup is done, so possibly a long time. Consider using [tmux](https://en.wikipedia.org/wiki/Tmux) if your SSH connection is unstable.
