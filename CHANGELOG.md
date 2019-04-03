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
