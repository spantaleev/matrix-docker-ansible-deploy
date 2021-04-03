[![Support room on Matrix](https://img.shields.io/matrix/matrix-docker-ansible-deploy:devture.com.svg?label=%23matrix-docker-ansible-deploy%3Adevture.com&logo=matrix&style=for-the-badge&server_fqdn=matrix.devture.com)](https://matrix.to/#/#matrix-docker-ansible-deploy:devture.com) [![donate](https://liberapay.com/assets/widgets/donate.svg)](https://liberapay.com/s.pantaleev/donate)

# Matrix (An open network for secure, decentralized communication) server setup using Ansible and Docker

## Purpose

This [Ansible](https://www.ansible.com/) playbook is meant to help you run your own [Matrix](http://matrix.org/) homeserver, along with the [various services](#supported-services) related to that.

That is, it lets you join the Matrix network using your own `@<username>:<your-domain>` identifier, all hosted on your own server (see [prerequisites](docs/prerequisites.md)).

We run all services in [Docker](https://www.docker.com/) containers (see [the container images we use](docs/container-images.md)), which lets us have a predictable and up-to-date setup, across multiple supported distros (see [prerequisites](docs/prerequisites.md)) and [architectures](docs/alternative-architectures.md) (x86/amd64 being recommended).

[Installation](docs/README.md) (upgrades) and some maintenance tasks are automated using [Ansible](https://www.ansible.com/) (see [our Ansible guide](docs/ansible.md)).


## Supported services

Using this playbook, you can get the following services configured on your server:

- (optional, default) a [Synapse](https://github.com/matrix-org/synapse) homeserver - storing your data and managing your presence in the [Matrix](http://matrix.org/) network

- (optional) [Amazon S3](https://aws.amazon.com/s3/) storage for Synapse's content repository (`media_store`) files using [Goofys](https://github.com/kahing/goofys)

- (optional, default) [PostgreSQL](https://www.postgresql.org/) database for Synapse. [Using an external PostgreSQL server](docs/configuring-playbook-external-postgres.md) is also possible.

- (optional, default) a [coturn](https://github.com/coturn/coturn) STUN/TURN server for WebRTC audio/video calls

- (optional, default) free [Let's Encrypt](https://letsencrypt.org/) SSL certificate, which secures the connection to the Synapse server and the Element web UI

- (optional, default) an [Element](https://app.element.io/) ([formerly Riot](https://element.io/previously-riot)) web UI, which is configured to connect to your own Synapse server by default

- (optional, default) an [ma1sd](https://github.com/ma1uta/ma1sd) Matrix Identity server

- (optional, default) an [Exim](https://www.exim.org/) mail server, through which all Matrix services send outgoing email (can be configured to relay through another SMTP server)

- (optional, default) an [nginx](http://nginx.org/) web server, listening on ports 80 and 443 - standing in front of all the other services. Using your own webserver [is possible](docs/configuring-playbook-own-webserver.md)

- (optional, advanced) the [matrix-synapse-rest-auth](https://github.com/ma1uta/matrix-synapse-rest-password-provider) REST authentication password provider module

- (optional, advanced) the [matrix-synapse-shared-secret-auth](https://github.com/devture/matrix-synapse-shared-secret-auth) password provider module

- (optional, advanced) the [matrix-synapse-ldap3](https://github.com/matrix-org/matrix-synapse-ldap3) LDAP Auth password provider module

- (optional, advanced) the [synapse-simple-antispam](https://github.com/t2bot/synapse-simple-antispam) spam checker module

- (optional, advanced) the [Matrix Corporal](https://github.com/devture/matrix-corporal) reconciliator and gateway for a managed Matrix server

- (optional) the [mautrix-telegram](https://github.com/tulir/mautrix-telegram) bridge for bridging your Matrix server to [Telegram](https://telegram.org/)

- (optional) the [mautrix-whatsapp](https://github.com/tulir/mautrix-whatsapp) bridge for bridging your Matrix server to [Whatsapp](https://www.whatsapp.com/)

- (optional) the [mautrix-facebook](https://github.com/tulir/mautrix-facebook) bridge for bridging your Matrix server to [Facebook](https://facebook.com/)

- (optional) the [mautrix-hangouts](https://github.com/tulir/mautrix-hangouts) bridge for bridging your Matrix server to [Google Hangouts](https://en.wikipedia.org/wiki/Google_Hangouts)

- (optional) the [mautrix-instagram](https://github.com/tulir/mautrix-instagram) bridge for bridging your Matrix server to [Instagram](https://instagram.com/)

- (optional) the [mautrix-signal](https://github.com/tulir/mautrix-signal) bridge for bridging your Matrix server to [Signal](https://www.signal.org/)

- (optional) the [matrix-appservice-irc](https://github.com/matrix-org/matrix-appservice-irc) bridge for bridging your Matrix server to [IRC](https://wikipedia.org/wiki/Internet_Relay_Chat)

- (optional) the [matrix-appservice-discord](https://github.com/Half-Shot/matrix-appservice-discord) bridge for bridging your Matrix server to [Discord](https://discordapp.com/)

- (optional) the [matrix-appservice-slack](https://github.com/matrix-org/matrix-appservice-slack) bridge for bridging your Matrix server to [Slack](https://slack.com/)

- (optional) the [matrix-appservice-webhooks](https://github.com/turt2live/matrix-appservice-webhooks) bridge for slack compatible webhooks ([ConcourseCI](https://concourse-ci.org/), [Slack](https://slack.com/) etc. pp.)

- (optional) the [matrix-sms-bridge](https://github.com/benkuly/matrix-sms-bridge) for bridging your Matrix server to SMS - see [docs/configuring-playbook-bridge-matrix-bridge-sms.md](docs/configuring-playbook-bridge-matrix-bridge-sms.md) for setup documentation

- (optional) the [mx-puppet-skype](https://hub.docker.com/r/sorunome/mx-puppet-skype) for bridging your Matrix server to [Skype](https://www.skype.com) - see [docs/configuring-playbook-bridge-mx-puppet-skype.md](docs/configuring-playbook-bridge-mx-puppet-skype.md) for setup documentation

- (optional) the [mx-puppet-slack](https://hub.docker.com/r/sorunome/mx-puppet-slack) for bridging your Matrix server to [Slack](https://slack.com) - see [docs/configuring-playbook-bridge-mx-puppet-slack.md](docs/configuring-playbook-bridge-mx-puppet-slack.md) for setup documentation

- (optional) the [mx-puppet-instagram](https://github.com/Sorunome/mx-puppet-instagram) bridge for Instagram-DMs ([Instagram](https://www.instagram.com/)) - see [docs/configuring-playbook-bridge-mx-puppet-instagram.md](docs/configuring-playbook-bridge-mx-puppet-instagram.md) for setup documentation

- (optional) the [mx-puppet-twitter](https://github.com/Sorunome/mx-puppet-twitter) bridge for Twitter-DMs ([Twitter](https://twitter.com/)) - see [docs/configuring-playbook-bridge-mx-puppet-twitter.md](docs/configuring-playbook-bridge-mx-puppet-twitter.md) for setup documentation

- (optional) the [mx-puppet-discord](https://github.com/matrix-discord/mx-puppet-discord) bridge for [Discord](https://discordapp.com/) - see [docs/configuring-playbook-bridge-mx-puppet-discord.md](docs/configuring-playbook-bridge-mx-puppet-discord.md) for setup documentation

- (optional) the [mx-puppet-groupme](https://gitlab.com/robintown/mx-puppet-groupme) bridge for [GroupMe](https://groupme.com/) - see [docs/configuring-playbook-bridge-mx-puppet-groupme.md](docs/configuring-playbook-bridge-mx-puppet-groupme.md) for setup documentation

- (optional) the [mx-puppet-steam](https://github.com/icewind1991/mx-puppet-steam) bridge for [Steam](https://steamapp.com/) - see [docs/configuring-playbook-bridge-mx-puppet-steam.md](docs/configuring-playbook-bridge-mx-puppet-steam.md) for setup documentation

- (optional) [Email2Matrix](https://github.com/devture/email2matrix) for relaying email messages to Matrix rooms - see [docs/configuring-playbook-email2matrix.md](docs/configuring-playbook-email2matrix.md) for setup documentation

- (optional) [Dimension](https://github.com/turt2live/matrix-dimension), an open source integrations manager for matrix clients - see [docs/configuring-playbook-dimension.md](docs/configuring-playbook-dimension.md) for setup documentation

- (optional) [Etherpad](https://etherpad.org), an open source collaborative text editor - see [docs/configuring-playbook-etherpad.md](docs/configuring-playbook-etherpad.md) for setup documentation

- (optional) [Jitsi](https://jitsi.org/), an open source video-conferencing platform - see [docs/configuring-playbook-jitsi.md](docs/configuring-playbook-jitsi.md) for setup documentation

- (optional) [matrix-reminder-bot](https://github.com/anoadragon453/matrix-reminder-bot) for scheduling one-off & recurring reminders and alarms - see [docs/configuring-playbook-bot-matrix-reminder-bot.md](docs/configuring-playbook-bot-matrix-reminder-bot.md) for setup documentation

- (optional) [Go-NEB](https://github.com/matrix-org/go-neb) multi functional bot written in Go - see [docs/configuring-playbook-bot-go-neb.md](docs/configuring-playbook-bot-go-neb.md) for setup documentation

- (optional) [Mjolnir](https://github.com/matrix-org/mjolnir), a moderation tool for Matrix - see [docs/configuring-playbook-bot-mjolnir.md](docs/configuring-playbook-bot-mjolnir.md) for setup documentation

- (optional) [synapse-admin](https://github.com/Awesome-Technologies/synapse-admin), a web UI tool for administrating users and rooms on your Matrix server - see [docs/configuring-playbook-synapse-admin.md](docs/configuring-playbook-synapse-admin.md) for setup documentation

- (optional) [matrix-registration](https://github.com/ZerataX/matrix-registration), a simple python application to have a token based matrix registration - see [docs/configuring-playbook-matrix-registration.md](docs/configuring-playbook-matrix-registration.md) for setup documentation

- (optional) the [Prometheus](https://prometheus.io) time-series database server, the Prometheus [node-exporter](https://prometheus.io/docs/guides/node-exporter/) host metrics exporter, and the [Grafana](https://grafana.com/) web UI - see [Enabling metrics and graphs (Prometheus, Grafana) for your Matrix server](docs/configuring-playbook-prometheus-grafana.md) for setup documentation

- (optional) the [Sygnal](https://github.com/matrix-org/sygnal) push gateway - see [Setting up the Sygnal push gateway](docs/configuring-playbook-sygnal.md) for setup documentation

Basically, this playbook aims to get you up-and-running with all the basic necessities around Matrix, without you having to do anything else.

**Note**: the list above is exhaustive. It includes optional or even some advanced components that you will most likely not need.
Sticking with the defaults (which install a subset of the above components) is the best choice, especially for a new installation.
You can always re-run the playbook later to add or remove components.


## Installation

To configure and install Matrix on your own server, follow the [README in the docs/ directory](docs/README.md).


## Changes

This playbook evolves over time, sometimes with backward-incompatible changes.

When updating the playbook, refer to [the changelog](CHANGELOG.md) to catch up with what's new.


## Support

- Matrix room: [#matrix-docker-ansible-deploy:devture.com](https://matrix.to/#/#matrix-docker-ansible-deploy:devture.com)

- IRC channel: `#matrix-docker-ansible-deploy` on the [Freenode](https://freenode.net/) IRC network (irc.freenode.net)

- Github issues: [spantaleev/matrix-docker-ansible-deploy/issues](https://github.com/spantaleev/matrix-docker-ansible-deploy/issues)
