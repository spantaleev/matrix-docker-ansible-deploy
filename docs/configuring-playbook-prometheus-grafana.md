# Enabling metrics and graphs for your Matrix server (optional)

It can be useful to have some (visual) insight into the performance of your homeserver.

You can enable this with the following settings in your configuration file (`inventory/host_vars/matrix.<your-domain>/vars.yml`):

Remember to add `stats.<your-domain>` to DNS as described in [Configuring DNS](configuring-dns.md) before running the playbook.

```yaml
matrix_prometheus_enabled: true

# You can remove this, if unnecessary.
matrix_prometheus_node_exporter_enabled: true

# You can remove this, if unnecessary.
matrix_prometheus_postgres_exporter_enabled: true

# You can remove this, if unnecessary.
matrix_prometheus_nginxlog_exporter_enabled: true

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
`matrix_prometheus_postgres_exporter_enabled`|[Postgres Exporter](configuring-playbook-prometheus-postgres.md) is an addon of sorts to expose Postgres database metrics to Prometheus.
`matrix_prometheus_nginxlog_exporter_enabled`|[NGINX Log Exporter](configuring-playbook-prometheus-nginxlog.md) is an addon of sorts to expose NGINX logs to Prometheus.
`matrix_grafana_enabled`|[Grafana](https://grafana.com/) is the visual component. It shows (on the `stats.<your-domain>` subdomain) the dashboards with the graphs that we're interested in
`matrix_grafana_anonymous_access`|By default you need to log in to see graphs. If you want to publicly share your graphs (e.g. when asking for help in [`#synapse:matrix.org`](https://matrix.to/#/#synapse:matrix.org?via=matrix.org&via=privacytools.io&via=mozilla.org)) you'll want to enable this option.
`matrix_grafana_default_admin_user`<br>`matrix_grafana_default_admin_password`|By default Grafana creates a user with `admin` as the username and password. If you feel this is insecure and you want to change it beforehand, you can do that here


## Security and privacy

Metrics and resulting graphs can contain a lot of information. This includes system specs but also usage patterns. This applies especially to small personal/family scale homeservers. Someone might be able to figure out when you wake up and go to sleep by looking at the graphs over time. Think about this before enabling anonymous access. And you should really not forget to change your Grafana password.

Most of our docker containers run with limited system access, but the `prometheus-node-exporter` has access to the host network stack and (readonly) root filesystem. This is required to report on them. If you don't like that, you can set `matrix_prometheus_node_exporter_enabled: false` (which is actually the default). You will still get Synapse metrics with this container disabled. Both of the dashboards will always be enabled, so you can still look at historical data after disabling either source.


## Collecting metrics to an external Prometheus server

**If the integrated Prometheus server is enabled** (`matrix_prometheus_enabled: true`), metrics are collected by it from each service via communication that happens over the container network. Each service does not need to expose its metrics "publicly".

When you'd like **to collect metrics from an external Prometheus server**, you need to expose service metrics outside of the container network.

