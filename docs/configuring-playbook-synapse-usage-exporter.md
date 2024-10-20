# Setting up synapse-usage-exporter (optional)

[synapse-usage-exporter](https://github.com/loelkes/synapse-usage-exporter) allows you to export the usage statistics of a Synapse homeserver to this container service and for the collected metrics to later be scraped by Prometheus.

Synapse does not include usage statistics in its Prometheus metrics. They can be reported to an HTTP `PUT` endpoint 5 minutes after startup and from then on at a fixed interval of once every three hours. This role integrates a simple [Flask](https://flask.palletsprojects.com) project that offers an HTTP `PUT` endpoint and holds the most recent received record available to be scraped by Prometheus.

Enabling this service will automatically:

- install the synapse-usage-exporter service
- re-configure Synapse to push (via HTTP `PUT`) usage statistics information to synapse-usage-exporter
- re-configure [Prometheus](./configuring-playbook-prometheus-grafana.md) (if Prometheus is enabled), to periodically scrape metrics from synapse-usage-exporter
- add a new [Grafana](./configuring-playbook-prometheus-grafana.md) dashboard (if Grafana is enabled) containing Synapse usage statistics

## Adjusting the playbook configuration

To enable synapse-usage-exporter, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_synapse_usage_exporter_enabled: true

# (Optional) Expose endpoint if you want to collect statistics from outside (from other homeservers).
# If enabled, synapse-usage-exporter will be exposed publicly at `matrix.example.com/report-usage-stats/push`.
# When collecting usage statistics for Synapse running on the same host, you don't need to enable this.
# You can adjust the hostname and path via `matrix_synapse_usage_exporter_hostname` and `matrix_synapse_usage_exporter_path_prefix`.
# matrix_synapse_usage_exporter_proxying_enabled: true
```

### Adjusting the synapse-usage-exporter URL

By default, this playbook installs synapse-usage-exporter on the `matrix.` subdomain, at the `/report-usage-stats/push` path (https://matrix.example.com/report-usage-stats/push). This makes it easy to install it, because it **doesn't require additional DNS records to be set up**. If that's okay, you can skip this section.

By tweaking the `matrix_synapse_usage_exporter_hostname` and `matrix_synapse_usage_exporter_path_prefix` variables, you can easily make the service available at a **different hostname and/or path** than the default one.

Example additional configuration for your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
# Change the default hostname and path prefix
# These variables are used only if (`matrix_synapse_usage_exporter_proxying_enabled: true`)
matrix_synapse_usage_exporter_hostname: sue.example.com
matrix_synapse_usage_exporter_path_prefix: /
```

## Adjusting DNS records

If you've changed the default hostname, **you may need to adjust your DNS** records to point the synapse-usage-exporter domain to the Matrix server.

See [Configuring DNS](configuring-dns.md) for details about DNS changes.

If you've decided to use the default hostname, you won't need to do any extra DNS configuration.

## Installing

After configuring the playbook, run the [installation](installing.md) command: `just install-all` or `just setup-all`
