# Enabling metrics and graphs (Prometheus, Grafana) for your Matrix server (optional)

The playbook can install [Grafana](https://grafana.com/) with [Prometheus](https://prometheus.io/) and configure performance metrics of your homeserver with graphs for you.

## Adjusting DNS records

By default, this playbook installs Grafana web user-interface on the `stats.` subdomain (`stats.example.com`) and requires you to create a CNAME record for `stats`, which targets `matrix.example.com`.

When setting, replace `example.com` with your own.

## Adjusting the playbook configuration

To enable Grafana and/or Prometheus, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
prometheus_enabled: true

# You can remove this, if unnecessary.
prometheus_node_exporter_enabled: true

# You can remove this, if unnecessary.
prometheus_postgres_exporter_enabled: true

# You can remove this, if unnecessary.
matrix_prometheus_nginxlog_exporter_enabled: true

grafana_enabled: true

grafana_anonymous_access: false

# This has no relation to your Matrix user ID. It can be any username you'd like.
# Changing the username subsequently won't work.
grafana_default_admin_user: "some_username_chosen_by_you"

# Changing the password subsequently won't work.
grafana_default_admin_password: "some_strong_password_chosen_by_you"
```

The retention policy of Prometheus metrics is [15 days by default](https://prometheus.io/docs/prometheus/latest/storage/#operational-aspects). Older data gets deleted automatically.

### Adjusting the Grafana URL (optional)

By tweaking the `grafana_hostname` variable, you can easily make the service available at a **different hostname** than the default one.

Example additional configuration for your `vars.yml` file:

```yaml
# Change the default hostname
grafana_hostname: grafana.example.com
```

After changing the domain, **you may need to adjust your DNS** records to point the Grafana domain to the Matrix server.

**Note**: It is possible to install Prometheus without installing Grafana. This case it is not required to create the CNAME record.

## Installing

After configuring the playbook and potentially [adjusting your DNS records](#adjusting-dns-records), run the playbook with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

## What does it do?

Name | Description
-----|----------
`prometheus_enabled`|[Prometheus](https://prometheus.io) is a time series database. It holds all the data we're going to talk about.
`prometheus_node_exporter_enabled`|[Node Exporter](https://prometheus.io/docs/guides/node-exporter/) is an addon of sorts to Prometheus that collects generic system information such as CPU, memory, filesystem, and even system temperatures
`prometheus_postgres_exporter_enabled`|[Postgres Exporter](configuring-playbook-prometheus-postgres.md) is an addon of sorts to expose Postgres database metrics to Prometheus.
`matrix_prometheus_nginxlog_exporter_enabled`|[NGINX Log Exporter](configuring-playbook-prometheus-nginxlog.md) is an addon of sorts to expose NGINX logs to Prometheus.
`grafana_enabled`|[Grafana](https://grafana.com/) is the visual component. It shows (on the `stats.example.com` subdomain) the dashboards with the graphs that we're interested in
`grafana_anonymous_access`|By default you need to log in to see graphs. If you want to publicly share your graphs (e.g. when asking for help in [`#synapse:matrix.org`](https://matrix.to/#/#synapse:matrix.org?via=matrix.org&via=privacytools.io&via=mozilla.org)) you'll want to enable this option.
`grafana_default_admin_user`<br>`grafana_default_admin_password`|By default Grafana creates a user with `admin` as the username and password. If you feel this is insecure and you want to change it beforehand, you can do that here

## Security and privacy

Metrics and resulting graphs can contain a lot of information. This includes system specs but also usage patterns. This applies especially to small personal/family scale homeservers. Someone might be able to figure out when you wake up and go to sleep by looking at the graphs over time. Think about this before enabling anonymous access. And you should really not forget to change your Grafana password.

Most of our docker containers run with limited system access, but the `prometheus-node-exporter` has access to the host network stack and (readonly) root filesystem. This is required to report on them. If you don't like that, you can set `prometheus_node_exporter_enabled: false` (which is actually the default). You will still get Synapse metrics with this container disabled. Both of the dashboards will always be enabled, so you can still look at historical data after disabling either source.

## Collecting metrics to an external Prometheus server

**If the integrated Prometheus server is enabled** (`prometheus_enabled: true`), metrics are collected by it from each service via communication that happens over the container network. Each service does not need to expose its metrics "publicly".

When you'd like **to collect metrics from an external Prometheus server**, you need to expose service metrics outside of the container network.

The playbook provides a single endpoint (`https://matrix.example.com/metrics/*`), under which various services may expose their metrics (e.g. `/metrics/node-exporter`, `/metrics/postgres-exporter`, `/metrics/hookshot`, etc). To expose all services on this `/metrics/*` feature, use `matrix_metrics_exposure_enabled`. To protect access using [Basic Authentication](https://en.wikipedia.org/wiki/Basic_access_authentication), see `matrix_metrics_exposure_http_basic_auth_enabled` and `matrix_metrics_exposure_http_basic_auth_users` below.

When using `matrix_metrics_exposure_enabled`, you don't need to expose metrics for individual services one by one.

The following variables may be of interest:

Name | Description
-----|----------
`matrix_metrics_exposure_enabled`|Set this to `true` to **enable metrics exposure for all services** on `https://matrix.example.com/metrics/*`. If you think this is too much, refer to the helpful (but nonexhaustive) list of individual `matrix_SERVICE_metrics_proxying_enabled` (or similar) variables below for exposing metrics on a per-service basis.
`matrix_metrics_exposure_http_basic_auth_enabled`|Set this to `true` to protect all `https://matrix.example.com/metrics/*` endpoints with [Basic Authentication](https://en.wikipedia.org/wiki/Basic_access_authentication) (see the other variables below for supplying the actual credentials). When enabled, all endpoints beneath `/metrics` will be protected with the same credentials
`matrix_metrics_exposure_http_basic_auth_users`|Set this to the Basic Authentication credentials (raw `htpasswd` file content) used to protect `/metrics/*`. This htpasswd-file needs to be generated with the `htpasswd` tool and can include multiple username/password pairs.
`matrix_synapse_metrics_enabled`|Set this to `true` to make Synapse expose metrics (locally, on the container network)
`matrix_synapse_metrics_proxying_enabled`|Set this to `true` to expose Synapse's metrics on `https://matrix.example.com/metrics/synapse/main-process` and `https://matrix.example.com/metrics/synapse/worker/TYPE-ID`. Read [below](#collecting-synapse-worker-metrics-to-an-external-prometheus-server) if you're running a Synapse worker setup (`matrix_synapse_workers_enabled: true`). To password-protect the metrics, see `matrix_metrics_exposure_http_basic_auth_users` above.
`prometheus_node_exporter_enabled`|Set this to `true` to enable the node (general system stats) exporter (locally, on the container network)
`prometheus_node_exporter_container_labels_traefik_enabled`|Set this to `true` to expose the node (general system stats) metrics on `https://matrix.example.com/metrics/node-exporter`. To password-protect the metrics, see `matrix_metrics_exposure_http_basic_auth_users` above.
`prometheus_postgres_exporter_enabled`|Set this to `true` to enable the [Postgres exporter](configuring-playbook-prometheus-postgres.md) (locally, on the container network)
`prometheus_postgres_exporter_container_labels_traefik_enabled`|Set this to `true` to expose the [Postgres exporter](configuring-playbook-prometheus-postgres.md) metrics on `https://matrix.example.com/metrics/postgres-exporter`. To password-protect the metrics, see `matrix_metrics_exposure_http_basic_auth_users` above.
`matrix_prometheus_nginxlog_exporter_enabled`|Set this to `true` to enable the [NGINX Log exporter](configuring-playbook-prometheus-nginxlog.md) (locally, on the container network)
`matrix_sliding_sync_metrics_enabled`|Set this to `true` to make [Sliding Sync](configuring-playbook-sliding-sync-proxy.md) expose metrics (locally, on the container network)
`matrix_sliding_sync_metrics_proxying_enabled`|Set this to `true` to expose the [Sliding Sync](configuring-playbook-sliding-sync-proxy.md) metrics on `https://matrix.example.com/metrics/sliding-sync`. To password-protect the metrics, see `matrix_metrics_exposure_http_basic_auth_users` above.
`matrix_bridge_hookshot_metrics_enabled`|Set this to `true` to make [Hookshot](configuring-playbook-bridge-hookshot.md) expose metrics (locally, on the container network)
`matrix_bridge_hookshot_metrics_proxying_enabled`|Set this to `true` to expose the [Hookshot](configuring-playbook-bridge-hookshot.md) metrics on `https://matrix.example.com/metrics/hookshot`. To password-protect the metrics, see `matrix_metrics_exposure_http_basic_auth_users` above.
`matrix_SERVICE_metrics_proxying_enabled`|Various other services/roles may provide similar `_metrics_enabled` and `_metrics_proxying_enabled` variables for exposing their metrics. Refer to each role for details. To password-protect the metrics, see `matrix_metrics_exposure_http_basic_auth_users` above or `matrix_SERVICE_container_labels_metrics_middleware_basic_auth_enabled`/`matrix_SERVICE_container_labels_metrics_middleware_basic_auth_users` variables provided by each role.
`matrix_media_repo_metrics_enabled`|Set this to `true` to make media-repo expose metrics (locally, on the container network)

### Collecting Synapse worker metrics to an external Prometheus server

If you are using workers (`matrix_synapse_workers_enabled: true`) and have enabled `matrix_synapse_metrics_proxying_enabled` as described above, the playbook will also automatically expose all Synapse worker threads' metrics to `https://matrix.example.com/metrics/synapse/worker/ID`, where `ID` corresponds to the worker `id` as exemplified in `matrix_synapse_workers_enabled_list`.

The playbook also generates an exemplary config file (`/matrix/synapse/external_prometheus.yml.template`) with all the correct paths which you can copy to your Prometheus server and adapt to your needs. Make sure to edit the specified `password_file` path and contents and path to your `synapse-v2.rules`. It will look a bit like this:

```yaml
scrape_configs:
  - job_name: 'synapse'
    metrics_path: /metrics/synapse/main-process
    scheme: https
    basic_auth:
      username: prometheus
      password_file: /etc/prometheus/password.pwd
    static_configs:
      - targets: ['matrix.example.com:443']
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
      - targets: ['matrix.example.com:443']
        labels:
          job: "generic_worker"
          index: 18111
```

## More information

- [Enabling synapse-usage-exporter for Synapse usage statistics](configuring-playbook-synapse-usage-exporter.md)
- [Understanding Synapse Performance Issues Through Grafana Graphs](https://element-hq.github.io/synapse/latest/usage/administration/understanding_synapse_through_grafana_graphs.html) at the Synapse Github Wiki
- [The Prometheus scraping rules](https://github.com/element-hq/synapse/tree/master/contrib/prometheus) (we use v2)
- [The Synapse Grafana dashboard](https://github.com/element-hq/synapse/tree/master/contrib/grafana)
- [The Node Exporter dashboard](https://github.com/rfrail3/grafana-dashboards) (for generic non-synapse performance graphs)
