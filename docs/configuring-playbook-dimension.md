# Setting up Dimension (optional)

**[Dimension](https://dimension.t2bot.io) can only be installed after Matrix services are installed and running.**
If you're just installing Matrix services for the first time, please continue with the [Configuration](configuring-playbook.md) / [Installation](installing.md) flow and come back here later.

## Prerequisites
For an Integration Manager like [Dimension](https://dimension.t2bot.io) to work, your server needs to have federation enabled (`matrix_synapse_federation_enabled: true`). This is the default for this playbook, so unless you've explicitly disabled federation, you're okay.

Other important prerequisite is the `dimension.<your-domain>` DNS record being set up correctly. See [Configuring your DNS server](configuring-dns.md) on how to set up DNS record correctly.

## Enable
[Dimension integrations manager](https://dimension.t2bot.io) installation is disabled by default. You can enable it in your configuration file (`inventory/host_vars/matrix.<your-domain>/vars.yml`):

```yaml
matrix_dimension_enabled: true
```


## Define admin users
These users can modify the integrations this Dimension supports. Admin interface is accessible by opening Dimension in Riot and clicking the settings icon.
Add this to your configuration file (`inventory/host_vars/matrix.<your-domain>/vars.yml`):

```yaml
matrix_dimension_admins: ['@user1:domain.com', '@user2:domain.com']
```

## Access token
You are required to specify an access token for Dimension to work.
To get an access token, follow these steps:

1. In a private browsing session (incognito window), open Riot.
2. It's preferable to use a dedicated user for the access token, so create and log in with that user's username and password.
3. Set the display name and avatar, if required.
4. In the settings page choose "Help & About", scroll down to the bottom and click `Access Token: <click to reveal>`.
5. Copy the highlighted text to your configuration.
6. Close the private browsing session. **Do not log out**. Logging out will invalidate the token, making it not work.

**Access tokens are sensitive information. Do not include them in any bug reports, messages, or logs. Do not share the access token with anyone.**

Add access token to your configuration file (`inventory/host_vars/matrix.<your-domain>/vars.yml`):

```yaml
matrix_dimension_access_token: "YOUR ACCESS TOKEN HERE"
```

For more information on how to acquire an access token, visit [https://t2bot.io/docs/access_tokens](https://t2bot.io/docs/access_tokens).

After these variables have been set, please run the following command to re-run setup and to restart Dimension:

```
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

## Additional features

To use a more custom configuration, you can define a `matrix_dimension_configuration_extension_yaml` string variable and put your configuration in it.
To learn more about how to do this, refer to the information about `matrix_dimension_configuration_extension_yaml` in the [default variables file](../roles/matrix-dimension/defaults/main.yml) of the Dimension component.

You can find all configuration options on [GitHub page of Dimension project](https://github.com/turt2live/matrix-dimension/blob/master/config/default.yaml).
