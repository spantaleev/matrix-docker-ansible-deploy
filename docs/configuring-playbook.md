<!--
SPDX-FileCopyrightText: 2018 - 2024 MDAD project contributors
SPDX-FileCopyrightText: 2018 - 2025 Slavi Pantaleev
SPDX-FileCopyrightText: 2020 Sabine Laszakovits
SPDX-FileCopyrightText: 2021 Cody Neiman
SPDX-FileCopyrightText: 2021 Matthew Cengia
SPDX-FileCopyrightText: 2021 Toni Spets
SPDX-FileCopyrightText: 2022 Julian Foad
SPDX-FileCopyrightText: 2022 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2022 Vladimir Panteleev
SPDX-FileCopyrightText: 2023 Shreyas Ajjarapu
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Configuring the playbook

<sup>[Prerequisites](prerequisites.md) > [Configuring DNS settings](configuring-dns.md) > [Getting the playbook](getting-the-playbook.md) > Configuring the playbook > [Installing](installing.md)</sup>

If you've configured your DNS records and retrieved the playbook's source code to your computer, you can start configuring the playbook. To do so, follow these steps inside the playbook directory:

1. create a directory to hold your configuration (`mkdir -p inventory/host_vars/matrix.example.com` where `example.com` is your "base domain")

2. copy the sample configuration file (`cp examples/vars.yml inventory/host_vars/matrix.example.com/vars.yml`)

3. edit the configuration file (`inventory/host_vars/matrix.example.com/vars.yml`) to your liking. You may also take a look at the various `roles/*/ROLE_NAME_HERE/defaults/main.yml` files (after importing external roles with `just update` into `roles/galaxy`) and see if there's something you'd like to copy over and override in your `vars.yml` configuration file.

4. copy the sample inventory hosts file (`cp examples/hosts inventory/hosts`)

5. edit the inventory hosts file (`inventory/hosts`) to your liking

