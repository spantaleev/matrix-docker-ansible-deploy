# Enabling Telemetry for your Matrix server (optional)

By default, this playbook configures your Matrix homeserver to not send any telemetry data anywhere.

The [matrix.org](https://matrix.org) team would really appreciate it if you could help the project out by reporting
anonymized usage statistics from your homeserver. Only very [basic aggregate
data](#usage-statistics-being-submitted) (e.g. number of users) will be reported, but it helps track the
growth of the Matrix community, and helps to make Matrix a success.


## Enabling Telemetry

If you'd like to **help by enabling submission of general usage statistics** for your homeserver, add this to your configuration file (`inventory/host_vars/matrix.<your-domain>/vars.yml`):

```yaml
matrix_synapse_report_stats: true
```


## Usage statistics being submitted

If statistics reporting is enabled, the information that gets submitted to the matrix.org team [according to the source code](https://github.com/matrix-org/synapse/blob/master/synapse/app/homeserver.py) is:

- your homeserver's domain name

- uptime of the homeserver program

- [Python](https://www.python.org/) version powering your homeserver

- total number of users on your home server (including bridged users)

- total number of native Matrix users on your home server

- total number of rooms on your homeserver

- total number of daily active users on your homeserver

- total number of daily active rooms on your homeserver

- total number of messages sent per day

- cache setting information

- CPU and memory statistics for the homeserver program

- database engine type and version
