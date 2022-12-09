[![Support room on Matrix](https://img.shields.io/matrix/matrix-docker-ansible-deploy:devture.com.svg?label=%23matrix-docker-ansible-deploy%3Adevture.com&logo=matrix&style=for-the-badge&server_fqdn=matrix.devture.com)](https://matrix.to/#/#matrix-docker-ansible-deploy:devture.com) [![donate](https://liberapay.com/assets/widgets/donate.svg)](https://liberapay.com/s.pantaleev/donate)

# Matrix (An open network for secure, decentralized communication) server setup using Ansible and Docker

## Purpose

This [Ansible](https://www.ansible.com/) playbook is meant to help you run your own [Matrix](http://matrix.org/) homeserver, along with the [various services](#supported-services) related to that.

That is, it lets you join the Matrix network using your own `@<username>:<your-domain>` identifier, all hosted on your own server (see [prerequisites](docs/prerequisites.md)).

We run all services in [Docker](https://www.docker.com/) containers (see [the container images we use](docs/container-images.md)), which lets us have a predictable and up-to-date setup, across multiple supported distros (see [prerequisites](docs/prerequisites.md)) and [architectures](docs/alternative-architectures.md) (x86/amd64 being recommended).

[Installation](docs/README.md) (upgrades) and some maintenance tasks are automated using [Ansible](https://www.ansible.com/) (see [our Ansible guide](docs/ansible.md)).


## Supported services

Using this playbook, you can get the following list of services configured on your server. Basically, this playbook aims to get you up-and-running with all the necessities around Matrix, without you having to do anything else.

**Note**: the list below is exhaustive. It includes optional or even some advanced components that you will most likely not need.
Sticking with the defaults (which install a subset of the above components) is the best choice, especially for a new installation.
You can always re-run the playbook later to add or remove components.


### Homeserver

The homeserver is the backbone of your matrix system. Choose one from the following list.

| Name | Default? | Description | Documentation |
| ---- | -------- | ----------- | ------------- | 
| [Synapse](https://github.com/matrix-org/synapse) | ✓ | Storing your data and managing your presence in the [Matrix](http://matrix.org/) network | [Link](docs/configuring-playbook-synapse.md) |
| [Conduit](https://conduit.rs) | x | Storing your data and managing your presence in the [Matrix](http://matrix.org/) network. Conduit is a lightweight open-source server implementation of the Matrix Specification with a focus on easy setup and low system requirements | [Link](docs/configuring-playbook-conduit.md) |
| [Dendrite](https://github.com/matrix-org/dendrite) | x | Storing your data and managing your presence in the [Matrix](http://matrix.org/) network. Dendrite is a second-generation Matrix homeserver written in Go, an alternative to Synapse. | [Link](docs/configuring-playbook-dendrite.md) |

### Clients

Web clients for matrix that you can host on your own domains.

| Name | Default? | Description | Documentation |
| ---- | -------- | ----------- | ------------- |
[Element](https://app.element.io/) | ✓ | Web UI, which is configured to connect to your own Synapse server by default | [Link](docs/configuring-playbook-client-element.md) |
| [Hydrogen](https://github.com/vector-im/hydrogen-web) | x | Web client | [Link](docs/configuring-playbook-client-hydrogen.md) |
| [Cinny](https://github.com/ajbura/cinny) |  x | Web client | [Link](docs/configuring-playbook-client-cinny.md) |



### Server Components

Services that run on the server to make the various parts of your installation work.

| Name | Default? | Description | Documentation |
| ---- | -------- | ----------- | ------------- |
| [PostgreSQL](https://www.postgresql.org/)| ✓ | Database for Synapse. [Using an external PostgreSQL server](docs/configuring-playbook-external-postgres.md) is also possible. | [Link](docs/configuring-playbook-external-postgres.md) |
| [Coturn](https://github.com/coturn/coturn) | ✓ | STUN/TURN server for WebRTC audio/video calls | [Link](docs/configuring-playbook-turn.md) |
| [nginx](http://nginx.org/) | ✓ | Web server, listening on ports 80 and 443 - standing in front of all the other services. Using your own webserver [is possible](docs/configuring-playbook-own-webserver.md) | [Link](docs/configuring-playbook-nginx.md) |
| [Let's Encrypt](https://letsencrypt.org/) | ✓ | Free  SSL certificate, which secures the connection to the Synapse server and the Element web UI | [Link](docs/configuring-playbook-ssl-certificates.md) |
| [ma1sd](https://github.com/ma1uta/ma1sd) | x | Matrix Identity Server | [Link](docs/configuring-playbook-ma1sd.md)
| [Exim](https://www.exim.org/) | ✓ | Mail server, through which all Matrix services send outgoing email (can be configured to relay through another SMTP server) | - |
| [Dimension](https://github.com/turt2live/matrix-dimension) | x | An open source integrations manager for matrix clients | [Link](docs/configuring-playbook-dimension.md) |
| [Sygnal](https://github.com/matrix-org/sygnal) | x | Push gateway | [Link](docs/configuring-playbook-sygnal.md) |
| [ntfy](https://ntfy.sh) | x | Push notifications server | [Link](docs/configuring-playbook-ntfy.md) |


### Authentication

Extend and modify how users are authenticated on your homeserver.

| Name | Default? | Description | Documentation |
| ---- | -------- | ----------- | ------------- | 
| [matrix-synapse-rest-auth](https://github.com/ma1uta/matrix-synapse-rest-password-provider) (advanced) | x | REST authentication password provider module | [Link](docs/configuring-playbook-rest-auth.md) |
|[matrix-synapse-shared-secret-auth](https://github.com/devture/matrix-synapse-shared-secret-auth) (advanced) | x | Password provider module | [Link](docs/configuring-playbook-shared-secret-auth.md) |
| [matrix-synapse-ldap3](https://github.com/matrix-org/matrix-synapse-ldap3) (advanced) | x | LDAP Auth password provider module | [Link](configuring-playbook-ldap-auth.md) |
| [matrix-ldap-registration-proxy](https://gitlab.com/activism.international/matrix_ldap_registration_proxy) (advanced) | x | A proxy that handles Matrix registration requests and forwards them to LDAP. | [Link](docs/configuring-playbook-matrix-ldap-registration-proxy.md) |
| [matrix-registration](https://github.com/ZerataX/matrix-registration) | x | A simple python application to have a token based matrix registration | [Link](docs/configuring-playbook-matrix-registration.md) |


### File Storage

Use alternative file storage to the default `media_store` folder.

| Name | Default? | Description | Documentation |
| ---- | -------- | ----------- | ------------- |
| [Goofys](https://github.com/kahing/goofys) | x | [Amazon S3](https://aws.amazon.com/s3/) (or other S3-compatible object store) storage for Synapse's content repository (`media_store`) files | [Link](docs/configuring-playbook-s3-goofys.md) |
| [synapse-s3-storage-provider](https://github.com/matrix-org/synapse-s3-storage-provider) | x | [Amazon S3](https://aws.amazon.com/s3/) (or other S3-compatible object store) storage for Synapse's content repository (`media_store`) files | [Link](docs/configuring-playbook-s3.md) |

### Bridges

Bridges can be used to connect your matrix installation with third-party communication networks.

| Name | Default? | Description | Documentation |
| ---- | -------- | ----------- | ------------- |
[mautrix-discord](https://github.com/mautrix/discord) | x | Bridge for bridging your Matrix server to [Discord](https://discord.com/) | [Link](docs/configuring-playbook-bridge-mautrix-discord.md) |
| [mautrix-telegram](https://github.com/mautrix/telegram) | x | Bridge for bridging your Matrix server to [Telegram](https://telegram.org/) | [Link](docs/configuring-playbook-bridge-mautrix-telegram.md) |
| [mautrix-whatsapp](https://github.com/mautrix/whatsapp) | x | Bridge for bridging your Matrix server to [WhatsApp](https://www.whatsapp.com/) | [Link](docs/configuring-playbook-bridge-mautrix-whatsapp.md) |
| [mautrix-facebook](https://github.com/mautrix/facebook) | x | Bridge for bridging your Matrix server to [Facebook](https://facebook.com/) | [Link](docs/configuring-playbook-bridge-mautrix-facebook.md) |
| [mautrix-twitter](https://github.com/mautrix/twitter) | x | Bridge for bridging your Matrix server to [Twitter](https://twitter.com/) | [Link](docs/configuring-playbook-bridge-mautrix-twitter.md) |
| [mautrix-hangouts](https://github.com/mautrix/hangouts) | x | Bridge for bridging your Matrix server to [Google Hangouts](https://en.wikipedia.org/wiki/Google_Hangouts) | [Link](docs/configuring-playbook-bridge-mautrix-hangouts.md) |
| [mautrix-googlechat](https://github.com/mautrix/googlechat) | x | Bridge for bridging your Matrix server to [Google Chat](https://en.wikipedia.org/wiki/Google_Chat) | [Link](docs/configuring-playbook-bridge-mautrix-googlechat.md) |
| [mautrix-instagram](https://github.com/mautrix/instagram) | x | Bridge for bridging your Matrix server to [Instagram](https://instagram.com/) | [Link](docs/configuring-playbook-bridge-mautrix-instagram.md) |
| [mautrix-signal](https://github.com/mautrix/signal) | x | Bridge for bridging your Matrix server to [Signal](https://www.signal.org/) | [Link](docs/configuring-playbook-bridge-mautrix-signal.md) |
| [beeper-linkedin](https://github.com/beeper/linkedin) | x | Bridge for bridging your Matrix server to [LinkedIn](https://www.linkedin.com/) | [Link](docs/configuring-playbook-bridge-beeper-linkedin.md) |
| [matrix-appservice-irc](https://github.com/matrix-org/matrix-appservice-irc) | x | Bridge for bridging your Matrix server to [IRC](https://wikipedia.org/wiki/Internet_Relay_Chat) | [Link](docs/configuring-playbook-bridge-appservice-irc.md) |
| [matrix-appservice-discord](https://github.com/Half-Shot/matrix-appservice-discord) | x | Bridge for bridging your Matrix server to [Discord](https://discordapp.com/) | [Link](docs/configuring-playbook-bridge-appservice-discord.md) |
| [matrix-appservice-slack](https://github.com/matrix-org/matrix-appservice-slack) | x | Bridge for bridging your Matrix server to [Slack](https://slack.com/) | [Link](docs/configuring-playbook-bridge-appservice-slack.md) |
| [matrix-appservice-webhooks](https://github.com/turt2live/matrix-appservice-webhooks) | x | Bridge for slack compatible webhooks ([ConcourseCI](https://concourse-ci.org/), [Slack](https://slack.com/) etc. pp.) | [Link](docs/configuring-playbook-bridge-appservice-webhooks.md) |
| [matrix-hookshot](https://github.com/Half-Shot/matrix-hookshot) | x | Bridge for bridging Matrix to generic webhooks and multiple project management services, such as GitHub, GitLab, Figma, and Jira in particular | [Link](docs/configuring-playbook-bridge-hookshot.md) |
| [matrix-sms-bridge](https://github.com/benkuly/matrix-sms-bridge) | x | Bridge for bridging your Matrix server to SMS | [Link](docs/configuring-playbook-bridge-matrix-bridge-sms.md) |
| [Heisenbridge](https://github.com/hifi/heisenbridge) | x | Bridge for bridging your Matrix server to IRC bouncer-style | [Link](docs/configuring-playbook-bridge-heisenbridge.md) |
| [go-skype-bridge](https://github.com/kelaresg/go-skype-bridge) | x | Bridge for bridging your Matrix server to [Skype](https://www.skype.com) | [Link](docs/configuring-playbook-bridge-go-skype-bridge.md) |
| [mx-puppet-slack](https://hub.docker.com/r/sorunome/mx-puppet-slack) | x | Bridge for bridging your Matrix server to [Slack](https://slack.com) | [Link](docs/configuring-playbook-bridge-mx-puppet-slack.md) |
| [mx-puppet-instagram](https://github.com/Sorunome/mx-puppet-instagram) | x | Bridge for Instagram-DMs ([Instagram](https://www.instagram.com/)) | [Link](docs/configuring-playbook-bridge-mx-puppet-instagram.md) |
| [mx-puppet-twitter](https://github.com/Sorunome/mx-puppet-twitter) | x | Bridge for Twitter-DMs ([Twitter](https://twitter.com/)) | [Link](docs/configuring-playbook-bridge-mx-puppet-twitter.md) |
| [mx-puppet-discord](https://github.com/matrix-discord/mx-puppet-discord) | x | Bridge for [Discord](https://discordapp.com/) | [Link](docs/configuring-playbook-bridge-mx-puppet-discord.md) |
| [mx-puppet-groupme](https://gitlab.com/xangelix-pub/matrix/mx-puppet-groupme) | x | Bridge for [GroupMe](https://groupme.com/) | [Link](docs/configuring-playbook-bridge-mx-puppet-groupme.md) |
| [mx-puppet-steam](https://github.com/icewind1991/mx-puppet-steam) | x | Bridge for [Steam](https://steamapp.com/) | [Link](docs/configuring-playbook-bridge-mx-puppet-steam.md) |
| [Email2Matrix](https://github.com/devture/email2matrix) | x | Bridge for relaying email messages to Matrix rooms | [Link](docs/configuring-playbook-email2matrix.md) |


### Bots

Bots provide various additional functionality to your installation.

| Name | Default? | Description | Documentation |
| ---- | -------- | ----------- | ------------- |
| [matrix-reminder-bot](https://github.com/anoadragon453/matrix-reminder-bot) | x | Bot for scheduling one-off & recurring reminders and alarms | [Link](docs/configuring-playbook-bot-matrix-reminder-bot.md) |
| [matrix-registration-bot](https://github.com/moan0s/matrix-registration-bot) | x | Bot for invitations by creating and managing registration tokens | [Link](docs/configuring-playbook-bot-matrix-registration-bot.md) |
| [maubot](https://github.com/maubot/maubot) | x | A plugin-based Matrix bot system | [Link](docs/configuring-playbook-bot-maubot.md) |
| [honoroit](https://gitlab.com/etke.cc/honoroit) | x | A helpdesk bot | [Link](docs/configuring-playbook-bot-honoroit.md) |
| [Postmoogle](https://gitlab.com/etke.cc/postmoogle) | x | Email to matrix bot | [Link](docs/configuring-playbook-bot-postmoogle.md) |
| [Go-NEB](https://github.com/matrix-org/go-neb) | x | A multi functional bot written in Go | [Link](docs/configuring-playbook-bot-go-neb.md) |
| [Mjolnir](https://github.com/matrix-org/mjolnir) | x | A moderation tool for Matrix | [Link](docs/configuring-playbook-bot-mjolnir.md) |
| [Buscarron](https://gitlab.com/etke.cc/buscarron) | x | Web forms (HTTP POST) to matrix | [Link](docs/configuring-playbook-bot-buscarron.md) |

### Administration

Services that help you in administrating and monitoring your matrix installation.


| Name | Default? | Description | Documentation |
| ---- | -------- | ----------- | ------------- |
| [synapse-admin](https://github.com/Awesome-Technologies/synapse-admin) | x | A web UI tool for administrating users and rooms on your Matrix server | [Link](docs/configuring-playbook-synapse-admin.md) |
| Metrics and Graphs | x | Consists of the [Prometheus](https://prometheus.io) time-series database server, the Prometheus [node-exporter](https://prometheus.io/docs/guides/node-exporter/) host metrics exporter, and the [Grafana](https://grafana.com/) web UI | [Link](docs/configuring-playbook-prometheus-grafana.md) |
| [Borg](https://borgbackup.org) | x | Backups | [Link](docs/configuring-playbook-backup-borg.md) |

### Misc

Various services that don't fit any other category.

| Name | Default? | Description | Documentation |
| ---- | -------- | ----------- | ------------- |
| [synapse-simple-antispam](https://github.com/t2bot/synapse-simple-antispam) (advanced) | x | A spam checker module | [Link](docs/configuring-playbook-synapse-simple-antispam.md) |
| [Matrix Corporal](https://github.com/devture/matrix-corporal) (advanced) | x | Reconciliator and gateway for a managed Matrix server | [Link](docs/configuring-playbook-matrix-corporal.md) |
| [Etherpad](https://etherpad.org) | x | An open source collaborative text editor | [Link](docs/configuring-playbook-etherpad.md) |
| [Jitsi](https://jitsi.org/) | x | An open source video-conferencing platform | [Link](docs/configuring-playbook-jitsi.md) |
| [Cactus Comments](https://cactus.chat) | x | A federated comment system built on matrix | [Link](docs/configuring-playbook-cactus-comments.md) |


## Installation

To configure and install Matrix on your own server, follow the [README in the docs/ directory](docs/README.md).


## Changes

This playbook evolves over time, sometimes with backward-incompatible changes.

When updating the playbook, refer to [the changelog](CHANGELOG.md) to catch up with what's new.


## Support

- Matrix room: [#matrix-docker-ansible-deploy:devture.com](https://matrix.to/#/#matrix-docker-ansible-deploy:devture.com)

- IRC channel: `#matrix-docker-ansible-deploy` on the [Libera Chat](https://libera.chat/) IRC network (irc.libera.chat:6697)

- GitHub issues: [spantaleev/matrix-docker-ansible-deploy/issues](https://github.com/spantaleev/matrix-docker-ansible-deploy/issues)


## Services by the community

- [etke.cc](https://etke.cc) - matrix-docker-ansible-deploy and system stuff "as a service". That service will create your matrix homeserver on your domain and server (doesn't matter if it's cloud provider or on an old laptop in the corner of your room), (optional) maintains it (server's system updates, cleanup, security adjustments, tuning, etc.; matrix homeserver updates & maintenance) and (optional) provide full-featured email service for your domain
