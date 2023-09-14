# Configuring the Ansible playbook

To configure the playbook, you need to have done the following things:

- have a server where Matrix services will run
- [configured your DNS records](configuring-dns.md)
- [retrieved the playbook's source code](getting-the-playbook.md) to your computer

You can then follow these steps inside the playbook directory:

1. create a directory to hold your configuration (`mkdir inventory/host_vars/matrix.<your-domain>`)

1. copy the sample configuration file (`cp examples/vars.yml inventory/host_vars/matrix.<your-domain>/vars.yml`)

1. edit the configuration file (`inventory/host_vars/matrix.<your-domain>/vars.yml`) to your liking. You may also take a look at the various `roles/*/ROLE_NAME_HERE/defaults/main.yml` files and see if there's something you'd like to copy over and override in your `vars.yml` configuration file.

1. copy the sample inventory hosts file (`cp examples/hosts inventory/hosts`)

1. edit the inventory hosts file (`inventory/hosts`) to your liking

1. (optional, advanced) to run Ansible against multiple servers with different `sudo` credentials, you can copy the sample inventory hosts yaml file for each of your hosts: (`cp examples/host.yml inventory/my_host1.yml` …) and use the [`ansible-all-hosts.sh`](../inventory/scripts/ansible-all-hosts.sh) script [in the installation step](installing.md).

For a basic Matrix installation, that's all you need.
For a more custom setup, see the [Other configuration options](#other-configuration-options) below.

When you're done with all the configuration you'd like to do, continue with [Installing](installing.md).


## Other configuration options

### Additional useful services

- [Setting up the Dimension Integration Manager](configuring-playbook-dimension.md) (optional; [unmaintained](https://github.com/spantaleev/matrix-docker-ansible-deploy/issues/2806#issuecomment-1673559299); after [installing](installing.md))

- [Setting up the Jitsi video-conferencing platform](configuring-playbook-jitsi.md) (optional)

- [Setting up Etherpad](configuring-playbook-etherpad.md) (optional)

- [Setting up Dynamic DNS](configuring-playbook-dynamic-dns.md) (optional)

- [Enabling metrics and graphs (Prometheus, Grafana) for your Matrix server](configuring-playbook-prometheus-grafana.md) (optional)

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

- [Serving your base domain using this playbook's nginx server](configuring-playbook-base-domain-serving.md) (optional)

- [Configure the Traefik reverse-proxy](configuring-playbook-traefik.md) (optional, advanced)

- (Deprecated) [Configure the Nginx reverse-proxy](configuring-playbook-nginx.md) (optional, advanced)

- [Using your own webserver, instead of this playbook's default reverse-proxy](configuring-playbook-own-webserver.md) (optional, advanced)

- [Adjusting TURN server configuration](configuring-playbook-turn.md) (optional, advanced)


### Server connectivity

- [Enabling Telemetry for your Matrix server](configuring-playbook-telemetry.md) (optional)

- [Controlling Matrix federation](configuring-playbook-federation.md) (optional)

- [Adjusting email-sending settings](configuring-playbook-email.md) (optional)

- [Setting up Hydrogen](configuring-playbook-client-hydrogen.md) - a new lightweight matrix client with legacy and mobile browser support (optional)

- [Setting up Cinny](configuring-playbook-client-cinny.md) - a web client focusing primarily on simple, elegant and secure interface (optional)

- [Setting up SchildiChat](configuring-playbook-client-schildichat.md) - a web client based on [Element](https://element.io/) with some extras and tweaks (optional)


### Authentication and user-related

- [Setting up an ma1sd Identity Server](configuring-playbook-ma1sd.md) (optional)

- [Setting up Synapse Admin](configuring-playbook-synapse-admin.md) (optional)

- [Setting up matrix-registration](configuring-playbook-matrix-registration.md) (optional)

- [Setting up the REST authentication password provider module](configuring-playbook-rest-auth.md) (optional, advanced)

- [Setting up the Shared Secret Auth password provider module](configuring-playbook-shared-secret-auth.md) (optional, advanced)

- [Setting up the LDAP password provider module](configuring-playbook-ldap-auth.md) (optional, advanced)

- [Setting up the ldap-registration-proxy](configuring-playbook-matrix-ldap-registration-proxy.md) (optional, advanced)

- [Setting up Synapse Simple Antispam](configuring-playbook-synapse-simple-antispam.md) (optional, advanced)

- [Setting up Matrix Corporal](configuring-playbook-matrix-corporal.md) (optional, advanced)

- [Matrix User Verification Service](configuring-playbook-user-verification-service.md) (optional, advanced)


### Bridging other networks

- [Setting up Mautrix Discord bridging](configuring-playbook-bridge-mautrix-discord.md) (optional)

- [Setting up Mautrix Telegram bridging](configuring-playbook-bridge-mautrix-telegram.md) (optional)

- [Setting up Mautrix Slack bridging](configuring-playbook-bridge-mautrix-slack.md) (optional)

- [Setting up Mautrix Google Messages bridging](configuring-playbook-bridge-mautrix-gmessages.md) (optional)

- [Setting up Mautrix Whatsapp bridging](configuring-playbook-bridge-mautrix-whatsapp.md) (optional)

- [Setting up Mautrix Facebook bridging](configuring-playbook-bridge-mautrix-facebook.md) (optional)

- [Setting up Mautrix Hangouts bridging](configuring-playbook-bridge-mautrix-hangouts.md) (optional)

- [Setting up Mautrix Google Chat bridging](configuring-playbook-bridge-mautrix-googlechat.md) (optional)

- [Setting up Mautrix Instagram bridging](configuring-playbook-bridge-mautrix-instagram.md) (optional)

- [Setting up Mautrix Twitter bridging](configuring-playbook-bridge-mautrix-twitter.md) (optional)

- [Setting up Mautrix Signal bridging](configuring-playbook-bridge-mautrix-signal.md) (optional)

- [Setting up Mautrix wsproxy for bridging Android SMS or Apple iMessage](configuring-playbook-bridge-mautrix-wsproxy.md) (optional)

- [Setting up Appservice IRC bridging](configuring-playbook-bridge-appservice-irc.md) (optional)

- [Setting up Appservice Discord bridging](configuring-playbook-bridge-appservice-discord.md) (optional)

- [Setting up Appservice Slack bridging](configuring-playbook-bridge-appservice-slack.md) (optional)

- [Setting up Appservice Webhooks bridging](configuring-playbook-bridge-appservice-webhooks.md) (optional)

- [Setting up Appservice Kakaotalk bridging](configuring-playbook-bridge-appservice-kakaotalk.md) (optional)

- [Setting up Beeper LinkedIn bridging](configuring-playbook-bridge-beeper-linkedin.md) (optional)

- [Setting up matrix-hookshot](configuring-playbook-bridge-hookshot.md) - a bridge between Matrix and multiple project management services, such as [GitHub](https://github.com), [GitLab](https://about.gitlab.com) and [JIRA](https://www.atlassian.com/software/jira). (optional)

- ~~[Setting up MX Puppet Skype bridging](configuring-playbook-bridge-mx-puppet-skype.md)~~ (optional) - this component has been broken for a long time, so it has been removed from the playbook. Consider [Setting up Go Skype Bridge bridging](configuring-playbook-bridge-go-skype-bridge.md)

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


### Bots

- [Setting up matrix-bot-chatgpt](configuring-playbook-bot-chatgpt.md) - a bot through which you can talk to the [ChatGPT](https://openai.com/blog/chatgpt/) model(optional)

- [Setting up matrix-reminder-bot](configuring-playbook-bot-matrix-reminder-bot.md) - a bot to remind you about stuff (optional)

- [Setting up matrix-registration-bot](configuring-playbook-bot-matrix-registration-bot.md) - a bot to create and manage registration tokens to invite users (optional)

- [Setting up maubot](configuring-playbook-bot-maubot.md) - a plugin-based Matrix bot system (optional)

- [Setting up honoroit](configuring-playbook-bot-honoroit.md) - a helpdesk bot (optional)

- [Setting up Go-NEB](configuring-playbook-bot-go-neb.md) - an extensible multifunctional bot (optional)

- [Setting up Mjolnir](configuring-playbook-bot-mjolnir.md) - a moderation tool/bot (optional)

- [Setting up Draupnir](configuring-playbook-bot-draupnir.md) - a moderation tool/bot, forked from Mjolnir and maintained by its former leader developer (optional)

- [Setting up Buscarron](configuring-playbook-bot-buscarron.md) - a bot you can use to send any form (HTTP POST, HTML) to a (encrypted) Matrix room (optional)


### Backups

- [Setting up borg backup](configuring-playbook-backup-borg.md) - a full Matrix server backup solution, including the Postgres database (optional)

- [Setting up postgres backup](configuring-playbook-postgres-backup.md) - a Postgres-database backup solution (note: does not include other files) (optional)


### Other specialized services

- [Setting up synapse-auto-compressor](configuring-playbook-synapse-auto-compressor.md) for compressing the database on Synapse homeservers (optional)

- [Setting up the Sliding Sync Proxy](configuring-playbook-sliding-sync-proxy.md) for clients which require Sliding Sync support (like Element X) (optional)

- [Setting up the Sygnal push gateway](configuring-playbook-sygnal.md) (optional)

- [Setting up the ntfy push notifications server](configuring-playbook-ntfy.md) (optional)

- [Setting up a Cactus Comments server](configuring-playbook-cactus-comments.md) - a federated comment system built on Matrix (optional)

- [Setting up the Rageshake bug report server](configuring-playbook-rageshake.md) (optional)
