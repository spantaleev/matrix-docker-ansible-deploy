# Setting up Hookshot (optional)

The playbook can install and configure [matrix-hookshot](https://github.com/Half-Shot/matrix-hookshot) for you.

See the project's [documentation](https://half-shot.github.io/matrix-hookshot/hookshot.html) to learn what it does and why it might be useful to you.


## Setup Instructions

Refer to the [official instructions](https://half-shot.github.io/matrix-hookshot/setup.html) to learn what the individual options do.

1. For each of the services (GitHub, GitLab, Jira, Figma, generic webhooks) fill in the respective variables `matrix_hookshot_service_*` listed in [main.yml](roles/matrix-bridge-hookshot/defaults/main.yml) as required.
2. Take special note of the `matrix_hookshot_*_enabled` variables. Services that need no further configuration are enabled by default (GitLab, Generic), while you must first add the required configuration and enable the others (GitHub, Jira, Figma).
3. If you're setting up the GitHub bridge, you'll need to generate and download a private key file after you created your GitHub app. Before running the playbook, you need to copy that file to `roles/matrix-bridge-hookshot/files/private-key.pem` so the playbook can install it for you.
4. If you've already installed Matrix services using the playbook before, you'll need to re-run it (`--tags=setup-all,start`). If not, proceed with [configuring other playbook services](configuring-playbook.md) and then with [Installing](installing.md). Get back to this guide once ready. Hookshot can be set up individually using the tag `setup-hookshot`.
5. Refer to the [official instructions](https://half-shot.github.io/matrix-hookshot/usage.html) to start using the bridge.


The provisioning API will be enabled automatically if you set `matrix_dimension_enabled: true` and provided a `matrix_hookshot_provisioning_secret`, unless you override it either way. To use hookshot with dimension, you will need to enter as "Provisioning URL": `http://matrix-hookshot:9002`, which is made up of the variables `matrix_hookshot_container_url` and `matrix_hookshot_provisioning_port`.

If metrics are enabled, they will be automatically available in the builtin Prometheus and Grafana, but you need to set up your own Dashboard for now. If additionally metrics proxying for use with external Prometheus is enabled (`matrix_nginx_proxy_proxy_synapse_metrics`), hookshot metrics will also be available (at `matrix_hookshot_metrics_endpoint`, default `/hookshot/metrics`, on the stats subdomain) and with the same password. See also [the Prometheus and Grafana docs](../configuring-playbook-prometheus-grafana.md).

Other configuration options are available via the `matrix_hookshot_configuration_extension_yaml` and `matrix_hookshot_registration_extension_yaml` variables, see the comments in `/roles/matrix-bridge-hookshot/defaults/main.yml` for how to use them.
