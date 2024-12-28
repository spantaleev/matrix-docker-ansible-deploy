# Configuring Dendrite (optional)

By default, this playbook configures the [Synapse](https://github.com/element-hq/synapse) Matrix server, but you can also use [Dendrite](https://github.com/matrix-org/dendrite).

**Notes**:

- **You can't switch an existing Matrix server's implementation** (e.g. Synapse -> Dendrite). Proceed below only if you're OK with losing data or you're dealing with a server on a new domain name, which hasn't participated in the Matrix federation yet.

- **homeserver implementations other than Synapse may not be fully functional**. The playbook may also not assist you in an optimal way (like it does with Synapse). Make yourself familiar with the downsides before proceeding

## Adjusting the playbook configuration

To use Dendrite, you **generally** need to add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_homeserver_implementation: dendrite
```

### Extending the configuration

There are some additional things you may wish to configure about the server.

Take a look at:

- `roles/custom/matrix-dendrite/defaults/main.yml` for some variables that you can customize via your `vars.yml` file
- `roles/custom/matrix-dendrite/templates/dendrite.yaml.j2` for the server's default configuration. You can override settings (even those that don't have dedicated playbook variables) using the `matrix_dendrite_configuration_extension_yaml` variable

**If there's an existing variable** which controls a setting you wish to change, you can simply define that variable in your configuration file (`inventory/host_vars/matrix.example.com/vars.yml`) and [re-run the playbook](installing.md) to apply the changes.

Alternatively, **if there is no pre-defined variable** for a Dendrite setting you wish to change:

- you can either **request a variable to be created** (or you can submit such a contribution yourself). Keep in mind that it's **probably not a good idea** to create variables for each one of Dendrite's various settings that rarely get used.

- or, you can **extend and override the default configuration** ([`dendrite.yaml.j2`](../roles/custom/matrix-dendrite/templates/dendrite.yaml.j2)) by making use of the `matrix_dendrite_configuration_extension_yaml` variable.

- or, if extending the configuration is still not powerful enough for your needs, you can **override the configuration completely** using `matrix_dendrite_configuration` (or `matrix_dendrite_configuration_yaml`).

For example, to override some Dendrite settings, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_dendrite_configuration_extension_yaml: |
  # Your custom YAML configuration for Dendrite goes here.
  # This configuration extends the default starting configuration (`matrix_dendrite_configuration_yaml`).
  #
  # You can override individual variables from the default configuration, or introduce new ones.
  #
  # If you need something more special, you can take full control by
  # completely redefining `matrix_dendrite_configuration_yaml`.
  #
  # Example configuration extension follows:
  #
  server_notices:
    system_mxid_localpart: notices
    system_mxid_display_name: "Server Notices"
    system_mxid_avatar_url: "mxc://example.com/oumMVlgDnLYFaPVkExemNVVZ"
    room_name: "Server Notices"
```

## Installing

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.
