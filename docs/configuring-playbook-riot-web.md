# Configuring Riot-web (optional)

By default, this playbook installs the [Riot-web](https://github.com/vector-im/riot-web) Matrix client web application.
If that's okay, you can skip this document.


## Disabling riot-web

If you'd like for the playbook to not install (or to uninstall the previously installed riot-web), you can disable it in your configuration file (`inventory/host_vars/matrix.<your-domain>/vars.yml`):

```yaml
matrix_riot_web_enabled: false
```

## Configuring riot-web settings

The playbook provides some customization variables you could use to change riot-web's settings.

Their defaults are defined in [`roles/matrix-riot-web/defaults/main.yml`](../roles/matrix-riot-web/defaults/main.yml) and they ultimately end up in the generated `/matrix/riot-web/config.json` file (on the server). This file is generated from the [`roles/matrix-riot-web/templates/config.json.j2`](../roles/matrix-riot-web/templates/config.json.j2) template.

**If there's an existing variable** which controls a setting you wish to change, you can simply define that variable in your configuration file (`inventory/host_vars/matrix.<your-domain>/vars.yml`) and [re-run the playbook](installing.md) to apply the changes.

Alternatively, **if there is no pre-defined variable** for a riot-web setting you wish to change:

- you can either **request a variable to be created** (or you can submit such a contribution yourself). Keep in mind that it's **probably not a good idea** to create variables for each one of riot-web's various settings that rarely get used.

- or, you can **extend and override the default configuration** ([`config.json.j2`](../roles/matrix-riot-web/templates/config.json.j2)) by making use of the `matrix_riot_web_configuration_extension_json_` variable. You can find information about this in [`roles/matrix-riot-web/defaults/main.yml`](../roles/matrix-riot-web/defaults/main.yml).

- or, if extending the configuration is still not powerful enough for your needs, you can **override the configuration completely** using `matrix_riot_web_configuration_default` (or `matrix_riot_web_configuration`). You can find information about this in [`roles/matrix-riot-web/defaults/main.yml`](../roles/matrix-riot-web/defaults/main.yml).


## Themes

To change the look of riot-web, you can define your own themes manually by using the `matrix_riot_web_settingDefaults_custom_themes` setting.

Or better yet, you can automatically pull it all themes provided by the [aaronraimist/riot-web-themes](https://github.com/aaronraimist/riot-web-themes) project by simply flipping a flag (`matrix_riot_web_themes_enabled: true`).

If you make your own theme, we encourage you to submit it to the **aaronraimist/riot-web-themes** project, so that the whole community could easily enjoy it.

Note that for a custom theme to work well, all riot-web/riot-desktop instances that you use must have the same theme installed.
