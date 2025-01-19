# Setting up matrix-hookshot (optional)

The playbook can install and configure [matrix-hookshot](https://github.com/matrix-org/matrix-hookshot) for you.

Hookshot can bridge [Webhooks](https://en.wikipedia.org/wiki/Webhook) from software project management services such as GitHub, GitLab, Jira, and Figma, as well as generic webhooks.

See the project's [documentation](https://matrix-org.github.io/matrix-hookshot/latest/hookshot.html) to learn what it does and why it might be useful to you.

**Note**: the playbook also supports [matrix-appservice-webhooks](configuring-playbook-bridge-appservice-webhooks.md), which however was deprecated by its author.

## Prerequisites

### Download GitHub app private key (optional)

If you're setting up the GitHub bridge, you need to create your GitHub app, and generate a private key file of it.

You need to download the private key file, if you will install the file manually or with the `aux` role. For details, see [the section below](#manage-github-private-key-with-aux-role).

## Adjusting the playbook configuration

Add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file. Make sure to replace `GITHUB_PRIVATE_KEY_HERE` with the one created [above](#download-github-app-private-key).

```yaml
matrix_hookshot_enabled: true

# Uncomment to enable end-to-bridge encryption.
# See: https://matrix-org.github.io/matrix-hookshot/latest/advanced/encryption.html
# matrix_hookshot_experimental_encryption_enabled: true

# Uncomment and paste the contents of GitHub app private key to enable GitHub bridge.
# Alternatively, you can use one of the other methods explained below on the "Manage GitHub Private Key with aux role" section.
# matrix_hookshot_github_private_key: "GITHUB_PRIVATE_KEY_HERE"
```

For each of the services (GitHub, GitLab, Jira, Figma, and generic webhooks) fill in the respective variables `matrix_hookshot_service_*` listed in [main.yml](../roles/custom/matrix-bridge-hookshot/defaults/main.yml) as required.

Take special note of the `matrix_hookshot_*_enabled` variables. Services that need no further configuration are enabled by default (GitLab and generic webhooks), while you must first add the required configuration and enable the others (GitHub, Jira, and Figma).

### Extending the configuration

You can configure additional options by adding the `matrix_hookshot_configuration_extension_yaml` and `matrix_hookshot_registration_extension_yaml` variables.

Refer the [official instructions](https://matrix-org.github.io/matrix-hookshot/latest/setup.html) and the comments in [main.yml](../roles/custom/matrix-bridge-hookshot/defaults/main.yml) to learn what the individual options do.

## Installing

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-service hookshot` or `just setup-all`

`just install-service hookshot` is useful for maintaining your setup quickly when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note `just setup-all` runs the `ensure-matrix-users-created` tag too.

## Usage

To use the bridge, you need to create a room and invite the Hookshot bot (`@hookshot:example.com`) to it.

Make sure the bot is able to send state events (usually the Moderator power level in clients).

Send `!hookshot help` to the bot to see the available commands.

Refer to [Hookshot's documentation](https://matrix-org.github.io/matrix-hookshot/latest/usage.html) for more details about using the bridge's various features.

💡 **Note**: the different listeners are bound to certain paths which might differ from those assumed by the hookshot documentation. See [URLs for bridges setup](#urls-for-bridges-setup) below.

### Reset crypto store

Should the crypto store be corrupted, you can reset it by executing this Ansible playbook with the tag `reset-hookshot-encryption` added:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=reset-hookshot-encryption
```

## More setup documentation

### URLs for bridges setup

Unless indicated otherwise, the following endpoints are reachable on your `matrix.` subdomain (if the feature is enabled).

| Listener | Default path | Variable | Used as |
|---|---|---|---|
| - | `/hookshot/webhooks/` | `matrix_hookshot_webhook_endpoint` | Webhook-prefix, which affects all webhook-related URLs below |
| generic | `/hookshot/webhooks/webhook` | `matrix_hookshot_generic_endpoint` | Generic webhooks |
| github oauth | `/hookshot/webhooks/oauth` | `matrix_hookshot_github_oauth_endpoint` | GitHub "Callback URL" |
| jira oauth | `/hookshot/webhooks/jira/oauth` | `matrix_hookshot_jira_oauth_endpoint` | Jira OAuth |
| figma endpoint | `/hookshot/webhooks/figma/webhook` | `matrix_hookshot_figma_endpoint` | Figma |
| provisioning | `/hookshot/v1/` | `matrix_hookshot_provisioning_endpoint` | Dimension [provisioning](#provisioning-api) |
| appservice | `/hookshot/_matrix/app/` | `matrix_hookshot_appservice_endpoint` | Matrix server |
| widgets | `/hookshot/widgetapi/` | `matrix_hookshot_widgets_endpoint` | Widgets |
| metrics | `/metrics/hookshot` | `matrix_hookshot_metrics_enabled` and exposure enabled via `matrix_hookshot_metrics_proxying_enabled` or `matrix_metrics_exposure_enabled`. Read more in the [Metrics section](#metrics) below. | Prometheus |

Also see the various `matrix_hookshot_container_labels_*` variables in [main.yml](../roles/custom/matrix-bridge-hookshot/defaults/main.yml), which expose URLs publicly

The different listeners are also reachable *internally* in the docker-network via the container's name (configured by `matrix_hookshot_container_url`) and on different ports (e.g. `matrix_hookshot_appservice_port`). Read [main.yml](../roles/custom/matrix-bridge-hookshot/defaults/main.yml) in detail for more info.

### Manage GitHub Private Key with aux role

The GitHub bridge requires you to install a private key file. This can be done in multiple ways:

- copy the *contents* of the downloaded file and set the variable `matrix_hookshot_github_private_key` to the contents (see example in [main.yml](../roles/custom/matrix-bridge-hookshot/defaults/main.yml)).
- somehow copy the file to the path `{{ matrix_hookshot_base_path }}/{{ matrix_hookshot_github_private_key_file }}` (default: `/matrix/hookshot/private-key.pem`) on the server manually.
- use the [`aux` role](https://github.com/mother-of-all-self-hosting/ansible-role-aux) to copy the file from an arbitrary path on your ansible client to the correct path on the server.

To use the `aux` role, make sure the `matrix_hookshot_github_private_key` variable is empty. Then add the following configuration to your `vars.yml` file:

```yaml
aux_file_definitions:
  - dest: "{{ matrix_hookshot_base_path }}/{{ matrix_hookshot_github_private_key_file }}"
    content: "{{ lookup('file', '/path/to/your-github-private-key.pem') }}"
    mode: '0400'
    owner: "{{ matrix_user_username }}"
    group: "{{ matrix_user_groupname }}"
```

For more information, see the documentation in the [default configuration of the aux role](https://github.com/mother-of-all-self-hosting/ansible-role-aux/blob/main/defaults/main.yml).

### Provisioning API

The provisioning API will be enabled automatically if you set `matrix_dimension_enabled: true` and provided a `matrix_hookshot_provisioning_secret`, unless you override it either way. To use hookshot with dimension, you will need to enter as "Provisioning URL": `http://matrix-hookshot:9002`, which is made up of the variables `matrix_hookshot_container_url` and `matrix_hookshot_provisioning_port`.

### Metrics

Metrics are **only enabled by default** if the builtin [Prometheus](configuring-playbook-prometheus-grafana.md) is enabled (by default, Prometheus isn't enabled). If so, metrics will automatically be collected by Prometheus and made available in Grafana. You will, however, need to set up your own Dashboard for displaying them.

To explicitly enable metrics, use `matrix_hookshot_metrics_enabled: true`. This only exposes metrics over the container network, however.

**To collect metrics from an external Prometheus server**, besides enabling metrics as described above, you will also need to enable metrics exposure on `https://matrix.example.com/metrics/hookshot` by:

- either enabling metrics exposure for Hookshot via `matrix_hookshot_metrics_proxying_enabled: true`
- or enabling metrics exposure for all services via `matrix_metrics_exposure_enabled: true`

Whichever one you go with, by default metrics are exposed publicly **without** password-protection. See [the Prometheus and Grafana docs](configuring-playbook-prometheus-grafana.md) for details about password-protection for metrics.

### Collision with matrix-appservice-webhooks

If you are also running [matrix-appservice-webhooks](configuring-playbook-bridge-appservice-webhooks.md), it reserves its namespace by the default setting `matrix_appservice_webhooks_user_prefix: '_webhook_'`. You should take care if you modify its or hookshot's prefix that they do not collide with each other's namespace (default `matrix_hookshot_generic_userIdPrefix: '_webhooks_'`).
