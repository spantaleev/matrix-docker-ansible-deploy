# Setting up Dimension integration manager (optional, unmaintained)

**Notes**:
- Dimension is **[officially unmaintained](https://github.com/spantaleev/matrix-docker-ansible-deploy/issues/2806#issuecomment-1673559299)**. We recommend not bothering with installing it.
- This playbook now supports running Dimension in both a federated and [unfederated](https://github.com/turt2live/matrix-dimension/blob/master/docs/unfederated.md) environments. This is handled automatically based on the value of `matrix_homeserver_federation_enabled`. Enabling Dimension, means that the `openid` API endpoints will be exposed on the Matrix Federation port (usually `8448`), even if [federation](configuring-playbook-federation.md) is disabled. It's something to be aware of, especially in terms of firewall whitelisting (make sure port `8448` is accessible).

The playbook can install and configure the [Dimension](https://dimension.t2bot.io) integration manager for you.

See the project's [documentation](https://github.com/turt2live/matrix-dimension/blob/master/README.md) to learn what it does and why it might be useful to you.

## Prerequisites

### Install Matrix services

Dimension can only be installed after Matrix services are installed and running. If you're just installing Matrix services for the first time, please continue with the [Configuration](configuring-playbook.md) / [Installation](installing.md) and come back here later.

### Register a dedicated Matrix user (optional, recommended)

We recommend that you create a dedicated Matrix user for Dimension (`dimension` is a good username).

Generate a strong password for the user. You can create one with a command like `pwgen -s 64 1`.

You can use the playbook to [register a new user](registering-users.md):

```sh
ansible-playbook -i inventory/hosts setup.yml --extra-vars='username=dimension password=PASSWORD_FOR_THE_USER admin=no' --tags=register-user
```

### Obtain an access token

Dimension requires an access token to be able to connect to your homeserver. Refer to the documentation on [how to obtain an access token](obtaining-access-tokens.md).

⚠️ **Warning**: Access tokens are sensitive information. Do not include them in any bug reports, messages, or logs. Do not share the access token with anyone.

## Adjusting the playbook configuration

To enable Dimension, add this to your configuration file (`inventory/host_vars/matrix.example.com/vars.yml`). Make sure to replace `ACCESS_TOKEN_HERE` with the one created [above](#obtain-an-access-token).

```yaml
matrix_dimension_enabled: true

matrix_dimension_access_token: "ACCESS_TOKEN_HERE"
```

### Define admin users

These users can modify the integrations this Dimension supports. Add this to your configuration file (`inventory/host_vars/matrix.example.com/vars.yml`):

```yaml
matrix_dimension_admins:
  - "@alice:{{ matrix_domain }}"
  - "@bob:{{ matrix_domain }}"
```

The admin interface is accessible within Element Web by accessing it in any room and clicking the cog wheel/settings icon in the top right. Currently, Dimension can be opened in Element Web by the "Add widgets, bridges, & bots" link in the room information.

### Adjusting the Dimension URL

By default, this playbook installs Dimension on the `dimension.` subdomain (`dimension.example.com`) and requires you to [adjust your DNS records](#adjusting-dns-records).

By tweaking the `matrix_dimension_hostname` and `matrix_dimension_path_prefix` variables, you can easily make the service available at a **different hostname and/or path** than the default one.

Example additional configuration for your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
# Switch to the domain used for Matrix services (`matrix.example.com`),
# so we won't need to add additional DNS records for Dimension.
matrix_dimension_hostname: "{{ matrix_server_fqn_matrix }}"

# Expose under the /dimension subpath
# matrix_dimension_path_prefix: /dimension
```

**Note**: While there is a `matrix_dimension_path_prefix` variable for changing the path where Dimension is served, overriding it is not possible due to [this Dimension issue](https://github.com/turt2live/matrix-dimension/issues/510). You must serve Dimension at a dedicated subdomain.

## Adjusting DNS records

Once you've decided on the domain and path, **you may need to adjust your DNS** records to point the Dimension domain to the Matrix server.

By default, you will need to create a CNAME record for `dimension`. See [Configuring DNS](configuring-dns.md) for details about DNS changes.

## Installing

After configuring the playbook and potentially [adjusting your DNS records](#adjusting-dns-records), run the playbook with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

**Notes**:

- The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

  `just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

- After Dimension has been installed you may need to log out and log back in for it to pick up the new integration manager. Then you can access integrations in Element Web by opening a room, clicking the Room info button (`i`) button in the top right corner of the screen, and then clicking Add widgets, bridges & bots.

## Jitsi domain

By default Dimension will use [jitsi.riot.im](https://jitsi.riot.im/) as the `conferenceDomain` of [Jitsi](https://jitsi.org/) audio/video conference widgets. For users running [a self-hosted Jitsi instance](./configuring-playbook-jitsi.md), you will likely want the widget to use your own Jitsi instance. Currently there is no way to configure this via the playbook, see [this issue](https://github.com/turt2live/matrix-dimension/issues/345) for details.

In the interim until the above limitation is resolved, an admin user needs to configure the domain via the admin ui once dimension is running. In Element Web, go to *Manage Integrations* &rightarrow; *Settings* &rightarrow; *Widgets* &rightarrow; *Jitsi Conference Settings* and set *Jitsi Domain* and *Jitsi Script URL* appropriately.

## Additional features

To use a more custom configuration, you can define a `matrix_dimension_configuration_extension_yaml` string variable and put your configuration in it. To learn more about how to do this, refer to the information about `matrix_dimension_configuration_extension_yaml` in the [default variables file](../roles/custom/matrix-dimension/defaults/main.yml) of the Dimension component.

You can find all configuration options on [GitHub page of Dimension project](https://github.com/turt2live/matrix-dimension/blob/master/config/default.yaml).
