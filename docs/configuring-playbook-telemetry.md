# Enabling Telemetry for your Matrix server (optional)

By default, this playbook configures your Matrix homeserver to not send any telemetry data anywhere.

The [matrix.org](https://matrix.org) team would really appreciate it if you could help the project out by reporting
usage statistics from your homeserver. Enabling usage statistics helps track the
growth of the Matrix community, and helps to make Matrix a success.


## Enabling Telemetry

If you'd like to **help by enabling submission of general usage statistics** for your homeserver, add this to your configuration file (`inventory/host_vars/matrix.<your-domain>/vars.yml`):

```yaml
matrix_synapse_report_stats: true
```


## Usage statistics being submitted

See [Synapse's documentation](https://github.com/matrix-org/synapse/blob/develop/docs/usage/administration/monitoring/reporting_homeserver_usage_statistics.md#available-statistics)
for a list of the individual parameters that are reported.
