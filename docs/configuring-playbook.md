# Configuring the Ansible playbook

To configure the playbook, you need to have done the following things:

- have a server where Matrix services will run
- [configured your DNS records](configuring-dns.md)
- [retrieved the playbook's source code](getting-the-playbook.md) to your computer

You can then follow these steps inside the playbook directory:

1. create a directory to hold your configuration (`mkdir -p inventory/host_vars/matrix.example.com` where `example.com` is your "base domain")

2. copy the sample configuration file (`cp examples/vars.yml inventory/host_vars/matrix.example.com/vars.yml`)

3. edit the configuration file (`inventory/host_vars/matrix.example.com/vars.yml`) to your liking. You may also take a look at the various `roles/*/ROLE_NAME_HERE/defaults/main.yml` files and see if there's something you'd like to copy over and override in your `vars.yml` configuration file.

4. copy the sample inventory hosts file (`cp examples/hosts inventory/hosts`)

5. edit the inventory hosts file (`inventory/hosts`) to your liking

6. (optional, advanced) you may wish to keep your `inventory` directory under version control with [git](https://git-scm.com/) or any other version-control system.

7. (optional, advanced) to run Ansible against multiple servers with different `sudo` credentials, you can copy the sample inventory hosts yaml file for each of your hosts: (`cp examples/host.yml inventory/my_host1.yml` …) and use the [`ansible-all-hosts.sh`](../bin/ansible-all-hosts.sh) script [in the installation step](installing.md).

For a basic Matrix installation, that's all you need.

For a more custom setup, see the [Other configuration options](#other-configuration-options) below.

When you're done with all the configuration you'd like to do, continue with [Installing](installing.md).


## Other configuration options

### Additional useful services

- [Setting up the Jitsi video-conferencing platform](configuring-playbook-jitsi.md) (optional)

- [Setting up Etherpad](configuring-playbook-etherpad.md) (optional)

- [Setting up Dynamic DNS](configuring-playbook-dynamic-dns.md) (optional)

- [Enabling metrics and graphs (Prometheus, Grafana) for your Matrix server](configuring-playbook-prometheus-grafana.md) (optional)

- [Enabling synapse-usage-exporter for Synapse usage statistics](configuring-playbook-synapse-usage-exporter.md) (optional)

### Core service adjustments

- Homeserver configuration:
  - [Configuring Synapse](configuring-playbook-synapse.md), if you're going with the default/recommended homeserver implementation (optional)

  - [Configuring Conduit](configuring-playbook-conduit.md), if you've switched to the [Conduit](https://conduit.rs) homeserver implementation (optional)

  - [Configuring Dendrite](configuring-playbook-dendrite.md), if you've switched to the [Dendrite](https://matrix-org.github.io/dendrite) homeserver implementation (optional)

- [Configuring Element](configuring-playbook-client-element.md) (optional)

- [Storing Matrix media files using matrix-media-repo](configuring-playbook-matrix-media-repo.md) (optional)

- [Storing Matrix media files on Amazon S3](configuring-playbook-s3.md) (optional)

- [Using an external PostgreSQL server](configuring-playbook-external-postgres.md) (optional)

- [Adjusting SSL certificate retrieval](configuring-playbook-ssl-certificates.md) (optional, advanced)

- [Serving the base domain](configuring-playbook-base-domain-serving.md) (optional)

- [Configuring the Traefik reverse-proxy](configuring-playbook-traefik.md) (optional, advanced)

- [Using your own webserver, instead of this playbook's Traefik reverse-proxy](configuring-playbook-own-webserver.md) (optional, advanced)

- [Adjusting TURN server configuration](configuring-playbook-turn.md) (optional, advanced)


### Server connectivity

- [Enabling Telemetry for your Matrix server](configuring-playbook-telemetry.md) (optional)

- [Controlling Matrix federation](configuring-playbook-federation.md) (optional)

- [Adjusting email-sending settings](configuring-playbook-email.md) (optional)

- [Setting up Hydrogen](configuring-playbook-client-hydrogen.md) - a new lightweight Matrix client with legacy and mobile browser support (optional)

- [Setting up Cinny](configuring-playbook-client-cinny.md) - a web client focusing primarily on simple, elegant and secure interface (optional)

- [Setting up SchildiChat](configuring-playbook-client-schildichat.md) - a web client based on [Element](https://element.io/) with some extras and tweaks (optional)


### Authentication and user-related

- [Setting up Matrix Authentication Service](configuring-playbook-matrix-authentication-service.md) (Next-generation auth for Matrix, based on OAuth 2.0/OIDC) (optional)

- [Setting up Appservice Double Puppet](configuring-playbook-appservice-double-puppet.md) (optional)

- [Setting up ma1sd Identity Server](configuring-playbook-ma1sd.md) (optional)

- [Setting up Synapse Admin](configuring-playbook-synapse-admin.md) (optional)

- [Setting up matrix-registration](configuring-playbook-matrix-registration.md) (optional)

- [Setting up the REST authentication password provider module](configuring-playbook-rest-auth.md) (optional, advanced)

- [Setting up the Shared Secret Auth password provider module](configuring-playbook-shared-secret-auth.md) (optional, advanced)

- [Setting up the LDAP authentication password provider module](configuring-playbook-ldap-auth.md) (optional, advanced)

- [Setting up matrix-ldap-registration-proxy](configuring-playbook-matrix-ldap-registration-proxy.md) (optional, advanced)

- [Setting up Synapse Simple Antispam](configuring-playbook-synapse-simple-antispam.md) (optional, advanced)

- [Setting up Matrix Corporal](configuring-playbook-matrix-corporal.md) (optional, advanced)

- [Setting up Matrix User Verification Service](configuring-playbook-user-verification-service.md) (optional, advanced)

- [Setting up Pantalaimon (E2EE aware proxy daemon)](configuring-playbook-pantalaimon.md) (optional, advanced)


### Bridging other networks

- [Setting up Mautrix Discord bridging](configuring-playbook-bridge-mautrix-discord.md) (optional)

- [Setting up Mautrix Telegram bridging](configuring-playbook-bridge-mautrix-telegram.md) (optional)

- [Setting up Mautrix Slack bridging](configuring-playbook-bridge-mautrix-slack.md) (optional)

- [Setting up Mautrix Google Messages bridging](configuring-playbook-bridge-mautrix-gmessages.md) (optional)

- [Setting up Mautrix Whatsapp bridging](configuring-playbook-bridge-mautrix-whatsapp.md) (optional)

- [Setting up Instagram bridging via Mautrix Meta](configuring-playbook-bridge-mautrix-meta-instagram.md) (optional)

- [Setting up Messenger bridging via Mautrix Meta](configuring-playbook-bridge-mautrix-meta-messenger.md) (optional)

- [Setting up Mautrix Google Chat bridging](configuring-playbook-bridge-mautrix-googlechat.md) (optional)

- [Setting up Mautrix Twitter bridging](configuring-playbook-bridge-mautrix-twitter.md) (optional)

- [Setting up Mautrix Signal bridging](configuring-playbook-bridge-mautrix-signal.md) (optional)

- [Setting up Mautrix wsproxy for bridging Android SMS or Apple iMessage](configuring-playbook-bridge-mautrix-wsproxy.md) (optional)

- [Setting up Appservice IRC bridging](configuring-playbook-bridge-appservice-irc.md) (optional)

- [Setting up Appservice Discord bridging](configuring-playbook-bridge-appservice-discord.md) (optional)

- [Setting up Appservice Slack bridging](configuring-playbook-bridge-appservice-slack.md) (optional)

- [Setting up Appservice Kakaotalk bridging](configuring-playbook-bridge-appservice-kakaotalk.md) (optional)

- [Setting up Beeper LinkedIn bridging](configuring-playbook-bridge-beeper-linkedin.md) (optional)

- [Setting up matrix-hookshot](configuring-playbook-bridge-hookshot.md) - a bridge between Matrix and multiple project management services, such as [GitHub](https://github.com), [GitLab](https://about.gitlab.com) and [JIRA](https://www.atlassian.com/software/jira). (optional)

- [Setting up MX Puppet Slack bridging](configuring-playbook-bridge-mx-puppet-slack.md) (optional)

- [Setting up MX Puppet Instagram bridging](configuring-playbook-bridge-mx-puppet-instagram.md) (optional)

- [Setting up MX Puppet Twitter bridging](configuring-playbook-bridge-mx-puppet-twitter.md) (optional)

- [Setting up MX Puppet Discord bridging](configuring-playbook-bridge-mx-puppet-discord.md) (optional)

- [Setting up MX Puppet GroupMe bridging](configuring-playbook-bridge-mx-puppet-groupme.md) (optional)

- [Setting up MX Puppet Steam bridging](configuring-playbook-bridge-mx-puppet-steam.md) (optional)

- [Setting up Go Skype Bridge bridging](configuring-playbook-bridge-go-skype-bridge.md) (optional)

- [Setting up Email2Matrix](configuring-playbook-email2matrix.md) (optional)

- [Setting up Postmoogle email bridging](configuring-playbook-bot-postmoogle.md) (optional)

- [Setting up Matrix SMS bridging](configuring-playbook-bridge-matrix-bridge-sms.md) (optional)

- [Setting up Heisenbridge bouncer-style IRC bridging](configuring-playbook-bridge-heisenbridge.md) (optional)

- [Setting up WeChat bridging](configuring-playbook-bridge-wechat.md) (optional)


### Bots

- [Setting up baibot](configuring-playbook-bot-baibot.md) - a bot through which you can talk to various [AI](https://en.wikipedia.org/wiki/Artificial_intelligence) / [Large Language Models](https://en.wikipedia.org/wiki/Large_language_model) services ([OpenAI](https://openai.com/)'s [ChatGPT](https://openai.com/blog/chatgpt/) and [others](https://github.com/etkecc/baibot/blob/main/docs/providers.md)) (optional)

- [Setting up matrix-reminder-bot](configuring-playbook-bot-matrix-reminder-bot.md) - a bot to remind you about stuff (optional)

- [Setting up matrix-registration-bot](configuring-playbook-bot-matrix-registration-bot.md) - a bot to create and manage registration tokens to invite users (optional)

- [Setting up maubot](configuring-playbook-bot-maubot.md) - a plugin-based Matrix bot system (optional)

- [Setting up Honoroit](configuring-playbook-bot-honoroit.md) - a helpdesk bot (optional)

- [Setting up Mjolnir](configuring-playbook-bot-mjolnir.md) - a moderation tool/bot (optional)

- [Setting up Draupnir](configuring-playbook-bot-draupnir.md) - a moderation tool/bot, forked from Mjolnir and maintained by its former leader developer (optional)

- [Setting up Draupnir for all/D4A](configuring-playbook-appservice-draupnir-for-all.md) - like the [Draupnir bot](configuring-playbook-bot-draupnir.md) mentioned above, but running in appservice mode and supporting multiple instances (optional)

- [Setting up Buscarron](configuring-playbook-bot-buscarron.md) - a bot you can use to send any form (HTTP POST, HTML) to a (encrypted) Matrix room (optional)


### Backups

- [Setting up BorgBackup](configuring-playbook-backup-borg.md) - a full Matrix server backup solution, including the Postgres database (optional)

- [Setting up postgres backup](configuring-playbook-postgres-backup.md) - a Postgres-database backup solution (note: does not include other files) (optional)


### Other specialized services

- [Setting up synapse-auto-compressor](configuring-playbook-synapse-auto-compressor.md) for compressing the database on Synapse homeservers (optional)

- [Setting up the Sliding Sync proxy](configuring-playbook-sliding-sync-proxy.md) for clients which require Sliding Sync support (like Element X) (optional)

- [Setting up the Sygnal push gateway](configuring-playbook-sygnal.md) (optional)

- [Setting up the ntfy push notifications server](configuring-playbook-ntfy.md) (optional)

- [Setting up Cactus Comments](configuring-playbook-cactus-comments.md) - a federated comment system built on Matrix (optional)

- [Setting up the rageshake bug report server](configuring-playbook-rageshake.md) (optional)

- [Setting up Prometheus Alertmanager integration via matrix-alertmanager-receiver](configuring-playbook-alertmanager-receiver.md) (optional)

### Deprecated / unmaintained / removed services

**Note**: since a deprecated or unmaintained service will not be updated, its bug or vulnerability will be unlikely to get patched. It is recommended to migrate from the service to an alternative if any, and make sure to do your own research before you decide to keep it running nonetheless.

- [Setting up Appservice Webhooks bridging](configuring-playbook-bridge-appservice-webhooks.md) (deprecated; the bridge's author suggests taking a look at [matrix-hookshot](https://github.com/matrix-org/matrix-hookshot) as a replacement, which can also be installed using [this playbook](configuring-playbook-bridge-hookshot.md))

- [Setting up the Dimension integration manager](configuring-playbook-dimension.md) ([unmaintained](https://github.com/spantaleev/matrix-docker-ansible-deploy/issues/2806#issuecomment-1673559299); after [installing](installing.md))

- [Setting up Go-NEB](configuring-playbook-bot-go-neb.md) (unmaintained; the bridge's author suggests taking a look at [matrix-hookshot](https://github.com/matrix-org/matrix-hookshot) as a replacement, which can also be installed using [this playbook](configuring-playbook-bridge-hookshot.md))

- [Setting up matrix-bot-chatgpt](configuring-playbook-bot-chatgpt.md) (unmaintained; the bridge's author suggests taking a look at [baibot](https://github.com/etkecc/baibot) as a replacement, which can also be installed using [this playbook](configuring-playbook-bot-baibot.md))

- [Setting up Mautrix Facebook bridging](configuring-playbook-bridge-mautrix-facebook.md) (deprecated in favor of the Messenger/Instagram bridge with [mautrix-meta-messenger](configuring-playbook-bridge-mautrix-meta-messenger.md))

- [Setting up Mautrix Hangouts bridging](configuring-playbook-bridge-mautrix-hangouts.md) (deprecated in favor of the Google Chat bridge with [mautrix-googlechat](configuring-playbook-bridge-mautrix-googlechat.md))

- [Setting up Mautrix Instagram bridging](configuring-playbook-bridge-mautrix-instagram.md) (deprecated in favor of the Messenger/Instagram bridge with [mautrix-meta-instagram](configuring-playbook-bridge-mautrix-meta-instagram.md))

- [Setting up MX Puppet Skype bridging](configuring-playbook-bridge-mx-puppet-skype.md) (removed; this component has been broken for a long time, so it has been removed from the playbook. Consider [setting up Go Skype Bridge bridging](configuring-playbook-bridge-go-skype-bridge.md))
