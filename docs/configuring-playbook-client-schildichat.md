# Configuring SchildiChat (optional)

By default, this playbook does not install the [SchildiChat](https://github.com/SchildiChat/schildichat-desktop) Matrix client web application.

**WARNING**: SchildiChat is based on Element-web, but its releases are lagging behind. As an example (from 2023-08-31), SchildiChat is 10 releases behind (it being based on element-web `v1.11.30`, while element-web is now on `v1.11.40`). Element-web frequently suffers from security issues, so running something based on an ancient Element-web release is **dangerous**. Use SchildiChat at your own risk!


## Enabling SchildiChat

If you'd like for the playbook to install SchildiChat, you can enable it in your configuration file (`inventory/host_vars/matrix.<your-domain>/vars.yml`):

```yaml
matrix_client_schildichat_enabled: true
```


## Configuring SchildiChat settings

The playbook provides some customization variables you could use to change schildichat's settings.

Their defaults are defined in [`roles/custom/matrix-client-schildichat/defaults/main.yml`](../roles/custom/matrix-client-schildichat/defaults/main.yml) and they ultimately end up in the generated `/matrix/schildichat/config.json` file (on the server). This file is generated from the [`roles/custom/matrix-client-schildichat/templates/config.json.j2`](../roles/custom/matrix-client-schildichat/templates/config.json.j2) template.

**If there's an existing variable** which controls a setting you wish to change, you can simply define that variable in your configuration file (`inventory/host_vars/matrix.<your-domain>/vars.yml`) and [re-run the playbook](installing.md) to apply the changes.

Alternatively, **if there is no pre-defined variable** for an schildichat setting you wish to change:

- you can either **request a variable to be created** (or you can submit such a contribution yourself). Keep in mind that it's **probably not a good idea** to create variables for each one of schildichat's various settings that rarely get used.

- or, you can **extend and override the default configuration** ([`config.json.j2`](../roles/custom/matrix-client-schildichat/templates/config.json.j2)) by making use of the `matrix_client_schildichat_configuration_extension_json_` variable. You can find information about this in [`roles/custom/matrix-client-schildichat/defaults/main.yml`](../roles/custom/matrix-client-schildichat/defaults/main.yml).

- or, if extending the configuration is still not powerful enough for your needs, you can **override the configuration completely** using `matrix_client_schildichat_configuration_default` (or `matrix_client_schildichat_configuration`). You can find information about this in [`roles/custom/matrix-client-schildichat/defaults/main.yml`](../roles/custom/matrix-client-schildichat/defaults/main.yml).


## Themes

To change the look of schildichat, you can define your own themes manually by using the `matrix_client_schildichat_setting_defaults_custom_themes` setting.

Or better yet, you can automatically pull it all themes provided by the [aaronraimist/element-themes](https://github.com/aaronraimist/element-themes) project by simply flipping a flag (`matrix_client_schildichat_themes_enabled: true`).

If you make your own theme, we encourage you to submit it to the **aaronraimist/element-themes** project, so that the whole community could easily enjoy it.

Note that for a custom theme to work well, all schildichat instances that you use must have the same theme installed.
