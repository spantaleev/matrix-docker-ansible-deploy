# Setting up SchildiChat Web (optional)

This playbook can install the [SchildiChat Web](https://github.com/SchildiChat/schildichat-desktop) Matrix client for you.

SchildiChat Web is a feature-rich messenger for Matrix based on Element Web with some extras and tweaks. It can be installed alongside or instead of Element Web.

💡 **Note**: the latest version of SchildiChat Web is also available on the web, hosted by 3rd parties. If you trust giving your credentials to the following 3rd party Single Page Application, you can consider using it from there:

- [app.schildi.chat](https://app.schildi.chat/), hosted by the [SchildiChat](https://schildi.chat/) developers

## Adjusting the playbook configuration

To enable SchildiChat Web, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_client_schildichat_enabled: true
```

### Themes

You can change the look of SchildiChat Web by pulling themes provided by the [aaronraimist/element-themes](https://github.com/aaronraimist/element-themes) project or defining your own themes manually.

#### Use themes by `element-themes`

To pull the themes from the `element-themes` project and use them for your SchildiChat Web instance, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_client_schildichat_themes_enabled: true
```

If the variable is set to `true`, all themes found in the repository specified with `matrix_client_schildichat_themes_repository_url` will be installed and enabled automatically.

Note that for a custom theme to work well, all SchildiChat Web instances that you use must have the same theme installed.

#### Define themes manually

You can also define your own themes manually by adding and adjusting the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
# Controls the `setting_defaults.custom_themes` setting of the SchildiChat Web configuration.
matrix_client_schildichat_setting_defaults_custom_themes: []
```

If you define your own themes with it and set `matrix_client_schildichat_themes_enabled` to `true` for the themes by `element-themes`, your themes will be preserved as well.

If you make your own theme, we encourage you to submit it to the **aaronraimist/element-themes** project, so that the whole community could easily enjoy it.

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

### Extending the configuration

There are some additional things you may wish to configure about the component.

Take a look at:

- `roles/custom/matrix-client-schildichat/defaults/main.yml` for some variables that you can customize via your `vars.yml` file
- `roles/custom/matrix-client-schildichat/templates/config.json.j2` for the component's default configuration. You can override settings (even those that don't have dedicated playbook variables) using the `matrix_client_schildichat_configuration_extension_json` variable

For example, to override some SchildiChat Web settings, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
 # Your custom JSON configuration for SchildiChat Web should go to `matrix_client_schildichat_configuration_extension_json`.
 # This configuration extends the default starting configuration (`matrix_client_schildichat_configuration_default`).
 #
 # You can override individual variables from the default configuration, or introduce new ones.
 #
 # If you need something more special, you can take full control by
 # completely redefining `matrix_client_schildichat_configuration_default`.
 #
matrix_client_schildichat_configuration_extension_json: |
 {
 "disable_3pid_login": true,
 "disable_login_language_selector": true
 }
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

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.
