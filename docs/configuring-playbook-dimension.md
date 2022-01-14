# Setting up Dimension (optional)

**[Dimension](https://dimension.t2bot.io) can only be installed after Matrix services are installed and running.**
If you're just installing Matrix services for the first time, please continue with the [Configuration](configuring-playbook.md) / [Installation](installing.md) flow and come back here later.

**Note**: This playbook now supports running [Dimension](https://dimension.t2bot.io) in both a federated and [unfederated](https://github.com/turt2live/matrix-dimension/blob/master/docs/unfederated.md) environments. This is handled automatically based on the value of `matrix_synapse_federation_enabled`. Enabling Dimension, means that the `openid` API endpoints will be exposed on the Matrix Federation port (usually `8448`), even if [federation](configuring-playbook-federation.md) is disabled. It's something to be aware of, especially in terms of firewall whitelisting (make sure port `8448` is accessible).


## Prerequisites

The `dimension.<your-domain>` DNS record must be created. See [Configuring your DNS server](configuring-dns.md) on how to set up DNS record correctly.


## Enable

[Dimension integrations manager](https://dimension.t2bot.io) installation is disabled by default. You can enable it in your configuration file (`inventory/host_vars/matrix.<your-domain>/vars.yml`):

```yaml
matrix_dimension_enabled: true
```


## Define admin users

These users can modify the integrations this Dimension supports. Admin interface is accessible at `https://dimension.<your-domain>/riot-app/admin` after logging in to element.
Add this to your configuration file (`inventory/host_vars/matrix.<your-domain>/vars.yml`):

```yaml
matrix_dimension_admins:
  - "@user1:{{ matrix_domain }}"
  - "@user2:{{ matrix_domain }}"
```


## Access token

We recommend that you create a dedicated Matrix user for Dimension (`dimension` is a good username).
Follow our [Registering users](registering-users.md) guide to learn how to register **a regular (non-admin) user**.

You are required to specify an access token (belonging to this new user) for Dimension to work.
To get an access token for the Dimension user, you can follow one of two options:

*Through an interactive login*:

1. In a private browsing session (incognito window), open Element.
1. Log in with the `dimension` user and its password.
1. Set the display name and avatar, if required.
1. In the settings page choose "Help & About", scroll down to the bottom and expand the `Access Token` section.
1. Copy the access token to your configuration.
1. Close the private browsing session. **Do not log out**. Logging out will invalidate the token, making it not work.

*With CURL*

```
curl -X POST --header 'Content-Type: application/json' -d '{
    "identifier": { "type": "m.id.user", "user": "YourDimensionUsername" },
    "password": "YourDimensionPassword",
    "type": "m.login.password"
}' 'https://matrix.YOURDOMAIN/_matrix/client/r0/login'
```
*Change `YourDimensionUsername`, `YourDimensionPassword`, and `YOURDOMAIN` accordingly.*

**Access tokens are sensitive information. Do not include them in any bug reports, messages, or logs. Do not share the access token with anyone.**

Add access token to your configuration file (`inventory/host_vars/matrix.<your-domain>/vars.yml`):

```yaml
matrix_dimension_access_token: "YOUR ACCESS TOKEN HERE"
```

For more information on how to acquire an access token, visit [https://t2bot.io/docs/access_tokens](https://t2bot.io/docs/access_tokens).


## Installation

After these variables have been set, please run the following command to re-run setup and to restart Dimension:

```
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

After Dimension has been installed you may need to log out and log back in for it to pick up the new integrations manager. Then you can access integrations in Element by opening a room, clicking the Room info button (`i`) button in the top right corner of the screen, and then clicking Add widgets, bridges & bots.


## Jitsi domain

By default Dimension will use [jitsi.riot.im](https://jitsi.riot.im/) as the `conferenceDomain` of [Jitsi](https://jitsi.org/) audio/video conference widgets. For users running [a self-hosted Jitsi instance](./configuring-playbook-jitsi.md), you will likely want the widget to use your own Jitsi instance. Currently there is no way to configure this via the playbook, see [this issue](https://github.com/turt2live/matrix-dimension/issues/345) for details.

In the interim until the above limitation is resolved, an admin user needs to configure the domain via the admin ui once dimension is running. In Element, go to *Manage Integrations* &rightarrow; *Settings* &rightarrow; *Widgets* &rightarrow; *Jitsi Conference Settings* and set *Jitsi Domain* and *Jitsi Script URL* appropriately.


## Additional features

To use a more custom configuration, you can define a `matrix_dimension_configuration_extension_yaml` string variable and put your configuration in it.
To learn more about how to do this, refer to the information about `matrix_dimension_configuration_extension_yaml` in the [default variables file](../roles/matrix-dimension/defaults/main.yml) of the Dimension component.

You can find all configuration options on [GitHub page of Dimension project](https://github.com/turt2live/matrix-dimension/blob/master/config/default.yaml).
