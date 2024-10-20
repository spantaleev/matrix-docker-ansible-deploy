# Configuring Element (optional)

By default, this playbook installs the [Element](https://github.com/element-hq/element-web) Matrix web client for you. If that's okay, you can skip this document.


## Disabling Element

If you'd like for the playbook to not install Element (or to uninstall it if it was previously installed), add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_client_element_enabled: false
```


## Adjusting the playbook configuration

The playbook provides some customization variables you could use to change Element's settings.

Their defaults are defined in [`roles/custom/matrix-client-element/defaults/main.yml`](../roles/custom/matrix-client-element/defaults/main.yml) and they ultimately end up in the generated `/matrix/element/config.json` file (on the server). This file is generated from the [`roles/custom/matrix-client-element/templates/config.json.j2`](../roles/custom/matrix-client-element/templates/config.json.j2) template.

**If there's an existing variable** which controls a setting you wish to change, you can simply define that variable in your configuration file (`inventory/host_vars/matrix.example.com/vars.yml`) and [re-run the playbook](installing.md) to apply the changes.

Alternatively, **if there is no pre-defined variable** for an Element setting you wish to change:

- you can either **request a variable to be created** (or you can submit such a contribution yourself). Keep in mind that it's **probably not a good idea** to create variables for each one of Element's various settings that rarely get used.

- or, you can **extend and override the default configuration** ([`config.json.j2`](../roles/custom/matrix-client-element/templates/config.json.j2)) by making use of the `matrix_client_element_configuration_extension_json_` variable. You can find information about this in [`roles/custom/matrix-client-element/defaults/main.yml`](../roles/custom/matrix-client-element/defaults/main.yml).

- or, if extending the configuration is still not powerful enough for your needs, you can **override the configuration completely** using `matrix_client_element_configuration_default` (or `matrix_client_element_configuration`). You can find information about this in [`roles/custom/matrix-client-element/defaults/main.yml`](../roles/custom/matrix-client-element/defaults/main.yml).


### Themes

To change the look of Element, you can define your own themes manually by using the `matrix_client_element_setting_defaults_custom_themes` setting.

Or better yet, you can automatically pull it all themes provided by the [aaronraimist/element-themes](https://github.com/aaronraimist/element-themes) project by simply flipping a flag (`matrix_client_element_themes_enabled: true`).

If you make your own theme, we encourage you to submit it to the **aaronraimist/element-themes** project, so that the whole community could easily enjoy it.

Note that for a custom theme to work well, all Element instances that you use must have the same theme installed.

### Adjusting the Element URL

By default, this playbook installs Element on the `element.` subdomain (`element.example.com`) and requires you to [adjust your DNS records](#adjusting-dns-records).

By tweaking the `matrix_client_element_hostname` and `matrix_client_element_path_prefix` variables, you can easily make the service available at a **different hostname and/or path** than the default one.

Example additional configuration for your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
# Switch to the domain used for Matrix services (`matrix.example.com`),
# so we won't need to add additional DNS records for Element.
matrix_client_element_hostname: "{{ matrix_server_fqn_matrix }}"

# Expose under the /element subpath
matrix_client_element_path_prefix: /element
```

## Adjusting DNS records

Once you've decided on the domain and path, **you may need to adjust your DNS** records to point the Element domain to the Matrix server.

By default, you will need to create a CNAME record for `element`. See [Configuring DNS](configuring-dns.md) for details about DNS changes.

If you've decided to reuse the `matrix.` domain, you won't need to do any extra DNS configuration.

## Installing

After configuring the playbook, run the [installation](installing.md) command: `just install-all` or `just setup-all`
