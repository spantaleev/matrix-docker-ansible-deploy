# Enabling metrics and graphs for Postgres (optional)

Expanding on the metrics exposed by the [synapse exporter and the node exporter](configuring-playbook-prometheus-grafana.md), the playbook enables the [postgres exporter](https://github.com/prometheus-community/postgres_exporter) that exposes more detailed information about what's happening on your postgres database.

You can enable this with the following settings in your configuration file (`inventory/host_vars/matrix.<your-domain>/vars.yml`):


```yaml
matrix_prometheus_postgres_exporter_enabled: true

# the role creates a postgres user as credential. You can configure these if required:
matrix_prometheus_postgres_exporter_database_username: 'matrix_prometheus_postgres_exporter'
matrix_prometheus_postgres_exporter_database_password: 'some-password'

```

## What does it do?

Name | Description
-----|----------
`matrix_prometheus_postgres_exporter_enabled`|Enable the postgres prometheus exporter. This sets up the docker container, connects it to the database and adds a 'job' to the prometheus config which tells prometheus about this new exporter. The default is 'false'
`matrix_prometheus_postgres_exporter_database_username`| The 'username' for the user that the exporter uses to connect to the database. The default is 'matrix_prometheus_postgres_exporter'
`matrix_prometheus_postgres_exporter_database_password`| The 'password' for the user that the exporter uses to connect to the database.


## More information

- [The PostgresSQL dashboard](https://grafana.com/grafana/dashboards/9628) (generic postgres dashboard)

