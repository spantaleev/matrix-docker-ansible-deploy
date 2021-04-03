# Configuring the Ansible playbook

To configure the playbook, you need to have done the following things:

- have a server where Matrix services will run
- [configured your DNS records](configuring-dns.md)
- [retrieved the playbook's source code](getting-the-playbook.md) to your computer

You can then follow these steps inside the playbook directory:

1. create a directory to hold your configuration (`mkdir inventory/host_vars/matrix.<your-domain>`)

1. copy the sample configuration file (`cp examples/vars.yml inventory/host_vars/matrix.<your-domain>/vars.yml`)

1. edit the configuration file (`inventory/host_vars/matrix.<your-domain>/vars.yml`) to your liking. You may also take a look at the various `roles/ROLE_NAME_HERE/defaults/main.yml` files and see if there's something you'd like to copy over and override in your `vars.yml` configuration file.

1. copy the sample inventory hosts file (`cp examples/hosts inventory/hosts`)

1. edit the inventory hosts file (`inventory/hosts`) to your liking


For a basic Matrix installation, that's all you need.
For a more custom setup, see the [Other configuration options](#other-configuration-options) below.

When you're done with all the configuration you'd like to do, continue with [Installing](installing.md).


## Other configuration options

### Additional useful services

- [Setting up the Dimension Integration Manager](configuring-playbook-dimension.md) (optional, but recommended; after [installing](installing.md))

- [Setting up the Jitsi video-conferencing platform](configuring-playbook-jitsi.md) (optional)

- [Setting up Dynamic DNS](configuring-playbook-dynamic-dns.md) (optional)

- [Enabling metrics and graphs (Prometheus, Grafana) for your Matrix server](configuring-playbook-prometheus-grafana.md) (optional)

### Core service adjustments

- [Configuring Synapse](configuring-playbook-synapse.md) (optional)

- [Configuring Element](configuring-playbook-client-element.md) (optional)

- [Storing Matrix media files on Amazon S3](configuring-playbook-s3.md) (optional)

- [Using an external PostgreSQL server](configuring-playbook-external-postgres.md) (optional)

- [Adjusting ma1sd Identity Server configuration](configuring-playbook-ma1sd.md) (optional)

- [Adjusting SSL certificate retrieval](configuring-playbook-ssl-certificates.md) (optional, advanced)

- [Serving your base domain using this playbook's nginx server](configuring-playbook-base-domain-serving.md) (optional)

- [Configure Nginx (optional, advanced)](configuring-playbook-nginx.md) (optional, advanced)

- [Using your own webserver, instead of this playbook's nginx proxy](configuring-playbook-own-webserver.md) (optional, advanced)

- [Adjusting TURN server configuration](configuring-playbook-turn.md) (optional, advanced)


### Server connectivity

- [Enabling Telemetry for your Matrix server](configuring-playbook-telemetry.md) (optional)

- [Controlling Matrix federation](configuring-playbook-federation.md) (optional)

- [Adjusting email-sending settings](configuring-playbook-email.md) (optional)


### Authentication and user-related

- [Setting up Synapse Admin](configuring-playbook-synapse-admin.md) (optional)

- [Setting up matrix-registration](configuring-playbook-matrix-registration.md) (optional)

- [Setting up the REST authentication password provider module](configuring-playbook-rest-auth.md) (optional, advanced)

- [Setting up the Shared Secret Auth password provider module](configuring-playbook-shared-secret-auth.md) (optional, advanced)

- [Setting up the LDAP password provider module](configuring-playbook-ldap-auth.md) (optional, advanced)

- [Setting up Synapse Simple Antispam](configuring-playbook-synapse-simple-antispam.md) (optional, advanced)

- [Setting up Matrix Corporal](configuring-playbook-matrix-corporal.md) (optional, advanced)


### Bridging other networks

- [Setting up Mautrix Telegram bridging](configuring-playbook-bridge-mautrix-telegram.md) (optional)

- [Setting up Mautrix Whatsapp bridging](configuring-playbook-bridge-mautrix-whatsapp.md) (optional)

- [Setting up Mautrix Facebook bridging](configuring-playbook-bridge-mautrix-facebook.md) (optional)

- [Setting up Mautrix Hangouts bridging](configuring-playbook-bridge-mautrix-hangouts.md) (optional)

- [Setting up Mautrix Instagram bridging](configuring-playbook-bridge-mautrix-instagram.md) (optional)

- [Setting up Mautrix Signal bridging](configuring-playbook-bridge-mautrix-signal.md) (optional)

- [Setting up Appservice IRC bridging](configuring-playbook-bridge-appservice-irc.md) (optional)

- [Setting up Appservice Discord bridging](configuring-playbook-bridge-appservice-discord.md) (optional)

- [Setting up Appservice Slack bridging](configuring-playbook-bridge-appservice-slack.md) (optional)

- [Setting up Appservice Webhooks bridging](configuring-playbook-bridge-appservice-webhooks.md) (optional)

- [Setting up MX Puppet Skype bridging](configuring-playbook-bridge-mx-puppet-skype.md) (optional)

- [Setting up MX Puppet Slack bridging](configuring-playbook-bridge-mx-puppet-slack.md) (optional)

- [Setting up MX Puppet Instagram bridging](configuring-playbook-bridge-mx-puppet-instagram.md) (optional)

- [Setting up MX Puppet Twitter bridging](configuring-playbook-bridge-mx-puppet-twitter.md) (optional)

- [Setting up MX Puppet Discord bridging](configuring-playbook-bridge-mx-puppet-discord.md) (optional)

- [Setting up MX Puppet GroupMe bridging](configuring-playbook-bridge-mx-puppet-groupme.md) (optional)

- [Setting up MX Puppet Steam bridging](configuring-playbook-bridge-mx-puppet-steam.md) (optional)

- [Setting up Email2Matrix](configuring-playbook-email2matrix.md) (optional)

- [Setting up Matrix SMS bridging](configuring-playbook-bridge-matrix-bridge-sms.md) (optional)


### Bots

- [Setting up matrix-reminder-bot](configuring-playbook-bot-matrix-reminder-bot.md) - a bot to remind you about stuff (optional)

- [Setting up Go-NEB](configuring-playbook-bot-go-neb.md) - an extensible multifunctional bot (optional)

- [Setting up Mjolnir](configuring-playbook-bot-mjolnir.md) - a moderation tool/bot (optional)


### Other specialized services

- [Setting up the Sygnal push gateway](configuring-playbook-sygnal.md) (optional)
