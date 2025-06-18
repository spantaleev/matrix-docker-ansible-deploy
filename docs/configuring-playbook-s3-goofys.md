<!--
SPDX-FileCopyrightText: 2022 Slavi Pantaleev
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Storing Synapse media files on Amazon S3 with Goofys (optional)

The playbook can install and configure [Goofys](https://github.com/kahing/goofys) for you.

Goofys makes it possible to store Synapse's content repository (`media_store`) files on Amazon S3 (or other S3-compatible service) object storage.

See the project's [documentation](https://github.com/kahing/goofys/blob/master/README.md) to learn what it does and why it might be useful to you.

**Note**: as performance of a Goofys-backed media store may not be ideal, you may wish to use [synapse-s3-storage-provider](configuring-playbook-synapse-s3-storage-provider.md) instead, another (and better performing) way to mount a S3 bucket for Synapse.

If you'd like to move your locally-stored media store data to Amazon S3 (or another S3-compatible object store), you can refer our migration instructions below.

## Adjusting the playbook configuration

After [creating the S3 bucket and configuring it](configuring-playbook-s3.md#bucket-creation-and-security-configuration), add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file (adapt to your needs):

```yaml
matrix_s3_media_store_enabled: true
matrix_s3_media_store_bucket_name: "your-bucket-name"
matrix_s3_media_store_aws_access_key: "access-key-goes-here"
matrix_s3_media_store_aws_secret_key: "secret-key-goes-here"
matrix_s3_media_store_region: "eu-central-1"
```

You can use any S3-compatible object store by **additionally** configuring these variables:

```yaml
matrix_s3_media_store_custom_endpoint_enabled: true
matrix_s3_media_store_custom_endpoint: "https://your-custom-endpoint"
```

If you have local media store files and wish to migrate to Backblaze B2 subsequently, follow our [migration guide to Backblaze B2](#migrating-to-backblaze-b2) below instead of applying this configuration as-is.

## Migrating from local filesystem storage to S3

It's a good idea to [make a complete server backup](faq.md#how-do-i-back-up-the-data-on-my-server) before migrating your local media store to an S3-backed one.

After making the backup, follow one of the guides below for a migration path from a locally-stored media store to one stored on S3-compatible storage:

- [Migrating to any S3-compatible storage (universal, but likely slow)](#migrating-to-any-s3-compatible-storage-universal-but-likely-slow)
- [Migrating to Backblaze B2](#migrating-to-backblaze-b2)

### Migrating to any S3-compatible storage (universal, but likely slow)

1. Proceed with the steps below without stopping Matrix services

2. Start by adding the base S3 configuration in your `vars.yml` file (seen above, may be different depending on the S3 provider of your choice)

3. In addition to the base configuration you see above, add this to your `vars.yml` file:

    ```yaml
    matrix_s3_media_store_path: /matrix/s3-media-store
    ```

    This enables S3 support, but mounts the S3 storage bucket to `/matrix/s3-media-store` without hooking it to your homeserver yet. Your homeserver will still continue using your local filesystem for its media store.

4. Run the playbook to apply the changes: `ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start`

5. Do an **initial sync of your files** by running this **on the server** (it may take a very long time):

    ```sh
    sudo -u matrix -- rsync --size-only --ignore-existing -avr /matrix/synapse/storage/media-store/. /matrix/s3-media-store/.
    ```

    You may need to install `rsync` manually.

6. Stop all Matrix services (`ansible-playbook -i inventory/hosts setup.yml --tags=stop`)

7. Start the S3 service by running this **on the server**: `systemctl start matrix-goofys`

8. Sync the files again by re-running the `rsync` command you see in step #5

9. Stop the S3 service by running this **on the server**: `systemctl stop matrix-goofys`

10. Get the old media store out of the way by running this command on the server:

    ```sh
    mv /matrix/synapse/storage/media-store /matrix/synapse/storage/media-store-local-backup
    ```

11. Remove the `matrix_s3_media_store_path` configuration from your `vars.yml` file (undoing step #3 above)

12. Run the playbook: `ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start`

13. You're done! Verify that loading existing (old) media files works and that you can upload new ones.

14. When confident that it all works, get rid of the local media store directory: `rm -rf /matrix/synapse/storage/media-store-local-backup`

### Migrating to Backblaze B2

1. While all Matrix services are running, run the following command on the server:

    (you need to adjust the 3 `--env` line below with your own data)

    ```sh
    docker run -it --rm -w /work \
    --env='B2_KEY_ID=YOUR_KEY_GOES_HERE' \
    --env='B2_KEY_SECRET=YOUR_SECRET_GOES_HERE' \
    --env='B2_BUCKET_NAME=YOUR_BUCKET_NAME_GOES_HERE' \
    --mount type=bind,src=/matrix/synapse/storage/media-store,dst=/work,ro \
    --entrypoint=/bin/sh \
    docker.io/tianon/backblaze-b2:3.6.0 \
    -c 'b2 authorize-account $B2_KEY_ID $B2_KEY_SECRET && b2 sync /work b2://$B2_BUCKET_NAME --skipNewer'
    ```

    This is some initial file sync, which may take a very long time.

2. Stop all Matrix services (`ansible-playbook -i inventory/hosts setup.yml --tags=stop`)

3. Run the command from step #1 again.

    Doing this will sync any new files that may have been created locally in the meantime.

    Now that Matrix services aren't running, we're sure to get Backblaze B2 and your local media store fully in sync.

4. Get the old media store out of the way by running this command on the server:

    ```sh
    mv /matrix/synapse/storage/media-store /matrix/synapse/storage/media-store-local-backup
    ```

5. Put the [Backblaze B2 settings](configuring-playbook-s3.md#backblaze-b2) in your `vars.yml` file

6. Run the playbook: `ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start`

7. You're done! Verify that loading existing (old) media files works and that you can upload new ones.

8. When confident that it all works, get rid of the local media store directory: `rm -rf /matrix/synapse/storage/media-store-local-backup`

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-goofys`.
