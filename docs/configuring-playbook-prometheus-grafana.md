# Enabling metrics and graphs for your Matrix server (optional)

It can be useful to have some (visual) insight into the performance of your homeserver.

You can enable this with the following settings in your configuration file (`inventory/host_vars/matrix.<your-domain>/vars.yml`):

Remember to add `stats.<your-domain>` to DNS as described in [Configuring DNS](configuring-dns.md) before running the playbook.

```yaml
matrix_prometheus_enabled: true

matrix_prometheus_node_exporter_enabled: true

matrix_grafana_enabled: true

matrix_grafana_anonymous_access: false

# This has no relation to your Matrix user id. It can be any username you'd like.
# Changing the username subsequently won't work.
matrix_grafana_default_admin_user: "some_username_chosen_by_you"

# Changing the password subsequently won't work.
matrix_grafana_default_admin_password: "some_strong_password_chosen_by_you"
```

By default, a [Grafana](https://grafana.com/) web user-interface will be available at `https://stats.<your-domain>`.

The retention policy of Prometheus metrics is [15 days by default](https://prometheus.io/docs/prometheus/latest/storage/#operational-aspects). Older data gets deleted automatically.


## What does it do?

Name | Description
-----|----------
`matrix_prometheus_enabled`|[Prometheus](https://prometheus.io) is a time series database. It holds all the data we're going to talk about.
`matrix_prometheus_node_exporter_enabled`|[Node Exporter](https://prometheus.io/docs/guides/node-exporter/) is an addon of sorts to Prometheus that collects generic system information such as CPU, memory, filesystem, and even system temperatures
`matrix_grafana_enabled`|[Grafana](https://grafana.com/) is the visual component. It shows (on the `stats.<your-domain>` subdomain) the dashboards with the graphs that we're interested in
`matrix_grafana_anonymous_access`|By default you need to log in to see graphs. If you want to publicly share your graphs (e.g. when asking for help in [`#synapse:matrix.org`](https://matrix.to/#/#synapse:matrix.org?via=matrix.org&via=privacytools.io&via=mozilla.org)) you'll want to enable this option.
`matrix_grafana_default_admin_user`<br>`matrix_grafana_default_admin_password`|By default Grafana creates a user with `admin` as the username and password. If you feel this is insecure and you want to change it beforehand, you can do that here


## Security and privacy

Metrics and resulting graphs can contain a lot of information. This includes system specs but also usage patterns. This applies especially to small personal/family scale homeservers. Someone might be able to figure out when you wake up and go to sleep by looking at the graphs over time. Think about this before enabling anonymous access. And you should really not forget to change your Grafana password.

Most of our docker containers run with limited system access, but the `prometheus-node-exporter` has access to the host network stack and (readonly) root filesystem. This is required to report on them. If you don't like that, you can set `matrix_prometheus_node_exporter_enabled: false` (which is actually the default). You will still get Synapse metrics with this container disabled. Both of the dashboards will always be enabled, so you can still look at historical data after disabling either source.


## Collecting metrics to an external Prometheus server

If you wish, you could expose homeserver metrics without enabling (installing) Prometheus and Grafana via the playbook. This may be useful for hooking Matrix services to an external Prometheus/Grafana installation.

To do this, you may be interested in the following variables:

Name | Description
-----|----------
`matrix_synapse_metrics_enabled`|Set this to `true` to make Synapse expose metrics (locally, on the container network)
`matrix_nginx_proxy_proxy_synapse_metrics`|Set this to `true` to make matrix-nginx-proxy expose the Synapse metrics at `https://matrix.DOMAIN/_synapse/metrics`
`matrix_nginx_proxy_proxy_synapse_metrics_basic_auth_enabled`|Set this to `true` to password-protect (using HTTP Basic Auth) `https://matrix.DOMAIN/_synapse/metrics` (the username is always `prometheus`, the password is defined in `matrix_nginx_proxy_proxy_synapse_metrics_basic_auth_key`)
`matrix_nginx_proxy_proxy_synapse_metrics_basic_auth_key`|Set this to a password to use for HTTP Basic Auth for protecting `https://matrix.DOMAIN/_synapse/metrics` (the username is always `prometheus` - it's not configurable). Do not write the password in plain text. See `man 1 htpasswd` or use `htpasswd -c mypass.htpasswd prometheus` to generate the expected hash for nginx. 
`matrix_server_fqn_grafana`|Use this variable to override the domain at which the Grafana web user-interface is at (defaults to `stats.DOMAIN`)

### Collecting worker metrics to an external Prometheus server

If you are using workers (`matrix_synapse_workers_enabled`) and have enabled `matrix_nginx_proxy_proxy_synapse_metrics` as described above, the playbook will also automatically proxy the all worker threads's metrics to `https://matrix.DOMAIN/_synapse-worker-TYPE-ID/metrics`, where `TYPE` corresponds to the type and `ID` to the instanceId of a worker as exemplified in `matrix_synapse_workers_enabled_list`.

The playbook also generates an exemplary prometheus.yml config file (`matrix_base_data_path/external_prometheus.yml.template`) with all the correct paths which you can copy to your Prometheus server and adapt to your needs, especially edit the specified `password_file` path and contents and path to your `synapse-v2.rules`.
It will look a bit like this:
```yaml
scrape_configs:
  - job_name: 'synapse'
    metrics_path: /_synapse/metrics
    scheme: https
    basic_auth:
      username: prometheus
      password_file: /etc/prometheus/password.pwd
    static_configs:
      - targets: ['matrix.DOMAIN:443']
        labels:
          job: "master"
          index: 1
  - job_name: 'synapse-generic_worker-1'
    metrics_path: /_synapse-worker-generic_worker-18111/metrics
    scheme: https
    basic_auth:
      username: prometheus
      password_file: /etc/prometheus/password.pwd
    static_configs:
      - targets: ['matrix.DOMAIN:443']
        labels:
          job: "generic_worker"
          index: 18111
```

### Collecting system and Postgres metrics to an external Prometheus server (advanced)

When you normally enable the Prometheus and Grafana via the playbook, it will also show general system (via node-exporter) and Postgres (via postgres-exporter) stats. If you are instead collecting your metrics to an external Prometheus server, you can follow this advanced configuration example to also export these stats.

It would be possible to use `matrix_prometheus_node_exporter_container_http_host_bind_port` etc., but that is not always the best choice, for example because your server is on a public network.

Use the following variables in addition to the ones mentioned above:

Name | Description
-----|----------
`matrix_nginx_proxy_proxy_grafana_enabled`|Set this to `true` to make the stats subdomain (`matrix_server_fqn_grafana`) available via the Nginx proxy
`matrix_ssl_additional_domains_to_obtain_certificates_for`|Add `"{{ matrix_server_fqn_grafana }}"` to this list to have letsencrypt fetch a certificate for the stats subdomain
`matrix_prometheus_node_exporter_enabled`|Set this to `true` to enable the node (general system stats) exporter
`matrix_prometheus_postgres_exporter_enabled`|Set this to `true` to enable the Postgres exporter
`matrix_nginx_proxy_proxy_grafana_additional_server_configuration_blocks`|Add locations to this list depending on which of the above exporters you enabled (see below)

```nginx
matrix_nginx_proxy_proxy_grafana_additional_server_configuration_blocks:
  - 'location /node-exporter/ {
  resolver 127.0.0.11 valid=5s;
  proxy_pass http://matrix-prometheus-node-exporter:9100/;
  auth_basic "protected";
  auth_basic_user_file /nginx-data/matrix-synapse-metrics-htpasswd;
  }'
  - 'location /postgres-exporter/ {
  resolver 127.0.0.11 valid=5s;
  proxy_pass http://matrix-prometheus-postgres-exporter:9187/;
  auth_basic "protected";
  auth_basic_user_file /nginx-data/matrix-synapse-metrics-htpasswd;
  }'
```
You can customize the `location`s to your liking, just point your Prometheus to there later (e.g. `stats.DOMAIN/node-exporter/metrics`). Nginx is very picky about the `proxy_pass`syntax: take care to follow the example closely and note the trailing slash as well as absent use of variables. postgres-exporter uses the nonstandard port 9187.

## More information

- [Understanding Synapse Performance Issues Through Grafana Graphs](https://github.com/matrix-org/synapse/wiki/Understanding-Synapse-Performance-Issues-Through-Grafana-Graphs) at the Synapse Github Wiki
- [The Prometheus scraping rules](https://github.com/matrix-org/synapse/tree/master/contrib/prometheus) (we use v2)
- [The Synapse Grafana dashboard](https://github.com/matrix-org/synapse/tree/master/contrib/grafana)
- [The Node Exporter dashboard](https://github.com/rfrail3/grafana-dashboards) (for generic non-synapse performance graphs)

