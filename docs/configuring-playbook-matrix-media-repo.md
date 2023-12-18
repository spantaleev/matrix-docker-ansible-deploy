# Setting up matrix-media-repo (optional)

[matrix-media-repo](https://docs.t2bot.io/matrix-media-repo/) (often abbreviated "MMR") is a highly customizable multi-domain media repository for Matrix. Intended for medium to large environments consisting of several homeservers, this media repo de-duplicates media (including remote media) while being fully compliant with the specification.

Smaller/individual homeservers can still make use of this project's features, though it may be difficult to set up or have higher than expected resource consumption. Please do your research before deploying this as this project may not be useful for your environment.

For a simpler alternative (which allows you to offload your media repository storage to S3, etc.), you can [configure S3 storage](configuring-playbook-s3.md) instead of setting up matrix-media-repo.

| **Table of Contents**                                                                       |
| :------------------------------------------------------------------------------------------ |
| [Quickstart](#quickstart)                                                                   |
| [Additional configuration options](#configuring-the-media-repo)                             |
| [Importing data from an existing media store](#importing-data-from-an-existing-media-store) |

## Quickstart

Add the following configuration to your `inventory/host_vars/matrix.DOMAIN/vars.yml` file and [re-run the installation process](./installing.md) for the playbook:

```yaml
matrix_media_repo_enabled: true

# (optional) Turned off by default
# matrix_media_repo_metrics_enabled: true
```

The repo is pre-configured for integrating with the Postgres database, NGINX proxy and [Prometheus/Grafana](configuring-playbook-prometheus-grafana.md) (if metrics enabled) from this playbook for all the available homeserver roles. When the media repo is enabled, other media store roles should be disabled (if using Synapse with other media store roles).

By default, the media-repo will use the local filesystem for data storage. Additional options include `s3` and `IPFS` (experimental). Access token caching is also enabled by default since the logout endpoints are proxied through the media repo.

## Configuring the media-repo

Additional common configuration options:
```yaml

# The postgres database pooling options

# The maximum number of connects to hold open. More of these allow for more concurrent
# processes to happen.
matrix_media_repo_database_max_connections: 25

# The maximum number of connects to leave idle. More of these reduces the time it takes
# to serve requests in low-traffic scenarios.
matrix_media_repo_database_max_idle_connections: 5

# These users have full access to the administrative functions of the media repository.
# See docs/admin.md for information on what these people can do. They must belong to one of the
# configured homeservers above.
# matrix_media_repo_admins: [
#   "@your_username:example.org"
# ]

matrix_media_repo_admins: []

# Datastores can be split into many areas when handling uploads. Media is still de-duplicated
# across all datastores (local content which duplicates remote content will re-use the remote
# content's location). This option is useful if your datastore is becoming very large, or if
# you want faster storage for a particular kind of media.
#
# To disable this datastore, making it readonly, specify `forKinds: []`.
#
# The kinds available are:
#   thumbnails    - Used to store thumbnails of media (local and remote).
#   remote_media  - Original copies of remote media (servers not configured by this repo).
#   local_media   - Original uploads for local media.
#   archives      - Archives of content (GDPR and similar requests).
matrix_media_repo_datastore_file_for_kinds: ["thumbnails", "remote_media", "local_media", "archives"]
matrix_media_repo_datastore_s3_for_kinds: []

# The s3 uploader needs a temporary location to buffer files to reduce memory usage on
# small file uploads. If the file size is unknown, the file is written to this location
# before being uploaded to s3 (then the file is deleted). If you aren't concerned about
# memory usage, set this to an empty string.
matrix_media_repo_datastore_s3_opts_temp_path: ""
matrix_media_repo_datastore_s3_opts_endpoint: "sfo2.digitaloceanspaces.com"
matrix_media_repo_datastore_s3_opts_access_key_id: ""
matrix_media_repo_datastore_s3_opts_access_secret: ""
matrix_media_repo_datastore_s3_opts_ssl: true
matrix_media_repo_datastore_s3_opts_bucket_name: "your-media-bucket"

# An optional region for where this S3 endpoint is located. Typically not needed, though
# some providers will need this (like Scaleway). Uncomment to use.
# matrix_media_repo_datastore_s3_opts_region: "sfo2"

# An optional storage class for tuning how the media is stored at s3.
# See https://aws.amazon.com/s3/storage-classes/ for details; uncomment to use.
# matrix_media_repo_datastore_s3_opts_storage_class: "STANDARD"

```

Full list of configuration options with documentation can be found in [`roles/custom/matrix-media-repo/defaults/main.yml`](https://github.com/spantaleev/matrix-docker-ansible-deploy/blob/master/roles/custom/matrix-media-repo/defaults/main.yml)

## Importing data from an existing media store

If you want to add this repo to an existing homeserver managed by the playbook, you will need to import existing media into MMR's database or you will lose access to older media while it is active. MMR versions up to `v1.3.3` only support importing from Synapse, but newer versions (at time of writing: only `latest`) also support importing from Dendrite.

**Before importing**: ensure you have an initial matrix-media-repo deployment by following the [quickstart](#quickstart) guide above

Depending on the homeserver implementation yu're using (Synapse, Dendrite), you'll need to use a different import tool (part of matrix-media-repo) and point it to the homeserver's database.

### Importing data from the Synapse media store

To import the Synapse media store, you're supposed to invoke the `import_synapse` tool which is part of the matrix-media-repo container image. Your Synapse database is called `synapse` by default, unless you've changed it by modifying `matrix_synapse_database_database`.

This guide here is adapted from the [upstream documentation about the import_synapse script](https://github.com/turt2live/matrix-media-repo#importing-media-from-synapse).

Run the following command on the server (after replacing `devture_postgres_connection_password` in it with the value found in your `vars.yml` file):

```sh
docker exec -it matrix-media-repo \
    /usr/local/bin/import_synapse \
        -dbName synapse \
        -dbHost matrix-postgres \
        -dbPort 5432 \
        -dbUsername matrix \
        -dbPassword devture_postgres_connection_password
```

Enter `1` for the Machine ID when prompted (you are not doing any horizontal scaling) unless you know what you're doing.

This should output a `msg="Import completed"` when finished successfully!

### Importing data from the Dendrite media store

If you're using the [Dendrite](configuring-playbook-dendrite.md) homeserver instead of the default for this playbook (Synapse), follow this importing guide here.

To import the Dendrite media store, you're supposed to invoke the `import_dendrite` tool which is part of the matrix-media-repo container image. Your Dendrite database is called `dendrite_mediaapi` by default, unless you've changed it by modifying `matrix_dendrite_media_api_database`.

Run the following command on the server (after replacing `devture_postgres_connection_password` in it with the value found in your `vars.yml` file):

```sh
docker exec -it matrix-media-repo \
    /usr/local/bin/import_dendrite \
        -dbName dendrite_mediaapi \
        -dbHost matrix-postgres \
        -dbPort 5432 \
        -dbUsername matrix \
        -dbPassword devture_postgres_connection_password
```

Enter `1` for the Machine ID when prompted (you are not doing any horizontal scaling) unless you know what you're doing.

This should output a `msg="Import completed"` when finished successfully!
