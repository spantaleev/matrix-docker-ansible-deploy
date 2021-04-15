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
`matrix_nginx_proxy_proxy_synapse_metrics_basic_auth_key`|Set this to a password to use for HTTP Basic Auth for protecting `https://matrix.DOMAIN/_synapse/metrics` (the username is always `prometheus` - it's not configurable)


## More information

- [Understanding Synapse Performance Issues Through Grafana Graphs](https://github.com/matrix-org/synapse/wiki/Understanding-Synapse-Performance-Issues-Through-Grafana-Graphs) at the Synapse Github Wiki
- [The Prometheus scraping rules](https://github.com/matrix-org/synapse/tree/master/contrib/prometheus) (we use v2)
- [The Synapse Grafana dashboard](https://github.com/matrix-org/synapse/tree/master/contrib/grafana)
- [The Node Exporter dashboard](https://github.com/rfrail3/grafana-dashboards) (for generic non-synapse performance graphs)

