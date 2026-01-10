<!--
SPDX-FileCopyrightText: 2021 - 2022 Aaron Raimist
SPDX-FileCopyrightText: 2021 - 2024 MDAD project contributors
SPDX-FileCopyrightText: 2021 - 2025 Slavi Pantaleev
SPDX-FileCopyrightText: 2021 Cody Neiman
SPDX-FileCopyrightText: 2021 Dan Arnfield
SPDX-FileCopyrightText: 2021 Marcus Proest
SPDX-FileCopyrightText: 2021 Matthew Cengia
SPDX-FileCopyrightText: 2022 Cody Wyatt Neiman
SPDX-FileCopyrightText: 2022 Julian Foad
SPDX-FileCopyrightText: 2022 Julian-Samuel Gebühr
SPDX-FileCopyrightText: 2023 Shreyas Ajjarapu
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Container images used by the playbook

This page summarizes the container ([Docker](https://www.docker.com/)) images used by the playbook when setting up your server.

We try to stick to official images (provided by their respective projects) as much as possible.

## Homeserver

| Service | Container image | Default? | Description |
| ------- | --------------- | -------- | ----------- |
| [Synapse](configuring-playbook-synapse.md) | [element-hq/synapse](https://ghcr.io/element-hq/synapse) | ✅ | Storing your data and managing your presence in the [Matrix](http://matrix.org/) network |
| [Conduit](configuring-playbook-conduit.md) | [matrixconduit/matrix-conduit](https://hub.docker.com/r/matrixconduit/matrix-conduit) | ❌ | Storing your data and managing your presence in the [Matrix](http://matrix.org/) network. Conduit is a lightweight open-source server implementation of the Matrix Specification with a focus on easy setup and low system requirements |
| [conduwuit](configuring-playbook-conduwuit.md) | [girlbossceo/conduwuit](https://ghcr.io/girlbossceo/conduwuit) | ❌ | Storing your data and managing your presence in the [Matrix](http://matrix.org/) network. conduwuit is a fork of Conduit. |
| [continuwuity](configuring-playbook-continuwuity.md) | [continuwuation/continuwuity](https://forgejo.ellis.link/continuwuation/continuwuity) | ❌ | Storing your data and managing your presence in the [Matrix](http://matrix.org/) network. continuwuity is a continuation of conduwuit. |
| [Dendrite](configuring-playbook-dendrite.md) | [matrixdotorg/dendrite-monolith](https://hub.docker.com/r/matrixdotorg/dendrite-monolith/) | ❌ | Storing your data and managing your presence in the [Matrix](http://matrix.org/) network. Dendrite is a second-generation Matrix homeserver written in Go, an alternative to Synapse. |

## Clients

Web clients for Matrix that you can host on your own domains.

| Service | Container image | Default? | Description |
| ------- | --------------- | -------- | ----------- |
| [Element Web](configuring-playbook-client-element-web.md) | [vectorim/element-web](https://hub.docker.com/r/vectorim/element-web/) | ✅ | Default Matrix web client, configured to connect to your own Synapse server |
| [Hydrogen](configuring-playbook-client-hydrogen.md) | [element-hq/hydrogen-web](https://ghcr.io/element-hq/hydrogen-web) | ❌ | Lightweight Matrix client with legacy and mobile browser support |
| [Cinny](configuring-playbook-client-cinny.md) | [ajbura/cinny](https://hub.docker.com/r/ajbura/cinny) | ❌ | Simple, elegant and secure web client |
| [SchildiChat Web](configuring-playbook-client-schildichat-web.md) | [etke.cc/schildichat-web](https://ghcr.io/etkecc/schildichat-web) | ❌ | Based on Element Web, with a more traditional instant messaging experience |

## Server Components

Services that run on the server to make the various parts of your installation work.

| Service | Container image | Default? | Description |
| ------- | --------------- | -------- | ----------- |
| [PostgreSQL](configuring-playbook-external-postgres.md) | [postgres](https://hub.docker.com/_/postgres/) | ✅ | Database for Synapse. [Using an external PostgreSQL server](configuring-playbook-external-postgres.md) is also possible. |
| [coturn](configuring-playbook-turn.md) | [coturn/coturn](https://hub.docker.com/r/coturn/coturn/) | ✅ | STUN/TURN server for WebRTC audio/video calls |
| [Traefik](configuring-playbook-traefik.md) | [Traefik](https://hub.docker.com/_/traefik/) | ✅ | Web server, listening on ports 80, 443 and 8448 — standing in front of all the other services. [Using your own webserver](configuring-playbook-own-webserver.md) is also possible. |
| [Let's Encrypt](configuring-playbook-ssl-certificates.md) | [certbot/certbot](https://hub.docker.com/r/certbot/certbot/) | ✅ | [Certbot](https://certbot.eff.org/) tool for obtaining SSL certificates from [Let's Encrypt](https://letsencrypt.org/) |
| [Exim](configuring-playbook-email.md) | [devture/exim-relay](https://hub.docker.com/r/devture/exim-relay/) | ✅ | Mail server, through which all Matrix services send outgoing email (can be configured to relay through another SMTP server) |
| [ma1sd](configuring-playbook-ma1sd.md) | [ma1uta/ma1sd](https://hub.docker.com/r/ma1uta/ma1sd/) | ❌ | Matrix Identity Server |
| [ddclient](configuring-playbook-dynamic-dns.md) | [linuxserver/ddclient](https://hub.docker.com/r/linuxserver/ddclient) | ❌ | Update dynamic DNS entries for accounts on Dynamic DNS Network Service Provider |
| [LiveKit Server](configuring-playbook-livekit-server.md) | [livekit/livekit-server](https://hub.docker.com/r/livekit/livekit-server/) | ❌ | WebRTC server for audio/video calls |
| [Livekit JWT Service](configuring-playbook-livekit-jwt-service.md) | [element-hq/lk-jwt-service](https://ghcr.io/element-hq/lk-jwt-service) | ❌ | JWT service for integrating [Element Call](./configuring-playbook-element-call.md) with [LiveKit Server](./configuring-playbook-livekit-server.md) |

## Authentication

Extend and modify how users are authenticated on your homeserver.

| Service | Container image | Default? | Description |
| ------- | --------------- | -------- | ----------- |
| [matrix-synapse-rest-auth](configuring-playbook-rest-auth.md) | (N/A) | ❌ | REST authentication password provider module |
| [matrix-synapse-shared-secret-auth](configuring-playbook-shared-secret-auth.md) | (N/A) | ❌ | Password provider module |
| [matrix-synapse-ldap3](configuring-playbook-ldap-auth.md) (advanced) | (N/A) | ❌ | LDAP Auth password provider module |
| [matrix-ldap-registration-proxy](configuring-playbook-matrix-ldap-registration-proxy.md) | [activism.international/matrix_ldap_registration_proxy](https://gitlab.com/activism.international/matrix_ldap_registration_proxy/container_registry) | ❌ | Proxy that handles Matrix registration requests and forwards them to LDAP |
| [matrix-registration](configuring-playbook-matrix-registration.md) | [zeratax/matrix-registration](https://hub.docker.com/r/devture/zeratax-matrix-registration/) | ❌ | Simple python application to have a token based Matrix registration |
| [Matrix User Verification Service](configuring-playbook-user-verification-service.md) | [matrixdotorg/matrix-user-verification-service](https://hub.docker.com/r/atrixdotorg/matrix-user-verification-service) | ❌ | Service to verify details of a user based on an Open ID token |
| [synapse-simple-antispam](configuring-playbook-synapse-simple-antispam.md) (advanced) | (N/A) | ❌ | Spam checker module |

## File Storage

Use alternative file storage to the default `media_store` folder.

| Service | Container image | Default? | Description |
| ------- | --------------- | -------- | ----------- |
| [Goofys](configuring-playbook-s3-goofys.md) | [ewoutp/goofys](https://hub.docker.com/r/ewoutp/goofys/) | ❌ | [Amazon S3](https://aws.amazon.com/s3/) (or other S3-compatible object store) storage for Synapse's content repository (`media_store`) files |
| [synapse-s3-storage-provider](configuring-playbook-s3.md) | (N/A) | ❌ | [Amazon S3](https://aws.amazon.com/s3/) (or other S3-compatible object store) storage for Synapse's content repository (`media_store`) files |
| [matrix-media-repo](configuring-playbook-matrix-media-repo.md) | [t2bot/matrix-media-repo](https://ghcr.io/t2bot/matrix-media-repo) | ❌ | Highly customizable multi-domain media repository for Matrix. Intended for medium to large deployments, this media repo de-duplicates media while being fully compliant with the specification. |

# Bridges

Bridges can be used to connect your Matrix installation with third-party communication networks.

| Service | Container image | Default? | Description |
| ------- | --------------- | -------- | ----------- |
| [mautrix-bluesky](configuring-playbook-bridge-mautrix-bluesky.md) | [mautrix/bluesky](https://mau.dev/mautrix/bluesky/container_registry) | ❌ | Bridge to [Bluesky](https://bsky.social/about) |
| [mautrix-discord](configuring-playbook-bridge-mautrix-discord.md) | [mautrix/discord](https://mau.dev/mautrix/discord/container_registry) | ❌ | Bridge to [Discord](https://discord.com/) |
| [mautrix-slack](configuring-playbook-bridge-mautrix-slack.md) | [mautrix/slack](https://mau.dev/mautrix/slack/container_registry) | ❌ | Bridge to [Slack](https://slack.com/) |
| [mautrix-telegram](configuring-playbook-bridge-mautrix-telegram.md) | [mautrix/telegram](https://mau.dev/mautrix/telegram/container_registry) | ❌ | Bridge to [Telegram](https://telegram.org/) |
| [mautrix-gmessages](configuring-playbook-bridge-mautrix-gmessages.md) | [mautrix/gmessages](https://mau.dev/mautrix/gmessages/container_registry) | ❌ | Bridge to [Google Messages](https://messages.google.com/) |
| [mautrix-whatsapp](configuring-playbook-bridge-mautrix-whatsapp.md) | [mautrix/whatsapp](https://mau.dev/mautrix/whatsapp/container_registry) | ❌ | Bridge to [WhatsApp](https://www.whatsapp.com/) |
| [mautrix-wsproxy](configuring-playbook-bridge-mautrix-wsproxy.md) | [mautrix/wsproxy](https://mau.dev/mautrix/wsproxy/container_registry) | ❌ | Bridge to Android SMS or Apple iMessage |
| [mautrix-twitter](configuring-playbook-bridge-mautrix-twitter.md) | [mautrix/twitter](https://mau.dev/mautrix/twitter/container_registry) | ❌ | Bridge to [Twitter](https://twitter.com/) |
| [mautrix-googlechat](configuring-playbook-bridge-mautrix-googlechat.md) | [mautrix/googlechat](https://mau.dev/mautrix/googlechat/container_registry) | ❌ | Bridge to [Google Chat](https://en.wikipedia.org/wiki/Google_Chat) |
| mautrix-meta (for [Messenger](configuring-playbook-bridge-mautrix-meta-messenger.md) and [Instagram](configuring-playbook-bridge-mautrix-meta-instagram.md)) | [mautrix/meta](https://mau.dev/mautrix/meta/container_registry) | ❌ | Bridge to [Messenger](https://messenger.com/) and [Instagram](https://instagram.com/) |
| [mautrix-signal](configuring-playbook-bridge-mautrix-signal.md) | [mautrix/signal](https://mau.dev/mautrix/signal/container_registry) | ❌ | Bridge to [Signal](https://www.signal.org/) |
| [beeper-linkedin](configuring-playbook-bridge-beeper-linkedin.md) | [beeper/linkedin](https://ghcr.io/beeper/linkedin) | ❌ | Bridge to [LinkedIn](https://www.linkedin.com/) |
| [matrix-appservice-irc](configuring-playbook-bridge-appservice-irc.md) | [matrixdotorg/matrix-appservice-irc](https://hub.docker.com/r/matrixdotorg/matrix-appservice-irc) | ❌ | Bridge to [IRC](https://wikipedia.org/wiki/Internet_Relay_Chat) |
| [matrix-appservice-kakaotalk](configuring-playbook-bridge-appservice-kakaotalk.md) | Self-building | ❌ | Bridge to [Kakaotalk](https://www.kakaocorp.com/page/service/service/KakaoTalk?lang=ENG) |
| [matrix-appservice-discord](configuring-playbook-bridge-appservice-discord.md) | [matrix-org/matrix-appservice-discord](https://ghcr.io/matrix-org/matrix-appservice-discord) | ❌ | Bridge to [Discord](https://discordapp.com/) |
| [matrix-appservice-slack](configuring-playbook-bridge-appservice-slack.md) | [matrixdotorg/matrix-appservice-slack](https://hub.docker.com/r/matrixdotorg/matrix-appservice-slack) | ❌ | Bridge to [Slack](https://slack.com/) |
| [matrix-hookshot](configuring-playbook-bridge-hookshot.md) | [halfshot/matrix-hookshot](https://hub.docker.com/r/halfshot/matrix-hookshot) | ❌ | Bridge for generic webhooks and multiple project management services, such as GitHub, GitLab, Figma, and Jira in particular |
| [matrix-sms-bridge](configuring-playbook-bridge-matrix-bridge-sms.md) | [folivonet/matrix-sms-bridge](https://hub.docker.com/repository/docker/folivonet/matrix-sms-bridge) | ❌ | Bridge to SMS |
| [matrix-wechat](configuring-playbook-bridge-wechat.md) | [lxduo/matrix-wechat](https://hub.docker.com/r/lxduo/matrix-wechat) | ❌ | Bridge to [WeChat](https://www.wechat.com/) |
| [MatrixZulipBridge](configuring-playbook-bridge-zulip.md) | [GearKite/MatrixZulipBridge](https://ghcr.io/gearkite/matrixzulipbridge) | ❌ | Puppeting appservice bridge for [Zulip](https://zulip.com/) |
| [Heisenbridge](configuring-playbook-bridge-heisenbridge.md) | [hif1/heisenbridge](https://hub.docker.com/r/hif1/heisenbridge) | ❌ | Bouncer-style bridge to [IRC](https://wikipedia.org/wiki/Internet_Relay_Chat) |
| [mx-puppet-groupme](configuring-playbook-bridge-mx-puppet-groupme.md) | [xangelix/mx-puppet-groupme](https://hub.docker.com/r/xangelix/mx-puppet-groupme) | ❌ | Bridge to [GroupMe](https://groupme.com/) |
| [matrix-steam-bridge](configuring-playbook-bridge-steam.md) | [jasonlaguidice/matrix-steam-bridge](https://github.com/jasonlaguidice/matrix-steam-bridge/pkgs/container/matrix-steam-bridge) | ❌ | Bridge to [Steam](https://steampowered.com/) |
| [mx-puppet-steam](configuring-playbook-bridge-mx-puppet-steam.md) | [icewind1991/mx-puppet-steam](https://hub.docker.com/r/icewind1991/mx-puppet-steam) | ❌ | Bridge to [Steam](https://steamapp.com/) |
| [Postmoogle](configuring-playbook-bridge-postmoogle.md) | [etke.cc/postmoogle](https://github.com/etkecc/postmoogle/container_registry) | ❌ | Email to Matrix bridge |

## Bots

Bots provide various additional functionality to your installation.

| Service | Container image | Default? | Description |
| ------- | --------------- | -------- | ----------- |
| [baibot](configuring-playbook-bot-baibot.md) | [etke.cc/baibot](https://ghcr.io/etkecc/baibot) | ❌ | Bot that exposes the power of [AI](https://en.wikipedia.org/wiki/Artificial_intelligence) / [Large Language Models](https://en.wikipedia.org/wiki/Large_language_model) to you |
| [matrix-reminder-bot](configuring-playbook-bot-matrix-reminder-bot.md) | [anoa/matrix-reminder-bot](https://hub.docker.com/r/anoa/matrix-reminder-bot) | ❌ | Bot for scheduling one-off & recurring reminders and alarms |
| [matrix-registration-bot](configuring-playbook-bot-matrix-registration-bot.md) | [moanos/matrix-registration-bot](https://hub.docker.com/r/moanos/matrix-registration-bot/) | ❌ | Bot for invitations by creating and managing registration tokens |
| [maubot](configuring-playbook-bot-maubot.md) | [dock.mau.dev/maubot/maubot](https://mau.dev/maubot/maubot/container_registry) | ❌ | Plugin-based Matrix bot system |
| [Honoroit](configuring-playbook-bot-honoroit.md) | [etke.cc/honoroit](https://github.com/etkecc/honoroit/container_registry) | ❌ | Helpdesk bot |
| [Mjolnir](configuring-playbook-bot-mjolnir.md) | [matrixdotorg/mjolnir](https://hub.docker.com/r/matrixdotorg/mjolnir) | ❌ | Moderation tool for Matrix |
| [Draupnir](configuring-playbook-bot-draupnir.md) | [gnuxie/draupnir](https://hub.docker.com/r/gnuxie/draupnir) | ❌ | Moderation tool for Matrix (Fork of Mjolnir) |
| [Buscarron](configuring-playbook-bot-buscarron.md) | [etke.cc/buscarron](https://ghcr.io/etkecc/buscarron) | ❌ | Web forms (HTTP POST) to Matrix |

## Administration

Services that help you in administrating and monitoring your Matrix installation.

| Service | Container image | Default? | Description |
| ------- | --------------- | -------- | ----------- |
| [matrix-alertmanager-receiver](configuring-playbook-alertmanager-receiver.md) | [metio/matrix-alertmanager-receiver](https://hub.docker.com/r/metio/matrix-alertmanager-receiver)  | ❌ | Prometheus' [Alertmanager](https://prometheus.io/docs/alerting/latest/alertmanager/) client |
| [Matrix Authentication Service](configuring-playbook-matrix-authentication-service.md) | [element-hq/matrix-authentication-service](https://ghcr.io/element-hq/matrix-authentication-service) | ❌ | OAuth 2.0 and OpenID Provider server |
| [synapse-admin](configuring-playbook-synapse-admin.md) | [etke.cc/synapse-admin](https://ghcr.io/etkecc/synapse-admin) | ❌ | Web UI tool for administrating users and rooms on your Matrix server |
| [Metrics and Graphs](configuring-playbook-prometheus-grafana.md) | [prom/prometheus](https://hub.docker.com/r/prom/prometheus/) | ❌ | [Prometheus](https://prometheus.io) time-series database server |
| [Metrics and Graphs](configuring-playbook-prometheus-grafana.md) | [prom/node-exporter](https://hub.docker.com/r/prom/node-exporter/) | ❌ | Prometheus [node-exporter](https://prometheus.io/docs/guides/node-exporter/) host metrics exporter |
| [Metrics and Graphs](configuring-playbook-prometheus-grafana.md) | [grafana/grafana](https://hub.docker.com/r/grafana/grafana/) | ❌ | Graphing tool that works well with the above two images. Our playbook also adds two dashboards for [Synapse](https://github.com/element-hq/synapse/tree/master/contrib/grafana) and [Node Exporter](https://github.com/rfrail3/grafana-dashboards) |
| [Metrics and Graphs](configuring-playbook-prometheus-grafana.md#enable-metrics-and-graphs-for-nginx-logs-optional) | [martin-helmich/prometheus-nginxlog-exporter/exporter](https://ghcr.io/martin-helmich/prometheus-nginxlog-exporter/exporter) | ❌ | Addon for Prometheus that gathers access logs from various nginx reverse-proxies |
| [Borg](configuring-playbook-backup-borg.md) | (N/A) | ❌ | Backups |
| [postgres-backup-local](configuring-playbook-postgres-backup.md) | [prodrigestivill/postgres-backup-local](https://hub.docker.com/r/prodrigestivill/postgres-backup-local) | ❌ | Create automatic database backups |
| [rageshake](configuring-playbook-rageshake.md) | [matrix-org/rageshake](https://ghcr.io/matrix-org/rageshake) | ❌ | Bug report server |
| [synapse-usage-exporter](configuring-playbook-synapse-usage-exporter.md) | Self-building | ❌ | Export the usage statistics of a Synapse homeserver to be scraped by Prometheus. |

## Misc

Various services that don't fit any other categories.

| Service | Container image | Default? | Description |
| ------- | --------------- | -------- | ----------- |
| [sliding-sync](configuring-playbook-sliding-sync-proxy.md) | [matrix-org/sliding-sync](https://ghcr.io/matrix-org/sliding-sync) | ❌ | Sliding Sync support for clients which require it (like old Element X versions, before it got switched to Simplified Sliding Sync) |
| [synapse_auto_accept_invite](configuring-playbook-synapse-auto-accept-invite.md) | (N/A) | ❌ | Synapse module to automatically accept invites |
| [synapse_auto_compressor](configuring-playbook-synapse-auto-compressor.md) | [mb-saces/rust-synapse-tools](https://gitlab.com/mb-saces/rust-synapse-tools/container_registry) | ❌ | Cli tool that automatically compresses Synapse's `state_groups` database table in background |
| [Matrix Corporal](configuring-playbook-matrix-corporal.md) (advanced) | [devture/matrix-corporal](https://hub.docker.com/r/devture/matrix-corporal/) | ❌ | Reconciliator and gateway for a managed Matrix server |
| [Etherpad](configuring-playbook-etherpad.md) | [etherpad/etherpad](https://hub.docker.com/r/etherpad/etherpad/) | ❌ | Open source collaborative text editor |
| [Jitsi](configuring-playbook-jitsi.md) | [jitsi/web](https://hub.docker.com/r/jitsi/web) | ❌ | [Jitsi](https://jitsi.org/) web UI |
| [Jitsi](configuring-playbook-jitsi.md) | [jitsi/jicofo](https://hub.docker.com/r/jitsi/jicofo) | ❌ | [Jitsi](https://jitsi.org/) Focus component |
| [Jitsi](configuring-playbook-jitsi.md) | [jitsi/prosody](https://hub.docker.com/r/jitsi/prosody) | ❌ | [Jitsi](https://jitsi.org/) Prosody XMPP server component |
| [Jitsi](configuring-playbook-jitsi.md) | [jitsi/jvb](https://hub.docker.com/r/jitsi/jvb) | ❌ | [Jitsi](https://jitsi.org/) Video Bridge component |
| [Cactus Comments](configuring-playbook-cactus-comments.md) | [cactuscomments/cactus-appservice](https://hub.docker.com/r/cactuscomments/cactus-appservice/) | ❌ | Federated comment system built on Matrix |
| [Cactus Comments](configuring-playbook-cactus-comments.md) | [joseluisq/static-web-server](https://hub.docker.com/r/joseluisq/static-web-server) | ❌ | Federated comment system built on Matrix |
| [Pantalaimon](configuring-playbook-pantalaimon.md) | [matrixdotorg/pantalaimon](https://hub.docker.com/r/matrixdotorg/pantalaimon) | ❌ | E2EE aware proxy daemon |
| [Sygnal](configuring-playbook-sygnal.md) | [matrixdotorg/sygnal](https://hub.docker.com/r/matrixdotorg/sygnal/) | ❌ | Reference Push Gateway for Matrix |
| [ntfy](configuring-playbook-ntfy.md) | [binwiederhier/ntfy](https://hub.docker.com/r/binwiederhier/ntfy/) | ❌ | Self-hosted, UnifiedPush-compatible push notifications server |
| [Element Call](configuring-playbook-element-call.md) | [element-hq/element-call](https://ghcr.io/element-hq/element-call) | ❌ | A native Matrix video conferencing application |

## Container images of deprecated / unmaintained services

The list of the deprecated or unmaintained services is available [here](configuring-playbook.md#deprecated--unmaintained--removed-services).

| Service | Container image | Default? | Description |
| ------- | --------------- | -------- | ----------- |
| [Dimension](configuring-playbook-dimension.md) | [turt2live/matrix-dimension](https://hub.docker.com/r/turt2live/matrix-dimension) | ❌ | Open source integration manager for Matrix clients |
| [Email2Matrix](configuring-playbook-email2matrix.md) | [devture/email2matrix](https://hub.docker.com/r/devture/email2matrix/) | ❌ | Bridge for relaying emails to Matrix rooms |
| [Go-NEB](configuring-playbook-bot-go-neb.md) | [matrixdotorg/go-neb](https://hub.docker.com/r/matrixdotorg/go-neb) | ❌ | Multi functional bot written in Go |
| [matrix-appservice-webhooks](configuring-playbook-bridge-appservice-webhooks.md) | [turt2live/matrix-appservice-webhooks](https://hub.docker.com/r/turt2live/matrix-appservice-webhooks) | ❌ | Bridge for slack compatible webhooks ([ConcourseCI](https://concourse-ci.org/), [Slack](https://slack.com/) etc. pp.) |
| [matrix-chatgpt-bot](configuring-playbook-bot-chatgpt.md) | [matrixgpt/matrix-chatgpt-bot](https://ghcr.io/matrixgpt/matrix-chatgpt-bot) | ❌ | Accessing ChatGPT via your favourite Matrix client |
| [mautrix-facebook](configuring-playbook-bridge-mautrix-facebook.md) | [mautrix/facebook](https://mau.dev/mautrix/facebook/container_registry) | ❌ | Bridge to [Facebook](https://facebook.com/) |
| [mautrix-instagram](configuring-playbook-bridge-mautrix-instagram.md) | [mautrix/instagram](https://mau.dev/mautrix/instagram/container_registry) | ❌ | Bridge to [Instagram](https://instagram.com/) |
| [mx-puppet-discord](configuring-playbook-bridge-mx-puppet-discord.md) | [mx-puppet/discord/mx-puppet-discord](https://gitlab.com/mx-puppet/discord/mx-puppet-discord/container_registry) | ❌ | Bridge to [Discord](https://discordapp.com/) |
| [mx-puppet-instagram](configuring-playbook-bridge-mx-puppet-instagram.md) | [sorunome/mx-puppet-instagram](https://hub.docker.com/r/sorunome/mx-puppet-instagram) | ❌ | Bridge for Instagram-DMs ([Instagram](https://www.instagram.com/)) |
| [mx-puppet-slack](configuring-playbook-bridge-mx-puppet-slack.md) | [mx-puppet/slack/mx-puppet-slack](https://gitlab.com/mx-puppet/slack/mx-puppet-slack/container_registry) | ❌ | Bridge to [Slack](https://slack.com) |
| [mx-puppet-twitter](configuring-playbook-bridge-mx-puppet-twitter.md) | [sorunome/mx-puppet-twitter](https://hub.docker.com/r/sorunome/mx-puppet-twitter) | ❌ | Bridge for Twitter-DMs ([Twitter](https://twitter.com/)) |
