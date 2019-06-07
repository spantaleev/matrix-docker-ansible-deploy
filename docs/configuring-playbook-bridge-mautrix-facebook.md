# Setting up Mautrix Facebook (optional)

The playbook can install and configure [mautrix-facebook](https://github.com/tulir/mautrix-facebook) for you.

See the project's [documentation](https://github.com/tulir/mautrix-facebook/wiki#usage) to learn what it does and why it might be useful to you.

```yaml
matrix_mautrix_facebook_enabled: true
```

## Usage

You then need to start a chat with `@facebookbot:YOUR_DOMAIN` (where `YOUR_DOMAIN` is your base domain, not the `matrix.` domain).


### Set up bridging

Send `login YOUR_FACEBOOK_EMAIL_ADDRESS YOUR_FACEBOOK_PASSWORD` to the bridge bot to enable bridging for your Facebook/Messenger account.

You can learn more here about authentication from the bridge's [official documentation on Authentication](https://github.com/tulir/mautrix-facebook/wiki/Authentication).

If you run into trouble, check the [Troubleshooting](#troubleshooting) section below.

After successfully enabling bridging, you may wish to [set up Double Puppeting](#set-up-double-puppeting).


### Set up Double Puppeting

**Note**: Double Puppeting can be configured only after you've already [set up bridging](#set-up-bridging).

If you'd like to use [Double Puppeting](https://github.com/tulir/mautrix-facebook/wiki/Authentication#double-puppeting) (hint: you most likely do), you should:

- retrieve a Matrix access token for yourself. You can use the following command:

```
curl \
--data '{"identifier": {"type": "m.id.user", "user": "YOUR_MATRIX_USERNAME" }, "password": "YOUR_MATRIX_PASSWORD", "type": "m.login.password", "device_id": "Mautrix-Facebook", "initial_device_display_name": "Mautrix-Facebook"}' \
https://matrix.DOMAIN/_matrix/client/r0/login
```

- send the access token to the bot. Example: `login-matrix MATRIX_ACCESS_TOKEN_HERE`

- make sure you don't log out the `Mautrix-Facebook` device some time in the future, as that would break the Double Puppeting feature


## Troubleshooting

### Facebook rejecting login attempts and forcing you to change password

If your Matrix server is in a wildly different location than where you usually use your Facebook account from, the bridge's login attempts may be outright rejected by Facebook. Along with that, Facebook may even force you to change the account's password.

If you happen to run into this problem while [setting up bridging](#set-up-bridging), try to first get a successful session up by logging in to Facebook through the Matrix server's IP address.

The easiest way to do this may be to use [sshutle](https://sshuttle.readthedocs.io/) to proxy your traffic through the Matrix server.

Example command for proxying your traffic through the Matrix server:

```
sshuttle -r root@matrix.DOMAIN:22 0/0
```

Once connected, you should be able to verify that you're browsing the web through the Matrix server's IP by checking [icanhazip](https://icanhazip.com/).

Then proceed to log in to [Facebook/Messenger](https://www.facebook.com/).

Once logged in, proceed to [set up bridging](#set-up-bridging).
