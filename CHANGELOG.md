# 2018-09-07

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
