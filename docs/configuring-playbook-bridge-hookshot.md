# Setting up Hookshot (optional)

The playbook can install and configure [matrix-hookshot](https://github.com/matrix-org/matrix-hookshot) for you.

Hookshot can bridge [Webhooks](https://en.wikipedia.org/wiki/Webhook) from software project management services such as GitHub, GitLab, JIRA, and Figma, as well as generic webhooks.

See the project's [documentation](https://matrix-org.github.io/matrix-hookshot/hookshot.html) to learn what it does in detail and why it might be useful to you.

Note: the playbook also supports [matrix-appservice-webhooks](configuring-playbook-bridge-appservice-webhooks.md), which however is soon to be archived by its author and to be replaced by hookshot.

## Setup Instructions

Refer to the [official instructions](https://matrix-org.github.io/matrix-hookshot/setup.html) to learn what the individual options do.

1. For each of the services (GitHub, GitLab, Jira, Figma, generic webhooks) fill in the respective variables `matrix_hookshot_service_*` listed in [main.yml](/roles/matrix-bridge-hookshot/defaults/main.yml) as required.
2. Take special note of the `matrix_hookshot_*_enabled` variables. Services that need no further configuration are enabled by default (GitLab, Generic), while you must first add the required configuration and enable the others (GitHub, Jira, Figma).
3. If you're setting up the GitHub bridge, you'll need to generate and download a private key file after you created your GitHub app. Copy the contents of that file to the variable `matrix_hookshot_github_private_key` so the playbook can install it for you, or use one of the [other methods](#manage-github-private-key-with-matrix-aux-role) explained below. 
4. If you've already installed Matrix services using the playbook before, you'll need to re-run it (`--tags=setup-all,start`). If not, proceed with [configuring other playbook services](configuring-playbook.md) and then with [Installing](installing.md). Get back to this guide once ready. Hookshot can be set up individually using the tag `setup-hookshot`.
5. Refer to [Hookshot's official instructions](https://matrix-org.github.io/matrix-hookshot/usage.html) to start using the bridge. Note that the different listeners are bound to certain paths (see `matrix_hookshot_matrix_nginx_proxy_configuration` in [init.yml](/roles/matrix-bridge-hookshot/tasks/init.yml)): by default webhooks root is `/hookshot/webhooks/`.

Other configuration options are available via the `matrix_hookshot_configuration_extension_yaml` and `matrix_hookshot_registration_extension_yaml` variables, see the comments in [main.yml](/roles/matrix-bridge-hookshot/defaults/main.yml) for how to use them.

### Manage GitHub Private Key with matrix-aux role

The GitHub bridge requires you to install a private key file. This can be done in multiple ways:
- copy the *contents* of the downloaded file and set the variable `matrix_hookshot_github_private_key` to the contents (see example in [main.yml](/roles/matrix-bridge-hookshot/defaults/main.yml)).
- somehow copy the file to the path `{{ matrix_hookshot_base_path }}/{{ matrix_hookshot_github_private_key_file }}` (default: `/matrix/hookshot/private-key.pem`) on the server manually.
- use the `matrix-aux` role to copy the file from an arbitrary path on your ansible client to the correct path on the server.

To use `matrix-aux`, make sure the `matrix_hookshot_github_private_key` variable is empty. Then add to `matrix-aux` configuration like this:
```yaml
matrix_aux_file_definitions:
  - dest: "{{ matrix_hookshot_base_path }}/{{ matrix_hookshot_github_private_key_file }}"
    content: "{{ lookup('file', '/path/to/your-github-private-key.pem') }}"
    mode: '0400'
    owner: "{{ matrix_user_username }}"
    group: "{{ matrix_user_groupname }}"
```
For more info see the documentation in the [matrix-aux base configuration file](/roles/matrix-aux/defaults/main.yml).

### Provisioning API

The provisioning API will be enabled automatically if you set `matrix_dimension_enabled: true` and provided a `matrix_hookshot_provisioning_secret`, unless you override it either way. To use hookshot with dimension, you will need to enter as "Provisioning URL": `http://matrix-hookshot:9002`, which is made up of the variables `matrix_hookshot_container_url` and `matrix_hookshot_provisioning_port`.

### Metrics

If metrics are enabled, they will be automatically available in the builtin Prometheus and Grafana, but you need to set up your own Dashboard for now. If additionally metrics proxying for use with external Prometheus is enabled (`matrix_nginx_proxy_proxy_synapse_metrics`), hookshot metrics will also be available (at `matrix_hookshot_metrics_endpoint`, default `/hookshot/metrics`, on the stats subdomain) and with the same password. See also [the Prometheus and Grafana docs](../configuring-playbook-prometheus-grafana.md).

### Collision with matrix-appservice-webhooks

If you are also running [matrix-appservice-webhooks](configuring-playbook-bridge-appservice-webhooks.md), it reserves its namespace by the default setting `matrix_appservice_webhooks_user_prefix: '_webhook_'`. You should take care if you modify its or hookshot's prefix that they do not collide with each other's namespace (default `matrix_hookshot_generic_user_id_prefix: '_webhooks_'`).