The playbook provides a single endpoint (`https://matrix.DOMAIN/metrics/*`), under which various services may expose their metrics (e.g. `/metrics/node-exporter`, `/metrics/postgres-exporter`, `/metrics/hookshot`, etc). To enable this `/metrics/*` feature, use `matrix_nginx_proxy_proxy_matrix_metrics_enabled`. To protect access using [Basic Authentication](https://en.wikipedia.org/wiki/Basic_access_authentication), see `matrix_nginx_proxy_proxy_matrix_metrics_basic_auth_enabled` below.

The following variables may be of interest:

Name | Description
-----|----------
`matrix_nginx_proxy_proxy_matrix_metrics_enabled`|Set this to `true` to enable metrics exposure for various services on `https://matrix.DOMAIN/metrics/*`. Refer to the individual `matrix_SERVICE_metrics_proxying_enabled` variables below for exposing metrics for each individual service.
`matrix_nginx_proxy_proxy_matrix_metrics_basic_auth_enabled`|Set this to `true` to protect all `https://matrix.DOMAIN/metrics/*` endpoints with [Basic Authentication](https://en.wikipedia.org/wiki/Basic_access_authentication) (see the other variables below for supplying the actual credentials). When enabled, all endpoints beneath `/metrics` will be protected with the same credentials
`matrix_nginx_proxy_proxy_matrix_metrics_basic_auth_username`|Set this to the Basic Authentication username you'd like to protect `/metrics/*` with. You also need to set `matrix_nginx_proxy_proxy_matrix_metrics_basic_auth_password`. If one username/password pair is not enough, you can leave the `username` and `password` variables unset and use `matrix_nginx_proxy_proxy_matrix_metrics_basic_auth_raw_content` instead
`matrix_nginx_proxy_proxy_matrix_metrics_basic_auth_password`|Set this to the Basic Authentication password you'd like to protect `/metrics/*` with
`matrix_nginx_proxy_proxy_matrix_metrics_basic_auth_raw_content`|Set this to the Basic Authentication credentials (raw `htpasswd` file content) used to protect `/metrics/*`. This htpasswd-file needs to be generated with the `htpasswd` tool and can include multiple username/password pairs. If you only need one credential, use `matrix_nginx_proxy_proxy_matrix_metrics_basic_auth_username` and `matrix_nginx_proxy_proxy_matrix_metrics_basic_auth_password` instead.
`matrix_synapse_metrics_enabled`|Set this to `true` to make Synapse expose metrics (locally, on the container network)
`matrix_synapse_metrics_proxying_enabled`|Set this to `true` to expose Synapse's metrics on `https://matrix.DOMAIN/metrics/synapse/main-process` and `https://matrix.DOMAIN/metrics/synapse/worker/TYPE-ID` (only takes effect if `matrix_nginx_proxy_proxy_matrix_metrics_enabled: true`). Read [below](#collecting-synapse-worker-metrics-to-an-external-prometheus-server) if you're running a Synapse worker setup (`matrix_synapse_workers_enabled: true`).
`matrix_prometheus_node_exporter_enabled`|Set this to `true` to enable the node (general system stats) exporter (locally, on the container network)
`matrix_prometheus_node_exporter_metrics_proxying_enabled`|Set this to `true` to expose the node (general system stats) metrics on `https://matrix.DOMAIN/metrics/node-exporter` (only takes effect if `matrix_nginx_proxy_proxy_matrix_metrics_enabled: true`)
`matrix_prometheus_postgres_exporter_enabled`|Set this to `true` to enable the [Postgres exporter](configuring-playbook-prometheus-postgres.md) (locally, on the container network)
`matrix_prometheus_nginxlog_exporter_enabled`|Set this to `true` to enable the [NGINX Log exporter](configuring-playbook-prometheus-nginxlog.md) (locally, on the container network)
`matrix_prometheus_postgres_exporter_metrics_proxying_enabled`|Set this to `true` to expose the [Postgres exporter](configuring-playbook-prometheus-postgres.md) metrics on `https://matrix.DOMAIN/metrics/postgres-exporter` (only takes effect if `matrix_nginx_proxy_proxy_matrix_metrics_enabled: true`)
`matrix_bridge_hookshot_metrics_enabled`|Set this to `true` to make [Hookshot](configuring-playbook-bridge-hookshot.md) expose metrics (locally, on the container network)
`matrix_bridge_hookshot_metrics_proxying_enabled`|Set this to `true` to expose the [Hookshot](configuring-playbook-bridge-hookshot.md) metrics on `https://matrix.DOMAIN/metrics/hookshot` (only takes effect if `matrix_nginx_proxy_proxy_matrix_metrics_enabled: true`)
`matrix_SERVICE_metrics_proxying_enabled`|Various other services/roles may provide similar `_metrics_enabled` and `_metrics_proxying_enabled` variables for exposing their metrics. Refer to each role for details. Only takes effect if `matrix_nginx_proxy_proxy_matrix_metrics_enabled: true`
`matrix_nginx_proxy_proxy_matrix_metrics_additional_user_location_configuration_blocks`|Add nginx `location` blocks to this list if you'd like to expose additional exporters manually (see below)

Example for how to make use of `matrix_nginx_proxy_proxy_matrix_metrics_additional_user_location_configuration_blocks` for exposing additional metrics locations:
```nginx
matrix_nginx_proxy_proxy_matrix_metrics_additional_user_location_configuration_blocks:
  - 'location /metrics/another-service {
  resolver 127.0.0.11 valid=5s;
  proxy_pass http://matrix-another-service:9100/metrics;
  }'
```

Using `matrix_nginx_proxy_proxy_matrix_metrics_additional_user_location_configuration_blocks` only takes effect if `matrix_nginx_proxy_proxy_matrix_metrics_enabled: true` (see above).

Note : The playbook will hash the basic_auth password for you on setup. Thus, you need to give the plain-text version of the password as a variable.

### Collecting Synapse worker metrics to an external Prometheus server

If you are using workers (`matrix_synapse_workers_enabled: true`) and have enabled `matrix_synapse_metrics_proxying_enabled` as described above, the playbook will also automatically expose all Synapse worker threads' metrics to `https://matrix.DOMAIN/metrics/synapse/worker/ID`, where `ID` corresponds to the worker `id` as exemplified in `matrix_synapse_workers_enabled_list`.

The playbook also generates an exemplary config file (`/matrix/synapse/external_prometheus.yml.template`) with all the correct paths which you can copy to your Prometheus server and adapt to your needs. Make sure to edit the specified `password_file` path and contents and path to your `synapse-v2.rules`.
It will look a bit like this:
```yaml
scrape_configs:
  - job_name: 'synapse'
    metrics_path: /metrics/synapse/main-process
    scheme: https
    basic_auth:
      username: prometheus
      password_file: /etc/prometheus/password.pwd
    static_configs:
      - targets: ['matrix.DOMAIN:443']
        labels:
          job: "master"
          index: 1
  - job_name: 'matrix-synapse-synapse-worker-generic-worker-0'
    metrics_path: /metrics/synapse/worker/generic-worker-0
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


## More information

- [Understanding Synapse Performance Issues Through Grafana Graphs](https://github.com/matrix-org/synapse/wiki/Understanding-Synapse-Performance-Issues-Through-Grafana-Graphs) at the Synapse Github Wiki
- [The Prometheus scraping rules](https://github.com/matrix-org/synapse/tree/master/contrib/prometheus) (we use v2)
- [The Synapse Grafana dashboard](https://github.com/matrix-org/synapse/tree/master/contrib/grafana)
- [The Node Exporter dashboard](https://github.com/rfrail3/grafana-dashboards) (for generic non-synapse performance graphs)
