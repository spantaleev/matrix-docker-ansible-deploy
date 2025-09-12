[![Support room on Matrix](https://img.shields.io/matrix/matrix-docker-ansible-deploy:devture.com.svg?label=%23matrix-docker-ansible-deploy%3Adevture.com&logo=matrix&style=for-the-badge&server_fqdn=matrix.devture.com&fetchMode=summary)](https://matrix.to/#/#matrix-docker-ansible-deploy:devture.com) [![donate](https://liberapay.com/assets/widgets/donate.svg)](https://liberapay.com/s.pantaleev/donate) [![REUSE status](https://api.reuse.software/badge/github.com/spantaleev/matrix-docker-ansible-deploy)](https://api.reuse.software/info/github.com/spantaleev/matrix-docker-ansible-deploy)

# Matrix (An open network for secure, decentralized communication) server setup using Ansible and Docker

## 🎯 Purpose

This [Ansible](https://www.ansible.com/) playbook is meant to help you run your own [Matrix](http://matrix.org/) homeserver, along with the [various services](#supported-services) related to that.

That is, it lets you join the Matrix network using your own user ID like `@alice:example.com`, all hosted on your own server (see [prerequisites](docs/prerequisites.md)).

We run all [supported services](#-supported-services) in [Docker](https://www.docker.com/) containers (see [the container images we use](docs/container-images.md)), which lets us have a predictable and up-to-date setup, across multiple supported distros (see [prerequisites](docs/prerequisites.md)) and [architectures](docs/alternative-architectures.md) (x86/amd64 being recommended).

Installation (upgrades) and some maintenance tasks are automated using [Ansible](https://www.ansible.com/) (see [our Ansible guide](docs/ansible.md)).

## ☁ Self-hosting or Managed / SaaS

This Ansible playbook tries to make self-hosting and maintaining a Matrix server fairly easy (see [Getting started](#-getting-started)). Still, running any service smoothly requires knowledge, time and effort.

If you like the [FOSS](https://en.wikipedia.org/wiki/Free_and_open-source_software) spirit of this Ansible playbook, but prefer to put the responsibility on someone else, you can also [get a managed Matrix server from etke.cc](https://etke.cc?utm_source=github&utm_medium=readme&utm_campaign=mdad) (both hosting and on-premises) - a service built on top of this Ansible playbook but with [additional components](https://etke.cc/help/extras/?utm_source=github&utm_medium=readme&utm_campaign=mdad) and [services](https://etke.cc/services/?utm_source=github&utm_medium=readme&utm_campaign=mdad) which all help you run a Matrix server with ease. Be advised that etke.cc operates on a subscription-based approach and there is no "just set up my server once and be done with it" option.

## 🚀 Getting started

We have detailed documentation in the [docs/](./docs) directory - see the Table of Contents in the [documentation README](./docs/README.md).

While the [list of supported services](#-supported-services) and documentation is very extensive, you don't need to read through everything. We recommend:

- Starting with the basics. You can always add/remove or tweak services later on.

- Following our installation guide. There are two guides available for beginners and advanced users:

    - ⚡ **[Quick start](./docs/quick-start.md) (for beginners)**: this is recommended for those who do not have an existing Matrix server and want to start quickly with "opinionated defaults".

    - **Full installation guide (for advanced users)**: if you need to import an existing Matrix server's data into the new server or want to learn more while setting up the server, follow this guide by starting with the **[Prerequisites](./docs/prerequisites.md)** documentation page.

If you experience an issue on configuring the playbook, setting up your server, maintaining services on it, etc., please take a look at our [FAQ](./docs/faq.md). If you cannot find an answer to your question, feel free to ask for [help and support](#-support).

## ✔ Supported services

Using this playbook, you can get the following list of services configured on your server. Basically, this playbook aims to get you up-and-running with all the necessities around Matrix, without you having to do anything else.

**Notes**:

- The list below is exhaustive. It includes optional or even some advanced components that you will most likely not need. Sticking with the defaults (which install a subset of the above components) is the best choice, especially for a new installation. You can always re-run the playbook later to add or remove components.

- Deprecated or unmaintained services are not listed. You can find documentations for them [here](docs/configuring-playbook.md#deprecated--unmaintained--removed-services).

### Homeserver

The homeserver is the backbone of your Matrix system. Choose one from the following list.

| Name | Default? | Description | Documentation |
| ---- | -------- | ----------- | ------------- |
| [Synapse](https://github.com/element-hq/synapse) | ✅ | Storing your data and managing your presence in the [Matrix](http://matrix.org/) network | [Link](docs/configuring-playbook-synapse.md) |
| [Conduit](https://conduit.rs) | ❌ | Storing your data and managing your presence in the [Matrix](http://matrix.org/) network. Conduit is a lightweight open-source server implementation of the Matrix Specification with a focus on easy setup and low system requirements | [Link](docs/configuring-playbook-conduit.md) |
| [conduwuit](https://conduwuit.puppyirl.gay/) | ❌ | Storing your data and managing your presence in the [Matrix](http://matrix.org/) network. conduwuit is a fork of Conduit. | [Link](docs/configuring-playbook-conduwuit.md) |
| [continuwuity](https://continuwuity.org) | ❌ | Storing your data and managing your presence in the [Matrix](http://matrix.org/) network. continuwuity is a continuation of conduwuit. | [Link](docs/configuring-playbook-continuwuity.md) |
| [Dendrite](https://github.com/element-hq/dendrite) | ❌ | Storing your data and managing your presence in the [Matrix](http://matrix.org/) network. Dendrite is a second-generation Matrix homeserver written in Go, an alternative to Synapse. | [Link](docs/configuring-playbook-dendrite.md) |

### Clients

Web clients for Matrix that you can host on your own domains.

| Name | Default? | Description | Documentation |
| ---- | -------- | ----------- | ------------- |
| [Element Web](https://github.com/element-hq/element-web) | ✅ | Default Matrix web client, configured to connect to your own Synapse server | [Link](docs/configuring-playbook-client-element-web.md) |
| [Hydrogen](https://github.com/element-hq/hydrogen-web) | ❌ | Lightweight Matrix client with legacy and mobile browser support | [Link](docs/configuring-playbook-client-hydrogen.md) |
| [Cinny](https://github.com/ajbura/cinny) |  ❌ | Simple, elegant and secure web client | [Link](docs/configuring-playbook-client-cinny.md) |
| [SchildiChat Web](https://schildi.chat/) | ❌ | Based on Element Web, with a more traditional instant messaging experience | [Link](docs/configuring-playbook-client-schildichat-web.md) |
| [FluffyChat Web](https://fluffychat.im/) | ❌ | The cutest messenger in Matrix | [Link](docs/configuring-playbook-client-fluffychat-web.md) |

### Server Components

Services that run on the server to make the various parts of your installation work.

| Name | Default? | Description | Documentation |
| ---- | -------- | ----------- | ------------- |
| [PostgreSQL](https://www.postgresql.org/)| ✅ | Database for Synapse. [Using an external PostgreSQL server](docs/configuring-playbook-external-postgres.md) is also possible. | [Link](docs/configuring-playbook-external-postgres.md) |
| [coturn](https://github.com/coturn/coturn) | ✅ | STUN/TURN server for WebRTC audio/video calls | [Link](docs/configuring-playbook-turn.md) |
| [Traefik](https://doc.traefik.io/traefik/) | ✅ | Web server, listening on ports 80, 443 and 8448 - standing in front of all the other services. [Using your own webserver](docs/configuring-playbook-own-webserver.md) is also possible. | [Link](docs/configuring-playbook-traefik.md) |
| [Let's Encrypt](https://letsencrypt.org/) | ✅ | Free SSL certificate, which secures the connection to all components | [Link](docs/configuring-playbook-ssl-certificates.md) |
| [Exim](https://www.exim.org/) | ✅ | Mail server, through which all Matrix services send outgoing email (can be configured to relay through another SMTP server) | [Link](docs/configuring-playbook-email.md) |
| [ma1sd](https://github.com/ma1uta/ma1sd) | ❌ | Matrix Identity Server | [Link](docs/configuring-playbook-ma1sd.md)
| [ddclient](https://github.com/linuxserver/docker-ddclient) | ❌ | Dynamic DNS | [Link](docs/configuring-playbook-dynamic-dns.md) |
| [LiveKit Server](https://github.com/livekit/livekit) | ❌ | WebRTC server for audio/video calls | [Link](docs/configuring-playbook-livekit-server.md) |
| [Livekit JWT Service](https://github.com/livekit/livekit-jwt-service) | ❌ | JWT service for integrating [Element Call](./configuring-playbook-element-call.md) with [LiveKit Server](./configuring-playbook-livekit-server.md) | [Link](docs/configuring-playbook-livekit-jwt-service.md) |

### Authentication

Extend and modify how users are authenticated on your homeserver.

| Name | Default? | Description | Documentation |
| ---- | -------- | ----------- | ------------- |
| [matrix-synapse-rest-auth](https://github.com/ma1uta/matrix-synapse-rest-password-provider) (advanced) | ❌ | REST authentication password provider module | [Link](docs/configuring-playbook-rest-auth.md) |
|[matrix-synapse-shared-secret-auth](https://github.com/devture/matrix-synapse-shared-secret-auth) (advanced) | ❌ | Password provider module | [Link](docs/configuring-playbook-shared-secret-auth.md) |
| [matrix-synapse-ldap3](https://github.com/matrix-org/matrix-synapse-ldap3) (advanced) | ❌ | LDAP Auth password provider module | [Link](docs/configuring-playbook-ldap-auth.md) |
| [matrix-ldap-registration-proxy](https://gitlab.com/activism.international/matrix_ldap_registration_proxy) (advanced) | ❌ | Proxy that handles Matrix registration requests and forwards them to LDAP | [Link](docs/configuring-playbook-matrix-ldap-registration-proxy.md) |
| [matrix-registration](https://github.com/ZerataX/matrix-registration) | ❌ | Simple python application to have a token based Matrix registration | [Link](docs/configuring-playbook-matrix-registration.md) |
| [Matrix User Verification Service](https://github.com/matrix-org/matrix-user-verification-service) | ❌ | Service to verify details of a user based on an Open ID token | [Link](docs/configuring-playbook-user-verification-service.md) |
| [synapse-simple-antispam](https://github.com/t2bot/synapse-simple-antispam) (advanced) | ❌ | Spam checker module | [Link](docs/configuring-playbook-synapse-simple-antispam.md) |

### File Storage

Use alternative file storage to the default `media_store` folder.

| Name | Default? | Description | Documentation |
| ---- | -------- | ----------- | ------------- |
| [Goofys](https://github.com/kahing/goofys) | ❌ | [Amazon S3](https://aws.amazon.com/s3/) (or other S3-compatible object store) storage for Synapse's content repository (`media_store`) files | [Link](docs/configuring-playbook-s3-goofys.md) |
| [synapse-s3-storage-provider](https://github.com/matrix-org/synapse-s3-storage-provider) | ❌ | [Amazon S3](https://aws.amazon.com/s3/) (or other S3-compatible object store) storage for Synapse's content repository (`media_store`) files | [Link](docs/configuring-playbook-s3.md) |
| [matrix-media-repo](https://github.com/turt2live/matrix-media-repo) | ❌ | Highly customizable multi-domain media repository for Matrix. Intended for medium to large deployments, this media repo de-duplicates media while being fully compliant with the specification. | [Link](docs/configuring-playbook-matrix-media-repo.md) |

### Bridges

Bridges can be used to connect your Matrix installation with third-party communication networks.

| Name | Default? | Description | Documentation |
| ---- | -------- | ----------- | ------------- |
| [mautrix-discord](https://github.com/mautrix/discord) | ❌ | Bridge to [Discord](https://discord.com/) | [Link](docs/configuring-playbook-bridge-mautrix-discord.md) |
| [mautrix-slack](https://github.com/mautrix/slack) | ❌ | Bridge to [Slack](https://slack.com/) | [Link](docs/configuring-playbook-bridge-mautrix-slack.md) |
| [mautrix-telegram](https://github.com/mautrix/telegram) | ❌ | Bridge to [Telegram](https://telegram.org/) | [Link](docs/configuring-playbook-bridge-mautrix-telegram.md) |
| [mautrix-gmessages](https://github.com/mautrix/gmessages) | ❌ | Bridge to [Google Messages](https://messages.google.com/) | [Link](docs/configuring-playbook-bridge-mautrix-gmessages.md) |
| [mautrix-whatsapp](https://github.com/mautrix/whatsapp) | ❌ | Bridge to [WhatsApp](https://www.whatsapp.com/) | [Link](docs/configuring-playbook-bridge-mautrix-whatsapp.md) |
| [mautrix-wsproxy](https://github.com/mautrix/wsproxy) | ❌ | Bridge to Android SMS or Apple iMessage | [Link](docs/configuring-playbook-bridge-mautrix-wsproxy.md) |
| [mautrix-bluesky](https://github.com/mautrix/bluesky) | ❌ | Bridge to [Bluesky](https://bsky.social/) | [Link](docs/configuring-playbook-bridge-mautrix-bluesky.md) |
| [mautrix-twitter](https://github.com/mautrix/twitter) | ❌ | Bridge to [Twitter](https://twitter.com/) | [Link](docs/configuring-playbook-bridge-mautrix-twitter.md) |
| [mautrix-googlechat](https://github.com/mautrix/googlechat) | ❌ | Bridge to [Google Chat](https://en.wikipedia.org/wiki/Google_Chat) | [Link](docs/configuring-playbook-bridge-mautrix-googlechat.md) |
| [mautrix-meta](https://github.com/mautrix/instagram) | ❌ | Bridge to [Messenger](https://messenger.com/) and [Instagram](https://instagram.com/) | Link for [Messenger](docs/configuring-playbook-bridge-mautrix-meta-messenger.md) / [Instagram](docs/configuring-playbook-bridge-mautrix-meta-instagram.md) |
| [mautrix-signal](https://github.com/mautrix/signal) | ❌ | Bridge to [Signal](https://www.signal.org/) | [Link](docs/configuring-playbook-bridge-mautrix-signal.md) |
| [beeper-linkedin](https://github.com/beeper/linkedin) | ❌ | Bridge to [LinkedIn](https://www.linkedin.com/) | [Link](docs/configuring-playbook-bridge-beeper-linkedin.md) |
| [matrix-appservice-irc](https://github.com/matrix-org/matrix-appservice-irc) | ❌ | Bridge to [IRC](https://wikipedia.org/wiki/Internet_Relay_Chat) | [Link](docs/configuring-playbook-bridge-appservice-irc.md) |
| [matrix-appservice-kakaotalk](https://src.miscworks.net/fair/matrix-appservice-kakaotalk) | ❌ | Bridge to [Kakaotalk](https://www.kakaocorp.com/page/service/service/KakaoTalk?lang=ENG) | [Link](docs/configuring-playbook-bridge-appservice-kakaotalk.md) |
| [matrix-appservice-discord](https://github.com/matrix-org/matrix-appservice-discord) | ❌ | Bridge to [Discord](https://discordapp.com/) | [Link](docs/configuring-playbook-bridge-appservice-discord.md) |
| [matrix-appservice-slack](https://github.com/matrix-org/matrix-appservice-slack) | ❌ | Bridge to [Slack](https://slack.com/) | [Link](docs/configuring-playbook-bridge-appservice-slack.md) |
| [matrix-hookshot](https://github.com/matrix-org/matrix-hookshot) | ❌ | Bridge for generic webhooks and multiple project management services, such as GitHub, GitLab, Figma, and Jira in particular | [Link](docs/configuring-playbook-bridge-hookshot.md) |
| [matrix-sms-bridge](https://github.com/benkuly/matrix-sms-bridge) | ❌ | Bridge to SMS | [Link](docs/configuring-playbook-bridge-matrix-bridge-sms.md) |
| [matrix-wechat](https://github.com/duo/matrix-wechat) | ❌ | Bridge to [WeChat](https://www.wechat.com/) | [Link](docs/configuring-playbook-bridge-wechat.md) |
| [Heisenbridge](https://github.com/hifi/heisenbridge) | ❌ | Bouncer-style bridge to [IRC](https://wikipedia.org/wiki/Internet_Relay_Chat) | [Link](docs/configuring-playbook-bridge-heisenbridge.md) |
| [go-skype-bridge](https://github.com/kelaresg/go-skype-bridge) | ❌ | Bridge to [Skype](https://www.skype.com) | [Link](docs/configuring-playbook-bridge-go-skype-bridge.md) |
| [mx-puppet-slack](https://gitlab.com/mx-puppet/slack/mx-puppet-slack) | ❌ | Bridge to [Slack](https://slack.com) | [Link](docs/configuring-playbook-bridge-mx-puppet-slack.md) |
| [mx-puppet-instagram](https://github.com/Sorunome/mx-puppet-instagram) | ❌ | Bridge for Instagram-DMs ([Instagram](https://www.instagram.com/)) | [Link](docs/configuring-playbook-bridge-mx-puppet-instagram.md) |
| [mx-puppet-twitter](https://github.com/Sorunome/mx-puppet-twitter) | ❌ | Bridge for Twitter-DMs ([Twitter](https://twitter.com/)) | [Link](docs/configuring-playbook-bridge-mx-puppet-twitter.md) |
| [mx-puppet-discord](https://gitlab.com/mx-puppet/discord/mx-puppet-discord) | ❌ | Bridge to [Discord](https://discordapp.com/) | [Link](docs/configuring-playbook-bridge-mx-puppet-discord.md) |
| [mx-puppet-groupme](https://gitlab.com/xangelix-pub/matrix/mx-puppet-groupme) | ❌ | Bridge to [GroupMe](https://groupme.com/) | [Link](docs/configuring-playbook-bridge-mx-puppet-groupme.md) |
| [mx-puppet-steam](https://github.com/icewind1991/mx-puppet-steam) | ❌ | Bridge to [Steam](https://steamapp.com/) | [Link](docs/configuring-playbook-bridge-mx-puppet-steam.md) |
| [matrix-steam-bridge](https://github.com/jasonlaguidice/matrix-steam-bridge) | ❌ | Bridge to [Steam](https://steampowered.com/) | [Link](docs/configuring-playbook-bridge-steam.md) |
| [Postmoogle](https://github.com/etkecc/postmoogle) | ❌ | Email to Matrix bridge | [Link](docs/configuring-playbook-bridge-postmoogle.md) |

### Bots

Bots provide various additional functionality to your installation.

| Name | Default? | Description | Documentation |
| ---- | -------- | ----------- | ------------- |
| [baibot](https://github.com/etkecc/baibot) | ❌ | Bot that exposes the power of [AI](https://en.wikipedia.org/wiki/Artificial_intelligence) / [Large Language Models](https://en.wikipedia.org/wiki/Large_language_model) to you | [Link](docs/configuring-playbook-bot-baibot.md) |
| [matrix-reminder-bot](https://github.com/anoadragon453/matrix-reminder-bot) | ❌ | Bot for scheduling one-off & recurring reminders and alarms | [Link](docs/configuring-playbook-bot-matrix-reminder-bot.md) |
| [matrix-registration-bot](https://github.com/moan0s/matrix-registration-bot) | ❌ | Bot for invitations by creating and managing registration tokens | [Link](docs/configuring-playbook-bot-matrix-registration-bot.md) |
| [maubot](https://github.com/maubot/maubot) | ❌ | Plugin-based Matrix bot system | [Link](docs/configuring-playbook-bot-maubot.md) |
| [Honoroit](https://github.com/etkecc/honoroit) | ❌ | Helpdesk bot | [Link](docs/configuring-playbook-bot-honoroit.md) |
| [Mjolnir](https://github.com/matrix-org/mjolnir) | ❌ | Moderation tool for Matrix | [Link](docs/configuring-playbook-bot-mjolnir.md) |
| [Draupnir](https://github.com/the-draupnir-project/Draupnir) | ❌ | Moderation tool for Matrix (Fork of Mjolnir) | [Link](docs/configuring-playbook-bot-draupnir.md) (for [appservice mode](docs/configuring-playbook-appservice-draupnir-for-all.md))|
| [Buscarron](https://github.com/etkecc/buscarron) | ❌ | Web forms (HTTP POST) to Matrix | [Link](docs/configuring-playbook-bot-buscarron.md) |

### Administration

Services that help you in administrating and monitoring your Matrix installation.

| Name | Default? | Description | Documentation |
| ---- | -------- | ----------- | ------------- |
| [matrix-alertmanager-receiver](https://github.com/metio/matrix-alertmanager-receiver) | ❌ | Prometheus' [Alertmanager](https://prometheus.io/docs/alerting/latest/alertmanager/) client | [Link](docs/configuring-playbook-alertmanager-receiver.md) |
| [Matrix Authentication Service](https://github.com/element-hq/matrix-authentication-service/) | ❌ | OAuth 2.0 and OpenID Provider server | [Link](docs/configuring-playbook-matrix-authentication-service.md) |
| [synapse-admin](https://github.com/etkecc/synapse-admin) | ❌ | Web UI tool for administrating users and rooms on your Matrix server | [Link](docs/configuring-playbook-synapse-admin.md) |
| Metrics and Graphs | ❌ | Consists of the [Prometheus](https://prometheus.io) time-series database server, the Prometheus [node-exporter](https://prometheus.io/docs/guides/node-exporter/) host metrics exporter, and the [Grafana](https://grafana.com/) web UI, with [prometheus-nginxlog-exporter](https://github.com/martin-helmich/prometheus-nginxlog-exporter/) being available too | [Link](docs/configuring-playbook-prometheus-grafana.md) (for [prometheus-nginxlog-exporter](docs/configuring-playbook-prometheus-grafana.md#enable-metrics-and-graphs-for-nginx-logs-optional)) |
| [Borg](https://borgbackup.org) | ❌ | Backups | [Link](docs/configuring-playbook-backup-borg.md) |
| [rageshake](https://github.com/matrix-org/rageshake) | ❌ | Bug report server | [Link](docs/configuring-playbook-rageshake.md) |
| [synapse-usage-exporter](https://github.com/loelkes/synapse-usage-exporter) | ❌ | Export the usage statistics of a Synapse homeserver to be scraped by Prometheus. | [Link](docs/configuring-playbook-synapse-usage-exporter.md) |

### Misc

Various services that don't fit any other categories.

| Name | Default? | Description | Documentation |
| ---- | -------- | ----------- | ------------- |
| [sliding-sync](https://github.com/matrix-org/sliding-sync)| ❌ | (Superseded by Simplified Sliding Sync integrated into Synapse > `1.114` and Conduit > `0.6.0`) Sliding Sync support for clients which require it (e.g. old Element X versions before Simplified Sliding Sync was developed) | [Link](docs/configuring-playbook-sliding-sync-proxy.md) |
| [synapse_auto_accept_invite](https://github.com/matrix-org/synapse-auto-accept-invite) | ❌ | Synapse module to automatically accept invites | [Link](docs/configuring-playbook-synapse-auto-accept-invite.md) |
| [synapse_auto_compressor](https://github.com/matrix-org/rust-synapse-compress-state/#automated-tool-synapse_auto_compressor) | ❌ | Cli tool that automatically compresses `state_groups` database table in background | [Link](docs/configuring-playbook-synapse-auto-compressor.md) |
| [Matrix Corporal](https://github.com/devture/matrix-corporal) (advanced) | ❌ | Reconciliator and gateway for a managed Matrix server | [Link](docs/configuring-playbook-matrix-corporal.md) |
| [Etherpad](https://etherpad.org) | ❌ | Open source collaborative text editor | [Link](docs/configuring-playbook-etherpad.md) |
| [Jitsi](https://jitsi.org/) | ❌ | Open source video-conferencing platform | [Link](docs/configuring-playbook-jitsi.md) |
| [Cactus Comments](https://cactus.chat) | ❌ | Federated comment system built on Matrix | [Link](docs/configuring-playbook-cactus-comments.md) |
| [Pantalaimon](https://github.com/matrix-org/pantalaimon) | ❌ | E2EE aware proxy daemon | [Link](docs/configuring-playbook-pantalaimon.md) |
| [Sygnal](https://github.com/matrix-org/sygnal) | ❌ | Push gateway | [Link](docs/configuring-playbook-sygnal.md) |
| [ntfy](https://ntfy.sh) | ❌ | Push notifications server | [Link](docs/configuring-playbook-ntfy.md) |
| [Element Call](https://github.com/element-hq/element-call) | ❌ | A native Matrix video conferencing application | [Link](docs/configuring-playbook-element-call.md) |

## 🆕 Changes

This playbook evolves over time, sometimes with backward-incompatible changes.

When updating the playbook, refer to [the changelog](CHANGELOG.md) to catch up with what's new.

## 🆘 Support

- Matrix room: [#matrix-docker-ansible-deploy:devture.com](https://matrix.to/#/#matrix-docker-ansible-deploy:devture.com)

- IRC channel: `#matrix-docker-ansible-deploy` on the [Libera Chat](https://libera.chat/) IRC network (irc.libera.chat:6697)

- GitHub issues: [spantaleev/matrix-docker-ansible-deploy/issues](https://github.com/spantaleev/matrix-docker-ansible-deploy/issues)

## 🌐 Translation

See the [i18n/README.md](i18n/README.md) file for more information about translation.

Translations are still work in progress.

## 🤝 Related

You may also be interested in [mash-playbook](https://github.com/mother-of-all-self-hosting/mash-playbook) - another Ansible playbook for self-hosting non-Matrix services (see its [List of supported services](https://github.com/mother-of-all-self-hosting/mash-playbook/blob/main/docs/supported-services.md)).

mash-playbook also makes use of [Traefik](./docs/configuring-playbook-traefik.md) as its reverse-proxy, so with minor [interoperability adjustments](https://github.com/mother-of-all-self-hosting/mash-playbook/blob/main/docs/interoperability.md), you can make matrix-docker-ansible-deploy and mash-playbook co-exist and host Matrix and non-Matrix services on the same server.
