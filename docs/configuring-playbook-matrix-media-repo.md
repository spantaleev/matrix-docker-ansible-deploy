# Setting up matrix-media-repo (optional)

[matrix-media-repo](https://docs.t2bot.io/matrix-media-repo/) is a highly customizable multi-domain media repository for Matrix. Intended for medium to large environments consisting of several homeservers, this media repo de-duplicates media (including remote media) while being fully compliant with the specification.

Smaller/individual homeservers can still make use of this project's features, though it may be difficult to set up or have higher than expected resource consumption. Please do your research before deploying this as this project may not be useful for your environment.

For a simpler alternative (which allows you to offload your media repository storage to S3, etc.), you can [configure S3 storage](configuring-playbook-s3.md) instead of setting up matrix-media-repo.

## Quickstart

Add the following configuration to your `inventory/host_vars/matrix.DOMAIN/vars.yml` file:

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
# See https://github.com/turt2live/matrix-media-repo/blob/release-v1.2.8/docs/admin.md for information on what these people can do. They must belong to one of the
# configured homeservers above.
matrix_media_repo_admins:
  admins: []
# admins:
#   - "@your_username:example.org"

# Datastores are places where media should be persisted. This isn't dedicated for just uploads:
# thumbnails and other misc data is also stored in these places. The media repo, when looking
# for a datastore to use, will always use the smallest datastore first.
matrix_media_repo_datastores:
  datastores:
    - type: file
      enabled: true # Enable this to set up data storage.
      # Datastores can be split into many areas when handling uploads. Media is still de-duplicated
      # across all datastores (local content which duplicates remote content will re-use the remote
      # content's location). This option is useful if your datastore is becoming very large, or if
      # you want faster storage for a particular kind of media.
      #
      # The kinds available are:
      #   thumbnails    - Used to store thumbnails of media (local and remote).
      #   remote_media  - Original copies of remote media (servers not configured by this repo).
      #   local_media   - Original uploads for local media.
      #   archives      - Archives of content (GDPR and similar requests).
      forKinds: ["thumbnails", "remote_media", "local_media", "archives"]
      opts:
        path: /data/media

    - type: s3
      enabled: false # Enable this to set up s3 uploads
      forKinds: ["thumbnails", "remote_media", "local_media", "archives"]
      opts:
        # The s3 uploader needs a temporary location to buffer files to reduce memory usage on
        # small file uploads. If the file size is unknown, the file is written to this location
        # before being uploaded to s3 (then the file is deleted). If you aren't concerned about
        # memory usage, set this to an empty string.
        tempPath: "/tmp/mediarepo_s3_upload"
        endpoint: sfo2.digitaloceanspaces.com
        accessKeyId: ""
        accessSecret: ""
        ssl: true
        bucketName: "your-media-bucket"
        # An optional region for where this S3 endpoint is located. Typically not needed, though
        # some providers will need this (like Scaleway). Uncomment to use.
        #region: "sfo2"
        # An optional storage class for tuning how the media is stored at s3.
        # See https://aws.amazon.com/s3/storage-classes/ for details; uncomment to use.
        #storageClass: STANDARD

    # The media repo does support an IPFS datastore, but only if the IPFS feature is enabled. If
    # the feature is not enabled, this will not work. Note that IPFS support is experimental at
    # the moment and not recommended for general use.
    #
    # NOTE: Everything you upload to IPFS will be publicly accessible, even when the media repo
    # puts authentication on the download endpoints. Only use this option for cases where you
    # expect your media to be publicly accessible.
    - type: ipfs
      enabled: false # Enable this to use IPFS support
      forKinds: ["local_media"]
      # The IPFS datastore currently has no options. It will use the daemon or HTTP API configured
      # in the IPFS section of your main config.
      opts: {}

```

Full list of configuration options with documentation can be found in `roles/custom/matrix-media-repo/templates/defaults/main.yml`

