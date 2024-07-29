# Setting up synapse-usage-exporter (optional)

[synapse-usage-exporter](https://github.com/loelkes/synapse-usage-exporter) allows you to export the usage statistics of a Synapse homeserver to this container service and for the collected metrics to later be scraped by Prometheus.

Synapse does not include usage statistics in its Prometheus metrics. They can be reported to an HTTP `PUT` endpoint 5 minutes after startup and from then on at a fixed interval of once every three hours. This role integrates a simple [Flask](https://flask.palletsprojects.com) project that offers an HTTP `PUT` endpoint and holds the most recent received record available to be scraped by Prometheus.

Enabling this service will automatically:

- install the synapse-usage-exporter service
- re-configure Synapse to push (via HTTP `PUT`) usage statistics information to synapse-usage-exporter
- re-configure [Prometheus](./configuring-playbook-prometheus-grafana.md) (if Prometheus is enabled), to periodically scrape metrics from synapse-usage-exporter
- add a new [Grafana](./configuring-playbook-prometheus-grafana.md) dashboard (if Grafana is enabled) containing Synapse usage statistics

## Quickstart

Add the following configuration to your `inventory/host_vars/matrix.DOMAIN/vars.yml` file and [re-run the installation process](./installing.md) for the playbook:

```yaml
matrix_synapse_usage_exporter_enabled: true

# (Optional) Expose endpoint if you want to collect statistics from outside (from other homeservers).
# If enabled, synapse-usage-exporter will be exposed publicly at `matrix.DOMAIN/report-usage-stats/push`.
# When collecting usage statistics for Synapse running on the same host, you don't need to enable this.
# You can adjust the hostname and path via `matrix_synapse_usage_exporter_hostname` and `matrix_synapse_usage_exporter_path_prefix`.
# matrix_synapse_usage_exporter_proxying_enabled: true
```
