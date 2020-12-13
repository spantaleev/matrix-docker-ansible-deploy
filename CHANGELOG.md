# 2020-12-11

## synapse-janitor support removed

We've removed support for the unmaintained [synapse-janitor](https://github.com/xwiki-labs/synapse_scripts) script. There's been past reports of it corrupting the Synapse database. Since there hasn't been any new development on it and it doesn't seem too useful nowadays, there's no point in including it in the playbook.

If you need to clean up or compact your database, consider using the Synapse Admin APIs directly. See our [Synapse maintenance](docs/maintenance-synapse.md) and [Postgres maintenance](docs/maintenance-postgres.md) documentation pages for more details.


## Docker 20.10 is here

(No need to do anything special in relation to this. Just something to keep in mind)

Docker 20.10 got released recently and your server will likely get it the next time you update.

This is the first major Docker update in a long time and it packs a lot of changes.
Some of them introduced some breakage for us initially (see [here](https://github.com/spantaleev/matrix-docker-ansible-deploy/commit/d08b27784f222effcbce2abf924bf07bbe0893be) and [here](https://github.com/spantaleev/matrix-docker-ansible-deploy/commit/7593d969e316cc0144bce378a5be58c76c2c37ee)), but it should be all good now.


# 2020-12-08

## openid APIs exposed by default on the federation port when federation disabled

We've changed some defaults. People running with our default configuration (federation enabled), are not affected at all.

If you are running an unfederated server (`matrix_synapse_federation_enabled: false`), this may be of interest to you.

When federation is disabled, but ma1sd or Dimension are enabled, we'll now expose the `openid` APIs on the federation port.
These APIs are necessary for some ma1sd features to work. If you'd like to prevent this, you can: `matrix_synapse_federation_port_openid_resource_required: false`.


# 2020-11-27

## Recent Jitsi updates may require configuration changes

We've recently [updated from Jitsi build 4857 to build 5142](https://github.com/spantaleev/matrix-docker-ansible-deploy/pull/719), which brings a lot of configuration changes.

**If you use our default Jitsi settings, you won't have to do anything.**

People who have [fine-tuned Jitsi](docs/configuring-playbook-jitsi.md#optional-fine-tune-jitsi) may find that some options got renamed now, others are gone and yet others still need to be defined in another way.

The next time you run the playbook [installation](docs/installing.md) command, our validation logic will tell you if you're using some variables like that and will recommend a migration path for each one.

Additionally, we've recently disabled transcriptions (`matrix_jitsi_enable_transcriptions: false`) and recording (`matrix_jitsi_enable_recording: false`) by default. These features did not work anyway, because we don't install the required dependencies for them (Jigasi and Jibri, respectively). If you've been somehow pointing your Jitsi installation to some manually installed Jigasi/Jibri service, you may need to toggle these flags back to enabled to have transcriptions and recordings working.


# 2020-11-23

## Breaking change matrix-sms-bridge

Because of many problems using gammu as SMS provider, matrix-sms-bridge now uses (https://github.com/RebekkaMa/android-sms-gateway-server) by default. See (the docs)[./docs/configuring-playbook-bridge-matrix-bridge-sms.md] which new vars you need to add.

If you are using this playbook to deploy matrix-sms-bridge and still really want to use gammu as SMS provider, we could possibly add support for both android-sms-gateway-server and gammu.

# 2020-11-13

## Breaking change matrix-sms-bridge

The new version of [matrix-sms-bridge](https://github.com/benkuly/matrix-sms-bridge) changed its database from neo4j to h2. You need to sync the bridge at the first start. Note that this only will sync rooms where the @smsbot:yourServer is member. For rooms without @smsbot:yourServer you need to kick and invite the telephone number **or** invite @smsbot:yourServer.

1. Add the following to your `vars.yml` file: `matrix_sms_bridge_container_extra_arguments=['--env SPRING_PROFILES_ACTIVE=initialsync']`
2. Login to your host shell and remove old systemd file from your host: `rm /etc/systemd/system/matrix-sms-bridge-database.service`
2. Run `ansible-playbook -i inventory/hosts setup.yml --tags=setup-matrix-sms-bridge,start`
3. Login to your host shell and check the logs with `journalctl -u matrix-sms-bridge` until the sync finished.
4. Remove the var from the first step.
5. Run `ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start`.

# 2020-11-10

## Dynamic DNS support

Thanks to [Scott Crossen](https://github.com/scottcrossen), the playbook can now manage Dynamic DNS for you using [ddclient](https://ddclient.net/).

To learn more, follow our [Dynamic DNS docs page](docs/configuring-playbook-dynamic-dns.md).


# 2020-10-28

## (Compatibility Break) https://matrix.DOMAIN/ now redirects to https://element.DOMAIN/

Until now, we used to serve a static page coming from Synapse at `https://matrix.DOMAIN/`. This page was not very useful to anyone.

Since `matrix.DOMAIN` may be accessed by regular users in certain conditions, it's probably better to redirect them to a better place (e.g. to the [Element](docs/configuring-playbook-client-element.md) client).

If Element is installed (`matrix_client_element_enabled: true`, which it is by default), we now redirect people to it, instead of showing them a Synapse static page.

If you'd like to control where the redirect goes, use the `matrix_nginx_proxy_proxy_matrix_client_redirect_root_uri_to_domain` variable.
To restore the old behavior of not redirecting anywhere and serving the Synapse static page, set it to an empty value (`matrix_nginx_proxy_proxy_matrix_client_redirect_root_uri_to_domain: ""`).


# 2020-10-26

## (Compatibility Break) /_synapse/admin is no longer publicly exposed by default

We used to expose the Synapse Admin APIs publicly (at `https://matrix.DOMAIN/_synapse/admin`).
These APIs require authentication with a valid access token, so it's not that big a deal to expose them.

However, following [official Synapse's reverse-proxying recommendations](https://github.com/matrix-org/synapse/blob/master/docs/reverse_proxy.md#synapse-administration-endpoints), we're no longer exposing `/_synapse/admin` by default.

If you'd like to restore restore the old behavior and expose `/_synapse/admin` publicly, you can use the following configuration (in your `vars.yml`):

```yaml
matrix_nginx_proxy_proxy_matrix_client_api_forwarded_location_synapse_admin_api_enabled: true
```


# 2020-10-02

## Minimum Ansible version raised to v2.7.0

We were claiming to support [Ansible](https://www.ansible.com/) v2.5.2 and higher, but issues like [#662](https://github.com/spantaleev/matrix-docker-ansible-deploy/issues/662) demonstrate that we need at least v2.7.0.

If you've been using the playbook without getting any errors until now, you're probably on a version higher than that already (or you're not using the `matrix-ma1sd` and `matrix-client-element` roles).

Our [Ansible docs page](docs/ansible.md) contains information on how to run a more up-to-date version of Ansible.


# 2020-10-01

## Postgres 13 support

The playbook now installs [Postgres 13](https://www.postgresql.org/about/news/postgresql-13-released-2077/) by default.

If you have have an existing setup, it's likely running on an older Postgres version (9.x, 10.x, 11.x or 12.x). You can easily upgrade by following the [upgrading PostgreSQL guide](docs/maintenance-postgres.md#upgrading-postgresql).

# 2020-09-01

## matrix-registration support

The playbook can now help you set up [matrix-registration](https://github.com/ZerataX/matrix-registration) - an application that lets you keep your Matrix server's registration private, but still allow certain users (those having a unique registration link) to register by themselves.

See our [Setting up matrix-registration](docs/configuring-playbook-matrix-registration.md) documentation page to get started.


# 2020-08-21

## rust-synapse-compress-state support

The playbook can now help you use [rust-synapse-compress-state](https://github.com/matrix-org/rust-synapse-compress-state) to compress the state groups in your Synapse database.

See our [Compressing state with rust-synapse-compress-state](docs/maintenance-synapse.md#compressing-state-with-rust-synapse-compress-state) documentation page to get started.


# 2020-07-22

## Synapse Admin support

The playbook can now help you set up [synapse-admin](https://github.com/Awesome-Technologies/synapse-admin).

See our [Setting up Synapse Admin](docs/configuring-playbook-synapse-admin.md) documentation to get started.


# 2020-07-20

## matrix-reminder-bot support

The playbook can now help you set up [matrix-reminder-bot](https://github.com/anoadragon453/matrix-reminder-bot).

See our [Setting up matrix-reminder-bot](docs/configuring-playbook-bot-matrix-reminder-bot.md) documentation to get started.


# 2020-07-17

## (Compatibility Break) Riot is now Element

As per the official announcement, [Riot has been rebraned to Element](https://element.io/blog/welcome-to-element/).

The playbook follows suit. Existing installations have a few options for how to handle this.

See our [Migrating to Element](docs/configuring-playbook-riot-web.md#migrating-to-element) documentation page for more details.


# 2020-07-03

## Steam bridging support via mx-puppet-steam

Thanks to [Hugues Morisset](https://github.com/izissise)'s efforts, the playbook now supports bridging to [Steam](https://steamapp.com/) via the [mx-puppet-steam](https://github.com/icewind1991/mx-puppet-steam) bridge. See our [Setting up MX Puppet Steam bridging](docs/configuring-playbook-bridge-mx-puppet-steam.md) documentation page for getting started.


# 2020-07-01

## Discord bridging support via mx-puppet-discord

Thanks to [Hugues Morisset](https://github.com/izissise)'s efforts, the playbook now supports bridging to [Discord](https://discordapp.com/) via the [mx-puppet-discord](https://github.com/Sorunome/mx-puppet-discord) bridge. See our [Setting up MX Puppet Discord bridging](docs/configuring-playbook-bridge-mx-puppet-discord.md) documentation page for getting started.

**Note**: this is a new Discord bridge. The playbook still retains Discord bridging via [matrix-appservice-discord](docs/configuring-playbook-bridge-appservice-discord.md). You're free too use the bridge that serves you better, or even both (for different users and use-cases).


# 2020-06-30

## Instagram and Twitter bridging support

Thanks to [Johanna Dorothea Reichmann](https://github.com/jdreichmann)'s efforts, the playbook now supports bridging to [Instagram](https://www.instagram.com/) via the [mx-puppet-instagram](https://github.com/Sorunome/mx-puppet-instagram) bridge. See our [Setting up MX Puppet Instagram bridging](docs/configuring-playbook-bridge-mx-puppet-instagram.md) documentation page for getting started.

Thanks to [Tulir Asokan](https://github.com/tulir)'s efforts, the playbook now supports bridging to [Twitter](https://twitter.com/) via the [mx-puppet-twitter](https://github.com/Sorunome/mx-puppet-twitter) bridge. See our [Setting up MX Puppet Twitter bridging](docs/configuring-playbook-bridge-mx-puppet-twitter.md) documentation page for getting started.


# 2020-06-28

## (Post Mortem / fixed Security Issue) Re-enabling User Directory search powered by the ma1sd Identity Server

User Directory search requests used to go to the ma1sd identity server by default, which queried its own stores and the Synapse database.

ma1sd's [security issue](https://github.com/ma1uta/ma1sd/issues/44) has been fixed in version `2.4.0`, with [this commit](ma1uta/ma1sd@2bb5a734d11662b06471113cf3d6b4cee5e33a85). `ma1sd 2.4.0` is now the default version for this playbook. For more information on what happened, please check the mentioned issue.

We are re-enabling user directory search with this update. Those who would like to keep it disabled can use this configuration: `matrix_nginx_proxy_proxy_matrix_user_directory_search_enabled: false`

As always, re-running the playbook is enough to get the updated bits.

# 2020-06-11

## SMS bridging requires db reset

The current version of [matrix-sms-bridge](https://github.com/benkuly/matrix-sms-bridge) needs you to delete the database to work as expected. Just remove `/matrix/matrix-sms-bridge/database/*`. It also adds a new requried var `matrix_sms_bridge_default_region`.

To reuse your existing rooms, invite `@smsbot:yourServer` to the room or write a message. You are also able to use automated room creation with telephonenumers by writing `sms send -t 01749292923 "Hello World"` in a room with `@smsbot:yourServer`. See [the docs](https://github.com/benkuly/matrix-sms-bridge) for more information.

# 2020-06-05

## SMS bridging support

Thanks to [benkuly](https://github.com/benkuly)'s efforts, the playbook now supports bridging to SMS (with one telephone number only) via [matrix-sms-bridge](https://github.com/benkuly/matrix-sms-bridge).

See our [Setting up Matrix SMS bridging](docs/configuring-playbook-bridge-matrix-bridge-sms.md) documentation page for getting started.


# 2020-05-19

## (Compatibility Break / Security Issue) Disabling User Directory search powered by the ma1sd Identity Server

User Directory search requests used to go to the ma1sd identity server by default, which queried its own stores and the Synapse database.

ma1sd current has [a security issue](https://github.com/ma1uta/ma1sd/issues/44), which made it leak information about all users - including users created by bridges, etc.

Until the issue gets fixed, we're making User Directory search not go to ma1sd by default. You **need to re-run the playbook and restart services to apply this workaround**.

*If you insist on restoring the old behavior* (**which has a security issue!**), you *might* use this configuration: `matrix_nginx_proxy_proxy_matrix_user_directory_search_enabled: "{{ matrix_ma1sd_enabled }}"`


# 2020-04-28

## Newer IRC bridge (with potential breaking change)

This upgrades matrix-appservice-irc from 0.14.1 to 0.16.0.  Upstream
made a change to how you define manual mappings.  If you added a
`mapping` to your configuration, you will need to update it accoring
to the [upstream
instructions](https://github.com/matrix-org/matrix-appservice-irc/blob/master/CHANGELOG.md#0150-2020-02-05).
If you did not include `mappings` in your configuration for IRC, no
change is necessary.  `mappings` is not part of the default
configuration.


# 2020-04-23

## Slack bridging support

Thanks to [Rodrigo Belem](https://github.com/rbelem)'s efforts, the playbook now supports bridging to [Slack](https://slack.com) via the [mx-puppet-slack](https://github.com/Sorunome/mx-puppet-slack) bridge.

See our [Setting up MX Puppet Slack bridging](docs/configuring-playbook-bridge-mx-puppet-slack.md) documentation page for getting started.


# 2020-04-09

## Skype bridging support

Thanks to [Rodrigo Belem](https://github.com/rbelem)'s efforts, the playbook now supports bridging to [Skype](https://www.skype.com) via the [mx-puppet-skype](https://github.com/Sorunome/mx-puppet-skype) bridge.

See our [Setting up MX Puppet Skype bridging](docs/configuring-playbook-bridge-mx-puppet-skype.md) documentation page for getting started.


# 2020-04-05

## Private Jitsi support

The [Jitsi support](#jitsi-support) we had landed a few weeks ago was working well, but it was always open to the whole world.

Running such an open instance is not desirable to most people, so [teutat3s](https://github.com/teutat3s) has contributed support for making Jitsi use authentication.

To make your Jitsi server more private, see the [configure internal Jitsi authentication and guests mode](docs/configuring-playbook-jitsi.md#optional-configure-internal-jitsi-authentication-and-guests-mode) section in our Jitsi documentation.


# 2020-04-03

## (Potential Backward Compatibility Break) ma1sd replaces mxisd

Thanks to [Marcel Partap](https://github.com/eMPee584)'s efforts, the [mxisd](https://github.com/kamax-io/mxisd) identity server, which has been deprecated for a long time, has finally been replaced by [ma1sd](https://github.com/ma1uta/ma1sd), a compatible fork.

**If you're using the default playbook configuration**, you don't need to do anything -- your mxisd installation will be replaced with ma1sd and all existing data will be migrated automatically the next time you run the playbook.

**If you're doing something more special** (defining custom `matrix_mxisd_*` variables), the playbook will ask you to rename them to `matrix_ma1sd_*`.
You're also encouraged to test that ma1sd works well for such a more custom setup.


# 2020-03-29

## Archlinux support

Thanks to [Christian Lupus](https://github.com/christianlupus)'s efforts, the playbook now supports installing to an [Archlinux](https://www.archlinux.org/) server.


# 2020-03-24

## Jitsi support

The playbook can now (optionally) install the [Jitsi](https://jitsi.org/) video-conferencing platform and integrate it with [Riot](docs/configuring-playbook-riot-web.md).

See our [Jitsi documentation page](docs/configuring-playbook-jitsi.md) to get started.


# 2020-03-15

## Raspberry Pi support

Thanks to [Gergely Horváth](https://github.com/hooger)'s effort, the playbook supports installing to a Raspberry Pi server, for at least some of the services.

Since most ready-made container images do not support that architecture, we achieve this by building images locally on the device itself.
See our [Self-building documentation page](docs/self-building.md) for how to get started.


# 2020-02-26

## Riot-web themes are here

The playbook now makes it easy to install custom riot-web themes.

To learn more, take a look at our [riot-web documentation on Themes](docs/configuring-playbook-riot-web.md#themes).


# 2020-02-24

## Customize the server name in Riot's login page

You can now customize the server name string that Riot-web displays in its login page.

These playbook variables, with these default values, have been added:

```
matrix_riot_web_default_server_name: "{{ matrix_domain }}"
```

The login page previously said "Sign in to your Matrix account on matrix.example.org" (the homeserver's domain name). It will now say "Sign in ... on example.org" (the server name) by default, or "Sign in ... on Our Server" if you set the variable to "Our Server".

To support this, the config.json template is changed to use the configuration key `default_server_config` for setting the default HS/IS, and the new configuration key `server_name` is added in there.


# 2020-01-30

## Disabling TLSv1.1

To improve security, we've removed TLSv1.1 support from our default matrix-nginx-proxy configuration.

If you need to support old clients, you can re-enable it with the following configuration: `matrix_nginx_proxy_ssl_protocols: "TLSv1.1 TLSv1.2 TLSv1.3"`


# 2020-01-21

## Postgres collation changes (action required!)

By default, we've been using a UTF-8 collation for Postgres. This is known to cause Synapse some troubles (see the [relevant issue](https://github.com/matrix-org/synapse/issues/6722)) on systems that use [glibc](https://www.gnu.org/software/libc/). We run Postgres in an [Alpine Linux](https://alpinelinux.org/) container (which uses [musl](https://www.musl-libc.org/), and not glibc), so our users are likely not affected by the index corruption problem observed by others.

Still, we might become affected in the future. In any case, it's imminent that Synapse will complain about databases which do not use a C collation.

To avoid future problems, we recommend that you run the following command:

```
ansible-playbook -i inventory/hosts setup.yml --tags=upgrade-postgres --extra-vars='{"postgres_force_upgrade": true}'
```

It forces a [Postgres database upgrade](docs/maintenance-postgres.md#upgrading-postgresql), which would recreate your Postgres database using the proper (`C`) collation. If you are low on disk space, or run into trouble, refer to the Postgres database upgrade documentation page.


# 2020-01-14

## Added support for Appservice Webhooks

Thanks to a contribution from [Björn Marten](https://github.com/tripleawwy) from [netresearch](https://www.netresearch.de/), the playbook can now install and configure [matrix-appservice-webhooks](https://github.com/turt2live/matrix-appservice-webhooks) for you. This bridge provides support for Slack-compatible webhooks.

Learn more in [Setting up Appservice Webhooks](docs/configuring-playbook-bridge-appservice-webhooks.md).


# 2020-01-12

## Added support for automatic Double Puppeting for all Mautrix bridges

Double Puppeting can now be easily enabled for all Mautrix bridges supported by the playbook (Facebook, Hangouts, Whatsapp, Telegram).

This is possible due to those bridges' integration with [matrix-synapse-shared-secret-auth](https://github.com/devture/matrix-synapse-shared-secret-auth) - yet another component that this playbook can install for you.

To get started, following the playbook's documentation for the bridge you'd like to configure.


# 2019-12-06

## Added support for an alternative method for using another webserver

We have added support for making `matrix-nginx-proxy` not being so invasive, so that it would be easier to [use your own webserver](docs/configuring-playbook-own-webserver.md).

The documentation has been updated with a **Method 2**, which might make "own webserver" setup easier in some cases (such as [reverse-proxying using Traefik](https://github.com/spantaleev/matrix-docker-ansible-deploy/issues/296)).

**Existing users** are not affected by this and **don't need to change anything**.
The defaults are still the same (`matrix-nginx-proxy` obtaining SSL certificates and doing everything for you automatically).


# 2019-11-10

## Tightened security around room directory publishing

As per this [advisory blog post](https://matrix.org/blog/2019/11/09/avoiding-unwelcome-visitors-on-private-matrix-servers), we've decided to change the default publishing rules for the Matrix room directory.

Our general goal is to favor privacy and security when running personal (family & friends) and corporate homeservers.
Both of these likely benefit from having a more secure default of **not showing the room directory without authentication** and **not publishing the room directory over federation**.

As with anything else, these new defaults can be overriden by changing the `matrix_synapse_allow_public_rooms_without_auth` and `matrix_synapse_allow_public_rooms_over_federation` variables, respectively.


# 2019-10-05

## Improved Postgres upgrading/importing

Postgres [upgrading](docs/maintenance-postgres.md#upgrading-postgresql) and [importing](docs/importing-postgres.md) have been improved to add support for multiple databases and roles.

Previously, the playbook would only take care of the `homeserver` database and `synapse` user.
We now back up and restore all databases and users on the Postgres server.

For now, the playbook only uses that one database (`homeserver`) and that one single user (`synapse`), so it's all the same.
However, in the future, additional components besides Synapse may also make use the Postgres database server.
One such example is the [matrix-appservice-slack](https://github.com/matrix-org/matrix-appservice-slack) bridge, which strongly encourages use of Postgres in its v1.0 release. We are yet to upgrade to it.

Additionally, Postgres [upgrading](docs/maintenance-postgres.md#upgrading-postgresql) now uses gzipped dump files by default, to minimize disk space usage.


# 2019-10-04

## Postgres 12 support

The playbook now installs [Postgres 12](https://www.postgresql.org/about/news/1976/) by default.

If you have have an existing setup, it's likely running on an older Postgres version (9.x, 10.x or 11.x). You can easily upgrade by following the [upgrading PostgreSQL guide](docs/maintenance-postgres.md#upgrading-postgresql).


# 2019-10-03

## Synapse 1.4.0

Synapse 1.4.0 [is out](https://matrix.org/blog/2019/10/03/synapse-1-4-0-released) with lots of changes related to privacy.

Its new defaults (which we adopt as well) mean that certain old data will automatically get purged after a certain number of days. 1.4.0 automatically garbage collects redacted messages (defaults to 7 days) and removes unused IP and user agent information stored in the user_ips table (defaults to 30 days). If you'd like to preserve this data, we encourage you to look at the `redaction_retention_period` and `user_ips_max_age` options (controllable by the `matrix_synapse_redaction_retention_period` and `matrix_synapse_user_ips_max_age` playbook variables, respectively) before doing the upgrade. If you'd like to keep data indefinitely, set these variables to `null` (e.g. `matrix_synapse_redaction_retention_period: ~`).

From now on the `trusted_key_servers` setting for Synapse is configurable. It still defaults to `matrix.org` just like it always has, but in a more explicit way now. If you'd like to use another trusted key server, adjust the `matrix_synapse_trusted_key_servers` playbook variable.

Synapse 1.4.0 also changes lots of things related to identity server integration.
Because Synapse will now by default be responsible for validating email addresses for user accounts, running without an identity server looks more feasible.
We still [have concerns](https://github.com/spantaleev/matrix-docker-ansible-deploy/pull/275/files#r331104117) over disabling the identity server by default, so for now it remains enabled.


# 2019-09-09

## Synapse Simple Antispam support

There have been lots of invite-spam attacks lately and [Travis](https://github.com/t2bot) has created a Synapse module ([synapse-simple-antispam](https://github.com/t2bot/synapse-simple-antispam)) to let people protect themselves.

From now on, you can easily install and configure this spam checker module through the playbook.

Learn more in [Setting up Synapse Simple Antispam](docs/configuring-playbook-synapse-simple-antispam.md).


# 2019-08-25

## Extensible Riot-web configuration

Similarly to [Extensible Synapse configuration](#extensible-synapse-configuration) (below), Riot-web configuration is also extensible now.

From now on, you can extend/override Riot-web's configuration by making use of the `matrix_riot_web_configuration_extension_json` variable.
This should be enough for most customization needs.

If you need even more power, you can now also take full control and override `matrix_riot_web_configuration_default` (or `matrix_riot_web_configuration`) directly.

Learn more in [Configuring Riot-web](docs/configuring-playbook-riot-web.md).


# 2019-08-22

## Extensible Synapse configuration

Previously, we had to create custom Ansible variables for each and every Synapse setting.
This lead to too much effort (and configuration ugliness) to all of Synapse's settings, so naturally, not all features of Synapse could be controlled through the playbook.

From now on, you can extend/override the Synapse server's configuration by making use of the `matrix_synapse_configuration_extension_yaml` variable.
This should be enough for most customization needs.

If you need even more power, you can now also take full control and override `matrix_synapse_configuration` (or `matrix_synapse_configuration_yaml`) directly.

Learn more here in [Configuring Synapse](docs/configuring-playbook-synapse.md).


# 2019-08-21

## Slack bridging support

Thanks to the [great work](https://github.com/spantaleev/matrix-docker-ansible-deploy/pull/205) of [kingoftheconnors](https://github.com/kingoftheconnors) and [Stuart Mumford (Cadair)](https://github.com/Cadair), the playbook now supports bridging to [Slack](https://slack.com) via the [appservice-slack](https://github.com/matrix-org/matrix-appservice-slack) bridge.

Additional details are available in [Setting up Appservice Slack bridging](docs/configuring-playbook-bridge-appservice-slack.md).

## Google Hangouts bridging support

Thanks to the [great work](https://github.com/spantaleev/matrix-docker-ansible-deploy/pull/251) of [Eduardo Beltrame (Munfred)](https://github.com/Munfred) and [Robbie D (microchipster)](https://github.com/microchipster), the playbook now supports bridging to [Google Hangouts](https://hangouts.google.com/) via the [mautrix-hangouts](https://mau.dev/tulir/mautrix-hangouts) bridge.

Additional details are available in [Setting up Mautrix Hangouts bridging](docs/configuring-playbook-bridge-mautrix-hangouts.md).


# 2019-08-05

## Email2Matrix support

Support for [Email2Matrix](https://github.com/devture/email2matrix) has been added.

It's an optional feature that you can enable via the playbook.

To learn more, see the [playbook's documentation on Email2Matrix](./docs/configuring-playbook-email2matrix.md).


# 2019-08-03

## Synapse logging level has been reduced to WARNING

After [some discussion in our support room](https://matrix.to/#/!PukFFdIcHgtaaHZflT:devture.com/$156476852524179TBeKy:matrix.org?via=devture.com&via=matrix.org&via=librem.one), we've decided to change the default logging level for Synapse from `INFO` to `WARNING`.

This greatly reduces the number of log messages that are being logged, leading to:

- much less disk space dedicated to Synapse and thus, logs kept for longer
- easier to find some important `WARNING`, `ERROR` and `CRITICAL` messages, as they're not longer buried in thousands of non-important `INFO` messages

If you'd like to track down an issue, you [can always increase the logging level as described here](./docs/maintenance-and-troubleshooting.md#increasing-synapse-logging).



# 2019-07-08

## Synapse Maintenance docs and synapse-janitor support are available

The playbook can now help you with Synapse's maintenance.

There's a new documentation page about [Synapse maintenance](./docs/maintenance-synapse.md) and another section on [Postgres vacuuming](./docs/maintenance-postgres.md#vacuuming-postgresql).

Among other things, if your Postgres database has grown significantly over time, you may wish to [ask the playbook to purge unused data with synapse-janitor](./docs/maintenance-synapse.md#purging-unused-data-with-synapse-janitor) for you.


## (BC Break) Rename run control variables

Some internal playbook control variables have been renamed.

This change **only affects people who run this playbook's roles from another playbook**.
If you're using this playbook as-is, you're not affected and don't need to do anything.

The following variables have been renamed:

- from `run_import_postgres` to `run_postgres_import`
- from `run_import_sqlite_db` to `run_postgres_import_sqlite_db`
- from `run_upgrade_postgres` to `run_postgres_upgrade`
- from `run_import_media_store` to `run_synapse_import_media_store`
- from `run_register_user` to `run_synapse_register_user`
- from `run_update_user_password` to `run_synapse_update_user_password`


# 2019-07-04

## Synapse no longer logs to text files

Following what the official Synapse Docker image is doing ([#5565](https://github.com/matrix-org/synapse/pull/5565)) and what we've been doing for mostly everything installed by this playbook, **Synapse no longer logs to text files** (`/matrix/synapse/run/homeserver.log*`).

From now on, Synapse would only log to console, which goes to systemd's journald.
To see Synapse's logs, execute: `journalctl -fu matrix-synapse`

Because of this, the following variables have become obsolete and were removed:

- `matrix_synapse_max_log_file_size_mb`
- `matrix_synapse_max_log_files_count`

To prevent confusion, it'd be better if you delete all old files manually after you've upgraded (`rm -f /matrix/synapse/run/homeserver.log*`).

Because Synapse is incredibly chatty when it comes to logging (here's [one such issue](https://github.com/matrix-org/synapse/issues/4751) describing the problem), if you're running an ancient distribution (like CentOS 7.0), be advised that systemd's journald default logging restrictions may not be high enough to capture all log messages generated by Synapse. This is especially true if you've got a busy (Synapse) server. We advise that you manually add `RateLimitInterval=0` and `RateLimitBurst=0` under `[Storage]` in the `/etc/systemd/journald.conf` file, followed by restarting the logging service (`systemctl restart systemd-journald`).


# 2019-06-27

## (BC Break) Discord bridge configuration is now entirely managed by the playbook

Until now, the `config.yaml` file for the [Discord bridge](docs/configuring-playbook-bridge-appservice-discord.md) was managed by the playbook, but the `registration.yaml` file was not.

From now on, the playbook will keep both configuration files sync for you.

This means that if you were making manual changes to the `/matrix/appservice-discord/discord-registration.yaml` configuration file, those would be lost the next time you run the playbook.

The bridge now stores configuration in a subdirectory (`/matrix/appservice-discord/config`).

Likewise, data is now also stored in a subdirectory (`/matrix/appservice-discord/data`). When you run the playbook with an existing database file (`/matrix/appservice-discord/discord.db`), the playbook will stop the bridge and relocate the database file to the `./data` directory. There's no data-loss involved. You'll need to restart the bridge manually though (`--tags=start`).

The main directory (`/matrix/appservice-discord`) may contain some leftover files (`user-store.db`, `room-store.db`, `config.yaml`, `discord-registration.yaml`, `invite_link`). These are no longer necessary and can be deleted manually.

We're now following the default sample configuration for the Discord bridge.
If you need to override some values, define them in `matrix_appservice_discord_configuration_extension_yaml`.


# 2019-06-24

## (BC Break) WhatsApp bridge configuration is now entirely managed by the playbook

Until now, configuration files for the [WhatsApp bridge](docs/configuring-playbook-bridge-mautrix-whatsapp.md) were created by the playbook initially, but never modified later on.

From now on, the playbook will keep the configuration in sync for you.

This means that if you were making manual changes to the `/matrix/mautrix-whatsapp/config.yaml` or `/matrix/mautrix-whatsapp/registration.yaml` configuration files, those would be lost the next time you run the playbook.

The bridge now stores configuration in a subdirectory (`/matrix/mautrix-whatsapp/config`), so your old configuration remains in the base directory (`/matrix/mautrix-whatsapp`).
You need to migrate any manual changes over to the new `matrix_mautrix_whatsapp_configuration_extension_yaml` variable, so that the playbook would apply them for you.

Likewise, data is now also stored in a subdirectory (`/matrix/mautrix-whatsapp/data`). When you run the playbook with an existing database file (`/matrix/mautrix-whatsapp/mautrix-whatsapp.db`), the playbook will stop the bridge and relocate the database file to the `./data` directory. There's no data-loss involved. You'll need to restart the bridge manually though (`--tags=start`).

We're now following the default configuration for the WhatsApp bridge.


# 2019-06-20

## (BC Break) IRC bridge configuration is now entirely managed by the playbook

Until now, configuration files for the [IRC bridge](docs/configuring-playbook-bridge-appservice-irc.md) were created by the playbook initially, but never modified later on.

From now on, the playbook will keep the configuration in sync for you.

This means that if you were making manual changes to the `/matrix/appservice-irc/config.yaml` or `/matrix/appservice-irc/registration.yaml` configuration files, those would be lost the next time you run the playbook.

The bridge now stores configuration in a subdirectory (`/matrix/appservice-irc/config`), so your old configuration remains in the base directory (`/matrix/appservice-irc`).

Previously, we asked people to configure bridged IRC servers by extending the bridge configuration (`matrix_appservice_irc_configuration_extension_yaml`). While this is still possible and will continue working forever, **we now recommend defining IRC servers in the easier to use `matrix_appservice_irc_ircService_servers` variable**. See [our IRC bridge documentation page](docs/configuring-playbook-bridge-appservice-irc.md) for an example.

If you decide to continue using `matrix_appservice_irc_configuration_extension_yaml`, you might be interested to know that `ircService.databaseUri` and a few other keys now have default values in the base configuration (`matrix_appservice_irc_configuration_yaml`). You may wish to stop redefining those keys, unless you really intend to override them. You most likely only need to override `ircService.servers`.

Bridge data (`passkey.pem` and database files) is now also stored in a subdirectory (`/matrix/appservice-irc/data`).
When you run the playbook with an existing `/matrix/appservice-irc/passkey.pem` file, the playbook will stop the bridge and relocate the passkey and database files (`rooms.db` and `users.db`) to the `./data` directory. There's no data-loss involved. You'll need to restart the bridge manually though (`--tags=start`).


# 2019-06-15

## (BC Break) Telegram bridge configuration is now entirely managed by the playbook

Until now, configuration files for the [Telegram bridge](docs/configuring-playbook-bridge-mautrix-telegram.md) were created by the playbook initially, but never modified later on.

From now on, the playbook will keep the configuration in sync for you.

This means that if you were making manual changes to the `/matrix/mautrix-telegram/config.yaml` or `/matrix/mautrix-telegram/registration.yaml` configuration files, those would be lost the next time you run the playbook.

The bridge now stores configuration in a subdirectory (`/matrix/mautrix-telegram/config`), so your old configuration remains in the base directory (`/matrix/mautrix-telegram`).
You need to migrate any manual changes over to the new `matrix_mautrix_telegram_configuration_extension_yaml` variable, so that the playbook would apply them for you.

Likewise, data is now also stored in a subdirectory (`/matrix/mautrix-telegram/data`). When you run the playbook with an existing database file (`/matrix/mautrix-telegram/mautrix-telegram.db`), the playbook will stop the bridge and relocate the database file to the `./data` directory. There's no data-loss involved. You'll need to restart the bridge manually though (`--tags=start`).

Also, we're now following the default configuration for the Telegram bridge, so some default configuration values are different:

- `edits_as_replies` (used to be `false`, now `true`) - previously replies were not sent over to Matrix at all; ow they are sent over as a reply to the original message
- `inline_images` (used to be `true`, now `false`) - this has to do with captioned images. Inline-image (included caption) are said to exhibit troubles on Riot iOS. When `false`, the caption arrives on the Matrix side as a separate message.
- `authless_portals` (used to be `false`, now `true`) - creating portals from the Telegram side is now possible
- `whitelist_group_admins` (used to be `false`, now `true`) - allows Telegram group admins to use the bot commands

If the new values are not to your liking, use `matrix_mautrix_telegram_configuration_extension_yaml` to specify an override (refer to `matrix_mautrix_telegram_configuration_yaml` to figure out which variable goes where).


# 2019-06-12

## Synapse v1.0

With [Synapse v1.0 now available](https://matrix.org/blog/2019/06/11/introducing-matrix-1-0-and-the-matrix-org-foundation) and most people being on at least Synapse v0.99, it's time to remove the `_matrix._tcp` DNS SRV record that we've been keeping for compatibility with old Synapse versions (<= 0.34).

According to the [Server Discovery specification](https://matrix.org/docs/spec/server_server/r0.1.2.html#server-discovery), it's no harm to keep the DNS SRV record. But since it's not necessary for federating with the larger Matrix network anymore, you should be safe to get rid of it.

**Note**: don't confuse the `_matrix._tcp` and `_matrix-identity._tcp` DNS SRV records. The latter, **must not** be removed.

For completeness, we must say that using a `_matrix._tcp` [SRV record for Server Delegation](docs/howto-server-delegation.md#server-delegation-via-a-dns-srv-record-advanced) is still valid and useful for certain deployments. It's just that our guide recommends the [`/.well-known/matrix/server` Server Delegation method](docs/howto-server-delegation.md#server-delegation-via-a-well-known-file), due to its easier implementation when using this playbook.

Besides this optional/non-urgent DNS change, assuming you're already on Synapse v0.99, upgrading to Synapse v1.0 should be as simple as [re-running the playbook](docs/maintenance-upgrading-services.md).


# 2019-06-07

## (BC Break) Facebook bridge configuration is now entirely managed by the playbook

Until now, configuration files for the [Facebook bridge](docs/configuring-playbook-bridge-mautrix-facebook.md) were created by the playbook initially, but never modified later on.

From now on, the playbook will keep the configuration in sync for you.

This means that if you were making manual changes to the `/matrix/mautrix-facebook/config.yaml` or `/matrix/mautrix-facebook/registration.yaml` configuration files, those would be lost the next time you run the playbook.

The bridge now stores configuration in a subdirectory (`/matrix/mautrix-facebook/config`), so your old configuration remains in the base directory (`/matrix/mautrix-facebook`).
You need to migrate any manual changes over to the new `matrix_mautrix_facebook_configuration_extension_yaml` variable, so that the playbook would apply them for you.

Likewise, data is now also stored in a subdirectory (`/matrix/mautrix-facebook/data`). When you run the playbook with an existing database file (`/matrix/mautrix-facebook/mautrix-facebook.db`), the playbook will stop the bridge and relocate the database file to the `./data` directory. There's no data-loss involved. You'll need to restart the bridge manually though (`--tags=start`).


# 2019-05-25

## Support for exposing container ports publicly (not just to the host)

Until now, various roles supported a `matrix_*_expose_port` variable, which would expose their container's port to the host. This was mostly useful for reverse-proxying manually (in case `matrix-nginx-proxy` was disabled). It could also be used for installing some playbook services (e.g. bridges, etc.) and wiring them to a separate (manual) Matrix setup.

`matrix_*_expose_port` variables were not granular enough - sometimes they would expose one port, other times multiple. They also didn't provide control over **where** to expose (to which port number and to which network interface), because they would usually hardcode something like `127.0.0.1:8080`.

All such variables have been superseded by a better (more flexible) way to do it.

**Most** people (including those not using `matrix-nginx-proxy`), **don't need** to bother with this.

Porting examples follow for people having more customized setups:

- **from** `matrix_synapse_container_expose_client_api_port: true` **to** `matrix_synapse_container_client_api_host_bind_port: '127.0.0.1:8008'`

- **from** `matrix_synapse_container_expose_federation_api_port: true` **to** `matrix_synapse_container_federation_api_plain_host_bind_port: '127.0.0.1:8048'` and possibly `matrix_synapse_container_federation_api_tls_host_bind_port: '8448'`

- **from** `matrix_synapse_container_expose_metrics_port: true` **to** `matrix_synapse_container_metrics_api_host_bind_port: '127.0.0.1:9100'`

- **from** `matrix_riot_web_container_expose_port: true` **to** `matrix_riot_web_container_http_host_bind_port: '127.0.0.1:8765'`

- **from** `matrix_mxisd_container_expose_port: true` **to** `matrix_mxisd_container_http_host_bind_port: '127.0.0.1:8090'`

- **from** `matrix_dimension_container_expose_port: true` **to** `matrix_dimension_container_http_host_bind_port: '127.0.0.1:8184'`

- **from** `matrix_corporal_container_expose_ports: true` **to** `matrix_corporal_container_http_gateway_host_bind_port: '127.0.0.1:41080'` and possibly `matrix_corporal_container_http_api_host_bind_port: '127.0.0.1:41081'`

- **from** `matrix_appservice_irc_container_expose_client_server_api_port: true` **to** `matrix_appservice_irc_container_http_host_bind_port: '127.0.0.1:9999'`

- **from** `matrix_appservice_discord_container_expose_client_server_api_port: true` **to** `matrix_appservice_discord_container_http_host_bind_port: '127.0.0.1:9005'`

As always, if you forget to remove usage of some outdated variable, the playbook will warn you.


# 2019-05-23

## (BC Break) Ansible 2.8 compatibility

Thanks to [@danbob](https://github.com/danbob), the playbook now [supports the new Ansible 2.8](https://github.com/spantaleev/matrix-docker-ansible-deploy/pull/187).

A manual change is required to the `inventory/hosts` file, changing the group name from `matrix-servers` to `matrix_servers` (dash to underscore).

To avoid doing it manually, run this:
- Linux: `sed -i 's/matrix-servers/matrix_servers/g' inventory/hosts`
- Mac: `sed -i '' 's/matrix-servers/matrix_servers/g' inventory/hosts`


# 2019-05-21

## Synapse no longer required

The playbook no longer insists on installing [Synapse](https://github.com/matrix-org/synapse) via the `matrix-synapse` role.

If you would prefer to install Synapse another way and just use the playbook to install other services, it should be possible (`matrix_synapse_enabled: false`).

Note that it won't necessarily be the best experience, since the playbook wires things to Synapse by default.
If you're using your own Synapse instance (especially one not running in a container), you may have to override many variables to point them to the correct place.

Having Synapse not be a required component potentially opens the door for installing alternative Matrix homeservers.


## Bridges are now separate from the Synapse role

Bridges are no longer part of the `matrix-synapse` role.
Each bridge now lives in its own separate role (`roles/matrix-bridge-*`).

These bridge roles are independent of the `matrix-synapse` role, so it should be possible to use them with a Synapse instance installed another way (not through the playbook).


## Renaming inconsistently-named Synapse variables

For better consistency, the following variables have been renamed:

- `matrix_enable_room_list_search` was renamed to `matrix_synapse_enable_room_list_search`
- `matrix_alias_creation_rules` was renamed to `matrix_synapse_alias_creation_rules`
- `matrix_nginx_proxy_matrix_room_list_publication_rulesdata_path` was renamed to `matrix_synapse_room_list_publication_rules`


# 2019-05-09

Besides a myriad of bug fixes and minor improvements, here are the more notable (bigger) features we can announce today.

## Mautrix Facebook/Messenger bridging support

The playbook now supports bridging with [Facebook](https://www.facebook.com/) by installing the [mautrix-facebook](https://github.com/tulir/mautrix-facebook) bridge. This playbook functionality is available thanks to [@izissise](https://github.com/izissise).

Additional details are available in [Setting up Mautrix Facebook bridging](docs/configuring-playbook-bridge-mautrix-facebook.md).

## mxisd Registration feature integration

The playbook can now help you integrate with mxisd's [Registration](https://github.com/kamax-matrix/mxisd/blob/master/docs/features/registration.md) feature.

Learn more in [mxisd-controlled Registration](docs/configuring-playbook-mxisd.md#mxisd-controlled-registration).


# 2019-04-16

## Caddy webserver examples

If you prefer using the [Caddy](https://caddyserver.com/) webserver instead of our own integrated nginx, we now have examples for it in the [`examples/caddy`](examples/caddy) directory

# 2019-04-10

## Goofys support for other S3-compatible object stores

Until now, you could optionally host Synapse's media repository on Amazon S3, but we now also support [using other S3-compatible object stores](docs/configuring-playbook-s3.md),


# 2019-04-03

## Ansible >= 2.5 is required

Due to recent playbook improvements and the fact that the world keeps turning, we're bumping the [version requirement for Ansible](docs/ansible.md#supported-ansible-versions) (2.4 -> 2.5).

We've also started building our own Docker image of Ansible ([devture/ansible](https://hub.docker.com/r/devture/ansible/)), which is useful for people who can't upgrade their local Ansible installation (see [Using Ansible via Docker](docs/ansible.md#using-ansible-via-docker)).


# 2019-03-19

## TLS support for Coturn

We've added TLS support to the Coturn TURN server installed by the playbook by default.
The certificates from the Matrix domain will be used for the Coturn server.

This feature is enabled by default for new installations.
To make use of TLS support for your existing Matrix server's Coturn, make sure to rebuild both Coturn and Synapse:

```bash
ansible-playbook -i inventory/hosts setup.yml --tags=setup-coturn,setup-synapse,start
```

People who have an extra firewall (besides the iptables firewall, which Docker manages automatically), will need to open these additional firewall ports: `5349/tcp` (TURN over TCP) and `5349/udp` (TURN over UDP).

People who build their own custom playbook from our roles should be aware that:

- the `matrix-coturn` role and actually starting Coturn (e.g. `--tags=start`), requires that certificates are already put in place. For this reason, it's usually a good idea to have the `matrix-coturn` role execute after `matrix-nginx-proxy` (which retrieves the certificates).

- there are a few variables that can help you enable TLS support for Coturn. See the `matrix-coturn` section in [group_vars/matrix-servers](./group_vars/matrix-servers).


# 2019-03-12

## matrix-nginx-proxy support for serving the base domain

If you don't have a dedicated server for your base domain and want to set up [Server Delegation via a well-known file](docs/howto-server-delegation.md#server-delegation-via-a-well-known-file), the playbook has got you covered now.

It's now possible for the playbook to obtain an SSL certificate and serve the necessary files for Matrix Server Delegation on your base domain.
Take a look at the new [Serving the base domain](docs/configuring-playbook-base-domain-serving.md) documentation page.


## (BC break) matrix-nginx-proxy data variable renamed

`matrix_nginx_proxy_data_path` was renamed to `matrix_nginx_proxy_base_path`.

There's a new `matrix_nginx_proxy_data_path` variable, which has a different use-purpose now (it's a subdirectory of `matrix_nginx_proxy_base_path` and is meant for storing various data files).


# 2019-03-10

## Dimension Integration Manager support

Thanks to [NullIsNot0](https://github.com/NullIsNot0), the playbook can now (optionally) install the [Dimension](https://dimension.t2bot.io/) Integration Manager.
To learn more, see the [Setting up Dimension](docs/configuring-playbook-dimension.md) documentation page.


# 2019-03-07

## Ability to customize mxisd's email templates

Thanks to [Sylvia van Os](https://github.com/TheLastProject), mxisd's email templates can now be customized easily.
To learn more, see the [Customizing email templates](docs/configuring-playbook-mxisd.md#customizing-email-templates) documentation page.


# 2019-03-05

## Discord bridging support

[@Lionstiger](https://github.com/Lionstiger) has done some great work adding Discord bridging support via [matrix-appservice-discord](https://github.com/Half-Shot/matrix-appservice-discord).
To learn more, see the [Setting up Appservice Discord bridging](docs/configuring-playbook-bridge-appservice-discord.md) documentation page.


# 2019-02-19

## Renaming variables

The following playbook variables were renamed:

- from `host_specific_hostname_identity` to `matrix_domain`
- from `hostname_identity` to `matrix_domain`
- from `hostname_matrix` to `matrix_server_fqn_matrix`
- from `hostname_riot` to `matrix_server_fqn_riot`
- from `host_specific_matrix_ssl_lets_encrypt_support_email` to `matrix_ssl_lets_encrypt_support_email`

Doing that, we've simplified things, made names less confusing (hopefully) and moved all variable names under the `matrix_` prefix.


# 2019-02-16

## Riot v1.0.1 support

You can now use the brand new and redesigned Riot.

The new version no longer has a homepage by default, so we've also removed the custom homepage that we've been installing.

However, we still provide you with hooks to install your own `home.html` file by specifying the `matrix_riot_web_embedded_pages_home_path` variable (used to be called `matrix_riot_web_homepage_template` before).


# 2019-02-14

## Synapse v0.99.1

As we're moving toward Synapse v1.0, things are beginning to stabilize.
Upgrading from v0.99.0 to v0.99.1 should be painless.

If you've been overriding the default configuration so that you can terminate TLS at the Synapse side (`matrix_synapse_no_tls: false`), you'll now have to replace this custom configuration with `matrix_synapse_tls_federation_listener_enabled: true`. The `matrix_synapse_no_tls` variable is no more.


# 2019-02-06

## Synapse v0.99 support and preparation for Synapse v1.0

Matrix is undergoing a lot of changes as it matures towards Synapse v1.0.
The first step is the Synapse v0.99 transitional release, which this playbook now supports.

If you've been using this playbook successfully until now, you'd be aware that we've been doing [Server Delegation](docs/howto-server-delegation.md) using a `_matrix._tcp` DNS SRV record (as per [Configuring DNS](docs/configuring-dns.md)).

Due to changes related to certificate file requirements that will affect us at Synapse v1.0, we'll have to stop using a **`_matrix._tcp` DNS SRV record in the future** (when Synapse goes to v1.0 - around 5th of March 2019). We **still need to keep the SRV record for now**, for backward compatibility with older Synapse versions (lower than v0.99).

**What you need to do now** is make use of this transitional Synapse v0.99 release to **prepare your federation settings for the future**. You have 2 choices to prepare yourself for compatibility with the future Synapse v1.0:

- (recommended) set up [Server Delegation via a well-known file](docs/howto-server-delegation.md#server-delegation-via-a-well-known-file), unless you are affected by the [Downsides of well-known-based Server Delegation](docs/howto-server-delegation.md#downsides-of-well-known-based-server-delegation). If you had previously set up the well-known `client` file, depending on how you've done it, it may be that there is nothing new required of you (besides [upgrading](docs/maintenance-upgrading-services.md)). After upgrading, you can [run a self-check](docs/maintenance-checking-services.md), which will tell you if you need to do anything extra with regard to setting up [Server Delegation via a well-known file](docs/howto-server-delegation.md#server-delegation-via-a-well-known-file). After some time, when most people have upgraded to Synapse v0.99 and older releases have disappeared, be prepared to drop your `_matrix._tcp` SRV record.

- (more advanced) if the [Downsides of well-known-based Server Delegation](docs/howto-server-delegation.md#downsides-of-well-known-based-server-delegation) are not to your liking, **as an alternative**, you can set up [Server Delegation via a DNS SRV record](docs/howto-server-delegation.md#server-delegation-via-a-dns-srv-record-advanced). In such a case, you get to keep using your existing `_matrix._tcp` DNS SRV record forever and need to NOT set up a `/.well-known/matrix/server` file. Don't forget that you need to do certificate changes though. Follow the guide at [Server Delegation via a DNS SRV record](docs/howto-server-delegation.md#server-delegation-via-a-dns-srv-record-advanced).


# 2019-02-01

## TLS v1.3 support

Now that the [nginx Docker image](https://hub.docker.com/_/nginx) has [added support for TLS v1.3](https://github.com/nginxinc/docker-nginx/issues/190), we have enabled that protocol by default.

When using:

- the **integrated nginx server**: TLS v1.3 support might not kick in immediately, because the nginx version hasn't been bumped and you may have an older build of the nginx Docker image (currently `nginx:1.15.8-alpine`). Typically, we do not re-pull images that you already have. When the nginx version gets bumped in the future, everyone will get the update. Until then, you could manually force-pull the rebuilt Docker image by running this on the server: `docker pull nginx:1.15.8-alpine`.

- **your own external nginx server**: if your external nginx server is too old, the new configuration we generate for you in `/matrix/nginx-proxy/conf.d/` might not work anymore, because it mentions `TLSv1.3` and your nginx version might not support that. You can adjust the SSL protocol list by overriding the `matrix_nginx_proxy_ssl_protocols` variable. Learn more in the documentation page for [Using your own webserver, instead of this playbook's nginx proxy](docs/configuring-playbook-own-webserver.md)

- **another web server**: you don't need to do anything to accommodate this change


# 2019-01-31

## IRC bridging support

[Devon Maloney (@Plailect)](https://github.com/Plailect) has done some great work bringing IRC bridging support via [matrix-appservice-irc](https://github.com/TeDomum/matrix-appservice-irc).
To learn more, see the [Setting up Appservice IRC](docs/configuring-playbook-bridge-appservice-irc.md) documentation page.


# 2019-01-29

## Running container processes as non-root, without capabilities and read-only

To improve security, this playbook no longer starts container processes as the `root` user.
Most containers were dropping privileges anyway, but we were trusting them with `root` privileges until they would do that.
Not anymore -- container processes now start as a non-root user (usually `matrix`) from the get-go.

For additional security, various capabilities are also dropped (see [why it's important](https://github.com/projectatomic/atomic-site/issues/203)) for all containers.

Additionally, most containers now use a read-only filesystem (see [why it's important](https://www.projectatomic.io/blog/2015/12/making-docker-images-write-only-in-production/)).
Containers are given write access only to the directories they need to write to.

A minor breaking change is the `matrix_nginx_proxy_proxy_matrix_client_api_client_max_body_size` variable having being renamed to `matrix_nginx_proxy_proxy_matrix_client_api_client_max_body_size_mb` (note the `_mb` suffix). The new variable expects a number value (e.g. `25M` -> `25`).
If you weren't customizing this variable, this wouldn't affect you.


## matrix-mailer is now based on Exim, not Postfix

While we would have preferred to stay with [Postfix](http://www.postfix.org/), we found out that it cannot run as a non-root user.
We've had to replace it with [Exim](https://www.exim.org/) (via the [devture/exim-relay](https://hub.docker.com/r/devture/exim-relay) container image).

The internal `matrix-mailer` service (running in a container) now listens on port `8025` (used to be `587` before).
The playbook will update your Synapse and mxisd email settings to match (`matrix-mailer:587` -> `matrix-mailer:8025`).

Using the [devture/exim-relay](https://hub.docker.com/r/devture/exim-relay) container image instead of [panubo/postfix](https://hub.docker.com/r/panubo/postfix/) also gives us a nice disk usage reduction (~200MB -> 8MB).


# 2019-01-17

## (BC Break) Making the playbook's roles more independent of one another

The following change **affects people running a more non-standard setup** - external Postgres or using our roles in their own other playbook.
**Most users don't need to do anything**, besides becoming aware of the new glue variables file [`group_vars/matrix-servers`](group_vars/matrix-servers).

Because people like using the playbook's components independently (outside of this playbook) and because it's much better for maintainability, we've continued working on separating them.
Still, we'd like to offer a turnkey solution for running a fully-featured Matrix server, so this playbook remains important for wiring up the various components.

With the new changes, **all roles are now only dependent on the minimal `matrix-base` role**. They are no longer dependent among themselves.

In addition, the following components can now be completely disabled (for those who want/need to):
- `matrix-coturn` by using `matrix_coturn_enabled: false`
- `matrix-mailer` by using `matrix_mailer_enabled: false`
- `matrix-postgres` by using `matrix_postgres_enabled: false`

The following changes had to be done:

- glue variables had to be introduced to the playbook, so it can wire together the various components. Those glue vars are stored in the [`group_vars/matrix-servers`](group_vars/matrix-servers) file. When overriding variables for a given component (role), you need to be aware of both the role defaults (`role/ROLE/defaults/main.yml`) and the role's corresponding section in the [`group_vars/matrix-servers`](group_vars/matrix-servers) file.

- `matrix_postgres_use_external` has been superceeded by the more consistently named `matrix_postgres_enabled` variable and a few other `matrix_synapse_database_` variables. See the [Using an external PostgreSQL server (optional)](docs/configuring-playbook-external-postgres.md) documentation page for an up-to-date replacement.

- Postgres tools (`matrix-postgres-cli` and `matrix-make-user-admin`) are no longer installed if you're not enabling the `matrix-postgres` role (`matrix_postgres_enabled: false`)

- roles, being more independent now, are more minimal and do not do so much magic for you. People that are building their own playbook using our roles will definitely need to take a look at the [`group_vars/matrix-servers`](group_vars/matrix-servers) file and adapt their playbooks with the same (or similar) wiring logic.


# 2019-01-16

## Splitting the playbook into multiple roles

For better maintainability, the playbook logic (which all used to reside in a single `matrix-server` role)
has been split out into a number of different roles: `matrix-synapse`, `matrix-postgres`, `matrix-riot-web`, `matrix-mxisd`, etc. (see the `roles/` directory).

To keep the filesystem more consistent with this separation, the **Postgres data had to be relocated**.

The default value of `matrix_postgres_data_path` was changed from `/matrix/postgres` to `/matrix/postgres/data`. The `/matrix/postgres` directory is what we consider a base path now (new variable `matrix_postgres_base_path`). **Your Postgres data files will automatically be relocated by the playbook** (`/matrix/postgres/*` -> `/matrix/postgres/data/`) when you run with `--tags=setup-all` (or `--tags=setup-postgres`). While this shouldn't cause data-loss, **it's better if you do a Postgres backup just in case**. You'd need to restart all services after this migration (`--tags=start`).


# 2019-01-11

## (BC Break) mxisd configuration changes

To be more flexible and to support the upcoming [mxisd](https://github.com/kamax-io/mxisd) 1.3.0 (when it gets released),
we've had to redo how mxisd gets configured.

The following variables are no longer supported by this playbook:

- `matrix_mxisd_ldap_enabled`
- `matrix_mxisd_ldap_connection_host`
- `matrix_mxisd_ldap_connection_tls`
- `matrix_mxisd_ldap_connection_port`
- `matrix_mxisd_ldap_connection_baseDn`
- `matrix_mxisd_ldap_connection_baseDns`
- `matrix_mxisd_ldap_connection_bindDn`
- `matrix_mxisd_ldap_connection_bindDn`
- `matrix_mxisd_ldap_connection_bindPassword`
- `matrix_mxisd_ldap_filter`
- `matrix_mxisd_ldap_attribute_uid_type`
- `matrix_mxisd_ldap_attribute_uid_value`
- `matrix_mxisd_ldap_connection_bindPassword`
- `matrix_mxisd_ldap_attribute_name`
- `matrix_mxisd_ldap_attribute_threepid_email`
- `matrix_mxisd_ldap_attribute_threepid_msisdn`
- `matrix_mxisd_ldap_identity_filter`
- `matrix_mxisd_ldap_identity_medium`
- `matrix_mxisd_ldap_auth_filter`
- `matrix_mxisd_ldap_directory_filter`
- `matrix_mxisd_template_config`

You are encouraged to use the `matrix_mxisd_configuration_extension_yaml` variable to define your own mxisd configuration additions and overrides.
Refer to the [default variables file](roles/matrix-mxisd/defaults/main.yml) for more information.

This new way of configuring mxisd is beneficial because:

- it lets us support all mxisd configuration options, as the playbook simply forwards them to mxisd without needing to care or understand them
- it lets you upgrade to newer mxisd versions and make use of their features, without us having to add support for them explicitly


# 2019-01-08

## (BC Break) Cronjob schedule no longer configurable

Due to the way we manage cronjobs now, you can no longer configure the schedule they're invoked at.

If you were previously using `matrix_ssl_lets_encrypt_renew_cron_time_definition` or `matrix_nginx_proxy_reload_cron_time_definition`
to set a custom schedule, you should note that these variables don't affect anything anymore.

If you miss this functionality, please [open an Issue](https://github.com/spantaleev/matrix-docker-ansible-deploy/issues/new) and let us know about your use case!


# 2018-12-23

## (BC Break) More SSL certificate retrieval methods

The playbook now lets you decide between 3 different SSL certificate retrieval methods:
- (default) obtaining free SSL certificates from Let's Encrypt
- generating self-signed SSL certificates
- managing SSL certificates manually

Learn more in [Adjusting SSL certificate retrieval](docs/configuring-playbook-ssl-certificates.md).

For people who use Let's Encrypt (mostly everyone, since it's the default), you'll also have to rename a variable in your configuration:

- before: `host_specific_matrix_ssl_support_email`
- after: `host_specific_matrix_ssl_lets_encrypt_support_email`


## (BC Break) mxisd upgrade with multiple base DN support

mxisd has bee upgraded to [version 1.2.2](https://github.com/kamax-matrix/mxisd/releases/tag/v1.2.2), which supports [multiple base DNs](https://github.com/kamax-matrix/mxisd/blob/v1.2.2/docs/stores/ldap.md#base).

If you were configuring this playbook's `matrix_mxisd_ldap_connection_baseDn` variable until now (a string containing a single base DN), you'll need to change to configuring the `matrix_mxisd_ldap_connection_baseDns` variable (an array containing multiple base DNs).

Example change:

- before: `matrix_mxisd_ldap_connection_baseDn: OU=Users,DC=example,DC=org`
- after: `matrix_mxisd_ldap_connection_baseDns: ['OU=Users,DC=example,DC=org']`


# 2018-12-21

## Synapse 0.34.0 and Python 3

Synapse has been upgraded to 0.34.0 and now uses Python 3.
Based on feedback from others, running Synapse on Python 3 is supposed to decrease memory usage significantly (~2x).


# 2018-12-12

## Riot homepage customization

You can now customize some parts of the Riot homepage (or even completely replace it with your own custom page).
See the `matrix_riot_web_homepage_` variables in `roles/matrix-riot-web/defaults/main.yml`.


# 2018-12-04

## mxisd extensibility

The [LDAP identity store for mxisd](https://github.com/kamax-matrix/mxisd/blob/master/docs/stores/ldap.md) can now be configured easily using playbook variables (see the `matrix_mxisd_ldap_` variables in `roles/matrix-server/defaults/main.yml`).


# 2018-11-28

## More scripts

* matrix-remove-all allows to uninstall everything with a single command
* matrix-make-user-admin allows to upgrade a user's privileges

## LDAP auth support via matrix-synapse-ldap3

The playbook can now install and configure [LDAP auth support](https://github.com/matrix-org/matrix-synapse-ldap3) for you.

Additional details are available in [Setting up the LDAP authentication password provider module](docs/configuring-playbook-ldap-auth.md).


# 2018-11-23

## Support for controlling public registration and room auto-join

The playbook now lets you enable public registration for users (controlled via `matrix_synapse_enable_registration`).
By default, public registration is forbidden.

You can also make people automatically get auto-joined to rooms (controlled via `matrix_synapse_auto_join_rooms`).

## Support for changing the welcome user id (welcome bot)

By default, `@riot-bot:matrix.org` is used to welcome newly registered users.
This can be changed to something else (or disabled) via the new `matrix_riot_web_welcome_user_id` variable.


# 2018-11-14

## Ability to set Synapse log levels

The playbook now allows you to set the log levels used by Synapse. The default logging levels remain the same.

You can now override following variables with any of the supported log levels listed here: https://docs.python.org/3/library/logging.html#logging-levels

```
matrix_synapse_log_level: "INFO"
matrix_synapse_storage_sql_log_level: "INFO"
matrix_synapse_root_log_level: "INFO"
```


# 2018-11-03

## Customize parts of Riot's config

You can now customize some parts of Riot's `config.json`. These playbook variables, with these default values, have been added:

```
matrix_riot_web_disable_custom_urls: true
matrix_riot_web_disable_guests: true
matrix_riot_web_integrations_ui_url: "https://scalar.vector.im/"
matrix_riot_web_integrations_rest_url: "https://scalar.vector.im/api"
matrix_riot_web_integrations_widgets_urls: "https://scalar.vector.im/api"
matrix_riot_web_integrations_jitsi_widget_url: "https://scalar.vector.im/api/widgets/jitsi.html"
```

This now allows you use a custom integrations manager like [Dimesion](https://dimension.t2bot.io). For example, if you wish to use the Dimension instance hosted at dimension.t2bot.io, you can set the following in your vars.yml file:

```
matrix_riot_web_integrations_ui_url: "https://dimension.t2bot.io/riot"
matrix_riot_web_integrations_rest_url: "https://dimension.t2bot.io/api/v1/scalar"
matrix_riot_web_integrations_widgets_urls: "https://dimension.t2bot.io/widgets"
matrix_riot_web_integrations_jitsi_widget_url: "https://dimension.t2bot.io/widgets/jitsi"
```

## SSL protocols used to serve Riot and Synapse

There's now a new `matrix_nginx_proxy_ssl_protocols` playbook variable, which controls the SSL protocols used to serve Riot and Synapse. Its default value is `TLSv1.1 TLSv1.2`. This playbook previously used `TLSv1 TLSv1.1 TLSv1.2` to serve Riot and Synapse.

You may wish to reenable TLSv1 if you need to access Riot in older browsers.

Note: Currently the dockerized nginx doesn't support TLSv1.3. See https://github.com/nginxinc/docker-nginx/issues/190 for more details.


# 2018-11-01

## Postgres 11 support

The playbook now installs [Postgres 11](https://www.postgresql.org/about/news/1894/) by default.

If you have have an existing setup, it's likely running on an older Postgres version (9.x or 10.x). You can easily upgrade by following the [upgrading PostgreSQL guide](docs/maintenance-postgres.md#upgrading-postgresql).


## (BC Break) Renaming playbook variables

Due to the large amount of features added to this playbook lately, to keep things manageable we've had to reorganize its configuration variables a bit.

The following playbook variables were renamed:

- from `matrix_docker_image_mxisd` to `matrix_mxisd_docker_image`
- from `matrix_docker_image_mautrix_telegram` to `matrix_mautrix_telegram_docker_image`
- from `matrix_docker_image_mautrix_whatsapp` to `matrix_mautrix_whatsapp_docker_image`
- from `matrix_docker_image_mailer` to `matrix_mailer_docker_image`
- from `matrix_docker_image_coturn` to `matrix_coturn_docker_image`
- from `matrix_docker_image_goofys` to `matrix_s3_goofys_docker_image`
- from `matrix_docker_image_riot` to `matrix_riot_web_docker_image`
- from `matrix_docker_image_nginx` to `matrix_nginx_proxy_docker_image`
- from `matrix_docker_image_synapse` to `matrix_synapse_docker_image`
- from `matrix_docker_image_postgres_v9` to `matrix_postgres_docker_image_v9`
- from `matrix_docker_image_postgres_v10` to `matrix_postgres_docker_image_v10`
- from `matrix_docker_image_postgres_latest` to `matrix_postgres_docker_image_latest`


# 2018-10-26

## Mautrix Whatsapp bridging support

The playbook now supports bridging with [Whatsapp](https://www.whatsapp.com/) by installing the [mautrix-whatsapp](https://github.com/tulir/mautrix-whatsapp) bridge. This playbook functionality is available thanks to [@izissise](https://github.com/izissise).

Additional details are available in [Setting up Mautrix Whatsapp bridging](docs/configuring-playbook-bridge-mautrix-whatsapp.md).


# 2018-10-25

## Support for controlling Matrix federation

The playbook can now help you with [Controlling Matrix federation](docs/configuring-playbook-federation), should you wish to run a more private (isolated) server.


# 2018-10-24

## Disabling riot-web guests

From now on, Riot's configuration setting `disable_guests` would be set to `true`.
The homeserver was rejecting guests anyway, so this is just a cosmetic change affecting Riot's UI.


# 2018-10-21

## Self-check maintenance command

The playbook can now [check if services are configured correctly](docs/maintenance-checking-services.md).


# 2018-10-05

## Presence tracking made configurable

The playbook can now enable/disable user presence-status tracking in Synapse, through the playbook's `matrix_synapse_use_presence` variable (having a default value of `true` - enabled).

If users participate in large rooms with many other servers, disabling presence will decrease server load significantly.


# 2018-09-27

## Synapse Cache Factor made configurable

The playbook now makes the Synapse cache factor configurable, through the playbook's `matrix_synapse_cache_factor` variable (having a default value of `0.5`).

Changing that value allows you to potentially decrease RAM usage or to increase performance by caching more stuff.
Some information on it is available here: https://github.com/matrix-org/synapse#help-synapse-eats-all-my-ram


# 2018-09-26

## Disabling Docker container logging

`--log-driver=none` is used for all Docker containers now.

All these containers are started through systemd anyway and get logged in journald, so there's no need for Docker to be logging the same thing using the default `json-file` driver. Doing that was growing `/var/lib/docker/containers/..` infinitely until service/container restart.

As a result of this, things like `docker logs matrix-synapse` won't work anymore. `journalctl -u matrix-synapse` is how one can see the logs.


# 2018-09-17

## Service discovery support

The playbook now helps you set up [service discovery](https://matrix.org/docs/spec/client_server/r0.4.0.html#server-discovery) using a `/.well-known/matrix/client` file.

Additional details are available in [Configuring service discovery via .well-known](docs/configuring-well-known.md).


## (BC Break) Renaming playbook variables

The following playbook variables were renamed:

- from `matrix_nginx_riot_web_data_path` to `matrix_riot_web_data_path`
- from `matrix_riot_web_default_identity_server_url` to `matrix_identity_server_url`


# 2018-09-07

## Mautrix Telegram bridging support

The playbook now supports bridging with [Telegram](https://telegram.org/) by installing the [mautrix-telegram](https://github.com/tulir/mautrix-telegram) bridge. This playbook functionality is available thanks to [@izissise](https://github.com/izissise).

Additional details are available in [Setting up Mautrix Telegram bridging](docs/configuring-playbook-bridge-mautrix-telegram.md).


## Events cache size increase and configurability for Matrix Synapse

The playbook now lets you configure Matrix Synapse's `event_cache_size` configuration via the `matrix_synapse_event_cache_size` playbook variable.

Previously, this value was hardcoded to `"10K"`. From now on, a more reasonable default of `"100K"` is used.


## Password-peppering support for Matrix Synapse

The playbook now supports enabling password-peppering for increased security in Matrix Synapse via the `matrix_synapse_password_config_pepper` playbook variable. Using a password pepper is disabled by default (just like it used to be before this playbook variable got introduced) and is not to be enabled/disabled after initial setup, as that would invalidate all existing passwords.


## Statistics-reporting support for Matrix Synapse

There's now a new `matrix_synapse_report_stats` playbook variable, which controls the `report_stats` configuration option for Matrix Synapse. It defaults to `false`, so no change is required to retain your privacy.

If you'd like to start reporting statistics about your homeserver (things like number of users, number of messages sent, uptime, load, etc.) to matrix.org, you can turn on stats reporting.


# 2018-08-29

## Changing the way SSL certificates are retrieved

We've been using [acmetool](https://github.com/hlandau/acme) (with the [willwill/acme-docker](https://hub.docker.com/r/willwill/acme-docker/) Docker image) until now.

Due to the Docker image being deprecated, and things looking bleak for acmetool's support of the newer ACME v2 API endpoint, we've switched to using [certbot](https://certbot.eff.org/) (with the [certbot/certbot](https://hub.docker.com/r/certbot/certbot/) Docker image).

Simply re-running the playbook will retrieve new certificates (via certbot) for you.
To ensure you don't leave any old files behind, though, you'd better do this:

- `systemctl stop 'matrix*'`
- stop your custom webserver, if you're running one (only affects you if you've installed with `matrix_nginx_proxy_enabled: false`)
- `mv /matrix/ssl /matrix/ssl-acmetool-delete-later`
- re-run the playbook's [installation](docs/installing.md)
- possibly delete `/matrix/ssl-acmetool-delete-later`


# 2018-08-21

## Matrix Corporal support

The playbook can now install and configure [matrix-corporal](https://github.com/devture/matrix-corporal) for you.

Additional details are available in [Setting up Matrix Corporal](docs/configuring-playbook-matrix-corporal.md).


# 2018-08-20

## Matrix Synapse rate limit control variables

The following new variables can now be configured to control Matrix Synapse's rate-limiting (default values are shown below).

```yaml
matrix_synapse_rc_messages_per_second: 0.2
matrix_synapse_rc_message_burst_count: 10.0
```

## Shared Secret Auth support via matrix-synapse-shared-secret-auth

The playbook can now install and configure [matrix-synapse-shared-secret-auth](https://github.com/devture/matrix-synapse-shared-secret-auth) for you.

Additional details are available in [Setting up the Shared Secret Auth password provider module](docs/configuring-playbook-shared-secret-auth.md).


# 2018-08-17

## REST auth support via matrix-synapse-rest-auth

The playbook can now install and configure [matrix-synapse-rest-auth](https://github.com/kamax-io/matrix-synapse-rest-auth) for you.

Additional details are available in [Setting up the REST authentication password provider module](docs/configuring-playbook-rest-auth.md).


## Compression improvements

Shifted Matrix Synapse compression from happening in the Matrix Synapse,
to happening in the nginx proxy that's in front of it.

Additionally, `riot-web` also gets compressed now (in the nginx proxy),
which drops the initial page load's size from 5.31MB to 1.86MB.


## Disabling some unnecessary Synapse services

The following services are not necessary, so they have been disabled:
- on the federation port (8448): the `client` service
- on the http port (8008, exposed over 443): the old Angular `webclient` and the `federation` service

Federation runs only on the federation port (8448) now.
The Client APIs run only on the http port (8008) now.


# 2018-08-15

## mxisd Identity Server support

The playbook now sets up an [mxisd](https://github.com/kamax-io/mxisd) Identity Server for you by default.
Additional details are available in [Adjusting mxisd Identity Server configuration](docs/configuring-playbook-mxisd.md).


# 2018-08-14

## Email-sending support

The playbook now configures an email-sending service (postfix) by default.
Additional details are available in [Adjusting email-sending settings](docs/configuring-playbook-email.md).

With this, Matrix Synapse is able to send email notifications for missed messages, etc.


# 2018-08-08


## (BC Break) Renaming playbook variables

The following playbook variables were renamed:

- from `matrix_max_upload_size_mb` to `matrix_synapse_max_upload_size_mb`
- from `matrix_max_log_file_size_mb` to `matrix_synapse_max_log_file_size_mb`
- from `matrix_max_log_files_count` to `matrix_synapse_max_log_files_count`
- from `docker_matrix_image` to `matrix_docker_image_synapse`
- from `docker_nginx_image` to `matrix_docker_image_nginx`
- from `docker_riot_image` to `matrix_docker_image_riot`
- from `docker_goofys_image` to `matrix_docker_image_goofys`
- from `docker_coturn_image` to `matrix_docker_image_coturn`

If you're overriding any of them in your `vars.yml` file, you'd need to change to the new names.


## Renaming Ansible playbook tag

The command for executing the whole playbook has changed.
The `setup-main` tag got renamed to `setup-all`.


## Docker container linking

Changed the way the Docker containers are linked together. The ones that need to communicate with others operate in a `matrix` network now and not in the default bridge network.
