# Enabling Telemetry for your Matrix server (optional)

By default, this playbook configures your Matrix homeserver to not send any telemetry data anywhere.

The [matrix.org](https://matrix.org) team would really appreciate it if you could help the project out by reporting
usage statistics from your homeserver. Enabling usage statistics helps track the
growth of the Matrix community, and helps to make Matrix a success.


## Enabling Telemetry

If you'd like to **help by enabling submission of general usage statistics** for your homeserver, add this to your configuration file (`inventory/host_vars/matrix.<your-domain>/vars.yml`):

```yaml
matrix_synapse_report_stats: true # for synapse 

matrix_dendrite_report_stats: true # for dendrite 
```


## Usage statistics being submitted

When enabled, your homeserver will regularly upload a few dozen statistics about your server.
This data includes your homeserver's domain, the total number of users, the number of active
users, the total number of rooms, and the number of messages sent per day on your homeserver.

See [Synapse's documentation](https://github.com/matrix-org/synapse/blob/develop/docs/usage/administration/monitoring/reporting_homeserver_usage_statistics.md#available-statistics) or [Dendrite's documentation](https://github.com/matrix-org/dendrite/blob/main/docs/FAQ.md#what-is-being-reported-when-enabling-phone-home-statistics)
for the full list of statistics that are reported.
