# Configuring Element (optional)

By default, this playbook installs the [Element](https://github.com/vector-im/element-web) Matrix client web application.
If that's okay, you can skip this document.


## Disabling Element

If you'd like for the playbook to not install Element (or to uninstall it if it was previously installed), you can disable it in your configuration file (`inventory/host_vars/matrix.<your-domain>/vars.yml`):

```yaml
matrix_client_element_enabled: false
```


## Configuring Element settings

The playbook provides some customization variables you could use to change Element's settings.

Their defaults are defined in [`roles/matrix-client-element/defaults/main.yml`](../roles/matrix-client-element/defaults/main.yml) and they ultimately end up in the generated `/matrix/element/config.json` file (on the server). This file is generated from the [`roles/matrix-client-element/templates/config.json.j2`](../roles/matrix-client-element/templates/config.json.j2) template.

**If there's an existing variable** which controls a setting you wish to change, you can simply define that variable in your configuration file (`inventory/host_vars/matrix.<your-domain>/vars.yml`) and [re-run the playbook](installing.md) to apply the changes.

Alternatively, **if there is no pre-defined variable** for an Element setting you wish to change:

- you can either **request a variable to be created** (or you can submit such a contribution yourself). Keep in mind that it's **probably not a good idea** to create variables for each one of Element's various settings that rarely get used.

- or, you can **extend and override the default configuration** ([`config.json.j2`](../roles/matrix-client-element/templates/config.json.j2)) by making use of the `matrix_client_element_configuration_extension_json_` variable. You can find information about this in [`roles/matrix-client-element/defaults/main.yml`](../roles/matrix-client-element/defaults/main.yml).

- or, if extending the configuration is still not powerful enough for your needs, you can **override the configuration completely** using `matrix_client_element_configuration_default` (or `matrix_client_element_configuration`). You can find information about this in [`roles/matrix-client-element/defaults/main.yml`](../roles/matrix-client-element/defaults/main.yml).


## Themes

To change the look of Element, you can define your own themes manually by using the `matrix_client_element_settingDefaults_custom_themes` setting.

Or better yet, you can automatically pull it all themes provided by the [aaronraimist/element-themes](https://github.com/aaronraimist/element-themes) project by simply flipping a flag (`matrix_client_element_themes_enabled: true`).

If you make your own theme, we encourage you to submit it to the **aaronraimist/element-themes** project, so that the whole community could easily enjoy it.

Note that for a custom theme to work well, all Element instances that you use must have the same theme installed.
