<!--
SPDX-FileCopyrightText: 2020 - 2022 MDAD project contributors
SPDX-FileCopyrightText: 2020 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2020 Aaron Raimist
SPDX-FileCopyrightText: 2023 Pierre 'McFly' Marty
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Configuring Element Web (optional)

By default, this playbook installs the [Element Web](https://github.com/element-hq/element-web) Matrix client for you. If that's okay, you can skip this document.

If you'd like to stop the playbook installing the client, see the section [below](#disabling-element-web) to check the configuration for disabling it.

💡 **Note**: the latest version of Element Web is also available on the web, hosted by 3rd parties. If you trust giving your credentials to the following 3rd party Single Page Applications, you can consider using it from there and avoiding the (small) overhead of self-hosting (by [disabling Element Web](#disabling-element-web)):

- [app.element.io](https://app.element.io/), hosted by [Element](https://element.io/)
- [app.etke.cc](https://app.etke.cc/), hosted by [etke.cc](https://etke.cc/)

## Adjusting DNS records

By default, this playbook installs Element Web on the `element.` subdomain (`element.example.com`) and requires you to create a CNAME record for `element`, which targets `matrix.example.com`.

When setting, replace `example.com` with your own.

## Adjusting the playbook configuration

### Set the country code for phone number inputs

You can change the country code (default: `GB`) to use when showing phone number inputs. To change it to `FR` for example, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_client_element_default_country_code: "FR"
```

### Themes

#### Change the default theme

You can change the default theme from `light` to `dark`. To do so, add the following configuration to your `vars.yml` file:

```yaml
# Controls the default theme
matrix_client_element_default_theme: 'dark'
```

#### Use themes by `element-themes`

You can change the look of Element Web by pulling themes provided by the [aaronraimist/element-themes](https://github.com/aaronraimist/element-themes) project or defining your own themes manually.

To pull the themes and use them for your Element Web instance, add the following configuration to your `vars.yml` file:

```yaml
matrix_client_element_themes_enabled: true
```

If the variable is set to `true`, all themes found in the repository specified with `matrix_client_element_themes_repository_url` will be installed and enabled automatically.

Note that for a custom theme to work well, all Element Web instances that you use must have the same theme installed.

#### Define themes manually

You can also define your own themes manually by adding and adjusting the following configuration to your `vars.yml` file:

```yaml
# Controls the `setting_defaults.custom_themes` setting of the Element Web configuration.
matrix_client_element_setting_defaults_custom_themes: []
```

If you define your own themes with it and set `matrix_client_element_themes_enabled` to `true` for the themes by `element-themes`, your themes will be preserved as well.

If you make your own theme, we encourage you to submit it to the **aaronraimist/element-themes** project, so that the whole community could easily enjoy it.

### Adjusting the Element Web URL (optional)

By tweaking the `matrix_client_element_hostname` and `matrix_client_element_path_prefix` variables, you can easily make the service available at a **different hostname and/or path** than the default one.

Example additional configuration for your `vars.yml` file:

```yaml
# Switch to the domain used for Matrix services (`matrix.example.com`),
# so we won't need to add additional DNS records for Element Web.
matrix_client_element_hostname: "{{ matrix_server_fqn_matrix }}"

# Expose under the /element subpath
matrix_client_element_path_prefix: /element
```

After changing the domain, **you may need to adjust your DNS** records to point the Element domain to the Matrix server.

If you've decided to reuse the `matrix.` domain, you won't need to do any extra DNS configuration.

### Extending the configuration

There are some additional things you may wish to configure about the component.

Take a look at:

- `roles/custom/matrix-client-element/defaults/main.yml` for some variables that you can customize via your `vars.yml` file
- `roles/custom/matrix-client-element/templates/config.json.j2` for the component's default configuration. You can override settings (even those that don't have dedicated playbook variables) using the `matrix_client_element_configuration_extension_json` variable

For example, to override some Element Web settings, add the following configuration to your `vars.yml` file:

```yaml
 # Your custom JSON configuration for Element Web should go to `matrix_client_element_configuration_extension_json`.
 # This configuration extends the default starting configuration (`matrix_client_element_configuration_default`).
 #
 # You can override individual variables from the default configuration, or introduce new ones.
 #
 # If you need something more special, you can take full control by
 # completely redefining `matrix_client_element_configuration_default`.
 #
matrix_client_element_configuration_extension_json: |
 {
 "disable_3pid_login": true,
 "disable_login_language_selector": true
 }
```

## Disabling Element Web

If you'd like for the playbook to not install Element Web (or to uninstall it if it was previously installed), add the following configuration to your `vars.yml` file:

```yaml
matrix_client_element_enabled: false
```

## Installing

After configuring the playbook and potentially [adjusting your DNS records](#adjusting-dns-records), run the playbook with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-client-element`.
