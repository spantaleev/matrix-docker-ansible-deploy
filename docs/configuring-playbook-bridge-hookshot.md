# Setting up matrix-hookshot (optional)

The playbook can install and configure [matrix-hookshot](https://github.com/matrix-org/matrix-hookshot) for you.

Hookshot can bridge [Webhooks](https://en.wikipedia.org/wiki/Webhook) from software project management services such as GitHub, GitLab, JIRA, and Figma, as well as generic webhooks.

See the project's [documentation](https://matrix-org.github.io/matrix-hookshot/latest/hookshot.html) to learn what it does and why it might be useful to you.

**Note**: the playbook also supports [matrix-appservice-webhooks](configuring-playbook-bridge-appservice-webhooks.md), which however was deprecated by its author.

## Setup Instructions

Refer to the [official instructions](https://matrix-org.github.io/matrix-hookshot/latest/setup.html) to learn what the individual options do.

1. Enable the bridge by adding `matrix_hookshot_enabled: true` to your `vars.yml` file
2. For each of the services (GitHub, GitLab, Jira, Figma, generic webhooks) fill in the respective variables `matrix_hookshot_service_*` listed in [main.yml](/roles/custom/matrix-bridge-hookshot/defaults/main.yml) as required.
3. Take special note of the `matrix_hookshot_*_enabled` variables. Services that need no further configuration are enabled by default (GitLab, Generic), while you must first add the required configuration and enable the others (GitHub, Jira, Figma).
4. If you're setting up the GitHub bridge, you'll need to generate and download a private key file after you created your GitHub app. Copy the contents of that file to the variable `matrix_hookshot_github_private_key` so the playbook can install it for you, or use one of the [other methods](#manage-github-private-key-with-aux-role) explained below.
5. If you've already installed Matrix services using the playbook before, you'll need to re-run it (`--tags=setup-all,start`). If not, proceed with [configuring other playbook services](configuring-playbook.md) and then with [Installing](installing.md). Get back to this guide once ready. Hookshot can be set up individually using the tag `setup-hookshot`.

Other configuration options are available via the `matrix_hookshot_configuration_extension_yaml` and `matrix_hookshot_registration_extension_yaml` variables, see the comments in [main.yml](/roles/custom/matrix-bridge-hookshot/defaults/main.yml) for how to use them.

Finally, run the playbook (see [installing](installing.md)).

### End-to-bridge encryption

You can enable [encryption](https://matrix-org.github.io/matrix-hookshot/latest/advanced/encryption.html) for Hookshot by adding `matrix_hookshot_encryption_enabled: true` to your configuration (`vars.yml`) and [executing the playbook](installing.md) again.

Should the crypto store be corrupted, you can reset it by executing this Ansible playbook with the tag `reset-hookshot-encryption` added, for example `ansible-playbook -i inventory/hosts setup.yml --tags=reset-hookshot-encryption`.

## Usage

To use the bridge, you need to create a room and invite the Hookshot bot (`@hookshot:example.com`) to it.

Make sure the bot is able to send state events (usually the Moderator power level in clients).

Send a `!hookshot help` message to see a list of help commands.

Refer to [Hookshot's documentation](https://matrix-org.github.io/matrix-hookshot/latest/usage.html) for more details about using the bridge's various features.

**Important**: Note that the different listeners are bound to certain paths which might differ from those assumed by the hookshot documentation, see [URLs for bridges setup](#urls-for-bridges-setup) below.

## More setup documentation

### URLs for bridges setup

Unless indicated otherwise, the following endpoints are reachable on your `matrix.` subdomain (if the feature is enabled).

| listener | default path | variable | used as |
|---|---|---|---|
| - | `/hookshot/webhooks/` | `matrix_hookshot_webhook_endpoint` | Webhook-prefix, which affects all webhook-related URLs below |
| generic | `/hookshot/webhooks/webhook` | `matrix_hookshot_generic_endpoint` | Generic webhooks |
| github oauth | `/hookshot/webhooks/oauth` | `matrix_hookshot_github_oauth_endpoint` | GitHub "Callback URL" |
| jira oauth | `/hookshot/webhooks/jira/oauth` | `matrix_hookshot_jira_oauth_endpoint` | JIRA OAuth |
| figma endpoint | `/hookshot/webhooks/figma/webhook` | `matrix_hookshot_figma_endpoint` | Figma |
| provisioning | `/hookshot/v1/` | `matrix_hookshot_provisioning_endpoint` | Dimension [provisioning](#provisioning-api) |
| appservice | `/hookshot/_matrix/app/` | `matrix_hookshot_appservice_endpoint` | Matrix server |
| widgets | `/hookshot/widgetapi/` | `matrix_hookshot_widgets_endpoint` | Widgets |
| metrics | `/metrics/hookshot` | `matrix_hookshot_metrics_enabled` and exposure enabled via `matrix_hookshot_metrics_proxying_enabled` or `matrix_metrics_exposure_enabled`. Read more in the [Metrics section](#metrics) below. | Prometheus |

Also see the various `matrix_hookshot_container_labels_*` variables in [main.yml](/roles/custom/matrix-bridge-hookshot/defaults/main.yml), which expose URLs publicly.

The different listeners are also reachable *internally* in the docker-network via the container's name (configured by `matrix_hookshot_container_url`) and on different ports (e.g. `matrix_hookshot_appservice_port`). Read [main.yml](/roles/custom/matrix-bridge-hookshot/defaults/main.yml) in detail for more info.

### Manage GitHub Private Key with aux role

The GitHub bridge requires you to install a private key file. This can be done in multiple ways:
- copy the *contents* of the downloaded file and set the variable `matrix_hookshot_github_private_key` to the contents (see example in [main.yml](/roles/custom/matrix-bridge-hookshot/defaults/main.yml)).
- somehow copy the file to the path `{{ matrix_hookshot_base_path }}/{{ matrix_hookshot_github_private_key_file }}` (default: `/matrix/hookshot/private-key.pem`) on the server manually.
- use the [`aux` role](https://github.com/mother-of-all-self-hosting/ansible-role-aux) to copy the file from an arbitrary path on your ansible client to the correct path on the server.

To use the `aux` role, make sure the `matrix_hookshot_github_private_key` variable is empty. Then add the following additional configuration:

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