6. (optional, advanced) you may wish to keep your `inventory` directory under version control with [git](https://git-scm.com/) or any other version-control system. The `inventory` directory path is ignored via `.gitignore`, so it won't be part of the playbook repository. You can safely create a new git repository inside that directory with `git init`, etc.

7. (optional, advanced) to run Ansible against multiple servers with different `sudo` credentials, you can copy the sample inventory hosts yaml file for each of your hosts: (`cp examples/host.yml inventory/my_host1.yml` …) and use the [`ansible-all-hosts.sh`](../bin/ansible-all-hosts.sh) script [in the installation step](installing.md).

For a basic Matrix installation, that's all you need.

For a more custom setup, see the [Other configuration options](#other-configuration-options) below.

[▶️](installing.md) When you're done with all the configuration you'd like to do, continue with [Installing](installing.md).

## Other configuration options

**Note**: some of the roles like one for integrating Etherpad or Jitsi are managed by their own repositories, and the configuration files for them cannot be found locally (in `roles/galaxy`) until those roles are fetched from the upstream projects. Check [requirements.yml](../requirements.yml) for the URLs of those roles.

### Core service adjustments

- Homeserver configuration:
  - [Configuring Synapse](configuring-playbook-synapse.md), if you're going with the default/recommended homeserver implementation

  - [Configuring Conduit](configuring-playbook-conduit.md), if you've switched to the [Conduit](https://conduit.rs) homeserver implementation

  - [Configuring conduwuit](configuring-playbook-conduwuit.md), if you've switched to the [conduwuit](https://conduwuit.puppyirl.gay/) homeserver implementation

  - [Configuring continuwuity](configuring-playbook-continuwuity.md), if you've switched to the [continuwuity](https://continuwuity.org) homeserver implementation

  - [Configuring Dendrite](configuring-playbook-dendrite.md), if you've switched to the [Dendrite](https://matrix-org.github.io/dendrite) homeserver implementation

- Server components:
  - [Using an external PostgreSQL server](configuring-playbook-external-postgres.md)

  - [Configuring a TURN server](configuring-playbook-turn.md) (advanced)

  - [Configuring the Traefik reverse-proxy](configuring-playbook-traefik.md) (advanced)

  - [Using your own webserver, instead of this playbook's Traefik reverse-proxy](configuring-playbook-own-webserver.md) (advanced)

  - [Adjusting SSL certificate retrieval](configuring-playbook-ssl-certificates.md) (advanced)

  - [Adjusting email-sending settings](configuring-playbook-email.md)

  - [Setting up ma1sd Identity Server](configuring-playbook-ma1sd.md)

  - [Setting up Dynamic DNS](configuring-playbook-dynamic-dns.md)

- Server connectivity:
  - [Enabling Telemetry for your Matrix server](configuring-playbook-telemetry.md)

  - [Controlling Matrix federation](configuring-playbook-federation.md)

  - [Configuring IPv6](./configuring-ipv6.md)

### Clients

Web clients for Matrix that you can host on your own domains.

- [Configuring Element Web](configuring-playbook-client-element-web.md), if you're going with the default/recommended client

- [Setting up Hydrogen](configuring-playbook-client-hydrogen.md), if you've enabled [Hydrogen](https://github.com/element-hq/hydrogen-web), a lightweight Matrix client with legacy and mobile browser support

- [Setting up Cinny](configuring-playbook-client-cinny.md), if you've enabled [Cinny](https://github.com/ajbura/cinny), a web client focusing primarily on simple, elegant and secure interface

- [Setting up SchildiChat Web](configuring-playbook-client-schildichat-web.md), if you've enabled [SchildiChat Web](https://schildi.chat/), a web client based on [Element Web](https://element.io/) with some extras and tweaks

- [Setting up FluffyChat Web](configuring-playbook-client-fluffychat-web.md), if you've enabled [FluffyChat Web](https://github.com/krille-chan/fluffychat), a cute cross-platform messenger (web, iOS, Android) for Matrix written in [Flutter](https://flutter.dev/)


### Authentication and user-related

Extend and modify how users are authenticated on your homeserver.

- [Setting up Matrix Authentication Service](configuring-playbook-matrix-authentication-service.md) (Next-generation auth for Matrix, based on OAuth 2.0/OIDC)

- [Setting up Appservice Double Puppet](configuring-playbook-appservice-double-puppet.md)

- [Setting up Synapse Admin](configuring-playbook-synapse-admin.md)

- [Setting up matrix-registration](configuring-playbook-matrix-registration.md)

- [Setting up the REST authentication password provider module](configuring-playbook-rest-auth.md) (advanced)

- [Setting up the Shared Secret Auth password provider module](configuring-playbook-shared-secret-auth.md) (advanced)

- [Setting up the LDAP authentication password provider module](configuring-playbook-ldap-auth.md) (advanced)

- [Setting up matrix-ldap-registration-proxy](configuring-playbook-matrix-ldap-registration-proxy.md) (advanced)

- [Setting up Synapse Simple Antispam](configuring-playbook-synapse-simple-antispam.md) (advanced)

- [Setting up Matrix User Verification Service](configuring-playbook-user-verification-service.md) (advanced)

### File Storage

Use alternative file storage to the default `media_store` folder.

- [Storing Matrix media files using matrix-media-repo](configuring-playbook-matrix-media-repo.md)

- [Storing Synapse media files on Amazon S3 or another compatible Object Storage](configuring-playbook-s3.md)

- [Storing Synapse media files on Amazon S3 with Goofys](configuring-playbook-s3-goofys.md)

- [Storing Synapse media files on Amazon S3 with synapse-s3-storage-provider](configuring-playbook-synapse-s3-storage-provider.md)

### Bridging other networks

Bridges can be used to connect your Matrix installation with third-party communication networks.

- [Setting up a Generic Mautrix Bridge](configuring-playbook-bridge-mautrix-bridges.md) — a common guide for configuring mautrix bridges

- [Setting up Mautrix Bluesky bridging](configuring-playbook-bridge-mautrix-bluesky.md)

- [Setting up Mautrix Discord bridging](configuring-playbook-bridge-mautrix-discord.md)

- [Setting up Mautrix Telegram bridging](configuring-playbook-bridge-mautrix-telegram.md)

- [Setting up Mautrix Slack bridging](configuring-playbook-bridge-mautrix-slack.md)

- [Setting up Mautrix Google Messages bridging](configuring-playbook-bridge-mautrix-gmessages.md)

- [Setting up Mautrix Whatsapp bridging](configuring-playbook-bridge-mautrix-whatsapp.md)

- [Setting up Instagram bridging via Mautrix Meta](configuring-playbook-bridge-mautrix-meta-instagram.md)

- [Setting up Messenger bridging via Mautrix Meta](configuring-playbook-bridge-mautrix-meta-messenger.md)

- [Setting up Mautrix Google Chat bridging](configuring-playbook-bridge-mautrix-googlechat.md)

- [Setting up Mautrix Twitter bridging](configuring-playbook-bridge-mautrix-twitter.md)

- [Setting up Mautrix Signal bridging](configuring-playbook-bridge-mautrix-signal.md)

- [Setting up Mautrix wsproxy for bridging Android SMS or Apple iMessage](configuring-playbook-bridge-mautrix-wsproxy.md)

- [Setting up Appservice IRC bridging](configuring-playbook-bridge-appservice-irc.md)

- [Setting up Appservice Discord bridging](configuring-playbook-bridge-appservice-discord.md)

- [Setting up Appservice Slack bridging](configuring-playbook-bridge-appservice-slack.md)

- [Setting up Appservice Kakaotalk bridging](configuring-playbook-bridge-appservice-kakaotalk.md)

- [Setting up Beeper LinkedIn bridging](configuring-playbook-bridge-beeper-linkedin.md)

- [Setting up matrix-hookshot](configuring-playbook-bridge-hookshot.md) — a bridge between Matrix and multiple project management services, such as [GitHub](https://github.com), [GitLab](https://about.gitlab.com) and [JIRA](https://www.atlassian.com/software/jira).

- [Setting up MX Puppet Slack bridging](configuring-playbook-bridge-mx-puppet-slack.md)

- [Setting up MX Puppet Instagram bridging](configuring-playbook-bridge-mx-puppet-instagram.md)

- [Setting up MX Puppet Twitter bridging](configuring-playbook-bridge-mx-puppet-twitter.md)

- [Setting up MX Puppet Discord bridging](configuring-playbook-bridge-mx-puppet-discord.md)

- [Setting up MX Puppet GroupMe bridging](configuring-playbook-bridge-mx-puppet-groupme.md)

- [Setting up Steam bridging](configuring-playbook-bridge-steam.md)

- [Setting up MX Puppet Steam bridging](configuring-playbook-bridge-mx-puppet-steam.md)

- [Setting up Go Skype Bridge bridging](configuring-playbook-bridge-go-skype-bridge.md)

- [Setting up Postmoogle email bridging](configuring-playbook-bridge-postmoogle.md)

- [Setting up Matrix SMS bridging](configuring-playbook-bridge-matrix-bridge-sms.md)

- [Setting up Heisenbridge bouncer-style IRC bridging](configuring-playbook-bridge-heisenbridge.md)

- [Setting up WeChat bridging](configuring-playbook-bridge-wechat.md)

### Bots

Bots provide various additional functionality to your installation.

- [Setting up baibot](configuring-playbook-bot-baibot.md) — a bot through which you can talk to various [AI](https://en.wikipedia.org/wiki/Artificial_intelligence) / [Large Language Models](https://en.wikipedia.org/wiki/Large_language_model) services ([OpenAI](https://openai.com/)'s [ChatGPT](https://openai.com/blog/chatgpt/) and [others](https://github.com/etkecc/baibot/blob/main/docs/providers.md))

- [Setting up matrix-reminder-bot](configuring-playbook-bot-matrix-reminder-bot.md) — a bot to remind you about stuff

- [Setting up matrix-registration-bot](configuring-playbook-bot-matrix-registration-bot.md) — a bot to create and manage registration tokens to invite users

- [Setting up maubot](configuring-playbook-bot-maubot.md) — a plugin-based Matrix bot system

- [Setting up Honoroit](configuring-playbook-bot-honoroit.md) — a helpdesk bot

- [Setting up Mjolnir](configuring-playbook-bot-mjolnir.md) — a moderation tool/bot

- [Setting up Draupnir](configuring-playbook-bot-draupnir.md) — a moderation tool/bot, forked from Mjolnir and maintained by its former leader developer

- [Setting up Draupnir for all/D4A](configuring-playbook-appservice-draupnir-for-all.md) — like the [Draupnir bot](configuring-playbook-bot-draupnir.md) mentioned above, but running in appservice mode and supporting multiple instances

- [Setting up Buscarron](configuring-playbook-bot-buscarron.md) — a bot you can use to send any form (HTTP POST, HTML) to a (encrypted) Matrix room

### Administration

Services that help you in administrating and monitoring your Matrix installation.

- [Setting up Prometheus Alertmanager integration via matrix-alertmanager-receiver](configuring-playbook-alertmanager-receiver.md)

- [Enabling metrics and graphs (Prometheus, Grafana) for your Matrix server](configuring-playbook-prometheus-grafana.md)

- [Setting up the rageshake bug report server](configuring-playbook-rageshake.md)

- [Enabling synapse-usage-exporter for Synapse usage statistics](configuring-playbook-synapse-usage-exporter.md)

- Backups:
  - [Setting up BorgBackup](configuring-playbook-backup-borg.md) — a full Matrix server backup solution, including the Postgres database

  - [Setting up Postgres backup](configuring-playbook-postgres-backup.md) — a Postgres-database backup solution (note: does not include other files)

### Other specialized services

Various services that don't fit any other categories.

- [Setting up Element Call](configuring-playbook-element-call.md) — a native Matrix video conferencing application, built on top of the [Matrix RTC stack](configuring-playbook-matrix-rtc.md) (optional)

- [Setting up LiveKit JWT Service](configuring-playbook-livekit-jwt-service.md) - a component of the [Matrix RTC stack](configuring-playbook-matrix-rtc.md) (optional)

- [Setting up LiveKit Server](configuring-playbook-livekit-server.md) - a component of the [Matrix RTC stack](configuring-playbook-matrix-rtc.md) (optional)

- [Setting up Matrix RTC](configuring-playbook-matrix-rtc.md) (optional)

- [Setting up Synapse Auto Invite Accept](configuring-playbook-synapse-auto-accept-invite.md)

- [Setting up synapse-auto-compressor](configuring-playbook-synapse-auto-compressor.md) for compressing the database on Synapse homeservers

- [Setting up Matrix Corporal](configuring-playbook-matrix-corporal.md) (advanced)

- [Setting up Etherpad](configuring-playbook-etherpad.md)

- [Setting up the Jitsi video-conferencing platform](configuring-playbook-jitsi.md)

- [Setting up Cactus Comments](configuring-playbook-cactus-comments.md) — a federated comment system built on Matrix

- [Setting up Pantalaimon (E2EE aware proxy daemon)](configuring-playbook-pantalaimon.md) (advanced)

- [Setting up the Sygnal push gateway](configuring-playbook-sygnal.md)

- [Setting up the ntfy push notifications server](configuring-playbook-ntfy.md)

### Deprecated / unmaintained / removed services

**Note**: since a deprecated or unmaintained service will not be updated, its bug or vulnerability will be unlikely to get patched. It is recommended to migrate from the service to an alternative if any, and make sure to do your own research before you decide to keep it running nonetheless.

- [Setting up the Sliding Sync proxy](configuring-playbook-sliding-sync-proxy.md) for clients which require Sliding Sync support (like old Element X versions, before it got switched to Simplified Sliding Sync)

- [Setting up Appservice Webhooks bridging](configuring-playbook-bridge-appservice-webhooks.md) (deprecated; the bridge's author suggests taking a look at [matrix-hookshot](https://github.com/matrix-org/matrix-hookshot) as a replacement, which can also be [installed using this playbook](configuring-playbook-bridge-hookshot.md))

- [Setting up the Dimension integration manager](configuring-playbook-dimension.md) ([unmaintained](https://github.com/spantaleev/matrix-docker-ansible-deploy/issues/2806#issuecomment-1673559299); after [installing](installing.md))

- [Setting up Email2Matrix](configuring-playbook-email2matrix.md) (removed; the author suggests taking a look at [Postmoogle](https://github.com/etkecc/postmoogle) as a replacement, which can also be [installed using this playbook](configuring-playbook-bridge-postmoogle.md))

- [Setting up Go-NEB](configuring-playbook-bot-go-neb.md) (unmaintained; the bridge's author suggests taking a look at [matrix-hookshot](https://github.com/matrix-org/matrix-hookshot) as a replacement, which can also be [installed using this playbook](configuring-playbook-bridge-hookshot.md))

- [Setting up matrix-bot-chatgpt](configuring-playbook-bot-chatgpt.md) (unmaintained; the bridge's author suggests taking a look at [baibot](https://github.com/etkecc/baibot) as a replacement, which can also be [installed using this playbook](configuring-playbook-bot-baibot.md))

- [Setting up Mautrix Facebook bridging](configuring-playbook-bridge-mautrix-facebook.md) (deprecated in favor of the Messenger/Instagram bridge with [mautrix-meta-messenger](configuring-playbook-bridge-mautrix-meta-messenger.md))

- [Setting up Mautrix Instagram bridging](configuring-playbook-bridge-mautrix-instagram.md) (deprecated in favor of the Messenger/Instagram bridge with [mautrix-meta-instagram](configuring-playbook-bridge-mautrix-meta-instagram.md))

- [Setting up MX Puppet Skype bridging](configuring-playbook-bridge-mx-puppet-skype.md) (removed; this component has been broken for a long time, so it has been removed from the playbook. Consider [setting up Go Skype Bridge bridging](configuring-playbook-bridge-go-skype-bridge.md))
