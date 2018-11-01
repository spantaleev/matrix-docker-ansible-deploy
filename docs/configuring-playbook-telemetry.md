# Enabling Telemetry for your Matrix server

By default, this playbook configures your Matrix homeserver to not send any telemetry data anywhere.

The [matrix.org](https://matrix.org) team would really appreciate it if you could help the project out by reporting
anonymized usage statistics from your homeserver. Only very basic aggregate
data (e.g. number of users) will be reported, but it helps track the
growth of the Matrix community, and helps to make Matrix a success.

If you'd like to **help by enabling submission of anonymized usage statistics** for your homeserver, add this to your configuration file (`inventory/matrix.<your-domain>/vars.yml`):

```yaml
matrix_synapse_report_stats: true
```
