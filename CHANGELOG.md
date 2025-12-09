# 2025-12-09

## Traefik Cert Dumper upgrade

The variable `traefik_certs_dumper_ssl_dir_path` was renamed to `traefik_certs_dumper_ssl_path`. Users who use [their own webserver with Traefik](docs/configuring-playbook-own-webserver.md) may need to adjust their configuration.

The variable `traefik_certs_dumper_dumped_certificates_dir_path` was renamed to `traefik_certs_dumper_dumped_certificates_path`. Users who use [SRV Server Delegation](docs/howto-srv-server-delegation.md) may need to adjust their configuration.

# 2025-11-23

## Matrix.to support

The playbook now supports [Matrix.to](https://github.com/matrix-org/matrix.to) — a simple URL redirection service which powers [matrix.to](https://matrix.to).

To learn more, see our [Setting up Matrix.to](docs/configuring-playbook-matrixto.md) documentation page.

# 2025-11-09

## matrix-appservice-webhooks has been removed from the playbook

[matrix-appservice-webhooks](./docs/configuring-playbook-bridge-appservice-webhooks.md) has been removed from the playbook, as it has been deprecated since more than several years.

The playbook will let you know if you're using any `matrix_appservice_webhooks_*` variables. You'll need to remove them from `vars.yml` and potentially [uninstall the bridge manually](./docs/configuring-playbook-bridge-appservice-webhooks.md#uninstalling-the-bridge-manually).

## mautrix-facebook and mautrix-instagram have been removed from the playbook

[mautrix-facebook](./docs/configuring-playbook-bridge-mautrix-facebook.md) and [mautrix-instagram](./docs/configuring-playbook-bridge-mautrix-instagram.md) have been removed from the playbook, as they have been deprecated in favor of the [mautrix-meta](https://github.com/mautrix/meta) Messenger/Instagram bridge, integrated to the playbook at [2024-02-19](#2024-02-19).

The playbook will let you know if you're using any variables for those bridges:

- `matrix_mautrix_facebook_*`
- `matrix_mautrix_instagram_*`

You'll need to remove them from `vars.yml` and potentially uninstall them manually. Consult pages below for details:

- [Instruction for mautrix-facebook](./docs/configuring-playbook-bridge-mautrix-facebook.md#uninstalling-the-bridge-manually)
- [Instruction for mautrix-instagram](./docs/configuring-playbook-bridge-mautrix-instagram.md#uninstalling-the-bridge-manually)

# 2025-11-08

## MatrixZulipBridge support

Thanks to [Suguru Hirahara](https://github.com/luixxiul), the playbook now supports the [GearKite/MatrixZulipBridge](https://github.com/GearKite/MatrixZulipBridg) bridge for bridging Matrix to [Zulip](https://zulip.com/).

To learn more, see our [Setting up Zulip bridging](docs/configuring-playbook-bridge-zulip.md) documentation page.

# 2025-11-07

## The matrix-chatgpt-bot has been removed from the playbook

The [matrix-bot-chatgpt](./docs/configuring-playbook-bot-chatgpt.md) has been removed from the playbook, as it has been deprecated since September 2024.

The playbook will let you know if you're using any `matrix_bot_chatgpt_*` variables. You'll need to remove them from `vars.yml` and potentially [uninstall the bot manually](./docs/configuring-playbook-bot-chatgpt.md#uninstalling-matrix-chatgpt-bot-manually).

# 2025-11-05

## The MX Puppet bridges for Discord, Instagram, Slack, and Twitter have been removed from the playbook

The MX Puppet bridges for Discord, Instagram, Slack, and Twitter have been removed from the playbook, as they have been unmaintained for more than several years and do not support important features like authenticated media. See [this issue](https://github.com/spantaleev/matrix-docker-ansible-deploy/issues/3867) for the context.

The playbook will let you know if you're using any variables for those bridges:

- `matrix_mx_puppet_discord_*`
- `matrix_mx_puppet_instagram_*`
- `matrix_mx_puppet_slack_*`
- `matrix_mx_puppet_twitter_*`

You'll need to remove them from `vars.yml` and potentially uninstall them manually. Consult pages below for details:

- [Instruction for MX Puppet Discord bridge](./docs/configuring-playbook-bridge-mx-puppet-discord.md#uninstalling-the-bridge-manually)
- [Instruction for MX Puppet Instagram bridge](./docs/configuring-playbook-bridge-mx-puppet-instagram.md#uninstalling-the-bridge-manually)
- [Instruction for MX Puppet Slack bridge](./docs/configuring-playbook-bridge-mx-puppet-slack.md#uninstalling-the-bridge-manually)
- [Instruction for MX Puppet Twitter bridge](./docs/configuring-playbook-bridge-mx-puppet-twitter.md#uninstalling-the-bridge-manually)

# 2025-11-04

## The Go Skype bridge has been removed from the playbook

The [go-skype-bridge](./docs/configuring-playbook-bridge-go-skype-bridge.md) has been removed from the playbook, as Skype has been discontinued since the May 2025.

The playbook will let you know if you're using any `matrix_go_skype_bridge_*` variables. You'll need to remove them from `vars.yml` and potentially [uninstall the bridge manually](./docs/configuring-playbook-bridge-go-skype-bridge.md#uninstalling-the-bridge-manually).

# 2025-10-02

## Element Admin support

The playbook now supports [Element Admin](./docs/configuring-playbook-element-admin.md) - a new web-based administration panel for Synapse and [Matrix Authentication Service](./docs/configuring-playbook-matrix-authentication-service.md).

Deployments based on Matrix Authentication Service may find it useful to run both Synapse Admin and Element Admin at the same time.

Deployments that don't rely on Matrix Authentication Service are unlikely to find anything useful in Element Admin right now (it's too basic in its current form).


# 2025-04-26

## Continuwuity support

Thanks to [Virkkunen](https://github.com/Virkkunen), we now have optional experimental [Continuwuity](./docs/configuring-playbook-continuwuity.md) homeserver support.

Continuwuity is a fork of [conduwuit](./docs/configuring-playbook-conduwuit.md), which the playbook also supports. It appears that conduwuit has been abandoned and various forks (like Continuwuity, [Tuwunel](https://github.com/matrix-construct/tuwunel) and possibly others) are continuing in its path.

Existing installations do **not** need to be updated. **Synapse is still the default homeserver implementation** installed by the playbook.

People that used to run conduwuit, may wish to:

- either [migrate from conduwuit to Continuwuity](./docs/configuring-playbook-continuwuity.md#migrating-from-conduwuit)
- or wait for some of the other forks to progress and for support for them to get added to the playbook

**The homeserver implementation of an existing server cannot be changed** (e.g. from Synapse/Conduit/Dendrite to Continuwuity) without data loss.


# 2025-04-09

## Element Call frontend installation is now optional

Because all Element clients (Element Web and Element X mobile) now embed and use their own Element Call frontend application (and not the one hosted via the playbook), it makes little sense for the playbook to self-host the Element Call frontend for you. Setting up the frontend requires an additional hostname (DNS setup) and it won't be used by Element clients anyway, so **we now recommend not installing the Element Call frontend**.

💡 A reason you may wish to continue installing the Element Call frontend (despite Matrix clients not making use of it), is if you need to use it standalone - directly via a browser (without a Matrix client).

The playbook now lets you [Decide between Element Call vs just the Matrix RTC stack](./docs/configuring-playbook-element-call.md#decide-between-element-call-vs-just-the-matrix-rtc-stack).

If you've already installed Element Call (via `matrix_element_call_enabled: true`), you can switch to installing just the [Matrix RTC (Real-Time Communication) stack](./docs/configuring-playbook-matrix-rtc.md) (all supporting services **without the Element Call frontend**) by:

1. Adjusting your `vars.yml` configuration like this:

```diff
-matrix_element_call_enabled: true
+matrix_rtc_enabled: true
```

2. [Re-running the playbook](./docs/installing.md) with the `setup-all` Ansible tag (e.g. `just setup-all`)

3. Getting rid of the `call.element.example.com` DNS record


# 2025-03-15

## Element Call support

The playbook now supports [Element Call](https://github.com/element-hq/element-call) as an optional feature. Thanks to [wjbeckett](https://github.com/wjbeckett) for getting us started via [PR#3562](https://github.com/spantaleev/matrix-docker-ansible-deploy/pull/3562).

Element Call is a native Matrix video conferencing application developed by [Element](https://element.io/) that has the goal of replacing [Jitsi](./docs/configuring-playbook-jitsi.md) and the old WebRTC stack used in previous Element versions.

💡 For now, Element Call is only supported with the [Synapse](docs/configuring-playbook-synapse.md) homeserver (with [federation](docs/configuring-playbook-federation.md) enabled) and [Element Web](docs/configuring-playbook-client-element-web.md) and Element X mobile clients. See the [Prerequisites](docs/configuring-playbook-element-call.md#prerequisites) section of the [Element Call documentation](docs/configuring-playbook-element-call.md) for more details.

To get started, see the [Configuring Element Call](docs/configuring-playbook-element-call.md) documentation page.


# 2025-03-08

## 6️⃣ IPv6 support enablement recommended by default

Our [default example configuration](./examples/vars.yml) and [Configuring DNS](./docs/configuring-dns.md) guides now recommend enabling [IPv6](https://en.wikipedia.org/wiki/IPv6) support. We recommend that everyone enables IPv6 support for their Matrix server, even if they don't have IPv6 connectivity yet.

Our new [Configuring IPv6](./docs/configuring-ipv6.md) documentation page has more details about the playbook's IPv6 support.

**Existing playbook users** will **need to do some manual work** to enable IPv6 support. This consists of:

- enabling IPv6 support for the Docker container networks:
	- add `devture_systemd_docker_base_ipv6_enabled: true` to their `vars.yml` configuration file
	- stop all services (`just stop-all`)
	- delete all container networks on the server: `docker network rm $(docker network ls -q)`
	- re-run the playbook fully: `just install-all`

- [configuring IPv6 (`AAAA`) DNS records](./docs/configuring-ipv6.md#configuring-dns-records-for-ipv6)

# 2025-02-26

## 🪦 Bye-bye, Email2Matrix

The [Email2Matrix](./docs/configuring-playbook-email2matrix.md) service has been superseded by the [Postmoogle](./docs/configuring-playbook-bridge-postmoogle.md) bridge for a long time now and was completely removed from the playbook today.

If you still have the Email2Matrix component installed on your Matrix server, the playbook can no longer help you uninstall it and you will need to do it manually as described in the [Uninstalling Email2Matrix manually](./docs/configuring-playbook-email2matrix.md#uninstalling-email2matrix-manually) section of the documentation. The playbook will warn you if there are any `matrix_email2matrix_*` variables still remaining in your configuration.


# 2025-02-23

## The playbook defaults to exposing the Coturn STUN port (3478) over UDP once again

Recently, we made the playbook [default to exposing the Coturn STUN port (3478) only over TCP](#the-playbook-now-defaults-to-exposing-the-coturn-stun-port-3478-only-over-tcp) to reduce the severity of DDoS amplification/reflection attacks.

It seems like old Element clients on mobile devices only support talking to the STUN port over UDP, not TCP.
To accommodate such ancient clients, we're now **reversing this change** and **defaulting to exposing the Coturn STUN port (3478) over UDP once again**.

In light of this new information, you have 2 options:

1. **If you already adapted to the previous change and would like to adapt to this change one again**:

- make sure the `3478/udp` port is whitelisted in your external firewall (if you have one) once again.

2. **If you don't care about old Element clients and wish to reduce the severity of DDoS amplification/reflection attacks**:

- Consider closing the STUN/UDP port with the following configuration:

  ```yaml
  matrix_coturn_container_stun_plain_host_bind_port_udp: ""
  ```

- Consider keeping `3478/udp` blocked in your external firewall (if you have one)

# 2025-02-21

## Docker daemon options are no longer adjusted when IPv6 is enabled

We landed [initial IPv6 support](#initial-work-on-ipv6-support) in the past via a `devture_systemd_docker_base_ipv6_enabled` variable that one had to toggle to `true`.

This variable did **2 different things at once**:

- ensured that container networks were created with IPv6 being enabled
- adjusted the Docker daemon's configuration to set `experimental: true` and `ip6tables: true` (a necessary prerequisite for creating IPv6-enabled networks)

Since Docker 27.0.1's [changes to how it handles IPv6](https://docs.docker.com/engine/release-notes/27/#ipv6), **adjusting the Docker daemon's configuration is no longer necessary**, because:
- `ip6tables` defaults to `true` for everyone
- `ip6tables` is out of the experimental phase, so `experimental` is no longer necessary

In light of this, we're introducing a new variable (`devture_systemd_docker_base_ipv6_daemon_options_changing_enabled`) for controlling if IPv6 should be force-enabled in the Docker daemon's configuration options.
Since most people should be on a modern enough Docker daemon version which doesn't require such changes, this variable defaults to `false`.

This change affects you like this:

- ✅ if you're **not explicitly enabling IPv6** (via `devture_systemd_docker_base_ipv6_enabled` in your configuration): you're unaffected
- ❓ if you're **explicitly enabling IPv6** (via `devture_systemd_docker_base_ipv6_enabled` in your configuration):
  - ✅ .. and you're on a modern enough Docker version (which you most likely are): the playbook will no longer mess with your Docker daemon options. You're unaffected.
  - 🔧 .. and you're on an old Docker version, you **are affected** and need to use the following configuration to restore the old behavior:

    ```yml
    # Force-enable IPv6 by changing the Docker daemon's options.
    # This is necessary for Docker < 27.0.1, but not for newer versions.
    devture_systemd_docker_base_ipv6_daemon_options_changing_enabled: true

    # Request that individual container networks are created with IPv6 enabled.
    devture_systemd_docker_base_ipv6_enabled: true
    ```

## Support for bridging to Bluesky via mautrix-bluesky

Thanks to [Zepmann](https://github.com/Zepmann), the playbook now supports bridging to [Bluesky](https://bsky.app/) via [mautrix-bluesky](https://github.com/mautrix/bluesky).

To learn more, see our [Setting up mautrix-bluesky](./docs/configuring-playbook-bridge-mautrix-bluesky.md) documentation page.


# 2025-02-19

## The playbook now defaults to exposing the Coturn STUN port (3478) only over TCP

We've previously done some work to **decrease the severity** of DDoS amplification attacks done through the [Coturn](./docs/configuring-playbook-turn.md)'s STUN port (2.8x -> 1.6x) as reported in [coturn: Lower DDoS amplification/reflection factor from 2.8 to 1.6 #2592](https://github.com/spantaleev/matrix-docker-ansible-deploy/issues/2592).

To **completely eliminate the problem** of DDoS amplification attacks done through the [Coturn](./docs/configuring-playbook-turn.md) STUN port even further (read more about this in [this article](https://stormwall.network/resources/blog/protect-against-ddos-based-on-stun-exploit)), the playbook now **disables exposure of the Coturn STUN port (`3478`) over UDP**. This is a bit heavy-handed, but is probably the only way to completely eliminate the problem.

The playbook now **only exposes the Coturn STUN port (`3478`) over TCP by default**.

💡 Users may wish to further remove the (now unnecessary) firewall rule allowing access to `3478/udp`.

If you'd like the Coturn STUN port to be exposed over UDP like before, you can revert to the previous behavior by using the following configuration in your `vars.yml` file:

```yaml
matrix_coturn_container_stun_plain_host_bind_port_udp: "3478"
```

> [!WARNING]
> People running Coturn directly on the `host` network (using `matrix_coturn_container_network: host`) will still have the STUN port exposed over UDP, as port exposure is done directly via Coturn and not via Docker. In such cases, the playbook cannot prevent `3478/udp` port exposure and you'd need to do it in another way (separate firewall rule, etc).


# 2025-02-17

## FluffyChat Web support

Thanks to [Aine](https://gitlab.com/etke.cc) of [etke.cc](https://etke.cc/), the playbook now supports [FluffyChat Web](https://github.com/krille-chan/fluffychat) as an additional Matrix client you can self-host.

To learn more, see our [Setting up FluffyChat Web](docs/configuring-playbook-client-fluffychat-web.md) documentation page.


# 2025-02-03

## The mautrix-hangouts bridge has been removed from the playbook

The [mautrix-hangouts](./docs/configuring-playbook-bridge-mautrix-hangouts.md) bridge has been deprecated in the playbook since December 2024 and finally got completely removed from the playbook in February 2025.

This is because Google Hangouts has been discontinued since the 1st of November 2022.

The playbook will let you know if you're using any `matrix_mautrix_hangouts_*` variables. You'll need to remove them from `vars.yml` and potentially [uninstall the bridge manually](./docs/configuring-playbook-bridge-mautrix-hangouts.md#uninstalling-the-bridge-manually).


# 2025-01-27

## Redis and KeyDB are no longer part of the playbook

**TLDR**: The playbook now exclusively uses Valkey as its Redis-compatible memorystore implementation, removing support for Redis and KeyDB. Most users are unaffected by this change unless they explicitly configured Redis or KeyDB variables. Only users that were explicitly defining `redis_*` or `keydb_*` variables will need to update their configuration to use `valkey_*` variables instead.

The playbook has gone through several iterations of memorystore implementations:

1. It initially used Redis, auto-installing it when needed by features/services
2. [Switched to KeyDB](#backward-compatibility-break-the-playbook-now-defaults-to-keydb-instead-of-redis) as the default, while keeping Redis support for those who wished to remain on Redis
3. [Switched to Valkey](#backward-compatibility-break-the-playbook-now-defaults-to-valkey-instead-of-keydb) due to [KeyDB issues](https://github.com/spantaleev/matrix-docker-ansible-deploy/issues/3544), while keeping Redis and KeyDB support, for those who wished to remain on them

To reduce configuration complexity and maintenance overhead, we are now:

- removing Redis and KeyDB support entirely
- using Valkey as the sole Redis-compatible memorystore implementation

To update your configuration:

- **Most users** don't need to do anything
- **Users that were explicitly sticking to Redis/KeyDB** need to update their `vars.yml` to use `valkey_*` variables instead


# 2025-01-19

## conduwuit support

Thanks to [Virkkunen](https://github.com/Virkkunen), we now have optional experimental [conduwuit](https://conduwuit.puppyirl.gay/) homeserver support for new installations.

conduwuit is a fork of [Conduit](./docs/configuring-playbook-conduit.md), which the playbook also supports. See [Differences from upstream Conduit](https://conduwuit.puppyirl.gay/differences.html).

Existing installations do **not** need to be updated. **Synapse is still the default homeserver implementation** installed by the playbook.

To try out conduwuit, we recommend that you **use a new server**. Refer to our [Configuring conduwuit](./docs/configuring-playbook-conduwuit.md) guide for details.

**The homeserver implementation of an existing server cannot be changed** (e.g. from Synapse/Conduit/Dendrite to conduwuit) without data loss.


# 2025-01-14

## (Backward Compatibility Break) Synapse v1.122.0 requires Postgres v13

The Synapse homeserver [requires Postgres v13 or newer](https://github.com/element-hq/synapse/issues/18034).

If you've been maintaining your setup for a while and you haven't been doing [Postgres upgrades](docs/maintenance-postgres.md#upgrading-postgresql), you may be on an old version of Postgres. The easiest way to check is to see the contents of the `/matrix/postgres/data/PG_VERSION` file.

If you're on a Postgres version older than v13, you need to [upgrade your Postgres setup](docs/maintenance-postgres.md#upgrading-postgresql) or Synapse will produce an error on startup.

If you're using an external Postgres server (not installed by this playbook), you'll need to figure out how to upgrade it yourself.

If you're not ready to upgrade your Postgres setup yet, you can temporarily remain on an old Synapse version by adding the following configuration to your `vars.yml` file:

```yaml
# Pinning to the last Synapse version which supports Postgres v11 and v12.
matrix_synapse_version: v1.121.1
```


# 2024-11-26

## (Backward Compatibility Break) Synapse now defaults to enabling authenticated media

**TLDR**: with this update, your Synapse homeserver will start requiring authentication for newly-uploaded media files. While the majority of the ecosystem (clients, bots, etc.) should support this, certain software may lack support for it (and you may wish to turn it off, if it's causing issues).

The default configuration for the Synapse homeserver now [enforces Authenticated media by default](https://element-hq.github.io/synapse/v1.120/upgrade.html#authenticated-media-is-now-enforced-by-default).

Servers like `matrix.org` have already [sunset unauthenticated media](https://matrix.org/blog/2024/06/26/sunsetting-unauthenticated-media/) months ago.

Now that **various clients, bots, bridges and extra services have caught up with authenticated media support**, Synapse developers seem confident that it's time to enable authenticated media by default.

We're changing the playbook configuration for authenticated media to keep up with upstream defaults changing.

Old and unmaintained bridges (like all mx-puppet bridges, etc.) do not support authenticated media. Other software may be similarly affected. If you experience issues with some Matrix-related software, you may wish to disable authenticated media and contact the software maintainers to let them know.

You can disable authenticated media at any time by setting `matrix_synapse_enable_authenticated_media: false` in your `vars.yml` configuration file and re-running the playbook.


# 2024-11-23

## (Backward Compatibility Break) The playbook now defaults to Valkey, instead of KeyDB

**TLDR**: if the playbook installed KeyDB (or Redis) as a dependency for you before, it will now replace it with [Valkey](https://valkey.io/) (a drop-in alternative). We [previously switched from Redis to KeyDB](#backward-compatibility-break-the-playbook-now-defaults-to-keydb-instead-of-redis), but Valkey is a better alternative, so we're switching again.

The playbook used to install Redis or KeyDB if services have a need for a Redis-compatible implementation ([enabling worker support for Synapse](docs/configuring-playbook-synapse.md#load-balancing-with-workers), [enabling Hookshot encryption](docs/configuring-playbook-bridge-hookshot.md#end-to-bridge-encryption), etc.).

Earlier this year, we switched from Redis to KeyDB — see [(Backward Compatibility Break) The playbook now defaults to KeyDB, instead of Redis](#backward-compatibility-break-the-playbook-now-defaults-to-keydb-instead-of-redis).

Because Valkey seems to be a better successor to Redis (than KeyDB) and likely doesn't suffer from [issues like this one](https://github.com/spantaleev/matrix-docker-ansible-deploy/issues/3544), we now replace KeyDB with Valkey.

Valkey (like KeyDB and Redis in the past) is an implicitly enabled dependency — you don't need custom configuration in `vars.yml` to enable it.

Next time your run the playbook (via the `setup-all` tag), **KeyDB will be automatically uninstalled and replaced with Valkey**. Some Synapse downtime may occur while the switch happens.

Users on `arm32` should be aware that there's **neither a prebuilt `arm32` container image for Valkey**, nor the Valkey role supports self-building yet. Users on this architecture likely don't run Synapse with workers, etc., so they're likely in no need of Valkey (or Redis/KeyDB). If Redis is necessary in an `arm32` deployment, disabling Valkey and making the playbook fall back to Redis is possible (see below).

**The playbook still supports Redis** and you can keep using Redis (for now) if you'd like, by adding this additional configuration to your `vars.yml` file:

```yml
# Explicitly disable both Valkey and KeyDB.
#
# Redis will be auto-enabled if necessary,
# because there's no other Redis-compatible implementation being enabled.
valkey_enabled: false
keydb_enabled: false
```

**The playbook still supports KeyDB** and you can keep using KeyDB (for now) if you'd like, by adding this additional configuration to your `vars.yml` file:

```yml
# Explicitly disable Valkey  enable KeyDB.
#
# Redis will not be auto-enabled beandcause a Redis-compatible implementation (KeyDB) is enabled.
valkey_enabled: false
keydb_enabled: true
```

At some point in time in the future, we'll remove both KeyDB and Redis from the playbook, so we recommend that you migrate to Valkey earlier anyway.


# 2024-11-14

## HTTP-compression support for Traefik-based setups

The playbook now **automatically enables HTTP-compression support** for major services powered by the playbook, like [Cinny](./docs/configuring-playbook-client-cinny.md), [Element Web](./docs/configuring-playbook-client-element-web.md), [Hydrogen](./docs/configuring-playbook-client-hydrogen.md), as well as for Matrix Client-Server and Federation APIs (`matrix.example.com`).

Other services installed by the playbook are currently not compression-enabled, but may become so over time. This change is rolled out on a per-service basis (as opposed to doing it globally, at the Traefik entrypoint level) to allow certain services or route endpoints which do not behave well when compressed (e.g. [issue 3749](https://github.com/spantaleev/matrix-docker-ansible-deploy/issues/3749)) to be excluded from compression.

A long time ago, various services were operating with `gzip`-compression enabled at the nginx level. Since the switch to Traefik (see [Goodbye, `matrix-nginx-proxy` 🪦](https://github.com/spantaleev/matrix-docker-ansible-deploy/blob/57c5271d9d6265a34a9d9cceb93365f685074f96/CHANGELOG.md#goodbye-matrix-nginx-proxy-)), all services (with the exception of Matrix APIs for Synapse worker-enabled setups which are powered by `nginx` via `synapse-reverse-proxy-companion`) have been operating without HTTP-compression support.

HTTP-compression is now done via Traefik's [compress](https://doc.traefik.io/traefik/middlewares/http/compress/) middleware. We use the default configuration for this middleware, which enables `zstd`, `br` and `gzip` support (in this order). This middleware's configuration can be configured via variables in the Traefik role (see `traefik_config_http_middlewares_compression_middleware_options`).

If you're using your own Traefik reverse-proxy server ([Traefik managed by you](./docs/configuring-playbook-own-webserver.md#traefik-managed-by-you)) instead of the playbook's integrated Traefik service, you can benefit from the same by:

- defining a [compress](https://doc.traefik.io/traefik/middlewares/http/compress/) middleware (via the [file](https://doc.traefik.io/traefik/providers/file/) or [Docker](https://doc.traefik.io/traefik/providers/docker/) providers)
- setting `matrix_playbook_reverse_proxy_traefik_middleware_compression_enabled` to `true`
- specifying the middleware's name in `matrix_playbook_reverse_proxy_traefik_middleware_compression_name` (e.g. `matrix_playbook_reverse_proxy_traefik_middleware_compression_name: my-compression-middleware@file`)

## Timeout adjustments for Traefik-based setups

The playbook now supports configuring various [transport.respondingTimeouts](https://doc.traefik.io/traefik/routing/entrypoints/#respondingtimeouts) timeout values (`readTimeout`, `writeTimeout`, `idleTimeout`) for the `web`, `web-secure` and `matrix-federation` entrypoints.

If you're using your own Traefik reverse-proxy server ([Traefik managed by you](./docs/configuring-playbook-own-webserver.md#traefik-managed-by-you)) instead of the playbook's integrated Traefik service, you may wish to do similar configuration changes to your setup manually.

The most interesting of these is the `readTimeout` configuration value (the maximum duration for reading the entire request, including the body), which used to default to `60s`. For large and slowly progressing file uploads, `60s` would often not be enough for the transfer to finish and uploads would end up being interrupted. The playbook now raises the `readTimeout` value to 5 minutes (`300s`) to improve this use-case.

The `traefik_config_entrypoint_web_transport_respondingTimeouts_*` variables (for the `web` entrypoint) cascade to affecting the timeout values for the `web-secure` and `matrix-federation` entrypoints, so you can easily adjust all timeout values using them.

Example of the default timeout values used by the playbook:

```yml
traefik_config_entrypoint_web_transport_respondingTimeouts_readTimeout: 300s

# 0s means "no timeout"
traefik_config_entrypoint_web_transport_respondingTimeouts_writeTimeout: 0s

traefik_config_entrypoint_web_transport_respondingTimeouts_idleTimeout: 180s
```

Alternatively, you may adjust the timeout values for specific entrypoints (like `web-secure` and `matrix-federation`) using dedicated variables (like `traefik_config_entrypoint_web_secure_transport_respondingTimeouts_readTimeout` and `matrix_playbook_public_matrix_federation_api_traefik_entrypoint_config_transport_respondingTimeouts_readTimeout`).


# 2024-11-08

## Support for synapse-admin auto-configuration via /.well-known/matrix/client

You can administrate your Synapse-powered homeserver using synapse-admin hosted externally (e.g. [admin.etke.cc](https://admin.etke.cc/)) and the synapse-admin instance would still auto-configure itself correctly for your server by [reading its `/.well-known/matrix/client` file](https://github.com/etkecc/synapse-admin/pull/126).

The playbook now configures the `/.well-known/matrix/client` file for this by default, injecting into it a `cc.etke.synapse-admin` section that contains the full synapse-admin configuration. This is done even if you don't enable the synapse-admin service in your configuration. The reason for always doing it is to allow users to skip the (small) overhead of self-hosting the non-core synapse-admin service, yet still be able to use it from elsewhere when needed.

If you don't ever plan on using synapse-admin from other servers (besides your own due to [self-hosting synapse-admin](./docs/configuring-playbook-synapse-admin.md)), you **can disable this** `/.well-known/matrix/client` configuration via `matrix_static_files_file_matrix_client_property_cc_etke_synapse_admin_enabled: false`


# 2024-10-28

## (BC Break) Postmoogle's variable names need adjustments

Due to the recategorization of [Postmoogle](./docs/configuring-playbook-bridge-postmoogle.md) from the bot to the bridge, its variables were renamed (`matrix_bot_postmoogle_` -> `matrix_postmoogle_`). You need to adjust your `vars.yml` configuration accordingly.

# 2024-10-19

## Support for Matrix Authentication Service

The playbook now supports installing and configuring [Matrix Authentication Service](./docs/configuring-playbook-matrix-authentication-service.md) (MAS).

Huge thanks to [Quentin Gliech](https://github.com/sandhose) from the [Element](https://element.io/) / [Matrix Authentication Service](https://github.com/element-hq/matrix-authentication-service) team for answering our numerous questions about MAS.

This is an **experimental service** and there are **still certain issues with it** (see [Expectations](./docs/configuring-playbook-matrix-authentication-service.md#expectations)). Matrix server administrators should only consider switching if they identify with one or more [reasons to use Matrix Authentication Service](./docs/configuring-playbook-matrix-authentication-service.md#reasons-to-use-matrix-authentication-service). As MAS adoption improves and more services are adjusted to support it, we expect that using MAS will become the norm.

Our [Setting up Matrix Authentication Service](./docs/configuring-playbook-matrix-authentication-service.md) documentation page has more details about this new service, what you might expect from the switch and how you can migrate your existing (Synapse) homeserver setup to MAS.


# 2024-09-27

## (BC Break) Postgres & Traefik roles have been relocated and variable names need adjustments

Various roles have been relocated from the [devture](https://github.com/devture) organization to the [mother-of-all-self-hosting](https://github.com/mother-of-all-self-hosting) organization.

Along with the relocation, the `devture_` prefix was dropped from their variable names, so you need to adjust your `vars.yml` configuration.

You need to do the following replacements:

- `devture_postgres_` -> `postgres_`
- `devture_traefik_` -> `traefik_`

As always, the playbook would let you know about this and point out any variables you may have missed.


# 2024-09-12

## Support for baibot

The playbook now supports installing [baibot](./docs/configuring-playbook-bot-baibot.md) (pronounced bye-bot) — a [Matrix](https://matrix.org/) bot developed by [etke.cc](https://etke.cc/) that exposes the power of [AI](https://en.wikipedia.org/wiki/Artificial_intelligence) / [Large Language Models](https://en.wikipedia.org/wiki/Large_language_model) to you. 🤖

It supports [OpenAI](https://openai.com/)'s [ChatGPT](https://openai.com/blog/chatgpt/) models, as well as many other [☁️ providers](https://github.com/etkecc/baibot/blob/main/docs/providers.md).

It's designed as a more private and [✨ featureful](https://github.com/etkecc/baibot/?tab=readme-ov-file#-features) alternative to the now-unmaintained [matrix-chatgpt-bot](./docs/configuring-playbook-bot-chatgpt.md).

To get started, see the [Setting up baibot](./docs/configuring-playbook-bot-baibot.md) documentation page.

## Switching synapse-admin to etke.cc's fork

The playbook now installs [etke.cc](https://etke.cc/)'s [fork](https://github.com/etkecc/synapse-admin) of [synapse-admin](https://github.com/Awesome-Technologies/synapse-admin) (originally developed by [Awesome-Technologies](https://github.com/Awesome-Technologies)). This fork is a drop-in replacement for the original software.

The creation of the fork has been provoked by users frequently encountering issues with the original synapse-admin software, such as unintentionally deleting their one-and-only admin user account (fixed [here](https://github.com/etkecc/synapse-admin/pull/1) and also contributed upstream [here](https://github.com/Awesome-Technologies/synapse-admin/pull/608) — to no avail for now). Since its inception, [a bunch of other quality-of-life improvements](https://github.com/etkecc/synapse-admin?tab=readme-ov-file#changes) have been made to the fork.

If upstream synapse-admin picks up the pace and improves, the etke.cc fork may disappear and the playbook may switch to the original software again. Until that time comes, we believe that etke.cc's fork is the better software to use right now.

If you'd like to switch back to the original synapse-admin software, you can do so by adding the following configuration to your `vars.yml` file:

```yaml
matrix_synapse_admin_docker_image: "{{ matrix_synapse_admin_docker_image_registry_prefix }}awesometechnologies/synapse-admin:{{ matrix_synapse_admin_version }}"
matrix_synapse_admin_docker_image_registry_prefix_upstream: docker.io/

matrix_synapse_admin_version: 0.10.3

# If you need self-building (if running on arm32), uncomment this.
# matrix_synapse_admin_container_image_self_build_repo: "https://github.com/Awesome-Technologies/synapse-admin.git"
```


# 2024-08-17

## New appservice-double-puppet service for better double-puppeting

Mautrix bridges are undergoing large changes as announced in the [August 2024 releases & progress](https://mau.fi/blog/2024-08-mautrix-release/) blog post.

The playbook has already upgraded to the rewritten mautrix-slack ([v0.1.0](https://github.com/mautrix/slack/releases/tag/v0.1.0)) and mautrix-signal ([v0.7.0](https://github.com/mautrix/signal/releases/tag/v0.7.0)) bridges.

The newly rewritten bridges do not support double-puppeting via [Shared Secret Auth](./docs/configuring-playbook-shared-secret-auth.md) anymore, which has prompted us to switch to the new & better [appservice method](https://docs.mau.fi/bridges/general/double-puppeting.html#appservice-method-new) for double-puppeting. The playbook automates this double-puppeting setup for you if you enable the new [Appservice Double Puppet](./docs/configuring-playbook-appservice-double-puppet.md) service.

All non-deprecated mautrix bridges in the playbook have been reworked to support double-puppeting via an Appservice. Most bridges still support double-puppeting via [Shared Secret Auth](./docs/configuring-playbook-shared-secret-auth.md), so the playbook supports it too. If only Shared Secret Auth is enabled, double-puppeting will be configured using that method (for the bridges that support it). That said, **Shared Secret Auth double-puppeting is being phased out and we recommend replacing it with the new Appservice method**.

We recommend **enabling double-puppeting via the new Appservice method** by adding the following configuration to your `vars.yml` file:

```yaml
matrix_appservice_double_puppet_enabled: true
```

You can still **keep** [Shared Secret Auth](./docs/configuring-playbook-shared-secret-auth.md) enabled. Non-mautrix bridges and other services (e.g. [matrix-corporal](./docs/configuring-playbook-matrix-corporal.md)) may still require it.

When both double-puppeting methods are enabled, the playbook will automatically choose the new and better Appservice method for bridges that support it.


# 2024-08-15

## matrix-media-repo now configured for Authenticated Media

Thanks to [Michael Hollister](https://github.com/Michael-Hollister) from [FUTO](https://www.futo.org/), our matrix-media-repo implementation now automatically [sets up signing keys](https://docs.t2bot.io/matrix-media-repo/v1.3.5/installation/signing-key/) for Authenticated Media (as per [MSC3916](https://github.com/matrix-org/matrix-spec-proposals/pull/3916)).

If you had never heard of Authenticated Media before, the [Sunsetting unauthenticated media](https://matrix.org/blog/2024/06/26/sunsetting-unauthenticated-media/) article on [matrix.org](https://matrix.org/) is a good introduction.

This feature is enabled for matrix-media-repo installations by default and will append an additional (matrix-media-repo-generated signing key) to your homeserver's (Synapse or Dendrite) signing key. See the [Signing keys](./docs/configuring-playbook-matrix-media-repo.md#signing-keys) and [Key backup and revoking](./docs/configuring-playbook-matrix-media-repo.md#key-backup-and-revoking) sections of the matrix-media-repo documentation for more details.

If you'd like to avoid this new feature, you can disable it by setting `matrix_media_repo_generate_signing_key: false` in your `vars.yml` configuration file.


# 2024-08-08

## (Backward Compatibility Break) matrix-corporal has been upgraded to v3

The playbook now installs [matrix-corporal](https://github.com/devture/matrix-corporal) v3.0.0, which brings support for **power-level management** (thanks to [this PR](https://github.com/devture/matrix-corporal/pull/32)).

This upgrade necessitates configuration policy changes as described in [matrix-corporal's changelog entry](https://github.com/devture/matrix-corporal/blob/5287cb81c82cd3b951c2a099b4697c3e0b384559/CHANGELOG.md#version-300-2024-08-08).

If you'd like to remain on the old (v2) version of matrix-corporal, you can do so by adding the following configuration to your `vars.yml` file:

```yaml
matrix_corporal_version: 2.8.0
```

# 2024-07-25

## synapse-usage-exporter support

Thanks to [Michael Hollister](https://github.com/Michael-Hollister) from [FUTO](https://www.futo.org/), the creators of the [Circles app](https://circu.li/), the playbook can now set up [synapse-usage-exporter](https://github.com/loelkes/synapse-usage-exporter) — a small [Flask](https://flask.palletsprojects.com)-based webservice which can capture usage statistics from Synapse (via HTTP `PUT`) and then make them available for Prometheus to scrape.

To learn more see our [Enabling synapse-usage-exporter for Synapse usage statistics](docs/configuring-playbook-synapse-usage-exporter.md) documentation page.


# 2024-07-06

## matrix-alertmanager-receiver support

For those wishing to more easily integrate [Prometheus](https://prometheus.io/)' alerting service ([Alertmanager](https://prometheus.io/docs/alerting/latest/alertmanager/)) with Matrix, the playbook can now set up [matrix-alertmanager-receiver](https://github.com/metio/matrix-alertmanager-receiver).

See [Setting up Prometheus Alertmanager integration via matrix-alertmanager-receiver](./docs/configuring-playbook-alertmanager-receiver.md) for more details.

## Traefik v3 and HTTP/3 are here now

**TLDR**: Traefik was migrated from v2 to v3. Minor changes were done to the playbook. Mostly everything else worked out of the box. Most people will not have to do any tweaks to their configuration. In addition, [HTTP/3](https://en.wikipedia.org/wiki/HTTP/3) support is now auto-enabled for the `web-secure` (port 443) and `matrix-federation` (port `8448`) entrypoints. If you have a firewall in front of your server and you wish to benefit from `HTTP3`, you will need to open the `443` and `8448` UDP ports in it.

### Traefik v3

The reverse-proxy that the playbook uses by default (Traefik) has recently been upgraded to v3 (see [this blog post](https://traefik.io/blog/announcing-traefik-proxy-v3-rc/) to learn about its new features). Version 3 includes some small breaking configuration changes requiring a [migration](https://doc.traefik.io/traefik/migration/v2-to-v3/).

We have **updated the playbook to Traefik v3** (make sure to run `just roles` / `make roles` to get it).

There were **only minor playbook changes required** to adapt to Traefik v3, and only to the Ansible role for [matrix-media-repo](./docs/configuring-playbook-matrix-media-repo.md) where we changed a few [`PathPrefix` instances to `PathRegexp`](https://doc.traefik.io/traefik/routing/routers/#path-pathprefix-and-pathregexp), because these instances were using a regular expression instead of a fixed path. For fixed-path values, `PathPrefix` is still the preferred matcher function to use.

**Most people using the playbook should not have to do any changes**.

If you're using the playbook's Traefik instance to reverse-proxy to some other services of your own (not managed by the playbook), you may wish to review their Traefik labels and make sure they're in line with the [Traefik v2 to v3 migration guide](https://doc.traefik.io/traefik/migration/v2-to-v3/).

If you've tweaked any of this playbook's `_path_prefix` variables and made them use a regular expression, you will now need to make additional adjustments. The playbook makes extensive use of `PathPrefix()` matchers in Traefik rules and `PathPrefix` does not support regular expressions anymore. To work around it, you may now need to override a whole `_traefik_rule` variable and switch it from [`PathPrefix` to `PathRegexp`](https://doc.traefik.io/traefik/routing/routers/#path-pathprefix-and-pathregexp).

If you're not using [matrix-media-repo](./docs/configuring-playbook-matrix-media-repo.md) (the only role we had to tweak to adapt it to Traefik v3), you **may potentially downgrade to Traefik v2** (if necessary) by adding `traefik_verison: v2.11.4` to your configuration. People using `matrix-media-repo` cannot downgrade this way, because `matrix-media-repo` has been adjusted to use `PathRegexp` — a [routing matcher](https://doc.traefik.io/traefik/v2.11/routing/routers/#rule) that Traefik v2 does not understand.

### HTTP/3 is enabled by default

In Traefik v3, [HTTP/3](https://en.wikipedia.org/wiki/HTTP/3) support is no longer considered experimental now. Due to this, **the playbook auto-enables HTTP3** for the `web-secure` (port 443) and `matrix-federation` (port `8448`) entrypoints.

HTTP3 uses the UDP protocol and **the playbook (together with Docker) will make sure that the appropriate ports** (`443` over UDP & `8448` over UDP) **are exposed and whitelisted in your server's firewall**. However, **if you have another firewall in front of your server** (as is the case for many cloud providers), **you will need to manually open these UDP ports**.

If you do not open the UDP ports correctly or there is some other issue, clients (browsers, mostly) will fall-back to [HTTP/2](https://en.wikipedia.org/wiki/HTTP/2) or even [HTTP/1.1](https://en.wikipedia.org/wiki/HTTP).

Still, if HTTP/3 cannot function correctly in your setup, it's best to disable advertising support for it (and misleading clients into trying to use HTTP/3).

To **disable HTTP/3**, you can use the following configuration:

```yaml
traefik_config_entrypoint_web_secure_http3_enabled: false

# Disabling HTTP/3 for the web-secure entrypoint (above),
# automatically disables it for the Matrix Federation entrypoint as well,
# so you do not necessarily need the configuration line below.
#
# Feel free to only keep it around if you're keeping HTTP/3 enabled for web-secure (by removing the line above),
# and would only like to disable HTTP/3 for the Matrix Federation entrypoint.
matrix_playbook_public_matrix_federation_api_traefik_entrypoint_config_http3_enabled: false
```

If you are using [your own webserver](./docs/configuring-playbook-own-webserver.md) (in front of Traefik), port binding on UDP port `8448` by default due to HTTP/3 is either unnecessary or [may get in the way](https://github.com/spantaleev/matrix-docker-ansible-deploy/issues/3402). If it does, you can disable it:

```yaml
# Disable HTTP/3 for the federation entrypoint.
# If you'd like HTTP/3, consider configuring it for your other reverse-proxy.
#
# Disabling this also sets `matrix_playbook_public_matrix_federation_api_traefik_entrypoint_host_bind_port_udp` to an empty value.
# If you'd like to keep HTTP/3 enabled here (for whatever reason), you may wish to explicitly
# set `matrix_playbook_public_matrix_federation_api_traefik_entrypoint_host_bind_port_udp` to something like '127.0.0.1:8449'.
matrix_playbook_public_matrix_federation_api_traefik_entrypoint_config_http3_enabled: false
```


# 2024-07-01

## synapse-admin is now restricted to your homeserver's URL by default

A new feature introduced in synapse-admin [v0.10.0](https://github.com/Awesome-Technologies/synapse-admin/releases/tag/0.10.0) (released and supported by the playbook since a a few months ago) provides the ability to [restrict its usage to a specific homeserver](https://github.com/Awesome-Technologies/synapse-admin/blob/e21e44362c879ac41f47c580b04210842b6ff3d7/README.md#restricting-available-homeserver) (or multiple homeservers).

The playbook has just started making use of this feature. **From now on, your synapse-admin instance will be restricted to the homeserver you're managing via the playbook**. When configured like this, the *Homeserver URL* field in synapse-admin's web UI changes from a text field to a dropdown having a single value (the URL of your homeserver). This makes usage simpler for most people, as they won't need to manually enter a *Homeserver URL* anymore.

If you'd like **to go back to the old unrestricted behavior**, use the following configuration:

```yaml
# Use this configuration to allow synapse-admin to manage any homeserver instance.
matrix_synapse_admin_config_restrictBaseUrl: []
```


# 2024-06-25

## The URL-prefix for Hookshot generic webhooks has changed

Until now, generic Hookshot webhook URLs looked like this: `https://matrix.example.com/hookshot/webhooks/:hookId`.

The `/hookshot/webhooks` common prefix gets stripped by Traefik automatically, so Hookshot only sees the part that comes after (`/:hookId`).

[A few years ago](https://github.com/spantaleev/matrix-docker-ansible-deploy/issues/1681), Hookshot started to prefer to handle webhooks at a `/webhook/:hookId` path (instead of directly at `/:hookId`).

To avoid future problems, we've [reconfigured](https://github.com/spantaleev/matrix-docker-ansible-deploy/commit/4704a60718946fd469aeee7fc3ae8127c633bb6b) our Hookshot configuration to use webhook URLs that include `/webhook` in the URL suffix (e.g. `/hookshot/webhooks/webhook/:hookId`, instead of `/hookshot/webhooks/:hookId`). This means that when we strip the common prefi (`/hookshot/webhooks`), we'll end up sending `/webhook/:hookId` to Hookshot, just like recommended.

When generating new webhooks, you should start seeing the new URLs being used.

**For now**, **both** old URLs (`/hookshot/webhooks/:hookId`) and new URLs (`/hookshot/webhooks/webhook/:hookId`) **continue to work**, so your webhooks will not break just yet.

However, **we recommend that you update all your old webhook URLs** (configured in other systems) to include the new `/webhook` path component, so that future Hookshot changes (whenever they come) will not break your webhooks. You don't need to do anything on the Hookshot side — you merely need to reconfigure the remote systems that use your webhook URLs.


# 2024-06-22

## The maubot user is now managed by the playbook

To make things easier and to be consistent with other roles, the [maubot](./docs/configuring-playbook-bot-maubot.md) user (`bot.maubot` by default) is [now](https://github.com/spantaleev/matrix-docker-ansible-deploy/pull/3376) automatically created be the playbook.

If you have an existing maubot installation, you will need to specify `matrix_bot_maubot_initial_password` in your `vars.yml` file to make the playbook not complain about it being undefined. Since the bot is already registered in your installation, there's nothing for the playbook to do anyway. In case you don't remember the password you've registered your maubot user account with, you can specify any value for this variable.

If you've registered another username for the bot (other than the recommended default of `bot.maubot`), consider adjusting the `matrix_bot_maubot_login` variable (e.g. `matrix_bot_maubot_login: my.maubot.username`).


# 2024-06-03

## WeChat bridging support

Thanks to [Tobias Diez](https://github.com/tobiasdiez)'s [efforts](https://github.com/spantaleev/matrix-docker-ansible-deploy/pull/3241), the playbook now supports bridging to [WeChat](https://www.wechat.com/) via the [matrix-wechat](https://github.com/duo/matrix-wechat) bridge.

See our [Setting up WeChat bridging](docs/configuring-playbook-bridge-wechat.md) documentation page for getting started.


# 2024-03-26

## (Backward Compatibility Break) The playbook now defaults to KeyDB, instead of Redis

**TLDR**: if the playbook used installed Redis as a dependency for you before, it will now replace it with [KeyDB](https://docs.keydb.dev/) (a drop-in alternative) due to [Redis having changed its license](https://redis.com/blog/redis-adopts-dual-source-available-licensing/).

Thanks to [Aine](https://gitlab.com/etke.cc) of [etke.cc](https://etke.cc/), the playbook now uses [KeyDB](https://docs.keydb.dev/) (a drop-in alternative for Redis), instead of [Redis](https://redis.io/).

The playbook used to install Redis (and now installs KeyDB in its place) if services have a need for it ([enabling worker support for Synapse](docs/configuring-playbook-synapse.md#load-balancing-with-workers), [enabling Hookshot encryption](docs/configuring-playbook-bridge-hookshot.md#end-to-bridge-encryption), etc.) or if you explicitly enabled the service (`redis_enabled: true` or `keydb_enabled: true`).

This change is provoked by the fact that [Redis is now "source available"](https://redis.com/blog/redis-adopts-dual-source-available-licensing/). According to the Limitations of [the new license](https://redis.com/legal/rsalv2-agreement/) (as best as we understand them, given that we're not lawyers), using Redis in the playbook (even in a commercial FOSS service like [etke.cc](https://etke.cc/)) does not violate the new Redis license. That said, we'd rather neither risk it, nor endorse shady licenses and products that pretend to be free-software. Another high-quality alternative to Redis seems to be [Dragonfly](https://www.dragonflydb.io/), but the [Dragonfly license](https://github.com/dragonflydb/dragonfly?tab=License-1-ov-file#readme) is no better than Redis's.

Next time your run the playbook (via the `setup-all` tag), **Redis will be automatically uninstalled and replaced with KeyDB**. Some Synapse downtime may occur while the switch happens.

Users on `arm32` should be aware that there's **neither a prebuilt `arm32` container image for KeyDB**, nor the KeyDB role supports self-building yet. Users on this architecture likely don't run Synapse with workers, etc., so they're likely in no need of KeyDB (or Redis). If Redis is necessary in an `arm32` deployment, disabling KeyDB and making the playbook fall back to Redis is possible (see below).

**The playbook still supports Redis** and you can keep using Redis (for now) if you'd like, by adding this additional configuration to your `vars.yml` file:

```yaml
# Explicitly disable KeyDB, which will auto-enable Redis
# if the playbook requires it as a dependency for its operation.
keydb_enabled: false
```


# 2024-03-24

## Initial work on IPv6 support

Thanks to [Tilo Spannagel](https://github.com/tilosp), the playbook can now enable IPv6 for container networks for various components (roles) via [the `devture_systemd_docker_base_ipv6_enabled` variable](https://github.com/devture/com.devture.ansible.role.systemd_docker_base/blob/c11a526bb8e318b42eb52055056377bb31154f13/defaults/main.yml#L14-L31).

It should be noted that:

- Matrix roles (`roles/custom/matrix-*`) respect this variable, but external roles (those defined in `requirements.yml` and installed via `just roles`) do not respect it yet. Additional work is necessary
- changing the variable subsequently may not change existing container networks. Refer to [these instructions](https://github.com/devture/com.devture.ansible.role.systemd_docker_base/blob/c11a526bb8e318b42eb52055056377bb31154f13/defaults/main.yml#L26-L30)
- this is all very new and untested

## Pantalaimon support

Thanks to [Julian Foad](https://matrix.to/#/@julian:foad.me.uk), the playbook can now install the [Pantalaimon](https://github.com/matrix-org/pantalaimon) E2EE aware proxy daemon for you. It's already possible to integrate it with [Draupnir](docs/configuring-playbook-bot-draupnir.md) to allow it to work in E2EE rooms — see our Draupnir docs for details.

See our [Setting up Pantalaimon](docs/configuring-playbook-pantalaimon.md) documentation to get started.


# 2024-03-05

## Support for Draupnir-for-all

Thanks to [FSG-Cat](https://github.com/FSG-Cat), the playbook can now install [Draupnir for all](./docs/configuring-playbook-appservice-draupnir-for-all.md) (aka multi-instance Draupnir running in appservice mode).

This is an alternative to [running Draupnir in bot mode](./docs/configuring-playbook-bot-draupnir.md), which is still supported by the playbook.

The documentation page for [Draupnir for all](./docs/configuring-playbook-appservice-draupnir-for-all.md) contains more information on how to install it.


# 2024-02-19

## Support for bridging to Facebook/Messenger via the new mautrix-meta bridge

The [mautrix-facebook](./docs/configuring-playbook-bridge-mautrix-facebook.md) and [mautrix-instagram](./docs/configuring-playbook-bridge-mautrix-instagram.md) bridges are being [superseded by a new bridge](https://github.com/mautrix/facebook/issues/332) — the [mautrix-meta](https://github.com/mautrix/meta) bridge.

The playbook now supports the new mautrix-meta bridge — a single bridge, which can run in different modes and bridge to Messenger (via [Facebook](https://facebook.com/), Facebook over [Tor](https://www.torproject.org/) or via [Messenger](https://messenger.com/)) and [Instagram](https://instagram.com/). The playbook makes this bridge available via 2 separate Ansible roles, allowing you to easily run 2 instances of mautrix-meta, for bridging to both services at the same time.

If you're using mautrix-facebook or mautrix-instagram right now, **you can still continue using the old bridges, but may wish to change to the new bridge implementations**. See:

- [Setting up Instagram bridging via Mautrix Meta](docs/configuring-playbook-bridge-mautrix-meta-instagram.md)

- [Setting up Messenger bridging via Mautrix Meta](docs/configuring-playbook-bridge-mautrix-meta-messenger.md)

The documentation pages contain more information on how to migrate.


# 2024-02-14

## Much larger Synapse caches and cache auto-tuning enabled by default

Thanks to [FSG-Cat](https://github.com/FSG-Cat), the playbook now uses much larger caches and enables Synapse's [cache auto-tuning functionality](https://matrix-org.github.io/synapse/latest/usage/configuration/config_documentation.html#caches-and-associated-values). This work and the default values used by the playbook are inspired by [Tom Foster](https://github.com/tcpipuk)'s [Synapse homeserver guide](https://tcpipuk.github.io/synapse/deployment/synapse.html).

The playbook has always used a very conservative cache factor (`matrix_synapse_caches_global_factor`) value of `0.5`, which may be OK for small and underactive deployments, but is not ideal for larger servers. Paradoxically, a small global cache factor value [does not necessarily decrease RAM usage as a whole](https://github.com/matrix-org/synapse/issues/3939).

The playbook now uses **a 20x larger cache factor** (currently `10`), adjusts a few other cache-related variables, and **enables cache auto-tuning** via the following variables:

- `matrix_synapse_cache_autotuning_max_cache_memory_usage` — defaults to 1/8 of total RAM with a cap of 2GB; values are specified in bytes
- `matrix_synapse_cache_autotuning_target_cache_memory_usage` — defaults to 1/16 of total RAM with a cap of 1GB; values are specified in bytes
- `matrix_synapse_cache_autotuning_min_cache_ttl` — defaults to `30s`

These values should be good defaults for most servers, but may change over time as we experiment further.

Refer to our new [Tuning caches and cache autotuning](docs/maintenance-synapse.md#tuning-caches-and-cache-autotuning) documentation section for more details.


# 2024-01-31

## (Backward-compatibility break) Minor changes necessary for some people serving a static website at the base domain

This only affects people who are [Serving a static website at the base domain](./docs/configuring-playbook-base-domain-serving.md#serving-a-static-website-at-the-base-domain), but not managing its `index.html` through the playbook.

That is, for people who have `matrix_static_files_file_index_html_enabled: false` in their `vars.yml` configuration, the playbook has a new default behavior. Since the playbook is not managing the `index.html` file, it will default to a more sensible way of handling the base domain — redirecting `https://example.com/` to `https://matrix.example.com/`, instead of serving a 404 page.

If you are managing your static website by yourself (by dropping files into `/matrix/static-files/public` somehow), then you probably don't wish for such redirection to happen. You can disable it by adding `matrix_static_files_container_labels_base_domain_root_path_redirection_enabled: false` to your `vars.yml` configuration file.


# 2024-01-20

## Support for more efficient (specialized) Synapse workers

Thanks to [Charles Wright](https://github.com/cvwright) from [FUTO](https://www.futo.org/), the creators of the [Circles app](https://circu.li/), the playbook has [received support](https://github.com/spantaleev/matrix-docker-ansible-deploy/pull/3100) for load-balancing the Synapse workload via [specialized workers](./docs/configuring-playbook-synapse.md#specialized-workers) which are supposed to work better than our old [generic workers](./docs/configuring-playbook-synapse.md#generic-workers) implementation.

For now, playbook defaults remain unchanged and the `one-of-each` [workers preset](./docs/configuring-playbook-synapse.md#worker-presets) continues being the default. However, the default may change in the future. If you'd like to remain on this preset even if/when the defaults change, consider explicitly adding `matrix_synapse_workers_preset: one-of-each` to your `vars.yml` configuration.

Our specialized workers setup is based on recommendations found in [Tom Foster](https://github.com/tcpipuk)'s [Synapse homeserver guide](https://tcpipuk.github.io/synapse/index.html). What's special about our new setup is that we try to parse information out of the request (who the user is; which room is being operated on) and try to forward similar requests to the same worker. As an example, this means that once a worker caches some room information, subsequent requests for the same room will be routed to the same worker (which supposedly still has the room's state cached).

To get started, refer to our [Specialized workers](./docs/configuring-playbook-synapse.md#specialized-workers) documentation section.


# 2024-01-17

## Switching to Element's AGPLv3-licensed Synapse release

A few months ago, the [Element](https://element.io/) company has [announced](https://element.io/blog/element-to-adopt-agplv3/) that their work on the Synapse homeserver would no longer be available under the permissive [Apache-2.0 license](https://www.apache.org/licenses/LICENSE-2.0), but only under:

- the [AGPLv3](https://www.gnu.org/licenses/agpl-3.0.en.html) free-software license — the same license that this Ansible playbook has always used
- a proprietary license, for those wishing for Element to [sell them an exception](https://gnu.org/philosophy/selling-exceptions.html) to the AGPLv3 license

You can also learn more in [this post](https://matrix.org/blog/2023/11/06/future-of-synapse-dendrite/) by the Matrix Foundation.

The change has [already happened](https://element.io/blog/synapse-now-lives-at-github-com-element-hq-synapse/) and the first Synapse release under the new license is here: [v1.99.0](https://github.com/element-hq/synapse/releases/tag/v1.99.0).

There is no up-to-date alternative Synapse fork right now and this free-software (AGPLv3-licensed) playbook is definitely not against free-software licenses, so we are now switching to the Element-maintained Synapse release.

**What does this mean to you?**

For most home users, it doesn't mean anything. Your installation will continue working as it should and you don't need to do anything.

For people building commercial products on top of Synapse, they may have to either buy a license exception from Element (from what we hear, the fee depends on the number of monthly-active users on your instance) or they may need to release all related code as free-software (which is what we've been doing at [etke.cc](https://etke.cc/) ([here](https://gitlab.com/etke.cc)) all along).

We're no lawyers and this changelog entry does not aim to give you the best legal advice, so please research on your own!

If you'd like to continue using the old Apache-2.0-licensed Synapse (for a while longer anyway), the playbook makes it possible by introducing a new Ansible variable. You can do it like this:

```yaml
# Switch the organization that Synapse container images (or source code for self-building) are pulled from.
# Note: the new default value is `element-hq/synapse`.
matrix_synapse_github_org_and_repo: matrix-org/synapse

# Pin the Synapse version to the last one (v1.98.0) released by the Matrix Foundation
# under the old permissive Apache-2.0 license.
matrix_synapse_version: v1.98.0
```

Notes:

- if you had already upgraded Synapse to `v1.99.0` by running this playbook, you will still be able to downgrade to `v1.98.0`, because both releases use the same database schema version (`SCHEMA_COMPAT_VERSION = 83` — see [here for v1.98.0](https://github.com/element-hq/synapse/blob/v1.98.0/synapse/storage/schema/__init__.py#L131-L134) and [here for v1.99.0](https://github.com/element-hq/synapse/blob/v1.99.0/synapse/storage/schema/__init__.py#L137-L140)). More details on Synapse's database schema are available [here](https://element-hq.github.io/synapse/develop/development/database_schema.html). It appears that there are no new database migrations introduced in `v1.99.0`, so going back to the older release is possible. This is not guaranteed to hold true for future Synapse releases, so if you're seeing this early-enough, consider pinning the version and organization before re-running the playbook and getting upgraded to the latest version

- running an outdated homeserver exposes you to security issues and incompatibilities. Only consider doing this as a short-term solution.

# 2024-01-16

## `Draupnir` has been relicensed to AFL-3.0

As of [#204](https://github.com/the-draupnir-project/Draupnir/pull/204) Draupnir changed its licence to AFL-3.0 from the CSL licence. This change affects playbook users who could not run Draupnir under the old license restrictions. The new license is considerably less restrictive and is OSI approved. Draupnir version v1.86.0 and later are covered by this license change.

# 2024-01-15

## Goodbye, `matrix-nginx-proxy` 🪦

**TLDR**: All traces of the `matrix-nginx-proxy` reverse-proxy component are now gone. This brought about many other internal changes (and security improvements), so setups may need minor adjustments or suffer some (temporary) breakage. People who have been on the Traefik-native setup may upgrade without much issues. Those running their own Traefik instance may need minor changes. People who have been postponing the migration away from `matrix-nginx-proxy` (for more than a year already!) will now finally need to do something about it.

### Backstory on `matrix-nginx-proxy`

We gather here today to celebrate the loss of a once-beloved component in our stack — `matrix-nginx-proxy`. It's been our [nginx](https://nginx.org/)-based reverse-proxy of choice since the [first commit](https://github.com/spantaleev/matrix-docker-ansible-deploy/tree/87f5883f2455fb115457b65f267f17de305c053c) of this playbook, 7 years ago.

For 6 years, `matrix-nginx-proxy` has been the front-most reverse-proxy in our setup (doing SSL termination, etc.). After [transitioning to Traefik last year](#traefik-is-the-default-reverse-proxy-now), `matrix-nginx-proxy` took a step back. Nevertheless, since it was so ingrained into the playbook, it still remained in use — even if only internally. Despite our warnings of its imminent death, many of you have indubitably continued to use it instead of Traefik. Its suffering continued for too long, because it served many different purposes and massive effort was required to transition them to others.

To us, `matrix-nginx-proxy` was:

- an [nginx](https://nginx.org/)-based reverse-proxy
- an Ansible role organizing the work of [certbot](https://certbot.eff.org/) — retrieving free [Let's Encrypt](https://letsencrypt.org/) SSL certificates for `matrix-nginx-proxy` and for the [coturn TURN server](./docs/configuring-playbook-turn.md)
- a central component for reverse-proxying to the [long list of services](./docs/configuring-playbook.md) supported by the playbook. As such, it became a dependency that all these services had to inject themselves into during runtime
- an intermediary through which addons (bridges, bots) communicated with the homeserver. Going through an intermediary (instead of directly talking to the homeserver) is useful when certain components (like [matrix-media-repo](./docs/configuring-playbook-matrix-media-repo.md) or [matrix-corporal](./docs/configuring-playbook-matrix-corporal.md)) are enabled, because it lets these services "steal routes" from the homeserver
- a webserver for serving the `/.well-known/matrix` static files (generated by the `matrix-base` role until now)
- a webserver [serving your base domain](./docs/configuring-playbook-base-domain-serving.md) (and also generating the `index.html` page for it)
- a central component providing global [HTTP Basic Auth](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication) password-protection for all `/metrics` endpoints when metrics were exposed publicly for consumption from a remote Prometheus server

Talk about a jack of all trades! The [UNIX philosophy](https://en.wikipedia.org/wiki/Unix_philosophy) (and Docker container philosophy) of "do one thing and do it well" had been severely violated for too long.

On a related note, we also had a large chain of reverse-proxies in the mix. In the worst case, it was something like this: (Traefik -> `matrix-nginx-proxy:8080` -> `matrix-nginx-proxy:12080` -> `matrix-synapse-reverse-proxy-companion:8008` -> `matrix-synapse:8008`).

Due to complexity and the playbook's flexibility (trying to accommodate a mix of tens of components), many layers of indirection were necessary. We do like reverse-proxies, but… not quite enough to enjoy going through a chain of ~4 of them before reaching the target service.

After **a ton of work** in the last weeks (200+ commits, which changed 467 files - 8684 insertions and 8913 deletions), **we're finally saying goodbye** to `matrix-nginx-proxy`.

### Going Traefik-native and cutting out all middlemen

In our new setup, you'll see the bare minimum number of reverse-proxies.

In most cases, there's only Traefik and all services being registered directly with it. When [Synapse workers](./docs/configuring-playbook-synapse.md#load-balancing-with-workers) are enabled, `matrix-synapse-reverse-proxy-companion` remains as an extra reverse-proxy that requests go through (for load-balancing to the correct Synapse worker), but in all other cases services are exposed directly.

This reduces "network" hops (improving performance) and also decreases the number of components (containers). Each Ansible role in our setup is now independent and doesn't need to interact with other roles during runtime.

### Traefik now has an extra job

Previously, **Traefik had a single purpose** — being the main reverse-proxy. It was either front-most (terminating SSL, etc.) or you were [fronting Traefik with your own other reverse-proxy](./docs/configuring-playbook-own-webserver.md#fronting-the-integrated-reverse-proxy-webserver-with-another-reverse-proxy). In any case — it had this central (yet decentralized) job.

Now, **Traefik has one more role** — it serves as an intermediary which allows addon services (bridges, bots, etc.) to communicate with the homeserver. As mentioned above, such an intermediary service is not strictly necessary in all kinds of setups, but more complex setups (including [matrix-media-repo](./docs/configuring-playbook-matrix-media-repo.md) or [matrix-corporal](./docs/configuring-playbook-matrix-corporal.md)) benefit from it.

To perform this new role, Traefik now has a new internal [entrypoint](https://doc.traefik.io/traefik/routing/entrypoints/) called `matrix-internal-matrix-client-api`. All homeservers (Conduit, Dendrite, Synapse and even `matrix-synapse-reverse-proxy-companion`) and homeserver-related core services ([matrix-media-repo](./docs/configuring-playbook-matrix-media-repo.md), [matrix-corporal](./docs/configuring-playbook-matrix-corporal.md) and potentially others) register their routes (using [container labels](https://docs.docker.com/config/labels-custom-metadata/)) not only on the public entrypoints (`web-secure`, `matrix-federation`), but also on this new internal entrypoint.

Doing so, services can contact Traefik on this entrypoint's dedicated port (the URL defaults to `http://matrix-traefik:8008`) and reach the homeserver Client-Server API as they expect. Internally, Traefik takes care of the routing to the correct service.

We've also considered keeping it simple and having services talk to the homeserver over the public internet (e.g. `https://matrix.example.com`) thus reusing all existing Traefik routing labels. In this scenario, performance was incredibly poor (e.g. 70 rps, instead of 1400 rps) due to TLS and networking overhead. The need for fast internal communication (via the new internal non-TLS-enabled Traefik entrypoint) is definitely there. In our benchmarks, Traefik even proved more efficient than nginx at doing this: ~1200 rps for Traefik compared to ~900 rps for nginx (out of ~1400 rps when talking to the Synapse homeserver directly).

Traefik serving this second purpose has a few downsides:

- Traefik becomes a runtime dependency for all homeserver-dependant container services
- all homeserver-dependant services now need to be connected to the `traefik` container network, even if they don't need public internet exposure

Despite these downsides (which the playbook manages automatically), we believe it's still a good compromise given the amount of complexity it eliminates and the performance benefits it yields. One alternative we've [considered](https://github.com/spantaleev/matrix-docker-ansible-deploy/pull/3045#issuecomment-1867327001) was adding a new intermediary service (e.g. `matrix-homeserver-proxy` powered by nginx), but this both had much higher complexity (one more component in the mix; duplication of effort to produce nginx-compatible route definitions for it) and slightly worse performance (see above).

People running the default Traefik setup do not need to do anything to make Traefik take on this extra job. Your Traefik configuration will be updated automatically.

**People running their own Traefik reverse-proxy need to do [minor adjustments](#people-managing-their-own-traefik-instance-need-to-do-minor-changes)**, as described in the section below.

You may disable Traefik acting as an intermediary by explicitly setting `matrix_playbook_public_matrix_federation_api_traefik_entrypoint_enabled` to `false`. Services would then be configured to talk to the homeserver directly, giving you a slight performance boost and a "simpler" Traefik setup. However, such a configuration is less tested and will cause troubles, especially if you enable more services (like `matrix-media-repo`, etc.) in the future. As such, it's not recommended.

### People managing their own Traefik instance need to do minor changes

This section is for people [managing their own Traefik instance on the Matrix server](./docs/configuring-playbook-own-webserver.md#traefik-managed-by-you). Those [using Traefik managed by the playbook](./docs/configuring-playbook-own-webserver.md#traefik-managed-by-the-playbook) don't need to do any changes.

Because [Traefik has an extra job now](#traefik-now-has-an-extra-job), you need to adapt your configuration to add the additional `matrix-internal-matrix-client-api` entrypoint and potentially configure the `matrix_playbook_reverse_proxy_container_network` variable. See the [Traefik managed by you](./docs/configuring-playbook-own-webserver.md#traefik-managed-by-you) documentation section for more details.

### People fronting Traefik with another reverse proxy need to do minor changes

We've already previously mentioned that you need to do some minor [configuration changes related to `traefik_additional_entrypoints_auto`](#backward-compatibility-configuration-changes-required-for-people-fronting-the-integrated-reverse-proxy-webserver-with-another-reverse-proxy).

If you don't do these changes (switching from `traefik_additional_entrypoints_auto` to multiple other variables), your Traefik setup will not automatically receive the new `matrix-internal-matrix-client-api` Traefik entrypoint and Traefik would not be able to perform [its new duty of connecting addons with the homeserver](#traefik-now-has-an-extra-job).

### Supported reverse proxy types are now fewer

This section is for people using a more custom reverse-proxy setup — those having `matrix_playbook_reverse_proxy_type` set to a value different than the default (`playbook-managed-traefik`).

Previously, we allowed you to set `matrix_playbook_reverse_proxy_type` to 7 different values to accommodate various reverse-proxy setups.

The complexity of this is too high, so we only support 3 values right now:

- (the default) `playbook-managed-traefik`, when you're [using Traefik managed by the playbook](./docs/configuring-playbook-own-webserver.md#traefik-managed-by-the-playbook)
- `other-traefik-container`, when you're [managing your own Traefik instance on the Matrix server](./docs/configuring-playbook-own-webserver.md#traefik-managed-by-you)
- `none`, when you wish for [no reverse-proxy integration to be done at all](./docs/configuring-playbook-own-webserver.md#using-no-reverse-proxy-on-the-matrix-side-at-all)

The `none` value is not recommended and may not work adequately, due to lack of testing and [Traefik's new responsibilities](#traefik-now-has-an-extra-job) in our setup.

**Previous values that are now gone** (and the playbook would report them as such) are: `playbook-managed-nginx`, `other-nginx-non-container`, `other-on-same-host` and `other-on-another-host`.

If you were using these values as a way to stay away from Traefik, you now have 2 options:

- (recommended) [Fronting Traefik with another reverse-proxy](./docs/configuring-playbook-own-webserver.md#fronting-the-integrated-reverse-proxy-webserver-with-another-reverse-proxy)
- (not recommended) [Using no reverse-proxy on the Matrix side at all](./docs/configuring-playbook-own-webserver.md#using-no-reverse-proxy-on-the-matrix-side-at-all) and reverse-proxying to each and every service manually

### Container networking changes

Now that `matrix-nginx-proxy` is not in the mix, it became easier to clear out some other long-overdue technical debt.

Since the very beginning of this playbook, all playbook services were connected to a single (shared) `matrix` container network. Later on, some additional container networks appeared, but most services (database, etc.) still remained in the `matrix` container network. This meant that any random container in this network could try to talk (or attack) the Postgres database operating in the same `matrix` network.

Moving components (especially the database) into other container networks was difficult — it required changes to many other components to ensure correct connectivity.

All the hard work has been done now. We've added much more isolation between services by splitting them up into separate networks (`matrix-homeserver`, `matrix-addons`, `matrix-monitoring`, `matrix-exim-relay`, etc). Components are only joined to the networks they need and should (for the most part) not be able to access unrelated things.

Carrying out these container networking changes necessitated modifying many components, so **we're hoping not too many bugs were introduced in the process**.

We've refrained from creating too many container networks (e.g. one for each component), to avoid exhausting Docker's default network pool and contaminating the container networks list too much.

### Metrics exposure changes

This section is for people who are exposing monitoring metrics publicly, to be consumed by an external Prometheus server.

Previously, `matrix-nginx-proxy` was potentially password-protecting all `/metrics/*` endpoints with the same username and password (specified as plain-text in your `vars.yml` configuration file).

From now on, there are new variables for doing roughly the same — `matrix_metrics_exposure_enabled`, `matrix_metrics_exposure_http_basic_auth_enabled` and `matrix_metrics_exposure_http_basic_auth_users`. See the [Prometheus & Grafana](./docs/configuring-playbook-prometheus-grafana.md) docs page for details.

`matrix-nginx-proxy` is not acting as a "global guardian" anymore. Now, each role provides its own metrics exposure and protection by registering with Traefik. Nevertheless, all roles are wired (via playbook configuration in `group_vars/matrix_servers`) to obey these new `matrix_metrics_exposure_*` variables. We've eliminated the centralization, but have kept the ease of use. Now, you can also do per-service password-protection (with different credentials), should you need to do that for some reason.

The playbook will tell you about all variables that you need to migrate during runtime, so rest assured — you shouldn't be able to miss anything!

### Matrix static files

As mentioned above, static files like `/.well-known/matrix/*` or your base domain's `index.html` file (when [serving the base domain via the Matrix server](./docs/configuring-playbook-base-domain-serving.md) was enabled) were generated by the `matrix-base` or `matrix-nginx-proxy` roles and put into a `/matrix/static-files` directory on the server. Then `matrix-nginx-proxy` was serving all these static files.

All of this has been extracted into a new `matrix-static-files` Ansible role that's part of the playbook. The static files generated by this new role still live at roughly the same place (`/matrix/static-files/public` directory, instead of `/matrix/static-files`).

The playbook will migrate and update the `/.well-known/matrix/*` files automatically but not your own files in `nginx-proxy/data/matrix-domain/` you will need to back these up yourself otherwise they will be lost. It will also warn you about usage of old variable names, so you can adapt to the new names.

### A note on performance

Some of you have been voicing their concerns (for a long time) about Traefik being too slow and nginx being better.

Some online benchmarks support this by demonstrating slightly higher SSL-termination performance in favor of nginx. The upcoming Traefik v3 release is [said to](https://medium.com/beyn-technology/is-nginx-dead-is-traefik-v3-20-faster-than-traefik-v2-f28ffb7eed3e) improve Traefik's SSL performance by some 20%, but that still ends up being somewhat slower than nginx.

We believe that using Traefik provides way too many benefits to worry about this minor performance impairment.

The heaviest part of running a Matrix homeserver is all the slow and potentially inefficient things the homeserver (e.g. Synapse) is doing. These things affect performance much more than whatever reverse-proxy is in front. Your server will die the same way by joining the famously large **Matrix HQ** room, no matter which reverse-proxy you put in front.

Even our previously mentioned benchmarks (yielding ~1300 rps) are synthetic — hitting a useless `/_matrix/client/versions` endpoint. Real-use does much more than this.

If this is still not convincing enough for you and you want the best possible performance, consider [Fronting Traefik with another reverse-proxy](./docs/configuring-playbook-own-webserver.md#fronting-the-integrated-reverse-proxy-webserver-with-another-reverse-proxy) (thus having the slowest part — SSL termination — happen elsewhere) or [Using no reverse-proxy on the Matrix side at all](./docs/configuring-playbook-own-webserver.md#using-no-reverse-proxy-on-the-matrix-side-at-all). The playbook will not get in your way of doing that, but these options may make your life much harder. Performance comes at a cost, after all.

### Migration procedure

The updated playbook will automatically perform some migration tasks for you:

1. It will stop and remove the `matrix-nginx-proxy` systemd service and container for you. This behavior cannot be disabled. It's essential that this service gets stopped, because it remaining running (and having container labels) may confuse Traefik as to where to route HTTP requests.

2. It will delete the `/matrix/nginx-proxy` directory and all files within it. You can disable this behavior by adding `matrix_playbook_migration_matrix_nginx_proxy_uninstallation_enabled: false` to your `vars.yml` configuration file. Doing so will leave its data around.

3. It will delete the `/matrix/ssl` directory and all files within it. You can disable this behavior by adding `matrix_playbook_migration_matrix_ssl_uninstallation_enabled: false` to your `vars.yml` configuration file. If you have some important certificates there for some reason, take them out or temporarily disable removal of these files until you do.

4. It will tell you about all variables (`matrix_nginx_proxy_*` and many others — even from other roles) that have changed during this large nginx-elimination upgrade. You can disable this behavior by adding `matrix_playbook_migration_matrix_nginx_proxy_elimination_variable_transition_checks_enabled: false` to your `vars.yml` configuration file.

5. It will tell you about any leftover `matrix_nginx_proxy_*` variables in your `vars.yml` file. You can disable this behavior by adding `matrix_playbook_migration_matrix_nginx_proxy_leftover_variable_validation_checks_enabled: false` to your `vars.yml` configuration file.

6. It will tell you about any leftover `matrix_ssl_*` variables in your `vars.yml` file. You can disable this behavior by adding `matrix_playbook_migration_matrix_ssl_leftover_variable_checks_enabled: false` to your `vars.yml` configuration file.

We don't recommend changing these variables and suppressing warnings, unless you know what you're doing.

**Most people should just upgrade as per-normal**, bearing in mind that a lot has changed and some issues may arise. The playbook would guide you through renamed variables automatically.

### Conclusion

Thousands of lines of code were changed across hundreds of files. All addons (bridges, bots) were rewired in terms of container networking and in terms of how they reach the homeserver.

I don't actively use all the ~100 components offered by the playbook (no one does), nor do I operate servers exercising all edge-cases. As such, issues may arise. Please have patience and report (or try to fix) these issues!


# 2024-01-14

## (Backward Compatibility) Configuration changes required for people fronting the integrated reverse-proxy webserver with another reverse-proxy

If you're on the default setup (using the Traefik reverse-proxy as installed by the playbook), you don't need to do anything.

People who are [Fronting the integrated Traefik reverse-proxy webserver with another reverse-proxy](./docs/configuring-playbook-own-webserver.md#fronting-the-integrated-reverse-proxy-webserver-with-another-reverse-proxy), as per our previous instructions are redefining `traefik_additional_entrypoints_auto` in their `vars.yml` configuration.

Such a full variable redefinion is intrustive, because it prevents the playbook from injecting additional entrypoints into the Traefik webserver. In the future, the playbook may have a need to do so.

For this reason, we no longer recommend completely redefining `traefik_additional_entrypoints_auto`. The playbook now defines [various `matrix_playbook_public_matrix_federation_api_traefik_entrypoint_*` variables in the `defaults/main.yml` file](https://github.com/spantaleev/matrix-docker-ansible-deploy/blob/master/roles/custom/matrix-base/defaults/main.yml) of the `matrix-base` role which can be used as a safer alternative to `traefik_additional_entrypoints_auto`.

Adapt your configuration as seen below:

```diff
-traefik_additional_entrypoints_auto:
-  - name: matrix-federation
-    port: 8449
-    host_bind_port: '127.0.0.1:8449'
-    config: {}
-    # If your reverse-proxy runs on another machine, remove the config above and use this config instead:
-    # config:
-    #   forwardedHeaders:
-    #     insecure: true
-    #     # trustedIPs: ['IP-ADDRESS-OF-YOUR-REVERSE-PROXY']
+# Uncomment and tweak the variable below if the name of your federation entrypoint is different
+# than the default value (matrix-federation).
+# matrix_federation_traefik_entrypoint: matrix-federation
+
+# Uncomment and tweak the variable below if you really wish to change the internal port number
+# that the federation endpoint uses. Changing it is generally not necessary.
+# Usually, changing `matrix_playbook_public_matrix_federation_api_traefik_entrypoint_host_bind_port` below is enough.
+#matrix_playbook_public_matrix_federation_api_traefik_entrypoint_port: 8449
+
+matrix_playbook_public_matrix_federation_api_traefik_entrypoint_host_bind_port: 127.0.0.1:8449
+
+# Adapt the variable below based on where your reverse-proxy runs:
+# - if it's on the Matrix server: keep `forwardedHeaders` and `insecure: true` as is
+# - if it's on another machine: remove `forwardedHeaders` and `insecure: true` and enable/configure `trustedIPs`
+matrix_playbook_public_matrix_federation_api_traefik_entrypoint_config_custom:
+  forwardedHeaders:
+    insecure: true
+  # trustedIPs: ['IP-ADDRESS-OF-YOUR-REVERSE-PROXY']
```

Also, feel free to read the [Fronting the integrated Traefik reverse-proxy webserver with another reverse-proxy](./docs/configuring-playbook-own-webserver.md#fronting-the-integrated-reverse-proxy-webserver-with-another-reverse-proxy) documentation section again for additional details.


# 2024-01-13

## matrix-reminder-bot update with more secure (backward-incompatible) default settings

**TLDR**: your updated (to [v0.3.0](https://github.com/anoadragon453/matrix-reminder-bot/releases/tag/v0.3.0)) [matrix-reminder-bot](./docs/configuring-playbook-bot-matrix-reminder-bot.md) is now more secure. By default, like other bridges/bots managed by the playbook, it will only provide its services to users of your own server (not to anyone, even across the Matrix Federation). If that's fine, there's nothing you need to do.

Maintenance of [matrix-reminder-bot](./docs/configuring-playbook-bot-matrix-reminder-bot.md) has been picked up by [Kim Brose](https://github.com/HarHarLinks) and [@svierne](https://github.com/svierne).

Thanks to them, a new [v0.3.0](https://github.com/anoadragon453/matrix-reminder-bot/releases/tag/v0.3.0) release is out. The new version is now available for the ARM64 architecture, so playbook users on this architecture will no longer need to wait for [self-building](./docs/self-building.md) to happen.

The new version also comes with new `allowlist` and `blocklist` settings, which make it possible to restrict who can use the bot. Previously anyone, even across the Matrix Federation could talk to it and schedule reminders.

The playbook defaults all bridges and bots (where possible) to only be exposed to users of the current homeserver, not users across federation. Thanks to the new version of this bot making such a restriction possible, we're now making use of it. The playbook (via its `group_vars/matrix_servers` file) automatically enables the `allowlist` (`matrix_bot_matrix_reminder_bot_allowlist_enabled: true`) and configures it in such a way (`matrix_bot_matrix_reminder_bot_allowlist_regexes_auto`) so as to restrict the bot to your homeserver's users.

If you need **to undo or tweak these security improvements**, you can change your `vars.yml` file to:

- disable the allowlist (`matrix_bot_matrix_reminder_bot_allowlist_enabled: false`), making the bot allow usage by anyone, anywhere

- inject additional allowed servers or users by adding **additional** (on top of the default allowlist in `matrix_bot_matrix_reminder_bot_allowlist_regexes_auto`) custom regexes in the `matrix_bot_matrix_reminder_bot_allowlist_regexes_custom` list variable (see the [syntax reference](https://github.com/anoadragon453/matrix-reminder-bot/blob/1e910c0aa3469d280d93ee7e6c6d577227a3460c/sample.config.yaml#L43-L49))

- override the default allowlist (in the `group_vars/matrix_servers` file) by redefining `matrix_bot_matrix_reminder_bot_allowlist_regexes_auto`


# 2024-01-05

## matrix-mailer has been replaced by the exim-relay external role

We're continuing our effort to make [the playbook use external roles for some things](#the-playbook-now-uses-external-roles-for-some-things), so as to avoid doing everything ourselves and to facilitate code re-use.

The `matrix-mailer` role has been moved to its own repository ([ansible-role-exim-relay](https://github.com/mother-of-all-self-hosting/ansible-role-exim-relay)) that this playbook now includes.

To migrate:

- pull the playbook changes, as usual
- update your roles (run `just roles` or `make roles`)
- update your `vars.yml`, renaming `matrix_mailer`-prefixed variables to `exim_relay`-prefixed ones (e.g. `matrix_mailer_sender_address` -> `exim_relay_sender_address`). If you find none, it means you're using the default configuration and your migraiton job is even simpler.
- re-run the playbook (`install-all` or `setup-all`)

The playbook will take care of stopping the old `matrix-mailer` systemd service, relocating its directory and restarting it under the new name (`matrix-exim-relay.service`).


# 2024-01-02

## mautrix-signal now powered by the new Go-based bridge

The old Python-based [mautrix-signal](https://github.com/mautrix/signal) bridge is no longer maintained upstream. It's also known to have issues linking new devices.

It seems like the path forward is to switch to the new mautrix-signal bridge written in Golang, which we did thanks to [PR #3031](https://github.com/spantaleev/matrix-docker-ansible-deploy/pull/3041) by [Pierre 'McFly' Marty](https://github.com/pm-McFly).

The playbook should **automatically migrate your mautrix-signal installation to the new bridge code**. You will **need to relink all your devices** to continue your bridged conversations.


# 2023-10-23

## Enabling `allow_public_rooms_over_federation` by default for Synapse

**TDLR**: if your Matrix server is federating (which it mostly likely is, unless you've [disabled federation](docs/configuring-playbook-federation.md#disabling-federation)), your public rooms will not only be joinable across federation (as they've always been), but from now on will be discoverable (made available as a list across federation). We're changing this by flipping the value for Synapse's `allow_public_rooms_over_federation` setting to `true`, going against the upstream default. Servers that disable federation are not affected. Servers that have public rooms which are not published to the room directory are also not affected.

We generally try to stick to the default configuration for Synapse (and all other components), unless these defaults seem wrong or harmful. One such previous case from a few months ago was us [Enabling `forget_rooms_on_leave` by default for Synapse](#enabling-forget_rooms_on_leave-by-default-for-synapse) — the default value was making Synapse more wasteful of resources by default.

Today, we're going against upstream defaults again and flipping the `allow_public_rooms_over_federation` configuration option to `true`. This way, public rooms on your server will be made discoverable by others via federation, using the [`GET /_matrix/federation/v1/publicRooms` of the Server-Server API](https://spec.matrix.org/v1.8/server-server-api/#get_matrixfederationv1publicrooms).

The upstream Synapse default is `false` (disabled), so that public rooms are not exposed for other servers to discover (learn about their existence). Nevertheless, even if these rooms are not exposed (listed) for discovery, they are **still joinable** by anyone who knows their address or is invited to the room by an existing member.

**We go against the upstream default** in an effort to make Matrix federation more useful — a public room should be globally public — not only joinable, but also discoverable across federation.

The **historical reasoning** behind this change is as follows:

- `allow_public_rooms_over_federation` seems to have been enabled by default for Synapse until v1.7.0 (~2019), just like we believe it should be for a globally-federating network — rooms should be joinable and discoverable across federation.

- In Synapse v1.7.0 (~2019), `allow_public_rooms_over_federation` [got disabled](https://github.com/element-hq/synapse/blob/e9069c9f919685606506f04527332e83fbfa44d9/docs/upgrade.md?plain=1#L1877-L1891) by default in a [security-by-obscurity](https://en.wikipedia.org/wiki/Security_through_obscurity) workaround for misconfigured servers. See the [Avoiding unwelcome visitors on private Matrix servers](https://matrix.org/blog/2019/11/09/avoiding-unwelcome-visitors-on-private-matrix-servers/) `matrix.org` blog article. We believe that people wishing for a truly private server, should [disable federation](docs/configuring-playbook-federation.md#disabling-federation), instead of having a fully-federating server and trying to hide its public rooms. We also provide other workarounds below. We (and the Synapse team, obviously) believe that Matrix should federate by default, so federating the public room list seems to make sense.

- [etke.cc](https://etke.cc/) has been developing the free-software [Matrix Rooms Search](https://github.com/etkecc/mrs) project for a while now. One public (demo) instance of it is hosted at [matrixrooms.info](https://matrixrooms.info/). This search engine tries to go through the Matrix federation and discover & index public rooms to allow people to find them. We believe it's vital for Matrix (and any chat or social network for that matter) to be more discoverable, so that people can find communities and others to talk to. Today (on 23rd of October 2023), `matrixrooms.info` is indexing `23066` Matrix servers. Of these, only `1567` servers (7%) are making their public rooms discoverable. Who knows what wonderful communities and rooms are available on these 93% other Matrix servers that are supposedly federating, but are still gate-keeping their public room list. Indubitably, many of these servers are hosted via matrix-docker-ansible-deploy, so we feel partially responsible for making Matrix federation less useful.

Here are **actions you may wish to take** as a result of this change:

- (recommended) embrace the new default. If your Matrix server is federating, your public rooms have always been joinable across federation anyway. Exposing the list of public rooms does no harm and more-so does good by contributing to the usefulness of the Matrix network by facilitating room discovery.

- (switch to a better way of doings things on your semi-private server) The problem that the Synapse team appears to have solved by flipping the `allow_public_rooms_over_federation` default in Synapse v1.7.0 seems to for "mostly private" servers, which federate and have a bunch of rooms made public (and published in their room directory) in an effort to allow people on the same homeserver to easily find and join them (self-onboarding). With the introduction of Matrix Spaces, you can reorganize your flow around spaces — you can auto-join your users to a Matrix Space (via Synapse's `auto_join_rooms` setting — controlled by our `matrix_synapse_auto_join_rooms` variable), then add a bunch of rooms to the space and make them joinable by people belonging to the space. That is to say, do not make rooms public and do not publish them to the room directory unless they are really public. Instead, use other mechanisms for semi-public rooms or private rooms. One alternative is to stick to what you're doing (public rooms published to your rooms directory) but having a `m.federate: true` flag set during creation (clients like Element Web have a nice UI checkbox for this) to explicitly disable federation for them.

- (keeping the old behavior) if you wish to keep doing what you're doing (keeping your Matrix server federating, but hiding its public rooms list), add `matrix_synapse_allow_public_rooms_over_federation: false` to your `vars.yml` configuration. This restores the old behavior. You may also consider [disabling federation](docs/configuring-playbook-federation.md#disabling-federation) completely instead of relying on security-by-obscurity measures.


# 2023-10-18

## Postgres parameters are automatically tuned now

The playbook has provided some hints about [Tuning PostgreSQL](docs/maintenance-postgres.md#tuning-postgresql) for quite a while now.

From now on, the [Postgres Ansible role](https://github.com/mother-of-all-self-hosting/ansible-role-postgres) automatically tunes your Postgres configuration with the same [calculation logic](https://github.com/le0pard/pgtune/blob/master/src/features/configuration/configurationSlice.js) that powers https://pgtune.leopard.in.ua/.

Our [Tuning PostgreSQL](docs/maintenance-postgres.md#tuning-postgresql) documentation page has details about how you can turn auto-tuning off or adjust the automatically-determined Postgres configuration parameters manually.

People who [enable load-balancing with Synapse workers](docs/configuring-playbook-synapse.md#load-balancing-with-workers) no longer need to increase the maximum number of Postgres connections manually (previously done via `postgres_process_extra_arguments`). There's a new variable (`postgres_max_connections`) for controlling this number and the playbook automatically raises its value from `200` to `500` for setups which enable workers.


# 2023-08-31

## SchildiChat Web support

Thanks to [Aine](https://gitlab.com/etke.cc) of [etke.cc](https://etke.cc/), the playbook can now set up the [SchildiChat Web](https://github.com/SchildiChat/schildichat-desktop) client.

See our [Configuring SchildiChat Web](docs/configuring-playbook-client-schildichat-web.md) documentation to get started.


# 2023-08-23

## mautrix-wsproxy support

Thanks to [Johan Swetzén](https://github.com/jswetzen)'s efforts (who finished what was started by [James Reilly](https://github.com/hanthor) and [Shreyas Ajjarapu](https://github.com/shreyasajj)), the playbook now supports bridging to Android SMS and Apple iMessage via the [mautrix-wsproxy](https://github.com/mautrix/wsproxy) service (in combination with a [mautrix-imessage](https://github.com/mautrix/imessage) bridge running on your Mac or Android phone).

See our [Setting up Mautrix wsproxy for bridging Android SMS or Apple iMessage](docs/configuring-playbook-bridge-mautrix-wsproxy.md) documentation page for getting started.


# 2023-07-24

## matrix-registration-bot usage changed

[matrix-registration-bot](docs/configuring-playbook-bot-matrix-registration-bot.md) got some updates and now supports password-only-based login. Therefore the bot now doesn't need any manual configuration except setting a password in your `vars.yml`. The bot will be registered as admin and access tokens will be obtained automatically by the bot.

**For existing users** You need to set `matrix_bot_matrix_registration_bot_bot_password` if you previously only used `matrix_bot_matrix_registration_bot_bot_access_token`. Please also remove the following deprecated settings

* `matrix_bot_matrix_registration_bot_bot_access_token`
* `matrix_bot_matrix_registration_bot_api_token`


# 2023-07-21

## mautrix-gmessages support

Thanks to [Shreyas Ajjarapu](https://github.com/shreyasajj)'s efforts, the playbook now supports bridging to [Google Messages](https://messages.google.com/) via the [mautrix-gmessages](https://github.com/mautrix/gmessages) bridge. See our [Setting up Mautrix Google Messages bridging](docs/configuring-playbook-bridge-mautrix-gmessages.md) documentation page for getting started.


# 2023-07-17

## matrix-media-repo support

Thanks to [Michael Hollister](https://github.com/Michael-Hollister) from [FUTO](https://www.futo.org/), the creators of the [Circles app](https://circu.li/), the playbook can now set up [matrix-media-repo](https://github.com/turt2live/matrix-media-repo) — an alternative way to store homeserver media files, powered by a homeserver-independent implementation which supports S3 storage, IPFS, deduplication and other advanced features.

To learn more see our [Storing Matrix media files using matrix-media-repo](docs/configuring-playbook-matrix-media-repo.md) documentation page.


# 2023-05-25

## Enabling `forget_rooms_on_leave` by default for Synapse

With the [Synapse v1.84.0 update](https://github.com/spantaleev/matrix-docker-ansible-deploy/pull/2698), we've also **changed the default value** of the `forget_rooms_on_leave` setting of Synapse to a value of `true`. This way, **when you leave a room, Synapse will now forget it automatically**.

The upstream Synapse default is `false` (disabled), so that you must forget rooms manually after leaving.

**We go against the upstream default** ([somewhat controversially](https://github.com/spantaleev/matrix-docker-ansible-deploy/pull/2700)) in an effort to make Synapse leaner and potentially do what we believe most users would expect their homeserver to be doing.

If you'd like to go back to the old behavior, add the following to your configuration: `matrix_synapse_forget_rooms_on_leave: false`


# 2023-04-03

## The matrix-jitsi role lives independently now

**TLDR**: the `matrix-jitsi` role is now included from the [ansible-role-jitsi](https://github.com/mother-of-all-self-hosting/ansible-role-jitsi) repository, part of the [MASH playbook](https://github.com/mother-of-all-self-hosting/mash-playbook). Some variables have been renamed. All functionality remains intact.

The `matrix-jitsi` role has been relocated in its own repository, part of the [MASH playbook](https://github.com/mother-of-all-self-hosting/mash-playbook) project — an Ansible playbook for self-hosting [a growing list of FOSS software](https://github.com/mother-of-all-self-hosting/mash-playbook/blob/main/docs/supported-services.md). If hosting a Jitsi stack on the Matrix server itself did not stand right with you or you always wanted to host most stuff, you can now use this new playbook to do so.

As part of the extraction process of this role out of the Matrix playbook, a few other things improved:

- **native Traefik support** has been added
- **support for hosting under a subpath** has been added, although it suffers from a few minor issues listed [here](https://github.com/mother-of-all-self-hosting/mash-playbook/blob/main/docs/services/jitsi.md#url)

You need to **update your roles** (`just roles` or `make roles`) regardless of whether you're using Jitsi or not.

If you're making use of Jitsi via this playbook, you will need to update variable references in your `vars.yml` file:

  - `matrix_jitsi_*_docker_image_` -> `matrix_jitsi_*_container_image_`
  - `matrix_jitsi_` -> `jitsi_`
  - some other internal variables have changed, but the playbook will tell you about them

# 2023-03-22

## ntfy Web App is disabled by default

ntfy provides a web app, which is now disabled by default, because it may be unknown to and unused by most users of this playbook. You can enable it by setting `ntfy_web_root: "app"` (see [ntfy documentation](docs/configuring-playbook-ntfy.md)).

This change was already applied a while before this entry, but as some users were reporting the missing web app, this entry was added (see [#2529](https://github.com/spantaleev/matrix-docker-ansible-deploy/issues/2529)).


# 2023-03-21

## The matrix-prometheus role lives independently now

**TLDR**: the `matrix-prometheus` role is now included from the [ansible-role-prometheus](https://github.com/mother-of-all-self-hosting/ansible-role-prometheus) repository, part of the [MASH playbook](https://github.com/mother-of-all-self-hosting/mash-playbook). Some variables have been renamed. All functionality remains intact.

The `matrix-prometheus` role has been relocated in its own repository, part of the [MASH playbook](https://github.com/mother-of-all-self-hosting/mash-playbook) project — an Ansible playbook for self-hosting [a growing list of FOSS software](https://github.com/mother-of-all-self-hosting/mash-playbook/blob/main/docs/supported-services.md). If hosting a Prometheus stack on the Matrix server itself did not stand right with you or you always wanted to host most stuff, you can now use this new playbook to do so.

Extracting the Prometheus role out of this Matrix playbook required huge internal refactoring to the way the Prometheus configuration (scraping jobs) is generated. If you notice any breakage after upgrading, let us know.

You need to **update your roles** (`just roles` or `make roles`) regardless of whether you're using Prometheus or not.

If you're making use of Prometheus via this playbook, you will need to update variable references in your `vars.yml` file:

  - `matrix_prometheus_docker_image_` -> `matrix_prometheus_container_image_`
  - `matrix_prometheus_` -> `prometheus_`
  - some other internal variables have changed, but the playbook will tell you about them


# 2023-03-12

## synapse-auto-compressor support

Thanks to [Aine](https://gitlab.com/etke.cc) of [etke.cc](https://etke.cc/), the playbook can now set up [rust-synapse-compress-state](https://github.com/matrix-org/rust-synapse-compress-state)'s `synapse_auto_compressor` tool to run periodically.

If enabled, `synapse_auto_compressor` runs on a schedule and compresses your Synapse database's `state_groups` table. It was possible to run `rust-synapse-compress-state` manually via the playbook even before — see [Compressing state with rust-synapse-compress-state](docs/maintenance-synapse.md#compressing-state-with-rust-synapse-compress-state). However, using `synapse_auto_compressor` is better, because:

- it runs on a more up-to-date version of `rust-synapse-compress-state`
- it's a set-it-and-forget-it tool that you can enable and never have to deal with manual compression anymore

This tool needs to be enabled manually, for now. In the future, we're considering enabling it by default for all Synapse installations.

See our [Setting up synapse-auto-compressor](docs/configuring-playbook-synapse-auto-compressor.md) documentation to get started.


# 2023-03-07

## Sliding Sync proxy (Element X) support

Thanks to [Benjamin Kampmann](https://github.com/gnunicorn) for [getting it started](https://github.com/spantaleev/matrix-docker-ansible-deploy/pull/2515), [FSG-Cat](https://github.com/FSG-Cat) for fixing it up and me ([Slavi](https://github.com/spantaleev)) for polishing it up, the playbook can now install and configure the [sliding-sync proxy](https://github.com/matrix-org/sliding-sync).

The upcoming Element X clients ([Element X iOS](https://github.com/vector-im/element-x-ios) and [Element X Android](https://github.com/vector-im/element-x-android)) require the `sliding-sync` proxy to do their job. **These clients are still in beta** (especially Element X Android, which requires manual compilation to get it working with a non-`matrix.org` homeseserver). Playbook users can now easily give these clients a try and help test them thanks to us having `sliding-sync` support.

To get started, see our [Setting up the Sliding Sync proxy](docs/configuring-playbook-sliding-sync-proxy.md) documentation page.


# 2023-03-02

## The matrix-etherpad role lives independently now

**TLDR**: the `matrix-etherpad` role is now included from [another repository](https://github.com/mother-of-all-self-hosting/ansible-role-etherpad). Some variables have been renamed. All functionality remains intact.

You need to **update your roles** (`just roles` or `make roles`) regardless of whether you're using Etherpad or not.

If you're making use of Etherpad via this playbook, you will need to update variable references in your `vars.yml` file:

- Rename `matrix_etherpad_public_endpoint` to `etherpad_path_prefix`

- Replace `matrix_etherpad_mode: dimension` with:
  - for `matrix-nginx-proxy` users:
    - `etherpad_nginx_proxy_dimension_integration_enabled: true`
    - `etherpad_hostname: "{{ matrix_server_fqn_dimension }}"`
  - for Traefik users:
    - define your own `etherpad_hostname` and `etherpad_path_prefix` as you see fit

- Rename all other variables:
  - `matrix_etherpad_docker_image_` -> `matrix_etherpad_container_image_`
  - `matrix_etherpad_` -> `etherpad_`

Along with this relocation, the new role also:

- supports [self-building](docs/self-building.md), so it should work on `arm32` and `arm64` architectures
- has native Traefik reverse-proxy support (Etherpad requests no longer go through `matrix-nginx-proxy` when using Traefik)


# 2023-02-26

## Traefik is the default reverse-proxy now

**TLDR**: new installations will now default to Traefik as their reverse-proxy. Existing users need to explicitly choose their reverse-proxy type. [Switching to Traefik](#how-do-i-switch-my-existing-setup-to-traefik) is strongly encouraged. `matrix-nginx-proxy` may break over time and will ultimately be removed.

As mentioned 2 weeks ago in [(Backward Compatibility) Reverse-proxy configuration changes and initial Traefik support](#backward-compatibility-reverse-proxy-configuration-changes-and-initial-traefik-support), the playbook is moving to Traefik as its default SSL-terminating reverse-proxy.

Until now, we've been doing the migration gradually and keeping full backward compatibility. New installations were defaulting to `matrix-nginx-proxy` (just like before), while existing installations were allowed to remain on `matrix-nginx-proxy` as well. This makes things very difficult for us, because we need to maintain and think about lots of different setups:

- Traefik managed by the playbook
- Traefik managed by the user in another way
- another reverse-proxy on the same host (`127.0.0.1` port exposure)
- another reverse-proxy on another host (`0.0.0.0` port exposure)
- `matrix-nginx-proxy` — an `nginx` container managed by the playbook
- `nginx` webserver operated by the user, running without a container on the same server

Each change we do and each new feature that comes in needs to support all these different ways of reverse-proxying. Because `matrix-nginx-proxy` was the default and pretty much everyone was (and still is) using it, means that new PRs also come with `matrix-nginx-proxy` as their main focus and Traefik as an afterthought, which means we need to spend hours fixing up Traefik support.

We can't spend all this time maintaining so many different configurations anymore. Traefik support has been an option for 2 weeks and lots of people have already migrated their server and have tested things out. Traefik is what we use and preferentially test for.

It's time for the **next step in our migration process** to Traefik and elimination of `matrix-nginx-proxy`:

- Traefik is now the default reverse-proxy for new installations
- All existing users need to explicitly choose their reverse-proxy type by defining the `matrix_playbook_reverse_proxy_type` variable in their `vars.yml` configuration file. We strongly encourage existing users to [switch the Traefik](#how-to-switch-an-existing-setup-to-traefik), as the nginx setup is bound to become more and more broken over time until it's ultimately removed

### How do I switch my existing setup to Traefik?

**For users who are on `matrix-nginx-proxy`** (the default reverse-proxy provided by the playbook), switching to Traefik can happen with a simple configuration change. Follow this section from 2 weeks ago: [How do I explicitly switch to Traefik right now?](#how-do-i-explicitly-switch-to-traefik-right-now).

If you experience trouble:

1. Follow [How do I remain on matrix-nginx-proxy?](#how-do-i-remain-on-matrix-nginx-proxy) to bring your server back online using the old reverse-proxy
2. Ask for help in our [support channels](README.md#support)
3. Try switching to Traefik again later

**For users with a more special reverse-proxying setup** (another nginx server, Apache, Caddy, etc.), the migration may not be so smooth. Follow the [Using your own webserver](docs/configuring-playbook-own-webserver.md) guide. Ideally, your custom reverse-proxy will be configured in such a way that it **fronts the Traefik reverse-proxy** provided by the playbook. Other means of reverse-proxying are more fragile and may be deprecated in the future.

### I already use my own Traefik server. How do I plug that in?

See the [Traefik managed by the playbook](docs/configuring-playbook-own-webserver.md#traefik-managed-by-the-playbook) section.

### Why is matrix-nginx-proxy used even after switching to Traefik?

This playbook manages many different services. All these services were initially integrated with `matrix-nginx-proxy`.

While we migrate all these components to have native Traefik support, some still go through nginx internally (Traefik -> local `matrix-nginx-proxy` -> component). As time goes on, internal reliance on `matrix-nginx-proxy` will gradually decrease until it's completely removed.

### How do I remain on matrix-nginx-proxy?

Most new work and testing targets Traefik, so remaining on nginx is **not** "the good old stable" option, but rather the "still available, but largely untested and likely to be broken very soon" option.

To proceed regardless of this warning, add `matrix_playbook_reverse_proxy_type: playbook-managed-nginx` to your configuration.

At some point in the **near** future (days, or even weeks at most), we hope to completely get rid of `matrix-nginx-proxy` (or break it enough to make it unusable), so you **will soon be forced to migrate** anyway. Plan your migration accordingly.

### How do I keep using my own other reverse-proxy?

We recommend that you follow the guide for [Fronting the integrated reverse-proxy webserver with another reverse-proxy](docs/configuring-playbook-own-webserver.md#fronting-the-integrated-reverse-proxy-webserver-with-another-reverse-proxy).


# 2023-02-25

## rageshake support

Thanks to [Benjamin Kampmann](https://github.com/gnunicorn), the playbook can now install and configure the [rageshake](https://github.com/matrix-org/rageshake) bug report server.

Additional details are available in [Setting up rageshake](docs/configuring-playbook-rageshake.md).


# 2023-02-17

## Synapse templates customization support

The playbook can now help you customize Synapse's templates.

Additional details are available in the [Customizing templates](docs/configuring-playbook-synapse.md#customizing-templates) section of our Synapse documentation.

## The matrix-redis role lives independently now

**TLDR**: the `matrix-redis` role is now included from another repository. Some variables have been renamed. All functionality remains intact.

The `matrix-redis` role (which configures [Redis](https://redis.io/)) has been extracted from the playbook and now lives in its [own repository](https://github.com/mother-of-all-self-hosting/ansible-role-redis). This makes it possible to easily use it in other Ansible playbooks.

You need to **update your roles** (`just roles` or `make roles`) regardless of whether you're enabling Ntfy or not. If you're making use of Ntfy via this playbook, you will need to update variable references in your `vars.yml` file (`matrix_redis_` -> `redis_`).

## The matrix-ntfy role lives independently now

**TLDR**: the `matrix-ntfy` role is now included from another repository. Some variables have been renamed. All functionality remains intact.

The `matrix-ntfy` role (which configures [Ntfy](https://ntfy.sh/)) has been extracted from the playbook and now lives in its [own repository](https://github.com/mother-of-all-self-hosting/ansible-role-ntfy). This makes it possible to easily use it in other Ansible playbooks.

You need to **update your roles** (`just roles` or `make roles`) regardless of whether you're enabling Ntfy or not. If you're making use of Ntfy via this playbook, you will need to update variable references in your `vars.yml` file (`matrix_ntfy_` -> `ntfy_`).


# 2023-02-15

## The matrix-grafana role lives independently now

**TLDR**: the `matrix-grafana` role is now included from another repository. Some variables have been renamed. All functionality remains intact.

The `matrix-grafana` role (which configures [Grafana](docs/configuring-playbook-prometheus-grafana.md)) has been extracted from the playbook and now lives in its [own repository](https://github.com/mother-of-all-self-hosting/ansible-role-grafana). This makes it possible to easily use it in other Ansible playbooks.

You need to **update your roles** (`just roles` or `make roles`) regardless of whether you're enabling Grafana or not. If you're making use of Grafana via this playbook, you will need to update variable references in your `vars.yml` file (`matrix_grafana_` -> `grafana_`).


# 2023-02-13

## The matrix-backup-borg role lives independently now

**TLDR**: the `matrix-backup-borg` role is now included from another repository. Some variables have been renamed. All functionality remains intact.

Thanks to [moan0s](https://github.com/moan0s), the `matrix-backup-borg` role (which configures [BorgBackup](docs/configuring-playbook-backup-borg.md)) has been extracted from the playbook and now lives in its [own repository](https://github.com/mother-of-all-self-hosting/ansible-role-backup_borg). This makes it possible to easily use it in other Ansible playbooks and will become part of [nextcloud-docker-ansible-deploy](https://github.com/spantaleev/nextcloud-docker-ansible-deploy) soon.

You need to **update your roles** (`just roles` or `make roles`) regardless of whether you're enabling Borg's backup functionality or not. If you're making use of BorgBackup via this playbook, you will need to update variable references in your `vars.yml` file (`matrix_backup_borg_` -> `backup_borg_`).


# 2023-02-12

## (Backward Compatibility) Reverse-proxy configuration changes and initial Traefik support

**TLDR**:

- there's a new `matrix_playbook_reverse_proxy_type` variable (see [roles/custom/matrix-base/defaults/main.yml](roles/custom/matrix-base/defaults/main.yml)), which lets you tell the playbook what reverse-proxy setup you'd like to have. This makes it easier for people who want to do reverse-proxying in other ways.
- the default reverse-proxy (`matrix_playbook_reverse_proxy_type`) is still `playbook-managed-nginx` (via `matrix-nginx-proxy`), for now. **Existing `matrix-nginx-proxy` users should not observe any changes** and can stay on this for now.
- **Users who use their [own other webserver](docs/configuring-playbook-own-webserver.md) (e.g. Apache, etc.) need to change** `matrix_playbook_reverse_proxy_type` to something like `other-on-same-host`, `other-on-another-host` or `other-nginx-non-container`
- we now have **optional [Traefik](https://traefik.io/) support**, so you could easily host Matrix and other Traefik-native services in containers on the same server. Traefik support is still experimental (albeit, good enough) and will improve over time. It does work, but certain esoteric features may not be there yet.
- **Traefik will become the default reverse-proxy in the near future**. `matrix-nginx-proxy` will either remain as an option, or be completely removed to simplify the playbook

### Motivation for redoing our reverse-proxy setup

The playbook has supported various reverse-proxy setups for a long time. We have various configuration variables (`matrix_nginx_proxy_enabled`, various `_host_bind_port` variables, etc.) which allow the playbook to adapt to these different setups. The whole situation was messy though — hard to figure out and with lots of variables to toggle to make things work as you'd expect — huge **operational complexity**.

We love containers, proven by the fact that **everything** that this playbook manages runs in a container. Yet, we weren't allowing people to easily host other web-exposed containers alongside Matrix services on the same server. We were using `matrix-nginx-proxy` (our integrated [nginx](https://nginx.org/) server), which was handling web-exposure and SSL termination for our own services, but we **weren't helping you with all your other containers**.

People who were **using `matrix-nginx-proxy`** were on the happy path on which everything worked well by default (Matrix-wise), **but** could not easily run other web-exposed services on their Matrix server because `matrix-nginx-proxy` was occupying ports `80` and `443`. Other services which wanted to get web exposure either had to be plugged into `matrix-nginx-proxy` (somewhat difficult) or people had to forgo using `matrix-nginx-proxy` in favor of something else.

Of those that decided to forgo `matrix-nginx-proxy`, many were **using nginx** on the same server without a container. This was likely some ancient nginx version, depending on your choice of distro. The Matrix playbook was trying to be helpful and even with `matrix_nginx_proxy_enabled: false` was still generating nginx configuration in `/matrix/nginx-proxy/conf.d`. Those configuration files were adapted for inclusion into an nginx server running locally. Disabling the `matrix-nginx-proxy` role like this, yet still having it produce files is a bit disgusting, but it's what we've had since the early beginnings of this playbook.

Others still, wanted to run Matrix locally (no SSL certificates), regardless of which web server technology this relied on, and then **reverse-proxy from another machine on the network** which was doing SSL termination. These people were:

- *either* relying on `matrix_nginx_proxy_enabled: false` as well, combined with exposing services manually (setting `_bind_port` variables)
- *or* better yet, they were keeping `matrix-nginx-proxy` enabled, but in `http`-only mode (no SSL certificate retrieval).

Despite this operational complexity, things worked and were reasonably flexible to adapt to all these situations.

When using `matrix-nginx-proxy` as is, we still had another problem — one of **internal playbook complexity**. Too many services need to be web-exposed (port 80/443, SSL certificates). Because of this, they all had to integrate with the `matrix-nginx-proxy` role. Tens of different roles explicitly integrating with `matrix-nginx-proxy` is not what we call clean. The `matrix-nginx-proxy` role contains variables for many of these roles (yikes). Other roles were more decoupled from it and were injecting configuration into `matrix-nginx-proxy` at runtime — see all the `inject_into_nginx_proxy.yml` task files in this playbook (more decoupled, but still… yikes).

The next problem is one of **efficiency, interoperability and cost-saving**. We're working on other playbooks:

- [vaultwarden-docker-ansible-deploy](https://github.com/spantaleev/vaultwarden-docker-ansible-deploy) for hosting the [Vaultwarden](https://github.com/dani-garcia/vaultwarden) server — an alternative implementation of the [Bitwarden](https://bitwarden.com/) password manager
- [gitea-docker-ansible-deploy](https://github.com/spantaleev/gitea-docker-ansible-deploy) — for hosting the [Gitea](https://gitea.io/) git source code hosting service
- [nextcloud-docker-ansible-deploy](https://github.com/spantaleev/nextcloud-docker-ansible-deploy) — for hosting the [Nextcloud](https://nextcloud.com/) groupware platform

We'd love for users to be able to **seamlessly use all these playbooks (and others, even) against a single server**. We don't want `matrix-nginx-proxy` to have a monopoly on port `80`/`443` and make it hard for other services to join in on the party. Such a thing forces people into running multiple servers (one for each service), which does provide nice security benefits, but is costly and ineffiecient. We'd like to make self-hosting these services cheap and easy.

These other playbooks have been using [Traefik](https://traefik.io/) as their default reverse-proxy for a long time. They can all coexist nicely together (as an example, see the [Interoperability](https://github.com/spantaleev/nextcloud-docker-ansible-deploy/blob/master/docs/configuring-playbook-interoperability.md) documentation for the [Nextcloud playbook](https://github.com/spantaleev/nextcloud-docker-ansible-deploy)). Now that this playbook is gaining Traefik support, it will be able to interoperate with them. If you're going this way, make sure to have the Matrix playbook install Traefik and have the others use `*_reverse_proxy_type: other-traefik-container`.

Finally, at [etke.cc — a managed Matrix server hosting service](https://etke.cc) (built on top of this playbook, and coincidentally [turning 2 years old today](https://etke.cc/news/upsyw4ykbtgmwhz8k7ukldx0zbbfq-fh0iqi3llixi0/) 🎉), we're allowing people to host some additional services besides Matrix components. Exposing these services to the web requires ugly hacks and configuration files being dropped into `/matrix/nginx-proxy/conf.d`. We believe that everything should run in independent containers and be exposed to the web via a Traefik server, without a huge Ansible role like `matrix-nginx-proxy` that everything else needs to integrate with.

### How do these changes fix all these problems?

The new `matrix_playbook_reverse_proxy_type` lets you easily specify your preferred reverse-proxy type, including `other-on-same-host`, `other-on-another-host` and `none`, so people who'd like to reverse-proxy with their own web server have more options now.

Using Traefik greatly simplifies things, so going forward we'll have a simpler and easier to maintain playbook, which is also interoperable with other services.

Traefik is a web server, which has been specifically **designed for reverse-proxying to services running in containers**. It's ideal for usage in an Ansible playbook which runs everything in containers.

**Traefik obtains SSL certificates automatically**, so there's no need for plugging additional tools like [Certbot](https://certbot.eff.org/) into your web server (like we were doing in the `matrix-nginx-proxy` role). No more certificate renewal timers, web server reloading timers, etc. It's just simpler.

Traefik is a **modern web server**. [HTTP/3](https://doc.traefik.io/traefik/routing/entrypoints/#http3) is supported already (experimentally) and will move to stable soon, in the upcoming Traefik v3 release.

Traefik does not lock important functionality we'd like to use into [plus packages like nginx does](https://www.nginx.com/products/nginx/), leading us to resolve to configuration workarounds. The default Traefik package is good enough as it is.

### Where we're at right now?

`matrix_playbook_reverse_proxy_type` still defaults to a value of `playbook-managed-nginx`.

Unless we have some regression, **existing `matrix-nginx-proxy` users should be able to update their Matrix server and not observe any changes**. Their setup should still remain on nginx and everything should still work as expected.

**Users using [their own webservers](docs/configuring-playbook-own-webserver.md) will need to change `matrix_playbook_reverse_proxy_type`** to something like `other-on-same-host`, `other-on-another-host` or `other-nginx-non-container`. Previously, they could toggle `matrix_nginx_proxy_enabled` to `false`, and that made the playbook automatically expose services locally. Currently, we only do this if you change the reverse-proxy type to `other-on-same-host`, `other-on-another-host` or `other-nginx-non-container`.

#### How do I explicitly switch to Traefik right now?

**Users who wish to migrate to Traefik** today, can do so by **adding** this to their configuration:

```yaml
matrix_playbook_reverse_proxy_type: playbook-managed-traefik
```

You may still need to keep certain old `matrix_nginx_proxy_*` variables (like `matrix_nginx_proxy_base_domain_serving_enabled`), even when using Traefik. For now, we recommend keeping all `matrix_nginx_proxy_*` variables just in case. In the future, reliance on `matrix-nginx-proxy` will be removed.

Switching to Traefik will obtain new SSL certificates from Let's Encrypt (stored in `/matrix/traefik/ssl/acme.json`). **The switch is reversible**. You can always go back to `playbook-managed-nginx` if Traefik is causing you trouble.

**Note**: toggling `matrix_playbook_reverse_proxy_type` between Traefik and nginx will uninstall the Traefik role and all of its data (under `/matrix/traefik`), so you may run into a Let's Encrypt rate limit if you do it often.

Treafik directly reverse-proxies to **some** services right now, but for most other services it goes through `matrix-nginx-proxy` (e.g. Traefik -> `matrix-nginx-proxy` -> [Ntfy](docs/configuring-playbook-ntfy.md)). So, even if you opt into Traefik, you'll still see `matrix-nginx-proxy` being installed in local-only mode. This will improve with time.

Some services (like [coturn](docs/configuring-playbook-turn.md) and [Postmoogle](docs/configuring-playbook-bridge-postmoogle.md)) cannot be reverse-proxied to directly from Traefik, so they require direct access to SSL certificate files extracted out of Traefik. The playbook does this automatically thanks to a new [com.devture.ansible.role.traefik_certs_dumper](https://github.com/devture/com.devture.ansible.role.traefik_certs_dumper) role utilizing the [traefik-certs-dumper](https://github.com/ldez/traefik-certs-dumper) tool.

Our Traefik setup mostly works, but certain esoteric features may not work. If you have a default setup, we expect you to have a good experience.

### Where we're going in the near future?

The `matrix-nginx-proxy` role is quite messy. It manages both nginx and Certbot and its certificate renewal scripts and timers. It generates configuration even when the role is disabled (weird). Although it doesn't directly reach into variables from other roles, it has explicit awareness of various other services that it reverse-proxies to (`roles/custom/matrix-nginx-proxy/templates/nginx/conf.d/matrix-ntfy.conf.j2`, etc.). We'd like to clean this up. The only way is probably to just get rid of the whole thing at some point.

For now, `matrix-nginx-proxy` will stay around.

As mentioned above, Traefik still reverse-proxies to some (most) services by going through a local-only `matrix-nginx-proxy` server. This has allowed us to add Traefik support to the playbook early on (without having to rework all services), but is not the final goal. We'll **work on making each service support Traefik natively**, so that traffic will not need to go through `matrix-nginx-proxy` anymore. In the end, choosing Traefik should only give you a pure Traefik installation with no `matrix-nginx-proxy` in sight.

As Traefik support becomes complete and proves to be stable for a while, especially as a playbook default, we will **most likely remove `matrix-nginx-proxy` completely**. It will likely be some months before this happens though. Keeping support for both Traefik and nginx in the playbook will be a burden, especially with most of us running Traefik in the future. The Traefik role should do everything nginx does in a better and cleaner way. Users who use their own `nginx` server on the Matrix server will be inconvenienced, as nothing will generate ready-to-include nginx configuration for them. Still, we hope it won't be too hard to migrate their setup to another way of doing things, like:

- not using nginx anymore. A common reason for using nginx until now was that you were running other containers and you need your own nginx to reverse-proxy to all of them. Just switch them to Traefik as well.
- running Traefik in local-only mode (`traefik_config_entrypoint_web_secure_enabled: false`) and using some nginx configuration which reverse-proxies to Traefik (we should introduce examples for this in `examples/nginx`).

### How do I help?

You can help by:

- **explicitly switching your server to Traefik** right now (see example configuration in [How do I explicitly switch to Traefik right now?](#how-do-i-explicitly-switch-to-traefik-right-now) above), testing, reporting troubles

- **adding native Traefik support to a role** (requires adding Traefik labels, etc.) — for inspiration, see these roles ([prometheus_node_exporter](https://github.com/mother-of-all-self-hosting/ansible-role-prometheus-node-exporter), [prometheus_postgres_exporter](https://github.com/mother-of-all-self-hosting/ansible-role-prometheus-postgres-exporter)) and how they're hooked into the playbook via [group_vars/matrix_servers](group_vars/matrix_servers).

- **adding reverse-proxying examples for nginx users** in `examples/nginx`. People who insist on using their own `nginx` server on the same Matrix host, can run Traefik in local-only mode (`traefik_config_entrypoint_web_secure_enabled: false`) and reverse-proxy to the Traefik server


# 2023-02-10

## Matrix Authentication Support for Jitsi

Thanks to [Jakob S.](https://github.com/jakicoll) ([zakk gGmbH](https://github.com/zakk-it)), Jitsi can now use Matrix for authentication (via [Matrix User Verification Service](https://github.com/matrix-org/matrix-user-verification-service)).

Additional details are available in the [Authenticate using Matrix OpenID (Auth-Type 'matrix')](docs/configuring-playbook-jitsi.md#authenticate-using-matrix-openid-auth-type-matrix).

## Draupnir moderation tool (bot) support

Thanks to [FSG-Cat](https://github.com/FSG-Cat), the playbook can now install and configure the [Draupnir](https://github.com/the-draupnir-project/Draupnir) moderation tool (bot). Draupnir is a fork of [Mjolnir](docs/configuring-playbook-bot-mjolnir.md) (which the playbook has supported for a long time) maintained by Mjolnir's former lead developer.

Additional details are available in [Setting up Draupnir](docs/configuring-playbook-bot-draupnir.md).


# 2023-02-05

## The matrix-prometheus-postgres-exporter role lives independently now

**TLDR**: the `matrix-prometheus-postgres-exporter` role is now included from another repository. Some variables have been renamed. All functionality remains intact.

The `matrix-prometheus-postgres-exporter` role (which configures [Prometheus Postgres Exporter](https://github.com/prometheus-community/postgres_exporter)) has been extracted from the playbook and now lives in its own repository at https://github.com/mother-of-all-self-hosting/ansible-role-prometheus-postgres-exporter

It's still part of the playbook, but is now installed via `ansible-galaxy` (by running `just roles` / `make roles`). Some variables have been renamed (`matrix_prometheus_postgres_exporter_` -> `prometheus_postgres_exporter_`, etc.). The playbook will report all variables that you need to rename to get upgraded. All functionality remains intact.

The `matrix-prometheus-services-proxy-connect` role has bee adjusted to help integrate the new `prometheus_postgres_exporter` role with our own services (`matrix-nginx-proxy`)

Other roles which aren't strictly related to Matrix are likely to follow this fate of moving to their own repositories. Extracting them out allows other Ansible playbooks to make use of these roles easily.


# 2023-01-26

## coturn can now use host-networking

Large coturn deployments (with a huge range of ports specified via `matrix_coturn_turn_udp_min_port` and `matrix_coturn_turn_udp_max_port`) experience a huge slowdown with how Docker publishes all these ports (setting up firewall forwarding rules), which leads to a very slow coturn service startup and shutdown.

Such deployments don't need to run coturn within a private container network anymore. coturn can now run with host-networking by using configuration like this:

```yaml
matrix_coturn_container_network: host
```

With such a configuration, **Docker no longer needs to configure thousands of firewall forwarding rules** each time coturn starts and stops. This, however, means that **you will need to ensure these ports are open** in your firewall yourself.

Thanks to us [tightening coturn security](#backward-compatibility-tightening-coturn-security-can-lead-to-connectivity-issues), running coturn with host-networking should be safe and not expose neither other services running on the host, nor other services running on the local network.

## (Backward Compatibility) Tightening coturn security can lead to connectivity issues

**TLDR**: users who run and access their Matrix server on a private network (likely a small minority of users) may experience connectivity issues with our new default coturn blocklists. They may need to override `matrix_coturn_denied_peer_ips` and remove some IP ranges from it.

Inspired by [this security article](https://www.rtcsec.com/article/cve-2020-26262-bypass-of-coturns-access-control-protection/), we've decided to make use of coturn's `denied-peer-ip` functionality to prevent relaying network traffic to certain private IP subnets. This ensures that your coturn server won't accidentally try to forward traffic to certain services running on your local networks. We run coturn in a container and in a private container network by default, which should prevent such access anyway, but having additional block layers in place is better.

If you access your Matrix server from a local network and need coturn to relay to private IP addresses, you may observe that relaying is now blocked due to our new default `denied-peer-ip` lists (specified in `matrix_coturn_denied_peer_ips`). If you experience such connectivity problems, consider overriding this setting in your `vars.yml` file and removing certain networks from it.

We've also added `no-multicast-peers` to the default coturn configuration, but we don't expect this to cause trouble for most people.


# 2023-01-21

## The matrix-prometheus-node-exporter role lives independently now

**TLDR**: the `matrix-prometheus-node-exporter` role is now included from another repository. Some variables have been renamed. All functionality remains intact.

The `matrix-prometheus-node-exporter` role (which configures [Prometheus node exporter](https://github.com/prometheus/node_exporter)) has been extracted from the playbook and now lives in its own repository at https://github.com/mother-of-all-self-hosting/ansible-role-prometheus-node-exporter

It's still part of the playbook, but is now installed via `ansible-galaxy` (by running `just roles` / `make roles`). Some variables have been renamed (`matrix_prometheus_node_exporter_` -> `prometheus_node_exporter_`, etc.). The playbook will report all variables that you need to rename to get upgraded. All functionality remains intact.

A new `matrix-prometheus-services-proxy-connect` role was added to the playbook to help integrate the new `prometheus_node_exporter` role with our own services (`matrix-nginx-proxy`)

Other roles which aren't strictly related to Matrix are likely to follow this fate of moving to their own repositories. Extracting them out allows other Ansible playbooks to make use of these roles easily.


# 2023-01-13

## Support for running commands via just

We've previously used [make](https://www.gnu.org/software/make/) for easily running some playbook commands (e.g. `make roles` which triggers `ansible-galaxy`, see [Makefile](Makefile)). Our `Makefile` is still around and you can still run these commands.

In addition, we've added support for running commands via [just](https://github.com/casey/just) — a more modern command-runner alternative to `make`. Instead of `make roles`, you can now run `just roles` to accomplish the same.

Our [justfile](justfile) already defines some additional helpful **shortcut** commands that weren't part of our `Makefile`. Here are some examples:

- `just install-all` to trigger the much longer `ansible-playbook -i inventory/hosts setup.yml --tags=install-all,ensure-matrix-users-created,start` command
- `just install-all --ask-vault-pass` — commands also support additional arguments (`--ask-vault-pass` will be appended to the above installation command)
- `just run-tags install-mautrix-slack,start` — to run specific playbook tags
- `just start-all` — (re-)starts all services
- `just stop-group postgres` — to stop only the Postgres service
- `just register-user alice secret-password yes` — registers an `alice` user with the `secret-password` password and admin access (admin = `yes`)

Additional helpful commands and shortcuts may be defined in the future.

This is all completely optional. If you find it difficult to [install `just`](https://github.com/casey/just#installation) or don't find any of this convenient, feel free to run all commands manually.


# 2023-01-11

## mautrix-slack support

Thanks to [Cody Neiman](https://github.com/xangelix)'s efforts, the playbook now supports bridging to [Slack](https://slack.com/) via the [mautrix-slack](https://mau.dev/mautrix/slack) bridge. See our [Setting up Mautrix Slack bridging](docs/configuring-playbook-bridge-mautrix-slack.md) documentation page for getting started.

**Note**: this is a new Slack bridge. The playbook still retains Slack bridging via [matrix-appservice-slack](docs/configuring-playbook-bridge-appservice-slack.md) and [mx-puppet-slack](docs/configuring-playbook-bridge-mx-puppet-slack.md). You're free to use the bridge that serves you better, or even all three of them (for different users and use-cases).


# 2023-01-10

## ChatGPT support

Thanks to [@bertybuttface](https://github.com/bertybuttface), the playbook can now help you set up [matrix-chatgpt-bot](https://github.com/matrixgpt/matrix-chatgpt-bot) — a bot through which you can talk to the [ChatGPT](https://openai.com/blog/chatgpt/) model.

See our [Setting up matrix-bot-chatgpt](docs/configuring-playbook-bot-chatgpt.md) documentation to get started.


# 2022-11-30

## matrix-postgres-backup has been replaced by the ansible-role-postgres-backup external role

Just like we've [replaced Postgres with an external role](#matrix-postgres-has-been-replaced-by-the-comdevtureansiblerolepostgres-external-role) on 2022-11-28, we're now replacing `matrix-postgres-backup` with an external role — [com.devture.ansible.role.postgres_backup](https://github.com/mother-of-all-self-hosting/ansible-role-postgres_backup).

You'll need to rename your `matrix_postgres_backup`-prefixed variables such that they use a `postgres_backup` prefix.


# 2022-11-28

## matrix-postgres has been replaced by the ansible-role-postgres external role

**TLDR**: the tasks that install the integrated Postgres server now live in an external role — [ansible-role-postgres](https://github.com/mother-of-all-self-hosting/ansible-role-postgres). You'll need to run `make roles` to install it, and to also rename your `matrix_postgres`-prefixed variables to use a `devture_postgres` prefix (e.g. `matrix_postgres_connection_password` -> `postgres_connection_password`). All your data will still be there! Some scripts have moved (`/usr/local/bin/matrix-postgres-cli` -> `/matrix/postgres/bin/cli`).

The `matrix-postgres` role that has been part of the playbook for a long time has been replaced with the [ansible-role-postgres](https://github.com/mother-of-all-self-hosting/ansible-role-postgres) role. This was done as part of our work to [use external roles for some things](#the-playbook-now-uses-external-roles-for-some-things) for better code re-use and maintainability.

The new role is an upgraded version of the old `matrix-postgres` role with these notable differences:

- it uses different names for its variables (`matrix_postgres` -> `devture_postgres`)
- when [Vacuuming PostgreSQL](docs/maintenance-postgres.md#vacuuming-postgresql), it will vacuum all your databases, not just the Synapse one

You'll need to run `make roles` to install the new role. You would also need to rename your `matrix_postgres`-prefixed variables to use a `devture_postgres` prefix.

Note: the systemd service still remains the same — `matrix-postgres.service`. Your data will still be in `/matrix/postgres`, etc. Postgres-related scripts will be moved to `/matrix/postgres/bin` (`/usr/local/bin/matrix-postgres-cli` -> `/matrix/postgres/bin/cli`, etc). Also see [The playbook no longer installs scripts in /usr/local/bin](#the-playbook-no-longer-installs-scripts-in-usrlocalbin).

## The playbook no longer installs scripts to /usr/local/bin

The locations of various scripts installed by the playbook have changed.

The playbook no longer contaminates your `/usr/local/bin` directory. All scripts installed by the playbook now live in `bin/` directories under `/matrix`. Some examples are below:

- `/usr/local/bin/matrix-remove-all` -> `/matrix/bin/remove-all`
- `/usr/local/bin/matrix-postgres-cli` -> `/matrix/postgres/bin/cli`
- `/usr/local/bin/matrix-ssl-lets-encrypt-certificates-renew` -> `/matrix/ssl/bin/lets-encrypt-certificates-renew`
- `/usr/local/bin/matrix-synapse-register-user` -> `/matrix/synapse/bin/register-user`


# 2022-11-25

## 2x-5x performance improvements in playbook runtime

**TLDR**: the playbook is 2x faster for running `--tags=setup-all` (and various other tags). It also has new `--tags=install-*` tags (like `--tags=install-all`), which skip uninstallation tasks and bring an additional 2.5x speedup. In total, the playbook can maintain your server 5 times faster.

Our [etke.cc managed Matrix hosting service](https://etke.cc) runs maintenance against hundreds of servers, so the playbook being fast means a lot. The [etke.cc Ansible playbook](https://github.com/etkecc/ansible) (which is an extension of this one) is growing to support more and more services (besides just Matrix), so the Matrix playbook being leaner prevents runtimes from becoming too slow and improves the customer experience.

Even when running `ansible-playbook` manually (as most of us here do), it's beneficial not to waste time and CPU resources.

Recently, a few large optimizations have been done to this playbook and its external roles (see [The playbook now uses external roles for some things](#the-playbook-now-uses-external-roles-for-some-things) and don't forget to run `make roles`):

1. Replacing Ansible `import_tasks` calls with `include_tasks`, which decreased runtime in half. Using `import_tasks` is slower and causes Ansible to go through and skip way too many tasks (tasks which could have been skipped altogether by not having Ansible include them in the first place). On an experimental VM, **deployment time was decreased from ~530 seconds to ~250 seconds**.

2. Introducing new `install-*` tags (`install-all` and `install-COMPONENT`, e.g. `install-synapse`, `install-bot-mjolnir`), which only run Ansible tasks pertaining to installation, while skipping uninstallation tasks. In most cases, people are maintaining the same setup or they're *adding* new components. Removing components is rare. Running thousands of uninstallation tasks each time is wasteful. On an experimental VM, **deployment time was decreased from ~250 seconds (`--tags=setup-all`) to ~100 seconds (`--tags=install-all`)**.

You can still use `--tags=setup-all`. In fact, that's the best way to ensure your server is reconciled with the `vars.yml` configuration.

If you know you haven't uninstalled any services since the last time you ran the playbook, you could run `--tags=install-all` instead and benefit from quicker runtimes. It should be noted that a service may become "eligible for uninstallation" even if your `vars.yml` file remains the same. In rare cases, we toggle services from being auto-installed to being optional, like we did on the 17th of March 2022 when we made [ma1sd not get installed by default](https://github.com/spantaleev/matrix-docker-ansible-deploy/blob/master/CHANGELOG.md#compatibility-break-ma1sd-identity-server-no-longer-installed-by-default). In such rare cases, you'd also need to run `--tags=setup-all`.


# 2022-11-22

# Automatic `matrix_architecture` determination

From now on, the playbook automatically determines your server's architecture and sets the `matrix_architecture` variable accordingly. You no longer need to set this variable manually in your `vars.yml` file.

# Docker and the Docker SDK for Python are now installed via external roles

We're continuing our effort to make [the playbook use external roles for some things](#the-playbook-now-uses-external-roles-for-some-things), so as to avoid doing everything ourselves and to facilitate code re-use.

Docker will now be installed on the server via the [geerlingguy.docker](https://github.com/geerlingguy/ansible-role-docker) Ansible role. If you'd like to manage the Docker installation yourself, you can disable the playbook's installation of Docker by setting `matrix_playbook_docker_installation_enabled: false`.

The Docker SDK for Python (named `docker-python`, `python-docker`, etc. on the different platforms) is now also installed by another role ([com.devture.ansible.role.docker_sdk_for_python](https://github.com/devture/com.devture.ansible.role.docker_sdk_for_python)). To disable this role and install the necessary tools yourself, use `devture_docker_sdk_for_python_installation_enabled: false`.

If you're hitting issues with Docker installation or Docker SDK for Python installation, consider reporting bugs or contributing to these other projects.

These additional roles are downloaded into the playbook directory (to `roles/galaxy`) via an `ansible-galaxy …` command. `make roles` is an easy shortcut for invoking the `ansible-galaxy` command to download these roles.


# 2022-11-20

## (Backward Compatibility Break) Changing how reverse-proxying to Synapse works — now via a `matrix-synapse-reverse-proxy-companion` service

**TLDR**: There's now a `matrix-synapse-reverse-proxy-companion` nginx service, which helps with reverse-proxying to Synapse and its various worker processes (if workers are enabled), so that `matrix-nginx-proxy` can be relieved of this role. `matrix-nginx-proxy` still remains as the public SSL-terminating reverse-proxy in the playbook. `matrix-synapse-reverse-proxy-companion` is just one more reverse-proxy thrown into the mix for convenience. People with a more custom reverse-proxying configuration may be affected — see [Webserver configuration](#webserver-configuration) below.

### Background

Previously, `matrix-nginx-proxy` forwarded requests to Synapse directly. When Synapse is running in worker mode, the reverse-proxying configuration is more complicated (different requests need to go to different Synapse worker processes). `matrix-nginx-proxy` had configuration for sending each URL endpoint to the correct Synapse worker responsible for handling it. However, sometimes people like to disable `matrix-nginx-proxy` (for whatever reason) as detailed in [Using your own webserver, instead of this playbook's nginx proxy](docs/configuring-playbook-own-webserver.md).

Because `matrix-nginx-proxy` was so central to request forwarding, when it was disabled and Synapse was running with workers enabled, there was nothing which could forward requests to the correct place anymore… which caused [problems such as this one affecting Dimension](https://github.com/spantaleev/matrix-docker-ansible-deploy/issues/2090).

### Solution

From now on, `matrix-nginx-proxy` is relieved of its function of reverse-proxying to Synapse and its various worker processes. This role is now handled by the new `matrix-synapse-reverse-proxy-companion` nginx service and works even if `matrix-nginx-proxy` is disabled. The purpose of the new `matrix-synapse-reverse-proxy-companion` service is to:

- serve as a companion to Synapse and know how to reverse-proxy to Synapse correctly (no matter if workers are enabled or not)

- provide a unified container address for reaching Synapse (no matter if workers are enabled or not)
  - `matrix-synapse-reverse-proxy-companion:8008` for Synapse Client-Server API traffic
  - `matrix-synapse-reverse-proxy-companion:8048` for Synapse Server-Server (Federation) API traffic

- simplify `matrix-nginx-proxy` configuration — it now only needs to send requests to `matrix-synapse-reverse-proxy-companion` or `matrix-dendrite`, etc., without having to worry about workers

- allow reverse-proxying to Synapse, even if `matrix-nginx-proxy` is disabled

`matrix-nginx-proxy` still remains as the public SSL-terminating reverse-proxy in the playbook. All traffic goes through it before reaching any of the services. It's just that now the Synapse traffic is routed through `matrix-synapse-reverse-proxy-companion` like this:

(`matrix-nginx-proxy` -> `matrix-synapse-reverse-proxy-companion` -> (`matrix-synapse` or some Synapse worker)).

Various services (like Dimension, etc.) still talk to Synapse via `matrix-nginx-proxy` (e.g. `http://matrix-nginx-proxy:12080`) preferentially. They only talk to Synapse via the reverse-proxy companion (e.g. `http://matrix-synapse-reverse-proxy-companion:8008`) if `matrix-nginx-proxy` is disabled. Services should not be talking to Synapse (e.g. `https://matrix-synapse:8008` directly anymore), because when workers are enabled, that's the Synapse `master` process and may not be serving all URL endpoints needed by the service.

### Webserver configuration

- if you're using `matrix-nginx-proxy` (`matrix_nginx_proxy_enabled: true`, which is the default for the playbook), you don't need to do anything

- if you're using your own `nginx` webserver running on the server, you shouldn't be affected. The `/matrix/nginx/conf.d` configuration and exposed ports that you're relying on will automatically be updated in a way that should work

- if you're using another local webserver (e.g. Apache, etc.) and haven't changed any ports (`matrix_*_host_bind_port` definitions), you shouldn't be affected. You're likely sending Matrix traffic to `127.0.0.1:8008` and `127.0.0.1:8048`. These ports (`8008` and `8048`) will still be exposed on `127.0.0.1` by default — just not by the `matrix-synapse` container from now on, but by the `matrix-synapse-reverse-proxy-companion` container instead

- if you've been exposing `matrix-synapse` ports (`matrix_synapse_container_client_api_host_bind_port`, etc.) manually, you should consider exposing `matrix-synapse-reverse-proxy-companion` ports instead

- if you're running Traefik and reverse-proxying directly to the `matrix-synapse` container, you should start reverse-proxying to the `matrix-synapse-reverse-proxy-companion` container instead. See [our updated Traefik example configuration](docs/configuring-playbook-own-webserver.md#sample-configuration-for-running-behind-traefik-20). Note: we now recommend calling the federation entry point `federation` (instead of `synapse`) and reverse-proxying the federation traffic via `matrix-nginx-proxy`, instead of sending it directly to Synapse (or `matrix-synapse-reverse-proxy-companion`). This makes the configuration simpler.


# 2022-11-05

## (Backward Compatibility Break) A new default standalone mode for Etherpad

Until now, [Etherpad](https://etherpad.org/) (which [the playbook could install for you](docs/configuring-playbook-etherpad.md)) required the [Dimension integration manager](docs/configuring-playbook-dimension.md) to also be installed, because Etherpad was hosted on the Dimension domain (at `dimension.example.com/etherpad`).

From now on, Etherpad can be installed in `standalone` mode on `etherpad.example.com` and used even without Dimension. This is much more versatile, so the playbook now defaults to this new mode (`etherpad_mode: standalone`).

If you've already got both Etherpad and Dimension in use you could:

- **either** keep hosting Etherpad under the Dimension domain by adding `etherpad_mode: dimension` to your `vars.yml` file. All your existing room widgets will continue working at the same URLs and no other changes will be necessary.

- **or**, you could change to hosting Etherpad separately on `etherpad.example.com`. You will need to [configure a DNS record](docs/configuring-dns.md) for this new domain. You will also need to reconfigure Dimension to use the new pad URLs (`https://etherpad.example.com/…`) going forward (refer to our [configuring Etherpad documentation](docs/configuring-playbook-etherpad.md)). All your existing room widgets (which still use `https://dimension.example.com/etherpad/…`) will break as Etherpad is not hosted there anymore. You will need to re-add them or to consider not using `standalone` mode


# 2022-11-04

## The playbook now uses external roles for some things

**TLDR**: when updating the playbook and before running it, you'll need to run `make roles` to make [ansible-galaxy](https://docs.ansible.com/ansible/latest/cli/ansible-galaxy.html) download dependency roles (see the [`requirements.yml` file](requirements.yml)) to the `roles/galaxy` directory. Without this, the playbook won't work.

We're in the process of trimming the playbook and making it reuse Ansible roles.

Starting now, the playbook is composed of 2 types of Ansible roles:

- those that live within the playbook itself (`roles/custom/*`)

- those downloaded from other sources (using [ansible-galaxy](https://docs.ansible.com/ansible/latest/cli/ansible-galaxy.html) to `roles/galaxy`, based on the [`requirements.yml` file](requirements.yml)). These roles are maintained by us or by other people from the Ansible community.

We're doing this for greater code-reuse (across Ansible playbooks, including our own related playbooks [gitea-docker-ansible-deploy](https://github.com/spantaleev/gitea-docker-ansible-deploy) and [nextcloud-docker-ansible-deploy](https://github.com/spantaleev/nextcloud-docker-ansible-deploy)) and decreased maintenance burden. Until now, certain features were copy-pasted across playbooks or were maintained separately in each one, with improvements often falling behind. We've also tended to do too much by ourselves — installing Docker on the server from our `matrix-base` role, etc. — something that we'd rather not do anymore by switching to the [geerlingguy.docker](https://galaxy.ansible.com/geerlingguy/docker) role.

Some variable names will change during the transition to having more and more external (galaxy) roles. There's a new `custom/matrix_playbook_migration` role added to the playbook which will tell you about these changes each time you run the playbook.

**From now on**, every time you update the playbook (well, every time the `requirements.yml` file changes), it's best to run `make roles` to update the roles downloaded from other sources. `make roles` is a shortcut (a `roles` target defined in [`Makefile`](Makefile) and executed by the [`make`](https://www.gnu.org/software/make/) utility) which ultimately runs [ansible-galaxy](https://docs.ansible.com/ansible/latest/cli/ansible-galaxy.html) to download Ansible roles. If you don't have `make`, you can also manually run the commands seen in the `Makefile`.


# 2022-10-14

## synapse-s3-storage-provider support

**`synapse-s3-storage-provider` support is very new and still relatively untested. Using it may cause data loss.**

You can now store your Synapse media repository files on Amazon S3 (or another S3-compatible object store) using [synapse-s3-storage-provider](https://github.com/matrix-org/synapse-s3-storage-provider) — a media provider for Synapse (Python module), which should work faster and more reliably than our previous [Goofys](docs/configuring-playbook-s3-goofys.md) implementation (Goofys will continue to work).

This is not just for initial installations. Users with existing files (stored in the local filesystem) can also migrate their files to `synapse-s3-storage-provider`.

To get started, see our [Storing Synapse media files on Amazon S3 with synapse-s3-storage-provider](docs/configuring-playbook-synapse-s3-storage-provider.md) documentation.

## Synapse container image customization support

We now support customizing the Synapse container image by adding additional build steps to its [`Dockerfile`](https://docs.docker.com/engine/reference/builder/).

Our [synapse-s3-storage-provider support](#synapse-s3-storage-provider-support) is actually built on this. When `s3-storage-provider` is enabled, we automatically add additional build steps to install its Python module into the Synapse image.

Besides this kind of auto-added build steps (for components supported by the playbook), we also let you inject your own custom build steps using configuration like this:

```yaml
matrix_synapse_container_image_customizations_enabled: true

matrix_synapse_container_image_customizations_dockerfile_body_custom: |
 RUN echo 'This is a custom step for building the customized Docker image for Synapse.'
 RUN echo 'You can override matrix_synapse_container_image_customizations_dockerfile_body_custom to add your own steps.'
 RUN echo 'You do NOT need to include a FROM clause yourself.'
```

People who have needed to customize Synapse previously had to fork the git repository, make their changes to the `Dockerfile` there, point the playbook to the new repository (`matrix_synapse_container_image_self_build_repo`) and enable self-building from scratch (`matrix_synapse_container_image_self_build: true`). This is harder and slower.

With the new Synapse-customization feature in the playbook, we use the original upstream (pre-built, if available) Synapse image and only build on top of it, right on the Matrix server. This is much faster than building all of Synapse from scratch.


# 2022-10-02

## matrix-ldap-registration-proxy support

Thanks to [@TheOneWithTheBraid](https://github.com/TheOneWithTheBraid), we now support installing [matrix-ldap-registration-proxy](https://gitlab.com/activism.international/matrix_ldap_registration_proxy) — a proxy which handles Matrix registration requests and forwards them to LDAP.

See our [Setting up matrix-ldap-registration-proxy](docs/configuring-playbook-matrix-ldap-registration-proxy.md) documentation to get started.


# 2022-09-15

## (Potential Backward Compatibility Break) Major improvements to Synapse workers

People who are interested in running a Synapse worker setup should know that **our Synapse worker implementation is much more powerful now**:

- we've added support for [Stream writers](#stream-writers-support)
- we've added support for [multiple federation sender workers](#multiple-federation-sender-workers-support)
- we've added support for [multiple pusher workers](#multiple-pusher-workers-support)
- we've added support for [running background tasks on a worker](#background-tasks-can-run-on-a-worker)
- we've restored support for [`appservice` workers](#appservice-worker-support-is-back)
- we've restored support for [`user_dir` workers](#user-directory-worker-support-is-back)
- we've made it possible to [reliably use more than 1 `media_repository` worker](#using-more-than-1-media-repository-worker-is-now-more-reliable)
- see the [Potential Backward Incompatibilities after these Synapse worker changes](#potential-backward-incompatibilities-after-these-synapse-worker-changes)

### Stream writers support

From now on, the playbook lets you easily set up various [stream writer workers](https://matrix-org.github.io/synapse/latest/workers.html#stream-writers) which can handle different streams (`events` stream; `typing` URL endpoints, `to_device` URL endpoints, `account_data` URL endpoints, `receipts` URL endpoints, `presence` URL endpoints). All of this work was previously handled by the main Synapse process, but can now be offloaded to stream writer worker processes.

If you're using `matrix_synapse_workers_preset: one-of-each`, you'll automatically get 6 additional workers (one for each of the above stream types). Our `little-federation-helper` preset (meant to be quite minimal and focusing in improved federation performance) does not include stream writer workers.

If you'd like to customize the number of workers we also make that possible using these variables:

```yaml
# Synapse only supports more than 1 worker for the `events` stream.
# All other streams can utilize either 0 or 1 workers, not more than that.
matrix_synapse_workers_stream_writer_events_stream_workers_count: 5
matrix_synapse_workers_stream_writer_typing_stream_workers_count: 1
matrix_synapse_workers_stream_writer_to_device_stream_workers_count: 1
matrix_synapse_workers_stream_writer_account_data_stream_workers_count: 1
matrix_synapse_workers_stream_writer_receipts_stream_workers_count: 1
matrix_synapse_workers_stream_writer_presence_stream_workers_count: 1
```

### Multiple federation sender workers support

Until now, we only supported a single `federation_sender` worker (`matrix_synapse_workers_federation_sender_workers_count` could either be `0` or `1`). From now on, you can have as many as you want to help with your federation traffic.

### Multiple pusher workers support

Until now, we only supported a single `pusher` worker (`matrix_synapse_workers_pusher_workers_count` could either be `0` or `1`). From now on, you can have as many as you want to help with pushing notifications out.

### Background tasks can run on a worker

From now on, you can put [background task processing on a worker](https://matrix-org.github.io/synapse/latest/workers.html#background-tasks).

With `matrix_synapse_workers_preset: one-of-each`, you'll get one `background` worker automatically. You can also control the `background` workers count with `matrix_synapse_workers_background_workers_count`. Only  `0` or `1` workers of this type are supported by Synapse.

### Appservice worker support is back

We previously had an `appservice` worker type, which [Synapse deprecated in v1.59.0](https://github.com/element-hq/synapse/blob/v1.59.0/docs/upgrade.md#deprecation-of-the-synapseappappservice-and-synapseappuser_dir-worker-application-types). So did we, at the time.

The new way to implement such workers is by using a `generic_worker` and dedicating it to the task of talking to Application Services. From now on, we have support for this.

With `matrix_synapse_workers_preset: one-of-each`, you'll get one `appservice` worker automatically. You can also control the `appservice` workers count with `matrix_synapse_workers_appservice_workers_count`. Only  `0` or `1` workers of this type are supported by Synapse.

### User Directory worker support is back

We previously had a `user_dir` worker type, which [Synapse deprecated in v1.59.0](https://github.com/element-hq/synapse/blob/v1.59.0/docs/upgrade.md#deprecation-of-the-synapseappappservice-and-synapseappuser_dir-worker-application-types). So did we, at the time.

The new way to implement such workers is by using a `generic_worker` and dedicating it to the task of serving the user directory. From now on, we have support for this.

With `matrix_synapse_workers_preset: one-of-each`, you'll get one `user_dir` worker automatically. You can also control the `user_dir` workers count with `matrix_synapse_workers_user_dir_workers_count`. Only  `0` or `1` workers of this type are supported by Synapse.

### Using more than 1 media repository worker is now more reliable

With `matrix_synapse_workers_preset: one-of-each`, we only launch one `media_repository` worker.

If you've been configuring `matrix_synapse_workers_media_repository_workers_count` manually, you may have increased that to more workers. When multiple media repository workers are in use, background tasks related to the media repository must always be configured to run on a single `media_repository` worker via `media_instance_running_background_jobs`. Until now, we weren't doing this correctly, but we now are.

### Potential Backward Incompatibilities after these Synapse worker changes

Below we'll discuss **potential backward incompatibilities**.

- **Worker names** (container names, systemd services, worker configuration files) **have changed**. Workers are now labeled sequentially (e.g. `matrix-synapse-worker_generic_worker-18111` -> `matrix-synapse-worker-generic-0`). The playbook will handle these changes automatically.

- Due to increased worker types support above, people who use `matrix_synapse_workers_preset: one-of-each` should be aware that with these changes, **the playbook will deploy 9 additional workers** (6 stream writers, 1 `appservice` worker, 1 `user_dir` worker, 1 background task worker). This **may increase RAM/CPU usage**, etc. If you find your server struggling, consider disabling some workers with the appropriate `matrix_synapse_workers_*_workers_count` variables.

- **Metric endpoints have also changed** (`/metrics/synapse/worker/generic_worker-18111` -> `/metrics/synapse/worker/generic-worker-0`). If you're [collecting metrics to an external Prometheus server](docs/configuring-playbook-prometheus-grafana.md#collecting-metrics-to-an-external-prometheus-server), consider revisiting our [Collecting Synapse worker metrics to an external Prometheus server](docs/configuring-playbook-prometheus-grafana.md#collecting-synapse-worker-metrics-to-an-external-prometheus-server) docs and updating your Prometheus configuration. **If you're collecting metrics to the integrated Prometheus server** (not enabled by default), **your Prometheus configuration will be updated automatically**. Old data (from before this change) may stick around though.

- **the format of `matrix_synapse_workers_enabled_list` has changed**. You were never advised to use this variable for directly creating workers (we advise people to control workers using `matrix_synapse_workers_preset` or by tweaking `matrix_synapse_workers_*_workers_count` variables only), but some people may have started using the `matrix_synapse_workers_enabled_list` variable to gain more control over workers. If you're one of them, you'll need to adjust its value. See `roles/custom/matrix-synapse/defaults/main.yml` for more information on the new format. The playbook will also do basic validation and complain if you got something wrong.


# 2022-09-09

## Cactus Comments support

Thanks to [Julian-Samuel Gebühr (@moan0s)](https://github.com/moan0s), the playbook can now set up [Cactus Comments](https://cactus.chat) — federated comment system for the web based on Matrix.

See our [Setting up Cactus Comments](docs/configuring-playbook-cactus-comments.md) documentation to get started.


# 2022-08-23

## Postmoogle email bridge support

Thanks to [Aine](https://gitlab.com/etke.cc) of [etke.cc](https://etke.cc/), the playbook can now set up the new [Postmoogle](https://github.com/etkecc/postmoogle) email bridge. Postmoogle is like the [Email2Matrix bridge](https://github.com/devture/email2matrix) (also [already supported by the playbook](docs/configuring-playbook-email2matrix.md)), but more capable and with the intention to soon support *sending* emails, not just receiving.

See our [Setting up Postmoogle email bridging](docs/configuring-playbook-bridge-postmoogle.md) documentation to get started.


# 2022-08-10

## mautrix-whatsapp default configuration changes

In [Pull Request #2012](https://github.com/spantaleev/matrix-docker-ansible-deploy/pull/2012), we've made some changes to the default configuration used by the `mautrix-whatsapp` bridge.

If you're using this bridge, you should look into this PR and see if the new configuration suits you. If not, you can always change individual preferences in your `vars.yml` file.

Most notably, spaces support has been enabled by default. The bridge will now group rooms into a Matrix space. **If you've already bridged to Whatsapp** prior to this update, you will need to send `!wa sync space` to the bridge bot to make it create the space and put your existing rooms into it.


# 2022-08-09

## Conduit support

Thanks to [Charles Wright](https://github.com/cvwright), we now have optional experimental [Conduit](https://conduit.rs) homeserver support for new installations. This comes as a follow-up to the playbook getting [Dendrite support](#dendrite-support) earlier this year.

Existing Synapse or Dendrite installations do **not** need to be updated. **Synapse is still the default homeserver implementation** installed by the playbook.

To try out Conduit, we recommend that you **use a new server** and the following `vars.yml` configuration:

```yaml
matrix_homeserver_implementation: conduit
```

**The homeserver implementation of an existing server cannot be changed** (e.g. from Synapse or Dendrite to Conduit) without data loss.


# 2022-07-29

## mautrix-discord support

Thanks to [MdotAmaan](https://github.com/MdotAmaan)'s efforts, the playbook now supports bridging to [Discord](https://discordapp.com/) via the [mautrix-discord](https://mau.dev/mautrix/discord) bridge. See our [Setting up Mautrix Discord bridging](docs/configuring-playbook-bridge-mautrix-discord.md) documentation page for getting started.

**Note**: this is a new Discord bridge. The playbook still retains Discord bridging via [matrix-appservice-discord](docs/configuring-playbook-bridge-appservice-discord.md) and [mx-puppet-discord](docs/configuring-playbook-bridge-mx-puppet-discord.md). You're free to use the bridge that serves you better, or even all three of them (for different users and use-cases).


# 2022-07-27

## matrix-appservice-kakaotalk support

The playbook now supports bridging to [Kakaotalk](https://www.kakaocorp.com/page/service/service/KakaoTalk?lang=ENG) via [matrix-appservice-kakaotalk](https://src.miscworks.net/fair/matrix-appservice-kakaotalk) — a bridge based on [node-kakao](https://github.com/storycraft/node-kakao) (now unmaintained) and some [mautrix-facebook](https://github.com/mautrix/facebook) code. Thanks to [hnarjis](https://github.com/hnarjis) for helping us add support for this!

See our [Setting up Appservice Kakaotalk bridging](docs/configuring-playbook-bridge-appservice-kakaotalk.md) documentation to get started.


# 2022-07-20

## maubot support

Thanks to [Stuart Mumford (@Cadair)](https://github.com/cadair) for starting ([PR #373](https://github.com/spantaleev/matrix-docker-ansible-deploy/pull/373) and [PR #622](https://github.com/spantaleev/matrix-docker-ansible-deploy/pull/622)) and to [Julian-Samuel Gebühr (@moan0s)](https://github.com/moan0s) for finishing up (in [PR #1894](https://github.com/spantaleev/matrix-docker-ansible-deploy/pull/1894)), the playbook can now help you set up [maubot](https://github.com/maubot/maubot) — a plugin-based Matrix bot system.

See our [Setting up maubot](docs/configuring-playbook-bot-maubot.md) documentation to get started.


# 2022-07-14

## mx-puppet-skype removal

The playbook no longer includes the [mx-puppet-skype](https://github.com/Sorunome/mx-puppet-skype) bridge, because it has been broken and unmaintained for a long time. Users that have `matrix_mx_puppet_skype_enabled` in their configuration files will encounter an error when running the playbook until they remove references to this bridge from their configuration.

To completely clean up your server from `mx-puppet-skype`'s presence on it:

- ensure your Ansible configuration (`vars.yml` file) no longer contains `matrix_mx_puppet_skype_*` references
- stop and disable the systemd service (run `systemctl disable --now matrix-mx-puppet-skype` on the server)
- delete the systemd service (run `rm /etc/systemd/system/matrix-mx-puppet-skype.service` on the server)
- delete `/matrix/mx-puppet-skype` (run `rm -rf /matrix/mx-puppet-skype` on the server)
- drop the `matrix_mx_puppet_skype` database (run `/usr/local/bin/matrix-postgres-cli` on the server, and execute the `DROP DATABASE matrix_mx_puppet_skype;` query there)

If you still need bridging to [Skype](https://www.skype.com/), consider switching to [go-skype-bridge](https://github.com/kelaresg/go-skype-bridge) instead. See [Setting up Go Skype Bridge bridging](docs/configuring-playbook-bridge-go-skype-bridge.md).

If you think this is a mistake and `mx-puppet-skype` works for you (or you get it to work somehow), let us know and we may reconsider this removal.

## signald (0.19.0+) upgrade requires data migration

In [Pull Request #1921](https://github.com/spantaleev/matrix-docker-ansible-deploy/pull/1921) we upgraded [signald](https://signald.org/) (used by the mautrix-signal bridge) from `v0.18.5` to `v0.20.0`.

Back in the [`v0.19.0` released of signald](https://gitlab.com/signald/signald/-/blob/main/releases/0.19.0.md) (which we skipped and migrated straight to `v0.20.0`), a new `--migrate-data` command had been added that migrates avatars, group images, attachments, etc., into the database (those were previously stored in the filesystem).

If you've been using the mautrix-signal bridge for a while, you may have files stored in the local filesystem, which will need to be upgraded.

We attempt to do this data migration automatically every time Signald starts (`matrix-mautrix-signal-daemon.service`) using a `ExecStartPre` systemd unit definition.

Keep an eye on your Signal bridge and let us know (in our [support room](README.md#support) or in [Pull Request #1921](https://github.com/spantaleev/matrix-docker-ansible-deploy/pull/1921)) if you experience any trouble!


# 2022-07-05

## Ntfy push notifications support

Thanks to [Julian Foad](https://matrix.to/#/@julian:foad.me.uk), the playbook can now install a [ntfy](https://ntfy.sh/) push notifications server for you.

See our [Setting up the ntfy push notifications server](docs/configuring-playbook-ntfy.md) documentation to get started.


# 2022-06-23

## (Potential Backward Compatibility Break) Changes around metrics collection

**TLDR**: we've made extensive **changes to metrics exposure/collection, which concern people using an external Prometheus server**. If you don't know what that is, you don't need to read below.

**Why do major changes to metrics**? Because various services were exposing metrics in different, hacky, ways. Synapse was exposing metrics at `/_synapse/metrics` and `/_synapse-worker-…/metrics` on the `matrix.example.com`. The Hookshot role was **repurposing** the Granana web UI domain (`stats.example.com`) for exposing its metrics on `stats.example.com/hookshot/metrics`, while protecting these routes using Basic Authentication **normally used for Synapse** (`/_synapse/metrics`). Node-exporter and Postgres-exporter roles were advising for more `stats.example.com` usage in manual ways. Each role was doing things differently and mixing variables from other roles. Each metrics endpoint was ending up in a different place, protected by who knows what Basic Authentication credentials (if protected at all).

**The solution**: a completely revamped way to expose metrics to an external Prometheus server. We are **introducing new `https://matrix.example.com/metrics/*` endpoints**, where various services *can* expose their metrics, for collection by external Prometheus servers. To enable the `/metrics/*` endpoints, use `matrix_nginx_proxy_proxy_matrix_metrics_enabled: true`. There's also a way to protect access using [Basic Authentication](https://en.wikipedia.org/wiki/Basic_access_authentication). See the `matrix-nginx-proxy` role or our [Collecting metrics to an external Prometheus server](docs/configuring-playbook-prometheus-grafana.md#collecting-metrics-to-an-external-prometheus-server) documentation for additional variables around `matrix_nginx_proxy_proxy_matrix_metrics_enabled`.

**If you are using the [Hookshot bridge](docs/configuring-playbook-bridge-hookshot.md)**, you may find that:
1. **Metrics may not be enabled by default anymore**:
    - If Prometheus is enabled (`prometheus_enabled: true`), then Hookshot metrics will be enabled automatically (`matrix_hookshot_metrics_enabled: true`). These metrics will be collected from the local (in-container) Prometheus over the container network.
    - **If Prometheus is not enabled** (you are either not using Prometheus or are using an external one), **Hookshot metrics will not be enabled by default anymore**. Feel free to enable them by setting `matrix_hookshot_metrics_enabled: true`. Also, see below.
2. When metrics are meant to be **consumed by an external Prometheus server**, `matrix_hookshot_metrics_proxying_enabled` needs to be set to `true`, so that metrics would be exposed (proxied) "publicly" on `https://matrix.example.com/metrics/hookshot`. To make use of this, you'll also need to enable the new `https://matrix.example.com/metrics/*` endpoints mentioned above, using `matrix_nginx_proxy_proxy_matrix_metrics_enabled`. Learn more in our [Collecting metrics to an external Prometheus server](docs/configuring-playbook-prometheus-grafana.md#collecting-metrics-to-an-external-prometheus-server) documentation.
3. **We've changed the URL we're exposing Hookshot metrics at** for external Prometheus servers. Until now, you were advised to consume Hookshot metrics from `https://stats.example.com/hookshot/metrics` (working in conjunction with `matrix_nginx_proxy_proxy_synapse_metrics`). From now on, **this no longer works**. As described above, you need to start consuming metrics from `https://matrix.example.com/metrics/hookshot`.

**If you're using node-exporter** (`matrix_prometheus_node_exporter_enabled: true`) and would like to collect its metrics from an external Prometheus server, see `matrix_prometheus_node_exporter_metrics_proxying_enabled` described in our [Collecting metrics to an external Prometheus server](docs/configuring-playbook-prometheus-grafana.md#collecting-metrics-to-an-external-prometheus-server) documentation. You will be able to collect its metrics from `https://matrix.example.com/metrics/node-exporter`.

**If you're using [postgres-exporter](docs/configuring-playbook-prometheus-grafana.md#enable-metrics-and-graphs-for-postgres-optional)** (`prometheus_postgres_exporter_enabled: true`) and would like to collect its metrics from an external Prometheus server, see `matrix_prometheus_services_proxy_connect_prometheus_postgres_exporter_metrics_proxying_enabled` described in our [Collecting metrics to an external Prometheus server](docs/configuring-playbook-prometheus-grafana.md#collecting-metrics-to-an-external-prometheus-server) documentation. You will be able to collect its metrics from `https://matrix.example.com/metrics/postgres-exporter`.

**If you're using Synapse** and would like to collect its metrics from an external Prometheus server, you may find that:

1. Exposing metrics is now done using `matrix_synapse_metrics_proxying_enabled`, not `matrix_nginx_proxy_proxy_synapse_metrics: true`. You may still need to enable metrics using `matrix_synapse_metrics_enabled: true` before exposing them.
2. Protecting metrics endpoints using [Basic Authentication](https://en.wikipedia.org/wiki/Basic_access_authentication) is now done in another way. See our [Collecting metrics to an external Prometheus server](docs/configuring-playbook-prometheus-grafana.md#collecting-metrics-to-an-external-prometheus-server) documentation
3. If Synapse metrics are exposed, they will be made available at `https://matrix.example.com/metrics/synapse/main-process` or `https://matrix.example.com/metrics/synapse/worker/TYPE-ID` (when workers are enabled), not at `https://matrix.example.com/_synapse/metrics` and `https://matrix.example.com/_synapse-worker-…/metrics`
4. The playbook still generates an `external_prometheus.yml.example` sample file for scraping Synapse from Prometheus as described in [Collecting Synapse worker metrics to an external Prometheus server](docs/configuring-playbook-prometheus-grafana.md#collecting-synapse-worker-metrics-to-an-external-prometheus-server), but it's now saved under `/matrix/synapse` (not `/matrix`).

**If you where already using a external Prometheus server** before this change, and you gave a hashed version of the password as a variable, the playbook will now take care of hashing the password for you. Thus, you need to provide the non-hashed version now.

# 2022-06-13

## go-skype-bridge bridging support

Thanks to [CyberShadow](https://github.com/CyberShadow), the playbook can now install the [go-skype-bridge](https://github.com/kelaresg/go-skype-bridge) bridge for bridging Matrix to [Skype](https://www.skype.com/).

See our [Setting up Go Skype Bridge bridging](docs/configuring-playbook-bridge-go-skype-bridge.md) documentation to get started.

The playbook has supported [mx-puppet-skype](https://github.com/Sorunome/mx-puppet-skype) bridging (see [Setting up MX Puppet Skype bridging](docs/configuring-playbook-bridge-mx-puppet-skype.md)) since [2020-04-09](#2020-04-09), but `mx-puppet-skype` is reportedly broken.


# 2022-06-09

## Running Ansible in a container can now happen on the Matrix server itself

If you're tired of being on an old and problematic Ansible version, you can now run [run Ansible in a container on the Matrix server itself](docs/ansible.md#running-ansible-in-a-container-on-the-matrix-server-itself).


# 2022-05-31

## Synapse v1.60 upgrade may cause trouble and require manual intervention

Synapse v1.60 will try to add a new unique index to `state_group_edges` upon startup and could fail if your database is corrupted.

We haven't observed this problem yet, but [the Synapse v1.60.0 upgrade notes](https://github.com/element-hq/synapse/blob/v1.60.0/docs/upgrade.md#adding-a-new-unique-index-to-state_group_edges-could-fail-if-your-database-is-corrupted) mention it, so we're giving you a heads up here in case you're unlucky.

**If Synapse fails to start** after your next playbook run, you'll need to:

- SSH into the Matrix server
- launch `/usr/local/bin/matrix-postgres-cli`
- switch to the `synapse` database: `\c synapse`
- run the following SQL query:

```sql
BEGIN;
DELETE FROM state_group_edges WHERE (ctid, state_group, prev_state_group) IN (
  SELECT row_id, state_group, prev_state_group
  FROM (
    SELECT
      ctid AS row_id,
      MIN(ctid) OVER (PARTITION BY state_group, prev_state_group) AS min_row_id,
      state_group,
      prev_state_group
    FROM state_group_edges
  ) AS t1
  WHERE row_id <> min_row_id
);
COMMIT;
```

You could then restart services: `ansible-playbook -i inventory/hosts setup.yml --tags=start`


# 2022-04-25

## Buscarron bot support

Thanks to [Aine](https://gitlab.com/etke.cc) of [etke.cc](https://etke.cc/), the playbook can now set up [the Buscarron bot](https://github.com/etkecc/buscarron). It's a bot you can use to send any form (HTTP POST, HTML) to a (encrypted) Matrix room

See our [Setting up Buscarron](docs/configuring-playbook-bot-buscarron.md) documentation to get started.


# 2022-04-21

## matrix-registration-bot support

Thanks to [Julian-Samuel Gebühr (@moan0s)](https://github.com/moan0s), the playbook can now help you set up [matrix-registration-bot](https://github.com/moan0s/matrix-registration-bot) — a bot that is used to create and manage registration tokens for a Matrix server.

See our [Setting up matrix-registration-bot](docs/configuring-playbook-bot-matrix-registration-bot.md) documentation to get started.


# 2022-04-19

## BorgBackup support

Thanks to [Aine](https://gitlab.com/etke.cc) of [etke.cc](https://etke.cc/), the playbook can now set up [Borg](https://www.borgbackup.org/) backups with [borgmatic](https://torsion.org/borgmatic/) of your Matrix server.

See our [Setting up BorgBackup](docs/configuring-playbook-backup-borg.md) documentation to get started.

## (Compatibility Break) Upgrading to Synapse v1.57 on setups using workers may require manual action

If you're running a worker setup for Synapse (`matrix_synapse_workers_enabled: true`), the [Synapse v1.57 upgrade notes](https://github.com/element-hq/synapse/blob/v1.57.0rc1/docs/upgrade.md#changes-to-database-schema-for-application-services) say that you may need to take special care when upgrading:

> Synapse v1.57.0 includes a change to the way transaction IDs are managed for application services. If your deployment uses a dedicated worker for application service traffic, **it must be stopped** when the database is upgraded (which normally happens when the main process is upgraded), to ensure the change is made safely without any risk of reusing transaction IDs.

If you're not running an `appservice` worker (`matrix_synapse_workers_preset: little-federation-helper` or `matrix_synapse_workers_appservice_workers_count: 0`), you are probably safe to upgrade as per normal, without taking any special care.

If you are running a setup with an `appservice` worker, or otherwise want to be on the safe side, we recommend the following upgrade path:

0. Pull the latest playbook changes
1. Stop all services (`ansible-playbook -i inventory/hosts setup.yml --tags=stop`)
2. Re-run the playbook (`ansible-playbook -i inventory/hosts setup.yml --tags=setup-all`)
3. Start Postgres (`systemctl start matrix-postgres` on the server)
4. Start the main Synapse process (`systemctl start matrix-synapse` on the server)
5. Wait a while so that Synapse can start and complete the database migrations. You can use `journalctl -fu matrix-synapse` on the server to get a clue. Waiting a few minutes should also be enough.
6. It should now be safe to start all other services. `ansible-playbook -i inventory/hosts setup.yml --tags=start` will do it for you


# 2022-04-14

## (Compatibility Break) Changes to `docker-src` permissions necessitating manual action

Users who build container images from source will need to manually correct file permissions of some directories on the server.

When self-building, the playbook used to `git clone` repositories (into `/matrix/SERVICE/docker-src`) using the `root` user, but now uses `matrix` instead to work around [the following issue with git 2.35.2](https://github.com/spantaleev/matrix-docker-ansible-deploy/issues/1749).

If you're on a non-`amd64` architecture (that is, you're overriding `matrix_architecture` in your `vars.yml` file) or you have enabled self-building for some service (e.g. `matrix_*_self_build: true`), you're certainly building some container images from source and have `docker-src` directories with mixed permissions lying around in various `/matrix/SERVICE` directories.

The playbook *could* correct these permissions automatically, but that requires additional Ansible tasks in some ~45 different places — something that takes considerable effort. So we ask users observing errors related to `docker-src` directories to correct the problem manually by **running this command on the Matrix server** (which deletes all `/matrix/*/docker-src` directories): `find /matrix -maxdepth 2 -name 'docker-src' | xargs rm -rf`


# 2022-03-17

## (Compatibility Break) ma1sd identity server no longer installed by default

The playbook no longer installs the [ma1sd](https://github.com/ma1uta/ma1sd) identity server by default. The next time you run the playbook, ma1sd will be uninstalled from your server, unless you explicitly enable the ma1sd service (see how below).

The main reason we used to install ma1sd by default in the past was to prevent Element clients from talking to the `matrix.org` / `vector.im` identity servers, by forcing it to talk to our own self-hosted (but otherwise useless) identity server instead, thus preventing contact list leaks.

Since Element clients no longer default to using a public identity server if another one is not provided, we can stop installing ma1sd.

If you need to install the ma1sd identity server for some reason, you can explicitly enable it by adding this to your `vars.yml` file:

```yaml
matrix_ma1sd_enabled: true
```


# 2022-02-12

## matrix_encryption_disabler support

We now support installing the [matrix_encryption_disabler](https://github.com/digitalentity/matrix_encryption_disabler) Synapse module, which lets you prevent End-to-End-Encryption from being enabled by users on your homeserver. The popular opinion is that this is dangerous and shouldn't be done, but there are valid use cases for disabling encryption discussed [here](https://github.com/matrix-org/synapse/issues/4401).

To enable this module (and prevent encryption from being used on your homserver), add `matrix_synapse_ext_encryption_disabler_enabled: true` to your configuration. This module provides further customization. Check its other configuration settings (and defaults) in `roles/custom/matrix-synapse/defaults/main.yml`.


# 2022-02-01

## matrix-hookshot bridging support

Thanks to [HarHarLinks](https://github.com/HarHarLinks), the playbook can now install the [matrix-hookshot](https://github.com/matrix-org/matrix-hookshot) bridge for bridging Matrix to multiple project management services, such as GitHub, GitLab and JIRA. See our [Setting up matrix-hookshot](docs/configuring-playbook-bridge-hookshot.md) documentation to get started.


# 2022-01-31

## ARM support for matrix-corporal

[matrix-corporal](https://github.com/devture/matrix-corporal) (as of version `2.2.3`) is now published to Docker Hub (see [devture/matrix-corporal](https://hub.docker.com/r/devture/matrix-corporal)) as a multi-arch container image with support for all these platforms: `linux/amd64`, `linux/arm64/v8` and `linux/arm/v7`. The playbook no longer resorts to self-building matrix-corporal on these ARM architectures.


# 2022-01-07

## Dendrite support

**TLDR**: We now have optional experimental [Dendrite](https://github.com/matrix-org/dendrite) homeserver support for new installations. **Existing (Synapse) installations need to be updated**, because some internals changed. See [Adapting the configuration for existing Synapse installations](#adapting-the-configuration-for-existing-synapse-installations).

[Jip J. Dekker](https://github.com/Dekker1) did the [initial work](https://github.com/spantaleev/matrix-docker-ansible-deploy/pull/818) of adding [Dendrite](https://github.com/matrix-org/dendrite) support to the playbook back in January 2021. Lots of work (and time) later, Dendrite support is finally ready for testing.

We believe that 2022 will be the year of the non-Synapse Matrix server!

The playbook was previously quite [Synapse](https://github.com/element-hq/synapse)-centric, but can now accommodate multiple homeserver implementations. Only one homeserver implementation can be active (installed) at a given time.

**Synapse is still the default homeserver implementation** installed by the playbook. A new variable (`matrix_homeserver_implementation`) controls which server implementation is enabled (`synapse` or `dendrite` at the given moment).

### Adapting the configuration for existing Synapse installations

Because the playbook is not so Synapse-centric anymore, a small configuration change is necessary for existing installations to bring them up to date.

The `vars.yml` file for **existing installations will need to be updated** by adding this **additional configuration**:

```yaml
# All secrets keys are now derived from `matrix_homeserver_generic_secret_key`, not from `matrix_synapse_macaroon_secret_key`.
# To keep them all the same, define `matrix_homeserver_generic_secret_key` in terms of `matrix_synapse_macaroon_secret_key`.
# Using a new secret value for this configuration key is also possible and should not cause any problems.
#
# Fun fact: new installations (based on the new `examples/vars.yml` file) do this in reverse.
# That is, the Synapse macaroon secret is derived from `matrix_homeserver_generic_secret_key`.
matrix_homeserver_generic_secret_key: "{{ matrix_synapse_macaroon_secret_key }}"
```

### Trying out Dendrite

Finally, **to try out Dendrite**, we recommend that you **use a new server** and the following addition to your `vars.yml` configuration:

```yaml
matrix_homeserver_implementation: dendrite
```

**The homeserver implementation of an existing server cannot be changed** (e.g. from Synapse to Dendrite) without data loss.

We're excited to gain support for other homeserver implementations, like [Conduit](https://conduit.rs/), etc!

## Honoroit bot support

Thanks to [Aine](https://gitlab.com/etke.cc) of [etke.cc](https://etke.cc/), the playbook can now help you set up [Honoroit](https://github.com/etkecc/honoroit) — a helpdesk bot.

See our [Setting up Honoroit](docs/configuring-playbook-bot-honoroit.md) documentation to get started.


# 2022-01-06

## Cinny support

Thanks to [Aine](https://gitlab.com/etke.cc) of [etke.cc](https://etke.cc/), the playbook now supports [Cinny](https://cinny.in/) — a new simple, elegant and secure Matrix client.

By default, we still install Element Web. Still, people who'd like to try Cinny out can now install it via the playbook.

Additional details are available in [Setting up Cinny](docs/configuring-playbook-client-cinny.md).


# 2021-12-22

## Twitter bridging support via mautrix-twitter

Thanks to [Matthew Cengia](https://github.com/mattcen) and [Shreyas Ajjarapu](https://github.com/shreyasajj), besides [mx-puppet-twitter](docs/configuring-playbook-bridge-mx-puppet-twitter.md), bridging to [Twitter](https://twitter.com/) can now also happen with [mautrix-twitter](docs/configuring-playbook-bridge-mautrix-twitter.md).


# 2021-12-14

## (Security) Users of the Signal bridge may wish to upgrade it to work around log4j vulnerability

Recently, a security vulnerability affecting the Java logging package `log4j` [has been discovered](https://www.huntress.com/blog/rapid-response-critical-rce-vulnerability-is-affecting-java). Software that uses this Java package is potentially vulnerable.

One such piece of software that is part of the playbook is the [mautrix-signal bridge](./docs/configuring-playbook-bridge-mautrix-signal.md), which [has been patched already](https://github.com/spantaleev/matrix-docker-ansible-deploy/pull/1452). If you're running this bridge, you may wish to [upgrade](./docs/maintenance-upgrading-services.md).


# 2021-11-11

## Dropped support for Postgres v9.6

Postgres v9.6 reached its end of life today, so the playbook will refuse to run for you if you're still on that version.

Synapse still supports v9.6 (for now), but we're retiring support for it early, to avoid having to maintain support for so many Postgres versions. Users that are still on Postgres v9.6 can easily [upgrade Postgres](docs/maintenance-postgres.md#upgrading-postgresql) via the playbook.


# 2021-10-23

## Hangouts bridge no longer updated, superseded by a Googlechat bridge

The mautrix-hangouts bridge is no longer receiving updates upstream and is likely to stop working in the future. We still retain support for this bridge in the playbook, but you're encouraged to switch away from it.

There's a new [mautrix-googlechat](https://github.com/mautrix/googlechat) bridge that you can [install using the playbook](docs/configuring-playbook-bridge-mautrix-googlechat.md). Your **Hangouts bridge data will not be migrated**, however. You need to start fresh with the new bridge.


# 2021-08-23

## LinkedIn bridging support via beeper-linkedin

Thanks to [Alexandar Mechev](https://github.com/apmechev), the playbook can now install the [beeper-linkedin](https://gitlab.com/beeper/linkedin) bridge for bridging to [LinkedIn](https://www.linkedin.com/) Messaging.

This brings the total number of bridges supported by the playbook up to 20. See all supported bridges [here](docs/configuring-playbook.md#bridging-other-networks).

To get started with bridging to LinkedIn, see [Setting up Beeper LinkedIn bridging](docs/configuring-playbook-bridge-beeper-linkedin.md).


# 2021-08-20

# Sygnal upgraded — ARM support and no longer requires a database

The [Sygnal](docs/configuring-playbook-sygnal.md) push gateway has been upgraded from `v0.9.0` to `v0.10.1`.

This is an optional component for the playbook, so most of our users wouldn't care about this announcement.

Since this feels like a relatively big (and untested, as of yet) Sygnal change, we're putting up this changelog entry.

The new version is also available for the ARM architecture. It also no longer requires a database anymore. If you need to downgrade to the previous version, changing `matrix_sygnal_version` or `matrix_sygnal_docker_image` will not be enough, as we've removed the `database` configuration completely. You'd need to switch to an earlier playbook commit.


# 2021-05-21

## Hydrogen support

Thanks to [Aaron Raimist](https://github.com/aaronraimist), the playbook now supports [Hydrogen](https://github.com/vector-im/hydrogen-web) — a new lightweight Matrix client with legacy and mobile browser support.

By default, we still install Element Web, as Hydrogen is still not fully-featured. Still, people who'd like to try Hydrogen out can now install it via the playbook.

Additional details are available in [Setting up Hydrogen](docs/configuring-playbook-client-hydrogen.md).


# 2021-05-19

## Heisenbridge support

Thanks to [Toni Spets (hifi)](https://github.com/hifi), the playbook now supports bridging to [IRC](https://en.wikipedia.org/wiki/Internet_Relay_Chat) using yet another bridge (besides matrix-appservice-irc), called [Heisenbridge](https://github.com/hifi/heisenbridge).

Additional details are available in [Setting up Heisenbridge bouncer-style IRC bridging](docs/configuring-playbook-bridge-heisenbridge.md).


# 2021-04-16

## Disabling TLSv1 and TLSv1.1 for coturn

To improve security, we've [removed TLSv1 and TLSv1.1 support](https://github.com/spantaleev/matrix-docker-ansible-deploy/pull/999) from our default [coturn](https://github.com/coturn/coturn) configuration.

If you need to support old clients, you can re-enable both (or whichever one you need) with the following configuration:

```yaml
matrix_coturn_tls_v1_enabled: true
matrix_coturn_tls_v1_1_enabled: true
```


# 2021-04-05

## Automated local Postgres backup support

Thanks to [foxcris](https://github.com/foxcris), the playbook can now make automated local Postgres backups on a fixed schedule using [docker-postgres-backup-local](https://github.com/prodrigestivill/docker-postgres-backup-local).

Additional details are available in [Setting up Postgres backup](docs/configuring-playbook-postgres-backup.md).


# 2021-04-03

## Mjolnir moderation tool (bot) support

Thanks to [Aaron Raimist](https://github.com/aaronraimist), the playbook can now install and configure the [Mjolnir](https://github.com/matrix-org/mjolnir) moderation tool (bot).

Additional details are available in [Setting up Mjolnir](docs/configuring-playbook-bot-mjolnir.md).


# 2021-03-20

## Sygnal push gateway support

The playbook can now install the [Sygnal](https://github.com/matrix-org/sygnal) push gateway for you.

This is only useful to people who develop/build their own Matrix client applications.

Additional details are available in our [Setting up the Sygnal push gateway](docs/configuring-playbook-sygnal.md) docs.


# 2021-03-16

## Go-NEB support

Thanks to [Zir0h](https://github.com/Zir0h), the playbook can now install and configure the [Go-NEB](https://github.com/matrix-org/go-neb) bot.

Additional details are available in [Setting up Go-NEB](docs/configuring-playbook-bot-go-neb.md).


# 2021-02-19

## GroupMe bridging support via mx-puppet-groupme

Thanks to [Cody Neiman](https://github.com/xangelix), the playbook can now install the [mx-puppet-groupme](https://gitlab.com/robintown/mx-puppet-groupme) bridge for bridging to [GroupMe](https://groupme.com).

This brings the total number of bridges supported by the playbook up to 18. See all supported bridges [here](docs/configuring-playbook.md#bridging-other-networks).

To get started, follow our [Setting up MX Puppet GroupMe](docs/configuring-playbook-bridge-mx-puppet-groupme.md) docs.

## Mautrix Instagram bridging support

The playbook now supports bridging with [Instagram](https://www.instagram.com/) by installing the [mautrix-instagram](https://github.com/tulir/mautrix-instagram) bridge. This playbook functionality is available thanks to [@MarcProe](https://github.com/MarcProe).

Additional details are available in [Setting up Mautrix Instagram bridging](docs/configuring-playbook-bridge-mautrix-instagram.md).

## Synapse workers support

After [lots and lots of work](https://github.com/spantaleev/matrix-docker-ansible-deploy/pull/456) (done over many months by [Marcel Partap](https://github.com/eMPee584), [Max Klenk](https://github.com/maxklenk), a few others from the [Technical University of Dresden, Germany](https://tu-dresden.de/) and various other contributors), support for Synapse workers has finally landed.

Having support for workers makes the playbook suitable for larger homeserver deployments.

Our setup is not yet perfect (we don't support all types of workers; scaling some of them (like `pusher`, `federation_sender`) beyond a single instance is not yet supported). Still, it's a great start and can already power homeservers with thousands of users, like the [Matrix deployment at TU Dresden](https://doc.matrix.tu-dresden.de/en/) discussed in [Matrix Live S06E09 — TU Dresden on their Matrix deployment](https://www.youtube.com/watch?v=UHJX2pmT2gk).

By default, workers are disabled and Synapse runs as a single process (homeservers don't necessarily need the complexity and increased memory requirements of running a worker-based setup).

To enable Synapse workers, follow our [Load balancing with workers](docs/configuring-playbook-synapse.md#load-balancing-with-workers) documentation.


# 2021-02-12

## (Potential Breaking Change) Monitoring/metrics support using Prometheus and Grafana

Thanks to [@Peetz0r](https://github.com/Peetz0r), the playbook can now install a bunch of tools for monitoring your Matrix server: the [Prometheus](https://prometheus.io) time-series database server, the Prometheus [node-exporter](https://prometheus.io/docs/guides/node-exporter/) host metrics exporter, and the [Grafana](https://grafana.com/) web UI.

To get get these installed, follow our [Enabling metrics and graphs (Prometheus, Grafana) for your Matrix server](docs/configuring-playbook-prometheus-grafana.md) docs page.

This update comes with a **potential breaking change** for people who were already exposing Synapse metrics (for consumption via another Prometheus installation). From now on, `matrix_synapse_metrics_enabled: true` no longer exposes metrics publicly via matrix-nginx-proxy (at `https://matrix.example.com/_synapse/metrics`). To do so, you'd need to explicitly set `matrix_nginx_proxy_proxy_synapse_metrics: true`.


# 2021-01-31

## Etherpad support

Thanks to [@pushytoxin](https://github.com/pushytoxin), the playbook can now install the [Etherpad](https://etherpad.org) realtime collaborative text editor. It can be used in a [Jitsi](https://jitsi.org/) audio/video call or integrated as a widget into Matrix chat rooms via the [Dimension](https://dimension.t2bot.io) integration manager.

To get it installed, follow [our Etherpad docs page](docs/configuring-playbook-etherpad.md).


# 2021-01-22

## (Breaking Change) Postgres changes that require manual intervention

We've made a lot of changes to our Postgres setup and some manual action is required (described below). Sorry about the hassle.

**TLDR**: people running an [external Postgres server](docs/configuring-playbook-external-postgres.md) don't need to change anything for now. Everyone else (the common/default case) is affected and manual intervention is required.

### Why?

- we had a default Postgres password (`matrix_postgres_connection_password: synapse-password`), which we think is **not ideal for security anymore**. We now ask you to generate/provide a strong password yourself. Postgres is normally not exposed outside the container network, making it relatively secure, but still:
  - by tweaking the configuration, you may end up intentionally or unintentionally exposing your Postgres server to the local network (or even publicly), while still using the default default credentials (`synapse` + `synapse-password`)
  - we can't be sure we trust all these services (bridges, etc). Some of them may try to talk to or attack `matrix-postgres` using the default credentials (`synapse` + `synapse-password`)
  - you may have other containers running on the same Docker network, which may try to talk to or attack `matrix-postgres` using the default credentials (`synapse` + `synapse-password`)
- our Postgres usage **was overly-focused on Synapse** (default username of `synapse` and default/main database of `homeserver`). Additional homeserver options are likely coming in the future ([Dendrite](https://matrix.org/docs/projects/server/dendrite), [Conduit](https://matrix.org/docs/projects/server/conduit), [The Construct](https://matrix.org/docs/projects/server/construct)), so being too focused on `matrix-synapse` is not great. From now on, Synapse is just another component of this playbook, which happens to have an *additional database* (called `synapse`) on the Postgres server.
- we try to reorganize things a bit, to make the playbook even friendlier to people running an [external Postgres server](docs/configuring-playbook-external-postgres.md). Work on this will proceed in the future.

So, this is some **effort to improve security** and to **prepare for a brighter future of having more homeserver options** than just Synapse.

### What has really changed?

- the default superuser Postgres username is now `matrix` (used to be `synapse`)
- the default Postgres database is now `matrix` (used to be `homeserver`)
- Synapse's database is now `synapse` (used to be `homeserver`). This is now just another "additional database" that the playbook manages for you
- Synapse's user called `synapse` is just a regular user that can only use the `synapse` database (not a superuser anymore)

### What do I do if I'm using the integrated Postgres server (default)?

By default, the playbook runs an integrated Postgres server for you in a container (`matrix-postgres`). Unless you've explicitly configured an [external Postgres server](docs/configuring-playbook-external-postgres.md), these steps are meant for you.

To migrate to the new setup, expect a few minutes of downtime, while you follow these steps:

1. We believe the steps below are safe and you won't encounter any data loss, but consider [making a Postgres backup](docs/maintenance-postgres.md#backing-up-postgresql) anyway. If you've never backed up Postgres, now would be a good time to try it.

2. Generate a strong password to be used for your superuser Postgres user (called `matrix`). You can create one with a command like `pwgen -s 64 1`. The **maximum length** for a Postgres password is 100 bytes (characters). Don't go crazy!

3. Update your playbook's `inventory/host_vars/matrix.example.com/vars.yml` file, adding a line like this:
    ```yaml
    matrix_postgres_connection_password: 'YOUR_POSTGRES_PASSWORD_HERE'
    ```

… where `YOUR_POSTGRES_PASSWORD_HERE` is to be replaced with the password you generated during step #2.

4. Stop all services: `ansible-playbook -i inventory/hosts setup.yml --tags=stop`
5. Log in to the server via SSH. The next commands will be performed there.
6. Start the Postgres database server: `systemctl start matrix-postgres`
7. Open a Postgres shell: `/usr/local/bin/matrix-postgres-cli`
8. Execute the following query, while making sure to **change the password inside** (**don't forget the ending `;`**):

    ```sql
    CREATE ROLE matrix LOGIN SUPERUSER PASSWORD 'YOUR_POSTGRES_PASSWORD_HERE';
    ```

… where `YOUR_POSTGRES_PASSWORD_HERE` is to be replaced with the password you generated during step #2.

9. Execute the following queries as you see them (no modifications necessary, so you can just **paste them all at once**):

    ```sql
    CREATE DATABASE matrix OWNER matrix;

    ALTER DATABASE postgres OWNER TO matrix;
    ALTER DATABASE template0 OWNER TO matrix;
    ALTER DATABASE template1 OWNER TO matrix;

    \c matrix;

    ALTER DATABASE homeserver RENAME TO synapse;

    ALTER ROLE synapse NOSUPERUSER NOCREATEDB NOCREATEROLE;

    \quit
    ```

    You may need to press *Enter* after pasting the lines above.

10. Re-run the playbook normally: `ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start`

### What do I do if I'm using an external Postgres server?

If you've explicitly configured an [external Postgres server](docs/configuring-playbook-external-postgres.md), there are **no changes** that you need to do at this time.

The fact that we've renamed Synapse's database from `homeserver` to `synapse` (in our defaults) should not affect you, as you're already explicitly defining `matrix_synapse_database_database` (if you've followed our guide, that is). If you're not explicitly defining this variable, you may wish to do so (`matrix_synapse_database_database: homeserver`), to avoid the new `synapse` default and keep things as they were.


# 2021-01-20

## (Breaking Change) The mautrix-facebook bridge now requires a Postgres database

**Update from 2021-11-15**: SQLite support has been re-added to the mautrix-facebook bridge in [v0.3.2](https://github.com/mautrix/facebook/releases/tag/v0.3.2). You can ignore this changelog entry.

A new version of the [mautrix-facebook](https://github.com/tulir/mautrix-facebook) bridge has been released. It's a full rewrite of its backend and the bridge now requires Postgres. New versions of the bridge can no longer run on SQLite.

**TLDR**: if you're NOT using an [external Postgres server](docs/configuring-playbook-external-postgres.md) and have NOT forcefully kept the bridge on SQLite during [The big move to all-on-Postgres (potentially dangerous)](#the-big-move-to-all-on-postgres-potentially-dangerous), you will be automatically upgraded without manual intervention. All you need to do is send a `login` message to the Facebook bridge bot again.

Whether this change requires your intervention depends mostly on:
- whether you're using an [external Postgres server](docs/configuring-playbook-external-postgres.md). If yes, then [you need to do something](#upgrade-path-for-people-running-an-external-postgres-server).
- or whether you've force-changed the bridge's database engine to SQLite (`matrix_mautrix_facebook_database_engine: 'sqlite'` in your `vars.yml`) some time in the past (likely during [The big move to all-on-Postgres (potentially dangerous)](#the-big-move-to-all-on-postgres-potentially-dangerous)).

As already mentioned above, you most likely don't need to do anything. If you rerun the playbook and don't get an error, you've been automatically upgraded. Just send a `login` message to the Facebook bridge bot again. Otherwise, read below for a solution.

### Upgrade path for people NOT running an external Postgres server (default for the playbook)

If you're **not running an external Postgres server**, then this bridge either already works on Postgres for you, or you've intentionally kept it back on SQLite with custom configuration (`matrix_mautrix_facebook_database_engine: 'sqlite'` in your `vars.yml`) .

Simply remove that custom configuration from your `vars.yml` file (if it's there) and re-run the playbook. It should upgrade you automatically. You'll need to send a `login` message to the Facebook bridge bot again.

Alternatively, [you can stay on SQLite for a little longer](#staying-on-sqlite-for-a-little-longer-temporary-solution).

### Upgrade path for people running an external Postgres server

For people using the internal Postgres server (the default for the playbook):
- we automatically create an additional `matrix_mautrix_facebook` Postgres database and credentials to access it
- we automatically adjust the bridge's `matrix_mautrix_facebook_database_*` variables to point the bridge to that Postgres database
- we use [pgloader](https://pgloader.io/) to automatically import the existing SQLite data for the bridge into the `matrix_mautrix_facebook` Postgres database

If you are using an [external Postgres server](docs/configuring-playbook-external-postgres.md), unfortunately we currently can't do any of that for you.

You have 3 ways to proceed:

- contribute to the playbook to make this possible (difficult)
- or, do the migration "steps" manually:
  - stop the bridge (`systemctl stop matrix-mautrix-facebook`)
  - create a new `matrix_mautrix_facebook` Postgres database for it
  - run [pgloader](https://pgloader.io/) manually (we import this bridge's data using default settings and it works well)
  - define `matrix_mautrix_facebook_database_*` variables in your `vars.yml` file (credentials, etc.) — you can find their defaults in `roles/custom/matrix-mautrix-facebook/defaults/main.yml`
  - switch the bridge to Postgres (`matrix_mautrix_facebook_database_engine: 'postgres'` in your `vars.yml` file)
  - re-run the playbook (`--tags=setup-all,start`) and ensure the bridge works (`systemctl status matrix-mautrix-facebook` and `journalctl -fu matrix-mautrix-facebook`)
  - send a `login` message to the Facebook bridge bot again
- or, [stay on SQLite for a little longer (temporary solution)](#staying-on-sqlite-for-a-little-longer-temporary-solution)

### Staying on SQLite for a little longer (temporary solution)

To keep using this bridge with SQLite for a little longer (**not recommended**), use the following configuration in your `vars.yml` file:

```yaml
# Force-change the database engine to SQLite.
matrix_mautrix_facebook_database_engine: 'sqlite'

# Force-downgrade to the last bridge version which supported SQLite.
matrix_mautrix_facebook_docker_image: "{{ matrix_mautrix_facebook_docker_image_name_prefix }}tulir/mautrix-facebook:da1b4ec596e334325a1589e70829dea46e73064b"
```

If you do this, keep in mind that **you can't run this forever**. This SQLite-supporting bridge version is not getting any updates and will break sooner or later. The playbook will also drop support for SQLite at some point in the future.


# 2021-01-17

## matrix-corporal goes 2.0

[matrix-corporal v2 has been released](https://github.com/devture/matrix-corporal/releases/tag/2.0.0) and the playbook also supports it now.

No manual intervention is required in the common case.

The new [matrix-corporal](https://github.com/devture/matrix-corporal) version is also the first one to support Interactive Authentication. If you wish to enable that (hint: you should), you'll need to set up the [REST auth password provider](docs/configuring-playbook-rest-auth.md). There's more information in [our matrix-corporal docs](docs/configuring-playbook-matrix-corporal.md).


# 2021-01-14

## Moving from cronjobs to systemd timers

We no longer use cronjobs for Let's Encrypt SSL renewal and `matrix-nginx-proxy`/`matrix-coturn` reloading. Instead, we've switched to systemd timers.

The largest benefit of this is that we no longer require you to install a cron daemon, thus simplifying our install procedure.

The playbook will migrate you from cronjobs to systemd timers automatically. This is just a heads up.


# 2021-01-08

## (Breaking Change) New SSL configuration

SSL configuration (protocols, ciphers) can now be more easily controlled thanks to us making use of configuration presets.

We define a few presets (old, intermediate, modern), following the [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/#server=nginx).

A new variable `matrix_nginx_proxy_ssl_preset` controls which preset is used (defaults to `"intermediate"`).

Compared to before, this changes nginx's `ssl_prefer_server_ciphers` to `off`  (used to default to `on`). It also add some more ciphers to the list, giving better performance on mobile devices, and removes some weak ciphers. More information in the [documentation](docs/configuring-playbook-nginx.md).

To revert to the old behaviour, set the following variables:

```yaml
matrix_nginx_proxy_ssl_ciphers: "EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH"
matrix_nginx_proxy_ssl_prefer_server_ciphers: "on"
```

Just like before, you can still use your own custom protocols by specifying them in `matrix_nginx_proxy_ssl_protocols`. Doing so overrides the values coming from the preset.


# 2021-01-03

## Signal bridging support via mautrix-signal

Thanks to [laszabine](https://github.com/laszabine)'s efforts, the playbook now supports bridging to [Signal](https://www.signal.org/) via the [mautrix-signal](https://github.com/tulir/mautrix-signal) bridge. See our [Setting up Mautrix Signal bridging](docs/configuring-playbook-bridge-mautrix-signal.md) documentation page for getting started.

If you had installed the mautrix-signal bridge while its Pull Request was still work-in-progress, you can migrate your data to the new and final setup by referring to [this comment](https://github.com/spantaleev/matrix-docker-ansible-deploy/pull/686#issuecomment-753510789).


# 2020-12-23

## The big move to all-on-Postgres (potentially dangerous)

**TLDR**: all your bridges (and other services) will likely be auto-migrated from SQLite/nedb to Postgres, hopefully without trouble. You can opt-out (see how below), if too worried about breakage.

Until now, we've only used Postgres as a database for Synapse. All other services (bridges, bots, etc.) were kept simple and used a file-based database (SQLite or nedb).

Since [this huge pull request](https://github.com/spantaleev/matrix-docker-ansible-deploy/pull/740), **all of our services now use Postgres by default**. Thanks to [Johanna Dorothea Reichmann](https://github.com/jdreichmann) for starting the work on it and for providing great input!

Moving all services to Postgres brings a few **benefits** to us:

- **improved performance**
- **improved compatibility**. Most bridges are deprecating SQLite/nedb support or offer less features when not on Postgres.
- **easier backups**. It's still some effort to take a proper backup (Postgres dump + various files, keys), but a Postgres dump now takes you much further.
- we're now **more prepared to introduce other services** that need a Postgres database — [Dendrite](https://github.com/matrix-org/dendrite), the [mautrix-signal](https://github.com/tulir/mautrix-signal) bridge (existing [pull request](https://github.com/spantaleev/matrix-docker-ansible-deploy/pull/686)), etc.

### Key takeway

- existing installations that use an [external Postgres](https://github.com/spantaleev/matrix-docker-ansible-deploy/blob/master/docs/configuring-playbook-external-postgres.md) server should be unaffected (they remain on SQLite/nedb for all services, except Synapse)

- for existing installations which use our integrated Postgres database server (`matrix-postgres`, which is the default), **we automatically migrate data** from SQLite/nedb to Postgres and **archive the database files** (`something.db` -> `something.db.backup`), so you can restore them if you need to go back (see how below).

### Opting-out of the Postgres migration

This is a **very large and somewhat untested change** (potentially dangerous), so **if you're not feeling confident/experimental, opt-out** of it for now. Still, it's the new default and what we (and various bridges) will focus on going forward, so don't stick to old ways for too long.

You can remain on SQLite/nedb (at least for now) by adding a variable like this to your `vars.yml` file for each service you use: `matrix_COMPONENT_database_engine: sqlite` (e.g. `matrix_mautrix_facebook_database_engine: sqlite`).

Some services (like `appservice-irc` and `appservice-slack`) don't use SQLite, so use `nedb`, instead of `sqlite` for them.

### Going back to SQLite/nedb if things went wrong

If you went with the Postgres migration and it went badly for you (some bridge not working as expected or not working at all), do this:

- stop all services (`ansible-playbook -i inventory/hosts setup.yml --tags=stop`)
- SSH into the server and rename the old database files (`something.db.backup` -> `something.db`). Example: `mv /matrix/mautrix-facebook/data/mautrix-facebook.db.backup /matrix/mautrix-facebook/data/mautrix-facebook.db`
- switch the affected service back to SQLite (e.g. `matrix_mautrix_facebook_database_engine: sqlite`). Some services (like `appservice-irc` and `appservice-slack`) don't use SQLite, so use `nedb`, instead of `sqlite` for them.
- re-run the playbook (`ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start`)
- [get in touch](README.md#support) with us

# 2020-12-11

## synapse-janitor support removed

We've removed support for the unmaintained [synapse-janitor](https://github.com/xwiki-labs/synapse_scripts) script. There's been past reports of it corrupting the Synapse database. Since there hasn't been any new development on it and it doesn't seem too useful nowadays, there's no point in including it in the playbook.

If you need to clean up or compact your database, consider using the Synapse Admin APIs directly. See our [Synapse maintenance](docs/maintenance-synapse.md) and [Postgres maintenance](docs/maintenance-postgres.md) documentation pages for more details.

## Docker 20.10 is here

(No need to do anything special in relation to this. Just something to keep in mind)

Docker 20.10 got released recently and your server will likely get it the next time you update.

This is the first major Docker update in a long time and it packs a lot of changes. Some of them introduced some breakage for us initially (see [here](https://github.com/spantaleev/matrix-docker-ansible-deploy/commit/d08b27784f222effcbce2abf924bf07bbe0893be) and [here](https://github.com/spantaleev/matrix-docker-ansible-deploy/commit/7593d969e316cc0144bce378a5be58c76c2c37ee)), but it should be all good now.


# 2020-12-08

## openid APIs exposed by default on the federation port when federation disabled

We've changed some defaults. People running with our default configuration (federation enabled), are not affected at all.

If you are running an unfederated server (`matrix_synapse_federation_enabled: false`), this may be of interest to you.

When federation is disabled, but ma1sd or Dimension are enabled, we'll now expose the `openid` APIs on the federation port. These APIs are necessary for some ma1sd features to work. If you'd like to prevent this, you can: `matrix_synapse_federation_port_openid_resource_required: false`.


# 2020-11-27

## Recent Jitsi updates may require configuration changes

We've recently [updated from Jitsi build 4857 to build 5142](https://github.com/spantaleev/matrix-docker-ansible-deploy/pull/719), which brings a lot of configuration changes.

**If you use our default Jitsi settings, you won't have to do anything.**

People who have [fine-tuned Jitsi](docs/configuring-playbook-jitsi.md#optional-fine-tune-jitsi) may find that some options got renamed now, others are gone and yet others still need to be defined in another way.

The next time you run the playbook [installation](docs/installing.md) command, our validation logic will tell you if you're using some variables like that and will recommend a migration path for each one.

Additionally, we've recently disabled transcriptions (`jitsi_enable_transcriptions: false`) and recording (`jitsi_enable_recording: false`) by default. These features did not work anyway, because we don't install the required dependencies for them (Jigasi and Jibri, respectively). If you've been somehow pointing your Jitsi installation to some manually installed Jigasi/Jibri service, you may need to toggle these flags back to enabled to have transcriptions and recordings working.


# 2020-11-23

## Breaking change matrix-sms-bridge

Because of many problems using gammu as SMS provider, matrix-sms-bridge now uses (https://github.com/RebekkaMa/android-sms-gateway-server) by default. See (the docs)[./docs/configuring-playbook-bridge-matrix-bridge-sms.md] which new vars you need to add.

If you are using this playbook to deploy matrix-sms-bridge and still really want to use gammu as SMS provider, we could possibly add support for both android-sms-gateway-server and gammu.

# 2020-11-13

## Breaking change matrix-sms-bridge

The new version of [matrix-sms-bridge](https://github.com/benkuly/matrix-sms-bridge) changed its database from neo4j to h2. You need to sync the bridge at the first start. Note that this only will sync rooms where the @smsbot:yourServer is member. For rooms without @smsbot:yourServer you need to kick and invite the telephone number **or** invite @smsbot:yourServer.

1. Add the following to your `vars.yml` file: `matrix_sms_bridge_container_extra_arguments=['--env SPRING_PROFILES_ACTIVE=initialsync']`
2. Login to your host shell and remove old systemd file from your host: `rm /etc/systemd/system/matrix-sms-bridge-database.service`
3. Run `ansible-playbook -i inventory/hosts setup.yml --tags=setup-matrix-sms-bridge,start`
4. Login to your host shell and check the logs with `journalctl -u matrix-sms-bridge` until the sync finished.
5. Remove the var from the first step.
6. Run `ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start`.

# 2020-11-10

## Dynamic DNS support

Thanks to [Scott Crossen](https://github.com/scottcrossen), the playbook can now manage Dynamic DNS for you using [ddclient](https://ddclient.net/).

To learn more, follow our [Dynamic DNS docs page](docs/configuring-playbook-dynamic-dns.md).


# 2020-10-28

## (Compatibility Break) https://matrix.example.com/ now redirects to https://element.example.com/

Until now, we used to serve a static page coming from Synapse at `https://matrix.example.com/`. This page was not very useful to anyone.

Since `matrix.example.com` may be accessed by regular users in certain conditions, it's probably better to redirect them to a better place (e.g. to [Element Web](docs/configuring-playbook-client-element-web.md)).

If Element Web is installed (`matrix_client_element_enabled: true`, which it is by default), we now redirect people to it, instead of showing them a Synapse static page.

If you'd like to control where the redirect goes, use the `matrix_nginx_proxy_proxy_matrix_client_redirect_root_uri_to_domain` variable. To restore the old behavior of not redirecting anywhere and serving the Synapse static page, set it to an empty value (`matrix_nginx_proxy_proxy_matrix_client_redirect_root_uri_to_domain: ""`).


# 2020-10-26

## (Compatibility Break) /_synapse/admin is no longer publicly exposed by default

We used to expose the Synapse Admin APIs publicly (at `https://matrix.example.com/_synapse/admin`). These APIs require authentication with a valid access token, so it's not that big a deal to expose them.

However, following [official Synapse's reverse-proxying recommendations](https://github.com/element-hq/synapse/blob/master/docs/reverse_proxy.md#synapse-administration-endpoints), we're no longer exposing `/_synapse/admin` by default.

If you'd like to restore restore the old behavior and expose `/_synapse/admin` publicly, you can use the following configuration (in your `vars.yml`):

```yaml
matrix_nginx_proxy_proxy_matrix_client_api_forwarded_location_synapse_admin_api_enabled: true
```


# 2020-10-02

## Minimum Ansible version raised to v2.7.0

We were claiming to support [Ansible](https://www.ansible.com/) v2.5.2 and higher, but issues like [#662](https://github.com/spantaleev/matrix-docker-ansible-deploy/issues/662) demonstrate that we need at least v2.7.0.

If you've been using the playbook without getting any errors until now, you're probably on a version higher than that already (or you're not using the `matrix-ma1sd` and `matrix-client-element` roles).

Our [Ansible docs page](docs/ansible.md) contains information on how to run a more up-to-date version of Ansible.


# 2020-10-01

## Postgres 13 support

The playbook now installs [Postgres 13](https://www.postgresql.org/about/news/postgresql-13-released-2077/) by default.

If you have have an existing setup, it's likely running on an older Postgres version (9.x, 10.x, 11.x or 12.x). You can easily upgrade by following the [upgrading PostgreSQL guide](docs/maintenance-postgres.md#upgrading-postgresql).

# 2020-09-01

## matrix-registration support

The playbook can now help you set up [matrix-registration](https://github.com/ZerataX/matrix-registration) — an application that lets you keep your Matrix server's registration private, but still allow certain users (those having a unique registration link) to register by themselves.

See our [Setting up matrix-registration](docs/configuring-playbook-matrix-registration.md) documentation page to get started.


# 2020-08-21

## rust-synapse-compress-state support

The playbook can now help you use [rust-synapse-compress-state](https://github.com/matrix-org/rust-synapse-compress-state) to compress the state groups in your Synapse database.

See our [Compressing state with rust-synapse-compress-state](docs/maintenance-synapse.md#compressing-state-with-rust-synapse-compress-state) documentation page to get started.


# 2020-07-22

## Synapse Admin support

The playbook can now help you set up [synapse-admin](https://github.com/Awesome-Technologies/synapse-admin).

See our [Setting up Synapse Admin](docs/configuring-playbook-synapse-admin.md) documentation to get started.


# 2020-07-20

## matrix-reminder-bot support

The playbook can now help you set up [matrix-reminder-bot](https://github.com/anoadragon453/matrix-reminder-bot).

See our [Setting up matrix-reminder-bot](docs/configuring-playbook-bot-matrix-reminder-bot.md) documentation to get started.


# 2020-07-17

## (Compatibility Break) Riot is now Element

As per the official announcement, [Riot has been rebraned to Element](https://element.io/blog/welcome-to-element/).

The playbook follows suit. Existing installations have a few options for how to handle this.

See our [Migrating to Element Web](docs/configuring-playbook-riot-web.md#migrating-to-element) documentation page for more details.


# 2020-07-03

## Steam bridging support via mx-puppet-steam

Thanks to [Hugues Morisset](https://github.com/izissise)'s efforts, the playbook now supports bridging to [Steam](https://steamapp.com/) via the [mx-puppet-steam](https://codeberg.org/icewind/mx-puppet-steam) bridge. See our [Setting up MX Puppet Steam bridging](docs/configuring-playbook-bridge-mx-puppet-steam.md) documentation page for getting started.


# 2020-07-01

## Discord bridging support via mx-puppet-discord

Thanks to [Hugues Morisset](https://github.com/izissise)'s efforts, the playbook now supports bridging to [Discord](https://discordapp.com/) via the [mx-puppet-discord](https://github.com/Sorunome/mx-puppet-discord) bridge. See our [Setting up MX Puppet Discord bridging](docs/configuring-playbook-bridge-mx-puppet-discord.md) documentation page for getting started.

**Note**: this is a new Discord bridge. The playbook still retains Discord bridging via [matrix-appservice-discord](docs/configuring-playbook-bridge-appservice-discord.md). You're free too use the bridge that serves you better, or even both (for different users and use-cases).


# 2020-06-30

## Instagram and Twitter bridging support

Thanks to [Johanna Dorothea Reichmann](https://github.com/jdreichmann)'s efforts, the playbook now supports bridging to [Instagram](https://www.instagram.com/) via the [mx-puppet-instagram](https://github.com/Sorunome/mx-puppet-instagram) bridge. See our [Setting up MX Puppet Instagram bridging](docs/configuring-playbook-bridge-mx-puppet-instagram.md) documentation page for getting started.

Thanks to [Tulir Asokan](https://github.com/tulir)'s efforts, the playbook now supports bridging to [Twitter](https://twitter.com/) via the [mx-puppet-twitter](https://github.com/Sorunome/mx-puppet-twitter) bridge. See our [Setting up MX Puppet Twitter bridging](docs/configuring-playbook-bridge-mx-puppet-twitter.md) documentation page for getting started.


# 2020-06-28

## (Post Mortem / fixed Security Issue) Re-enabling User Directory search powered by the ma1sd Identity Server

User Directory search requests used to go to the ma1sd identity server by default, which queried its own stores and the Synapse database.

ma1sd's [security issue](https://github.com/ma1uta/ma1sd/issues/44) has been fixed in version `2.4.0`, with [this commit](ma1uta/ma1sd@2bb5a734d11662b06471113cf3d6b4cee5e33a85). `ma1sd 2.4.0` is now the default version for this playbook. For more information on what happened, please check the mentioned issue.

We are re-enabling user directory search with this update. Those who would like to keep it disabled can use this configuration: `matrix_nginx_proxy_proxy_matrix_user_directory_search_enabled: false`

As always, re-running the playbook is enough to get the updated bits.

# 2020-06-11

## SMS bridging requires db reset

The current version of [matrix-sms-bridge](https://github.com/benkuly/matrix-sms-bridge) needs you to delete the database to work as expected. Just remove `/matrix/matrix-sms-bridge/database/*`. It also adds a new required var `matrix_sms_bridge_default_region`.

To reuse your existing rooms, invite `@smsbot:yourServer` to the room or write a message. You are also able to use automated room creation with telephonenumers by writing `sms send -t 01749292923 "Hello World"` in a room with `@smsbot:yourServer`. See [the docs](https://github.com/benkuly/matrix-sms-bridge) for more information.

# 2020-06-05

## SMS bridging support

Thanks to [benkuly](https://github.com/benkuly)'s efforts, the playbook now supports bridging to SMS (with one telephone number only) via [matrix-sms-bridge](https://github.com/benkuly/matrix-sms-bridge).

See our [Setting up Matrix SMS bridging](docs/configuring-playbook-bridge-matrix-bridge-sms.md) documentation page for getting started.


# 2020-05-19

## (Compatibility Break / Security Issue) Disabling User Directory search powered by the ma1sd Identity Server

User Directory search requests used to go to the ma1sd identity server by default, which queried its own stores and the Synapse database.

ma1sd current has [a security issue](https://github.com/ma1uta/ma1sd/issues/44), which made it leak information about all users — including users created by bridges, etc.

Until the issue gets fixed, we're making User Directory search not go to ma1sd by default. You **need to re-run the playbook and restart services to apply this workaround**.

*If you insist on restoring the old behavior* (**which has a security issue!**), you *might* use this configuration: `matrix_nginx_proxy_proxy_matrix_user_directory_search_enabled: "{{ matrix_ma1sd_enabled }}"`


# 2020-04-28

## Newer IRC bridge (with potential breaking change)

This upgrades matrix-appservice-irc from 0.14.1 to 0.16.0. Upstream
made a change to how you define manual mappings. If you added a
`mapping` to your configuration, you will need to update it according
to the [upstream
instructions](https://github.com/matrix-org/matrix-appservice-irc/blob/master/CHANGELOG.md#0150-2020-02-05). If you did not include `mappings` in your configuration for IRC, no
change is necessary. `mappings` is not part of the default
configuration.


# 2020-04-23

## Slack bridging support

Thanks to [Rodrigo Belem](https://github.com/rbelem)'s efforts, the playbook now supports bridging to [Slack](https://slack.com) via the [mx-puppet-slack](https://github.com/Sorunome/mx-puppet-slack) bridge.

See our [Setting up MX Puppet Slack bridging](docs/configuring-playbook-bridge-mx-puppet-slack.md) documentation page for getting started.


# 2020-04-09

## Skype bridging support

Thanks to [Rodrigo Belem](https://github.com/rbelem)'s efforts, the playbook now supports bridging to [Skype](https://www.skype.com) via the [mx-puppet-skype](https://github.com/Sorunome/mx-puppet-skype) bridge.

See our [Setting up MX Puppet Skype bridging](docs/configuring-playbook-bridge-mx-puppet-skype.md) documentation page for getting started.


# 2020-04-05

## Private Jitsi support

The [Jitsi support](#jitsi-support) we had landed a few weeks ago was working well, but it was always open to the whole world.

Running such an open instance is not desirable to most people, so [teutat3s](https://github.com/teutat3s) has contributed support for making Jitsi use authentication.

To make your Jitsi server more private, see the [configure internal Jitsi authentication and guests mode](docs/configuring-playbook-jitsi.md#optional-configure-internal-jitsi-authentication-and-guests-mode) section in our Jitsi documentation.


# 2020-04-03

## (Potential Backward Compatibility Break) ma1sd replaces mxisd

Thanks to [Marcel Partap](https://github.com/eMPee584)'s efforts, the [mxisd](https://github.com/kamax-io/mxisd) identity server, which has been deprecated for a long time, has finally been replaced by [ma1sd](https://github.com/ma1uta/ma1sd), a compatible fork.

**If you're using the default playbook configuration**, you don't need to do anything — your mxisd installation will be replaced with ma1sd and all existing data will be migrated automatically the next time you run the playbook.

**If you're doing something more special** (defining custom `matrix_mxisd_*` variables), the playbook will ask you to rename them to `matrix_ma1sd_*`. You're also encouraged to test that ma1sd works well for such a more custom setup.


# 2020-03-29

## Archlinux support

Thanks to [Christian Lupus](https://github.com/christianlupus)'s efforts, the playbook now supports installing to an [Archlinux](https://www.archlinux.org/) server.


# 2020-03-24

## Jitsi support

The playbook can now (optionally) install the [Jitsi](https://jitsi.org/) video-conferencing platform and integrate it with [Riot](docs/configuring-playbook-riot-web.md).

See our [Jitsi documentation page](docs/configuring-playbook-jitsi.md) to get started.


# 2020-03-15

## Raspberry Pi support

Thanks to [Gergely Horváth](https://github.com/hooger)'s effort, the playbook supports installing to a Raspberry Pi server, for at least some of the services.

Since most ready-made container images do not support that architecture, we achieve this by building images locally on the device itself. See our [Self-building documentation page](docs/self-building.md) for how to get started.


# 2020-02-26

## Riot-web themes are here

The playbook now makes it easy to install custom riot-web themes.

To learn more, take a look at our [riot-web documentation on Themes](docs/configuring-playbook-riot-web.md#themes).


# 2020-02-24

## Customize the server name in Riot's login page

You can now customize the server name string that Riot-web displays in its login page.

These playbook variables, with these default values, have been added:

```yaml
matrix_riot_web_default_server_name: "{{ matrix_domain }}"
```

The login page previously said "Sign in to your Matrix account on matrix.example.org" (the homeserver's domain name). It will now say "Sign in … on example.org" (the server name) by default, or "Sign in … on Our Server" if you set the variable to "Our Server".

To support this, the config.json template is changed to use the configuration key `default_server_config` for setting the default HS/IS, and the new configuration key `server_name` is added in there.


# 2020-01-30

## Disabling TLSv1.1

To improve security, we've removed TLSv1.1 support from our default matrix-nginx-proxy configuration.

If you need to support old clients, you can re-enable it with the following configuration: `matrix_nginx_proxy_ssl_protocols: "TLSv1.1 TLSv1.2 TLSv1.3"`


# 2020-01-21

## Postgres collation changes (action required!)

By default, we've been using a UTF-8 collation for Postgres. This is known to cause Synapse some troubles (see the [relevant issue](https://github.com/matrix-org/synapse/issues/6722)) on systems that use [glibc](https://www.gnu.org/software/libc/). We run Postgres in an [Alpine Linux](https://alpinelinux.org/) container (which uses [musl](https://www.musl-libc.org/), and not glibc), so our users are likely not affected by the index corruption problem observed by others.

Still, we might become affected in the future. In any case, it's imminent that Synapse will complain about databases which do not use a C collation.

To avoid future problems, we recommend that you run the following command:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=upgrade-postgres --extra-vars='{"postgres_force_upgrade": true}'
```

It forces a [Postgres database upgrade](docs/maintenance-postgres.md#upgrading-postgresql), which would recreate your Postgres database using the proper (`C`) collation. If you are low on disk space, or run into trouble, refer to the Postgres database upgrade documentation page.


# 2020-01-14

## Added support for Appservice Webhooks

Thanks to a contribution from [Björn Marten](https://github.com/tripleawwy) from [netresearch](https://www.netresearch.de/), the playbook can now install and configure [matrix-appservice-webhooks](https://github.com/turt2live/matrix-appservice-webhooks) for you. This bridge provides support for Slack-compatible webhooks.

Learn more in [Setting up Appservice Webhooks bridging](docs/configuring-playbook-bridge-appservice-webhooks.md).


# 2020-01-12

## Added support for automatic Double Puppeting for all Mautrix bridges

Double Puppeting can now be easily enabled for all Mautrix bridges supported by the playbook (Facebook, Hangouts, Whatsapp, Telegram).

This is possible due to those bridges' integration with [matrix-synapse-shared-secret-auth](https://github.com/devture/matrix-synapse-shared-secret-auth) — yet another component that this playbook can install for you.

To get started, following the playbook's documentation for the bridge you'd like to configure.


# 2019-12-06

## Added support for an alternative method for using another webserver

We have added support for making `matrix-nginx-proxy` not being so invasive, so that it would be easier to [use your own webserver](docs/configuring-playbook-own-webserver.md).

The documentation has been updated with a **Method 2**, which might make "own webserver" setup easier in some cases (such as [reverse-proxying using Traefik](https://github.com/spantaleev/matrix-docker-ansible-deploy/issues/296)).

**Existing users** are not affected by this and **don't need to change anything**. The defaults are still the same (`matrix-nginx-proxy` obtaining SSL certificates and doing everything for you automatically).


# 2019-11-10

## Tightened security around room directory publishing

As per this [advisory blog post](https://matrix.org/blog/2019/11/09/avoiding-unwelcome-visitors-on-private-matrix-servers), we've decided to change the default publishing rules for the Matrix room directory.

Our general goal is to favor privacy and security when running personal (family & friends) and corporate homeservers. Both of these likely benefit from having a more secure default of **not showing the room directory without authentication** and **not publishing the room directory over federation**.

As with anything else, these new defaults can be overridden by changing the `matrix_synapse_allow_public_rooms_without_auth` and `matrix_synapse_allow_public_rooms_over_federation` variables, respectively.


# 2019-10-05

## Improved Postgres upgrading/importing

Postgres [upgrading](docs/maintenance-postgres.md#upgrading-postgresql) and [importing](docs/importing-postgres.md) have been improved to add support for multiple databases and roles.

Previously, the playbook would only take care of the `homeserver` database and `synapse` user. We now back up and restore all databases and users on the Postgres server.

For now, the playbook only uses that one database (`homeserver`) and that one single user (`synapse`), so it's all the same. However, in the future, additional components besides Synapse may also make use the Postgres database server. One such example is the [matrix-appservice-slack](https://github.com/matrix-org/matrix-appservice-slack) bridge, which strongly encourages use of Postgres in its v1.0 release. We are yet to upgrade to it.

Additionally, Postgres [upgrading](docs/maintenance-postgres.md#upgrading-postgresql) now uses gzipped dump files by default, to minimize disk space usage.


# 2019-10-04

## Postgres 12 support

The playbook now installs [Postgres 12](https://www.postgresql.org/about/news/1976/) by default.

If you have have an existing setup, it's likely running on an older Postgres version (9.x, 10.x or 11.x). You can easily upgrade by following the [upgrading PostgreSQL guide](docs/maintenance-postgres.md#upgrading-postgresql).


# 2019-10-03

## Synapse 1.4.0

Synapse 1.4.0 [is out](https://matrix.org/blog/2019/10/03/synapse-1-4-0-released) with lots of changes related to privacy.

Its new defaults (which we adopt as well) mean that certain old data will automatically get purged after a certain number of days. 1.4.0 automatically garbage collects redacted messages (defaults to 7 days) and removes unused IP and user agent information stored in the user_ips table (defaults to 30 days). If you'd like to preserve this data, we encourage you to look at the `redaction_retention_period` and `user_ips_max_age` options (controllable by the `matrix_synapse_redaction_retention_period` and `matrix_synapse_user_ips_max_age` playbook variables, respectively) before doing the upgrade. If you'd like to keep data indefinitely, set these variables to `null` (e.g. `matrix_synapse_redaction_retention_period: ~`).

From now on the `trusted_key_servers` setting for Synapse is configurable. It still defaults to `matrix.org` just like it always has, but in a more explicit way now. If you'd like to use another trusted key server, adjust the `matrix_synapse_trusted_key_servers` playbook variable.

Synapse 1.4.0 also changes lots of things related to identity server integration. Because Synapse will now by default be responsible for validating email addresses for user accounts, running without an identity server looks more feasible. We still [have concerns](https://github.com/spantaleev/matrix-docker-ansible-deploy/pull/275/files#r331104117) over disabling the identity server by default, so for now it remains enabled.


# 2019-09-09

## Synapse Simple Antispam support

There have been lots of invite-spam attacks lately and [Travis](https://github.com/t2bot) has created a Synapse module ([synapse-simple-antispam](https://github.com/t2bot/synapse-simple-antispam)) to let people protect themselves.

From now on, you can easily install and configure this spam checker module through the playbook.

Learn more in [Setting up Synapse Simple Antispam](docs/configuring-playbook-synapse-simple-antispam.md).


# 2019-08-25

## Extensible Riot-web configuration

Similarly to [Extensible Synapse configuration](#extensible-synapse-configuration) (below), Riot-web configuration is also extensible now.

From now on, you can extend/override Riot-web's configuration by making use of the `matrix_riot_web_configuration_extension_json` variable. This should be enough for most customization needs.

If you need even more power, you can now also take full control and override `matrix_riot_web_configuration_default` (or `matrix_riot_web_configuration`) directly.

Learn more in [Configuring Riot-web](docs/configuring-playbook-riot-web.md).


# 2019-08-22

## Extensible Synapse configuration

Previously, we had to create custom Ansible variables for each and every Synapse setting. This lead to too much effort (and configuration ugliness) to all of Synapse's settings, so naturally, not all features of Synapse could be controlled through the playbook.

From now on, you can extend/override the Synapse server's configuration by making use of the `matrix_synapse_configuration_extension_yaml` variable. This should be enough for most customization needs.

If you need even more power, you can now also take full control and override `matrix_synapse_configuration` (or `matrix_synapse_configuration_yaml`) directly.

Learn more here in [Configuring Synapse](docs/configuring-playbook-synapse.md).


# 2019-08-21

## Slack bridging support

Thanks to the [great work](https://github.com/spantaleev/matrix-docker-ansible-deploy/pull/205) of [kingoftheconnors](https://github.com/kingoftheconnors) and [Stuart Mumford (Cadair)](https://github.com/Cadair), the playbook now supports bridging to [Slack](https://slack.com) via the [appservice-slack](https://github.com/matrix-org/matrix-appservice-slack) bridge.

Additional details are available in [Setting up Appservice Slack bridging](docs/configuring-playbook-bridge-appservice-slack.md).

## Google Hangouts bridging support

Thanks to the [great work](https://github.com/spantaleev/matrix-docker-ansible-deploy/pull/251) of [Eduardo Beltrame (Munfred)](https://github.com/Munfred) and [Robbie D (microchipster)](https://github.com/microchipster), the playbook now supports bridging to [Google Hangouts](https://hangouts.google.com/) via the [mautrix-hangouts](https://mau.dev/tulir/mautrix-hangouts) bridge.

Additional details are available in [Setting up Mautrix Hangouts bridging](docs/configuring-playbook-bridge-mautrix-hangouts.md).


# 2019-08-05

## Email2Matrix support

Support for [Email2Matrix](https://github.com/devture/email2matrix) has been added.

It's an optional feature that you can enable via the playbook.

To learn more, see the [playbook's documentation on Email2Matrix](./docs/configuring-playbook-email2matrix.md).


# 2019-08-03

## Synapse logging level has been reduced to WARNING

After [some discussion in our support room](https://matrix.to/#/!PukFFdIcHgtaaHZflT:devture.com/$156476852524179TBeKy:matrix.org?via=devture.com&via=matrix.org&via=librem.one), we've decided to change the default logging level for Synapse from `INFO` to `WARNING`.

This greatly reduces the number of log messages that are being logged, leading to:

- much less disk space dedicated to Synapse and thus, logs kept for longer
- easier to find some important `WARNING`, `ERROR` and `CRITICAL` messages, as they're not longer buried in thousands of non-important `INFO` messages

If you'd like to track down an issue, you [can always increase the logging level as described here](./docs/maintenance-and-troubleshooting.md#increasing-synapse-logging).


# 2019-07-08

## Synapse Maintenance docs and synapse-janitor support are available

The playbook can now help you with Synapse's maintenance.

There's a new documentation page about [Synapse maintenance](./docs/maintenance-synapse.md) and another section on [Postgres vacuuming](./docs/maintenance-postgres.md#vacuuming-postgresql).

Among other things, if your Postgres database has grown significantly over time, you may wish to [ask the playbook to purge unused data with synapse-janitor](./docs/maintenance-synapse.md#purging-unused-data-with-synapse-janitor) for you.

## (BC Break) Rename run control variables

Some internal playbook control variables have been renamed.

This change **only affects people who run this playbook's roles from another playbook**. If you're using this playbook as-is, you're not affected and don't need to do anything.

The following variables have been renamed:

- from `run_import_postgres` to `run_postgres_import`
- from `run_import_sqlite_db` to `run_postgres_import_sqlite_db`
- from `run_upgrade_postgres` to `run_postgres_upgrade`
- from `run_import_media_store` to `run_synapse_import_media_store`
- from `run_register_user` to `run_synapse_register_user`
- from `run_update_user_password` to `run_synapse_update_user_password`


# 2019-07-04

## Synapse no longer logs to text files

Following what the official Synapse Docker image is doing ([#5565](https://github.com/matrix-org/synapse/pull/5565)) and what we've been doing for mostly everything installed by this playbook, **Synapse no longer logs to text files** (`/matrix/synapse/run/homeserver.log*`).

From now on, Synapse would only log to console, which goes to systemd's journald. To see Synapse's logs, execute: `journalctl -fu matrix-synapse`

Because of this, the following variables have become obsolete and were removed:

- `matrix_synapse_max_log_file_size_mb`
- `matrix_synapse_max_log_files_count`

To prevent confusion, it'd be better if you delete all old files manually after you've upgraded (`rm -f /matrix/synapse/run/homeserver.log*`).

Because Synapse is incredibly chatty when it comes to logging (here's [one such issue](https://github.com/matrix-org/synapse/issues/4751) describing the problem), if you're running an ancient distribution (like CentOS 7.0), be advised that systemd's journald default logging restrictions may not be high enough to capture all log messages generated by Synapse. This is especially true if you've got a busy (Synapse) server. We advise that you manually add `RateLimitInterval=0` and `RateLimitBurst=0` under `[Storage]` in the `/etc/systemd/journald.conf` file, followed by restarting the logging service (`systemctl restart systemd-journald`).


# 2019-06-27

## (BC Break) Discord bridge configuration is now entirely managed by the playbook

Until now, the `config.yaml` file for the [Discord bridge](docs/configuring-playbook-bridge-appservice-discord.md) was managed by the playbook, but the `registration.yaml` file was not.

From now on, the playbook will keep both configuration files sync for you.

This means that if you were making manual changes to the `/matrix/appservice-discord/discord-registration.yaml` configuration file, those would be lost the next time you run the playbook.

The bridge now stores configuration in a subdirectory (`/matrix/appservice-discord/config`).

Likewise, data is now also stored in a subdirectory (`/matrix/appservice-discord/data`). When you run the playbook with an existing database file (`/matrix/appservice-discord/discord.db`), the playbook will stop the bridge and relocate the database file to the `./data` directory. There's no data-loss involved. You'll need to restart the bridge manually though (`--tags=start`).

The main directory (`/matrix/appservice-discord`) may contain some leftover files (`user-store.db`, `room-store.db`, `config.yaml`, `discord-registration.yaml`, `invite_link`). These are no longer necessary and can be deleted manually.

We're now following the default sample configuration for the Discord bridge. If you need to override some values, define them in `matrix_appservice_discord_configuration_extension_yaml`.


# 2019-06-24

## (BC Break) WhatsApp bridge configuration is now entirely managed by the playbook

Until now, configuration files for the [WhatsApp bridge](docs/configuring-playbook-bridge-mautrix-whatsapp.md) were created by the playbook initially, but never modified later on.

From now on, the playbook will keep the configuration in sync for you.

This means that if you were making manual changes to the `/matrix/mautrix-whatsapp/config.yaml` or `/matrix/mautrix-whatsapp/registration.yaml` configuration files, those would be lost the next time you run the playbook.

The bridge now stores configuration in a subdirectory (`/matrix/mautrix-whatsapp/config`), so your old configuration remains in the base directory (`/matrix/mautrix-whatsapp`). You need to migrate any manual changes over to the new `matrix_mautrix_whatsapp_configuration_extension_yaml` variable, so that the playbook would apply them for you.

Likewise, data is now also stored in a subdirectory (`/matrix/mautrix-whatsapp/data`). When you run the playbook with an existing database file (`/matrix/mautrix-whatsapp/mautrix-whatsapp.db`), the playbook will stop the bridge and relocate the database file to the `./data` directory. There's no data-loss involved. You'll need to restart the bridge manually though (`--tags=start`).

We're now following the default configuration for the WhatsApp bridge.


# 2019-06-20

## (BC Break) IRC bridge configuration is now entirely managed by the playbook

Until now, configuration files for the [IRC bridge](docs/configuring-playbook-bridge-appservice-irc.md) were created by the playbook initially, but never modified later on.

From now on, the playbook will keep the configuration in sync for you.

This means that if you were making manual changes to the `/matrix/appservice-irc/config.yaml` or `/matrix/appservice-irc/registration.yaml` configuration files, those would be lost the next time you run the playbook.

The bridge now stores configuration in a subdirectory (`/matrix/appservice-irc/config`), so your old configuration remains in the base directory (`/matrix/appservice-irc`).

Previously, we asked people to configure bridged IRC servers by extending the bridge configuration (`matrix_appservice_irc_configuration_extension_yaml`). While this is still possible and will continue working forever, **we now recommend defining IRC servers in the easier to use `matrix_appservice_irc_ircService_servers` variable**. See [our IRC bridge documentation page](docs/configuring-playbook-bridge-appservice-irc.md) for an example.

If you decide to continue using `matrix_appservice_irc_configuration_extension_yaml`, you might be interested to know that `ircService.databaseUri` and a few other keys now have default values in the base configuration (`matrix_appservice_irc_configuration_yaml`). You may wish to stop redefining those keys, unless you really intend to override them. You most likely only need to override `ircService.servers`.

Bridge data (`passkey.pem` and database files) is now also stored in a subdirectory (`/matrix/appservice-irc/data`). When you run the playbook with an existing `/matrix/appservice-irc/passkey.pem` file, the playbook will stop the bridge and relocate the passkey and database files (`rooms.db` and `users.db`) to the `./data` directory. There's no data-loss involved. You'll need to restart the bridge manually though (`--tags=start`).


# 2019-06-15

## (BC Break) Telegram bridge configuration is now entirely managed by the playbook

Until now, configuration files for the [Telegram bridge](docs/configuring-playbook-bridge-mautrix-telegram.md) were created by the playbook initially, but never modified later on.

From now on, the playbook will keep the configuration in sync for you.

This means that if you were making manual changes to the `/matrix/mautrix-telegram/config.yaml` or `/matrix/mautrix-telegram/registration.yaml` configuration files, those would be lost the next time you run the playbook.

The bridge now stores configuration in a subdirectory (`/matrix/mautrix-telegram/config`), so your old configuration remains in the base directory (`/matrix/mautrix-telegram`). You need to migrate any manual changes over to the new `matrix_mautrix_telegram_configuration_extension_yaml` variable, so that the playbook would apply them for you.

Likewise, data is now also stored in a subdirectory (`/matrix/mautrix-telegram/data`). When you run the playbook with an existing database file (`/matrix/mautrix-telegram/mautrix-telegram.db`), the playbook will stop the bridge and relocate the database file to the `./data` directory. There's no data-loss involved. You'll need to restart the bridge manually though (`--tags=start`).

Also, we're now following the default configuration for the Telegram bridge, so some default configuration values are different:

- `edits_as_replies` (used to be `false`, now `true`) — previously replies were not sent over to Matrix at all; ow they are sent over as a reply to the original message
- `inline_images` (used to be `true`, now `false`) — this has to do with captioned images. Inline-image (included caption) are said to exhibit troubles on Riot iOS. When `false`, the caption arrives on the Matrix side as a separate message.
- `authless_portals` (used to be `false`, now `true`) — creating portals from the Telegram side is now possible
- `whitelist_group_admins` (used to be `false`, now `true`) — allows Telegram group admins to use the bot commands

If the new values are not to your liking, use `matrix_mautrix_telegram_configuration_extension_yaml` to specify an override (refer to `matrix_mautrix_telegram_configuration_yaml` to figure out which variable goes where).


# 2019-06-12

## Synapse v1.0

With [Synapse v1.0 now available](https://matrix.org/blog/2019/06/11/introducing-matrix-1-0-and-the-matrix-org-foundation) and most people being on at least Synapse v0.99, it's time to remove the `_matrix._tcp` DNS SRV record that we've been keeping for compatibility with old Synapse versions (<= 0.34).

According to the [Server Discovery specification](https://matrix.org/docs/spec/server_server/r0.1.2.html#server-discovery), it's no harm to keep the DNS SRV record. But since it's not necessary for federating with the larger Matrix network anymore, you should be safe to get rid of it.

**Note**: don't confuse the `_matrix._tcp` and `_matrix-identity._tcp` DNS SRV records. The latter, **must not** be removed.

For completeness, we must say that using a `_matrix._tcp` [SRV record for Server Delegation](docs/howto-server-delegation.md#server-delegation-via-a-dns-srv-record-advanced) is still valid and useful for certain deployments. It's just that our guide recommends the [`/.well-known/matrix/server` Server Delegation method](docs/howto-server-delegation.md#server-delegation-via-a-well-known-file), due to its easier implementation when using this playbook.

Besides this optional/non-urgent DNS change, assuming you're already on Synapse v0.99, upgrading to Synapse v1.0 should be as simple as [re-running the playbook](docs/maintenance-upgrading-services.md).


# 2019-06-07

## (BC Break) Facebook bridge configuration is now entirely managed by the playbook

Until now, configuration files for the [Facebook bridge](docs/configuring-playbook-bridge-mautrix-facebook.md) were created by the playbook initially, but never modified later on.

From now on, the playbook will keep the configuration in sync for you.

This means that if you were making manual changes to the `/matrix/mautrix-facebook/config.yaml` or `/matrix/mautrix-facebook/registration.yaml` configuration files, those would be lost the next time you run the playbook.

The bridge now stores configuration in a subdirectory (`/matrix/mautrix-facebook/config`), so your old configuration remains in the base directory (`/matrix/mautrix-facebook`). You need to migrate any manual changes over to the new `matrix_mautrix_facebook_configuration_extension_yaml` variable, so that the playbook would apply them for you.

Likewise, data is now also stored in a subdirectory (`/matrix/mautrix-facebook/data`). When you run the playbook with an existing database file (`/matrix/mautrix-facebook/mautrix-facebook.db`), the playbook will stop the bridge and relocate the database file to the `./data` directory. There's no data-loss involved. You'll need to restart the bridge manually though (`--tags=start`).


# 2019-05-25

## Support for exposing container ports publicly (not just to the host)

Until now, various roles supported a `matrix_*_expose_port` variable, which would expose their container's port to the host. This was mostly useful for reverse-proxying manually (in case `matrix-nginx-proxy` was disabled). It could also be used for installing some playbook services (e.g. bridges, etc.) and wiring them to a separate (manual) Matrix setup.

`matrix_*_expose_port` variables were not granular enough — sometimes they would expose one port, other times multiple. They also didn't provide control over **where** to expose (to which port number and to which network interface), because they would usually hardcode something like `127.0.0.1:8080`.

All such variables have been superseded by a better (more flexible) way to do it.

**Most** people (including those not using `matrix-nginx-proxy`), **don't need** to bother with this.

Porting examples follow for people having more customized setups:

- **from** `matrix_synapse_container_expose_client_api_port: true` **to** `matrix_synapse_container_client_api_host_bind_port: '127.0.0.1:8008'`

- **from** `matrix_synapse_container_expose_federation_api_port: true` **to** `matrix_synapse_container_federation_api_plain_host_bind_port: '127.0.0.1:8048'` and possibly `matrix_synapse_container_federation_api_tls_host_bind_port: '8448'`

- **from** `matrix_synapse_container_expose_metrics_port: true` **to** `matrix_synapse_container_metrics_api_host_bind_port: '127.0.0.1:9100'`

- **from** `matrix_riot_web_container_expose_port: true` **to** `matrix_riot_web_container_http_host_bind_port: '127.0.0.1:8765'`

- **from** `matrix_mxisd_container_expose_port: true` **to** `matrix_mxisd_container_http_host_bind_port: '127.0.0.1:8090'`

- **from** `matrix_dimension_container_expose_port: true` **to** `matrix_dimension_container_http_host_bind_port: '127.0.0.1:8184'`

- **from** `matrix_corporal_container_expose_ports: true` **to** `matrix_corporal_container_http_gateway_host_bind_port: '127.0.0.1:41080'` and possibly `matrix_corporal_container_http_api_host_bind_port: '127.0.0.1:41081'`

- **from** `matrix_appservice_irc_container_expose_client_server_api_port: true` **to** `matrix_appservice_irc_container_http_host_bind_port: '127.0.0.1:9999'`

- **from** `matrix_appservice_discord_container_expose_client_server_api_port: true` **to** `matrix_appservice_discord_container_http_host_bind_port: '127.0.0.1:9005'`

As always, if you forget to remove usage of some outdated variable, the playbook will warn you.


# 2019-05-23

## (BC Break) Ansible 2.8 compatibility

Thanks to [@danbob](https://github.com/danbob), the playbook now [supports the new Ansible 2.8](https://github.com/spantaleev/matrix-docker-ansible-deploy/pull/187).

A manual change is required to the `inventory/hosts` file, changing the group name from `matrix-servers` to `matrix_servers` (dash to underscore).

To avoid doing it manually, run this:
- Linux: `sed -i 's/matrix-servers/matrix_servers/g' inventory/hosts`
- Mac: `sed -i '' 's/matrix-servers/matrix_servers/g' inventory/hosts`


# 2019-05-21

## Synapse no longer required

The playbook no longer insists on installing [Synapse](https://github.com/element-hq/synapse) via the `matrix-synapse` role.

If you would prefer to install Synapse another way and just use the playbook to install other services, it should be possible (`matrix_synapse_enabled: false`).

Note that it won't necessarily be the best experience, since the playbook wires things to Synapse by default. If you're using your own Synapse instance (especially one not running in a container), you may have to override many variables to point them to the correct place.

Having Synapse not be a required component potentially opens the door for installing alternative Matrix homeservers.

## Bridges are now separate from the Synapse role

Bridges are no longer part of the `matrix-synapse` role. Each bridge now lives in its own separate role (`roles/custom/matrix-bridge-*`).

These bridge roles are independent of the `matrix-synapse` role, so it should be possible to use them with a Synapse instance installed another way (not through the playbook).

## Renaming inconsistently-named Synapse variables

For better consistency, the following variables have been renamed:

- `matrix_enable_room_list_search` was renamed to `matrix_synapse_enable_room_list_search`
- `matrix_alias_creation_rules` was renamed to `matrix_synapse_alias_creation_rules`
- `matrix_nginx_proxy_matrix_room_list_publication_rulesdata_path` was renamed to `matrix_synapse_room_list_publication_rules`


# 2019-05-09

Besides a myriad of bug fixes and minor improvements, here are the more notable (bigger) features we can announce today.

## Mautrix Facebook/Messenger bridging support

The playbook now supports bridging with [Facebook](https://www.facebook.com/) by installing the [mautrix-facebook](https://github.com/tulir/mautrix-facebook) bridge. This playbook functionality is available thanks to [@izissise](https://github.com/izissise).

Additional details are available in [Setting up Mautrix Facebook bridging](docs/configuring-playbook-bridge-mautrix-facebook.md).

## mxisd Registration feature integration

The playbook can now help you integrate with mxisd's [Registration](https://github.com/kamax-matrix/mxisd/blob/master/docs/features/registration.md) feature.

Learn more in [mxisd-controlled Registration](docs/configuring-playbook-mxisd.md#mxisd-controlled-registration).


# 2019-04-16

## Caddy webserver examples

If you prefer using the [Caddy](https://caddyserver.com/) webserver instead of our own integrated nginx, we now have examples for it in the [`examples/caddy`](examples/caddy) directory

# 2019-04-10

## Goofys support for other S3-compatible object stores

Until now, you could optionally host Synapse's media repository on Amazon S3, but we now also support [using other S3-compatible object stores](docs/configuring-playbook-s3.md),


# 2019-04-03

## Ansible >= 2.5 is required

Due to recent playbook improvements and the fact that the world keeps turning, we're bumping the [version requirement for Ansible](docs/ansible.md#supported-ansible-versions) (2.4 -> 2.5).

We've also started building our own Docker image of Ansible ([devture/ansible](https://hub.docker.com/r/devture/ansible/)), which is useful for people who can't upgrade their local Ansible installation (see [Using Ansible via Docker](docs/ansible.md#using-ansible-via-docker)).


# 2019-03-19

## TLS support for coturn

We've added TLS support to the coturn TURN server installed by the playbook by default. The certificates from the Matrix domain will be used for the coturn server.

This feature is enabled by default for new installations. To make use of TLS support for your existing Matrix server's coturn, make sure to rebuild both coturn and Synapse:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-coturn,setup-synapse,start
```

People who have an extra firewall (besides the iptables firewall, which Docker manages automatically), will need to open these additional firewall ports: `5349/tcp` (TURN over TCP) and `5349/udp` (TURN over UDP).

People who build their own custom playbook from our roles should be aware that:

- the `matrix-coturn` role and actually starting coturn (e.g. `--tags=start`), requires that certificates are already put in place. For this reason, it's usually a good idea to have the `matrix-coturn` role execute after `matrix-nginx-proxy` (which retrieves the certificates).

- there are a few variables that can help you enable TLS support for coturn. See the `matrix-coturn` section in [group_vars/matrix-servers](./group_vars/matrix-servers).


# 2019-03-12

## matrix-nginx-proxy support for serving the base domain

If you don't have a dedicated server for your base domain and want to set up [Server Delegation via a well-known file](docs/howto-server-delegation.md#server-delegation-via-a-well-known-file), the playbook has got you covered now.

It's now possible for the playbook to obtain an SSL certificate and serve the necessary files for Matrix Server Delegation on your base domain. Take a look at the new [Serving the base domain](docs/configuring-playbook-base-domain-serving.md) documentation page.

## (BC break) matrix-nginx-proxy data variable renamed

`matrix_nginx_proxy_data_path` was renamed to `matrix_nginx_proxy_base_path`.

There's a new `matrix_nginx_proxy_data_path` variable, which has a different use-purpose now (it's a subdirectory of `matrix_nginx_proxy_base_path` and is meant for storing various data files).


# 2019-03-10

## Dimension integration manager support

Thanks to [NullIsNot0](https://github.com/NullIsNot0), the playbook can now (optionally) install the [Dimension](https://dimension.t2bot.io/) integration manager. To learn more, see the [Setting up Dimension](docs/configuring-playbook-dimension.md) documentation page.


# 2019-03-07

## Ability to customize mxisd's email templates

Thanks to [Sylvia van Os](https://github.com/TheLastProject), mxisd's email templates can now be customized easily. To learn more, see the [Customizing email templates](docs/configuring-playbook-mxisd.md#customizing-email-templates) documentation page.


# 2019-03-05

## Discord bridging support

[@Lionstiger](https://github.com/Lionstiger) has done some great work adding Discord bridging support via [matrix-appservice-discord](https://github.com/matrix-org/matrix-appservice-discord). To learn more, see the [Setting up Appservice Discord bridging](docs/configuring-playbook-bridge-appservice-discord.md) documentation page.


# 2019-02-19

## Renaming variables

The following playbook variables were renamed:

- from `host_specific_hostname_identity` to `matrix_domain`
- from `hostname_identity` to `matrix_domain`
- from `hostname_matrix` to `matrix_server_fqn_matrix`
- from `hostname_riot` to `matrix_server_fqn_riot`
- from `host_specific_matrix_ssl_lets_encrypt_support_email` to `matrix_ssl_lets_encrypt_support_email`

Doing that, we've simplified things, made names less confusing (hopefully) and moved all variable names under the `matrix_` prefix.


# 2019-02-16

## Riot v1.0.1 support

You can now use the brand new and redesigned Riot.

The new version no longer has a homepage by default, so we've also removed the custom homepage that we've been installing.

However, we still provide you with hooks to install your own `home.html` file by specifying the `matrix_riot_web_embedded_pages_home_path` variable (used to be called `matrix_riot_web_homepage_template` before).


# 2019-02-14

## Synapse v0.99.1

As we're moving toward Synapse v1.0, things are beginning to stabilize. Upgrading from v0.99.0 to v0.99.1 should be painless.

If you've been overriding the default configuration so that you can terminate TLS at the Synapse side (`matrix_synapse_no_tls: false`), you'll now have to replace this custom configuration with `matrix_synapse_tls_federation_listener_enabled: true`. The `matrix_synapse_no_tls` variable is no more.


# 2019-02-06

## Synapse v0.99 support and preparation for Synapse v1.0

Matrix is undergoing a lot of changes as it matures towards Synapse v1.0. The first step is the Synapse v0.99 transitional release, which this playbook now supports.

If you've been using this playbook successfully until now, you'd be aware that we've been doing [Server Delegation](docs/howto-server-delegation.md) using a `_matrix._tcp` DNS SRV record (as per [Configuring DNS](docs/configuring-dns.md)).

Due to changes related to certificate file requirements that will affect us at Synapse v1.0, we'll have to stop using a **`_matrix._tcp` DNS SRV record in the future** (when Synapse goes to v1.0 — around 5th of March 2019). We **still need to keep the SRV record for now**, for backward compatibility with older Synapse versions (lower than v0.99).

**What you need to do now** is make use of this transitional Synapse v0.99 release to **prepare your federation settings for the future**. You have 2 choices to prepare yourself for compatibility with the future Synapse v1.0:

- (recommended) set up [Server Delegation via a well-known file](docs/howto-server-delegation.md#server-delegation-via-a-well-known-file), unless you are affected by the [Downsides of well-known-based Server Delegation](docs/howto-server-delegation.md#downsides-of-well-known-based-server-delegation). If you had previously set up the well-known `client` file, depending on how you've done it, it may be that there is nothing new required of you (besides [upgrading](docs/maintenance-upgrading-services.md)). After upgrading, you can [run a self-check](docs/maintenance-and-troubleshooting.md#how-to-check-if-services-work), which will tell you if you need to do anything extra with regard to setting up [Server Delegation via a well-known file](docs/howto-server-delegation.md#server-delegation-via-a-well-known-file). After some time, when most people have upgraded to Synapse v0.99 and older releases have disappeared, be prepared to drop your `_matrix._tcp` SRV record.

- (more advanced) if the [Downsides of well-known-based Server Delegation](docs/howto-server-delegation.md#downsides-of-well-known-based-server-delegation) are not to your liking, **as an alternative**, you can set up [Server Delegation via a DNS SRV record](docs/howto-server-delegation.md#server-delegation-via-a-dns-srv-record-advanced). In such a case, you get to keep using your existing `_matrix._tcp` DNS SRV record forever and need to NOT set up a `/.well-known/matrix/server` file. Don't forget that you need to do certificate changes though. Follow the guide at [Server Delegation via a DNS SRV record](docs/howto-server-delegation.md#server-delegation-via-a-dns-srv-record-advanced).


# 2019-02-01

## TLS v1.3 support

Now that the [nginx Docker image](https://hub.docker.com/_/nginx) has [added support for TLS v1.3](https://github.com/nginxinc/docker-nginx/issues/190), we have enabled that protocol by default.

When using:

- the **integrated nginx server**: TLS v1.3 support might not kick in immediately, because the nginx version hasn't been bumped and you may have an older build of the nginx Docker image (currently `nginx:1.15.8-alpine`). Typically, we do not re-pull images that you already have. When the nginx version gets bumped in the future, everyone will get the update. Until then, you could manually force-pull the rebuilt Docker image by running this on the server: `docker pull nginx:1.15.8-alpine`.

- **your own external nginx server**: if your external nginx server is too old, the new configuration we generate for you in `/matrix/nginx-proxy/conf.d/` might not work anymore, because it mentions `TLSv1.3` and your nginx version might not support that. You can adjust the SSL protocol list by overriding the `matrix_nginx_proxy_ssl_protocols` variable. Learn more in the documentation page for [Using your own webserver, instead of this playbook's nginx proxy](docs/configuring-playbook-own-webserver.md)

- **another web server**: you don't need to do anything to accommodate this change


# 2019-01-31

## IRC bridging support

[Devon Maloney (@Plailect)](https://github.com/Plailect) has done some great work bringing IRC bridging support via [matrix-appservice-irc](https://github.com/TeDomum/matrix-appservice-irc). To learn more, see the [Setting up Appservice IRC bridging](docs/configuring-playbook-bridge-appservice-irc.md) documentation page.


# 2019-01-29

## Running container processes as non-root, without capabilities and read-only

To improve security, this playbook no longer starts container processes as the `root` user. Most containers were dropping privileges anyway, but we were trusting them with `root` privileges until they would do that. Not anymore — container processes now start as a non-root user (usually `matrix`) from the get-go.

For additional security, various capabilities are also dropped (see [why it's important](https://github.com/projectatomic/atomic-site/issues/203)) for all containers.

Additionally, most containers now use a read-only filesystem (see [why it's important](https://www.projectatomic.io/blog/2015/12/making-docker-images-write-only-in-production/)). Containers are given write access only to the directories they need to write to.

A minor breaking change is the `matrix_nginx_proxy_proxy_matrix_client_api_client_max_body_size` variable having being renamed to `matrix_nginx_proxy_proxy_matrix_client_api_client_max_body_size_mb` (note the `_mb` suffix). The new variable expects a number value (e.g. `25M` -> `25`). If you weren't customizing this variable, this wouldn't affect you.

## matrix-mailer is now based on Exim, not Postfix

While we would have preferred to stay with [Postfix](http://www.postfix.org/), we found out that it cannot run as a non-root user. We've had to replace it with [Exim](https://www.exim.org/) (via the [devture/exim-relay](https://hub.docker.com/r/devture/exim-relay) container image).

The internal `matrix-mailer` service (running in a container) now listens on port `8025` (used to be `587` before). The playbook will update your Synapse and mxisd email settings to match (`matrix-mailer:587` -> `matrix-mailer:8025`).

Using the [devture/exim-relay](https://hub.docker.com/r/devture/exim-relay) container image instead of [panubo/postfix](https://hub.docker.com/r/panubo/postfix/) also gives us a nice disk usage reduction (~200MB -> 8MB).


# 2019-01-17

## (BC Break) Making the playbook's roles more independent of one another

The following change **affects people running a more non-standard setup** — external Postgres or using our roles in their own other playbook.
**Most users don't need to do anything**, besides becoming aware of the new glue variables file [`group_vars/matrix-servers`](group_vars/matrix-servers).

Because people like using the playbook's components independently (outside of this playbook) and because it's much better for maintainability, we've continued working on separating them. Still, we'd like to offer a turnkey solution for running a fully-featured Matrix server, so this playbook remains important for wiring up the various components.

With the new changes, **all roles are now only dependent on the minimal `matrix-base` role**. They are no longer dependent among themselves.

In addition, the following components can now be completely disabled (for those who want/need to):
- `matrix-coturn` by using `matrix_coturn_enabled: false`
- `matrix-mailer` by using `matrix_mailer_enabled: false`
- `matrix-postgres` by using `matrix_postgres_enabled: false`

The following changes had to be done:

- glue variables had to be introduced to the playbook, so it can wire together the various components. Those glue vars are stored in the [`group_vars/matrix-servers`](group_vars/matrix-servers) file. When overriding variables for a given component (role), you need to be aware of both the role defaults (`role/ROLE/defaults/main.yml`) and the role's corresponding section in the [`group_vars/matrix-servers`](group_vars/matrix-servers) file.

- `matrix_postgres_use_external` has been superseded by the more consistently named `matrix_postgres_enabled` variable and a few other `matrix_synapse_database_` variables. See the [Using an external PostgreSQL server (optional)](docs/configuring-playbook-external-postgres.md) documentation page for an up-to-date replacement.

- Postgres tools (`matrix-postgres-cli` and `matrix-make-user-admin`) are no longer installed if you're not enabling the `matrix-postgres` role (`matrix_postgres_enabled: false`)

- roles, being more independent now, are more minimal and do not do so much magic for you. People that are building their own playbook using our roles will definitely need to take a look at the [`group_vars/matrix-servers`](group_vars/matrix-servers) file and adapt their playbooks with the same (or similar) wiring logic.


# 2019-01-16

## Splitting the playbook into multiple roles

For better maintainability, the playbook logic (which all used to reside in a single `matrix-server` role)
has been split out into a number of different roles: `matrix-synapse`, `matrix-postgres`, `matrix-riot-web`, `matrix-mxisd`, etc. (see the `roles/` directory).

To keep the filesystem more consistent with this separation, the **Postgres data had to be relocated**.

The default value of `matrix_postgres_data_path` was changed from `/matrix/postgres` to `/matrix/postgres/data`. The `/matrix/postgres` directory is what we consider a base path now (new variable `matrix_postgres_base_path`). **Your Postgres data files will automatically be relocated by the playbook** (`/matrix/postgres/*` -> `/matrix/postgres/data/`) when you run with `--tags=setup-all` (or `--tags=setup-postgres`). While this shouldn't cause data-loss, **it's better if you do a Postgres backup just in case**. You'd need to restart all services after this migration (`--tags=start`).


# 2019-01-11

## (BC Break) mxisd configuration changes

To be more flexible and to support the upcoming [mxisd](https://github.com/kamax-io/mxisd) 1.3.0 (when it gets released),
we've had to redo how mxisd gets configured.

The following variables are no longer supported by this playbook:

- `matrix_mxisd_ldap_enabled`
- `matrix_mxisd_ldap_connection_host`
- `matrix_mxisd_ldap_connection_tls`
- `matrix_mxisd_ldap_connection_port`
- `matrix_mxisd_ldap_connection_baseDn`
- `matrix_mxisd_ldap_connection_baseDns`
- `matrix_mxisd_ldap_connection_bindDn`
- `matrix_mxisd_ldap_connection_bindDn`
- `matrix_mxisd_ldap_connection_bindPassword`
- `matrix_mxisd_ldap_filter`
- `matrix_mxisd_ldap_attribute_uid_type`
- `matrix_mxisd_ldap_attribute_uid_value`
- `matrix_mxisd_ldap_connection_bindPassword`
- `matrix_mxisd_ldap_attribute_name`
- `matrix_mxisd_ldap_attribute_threepid_email`
- `matrix_mxisd_ldap_attribute_threepid_msisdn`
- `matrix_mxisd_ldap_identity_filter`
- `matrix_mxisd_ldap_identity_medium`
- `matrix_mxisd_ldap_auth_filter`
- `matrix_mxisd_ldap_directory_filter`
- `matrix_mxisd_template_config`

You are encouraged to use the `matrix_mxisd_configuration_extension_yaml` variable to define your own mxisd configuration additions and overrides. Refer to the [default variables file](roles/custom/matrix-mxisd/defaults/main.yml) for more information.

This new way of configuring mxisd is beneficial because:

- it lets us support all mxisd configuration options, as the playbook simply forwards them to mxisd without needing to care or understand them
- it lets you upgrade to newer mxisd versions and make use of their features, without us having to add support for them explicitly


# 2019-01-08

## (BC Break) Cronjob schedule no longer configurable

Due to the way we manage cronjobs now, you can no longer configure the schedule they're invoked at.

If you were previously using `matrix_ssl_lets_encrypt_renew_cron_time_definition` or `matrix_nginx_proxy_reload_cron_time_definition`
to set a custom schedule, you should note that these variables don't affect anything anymore.

If you miss this functionality, please [open an Issue](https://github.com/spantaleev/matrix-docker-ansible-deploy/issues/new) and let us know about your use case!


# 2018-12-23

## (BC Break) More SSL certificate retrieval methods

The playbook now lets you decide between 3 different SSL certificate retrieval methods:
- (default) obtaining free SSL certificates from Let's Encrypt
- generating self-signed SSL certificates
- managing SSL certificates manually

Learn more in [Adjusting SSL certificate retrieval](docs/configuring-playbook-ssl-certificates.md).

For people who use Let's Encrypt (mostly everyone, since it's the default), you'll also have to rename a variable in your configuration:

- before: `host_specific_matrix_ssl_support_email`
- after: `host_specific_matrix_ssl_lets_encrypt_support_email`

## (BC Break) mxisd upgrade with multiple base DN support

mxisd has bee upgraded to [version 1.2.2](https://github.com/kamax-matrix/mxisd/releases/tag/v1.2.2), which supports [multiple base DNs](https://github.com/kamax-matrix/mxisd/blob/v1.2.2/docs/stores/ldap.md#base).

If you were configuring this playbook's `matrix_mxisd_ldap_connection_baseDn` variable until now (a string containing a single base DN), you'll need to change to configuring the `matrix_mxisd_ldap_connection_baseDns` variable (an array containing multiple base DNs).

Example change:

- before: `matrix_mxisd_ldap_connection_baseDn: OU=Users,DC=example,DC=org`
- after: `matrix_mxisd_ldap_connection_baseDns: ['OU=Users,DC=example,DC=org']`


# 2018-12-21

## Synapse 0.34.0 and Python 3

Synapse has been upgraded to 0.34.0 and now uses Python 3. Based on feedback from others, running Synapse on Python 3 is supposed to decrease memory usage significantly (~2x).


# 2018-12-12

## Riot homepage customization

You can now customize some parts of the Riot homepage (or even completely replace it with your own custom page). See the `matrix_riot_web_homepage_` variables in `roles/custom/matrix-riot-web/defaults/main.yml`.


# 2018-12-04

## mxisd extensibility

The [LDAP identity store for mxisd](https://github.com/kamax-matrix/mxisd/blob/master/docs/stores/ldap.md) can now be configured easily using playbook variables (see the `matrix_mxisd_ldap_` variables in `roles/custom/matrix-server/defaults/main.yml`).


# 2018-11-28

## More scripts

* matrix-remove-all allows to uninstall everything with a single command
* matrix-make-user-admin allows to upgrade a user's privileges

## LDAP auth support via matrix-synapse-ldap3

The playbook can now install and configure [LDAP auth support](https://github.com/matrix-org/matrix-synapse-ldap3) for you.

Additional details are available in [Setting up the LDAP authentication password provider module](docs/configuring-playbook-ldap-auth.md).


# 2018-11-23

## Support for controlling public registration and room auto-join

The playbook now lets you enable public registration for users (controlled via `matrix_synapse_enable_registration`). By default, public registration is forbidden.

You can also make people automatically get auto-joined to rooms (controlled via `matrix_synapse_auto_join_rooms`).

## Support for changing the welcome user ID (welcome bot)

By default, `@riot-bot:matrix.org` is used to welcome newly registered users. This can be changed to something else (or disabled) via the new `matrix_riot_web_welcome_user_id` variable.


# 2018-11-14

## Ability to set Synapse log levels

The playbook now allows you to set the log levels used by Synapse. The default logging levels remain the same.

You can now override following variables with any of the supported log levels listed here: https://docs.python.org/3/library/logging.html#logging-levels

```yaml
matrix_synapse_log_level: "INFO"
matrix_synapse_storage_sql_log_level: "INFO"
matrix_synapse_root_log_level: "INFO"
```


# 2018-11-03

## Customize parts of Riot's config

You can now customize some parts of Riot's `config.json`. These playbook variables, with these default values, have been added:

```yaml
matrix_riot_web_disable_custom_urls: true
matrix_riot_web_disable_guests: true
matrix_riot_web_integrations_ui_url: "https://scalar.vector.im/"
matrix_riot_web_integrations_rest_url: "https://scalar.vector.im/api"
matrix_riot_web_integrations_widgets_urls: "https://scalar.vector.im/api"
matrix_riot_web_integrations_jitsi_widget_url: "https://scalar.vector.im/api/widgets/jitsi.html"
```

This now allows you use a custom integration manager like [Dimension](https://dimension.t2bot.io). For example, if you wish to use the Dimension instance hosted at dimension.t2bot.io, you can set the following in your vars.yml file:

```yaml
matrix_riot_web_integrations_ui_url: "https://dimension.t2bot.io/riot"
matrix_riot_web_integrations_rest_url: "https://dimension.t2bot.io/api/v1/scalar"
matrix_riot_web_integrations_widgets_urls: "https://dimension.t2bot.io/widgets"
matrix_riot_web_integrations_jitsi_widget_url: "https://dimension.t2bot.io/widgets/jitsi"
```

## SSL protocols used to serve Riot and Synapse

There's now a new `matrix_nginx_proxy_ssl_protocols` playbook variable, which controls the SSL protocols used to serve Riot and Synapse. Its default value is `TLSv1.1 TLSv1.2`. This playbook previously used `TLSv1 TLSv1.1 TLSv1.2` to serve Riot and Synapse.

You may wish to re-enable TLSv1 if you need to access Riot in older browsers.

Note: Currently the dockerized nginx doesn't support TLSv1.3. See https://github.com/nginxinc/docker-nginx/issues/190 for more details.


# 2018-11-01

## Postgres 11 support

The playbook now installs [Postgres 11](https://www.postgresql.org/about/news/1894/) by default.

If you have have an existing setup, it's likely running on an older Postgres version (9.x or 10.x). You can easily upgrade by following the [upgrading PostgreSQL guide](docs/maintenance-postgres.md#upgrading-postgresql).

## (BC Break) Renaming playbook variables

Due to the large amount of features added to this playbook lately, to keep things manageable we've had to reorganize its configuration variables a bit.

The following playbook variables were renamed:

- from `matrix_docker_image_mxisd` to `matrix_mxisd_docker_image`
- from `matrix_docker_image_mautrix_telegram` to `matrix_mautrix_telegram_docker_image`
- from `matrix_docker_image_mautrix_whatsapp` to `matrix_mautrix_whatsapp_docker_image`
- from `matrix_docker_image_mailer` to `matrix_mailer_docker_image`
- from `matrix_docker_image_coturn` to `matrix_coturn_docker_image`
- from `matrix_docker_image_goofys` to `matrix_s3_goofys_docker_image`
- from `matrix_docker_image_riot` to `matrix_riot_web_docker_image`
- from `matrix_docker_image_nginx` to `matrix_nginx_proxy_docker_image`
- from `matrix_docker_image_synapse` to `matrix_synapse_docker_image`
- from `matrix_docker_image_postgres_v9` to `matrix_postgres_docker_image_v9`
- from `matrix_docker_image_postgres_v10` to `matrix_postgres_docker_image_v10`
- from `matrix_docker_image_postgres_latest` to `matrix_postgres_docker_image_latest`


# 2018-10-26

## Mautrix Whatsapp bridging support

The playbook now supports bridging with [Whatsapp](https://www.whatsapp.com/) by installing the [mautrix-whatsapp](https://github.com/tulir/mautrix-whatsapp) bridge. This playbook functionality is available thanks to [@izissise](https://github.com/izissise).

Additional details are available in [Setting up Mautrix Whatsapp bridging](docs/configuring-playbook-bridge-mautrix-whatsapp.md).


# 2018-10-25

## Support for controlling Matrix federation

The playbook can now help you with [Controlling Matrix federation](docs/configuring-playbook-federation), should you wish to run a more private (isolated) server.


# 2018-10-24

## Disabling riot-web guests

From now on, Riot's configuration setting `disable_guests` would be set to `true`. The homeserver was rejecting guests anyway, so this is just a cosmetic change affecting Riot's UI.


# 2018-10-21

## Self-check maintenance command

The playbook can now [check if services are configured correctly](docs/maintenance-and-troubleshooting.md#how-to-check-if-services-work).


# 2018-10-05

## Presence tracking made configurable

The playbook can now enable/disable user presence-status tracking in Synapse, through the playbook's `matrix_synapse_use_presence` variable (having a default value of `true` — enabled).

If users participate in large rooms with many other servers, disabling presence will decrease server load significantly.


# 2018-09-27

## Synapse Cache Factor made configurable

The playbook now makes the Synapse cache factor configurable, through the playbook's `matrix_synapse_cache_factor` variable (having a default value of `0.5`).

Changing that value allows you to potentially decrease RAM usage or to increase performance by caching more stuff. Some information on it is available here: https://github.com/element-hq/synapse#help-synapse-eats-all-my-ram


# 2018-09-26

## Disabling Docker container logging

`--log-driver=none` is used for all Docker containers now.

All these containers are started through systemd anyway and get logged in journald, so there's no need for Docker to be logging the same thing using the default `json-file` driver. Doing that was growing `/var/lib/docker/containers/…` infinitely until service/container restart.

As a result of this, things like `docker logs matrix-synapse` won't work anymore. `journalctl -u matrix-synapse` is how one can see the logs.


# 2018-09-17

## Service discovery support

The playbook now helps you set up [service discovery](https://matrix.org/docs/spec/client_server/r0.4.0.html#server-discovery) using a `/.well-known/matrix/client` file.

Additional details are available in [Configuring service discovery via .well-known](docs/configuring-well-known.md).

## (BC Break) Renaming playbook variables

The following playbook variables were renamed:

- from `matrix_nginx_riot_web_data_path` to `matrix_riot_web_data_path`
- from `matrix_riot_web_default_identity_server_url` to `matrix_identity_server_url`


# 2018-09-07

## Mautrix Telegram bridging support

The playbook now supports bridging with [Telegram](https://telegram.org/) by installing the [mautrix-telegram](https://github.com/tulir/mautrix-telegram) bridge. This playbook functionality is available thanks to [@izissise](https://github.com/izissise).

Additional details are available in [Setting up Mautrix Telegram bridging](docs/configuring-playbook-bridge-mautrix-telegram.md).

## Events cache size increase and configurability for Matrix Synapse

The playbook now lets you configure Matrix Synapse's `event_cache_size` configuration via the `matrix_synapse_event_cache_size` playbook variable.

Previously, this value was hardcoded to `"10K"`. From now on, a more reasonable default of `"100K"` is used.

## Password-peppering support for Matrix Synapse

The playbook now supports enabling password-peppering for increased security in Matrix Synapse via the `matrix_synapse_password_config_pepper` playbook variable. Using a password pepper is disabled by default (just like it used to be before this playbook variable got introduced) and is not to be enabled/disabled after initial setup, as that would invalidate all existing passwords.

## Statistics-reporting support for Matrix Synapse

There's now a new `matrix_synapse_report_stats` playbook variable, which controls the `report_stats` configuration option for Matrix Synapse. It defaults to `false`, so no change is required to retain your privacy.

If you'd like to start reporting statistics about your homeserver (things like number of users, number of messages sent, uptime, load, etc.) to matrix.org, you can turn on stats reporting.


# 2018-08-29

## Changing the way SSL certificates are retrieved

We've been using [acmetool](https://github.com/hlandau/acme) (with the [willwill/acme-docker](https://hub.docker.com/r/willwill/acme-docker/) Docker image) until now.

Due to the Docker image being deprecated, and things looking bleak for acmetool's support of the newer ACME v2 API endpoint, we've switched to using [certbot](https://certbot.eff.org/) (with the [certbot/certbot](https://hub.docker.com/r/certbot/certbot/) Docker image).

Simply re-running the playbook will retrieve new certificates (via certbot) for you. To ensure you don't leave any old files behind, though, you'd better do this:

- `systemctl stop 'matrix*'`
- stop your custom webserver, if you're running one (only affects you if you've installed with `matrix_nginx_proxy_enabled: false`)
- `mv /matrix/ssl /matrix/ssl-acmetool-delete-later`
- re-run the playbook's [installation](docs/installing.md)
- possibly delete `/matrix/ssl-acmetool-delete-later`


# 2018-08-21

## Matrix Corporal support

The playbook can now install and configure [matrix-corporal](https://github.com/devture/matrix-corporal) for you.

Additional details are available in [Setting up Matrix Corporal](docs/configuring-playbook-matrix-corporal.md).


# 2018-08-20

## Matrix Synapse rate limit control variables

The following new variables can now be configured to control Matrix Synapse's rate-limiting (default values are shown below).

```yaml
matrix_synapse_rc_messages_per_second: 0.2
matrix_synapse_rc_message_burst_count: 10.0
```

## Shared Secret Auth support via matrix-synapse-shared-secret-auth

The playbook can now install and configure [matrix-synapse-shared-secret-auth](https://github.com/devture/matrix-synapse-shared-secret-auth) for you.

Additional details are available in [Setting up the Shared Secret Auth password provider module](docs/configuring-playbook-shared-secret-auth.md).


# 2018-08-17

## REST auth support via matrix-synapse-rest-auth

The playbook can now install and configure [matrix-synapse-rest-auth](https://github.com/kamax-io/matrix-synapse-rest-auth) for you.

Additional details are available in [Setting up the REST authentication password provider module](docs/configuring-playbook-rest-auth.md).

## Compression improvements

Shifted Matrix Synapse compression from happening in the Matrix Synapse,
to happening in the nginx proxy that's in front of it.

Additionally, `riot-web` also gets compressed now (in the nginx proxy),
which drops the initial page load's size from 5.31MB to 1.86MB.

## Disabling some unnecessary Synapse services

The following services are not necessary, so they have been disabled:
- on the federation port (8448): the `client` service
- on the http port (8008, exposed over 443): the old Angular `webclient` and the `federation` service

Federation runs only on the federation port (8448) now. The Client APIs run only on the http port (8008) now.


# 2018-08-15

## mxisd Identity Server support

The playbook now sets up an [mxisd](https://github.com/kamax-io/mxisd) Identity Server for you by default. Additional details are available in [Setting up ma1sd Identity Server](docs/configuring-playbook-mxisd.md).


# 2018-08-14

## Email-sending support

The playbook now configures an email-sending service (postfix) by default. Additional details are available in [Adjusting email-sending settings](docs/configuring-playbook-email.md).

With this, Matrix Synapse is able to send email notifications for missed messages, etc.


# 2018-08-08

## (BC Break) Renaming playbook variables

The following playbook variables were renamed:

- from `matrix_max_upload_size_mb` to `matrix_synapse_max_upload_size_mb`
- from `matrix_max_log_file_size_mb` to `matrix_synapse_max_log_file_size_mb`
- from `matrix_max_log_files_count` to `matrix_synapse_max_log_files_count`
- from `docker_matrix_image` to `matrix_docker_image_synapse`
- from `docker_nginx_image` to `matrix_docker_image_nginx`
- from `docker_riot_image` to `matrix_docker_image_riot`
- from `docker_goofys_image` to `matrix_docker_image_goofys`
- from `docker_coturn_image` to `matrix_docker_image_coturn`

If you're overriding any of them in your `vars.yml` file, you'd need to change to the new names.

## Renaming Ansible playbook tag

The command for executing the whole playbook has changed. The `setup-main` tag got renamed to `setup-all`.

## Docker container linking

Changed the way the Docker containers are linked together. The ones that need to communicate with others operate in a `matrix` network now and not in the default bridge network.
