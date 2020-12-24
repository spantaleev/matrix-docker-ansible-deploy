[![Support room on Matrix](https://img.shields.io/matrix/matrix-docker-ansible-deploy:devture.com.svg?label=%23matrix-docker-ansible-deploy%3Adevture.com&logo=matrix&style=for-the-badge&server_fqdn=matrix.devture.com)](https://matrix.to/#/#matrix-docker-ansible-deploy:devture.com) [![donate](https://liberapay.com/assets/widgets/donate.svg)](https://liberapay.com/s.pantaleev/donate)

# Matrix (An open network for secure, decentralized communication) server setup using Ansible and Docker

## Purpose

This Ansible playbook is meant to easily let you run your own [Matrix](http://matrix.org/) homeserver.

That is, it lets you join the Matrix network with your own `@<username>:<your-domain>` identifier, all hosted on your own server.

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

- (optional) the [matrix-appservice-irc](https://github.com/matrix-org/matrix-appservice-irc) bridge for bridging your Matrix server to [IRC](https://wikipedia.org/wiki/Internet_Relay_Chat)

- (optional) the [matrix-appservice-discord](https://github.com/Half-Shot/matrix-appservice-discord) bridge for bridging your Matrix server to [Discord](https://discordapp.com/)

- (optional) the [matrix-appservice-slack](https://github.com/matrix-org/matrix-appservice-slack) bridge for bridging your Matrix server to [Slack](https://slack.com/)

- (optional) the [matrix-appservice-webhooks](https://github.com/turt2live/matrix-appservice-webhooks) bridge for slack compatible webhooks ([ConcourseCI](https://concourse-ci.org/), [Slack](https://slack.com/) etc. pp.)

- (optional) the [mx-puppet-instagram](https://github.com/Sorunome/mx-puppet-instagram) bridge for Instagram-DMs ([Instagram](https://www.instagram.com/)) - see [docs/configuring-playbook-bridge-mx-puppet-instagram.md](docs/configuring-playbook-bridge-mx-puppet-instagram.md) for setup documentation

- (optional) the [mx-puppet-twitter](https://github.com/Sorunome/mx-puppet-twitter) bridge for Twitter-DMs ([Twitter](https://twitter.com/) - see [docs/configuring-playbook-bridge-mx-puppet-twitter.md](docs/configuring-playbook-bridge-mx-puppet-twitter.md) for setup documentation

- (optional) the [mx-puppet-discord](https://github.com/matrix-discord/mx-puppet-discord) bridge for [Discord](https://discordapp.com/)) - see [docs/configuring-playbook-bridge-mx-puppet-discord.md](docs/configuring-playbook-bridge-mx-puppet-discord.md) for setup documentation

- (optional) the [mx-puppet-steam](https://github.com/icewind1991/mx-puppet-steam) bridge for [Steam](https://steamapp.com/)) - see [docs/configuring-playbook-bridge-mx-puppet-steam.md](docs/configuring-playbook-bridge-mx-puppet-steam.md) for setup documentation

- (optional) the [matrix-sms-bridge](https://github.com/benkuly/matrix-sms-bridge) for bridging your Matrix server to SMS - see [docs/configuring-playbook-bridge-matrix-bridge-sms.md](docs/configuring-playbook-bridge-matrix-bridge-sms.md) for setup documentation

- (optional) [Email2Matrix](https://github.com/devture/email2matrix) for relaying email messages to Matrix rooms - see [docs/configuring-playbook-email2matrix.md](docs/configuring-playbook-email2matrix.md) for setup documentation

- (optional) [Dimension](https://github.com/turt2live/matrix-dimension), an open source integrations manager for matrix clients - see [docs/configuring-playbook-dimension.md](docs/configuring-playbook-dimension.md) for setup documentation

- (optional) [Jitsi](https://jitsi.org/), an open source video-conferencing platform - see [docs/configuring-playbook-jitsi.md](docs/configuring-playbook-jitsi.md) for setup documentation

- (optional) [matrix-reminder-bot](https://github.com/anoadragon453/matrix-reminder-bot) for scheduling one-off & recurring reminders and alarms - see [docs/configuring-playbook-bot-matrix-reminder-bot.md](docs/configuring-playbook-bot-matrix-reminder-bot.md) for setup documentation

- (optional) [synapse-admin](https://github.com/Awesome-Technologies/synapse-admin), a web UI tool for administrating users and rooms on your Matrix server - see [docs/configuring-playbook-synapse-admin.md](docs/configuring-playbook-synapse-admin.md) for setup documentation

- (optional) [matrix-registration](https://github.com/ZerataX/matrix-registration), a simple python application to have a token based matrix registration - see [docs/configuring-playbook-matrix-registration.md](docs/configuring-playbook-matrix-registration.md) for setup documentation

Basically, this playbook aims to get you up-and-running with all the basic necessities around Matrix, without you having to do anything else.

**Note**: the list above is exhaustive. It includes optional or even some advanced components that you will most likely not need.
Sticking with the defaults (which install a subset of the above components) is the best choice, especially for a new installation.
You can always re-run the playbook later to add or remove components.


## What's different about this Ansible playbook?

This is similar to the [EMnify/matrix-synapse-auto-deploy](https://github.com/EMnify/matrix-synapse-auto-deploy) Ansible deployment, but:

- this one is a complete Ansible playbook (instead of just a role), so it's **easier to run** - especially for folks not familiar with Ansible

- this one installs and hooks together **a lot more Matrix-related services** for you (see above)

- this one **can be executed more than once** without causing trouble

- works on various distros: **CentOS** (7.0+), Debian-based distributions (**Debian** 9/Stretch+, **Ubuntu** 16.04+), **Archlinux**

- this one installs everything in a single directory (`/matrix` by default) and **doesn't "contaminate" your server** with files all over the place

- this one **doesn't necessarily take over** ports 80 and 443. By default, it sets up nginx for you there, but you can also [use your own webserver](docs/configuring-playbook-own-webserver.md)

- this one **runs everything in Docker containers**, so it's likely more predictable and less fragile (see [Docker images used by this playbook](#docker-images-used-by-this-playbook))

- this one retrieves and automatically renews free [Let's Encrypt](https://letsencrypt.org/) **SSL certificates** for you

- this one optionally can store the `media_store` content repository files on [Amazon S3](https://aws.amazon.com/s3/) (but defaults to storing files on the server's filesystem)

- this one optionally **allows you to use an external PostgreSQL server** for Synapse's database (but defaults to running one in a container)

- helps you **import data from a previous installation** (so you can migrate your manual virtualenv/Docker setup to a more managed one)


## Installation

To configure and install Matrix on your own server, follow the [README in the docs/ directory](docs/README.md).


## Changes

This playbook evolves over time, sometimes with backward-incompatible changes.

When updating the playbook, refer to [the changelog](CHANGELOG.md) to catch up with what's new.


## Docker images used by this playbook

This playbook sets up your server using the following Docker images:

- [matrixdotorg/synapse](https://hub.docker.com/r/matrixdotorg/synapse/) - the official [Synapse](https://github.com/matrix-org/synapse) Matrix homeserver (optional)

- [instrumentisto/coturn](https://hub.docker.com/r/instrumentisto/coturn/) - the [Coturn](https://github.com/coturn/coturn) STUN/TURN server (optional)

- [vectorim/element-web](https://hub.docker.com/r/vectorim/element-web/) - the [Element](https://element.io/) web client (optional)

- [ma1uta/ma1sd](https://hub.docker.com/r/ma1uta/ma1sd/) - the [ma1sd](https://github.com/ma1uta/ma1sd) Matrix Identity server (optional)

- [postgres](https://hub.docker.com/_/postgres/) - the [Postgres](https://www.postgresql.org/) database server (optional)

- [ewoutp/goofys](https://hub.docker.com/r/ewoutp/goofys/) - the [Goofys](https://github.com/kahing/goofys) Amazon [S3](https://aws.amazon.com/s3/) file-system-mounting program (optional)

- [devture/exim-relay](https://hub.docker.com/r/devture/exim-relay/) - the [Exim](https://www.exim.org/) email server (optional)

- [devture/email2matrix](https://hub.docker.com/r/devture/email2matrix/) - the [Email2Matrix](https://github.com/devture/email2matrix) email server, which can relay email messages to Matrix rooms (optional)

- [devture/matrix-corporal](https://hub.docker.com/r/devture/matrix-corporal/) - [Matrix Corporal](https://github.com/devture/matrix-corporal): reconciliator and gateway for a managed Matrix server (optional)

- [devture/zeratax-matrix-registration](https://hub.docker.com/r/devture/zeratax-matrix-registration/) - [matrix-registration](https://github.com/ZerataX/matrix-registration): a simple python application to have a token based matrix registration (optional)

- [nginx](https://hub.docker.com/_/nginx/) - the [nginx](http://nginx.org/) web server (optional)

- [certbot/certbot](https://hub.docker.com/r/certbot/certbot/) - the [certbot](https://certbot.eff.org/) tool for obtaining SSL certificates from [Let's Encrypt](https://letsencrypt.org/) (optional)

- [tulir/mautrix-telegram](https://hub.docker.com/r/tulir/mautrix-telegram/) - the [mautrix-telegram](https://github.com/tulir/mautrix-telegram) bridge to [Telegram](https://telegram.org/) (optional)

- [tulir/mautrix-whatsapp](https://hub.docker.com/r/tulir/mautrix-whatsapp/) - the [mautrix-whatsapp](https://github.com/tulir/mautrix-whatsapp) bridge to [Whatsapp](https://www.whatsapp.com/) (optional)

- [tulir/mautrix-facebook](https://hub.docker.com/r/tulir/mautrix-facebook/) - the [mautrix-facebook](https://github.com/tulir/mautrix-facebook) bridge to [Facebook](https://facebook.com/) (optional)

- [tulir/mautrix-hangouts](https://hub.docker.com/r/tulir/mautrix-hangouts/) - the [mautrix-hangouts](https://github.com/tulir/mautrix-hangouts) bridge to [Google Hangouts](https://en.wikipedia.org/wiki/Google_Hangouts) (optional)

- [matrixdotorg/matrix-appservice-irc](https://hub.docker.com/r/matrixdotorg/matrix-appservice-irc) - the [matrix-appservice-irc](https://github.com/matrix-org/matrix-appservice-irc) bridge to [IRC](https://wikipedia.org/wiki/Internet_Relay_Chat) (optional)

- [halfshot/matrix-appservice-discord](https://hub.docker.com/r/halfshot/matrix-appservice-discord) - the [matrix-appservice-discord](https://github.com/Half-Shot/matrix-appservice-discord) bridge to [Discord](https://discordapp.com/) (optional)

- [cadair/matrix-appservice-slack](https://hub.docker.com/r/cadair/matrix-appservice-slack) - the [matrix-appservice-slack](https://github.com/matrix-org/matrix-appservice-slack) bridge to [Slack](https://slack.com/) (optional)

- [turt2live/matrix-appservice-webhooks](https://hub.docker.com/r/turt2live/matrix-appservice-webhooks) - the [Appservice Webhooks](https://github.com/turt2live/matrix-appservice-webhooks) bridge (optional)

- [folivonet/matrix-sms-bridge](https://hub.docker.com/repository/docker/folivonet/matrix-sms-bridge) - the [matrix-sms-brdige](https://github.com/benkuly/matrix-sms-bridge) (optional)

- [sorunome/mx-puppet-skype](https://hub.docker.com/r/sorunome/mx-puppet-skype) - the [mx-puppet-skype](https://github.com/Sorunome/mx-puppet-skype) bridge to [Skype](https://www.skype.com) (optional)

- [sorunome/mx-puppet-slack](https://hub.docker.com/r/sorunome/mx-puppet-slack) - the [mx-puppet-slack](https://github.com/Sorunome/mx-puppet-slack) bridge to [Slack](https://slack.com) (optional)

- [sorunome/mx-puppet-instagram](https://hub.docker.com/r/sorunome/mx-puppet-instagram) - the [mx-puppet-instagram](https://github.com/Sorunome/mx-puppet-instagram) bridge to [Instagram](https://www.instagram.com) (optional)

- [sorunome/mx-puppet-twitter](https://hub.docker.com/r/sorunome/mx-puppet-twitter) - the [mx-puppet-twitter](https://github.com/Sorunome/mx-puppet-twitter) bridge to [Twitter](https://twitter.com) (optional)

- [sorunome/mx-puppet-discord](https://hub.docker.com/r/sorunome/mx-puppet-discord) - the [mx-puppet-discord](https://github.com/matrix-discord/mx-puppet-discord) bridge to [Discord](https://discordapp.com) (optional)

- [icewind1991/mx-puppet-steam](https://hub.docker.com/r/icewind1991/mx-puppet-steam) - the [mx-puppet-steam](https://github.com/icewind1991/mx-puppet-steam) bridge to [Steam](https://steampowered.com) (optional)

- [turt2live/matrix-dimension](https://hub.docker.com/r/turt2live/matrix-dimension) - the [Dimension](https://dimension.t2bot.io/) integrations manager (optional)

- [jitsi/web](https://hub.docker.com/r/jitsi/web) - the [Jitsi](https://jitsi.org/) web UI (optional)

- [jitsi/jicofo](https://hub.docker.com/r/jitsi/jicofo) - the [Jitsi](https://jitsi.org/) Focus component (optional)

- [jitsi/prosody](https://hub.docker.com/r/jitsi/prosody) - the [Jitsi](https://jitsi.org/) Prosody XMPP server component (optional)

- [jitsi/jvb](https://hub.docker.com/r/jitsi/jvb) - the [Jitsi](https://jitsi.org/) Video Bridge component (optional)

- [anoa/matrix-reminder-bot](https://hub.docker.com/r/anoa/matrix-reminder-bot) - the [matrix-reminder-bot](https://github.com/anoadragon453/matrix-reminder-bot) bot for one-off & recurring reminders and alarms (optional)

- [awesometechnologies/synapse-admin](https://hub.docker.com/r/awesometechnologies/synapse-admin) - the [synapse-admin](https://github.com/Awesome-Technologies/synapse-admin) web UI tool for administrating users and rooms on your Matrix server (optional)


## Deficiencies

This Ansible playbook can be improved in the following ways:

- setting up automatic backups to one or more storage providers


## Support

- Matrix room: [#matrix-docker-ansible-deploy:devture.com](https://matrix.to/#/#matrix-docker-ansible-deploy:devture.com)

- IRC channel: `#matrix-docker-ansible-deploy` on the [Freenode](https://freenode.net/) IRC network (irc.freenode.net)

- Github issues: [spantaleev/matrix-docker-ansible-deploy/issues](https://github.com/spantaleev/matrix-docker-ansible-deploy/issues)
