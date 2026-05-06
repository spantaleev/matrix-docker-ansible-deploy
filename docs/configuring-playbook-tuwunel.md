<!--
SPDX-FileCopyrightText: 2026 MDAD project contributors
SPDX-FileCopyrightText: 2026 Jason Volk

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Configuring Tuwunel (optional)

The playbook can install and configure the [Tuwunel](https://matrix-construct.github.io/tuwunel/) Matrix homeserver for you.

Tuwunel is a featureful homeserver written entirely in Rust, intended as a scalable, low-cost, enterprise-ready alternative to Synapse that fully implements the [Matrix specification](https://spec.matrix.org/latest/) for all but the most niche uses. It is the official successor to [conduwuit](configuring-playbook-conduwuit.md), is now sponsored by the government of Switzerland 🇨🇭 (where it is currently deployed for citizens), and is used by a number of organisations with a vested interest in its continued development. See the project's [documentation](https://matrix-construct.github.io/tuwunel/) for further background.

By default, the playbook installs [Synapse](https://github.com/element-hq/synapse) as it's the only full-featured Matrix server at the moment. If that's okay, you can skip this document.

> [!WARNING]
> - **You can't switch an existing Matrix server's implementation** (e.g. Synapse → Tuwunel). Proceed below only if you're OK with starting over, or you're dealing with a server on a new domain name which hasn't participated in the Matrix federation yet. The one exception is migrating from conduwuit; see [Migrating from conduwuit](#migrating-from-conduwuit).
> - **Homeserver implementations other than Synapse may not be fully functional** with every part of this playbook. Make yourself familiar with the trade-offs before proceeding.

## Adjusting the playbook configuration

To use Tuwunel, set the following on `inventory/host_vars/matrix.example.com/vars.yml`:

```yaml
matrix_homeserver_implementation: tuwunel

# Open the registration endpoint long enough to create your first user.
# After signing up, set this back to false.
matrix_tuwunel_config_allow_registration: true

# A registration token to protect the endpoint from abuse.
# Generate one with `pwgen -s 64 1` or similar.
matrix_tuwunel_config_registration_token: ''
```

The first user account that registers becomes a server admin and is automatically invited to the admin room. See [Creating the first user account](#creating-the-first-user-account) below for the bootstrap procedure.

## Wiring done for you

When `matrix_homeserver_implementation: tuwunel` is set, the playbook automatically integrates Tuwunel with the rest of your stack:

- **Federation.** Toggled by `matrix_homeserver_federation_enabled`. The federation virtual host (port 8448 in the default setup) is wired up via Traefik labels.
- **Well-known.** `matrix_tuwunel_config_well_known_client` is set to your public homeserver URL whenever SSL is enabled. Matrix clients use this for delegated-domain server discovery; identity-provider entries below can also omit their `callback_url`, since Tuwunel derives `<well-known>/_matrix/client/unstable/login/sso/callback/<client_id>` automatically.
- **Element Call / MatrixRTC.** When the [LiveKit JWT service](configuring-playbook-matrix-rtc.md) is enabled, Tuwunel publishes its public URL through `.well-known/matrix/client` per [MSC4143](https://github.com/matrix-org/matrix-spec-proposals/pull/4143).
- **Legacy calls (TURN).** When [Coturn](configuring-playbook-turn.md) is enabled, its URIs and shared secret (or username/password, depending on `coturn_authentication_method`) are wired automatically.

## Extending the configuration

Tuwunel exposes a large configuration surface. The role surfaces commonly used options as Ansible variables under `matrix_tuwunel_config_*`. See [`roles/custom/matrix-tuwunel/defaults/main.yml`](../roles/custom/matrix-tuwunel/defaults/main.yml) for the complete list, and [`roles/custom/matrix-tuwunel/templates/tuwunel.toml.j2`](../roles/custom/matrix-tuwunel/templates/tuwunel.toml.j2) for the rendered configuration.

For options that aren't surfaced as a dedicated variable, [environment variables](https://matrix-construct.github.io/tuwunel/configuration.html#environment-variables) are the recommended override mechanism. They take priority over the rendered TOML, are scoped to the running container, and require no template patching:

```yaml
matrix_tuwunel_environment_variables_extension: |
  TUWUNEL_REQUEST_TIMEOUT=60
  TUWUNEL_DNS_CACHE_SIZE=131072
```

Keys nested under a TOML section use `__` (double underscore) to descend, e.g. `TUWUNEL_WELL_KNOWN__SERVER`. User-named sections become path segments too: `TUWUNEL_STORAGE_PROVIDER__ARCHIVE__S3__URL` overrides the `url` field of the `archive` storage provider in the example below.

If you need wholesale control of the configuration file, copy [`roles/custom/matrix-tuwunel/templates/tuwunel.toml.j2`](../roles/custom/matrix-tuwunel/templates/tuwunel.toml.j2) into your inventory and point `matrix_tuwunel_template_tuwunel_config` at your copy.

The container image published as `:latest` is built with `io_uring`, `jemalloc`, LDAP, blurhashing, URL preview, sentry telemetry, and zstd compression all enabled, so most opt-in features are simply a configuration toggle away.

### Identity providers (OAuth2 / OIDC)

Configure one or more `[[global.identity_provider]]` entries via a list. Each entry maps directly to Tuwunel's [identity-provider fields](https://matrix-construct.github.io/tuwunel/authentication/providers.html); only the fields you set are emitted. GitHub, GitLab, and Google have built-in `issuer_url` defaults so a `client_id` plus `client_secret` is enough; for any other `brand` (Apple, Facebook, Keycloak, MAS, Twitter, etc.) you must supply `issuer_url` explicitly:

```yaml
matrix_tuwunel_config_identity_providers:
  - brand: keycloak
    client_id: matrix
    client_secret: '<provider secret>'
    issuer_url: https://sso.example.com/realms/matrix
    callback_url: https://matrix.example.com/_matrix/client/unstable/login/sso/callback/matrix
    trusted: true
  - brand: github
    client_id: '<github oauth app id>'
    client_secret: '<github oauth app secret>'
```

Self-hosted providers must supply both `client_id` and `issuer_url`. Set `trusted: true` only on providers you operate yourself; trusting a public provider (GitHub, Google, etc.) is an account-takeover risk.

### LDAP

Tuwunel can authenticate `m.login.password` requests against an LDAP directory and, in search-then-bind mode, keep admin status in sync with directory membership. The shipped image already includes the `ldap` build feature.

```yaml
matrix_tuwunel_config_ldap_enabled: true
matrix_tuwunel_config_ldap_uri: ldaps://ldap.example.com:636
matrix_tuwunel_config_ldap_base_dn: ou=users,dc=example,dc=org
matrix_tuwunel_config_ldap_bind_dn: cn=ldap-reader,dc=example,dc=org
matrix_tuwunel_config_ldap_bind_password_file: /etc/tuwunel/ldap.pw
matrix_tuwunel_config_ldap_filter: '(&(objectClass=person)(memberOf=cn=matrix,ou=groups,dc=example,dc=org))'
```

> [!NOTE]
> `bind_password_file` is read **inside the container**. The role bind-mounts `/matrix/tuwunel/config` to `/etc/tuwunel` (read-only) and `/matrix/tuwunel/data` to `/var/lib/tuwunel`. To make the file available at the path above, drop it on the host at `/matrix/tuwunel/config/ldap.pw` (owned by `matrix:matrix`) before running the playbook; the role does not template secret files for you.

For direct-bind, anonymous-search, and admin-sync details, see [LDAP authentication](https://matrix-construct.github.io/tuwunel/authentication/ldap.html).

### JWT login

Tuwunel can accept signed JSON Web Tokens both as a login flow and as a User-Interactive Authentication step:

```yaml
matrix_tuwunel_config_jwt_enabled: true
matrix_tuwunel_config_jwt_key: '<shared secret>'
matrix_tuwunel_config_jwt_format: HMAC          # one of HMAC, B64HMAC, ECDSA, EDDSA
matrix_tuwunel_config_jwt_algorithm: HS256
matrix_tuwunel_config_jwt_audience: ['matrix']
matrix_tuwunel_config_jwt_issuer: ['https://issuer.example.com']
```

The defaults match Synapse's `experimental_features.jwt_config` semantics, so a key + algorithm port should authenticate the same set of tokens. See [Enterprise JWT](https://matrix-construct.github.io/tuwunel/authentication/jwt.html) for the full reference, including the asymmetric (ECDSA / EdDSA) formats and the operator-controlled UIAA override flow.

### Media storage providers

Each entry becomes a `[global.storage_provider.<id>.<kind>]` block. `kind` is `local` or `s3`; the remaining keys map directly to the fields documented in [Storage providers](https://matrix-construct.github.io/tuwunel/media/storage.html):

```yaml
matrix_tuwunel_config_storage_providers:
  - id: primary
    kind: local
    base_path: /var/lib/tuwunel/media

  - id: archive
    kind: s3
    url: s3://my-bucket/media
    region: us-east-1
    key: AKIA...
    secret: '<aws secret>'
    multipart_threshold: 100 MiB
```

The S3 backend ships with native multipart upload, so no goofys/rclone sidecar is required. MinIO, Cloudflare R2, and DigitalOcean Spaces all work; set `endpoint` and `use_vhost_request: false` as appropriate.

> [!NOTE]
> Local provider paths must live under `/var/lib/tuwunel` (the container's data mount, persisted on the host at `/matrix/tuwunel/data`), or you must mount the target directory into the container yourself via `matrix_tuwunel_container_extra_arguments`. The container otherwise runs read-only.

### RocksDB and cache tuning

Tuwunel embeds RocksDB. The defaults (`rocksdb_compression_algo: zstd`) suit most deployments. For high-throughput servers you may want to enable direct I/O, raise parallelism, and bump the cache modifier:

```yaml
matrix_tuwunel_config_rocksdb_direct_io: true
matrix_tuwunel_config_rocksdb_parallelism_threads: 8
matrix_tuwunel_config_cache_capacity_modifier: 2.0
matrix_tuwunel_config_database_backup_path: /var/lib/tuwunel/backups
```

If you run on ZFS, the [Tuwunel maintenance guide](https://matrix-construct.github.io/tuwunel/maintenance.html#zfs) lists the dataset properties (`recordsize`, `primarycache`, `compression`, `atime`, `logbias`) and config flags (`rocksdb_direct_io`, `rocksdb_allow_fallocate`) you need to adjust to avoid severe write amplification.

To enable Sentry crash reporting, set `matrix_tuwunel_config_sentry_enabled: true`.

### Federation gating

Tuwunel accepts regular-expression patterns at every level of remote-server filtering:

```yaml
matrix_tuwunel_config_forbidden_remote_server_names:
  - 'bad\.example\.com$'
matrix_tuwunel_config_forbidden_remote_room_directory_server_names:
  - 'spam\.example\.com$'
matrix_tuwunel_config_prevent_media_downloads_from:
  - 'heavy\.example\.com$'
```

Tuwunel additionally implements [MSC4284 policy servers](https://github.com/matrix-org/matrix-spec-proposals/pull/4284) for room-level federation gating; that lives in room state and needs no playbook configuration.

### Default room version

The role sets `default_room_version: '12'`, so newly created rooms default to Matrix [room version 12](https://github.com/matrix-org/matrix-spec-proposals/pull/4289) ("Hydra"). Override `matrix_tuwunel_config_default_room_version` if you need an earlier version for client compatibility.

## Creating the first user account

Unlike Synapse and Dendrite, Tuwunel does not register users from the command line or via the playbook. On first startup it logs a one-time-use registration token to its journal:

```sh
# Adjust the duration if necessary or remove the --since argument.
journalctl -u matrix-tuwunel.service --since="10 minutes ago"
```

Use the token to create your first account from any client that supports token-gated registration (e.g. [Element Web](configuring-playbook-client-element-web.md)). The account is auto-promoted to admin and invited to the admin room together with the `@conduit:<server_name>` server bot. The bot keeps the legacy `conduit` localpart due to the project's lineage from Conduit.

## Configuring bridges and appservices

The playbook does not auto-register appservices for Tuwunel. After your bridge has produced its `registration.yaml` (e.g. `/matrix/mautrix-signal/bridge/registration.yaml`), register it manually by sending the contents to the admin room, prefixed with `!admin appservices register` and wrapped in a fenced code block:

    !admin appservices register
    ```
    id: signal
    url: http://matrix-mautrix-signal:29328
    as_token: <token>
    hs_token: <token>
    sender_localpart: _bot_signalbot
    rate_limited: false
    namespaces:
      users:
        - exclusive: true
          regex: '^@signal_.+:example\.org$'
        - exclusive: true
          regex: '^@signalbot:example\.org$'
      aliases:
        - exclusive: true
          regex: '^#signal_.+:example\.org$'
    ```

Registrations stored this way are persisted in the database and survive restarts. Re-running the command with the same `id` replaces the existing entry. See [Application services](https://matrix-construct.github.io/tuwunel/appservices.html) for the full reference and admin commands.

## Migrating from conduwuit

Tuwunel is a "binary swap" for conduwuit; it reads conduwuit's RocksDB layout directly, so migration is a data move, not an export/import.

1. Set `matrix_homeserver_implementation: tuwunel` on `vars.yml` and remove any `matrix_conduwuit_*` overrides.
2. Run a full installation so that the new service is created and the old one removed (e.g. `just setup-all`).
3. Run `just run-tags tuwunel-migrate-from-conduwuit`.

The migration stops `matrix-conduwuit.service`, copies `/matrix/conduwuit` into `/matrix/tuwunel`, renames the config file, and starts `matrix-tuwunel.service`. The freshly generated tuwunel data directory is preserved alongside as `/matrix/tuwunel_old` until you remove it manually.

> [!CAUTION]
> Migrating from any other Conduit derivative (Conduit itself, Continuwuity, or any other fork) is **not supported** and will corrupt your database. All Conduit forks share the same linear database version with no awareness of each other; switching between them produces unrecoverable damage. See the [upstream migration table](https://matrix-construct.github.io/tuwunel/#migrating-to-tuwunel).

## Troubleshooting

As with all other services, the logs are available via [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html):

```sh
journalctl -fu matrix-tuwunel
```

Logging verbosity is controlled by `matrix_tuwunel_config_log` in [`tracing-subscriber` env-filter syntax](https://docs.rs/tracing-subscriber/latest/tracing_subscriber/filter/struct.EnvFilter.html). The default (`info,state_res=warn`) is reasonable for production; for debugging, try `debug` or scope it tighter, e.g. `info,tuwunel_service::sending=debug`.

For RocksDB-level issues, online backups, and offline backup procedures, see the [Tuwunel maintenance guide](https://matrix-construct.github.io/tuwunel/maintenance.html). For protocol-compliance state across MSCs, the spec, and Complement, the project's [compliance dashboard](https://matrix-construct.github.io/tuwunel/development/compliance.html) is the authoritative tracker.
