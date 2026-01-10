<!--
SPDX-FileCopyrightText: 2019 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2020 Marcel Partap
SPDX-FileCopyrightText: 2021 - 2023 MDAD project contributors
SPDX-FileCopyrightText: 2021 Sergei Shikalov
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara
SPDX-FileCopyrightText: 2024 Daniel Vinci

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Configuring Synapse (optional)

By default, this playbook configures the [Synapse](https://github.com/element-hq/synapse) Matrix server, so that it works for the general case. If that's okay, you can skip this document.

💡 See this page for details about maintaining Synapse: [Synapse maintenance](maintenance-synapse.md)

## Adjusting the playbook configuration

### Load balancing with workers

To have Synapse gracefully handle thousands of users, worker support should be enabled. It factors out some homeserver tasks and spreads the load of incoming client and server-to-server traffic between multiple processes. More information can be found in the [official Synapse workers documentation](https://github.com/element-hq/synapse/blob/master/docs/workers.md) and [Tom Foster](https://github.com/tcpipuk)'s [Synapse homeserver guide](https://tcpipuk.github.io/synapse/index.html).

To enable Synapse worker support, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_synapse_workers_enabled: true

matrix_synapse_workers_preset: one-of-each
```

By default, this enables the `one-of-each` [worker preset](#worker-presets), but you may wish to use another preset or [control the number of worker instances](#controlling-the-number-of-worker-instances).

#### Worker presets

We support a few configuration presets (`matrix_synapse_workers_preset: one-of-each` being the default configuration right now):

- (federation-only) `little-federation-helper` — a very minimal worker configuration to improve federation performance
- (generic) `one-of-each` — defaults to one worker of each supported type — no smart routing, just generic workers
- (specialized) `specialized-workers` — defaults to one worker of each supported type, but disables generic workers and uses [specialized workers](#specialized-workers) instead

These presets represent a few common configurations. There are many worker types which can be mixed and matched based on your needs.

##### Generic workers

Previously, the playbook only supported the most basic type of load-balancing. We call it **generic load-balancing** below, because incoming HTTP requests are sent to a generic worker. Load-balancing was done based on the requestor's IP address. This is simple, but not necessarily optimal. If you're accessing your account from multiple IP addresses (e.g. your mobile phone being on a different network than your PC), these separate requests may potentially be routed to different workers, each of which would need to cache roughly the same data.

This is **still the default load-balancing method (preset) used by the playbook**.

To use generic load-balancing, do not specify `matrix_synapse_workers_preset` to make it use the default value (`one-of-each`), or better yet — explicitly set it as `one-of-each`.

You may also consider [tweaking the number of workers of each type](#controlling-the-number-of-worker-instances) from the default (one of each).

##### Specialized workers

The playbook now supports a smarter **specialized load-balancing** inspired by [Tom Foster](https://github.com/tcpipuk)'s [Synapse homeserver guide](https://tcpipuk.github.io/synapse/index.html). Instead of routing requests to one or more [generic workers](#generic-workers) based only on the requester's IP address, specialized load-balancing routes to **4 different types of specialized workers** based on **smarter criteria** — the access token (username) of the requester and/or on the resource (room, etc.) being requested.

The playbook supports these **4 types** of specialized workers:

- Room workers — handles various [Client-Server](https://spec.matrix.org/v1.9/client-server-api/) & [Federation](https://spec.matrix.org/v1.9/server-server-api) APIs dedicated to handling specific rooms
- Sync workers — handles various [Client-Server](https://spec.matrix.org/v1.9/client-server-api/) APIs related to synchronization (most notably [the `/sync` endpoint](https://spec.matrix.org/v1.9/client-server-api/#get_matrixclientv3sync))
- Client readers — handles various [Client-Server](https://spec.matrix.org/v1.9/client-server-api/) APIs which are not for specific rooms (handled by **room workers**) or for synchronization (handled by **sync workers**)
- Federation readers — handles various [Federation](https://spec.matrix.org/v1.9/server-server-api) APIs which are not for specific rooms (handled by **room workers**)

To use specialized load-balancing, consider enabling the `specialized-workers` [worker preset](#worker-presets) and potentially [tweaking the number of workers of each type](#controlling-the-number-of-worker-instances) from the default (one of each).

##### Controlling the number of worker instances

If you'd like more customization power, you can start with one of the [worker presets](#worker-presets) and then tweak various `matrix_synapse_workers_*_count` variables manually.

To find what variables are available for you to override in your own `vars.yml` configuration file, see the [`defaults/main.yml` file for the `matrix-synapse` Ansible role](../roles/custom/matrix-synapse/defaults/main.yml).

The only thing you **cannot** do is mix [generic workers](#generic-workers) and [specialized workers](#specialized-workers).

##### Effect of enabling workers on the rest of your server

When Synapse workers are enabled, the integrated [Postgres database is tuned](maintenance-postgres.md#tuning-postgresql), so that the maximum number of Postgres connections are increased from `200` to `500`. If you need to decrease or increase the number of maximum Postgres connections further, use the `postgres_max_connections` variable.

A separate Ansible role (`matrix-synapse-reverse-proxy-companion`) and component handles load-balancing for workers. This role/component is automatically enabled when you enable workers. Make sure to use the `setup-all` tag (not `install-all`!) during the playbook's [installation](./installing.md) process, especially if you're disabling workers, so that components may be installed/uninstalled correctly.

In case any problems occur, make sure to have a look at the [list of synapse issues about workers](https://github.com/element-hq/synapse/issues?q=workers+in%3Atitle) and your `journalctl --unit 'matrix-*'`.

### Synapse + OpenID Connect for Single-Sign-On

💡 An alternative to setting up OIDC in Synapse is to use [Matrix Authentication Service](./configuring-playbook-matrix-authentication-service.md) (MAS). Newer clients (like Element X) only support SSO-based authentication via MAS and not via the legacy Synapse OIDC setup described below. That said, MAS is still a new experimental service which comes with its own downsides. Consult its documentation to learn if it will be a good fit for your deployment.

If you'd like to use OpenID Connect authentication with Synapse, you'll need some additional configuration.

This example configuration is for [keycloak](https://www.keycloak.org/), an opensource Identity Provider maintained by Red Hat.

For more detailed documentation on available options and how to setup keycloak, see the [Synapse documentation on OpenID Connect with keycloak](https://github.com/element-hq/synapse/blob/develop/docs/openid.md#keycloak).

In case you encounter errors regarding the parsing of the variables, you can try to add `{% raw %}` and `{% endraw %}` blocks around them. For example ;

```yaml
matrix_synapse_oidc_enabled: true

matrix_synapse_oidc_providers:
  - idp_id: keycloak
    idp_name: "My KeyCloak server"
    issuer: "https://url.ix/realms/{realm_name}"
    client_id: "matrix"
    client_secret: "{{ vault_synapse_keycloak }}"
    scopes: ["openid", "profile"]
    user_mapping_provider:
      config:
        localpart_template: "{% raw %}{{ user.preferred_username }}{% endraw %}"
        display_name_template: "{% raw %}{{ user.name }}{% endraw %}"
        email_template: "{% raw %}{{ user.email }}{% endraw %}"
    allow_existing_users: true # Optional
    backchannel_logout_enabled: true # Optional
```

### Customizing templates

[Templates](https://github.com/element-hq/synapse/blob/develop/docs/templates.md) are used by Synapse for showing **certain web pages** handled by the server, as well as for **email notifications**.

This playbook allows you to customize the default templates (see the [`synapse/res/templates` directory](https://github.com/element-hq/synapse/tree/develop/synapse/res/templates)).

If template customization is enabled, the playbook will build a custom container image based on the official one.

Your custom templates need to live in a public or private git repository. This repository will be cloned during Synapse image customization (during the playbook run).

To enable template customizations, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
# If you'd like to ensure that the customized image is built each time the playbook runs, enable this.
# Otherwise, the customized image will only be rebuilt whenever the Synapse version changes (once every ~2 weeks).
# matrix_synapse_docker_image_customized_build_nocache: true

matrix_synapse_container_image_customizations_templates_enabled: true

# Our templates live in a templates/ directory within the repository.
# If they're at the root path, delete this line.
matrix_synapse_container_image_customizations_templates_in_container_template_files_relative_path: templates

matrix_synapse_container_image_customizations_templates_git_repository_url: git@github.com:organization/repository.git
matrix_synapse_container_image_customizations_templates_git_repository_branch: main

matrix_synapse_container_image_customizations_templates_git_repository_keyscan_enabled: true
matrix_synapse_container_image_customizations_templates_git_repository_keyscan_hostname: github.com

# If your git repository is public, do not define the private key (remove the variable).
matrix_synapse_container_image_customizations_templates_git_repository_ssh_private_key: |
  -----BEGIN OPENSSH PRIVATE KEY-----
  …
  -----END OPENSSH PRIVATE KEY-----
```

As mentioned in Synapse's Templates documentation, Synapse will fall back to its own templates if a template is not found in that directory. Due to this, it's recommended to only store and maintain template files in your repository if you need to make custom changes. Other files (which you don't need to change), should not be duplicated, so that you don't need to worry about getting out-of-sync with the original Synapse templates.

### Extending the configuration

There are some additional things you may wish to configure about the server.

Take a look at:

- `roles/custom/matrix-synapse/defaults/main.yml` for some variables that you can customize via your `vars.yml` file
- `roles/custom/matrix-synapse/templates/synapse/homeserver.yaml.j2` for the server's default configuration. You can override settings (even those that don't have dedicated playbook variables) using the `matrix_synapse_configuration_extension_yaml` variable

## Installing

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

## Usage

### Synapse Admin

With [Synapse Admin](configuring-playbook-synapse-admin.md), certain Synapse administration tasks (managing users and rooms, etc.) can be performed via a web user-interace.

The playbook can install and configure Synapse Admin for you. For details about it, see [this page](configuring-playbook-synapse-admin.md).

### Monitoring Synapse Metrics with Prometheus and Grafana

This playbook allows you to enable Synapse metrics, which can provide insight into the performance and activity of Synapse.

To enable Synapse runtime metrics, see: [Enabling metrics and graphs (Prometheus, Grafana) for your Matrix server](configuring-playbook-prometheus-grafana.md) and [its subsection](configuring-playbook-prometheus-grafana.md#expose-metrics-of-other-services-roles)

To enable Synapse usage metrics, see: [Enabling synapse-usage-exporter for Synapse usage statistics](configuring-playbook-synapse-usage-exporter.md)

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-synapse`.

### Increase logging verbosity

Because Synapse is originally very chatty when it comes to logging, we intentionally reduce its [logging level](https://docs.python.org/3/library/logging.html#logging-levels) from `INFO` to `WARNING`.

If you'd like to debug an issue or [report a Synapse bug](https://github.com/element-hq/synapse/issues/new/choose) to the developers, it'd be better if you temporarily increase the logging verbosity to `INFO`. To do so, add the following configuration to your `vars.yml` file and re-run the playbook:

```yaml
matrix_synapse_log_level: "INFO"
matrix_synapse_storage_sql_log_level: "INFO"
matrix_synapse_root_log_level: "INFO"
