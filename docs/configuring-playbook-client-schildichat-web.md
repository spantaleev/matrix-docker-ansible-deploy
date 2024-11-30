# Setting up SchildiChat Web (optional)

This playbook can install the [SchildiChat Web](https://github.com/SchildiChat/schildichat-desktop) Matrix client for you.

SchildiChat Web is a feature-rich messenger for Matrix based on Element Web with some extras and tweaks. It can be installed alongside or instead of Element Web.

💡 **Note**: the latest version of SchildiChat Web is also available on the web, hosted by 3rd parties. If you trust giving your credentials to the following 3rd party Single Page Application, you can consider using it from there:

- [app.schildi.chat](https://app.schildi.chat/), hosted by the [SchildiChat](https://schildi.chat/) developers

**WARNING**: SchildiChat Web is based on Element Web, but its releases are lagging behind. As of 2024-11, SchildiChat Web is many releases behind (it being based on Element Web `v1.11.36`, while Element Web is now on `v1.11.85`). Element Web frequently suffers from security issues (see [here](https://github.com/element-hq/element-web/security) for known issues), so running something based on an ancient Element Web release is **unsafe**. Use SchildiChat Web at your own risk!

## Adjusting the playbook configuration

To enable SchildiChat Web, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_client_schildichat_enabled: true
```

The playbook provides some customization variables you could use to change SchildiChat Web's settings.

Their defaults are defined in [`roles/custom/matrix-client-schildichat/defaults/main.yml`](../roles/custom/matrix-client-schildichat/defaults/main.yml) and they ultimately end up in the generated `/matrix/schildichat/config.json` file (on the server). This file is generated from the [`roles/custom/matrix-client-schildichat/templates/config.json.j2`](../roles/custom/matrix-client-schildichat/templates/config.json.j2) template.

**If there's an existing variable** which controls a setting you wish to change, you can simply define that variable in your configuration file (`inventory/host_vars/matrix.example.com/vars.yml`) and [re-run the playbook](installing.md) to apply the changes.

Alternatively, **if there is no pre-defined variable** for a SchildiChat Web setting you wish to change:

- you can either **request a variable to be created** (or you can submit such a contribution yourself). Keep in mind that it's **probably not a good idea** to create variables for each one of SchildiChat Web's various settings that rarely get used.

- or, you can **extend and override the default configuration** ([`config.json.j2`](../roles/custom/matrix-client-schildichat/templates/config.json.j2)) by making use of the `matrix_client_schildichat_configuration_extension_json_` variable. You can find information about this in [`roles/custom/matrix-client-schildichat/defaults/main.yml`](../roles/custom/matrix-client-schildichat/defaults/main.yml).

- or, if extending the configuration is still not powerful enough for your needs, you can **override the configuration completely** using `matrix_client_schildichat_configuration_default` (or `matrix_client_schildichat_configuration`). You can find information about this in [`roles/custom/matrix-client-schildichat/defaults/main.yml`](../roles/custom/matrix-client-schildichat/defaults/main.yml).

### Themes

To change the look of SchildiChat Web, you can define your own themes manually by using the `matrix_client_schildichat_setting_defaults_custom_themes` setting.

Or better yet, you can automatically pull it all themes provided by the [aaronraimist/element-themes](https://github.com/aaronraimist/element-themes) project by simply flipping a flag (`matrix_client_schildichat_themes_enabled: true`).

If you make your own theme, we encourage you to submit it to the **aaronraimist/element-themes** project, so that the whole community could easily enjoy it.

Note that for a custom theme to work well, all SchildiChat Web instances that you use must have the same theme installed.

### Adjusting the SchildiChat Web URL

By default, this playbook installs SchildiChat Web on the `schildichat.` subdomain (`schildichat.example.com`) and requires you to [adjust your DNS records](#adjusting-dns-records).

By tweaking the `matrix_client_schildichat_hostname` and `matrix_client_schildichat_path_prefix` variables, you can easily make the service available at a **different hostname and/or path** than the default one.

Example additional configuration for your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
# Switch to the domain used for Matrix services (`matrix.example.com`),
# so we won't need to add additional DNS records for SchildiChat Web.
matrix_client_schildichat_hostname: "{{ matrix_server_fqn_matrix }}"

# Expose under the /schildichat subpath
matrix_client_schildichat_path_prefix: /schildichat
```

## Adjusting DNS records

Once you've decided on the domain and path, **you may need to adjust your DNS** records to point the SchildiChat Web domain to the Matrix server.

By default, you will need to create a CNAME record for `schildichat`. See [Configuring DNS](configuring-dns.md) for details about DNS changes.

If you've decided to reuse the `matrix.` domain, you won't need to do any extra DNS configuration.

## Installing

After configuring the playbook and potentially [adjusting your DNS records](#adjusting-dns-records), run the playbook with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with `just` program are also available: `just run-tags install-all,start` or `just run-tags setup-all,start`

`just run-tags install-all,start` is useful for maintaining your setup quickly when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just run-tags setup-all,start`, or these components will still remain installed. For more information about `just` shortcuts, take a look at this page: [Running `just` commands](just.md)
