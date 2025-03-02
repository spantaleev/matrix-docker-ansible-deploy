<!--
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara
SPDX-FileCopyrightText: 2024 Michael Hollister
SPDX-FileCopyrightText: 2024 Slavi Pantaleev

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Enabling synapse-usage-exporter for Synapse usage statistics (optional)

The playbook can install and configure [synapse-usage-exporter](https://github.com/loelkes/synapse-usage-exporter) for you.

It allows you to export the usage statistics of a Synapse homeserver to this container service and for the collected metrics to later be scraped by Prometheus.

Synapse does not include usage statistics in its Prometheus metrics. They can be reported to an HTTP `PUT` endpoint 5 minutes after startup and from then on at a fixed interval of once every three hours. This role integrates a simple [Flask](https://flask.palletsprojects.com) project that offers an HTTP `PUT` endpoint and holds the most recent received record available to be scraped by Prometheus.

See the project's [documentation](https://github.com/loelkes/synapse-usage-exporter/blob/main/README.md) to learn what it does and why it might be useful to you.

## What does it do?

Enabling this service will automatically:

- install the synapse-usage-exporter service
- re-configure Synapse to push (via HTTP `PUT`) usage statistics information to synapse-usage-exporter
- re-configure [Prometheus](./configuring-playbook-prometheus-grafana.md) (if Prometheus is enabled), to periodically scrape metrics from synapse-usage-exporter
- add a new [Grafana](./configuring-playbook-prometheus-grafana.md) dashboard (if Grafana is enabled) containing Synapse usage statistics

## Adjusting DNS records (optional)

By default, this playbook installs synapse-usage-exporter on the `matrix.` subdomain, at the `/report-usage-stats/push` path (https://matrix.example.com/report-usage-stats/push). This makes it easy to install it, because it **doesn't require additional DNS records to be set up**. If that's okay, you can skip this section.

If you wish to adjust it, see the section [below](#adjusting-the-synapse-usage-exporter-url-optional) for details about DNS configuration.

## Adjusting the playbook configuration

To enable synapse-usage-exporter, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_synapse_usage_exporter_enabled: true

# (Optional) Expose endpoint if you want to collect statistics from outside (from other homeservers).
# If enabled, synapse-usage-exporter will be exposed publicly at `matrix.example.com/report-usage-stats/push`.
# When collecting usage statistics for Synapse running on the same host, you don't need to enable this.
# You can adjust the hostname and path via `matrix_synapse_usage_exporter_hostname` and `matrix_synapse_usage_exporter_path_prefix`.
# matrix_synapse_usage_exporter_proxying_enabled: true
```

### Adjusting the synapse-usage-exporter URL (optional)

By tweaking the `matrix_synapse_usage_exporter_hostname` and `matrix_synapse_usage_exporter_path_prefix` variables, you can easily make the service available at a **different hostname and/or path** than the default one.

Example additional configuration for your `vars.yml` file:

```yaml
# Change the default hostname and path prefix
# These variables are used only if (`matrix_synapse_usage_exporter_proxying_enabled: true`)
matrix_synapse_usage_exporter_hostname: sue.example.com
matrix_synapse_usage_exporter_path_prefix: /
```

If you've changed the default hostname, you may need to create a CNAME record for the synapse-usage-exporter domain (`sue.example.com`), which targets `matrix.example.com`.

When setting, replace `example.com` with your own.

### Extending the configuration

There are some additional things you may wish to configure about the component.

Take a look at:

- `roles/custom/matrix-synapse-usage-exporter/defaults/main.yml` for some variables that you can customize via your `vars.yml` file

## Installing

After configuring the playbook and potentially [adjusting your DNS records](#adjusting-dns-records), run the playbook with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-synapse-usage-exporter`.
