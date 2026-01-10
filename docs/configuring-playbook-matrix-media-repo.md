<!--
SPDX-FileCopyrightText: 2023 - 2024 Michael Hollister
SPDX-FileCopyrightText: 2023 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2023 MDAD project contributors
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Storing Matrix media files using matrix-media-repo (optional)

The playbook can install and configure [matrix-media-repo](https://docs.t2bot.io/matrix-media-repo/) (often abbreviated "MMR") for you.

MMR is a highly customizable multi-domain media repository for Matrix. Intended for medium to large environments consisting of several homeservers, this media repo de-duplicates media (including remote media) while being fully compliant with the specification.

**Notes**:
- If MMR is enabled, other media store roles should be disabled (if using Synapse with other media store roles).
- Smaller/individual homeservers can still make use of this project's features, though it may be difficult to set up or have higher than expected resource consumption. Please do your research before deploying this as this project may not be useful for your environment.
- For a simpler alternative (which allows you to offload your media repository storage to S3, etc.), you can [configure S3 storage](configuring-playbook-s3.md) instead of setting up matrix-media-repo.

## Adjusting the playbook configuration

To enable matrix-media-repo, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_media_repo_enabled: true
```

By default, the media-repo will use the local filesystem for data storage. You can alternatively use a `s3` cloud backend as well. Access token caching is also enabled by default since the logout endpoints are proxied through the media repo.

### Enable metrics

The playbook can enable and configure the metrics of the service for you.

Metrics are **only enabled by default** if the builtin [Prometheus](configuring-playbook-prometheus-grafana.md) is enabled (by default, Prometheus isn't enabled). If so, metrics will automatically be collected by Prometheus and made available in Grafana. You will, however, need to set up your own Dashboard for displaying them.

To enable the metrics, add the following configuration to your `vars.yml` file:

```yaml
# Expose metrics (locally, on the container network).
matrix_media_repo_metrics_enabled: true
```

**To collect metrics from an external Prometheus server**, besides enabling metrics as described above, you will also need to enable metrics exposure on `https://matrix.example.com/metrics/matrix-media-repo` by adding the following configuration to your `vars.yml` file:

```yaml
matrix_media_repo_metrics_proxying_enabled: true
```

By default metrics are exposed publicly **without** password-protection. To password-protect the metrics with dedicated credentials, add the following configuration to your `vars.yml` file:

```yaml
matrix_media_repo_container_labels_traefik_metrics_middleware_basic_auth_enabled: true
matrix_media_repo_container_labels_traefik_metrics_middleware_basic_auth_users: ''
```

To `matrix_media_repo_container_labels_traefik_metrics_middleware_basic_auth_users`, set the Basic Authentication credentials (raw `htpasswd` file content) used to protect the endpoint. See https://doc.traefik.io/traefik/middlewares/http/basicauth/#users for details about it.

**Note**: alternatively, you can use `matrix_metrics_exposure_enabled` to expose all services on this `/metrics/*` feature, and you can use `matrix_metrics_exposure_http_basic_auth_enabled` and `matrix_metrics_exposure_http_basic_auth_users` to password-protect the metrics of them. See [this section](configuring-playbook-prometheus-grafana.md#collecting-metrics-to-an-external-prometheus-server) for more information.

#### Enable Grafana (optional)

Probably you wish to enable Grafana along with Prometheus for generating graphs of the metrics.

To enable Grafana, see [this section](configuring-playbook-prometheus-grafana.md#adjusting-the-playbook-configuration-grafana) for instructions.

### Extending the configuration

There are some additional things you may wish to configure about the component.

Take a look at:

- `roles/custom/matrix-media-repo/defaults/main.yml` for some variables that you can customize via your `vars.yml` file

Here is a list of additional common configuration options:

```yaml
# The Postgres database pooling options

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
#   "@alice:example.org"
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
#   thumbnails    — Used to store thumbnails of media (local and remote).
#   remote_media  — Original copies of remote media (servers not configured by this repo).
#   local_media   — Original uploads for local media.
#   archives      — Archives of content (GDPR and similar requests).
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

## Signing Keys

Authenticated media endpoints ([MSC3916](https://github.com/matrix-org/matrix-spec-proposals/pull/3916)) requires MMR to have a configured signing key to authorize outbound federation requests. Additionally, the signing key must be merged with your homeserver's signing key file.

The playbook default is to generate a MMR signing key when invoking the setup role and merge it with your homeserver if you are using Synapse or Dendrite. This can be disabled if desired by setting the option in your inventory:

```yaml
matrix_media_repo_generate_signing_key: false
```

If you wish to manually generate the signing key and merge it with your homeserver's signing key file, see https://docs.t2bot.io/matrix-media-repo/v1.3.5/installation/signing-key/ for more details.

**Note that if you uninstall MMR from the playbook, it will not remove the old MMR signing key from your homeserver's signing key file. You will have to remove it manually.**

### Key backup and revoking

Since your homeserver signing key file is modified by the playbook, a backup will be created in `HOMESERVER_DIR/config/example.com.signing.key.backup`. If you need to remove/revoke old keys, you can restore from this backup or remove the MMR key ID from your `example.com.signing.key` file.

Additionally, its recommended after revoking a signing key to update your homeserver config file (`old_signing_keys` field for Synapse and `old_private_keys` for Dendrite). See your homeserver config file for further documentation on how to populate the field.

## Importing data from an existing media store

If you want to add this repo to an existing homeserver managed by the playbook, you will need to import existing media into MMR's database or you will lose access to older media while it is active. MMR versions up to `v1.3.3` only support importing from Synapse, but newer versions (at time of writing: only `latest`) also support importing from Dendrite.

**Before importing**: ensure you have an initial matrix-media-repo deployment by following the [quickstart](#quickstart) guide above

Depending on the homeserver implementation yu're using (Synapse, Dendrite), you'll need to use a different import tool (part of matrix-media-repo) and point it to the homeserver's database.

### Importing data from the Synapse media store

To import the Synapse media store, you're supposed to invoke the `import_synapse` tool which is part of the matrix-media-repo container image. Your Synapse database is called `synapse` by default, unless you've changed it by modifying `matrix_synapse_database_database`.

This guide here is adapted from the [upstream documentation about the import_synapse script](https://github.com/turt2live/matrix-media-repo#importing-media-from-synapse).

Run the following command on the server (after replacing `postgres_connection_password` in it with the value found in your `vars.yml` file):

```sh
docker exec -it matrix-media-repo \
    /usr/local/bin/import_synapse \
        -dbName synapse \
        -dbHost matrix-postgres \
        -dbPort 5432 \
        -dbUsername matrix \
        -dbPassword postgres_connection_password
```

Enter `1` for the Machine ID when prompted (you are not doing any horizontal scaling) unless you know what you're doing.

This should output a `msg="Import completed"` when finished successfully!

### Importing data from the Dendrite media store

If you're using the [Dendrite](configuring-playbook-dendrite.md) homeserver instead of the default for this playbook (Synapse), follow this importing guide here.

To import the Dendrite media store, you're supposed to invoke the `import_dendrite` tool which is part of the matrix-media-repo container image. Your Dendrite database is called `dendrite_mediaapi` by default, unless you've changed it by modifying `matrix_dendrite_media_api_database`.

Run the following command on the server (after replacing `postgres_connection_password` in it with the value found in your `vars.yml` file):

```sh
docker exec -it matrix-media-repo \
    /usr/local/bin/import_dendrite \
        -dbName dendrite_mediaapi \
        -dbHost matrix-postgres \
        -dbPort 5432 \
        -dbUsername matrix \
        -dbPassword postgres_connection_password
```

Enter `1` for the Machine ID when prompted (you are not doing any horizontal scaling) unless you know what you're doing.

This should output a `msg="Import completed"` when finished successfully!

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-media-repo`.

### Increase logging verbosity

If you want to turn on sentry's built-in debugging, add the following configuration to your `vars.yml` file and re-run the playbook:

```yaml
matrix_media_repo_sentry_debug: true
```
