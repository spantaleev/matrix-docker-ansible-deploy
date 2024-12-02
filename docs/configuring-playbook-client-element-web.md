# Configuring Element Web (optional)

By default, this playbook installs the [Element Web](https://github.com/element-hq/element-web) Matrix client for you. If that's okay, you can skip this document.

💡 **Note**: the latest version of Element Web is also available on the web, hosted by 3rd parties. If you trust giving your credentials to the following 3rd party Single Page Applications, you can consider using it from there and avoiding the (small) overhead of self-hosting (by [disabling Element Web](#disabling-element-web)):

- [app.element.io](https://app.element.io/), hosted by [Element](https://element.io/)
- [app.etke.cc](https://app.etke.cc/), hosted by [etke.cc](https://etke.cc/)

## Disabling Element Web

If you'd like for the playbook to not install Element Web (or to uninstall it if it was previously installed), add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_client_element_enabled: false
```

## Adjusting the playbook configuration

The playbook provides some customization variables you could use to change Element Web's settings.

Their defaults are defined in [`roles/custom/matrix-client-element/defaults/main.yml`](../roles/custom/matrix-client-element/defaults/main.yml) and they ultimately end up in the generated `/matrix/element/config.json` file (on the server). This file is generated from the [`roles/custom/matrix-client-element/templates/config.json.j2`](../roles/custom/matrix-client-element/templates/config.json.j2) template.

**If there's an existing variable** which controls a setting you wish to change, you can simply define that variable in your configuration file (`inventory/host_vars/matrix.example.com/vars.yml`) and [re-run the playbook](installing.md) to apply the changes.

Alternatively, **if there is no pre-defined variable** for an Element Web setting you wish to change:

- you can either **request a variable to be created** (or you can submit such a contribution yourself). Keep in mind that it's **probably not a good idea** to create variables for each one of Element Web's various settings that rarely get used.

- or, you can **extend and override the default configuration** ([`config.json.j2`](../roles/custom/matrix-client-element/templates/config.json.j2)) by making use of the `matrix_client_element_configuration_extension_json_` variable. You can find information about this in [`roles/custom/matrix-client-element/defaults/main.yml`](../roles/custom/matrix-client-element/defaults/main.yml).

- or, if extending the configuration is still not powerful enough for your needs, you can **override the configuration completely** using `matrix_client_element_configuration_default` (or `matrix_client_element_configuration`). You can find information about this in [`roles/custom/matrix-client-element/defaults/main.yml`](../roles/custom/matrix-client-element/defaults/main.yml).

### Themes

To change the look of Element Web, you can define your own themes manually by using the `matrix_client_element_setting_defaults_custom_themes` setting.

Or better yet, you can automatically pull it all themes provided by the [aaronraimist/element-themes](https://github.com/aaronraimist/element-themes) project by simply flipping a flag (`matrix_client_element_themes_enabled: true`).

If you make your own theme, we encourage you to submit it to the **aaronraimist/element-themes** project, so that the whole community could easily enjoy it.

Note that for a custom theme to work well, all Element Web instances that you use must have the same theme installed.

### Adjusting the Element Web URL

By default, this playbook installs Element Web on the `element.` subdomain (`element.example.com`) and requires you to [adjust your DNS records](#adjusting-dns-records).

By tweaking the `matrix_client_element_hostname` and `matrix_client_element_path_prefix` variables, you can easily make the service available at a **different hostname and/or path** than the default one.

Example additional configuration for your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
# Switch to the domain used for Matrix services (`matrix.example.com`),
# so we won't need to add additional DNS records for Element Web.
matrix_client_element_hostname: "{{ matrix_server_fqn_matrix }}"

# Expose under the /element subpath
matrix_client_element_path_prefix: /element
```

## Adjusting DNS records

Once you've decided on the domain and path, **you may need to adjust your DNS** records to point the Element Web domain to the Matrix server.

By default, you will need to create a CNAME record for `element`. See [Configuring DNS](configuring-dns.md) for details about DNS changes.

If you've decided to reuse the `matrix.` domain, you won't need to do any extra DNS configuration.

## Installing

After configuring the playbook and potentially [adjusting your DNS records](#adjusting-dns-records), run the playbook with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.
