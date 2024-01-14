# Setting up Dimension (optional)

**[Dimension](https://dimension.t2bot.io) can only be installed after Matrix services are installed and running.**
If you're just installing Matrix services for the first time, please continue with the [Configuration](configuring-playbook.md) / [Installation](installing.md) flow and come back here later.

**Note**: Dimension is **[officially unmaintained](https://github.com/spantaleev/matrix-docker-ansible-deploy/issues/2806#issuecomment-1673559299)**. We recommend not bothering with installing it.

**Note**: This playbook now supports running [Dimension](https://dimension.t2bot.io) in both a federated and [unfederated](https://github.com/turt2live/matrix-dimension/blob/master/docs/unfederated.md) environments. This is handled automatically based on the value of `matrix_homeserver_federation_enabled`. Enabling Dimension, means that the `openid` API endpoints will be exposed on the Matrix Federation port (usually `8448`), even if [federation](configuring-playbook-federation.md) is disabled. It's something to be aware of, especially in terms of firewall whitelisting (make sure port `8448` is accessible).


## Decide on a domain and path

By default, Dimension is configured to use its own dedicated domain (`dimension.DOMAIN`) and requires you to [adjust your DNS records](#adjusting-dns-records).

You can override the domain and path like this:

```yaml
# Switch to another hostname compared to the default (`dimension.{{ matrix_domain }}`)
matrix_dimension_hostname: "integrations.{{ matrix_domain }}"

```

While there is a `matrix_dimension_path_prefix` variable for changing the path where Dimension is served, overriding it is not possible right now due to [this Dimension issue](https://github.com/turt2live/matrix-dimension/issues/510). You must serve Dimension at a dedicated subdomain until this issue is solved.


## Adjusting DNS records

Once you've decided on the domain and path, **you may need to adjust your DNS** records to point the Dimension domain to the Matrix server.


## Enable

To enable Dimension, add this to your configuration file (`inventory/host_vars/matrix.<your-domain>/vars.yml`):

```yaml
matrix_dimension_enabled: true
```


## Define admin users

These users can modify the integrations this Dimension supports.
Add this to your configuration file (`inventory/host_vars/matrix.<your-domain>/vars.yml`):

```yaml
matrix_dimension_admins:
  - "@user1:{{ matrix_domain }}"
  - "@user2:{{ matrix_domain }}"
```

The admin interface is accessible within Element by accessing it in any room and clicking the cog wheel/settings icon in the top right. Currently, Dimension can be opened in Element by the "Add widgets, bridges, & bots" link in the room information.

## Access token

We recommend that you create a dedicated Matrix user for Dimension (`dimension` is a good username).
Follow our [Registering users](registering-users.md) guide to learn how to register **a regular (non-admin) user**.

You are required to specify an access token (belonging to this new user) for Dimension to work.
To get an access token for the Dimension user, you can follow the documentation on [how to do obtain an access token](obtaining-access-tokens.md).

**Access tokens are sensitive information. Do not include them in any bug reports, messages, or logs. Do not share the access token with anyone.**

Add access token to your configuration file (`inventory/host_vars/matrix.<your-domain>/vars.yml`):

```yaml
matrix_dimension_access_token: "YOUR ACCESS TOKEN HERE"
```

For more information on how to acquire an access token, visit [https://t2bot.io/docs/access_tokens](https://t2bot.io/docs/access_tokens).


## Installation

After these variables have been set and you have potentially [adjusted your DNS records](#adjusting-dns-records), please run the following command to re-run setup and to restart Dimension:

```
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

After Dimension has been installed you may need to log out and log back in for it to pick up the new integrations manager. Then you can access integrations in Element by opening a room, clicking the Room info button (`i`) button in the top right corner of the screen, and then clicking Add widgets, bridges & bots.


## Jitsi domain

By default Dimension will use [jitsi.riot.im](https://jitsi.riot.im/) as the `conferenceDomain` of [Jitsi](https://jitsi.org/) audio/video conference widgets. For users running [a self-hosted Jitsi instance](./configuring-playbook-jitsi.md), you will likely want the widget to use your own Jitsi instance. Currently there is no way to configure this via the playbook, see [this issue](https://github.com/turt2live/matrix-dimension/issues/345) for details.

In the interim until the above limitation is resolved, an admin user needs to configure the domain via the admin ui once dimension is running. In Element, go to *Manage Integrations* &rightarrow; *Settings* &rightarrow; *Widgets* &rightarrow; *Jitsi Conference Settings* and set *Jitsi Domain* and *Jitsi Script URL* appropriately.


## Additional features

To use a more custom configuration, you can define a `matrix_dimension_configuration_extension_yaml` string variable and put your configuration in it.
To learn more about how to do this, refer to the information about `matrix_dimension_configuration_extension_yaml` in the [default variables file](../roles/custom/matrix-dimension/defaults/main.yml) of the Dimension component.

You can find all configuration options on [GitHub page of Dimension project](https://github.com/turt2live/matrix-dimension/blob/master/config/default.yaml).
