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
See the `matrix_riot_web_homepage_` variables in `roles/matrix-server/defaults/main.yml`.


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

If you have have an existing setup, it's likely running on an older Postgres version (9.x or 10.x). You can easily upgrade by following the [Maintenance / upgrading PostgreSQL](docs/maintenance-upgrading-postgres.md) guide.


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
