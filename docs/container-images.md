# Container images used by the playbook

This page summarizes the container ([Docker](https://www.docker.com/)) images used by the playbook when setting up your server.

We try to stick to official images (provided by their respective projects) as much as possible.


## Homeserver

| Service | Container image | Default? | Description |
| ------- | --------------- | -------- | ----------- |
| [Synapse](configuring-playbook-synapse.md) | [element-hq/synapse](https://ghcr.io/element-hq/synapse) | ✓ | Storing your data and managing your presence in the [Matrix](http://matrix.org/) network |
| [Conduit](configuring-playbook-conduit.md) | [matrixconduit/matrix-conduit](https://hub.docker.com/r/matrixconduit/matrix-conduit) | x | Storing your data and managing your presence in the [Matrix](http://matrix.org/) network. Conduit is a lightweight open-source server implementation of the Matrix Specification with a focus on easy setup and low system requirements |
| [Dendrite](configuring-playbook-dendrite.md) | [matrixdotorg/dendrite-monolith](https://hub.docker.com/r/matrixdotorg/dendrite-monolith/) | x | Storing your data and managing your presence in the [Matrix](http://matrix.org/) network. Dendrite is a second-generation Matrix homeserver written in Go, an alternative to Synapse. |

## Clients

Web clients for Matrix that you can host on your own domains.

| Service | Container image | Default? | Description |
| ------- | --------------- | -------- | ----------- |
| [Element Web](configuring-playbook-client-element-web.md) | [vectorim/element-web](https://hub.docker.com/r/vectorim/element-web/) | ✓ | Default Matrix web client, configured to connect to your own Synapse server |
| [Hydrogen](configuring-playbook-client-hydrogen.md) | [element-hq/hydrogen-web](https://ghcr.io/element-hq/hydrogen-web) | x | Lightweight Matrix client with legacy and mobile browser support |
| [Cinny](configuring-playbook-client-cinny.md) | [ajbura/cinny](https://hub.docker.com/r/ajbura/cinny) | x | Simple, elegant and secure web client |
| [SchildiChat Web](configuring-playbook-client-schildichat-web.md) | [etke.cc/schildichat-web](https://ghcr.io/etkecc/schildichat-web) | x | Based on Element Web, with a more traditional instant messaging experience |

## Server Components

Services that run on the server to make the various parts of your installation work.

| Service | Container image | Default? | Description |
| ------- | --------------- | -------- | ----------- |
| [PostgreSQL](configuring-playbook-external-postgres.md) | [postgres](https://hub.docker.com/_/postgres/) | ✓ | Database for Synapse. [Using an external PostgreSQL server](configuring-playbook-external-postgres.md) is also possible. |
| [Coturn](configuring-playbook-turn.md) | [coturn/coturn](https://hub.docker.com/r/coturn/coturn/) | ✓ | STUN/TURN server for WebRTC audio/video calls |
| [Traefik](configuring-playbook-traefik.md) | [Traefik](https://hub.docker.com/_/traefik/) | ✓ | Web server, listening on ports 80, 443 and 8448 - standing in front of all the other services. Using your own webserver [is possible](configuring-playbook-own-webserver.md) |
| [Let's Encrypt](configuring-playbook-ssl-certificates.md) | [certbot/certbot](https://hub.docker.com/r/certbot/certbot/) | ✓ | The [certbot](https://certbot.eff.org/) tool for obtaining SSL certificates from [Let's Encrypt](https://letsencrypt.org/) |
| [Exim](configuring-playbook-email.md) | [devture/exim-relay](https://hub.docker.com/r/devture/exim-relay/) | ✓ | Mail server, through which all Matrix services send outgoing email (can be configured to relay through another SMTP server) |
| [ma1sd](configuring-playbook-ma1sd.md) | [ma1uta/ma1sd](https://hub.docker.com/r/ma1uta/ma1sd/) | x | Matrix Identity Server |
| [ddclient](configuring-playbook-dynamic-dns.md) | [linuxserver/ddclient](https://hub.docker.com/r/linuxserver/ddclient) | x | Update dynamic DNS entries for accounts on Dynamic DNS Network Service Provider |

## Authentication

Extend and modify how users are authenticated on your homeserver.

| Service | Container image | Default? | Description |
| ------- | --------------- | -------- | ----------- |
| [matrix-synapse-rest-auth](configuring-playbook-rest-auth.md) | (N/A) | x | REST authentication password provider module |
| [matrix-synapse-shared-secret-auth](configuring-playbook-shared-secret-auth.md) | (N/A) | x | Password provider module |
| [matrix-synapse-ldap3](configuring-playbook-ldap-auth.md) (advanced) | (N/A) | x | LDAP Auth password provider module |
| [matrix-ldap-registration-proxy](configuring-playbook-matrix-ldap-registration-proxy.md) | [activism.international/matrix_ldap_registration_proxy](https://gitlab.com/activism.international/matrix_ldap_registration_proxy/container_registry) | x | A proxy that handles Matrix registration requests and forwards them to LDAP. |
| [matrix-registration](configuring-playbook-matrix-registration.md) | [zeratax/matrix-registration](https://hub.docker.com/r/devture/zeratax-matrix-registration/) | x | A simple python application to have a token based Matrix registration |
| [Matrix User Verification Service](configuring-playbook-user-verification-service.md) (UVS) | [matrixdotorg/matrix-user-verification-service](https://hub.docker.com/r/atrixdotorg/matrix-user-verification-service) | x | Service to verify details of a user based on an Open ID token |
| [synapse-simple-antispam](configuring-playbook-synapse-simple-antispam.md) (advanced) | (N/A) | x | A spam checker module |

## File Storage

Use alternative file storage to the default `media_store` folder.

| Service | Container image | Default? | Description |
| ------- | --------------- | -------- | ----------- |
| [Goofys](configuring-playbook-s3-goofys.md) | [ewoutp/goofys](https://hub.docker.com/r/ewoutp/goofys/) | x | [Amazon S3](https://aws.amazon.com/s3/) (or other S3-compatible object store) storage for Synapse's content repository (`media_store`) files |
| [synapse-s3-storage-provider](configuring-playbook-s3.md) | (N/A) | x | [Amazon S3](https://aws.amazon.com/s3/) (or other S3-compatible object store) storage for Synapse's content repository (`media_store`) files |
| [matrix-media-repo](configuring-playbook-matrix-media-repo.md) | [t2bot/matrix-media-repo](https://ghcr.io/t2bot/matrix-media-repo) | x | matrix-media-repo is a highly customizable multi-domain media repository for Matrix. Intended for medium to large deployments, this media repo de-duplicates media while being fully compliant with the specification. |

# Bridges

Bridges can be used to connect your Matrix installation with third-party communication networks.

| Service | Container image | Default? | Description |
| ------- | --------------- | -------- | ----------- |
| [mautrix-discord](configuring-playbook-bridge-mautrix-discord.md) | [mautrix/discord](https://mau.dev/mautrix/discord/container_registry) | x | Bridge to [Discord](https://discord.com/) |
| [mautrix-slack](configuring-playbook-bridge-mautrix-slack.md) | [mautrix/slack](https://mau.dev/mautrix/slack/container_registry) | x | Bridge to [Slack](https://slack.com/) |
| [mautrix-telegram](configuring-playbook-bridge-mautrix-telegram.md) | [mautrix/telegram](https://mau.dev/mautrix/telegram/container_registry) | x | Bridge to [Telegram](https://telegram.org/) |
| [mautrix-gmessages](configuring-playbook-bridge-mautrix-gmessages.md) | [mautrix/gmessages](https://mau.dev/mautrix/gmessages/container_registry) | x | Bridge to [Google Messages](https://messages.google.com/) |
| [mautrix-whatsapp](configuring-playbook-bridge-mautrix-whatsapp.md) | [mautrix/whatsapp](https://mau.dev/mautrix/whatsapp/container_registry) | x | Bridge to [WhatsApp](https://www.whatsapp.com/) |
| [mautrix-wsproxy](configuring-playbook-bridge-mautrix-wsproxy.md) | [mautrix/wsproxy](https://mau.dev/mautrix/wsproxy/container_registry) | x | Bridge to Android SMS or Apple iMessage |
| [mautrix-twitter](configuring-playbook-bridge-mautrix-twitter.md) | [mautrix/twitter](https://mau.dev/mautrix/twitter/container_registry) | x | Bridge to [Twitter](https://twitter.com/) |
| [mautrix-googlechat](configuring-playbook-bridge-mautrix-googlechat.md) | [mautrix/googlechat](https://mau.dev/mautrix/googlechat/container_registry) | x | Bridge to [Google Chat](https://en.wikipedia.org/wiki/Google_Chat) |
| mautrix-meta (for [Messenger](configuring-playbook-bridge-mautrix-meta-messenger.md) and [Instagram](configuring-playbook-bridge-mautrix-meta-instagram.md)) | [mautrix/meta](https://mau.dev/mautrix/meta/container_registry) | x | Bridge to [Messenger](https://messenger.com/) and [Instagram](https://instagram.com/) |
| [mautrix-signal](configuring-playbook-bridge-mautrix-signal.md) | [mautrix/signal](https://mau.dev/mautrix/signal/container_registry) | x | Bridge to [Signal](https://www.signal.org/) |
| [beeper-linkedin](configuring-playbook-bridge-beeper-linkedin.md) | [beeper/linkedin](https://ghcr.io/beeper/linkedin) | x | Bridge to [LinkedIn](https://www.linkedin.com/) |
| [matrix-appservice-irc](configuring-playbook-bridge-appservice-irc.md) | [matrixdotorg/matrix-appservice-irc](https://hub.docker.com/r/matrixdotorg/matrix-appservice-irc) | x | Bridge to [IRC](https://wikipedia.org/wiki/Internet_Relay_Chat) |
| [matrix-appservice-kakaotalk](configuring-playbook-bridge-appservice-kakaotalk.md) | Self-building | x | Bridge to [Kakaotalk](https://www.kakaocorp.com/page/service/service/KakaoTalk?lang=ENG) |
| [matrix-appservice-discord](configuring-playbook-bridge-appservice-discord.md) | [matrix-org/matrix-appservice-discord](https://ghcr.io/matrix-org/matrix-appservice-discord) | x | Bridge to [Discord](https://discordapp.com/) |
| [matrix-appservice-slack](configuring-playbook-bridge-appservice-slack.md) | [matrixdotorg/matrix-appservice-slack](https://hub.docker.com/r/matrixdotorg/matrix-appservice-slack) | x | Bridge to [Slack](https://slack.com/) |
| [matrix-hookshot](configuring-playbook-bridge-hookshot.md) | [halfshot/matrix-hookshot](https://hub.docker.com/r/halfshot/matrix-hookshot) | x | Bridge for generic webhooks and multiple project management services, such as GitHub, GitLab, Figma, and Jira in particular |
| [matrix-sms-bridge](configuring-playbook-bridge-matrix-bridge-sms.md) | [folivonet/matrix-sms-bridge](https://hub.docker.com/repository/docker/folivonet/matrix-sms-bridge) | x | Bridge to SMS |
| [matrix-wechat](configuring-playbook-bridge-wechat.md) | [lxduo/matrix-wechat](https://hub.docker.com/r/lxduo/matrix-wechat) | x | Bridge to [WeChat](https://www.wechat.com/) |
| [Heisenbridge](configuring-playbook-bridge-heisenbridge.md) | [hif1/heisenbridge](https://hub.docker.com/r/hif1/heisenbridge) | x | Bouncer-style bridge to [IRC](https://wikipedia.org/wiki/Internet_Relay_Chat) |
| [go-skype-bridge](configuring-playbook-bridge-go-skype-bridge.md) | [nodefyme/go-skype-bridge](https://hub.docker.com/r/nodefyme/go-skype-bridge) | x | Bridge to [Skype](https://www.skype.com) |
| [mx-puppet-slack](configuring-playbook-bridge-mx-puppet-slack.md) | [mx-puppet/slack/mx-puppet-slack](https://gitlab.com/mx-puppet/slack/mx-puppet-slack/container_registry) | x | Bridge to [Slack](https://slack.com) |
| [mx-puppet-instagram](configuring-playbook-bridge-mx-puppet-instagram.md) | [sorunome/mx-puppet-instagram](https://hub.docker.com/r/sorunome/mx-puppet-instagram) | x | Bridge for Instagram-DMs ([Instagram](https://www.instagram.com/)) |
| [mx-puppet-twitter](configuring-playbook-bridge-mx-puppet-twitter.md) | [sorunome/mx-puppet-twitter](https://hub.docker.com/r/sorunome/mx-puppet-twitter) | x | Bridge for Twitter-DMs ([Twitter](https://twitter.com/)) |
| [mx-puppet-discord](configuring-playbook-bridge-mx-puppet-discord.md) | [mx-puppet/discord/mx-puppet-discord](https://gitlab.com/mx-puppet/discord/mx-puppet-discord/container_registry) | x | Bridge to [Discord](https://discordapp.com/) |
| [mx-puppet-groupme](configuring-playbook-bridge-mx-puppet-groupme.md) | [xangelix/mx-puppet-groupme](https://hub.docker.com/r/xangelix/mx-puppet-groupme) | x | Bridge to [GroupMe](https://groupme.com/) |
| [mx-puppet-steam](configuring-playbook-bridge-mx-puppet-steam.md) | [icewind1991/mx-puppet-steam](https://hub.docker.com/r/icewind1991/mx-puppet-steam) | x | Bridge to [Steam](https://steamapp.com/) |
| [Email2Matrix](configuring-playbook-email2matrix.md) | [devture/email2matrix](https://hub.docker.com/r/devture/email2matrix/) | x | Bridge for relaying emails to Matrix rooms |
| [Postmoogle](docs/configuring-playbook-bridge-postmoogle.md) | [etke.cc/postmoogle](https://github.com/etkecc/postmoogle/container_registry) | x | Email to Matrix bridge |

## Bots

Bots provide various additional functionality to your installation.

| Service | Container image | Default? | Description |
| ------- | --------------- | -------- | ----------- |
| [baibot](configuring-playbook-bot-baibot.md) | [etke.cc/baibot](https://ghcr.io/etkecc/baibot) | x | A bot that exposes the power of [AI](https://en.wikipedia.org/wiki/Artificial_intelligence) / [Large Language Models](https://en.wikipedia.org/wiki/Large_language_model) to you |
| [matrix-reminder-bot](configuring-playbook-bot-matrix-reminder-bot.md) | [anoa/matrix-reminder-bot](https://hub.docker.com/r/anoa/matrix-reminder-bot) |  x | Bot for scheduling one-off & recurring reminders and alarms |
| [matrix-registration-bot](configuring-playbook-bot-matrix-registration-bot.md) | [moanos/matrix-registration-bot](https://hub.docker.com/r/moanos/matrix-registration-bot/) | x | Bot for invitations by creating and managing registration tokens |
| [maubot](configuring-playbook-bot-maubot.md) | [dock.mau.dev/maubot/maubot](https://mau.dev/maubot/maubot/container_registry) | x | A plugin-based Matrix bot system |
| [Honoroit](configuring-playbook-bot-honoroit.md) | [etke.cc/honoroit](https://github.com/etkecc/honoroit/container_registry) | x | A helpdesk bot |
| [Mjolnir](configuring-playbook-bot-mjolnir.md) | [matrixdotorg/mjolnir](https://hub.docker.com/r/matrixdotorg/mjolnir) | x | A moderation tool for Matrix |
| [Draupnir](configuring-playbook-bot-draupnir.md) | [gnuxie/draupnir](https://hub.docker.com/r/gnuxie/draupnir) | x | A moderation tool for Matrix (Fork of Mjolnir) |
| [Buscarron](configuring-playbook-bot-buscarron.md) | [etke.cc/buscarron](https://ghcr.io/etkecc/buscarron) | x | Web forms (HTTP POST) to Matrix |

## Administration

Services that help you in administrating and monitoring your Matrix installation.

| Service | Container image | Default? | Description |
| ------- | --------------- | -------- | ----------- |
| [matrix-alertmanager-receiver](configuring-playbook-alertmanager-receiver.md) | [metio/matrix-alertmanager-receiver](https://hub.docker.com/r/metio/matrix-alertmanager-receiver)  | x | Prometheus' [Alertmanager](https://prometheus.io/docs/alerting/latest/alertmanager/) client |
| [Matrix Authentication Service](configuring-playbook-matrix-authentication-service.md) | [element-hq/matrix-authentication-service](https://ghcr.io/element-hq/matrix-authentication-service) | x | OAuth 2.0 and OpenID Provider server |
| [synapse-admin](configuring-playbook-synapse-admin.md) | [etke.cc/synapse-admin](https://ghcr.io/etkecc/synapse-admin) | x | A web UI tool for administrating users and rooms on your Matrix server |
| [Metrics and Graphs](configuring-playbook-prometheus-grafana.md) | [prom/prometheus](https://hub.docker.com/r/prom/prometheus/) | x | [Prometheus](https://prometheus.io) time-series database server |
| [Metrics and Graphs](configuring-playbook-prometheus-grafana.md) | [prom/node-exporter](https://hub.docker.com/r/prom/node-exporter/) | x | Prometheus [node-exporter](https://prometheus.io/docs/guides/node-exporter/) host metrics exporter |
| [Metrics and Graphs](configuring-playbook-prometheus-grafana.md) | [grafana/grafana](https://hub.docker.com/r/grafana/grafana/) | x | Graphing tool that works well with the above two images. Our playbook also adds two dashboards for [Synapse](https://github.com/element-hq/synapse/tree/master/contrib/grafana) and [Node Exporter](https://github.com/rfrail3/grafana-dashboards) |
| [Metrics and Graphs](configuring-playbook-prometheus-nginxlog.md) | [martin-helmich/prometheus-nginxlog-exporter/exporter](https://ghcr.io/martin-helmich/prometheus-nginxlog-exporter/exporter) | x | Addon for Prometheus that gathers access logs from various nginx reverse-proxies |
| [Borg](configuring-playbook-backup-borg.md) | (N/A) | x | Backups |
| [rageshake](configuring-playbook-rageshake.md) | [matrix-org/rageshake](https://ghcr.io/matrix-org/rageshake) | x | Bug report server |
| [synapse-usage-exporter](configuring-playbook-synapse-usage-exporter.md) | Self-building | x | Export the usage statistics of a Synapse homeserver to be scraped by Prometheus. |

## Misc

Various services that don't fit any other categories.

| Service | Container image | Default? | Description |
| ------- | --------------- | -------- | ----------- |
| [sliding-sync](configuring-playbook-sliding-sync-proxy.md) | [matrix-org/sliding-sync](https://ghcr.io/matrix-org/sliding-sync) | x | Sliding Sync support for clients which require it (like old Element X versions, before it got switched to Simplified Sliding Sync) |
| [synapse_auto_accept_invite](configuring-playbook-synapse-auto-accept-invite.md) | (N/A) | x | A Synapse module to automatically accept invites. |
| [synapse_auto_compressor](configuring-playbook-synapse-auto-compressor.md) | [etke.cc/rust-synapse-compress-state](https://gitlab.com/etke.cc/rust-synapse-compress-state/container_registry) | x | A cli tool that automatically compresses `state_groups` database table in background. |
| [Matrix Corporal](configuring-playbook-matrix-corporal.md) (advanced) | [devture/matrix-corporal](https://hub.docker.com/r/devture/matrix-corporal/) | x | Reconciliator and gateway for a managed Matrix server |
| [Etherpad](configuring-playbook-etherpad.md) | [etherpad/etherpad](https://hub.docker.com/r/etherpad/etherpad/) | x | An open source collaborative text editor |
| [Jitsi](configuring-playbook-jitsi.md) | [jitsi/web](https://hub.docker.com/r/jitsi/web) | x | the [Jitsi](https://jitsi.org/) web UI |
| [Jitsi](configuring-playbook-jitsi.md) | [jitsi/jicofo](https://hub.docker.com/r/jitsi/jicofo) | x | the [Jitsi](https://jitsi.org/) Focus component |
| [Jitsi](configuring-playbook-jitsi.md) | [jitsi/prosody](https://hub.docker.com/r/jitsi/prosody) | x | the [Jitsi](https://jitsi.org/) Prosody XMPP server component |
| [Jitsi](configuring-playbook-jitsi.md) | [jitsi/jvb](https://hub.docker.com/r/jitsi/jvb) | x | the [Jitsi](https://jitsi.org/) Video Bridge component |
| [Cactus Comments](configuring-playbook-cactus-comments.md) | [cactuscomments/cactus-appservice](https://hub.docker.com/r/cactuscomments/cactus-appservice/) | x | A federated comment system built on Matrix |
| [Cactus Comments](configuring-playbook-cactus-comments.md) | [joseluisq/static-web-server](https://hub.docker.com/r/joseluisq/static-web-server) | x | A federated comment system built on Matrix |
| [Pantalaimon](configuring-playbook-pantalaimon.md) | [matrixdotorg/pantalaimon](https://hub.docker.com/r/matrixdotorg/pantalaimon) | x | An E2EE aware proxy daemon |
| [Sygnal](configuring-playbook-sygnal.md) | [matrixdotorg/sygnal](https://hub.docker.com/r/matrixdotorg/sygnal/) | x | Reference Push Gateway for Matrix |
| [ntfy](configuring-playbook-ntfy.md) | [binwiederhier/ntfy](https://hub.docker.com/r/binwiederhier/ntfy/) | x | Self-hosted, UnifiedPush-compatible push notifications server |

## Container images of deprecated / unmaintained services

The list of the deprecated or unmaintained services is available [here](configuring-playbook.md#deprecated--unmaintained--removed-services).

| Service | Container image | Default? | Description |
| ------- | --------------- | -------- | ----------- |
| [matrix-appservice-webhooks](configuring-playbook-bridge-appservice-webhooks.md) | [turt2live/matrix-appservice-webhooks](https://hub.docker.com/r/turt2live/matrix-appservice-webhooks) | x | Bridge for slack compatible webhooks ([ConcourseCI](https://concourse-ci.org/), [Slack](https://slack.com/) etc. pp.) |
| [Dimension](configuring-playbook-dimension.md) | [turt2live/matrix-dimension](https://hub.docker.com/r/turt2live/matrix-dimension) | x | An open source integration manager for Matrix clients |
| [Go-NEB](configuring-playbook-bot-go-neb.md) | [matrixdotorg/go-neb](https://hub.docker.com/r/matrixdotorg/go-neb) | x | A multi functional bot written in Go |
| [matrix-chatgpt-bot](configuring-playbook-bot-chatgpt.md) | [matrixgpt/matrix-chatgpt-bot](https://ghcr.io/matrixgpt/matrix-chatgpt-bot) | x | Accessing ChatGPT via your favourite Matrix client |
| [mautrix-facebook](configuring-playbook-bridge-mautrix-facebook.md) | [mautrix/facebook](https://mau.dev/mautrix/facebook/container_registry) | x | Bridge to [Facebook](https://facebook.com/) |
| [mautrix-hangouts](configuring-playbook-bridge-mautrix-hangouts.md) | [mautrix/hangouts](https://mau.dev/mautrix/hangouts/container_registry) | x | Bridge to [Google Hangouts](https://en.wikipedia.org/wiki/Google_Hangouts) |
| [mautrix-instagram](configuring-playbook-bridge-mautrix-instagram.md) | [mautrix/instagram](https://mau.dev/mautrix/instagram/container_registry) | x | Bridge to [Instagram](https://instagram.com/) |
