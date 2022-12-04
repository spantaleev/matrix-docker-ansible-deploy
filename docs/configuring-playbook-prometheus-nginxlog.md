# Enabling metrics and graphs for NginX logs (optional)

It can be useful to have some (visual) insight into NignX logs.

This adds [prometheus-nginxlog-exporter](https://github.com/martin-helmich/prometheus-nginxlog-exporter/) to your matrix deployment.
It will provide a prometheus 'metrics' endpoint exposing data from both the `matrix-nginx-proxy` and `matrix-synapse-reverse-proxy-companion` logs and automatically aggregrates the data with prometheus.
Optionally it visualizes the data when [`matrix-grafana`](configuring-playbook-prometheus-grafana.md) is enabled by means of a dedicated dashboard named `NGINX PROXY`

You can enable this role by adding the following setting in your configuration file (`inventory/host_vars/matrix.<your-domain>/vars.yml`):

```yaml
matrix_prometheus_nginxlog_exporter_enabled: true

# required depency
matrix_prometheus_enabled: true

# optional for visualization
matrix_grafana_enabled: true
```

x | Prerequisites | var | Description
|:--:|:--:|:--:|:--|
**REQUIRED** | `matrix-prometheus`| `matrix_prometheus_enabled`|[Prometheus](https://prometheus.io) is a time series database. It holds all the data we're going to talk about.
Optional | [`matrix-grafana`](configuring-playbook-prometheus-grafana.md) | [`matrix_grafana_enabled`](configuring-playbook-prometheus-grafana.md)|[Grafana](https://grafana.com) is the visual component. It shows (on the `stats.<your-domain>` subdomain) the dashboards with the graphs that we're interested in. When enabled the `NGINX PROXY` dashboard is automatically added.

## Docker Image Compatibility

At the moment of writing only images for `amd64` and `arm64` architectures are available

The playbook currently does not support building an image.
You can however use a custom-build image by setting
```yaml
matrix_prometheus_nginxlog_exporter_docker_image_arch_check_enabled: false
matrix_prometheus_nginxlog_exporter_docker_image: path/to/docker/image:tag
```


## Security and privacy

Metrics and resulting graphs can contain a lot of information. NginX logs contain information about visitor IP address, URLs, UserAgents and more. This information can reveal usage patterns and could be considered Personally Identifiable Information (PII). Think about this before enabling (anonymous) access. And you should really not forget to change your Grafana password.


## Collecting metrics to an external Prometheus server

The playbook will automatically integrate the metrics into the Prometheus server provided with this playbook.

The playbook provides a single endpoint (`https://matrix.DOMAIN/metrics/*`), under which various services may expose their metrics (e.g. `/metrics/node-exporter`, `/metrics/postgres-exporter`, `/metrics/nginxlog`, etc). To enable this `/metrics/*` feature, use `matrix_nginx_proxy_proxy_matrix_metrics_enabled`. To protect access using [Basic Authentication](https://en.wikipedia.org/wiki/Basic_access_authentication), see `matrix_nginx_proxy_proxy_matrix_metrics_basic_auth_enabled`.

The metrics of this role will be exposed on `https://matrix.DOMAIN/metrics/nginxlog` when setting
```yaml
matrix_prometheus_nginxlog_exporter_metrics_proxying_enabled: true

# required dependency
matrix_nginx_proxy_proxy_matrix_metrics_enabled: true
```

The following variables may be of interest:

Name | Description
-----|----------
`matrix_nginx_proxy_proxy_matrix_metrics_enabled`|Set this to `true` to enable metrics exposure for various services on `https://matrix.DOMAIN/metrics/*`. Refer to the individual `matrix_SERVICE_metrics_proxying_enabled` variables below for exposing metrics for each individual service.