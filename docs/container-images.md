# Container Images used by the playbook

This page summarizes the container ([Docker](https://www.docker.com/)) images used by the playbook when setting up your server.

We try to stick to official images (provided by their respective projects) as much as possible.


## Container images used by default

These services are enabled and used by default, but you can turn them off, if you wish.

- [matrixdotorg/synapse](https://hub.docker.com/r/matrixdotorg/synapse/) - the official [Synapse](https://github.com/matrix-org/synapse) Matrix homeserver (optional)

- [instrumentisto/coturn](https://hub.docker.com/r/instrumentisto/coturn/) - the [Coturn](https://github.com/coturn/coturn) STUN/TURN server (optional)

- [vectorim/element-web](https://hub.docker.com/r/vectorim/element-web/) - the [Element](https://element.io/) web client (optional)

- [ma1uta/ma1sd](https://hub.docker.com/r/ma1uta/ma1sd/) - the [ma1sd](https://github.com/ma1uta/ma1sd) Matrix Identity server (optional)

- [postgres](https://hub.docker.com/_/postgres/) - the [Postgres](https://www.postgresql.org/) database server (optional)

- [devture/exim-relay](https://hub.docker.com/r/devture/exim-relay/) - the [Exim](https://www.exim.org/) email server (optional)

- [nginx](https://hub.docker.com/_/nginx/) - the [nginx](http://nginx.org/) web server (optional)

- [certbot/certbot](https://hub.docker.com/r/certbot/certbot/) - the [certbot](https://certbot.eff.org/) tool for obtaining SSL certificates from [Let's Encrypt](https://letsencrypt.org/) (optional)


## Optional other container images we may use

These services are not part of our default installation, but can be enabled by [configuring the playbook](configuring-playbook.md) (either before the initial installation or any time later):

- [ewoutp/goofys](https://hub.docker.com/r/ewoutp/goofys/) - the [Goofys](https://github.com/kahing/goofys) Amazon [S3](https://aws.amazon.com/s3/) file-system-mounting program (optional)

- [etherpad/etherpad](https://hub.docker.com/r/etherpad/etherpad/) - the [Etherpad](https://etherpad.org) realtime collaborative text editor that can be used in a Jitsi audio/video call or integrated as a widget into Matrix chat rooms via the Dimension integration manager (optional)

- [devture/email2matrix](https://hub.docker.com/r/devture/email2matrix/) - the [Email2Matrix](https://github.com/devture/email2matrix) email server, which can relay email messages to Matrix rooms (optional)

- [devture/matrix-corporal](https://hub.docker.com/r/devture/matrix-corporal/) - [Matrix Corporal](https://github.com/devture/matrix-corporal): reconciliator and gateway for a managed Matrix server (optional)

- [zeratax/matrix-registration](https://hub.docker.com/r/devture/zeratax-matrix-registration/) - [matrix-registration](https://github.com/ZerataX/matrix-registration): a simple python application to have a token based matrix registration (optional)

- [tulir/mautrix-telegram](https://mau.dev/tulir/mautrix-telegram/container_registry) - the [mautrix-telegram](https://github.com/tulir/mautrix-telegram) bridge to [Telegram](https://telegram.org/) (optional)

- [tulir/mautrix-whatsapp](https://mau.dev/tulir/mautrix-whatsapp/container_registry) - the [mautrix-whatsapp](https://github.com/tulir/mautrix-whatsapp) bridge to [Whatsapp](https://www.whatsapp.com/) (optional)

- [tulir/mautrix-facebook](https://mau.dev/tulir/mautrix-facebook/container_registry) - the [mautrix-facebook](https://github.com/tulir/mautrix-facebook) bridge to [Facebook](https://facebook.com/) (optional)

- [tulir/mautrix-hangouts](https://mau.dev/tulir/mautrix-hangouts/container_registry) - the [mautrix-hangouts](https://github.com/tulir/mautrix-hangouts) bridge to [Google Hangouts](https://en.wikipedia.org/wiki/Google_Hangouts) (optional)

- [tulir/mautrix-instagram](https://mau.dev/tulir/mautrix-instagram/container_registry) - the [mautrix-instagram](https://github.com/tulir/mautrix-instagram) bridge to [Instagram](https://instagram.com/) (optional)

- [tulir/mautrix-signal](https://mau.dev/tulir/mautrix-signal/container_registry) - the [mautrix-signal](https://github.com/tulir/mautrix-signal) bridge to [Signal](https://www.signal.org/) (optional)

- [matrixdotorg/matrix-appservice-irc](https://hub.docker.com/r/matrixdotorg/matrix-appservice-irc) - the [matrix-appservice-irc](https://github.com/matrix-org/matrix-appservice-irc) bridge to [IRC](https://wikipedia.org/wiki/Internet_Relay_Chat) (optional)

- [halfshot/matrix-appservice-discord](https://hub.docker.com/r/halfshot/matrix-appservice-discord) - the [matrix-appservice-discord](https://github.com/Half-Shot/matrix-appservice-discord) bridge to [Discord](https://discordapp.com/) (optional)

- [cadair/matrix-appservice-slack](https://hub.docker.com/r/cadair/matrix-appservice-slack) - the [matrix-appservice-slack](https://github.com/matrix-org/matrix-appservice-slack) bridge to [Slack](https://slack.com/) (optional)

- [turt2live/matrix-appservice-webhooks](https://hub.docker.com/r/turt2live/matrix-appservice-webhooks) - the [Appservice Webhooks](https://github.com/turt2live/matrix-appservice-webhooks) bridge (optional)

- [folivonet/matrix-sms-bridge](https://hub.docker.com/repository/docker/folivonet/matrix-sms-bridge) - the [matrix-sms-bridge](https://github.com/benkuly/matrix-sms-bridge) (optional)

- [sorunome/mx-puppet-skype](https://hub.docker.com/r/sorunome/mx-puppet-skype) - the [mx-puppet-skype](https://github.com/Sorunome/mx-puppet-skype) bridge to [Skype](https://www.skype.com) (optional)

- [sorunome/mx-puppet-slack](https://hub.docker.com/r/sorunome/mx-puppet-slack) - the [mx-puppet-slack](https://github.com/Sorunome/mx-puppet-slack) bridge to [Slack](https://slack.com) (optional)

- [sorunome/mx-puppet-instagram](https://hub.docker.com/r/sorunome/mx-puppet-instagram) - the [mx-puppet-instagram](https://github.com/Sorunome/mx-puppet-instagram) bridge to [Instagram](https://www.instagram.com) (optional)

- [sorunome/mx-puppet-twitter](https://hub.docker.com/r/sorunome/mx-puppet-twitter) - the [mx-puppet-twitter](https://github.com/Sorunome/mx-puppet-twitter) bridge to [Twitter](https://twitter.com) (optional)

- [sorunome/mx-puppet-discord](https://hub.docker.com/r/sorunome/mx-puppet-discord) - the [mx-puppet-discord](https://github.com/matrix-discord/mx-puppet-discord) bridge to [Discord](https://discordapp.com) (optional)

- [xangelix/mx-puppet-groupme](https://hub.docker.com/r/xangelix/mx-puppet-groupme) - the [mx-puppet-groupme](https://gitlab.com/robintown/mx-puppet-groupme) bridge to [GroupMe](https://groupme.com/) (optional)

- [icewind1991/mx-puppet-steam](https://hub.docker.com/r/icewind1991/mx-puppet-steam) - the [mx-puppet-steam](https://github.com/icewind1991/mx-puppet-steam) bridge to [Steam](https://steampowered.com) (optional)

- [turt2live/matrix-dimension](https://hub.docker.com/r/turt2live/matrix-dimension) - the [Dimension](https://dimension.t2bot.io/) integrations manager (optional)

- [jitsi/web](https://hub.docker.com/r/jitsi/web) - the [Jitsi](https://jitsi.org/) web UI (optional)

- [jitsi/jicofo](https://hub.docker.com/r/jitsi/jicofo) - the [Jitsi](https://jitsi.org/) Focus component (optional)

- [jitsi/prosody](https://hub.docker.com/r/jitsi/prosody) - the [Jitsi](https://jitsi.org/) Prosody XMPP server component (optional)

- [jitsi/jvb](https://hub.docker.com/r/jitsi/jvb) - the [Jitsi](https://jitsi.org/) Video Bridge component (optional)

- [anoa/matrix-reminder-bot](https://hub.docker.com/r/anoa/matrix-reminder-bot) - the [matrix-reminder-bot](https://github.com/anoadragon453/matrix-reminder-bot) bot for one-off & recurring reminders and alarms (optional)

- [matrixdotorg/go-neb](https://hub.docker.com/r/matrixdotorg/go-neb) - the [Go-NEB](https://github.com/matrix-org/go-neb) bot (optional)

- [matrixdotorg/mjolnir](https://hub.docker.com/r/matrixdotorg/mjolnir) - the [mjolnir](https://github.com/matrix-org/mjolnir) moderation bot (optional)

- [awesometechnologies/synapse-admin](https://hub.docker.com/r/awesometechnologies/synapse-admin) - the [synapse-admin](https://github.com/Awesome-Technologies/synapse-admin) web UI tool for administrating users and rooms on your Matrix server (optional)

- [prom/prometheus](https://hub.docker.com/r/prom/prometheus/) - [Prometheus](https://github.com/prometheus/prometheus/) is a systems and service monitoring system

- [prom/node-exporter](https://hub.docker.com/r/prom/node-exporter/) - [Prometheus Node Exporter](https://github.com/prometheus/node_exporter/) is an addon for Prometheus that gathers standard system metrics

- [grafana/grafana](https://hub.docker.com/r/grafana/grafana/) - [Grafana](https://github.com/grafana/grafana/) is a graphing tool that works well with the above two images. Our playbook also adds two dashboards for [Synapse](https://github.com/matrix-org/synapse/tree/master/contrib/grafana) and  [Node Exporter](https://github.com/rfrail3/grafana-dashboards)

- [matrixdotorg/sygnal](https://hub.docker.com/r/matrixdotorg/sygnal/) - [Sygnal](https://github.com/matrix-org/sygnal) is a reference Push Gateway for Matrix
