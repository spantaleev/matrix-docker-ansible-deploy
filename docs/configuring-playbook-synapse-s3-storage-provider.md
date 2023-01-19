# Storing Synapse media files on Amazon S3 with synapse-s3-storage-provider (optional)

If you'd like to store Synapse's content repository (`media_store`) files on Amazon S3 (or other S3-compatible service),
you can use the [synapse-s3-storage-provider](https://github.com/matrix-org/synapse-s3-storage-provider) media provider module for Synapse.

An alternative (which has worse performance) is to use [Goofys to mount the S3 store to the local filesystem](configuring-playbook-s3-goofys.md).


## How it works?

Summarized writings here are inspired by [this article](https://quentin.dufour.io/blog/2021-09-14/matrix-synapse-s3-storage/).

The way media storage providers in Synapse work has some caveats:

- Synapse still continues to use locally-stored files (for creating thumbnails, serving files, etc)
- the media storage provider is just an extra storage mechanism (in addition to the local filesystem)
- all files are stored locally at first, and then copied to the media storage provider (either synchronously or asynchronously)
- if a file is not available on the local filesystem, it's pulled from a media storage provider

You may be thinking **if all files are stored locally as well, what's the point**?

You can run some scripts to delete the local files once in a while (which we do automatically by default - see [Periodically cleaning up the local filesystem](#periodically-cleaning-up-the-local-filesystem)), thus freeing up local disk space. If these files are needed in the future (for serving them to users, etc.), Synapse will pull them from the media storage provider on demand.

While you will need some local disk space around, it's only to accommodate usage, etc., and won't grow as large as your S3 store.


## Installing

After [creating the S3 bucket and configuring it](configuring-playbook-s3.md#bucket-creation-and-security-configuration), you can proceed to configure `s3-storage-provider` in your configuration file (`inventory/host_vars/matrix.<your-domain>/vars.yml`):

```yaml
matrix_synapse_ext_synapse_s3_storage_provider_enabled: true
matrix_synapse_ext_synapse_s3_storage_provider_config_bucket: your-bucket-name
matrix_synapse_ext_synapse_s3_storage_provider_config_region_name: some-region-name # e.g. eu-central-1
matrix_synapse_ext_synapse_s3_storage_provider_config_endpoint_url: https://s3.REGION_NAME.amazonaws.com # adjust this
matrix_synapse_ext_synapse_s3_storage_provider_config_access_key_id: access-key-goes-here
matrix_synapse_ext_synapse_s3_storage_provider_config_secret_access_key: secret-key-goes-here
matrix_synapse_ext_synapse_s3_storage_provider_config_storage_class: STANDARD # or STANDARD_IA, etc.

# For additional advanced settings, take a look at `roles/custom/matrix-synapse/defaults/main.yml`
```

If you have existing files in Synapse's media repository (`/matrix/synapse/media-store/..`):

- new files will start being stored both locally and on the S3 store
- the existing files will remain on the local filesystem only until [migrating them to the S3 store](#migrating-your-existing-media-files-to-the-s3-store)
- at some point (and periodically in the future), you can delete local files which have been uploaded to the S3 store already

Regardless of whether you need to [Migrate your existing files to the S3 store](#migrating-your-existing-media-files-to-the-s3-store) or not, make sure you've familiarized yourself with [How it works?](#how-it-works) above and [Periodically cleaning up the local filesystem](#periodically-cleaning-up-the-local-filesystem) below.


## Migrating your existing media files to the S3 store

Migrating your existing data can happen in multiple ways:

- [using the `s3_media_upload` script from `synapse-s3-storage-provider`](#using-the-s3_media_upload-script-from-synapse-s3-storage-provider) (very slow when dealing with lots of data)
- [using another tool in combination with `s3_media_upload`](#using-another-tool-in-combination-with-s3_media_upload) (quicker when dealing with lots of data)

### Using the `s3_media_upload` script from `synapse-s3-storage-provider`

Instead of using `s3_media_upload` directly, which is very slow and painful for an initial data migration, we recommend [using another tool in combination with `s3_media_upload`](#using-another-tool-in-combination-with-s3_media_upload).

To copy your existing files, SSH into the server and run `/matrix/synapse/ext/s3-storage-provider/bin/shell`.

This launches a Synapse container, which has access to the local media store, Postgres database, S3 store and has some convenient environment variables configured for you to use (`MEDIA_PATH`, `BUCKET`, `ENDPOINT`, `UPDATE_DB_DAYS`, etc).

Then use the following commands (`$` values come from environment variables - they're **not placeholders** that you need to substitute):

1. `s3_media_upload update-db $UPDATE_DB_DURATION` - create a local SQLite database (`cache.db`) with a list of media repository files (from the `synapse` Postgres database) eligible for operating on
  - `$UPDATE_DB_DURATION` is influenced by the `matrix_synapse_ext_synapse_s3_storage_provider_update_db_day_count` variable (defaults to `0`)
  - `$UPDATE_DB_DURATION` defaults to `0d` (0 days), which means **include files which haven't been accessed for more than 0 days** (that is, **all files will be included**).
2. `s3_media_upload check-deleted $MEDIA_PATH` - check whether files in the local cache still exist in the local media repository directory
3. `s3_media_upload upload $MEDIA_PATH $BUCKET --delete --storage-class $STORAGE_CLASS --endpoint-url $ENDPOINT` - uploads locally-stored files to S3 and deletes them from the local media repository directory

The `s3_media_upload upload` command may take a lot of time to complete.

Instead of running the above commands manually in the shell, you can also run the `/matrix/synapse/ext/s3-storage-provider/bin/migrate` script which will run the same commands automatically. We demonstrate how to do it manually, because:

- it's what the upstream project demonstrates and it teaches you how to use the `s3_media_upload` tool
- allows you to check and verify the output of each command, to catch mistakes
- includes progress bars and detailed output for each command
- allows you to easily interrupt slow-running commands, etc. (the `/matrix/synapse/ext/s3-storage-provider/bin/migrate` starts a container without interactive TTY support, so `Ctrl+C` may not work and you and require killing via `docker kill ..`)

### Using another tool in combination with `s3_media_upload`

To migrate your existing local data to S3, we recommend to:

- **first** use another tool ([`aws s3`](#copying-data-to-amazon-s3) or [`b2 sync`](#copying-data-to-backblaze-b2), etc.) to copy the local files to the S3 bucket

- **only then** [use the `s3_media_upload` tool to finish the migration](#using-the-s3_media_upload-script-from-synapse-s3-storage-provider) (this checks to ensure all files are uploaded and then deletes the local files)

#### Copying data to Amazon S3

To copy to AWS S3, start a container on the Matrix server like this:

```sh
docker run -it --rm \
-w /work \
--env-file=/matrix/synapse/ext/s3-storage-provider/env \
--mount type=bind,src=/matrix/synapse/storage/media-store,dst=/work,ro \
--entrypoint=/bin/sh \
docker.io/amazon/aws-cli:2.9.16 \
-c 'aws s3 sync /work/. s3://$BUCKET/'
```

#### Copying data to Backblaze B2

To copy to Backblaze B2, start a container on the Matrix server like this:

```sh
docker run -it --rm \
-w /work \
--env='B2_KEY_ID=YOUR_KEY_GOES_HERE' \
--env='B2_KEY_SECRET=YOUR_SECRET_GOES_HERE' \
--env='B2_BUCKET_NAME=YOUR_BUCKET_NAME_GOES_HERE' \
--mount type=bind,src=/matrix/synapse/storage/media-store,dst=/work,ro \
--entrypoint=/bin/sh \
docker.io/tianon/backblaze-b2:3.6.0 \
-c 'b2 authorize-account $B2_KEY_ID $B2_KEY_SECRET && b2 sync /work b2://$B2_BUCKET_NAME --skipNewer'
```

## Periodically cleaning up the local filesystem

As described in [How it works?](#how-it-works) above, when new media is uploaded to the Synapse homeserver, it's first stored locally and then also stored on the remote S3 storage.

By default, we periodically ensure that all local files are uploaded to S3 and are then removed from the local filesystem. This is done automatically using:

- the `/matrix/synapse/ext/s3-storage-provider/bin/migrate` script
- .. invoked via the `matrix-synapse-s3-storage-provider-migrate.service` service
- .. triggered by the `matrix-synapse-s3-storage-provider-migrate.timer` timer, every day at 05:00

So.. you don't need to perform any maintenance yourself.
