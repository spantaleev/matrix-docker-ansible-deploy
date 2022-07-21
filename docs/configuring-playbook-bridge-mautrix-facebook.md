# Setting up Mautrix Facebook (optional)

The playbook can install and configure [mautrix-facebook](https://github.com/mautrix/facebook) for you.

See the project's [documentation](https://github.com/mautrix/facebook/blob/master/ROADMAP.md) to learn what it does and why it might be useful to you.

```yaml
matrix_mautrix_facebook_enabled: true
```

There are some additional things you may wish to configure about the bridge before you continue.

Encryption support is off by default. If you would like to enable encryption, add the following to your `vars.yml` file:
```yaml
matrix_mautrix_facebook_configuration_extension_yaml: |
  bridge:
    encryption:
      allow: true
      default: true
```

If you would like to be able to administrate the bridge from your account it can be configured like this:
```yaml
matrix_mautrix_facebook_configuration_extension_yaml: |
  bridge:
    permissions:
      '@YOUR_USERNAME:{{ matrix_domain }}': admin
```

Using both would look like

```yaml
matrix_mautrix_facebook_configuration_extension_yaml: |
  bridge:
    permissions:
      '@YOUR_USERNAME:{{ matrix_domain }}': admin
    encryption:
      allow: true
      default: true
```

You may wish to look at `roles/matrix-bridge-mautrix-facebook/templates/config.yaml.j2` and `roles/matrix-bridge-mautrix-facebook/defaults/main.yml` to find other things you would like to configure.


## Set up Double Puppeting

If you'd like to use [Double Puppeting](https://docs.mau.fi/bridges/general/double-puppeting.html) (hint: you most likely do), you have 2 ways of going about it.

### Method 1: automatically, by enabling Shared Secret Auth

The bridge will automatically perform Double Puppeting if you enable [Shared Secret Auth](configuring-playbook-shared-secret-auth.md) for this playbook.

This is the recommended way of setting up Double Puppeting, as it's easier to accomplish, works for all your users automatically, and has less of a chance of breaking in the future.

### Method 2: manually, by asking each user to provide a working access token

**Note**: This method for enabling Double Puppeting can be configured only after you've already set up bridging (see [Usage](#usage)).

When using this method, **each user** that wishes to enable Double Puppeting needs to follow the following steps:

- retrieve a Matrix access token for yourself. You can use the following command:

```
curl \
--data '{"identifier": {"type": "m.id.user", "user": "YOUR_MATRIX_USERNAME" }, "password": "YOUR_MATRIX_PASSWORD", "type": "m.login.password", "device_id": "Mautrix-Facebook", "initial_device_display_name": "Mautrix-Facebook"}' \
https://matrix.DOMAIN/_matrix/client/r0/login
```

- send the access token to the bot. Example: `login-matrix MATRIX_ACCESS_TOKEN_HERE`

- make sure you don't log out the `Mautrix-Facebook` device some time in the future, as that would break the Double Puppeting feature


## Usage

You then need to start a chat with `@facebookbot:YOUR_DOMAIN` (where `YOUR_DOMAIN` is your base domain, not the `matrix.` domain).

Send `login YOUR_FACEBOOK_EMAIL_ADDRESS` to the bridge bot to enable bridging for your Facebook Messenger account. You can learn more here about authentication from the bridge's [official documentation on Authentication](https://docs.mau.fi/bridges/python/facebook/authentication.html).

If you run into trouble, check the [Troubleshooting](#troubleshooting) section below.

After successfully enabling bridging, you may wish to [set up Double Puppeting](#set-up-double-puppeting), if you haven't already done so.


## Troubleshooting

### Facebook rejecting login attempts and forcing you to change password

If your Matrix server is in a wildly different location than where you usually use your Facebook account from, the bridge's login attempts may be outright rejected by Facebook. Along with that, Facebook may even force you to change the account's password.

If you happen to run into this problem while [setting up bridging](#usage), try to first get a successful session up by logging in to Facebook through the Matrix server's IP address.

The easiest way to do this may be to use [sshuttle](https://sshuttle.readthedocs.io/) to proxy your traffic through the Matrix server.

Example command for proxying your traffic through the Matrix server:

```
sshuttle -r root@matrix.DOMAIN:22 0/0
```

Once connected, you should be able to verify that you're browsing the web through the Matrix server's IP by checking [icanhazip](https://icanhazip.com/).

Then proceed to log in to [Facebook/Messenger](https://www.facebook.com/).

Once logged in, proceed to [set up bridging](#usage).

If that doesn't work, enable 2FA [Facebook help page on enabling 2FA](https://www.facebook.com/help/148233965247823) and try to login again with a new password, and entering the 2FA code when prompted, it may take more then one try, in between attempts, check facebook.com to see if they are requiring another password change
