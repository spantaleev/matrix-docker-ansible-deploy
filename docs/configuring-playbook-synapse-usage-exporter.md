# Setting up synapse-usage-exporter (optional)

[synapse-usage-exporter](https://github.com/loelkes/synapse-usage-exporter) Allows you to export the usage statistics of a Synapse homeserver to this container service and be scraped by Prometheus. Synapse does not include usage statistics in its prometheus metrics. They can be reported to a HTTP PUT endpoint 5 minutes after startup and from then on at a fixed interval of once every three hours. This role integrates a simple Flask project that offers a HTTP PUT endpoint and holds the most recent received record available to be scraped py Prometheus.

## Quickstart

Add the following configuration to your `inventory/host_vars/matrix.DOMAIN/vars.yml` file and [re-run the installation process](./installing.md) for the playbook:

```yaml
matrix_synapse_usage_exporter_enabled: true

# (optional) Expose endpoint if you want to collect statistics from other homeservers: `matrix.DOMAIN/report-usage-stats/push`
# matrix_synapse_usage_exporter_proxying_enabled: true
```
