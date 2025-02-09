<!--
SPDX-FileCopyrightText: 2022 ikkemaniac
SPDX-FileCopyrightText: 2023 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Enabling metrics and graphs for nginx logs (optional)

## Prerequisite

To make use of this, you need to install [Prometheus](./configuring-playbook-prometheus-grafana.md) either via the playbook or externally. When using an external Prometheus, configuration adjustments are necessary — see [Save metrics on an external Prometheus server](#save-metrics-on-an-external-prometheus-server).

## Adjusting the playbook configuration

### Save metrics on an external Prometheus server (optional)

> [!WARNING]
> Metrics and resulting graphs can contain a lot of information. nginx logs contain information like IP address, URLs, UserAgents and more. This information can reveal usage patterns and could be considered Personally Identifiable Information (PII). Think about this before enabling (anonymous) access. And you should really not forget to change your Grafana password.

The playbook will automatically integrate the metrics into the [Prometheus](./configuring-playbook-prometheus-grafana.md) server provided with this playbook (if enabled). In such cases, the metrics endpoint is not exposed publicly — it's only available on the container network.

When using an external Prometheus server, you'll need to expose metrics publicly. See [Collecting metrics to an external Prometheus server](./configuring-playbook-prometheus-grafana.md#collecting-metrics-to-an-external-prometheus-server).

For password-protection, use or (`matrix_prometheus_nginxlog_exporter_container_labels_metrics_middleware_basic_auth_enabled` and `matrix_prometheus_nginxlog_exporter_container_labels_metrics_middleware_basic_auth_users`).

### Docker Image Compatibility (optional)

At the moment of writing only images for `amd64` and `arm64` architectures are available. The playbook currently does not support [self-building](./self-building.md) a container image on other architectures. You can however use a custom-build image by setting:

```yaml
matrix_prometheus_nginxlog_exporter_docker_image_arch_check_enabled: false
matrix_prometheus_nginxlog_exporter_docker_image: path/to/docker/image:tag
```

### Extending the configuration

There are some additional things you may wish to configure about the component.

Take a look at:

- `roles/custom/matrix-prometheus-nginxlog-exporter/defaults/main.yml` for some variables that you can customize via your `vars.yml` file

## Installing

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-prometheus-nginxlog-exporter`.
