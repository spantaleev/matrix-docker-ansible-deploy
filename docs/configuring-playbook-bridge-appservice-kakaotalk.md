# Setting up Appservice Kakaotalk (optional)

The playbook can install and configure [matrix-appservice-kakaotalk](https://src.miscworks.net/fair/matrix-appservice-kakaotalk) for you. `matrix-appservice-kakaotalk` is a bridge to [Kakaotalk](https://www.kakaocorp.com/page/service/service/KakaoTalk?lang=ENG) based on [node-kakao](https://github.com/storycraft/node-kakao) (now unmaintained) and some [mautrix-facebook](https://github.com/mautrix/facebook) code.

See the project's [documentation](https://src.miscworks.net/fair/matrix-appservice-kakaotalk) to learn what it does and why it might be useful to you.


## Installing

To enable the bridge, add this to your `vars.yml` file:

```yaml
matrix_appservice_kakaotalk_enabled: true
```

You may optionally wish to add some [Additional configuration](#additional-configuration), or to [prepare for double-puppeting](#set-up-double-puppeting) before the initial installation.

After adjusting your `vars.yml` file, re-run the playbook and restart all services: `ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start`

To make use of the Kakaotalk bridge, see [Usage](#usage) below.


### Additional configuration

There are some additional things you may wish to configure about the bridge.

Take a look at:

- `roles/matrix-bridge-appservice-kakaotalk/defaults/main.yml` for some variables that you can customize via your `vars.yml` file
- `roles/matrix-bridge-appservice-kakaotalk/templates/config.yaml.j2` for the bridge's default configuration. You can override settings (even those that don't have dedicated playbook variables) using the `matrix_appservice_kakaotalk_configuration_extension_yaml` variable


### Set up Double Puppeting

If you'd like to use [Double Puppeting](https://docs.mau.fi/bridges/general/double-puppeting.html) (hint: you most likely do), you have 2 ways of going about it.

#### Method 1: automatically, by enabling Shared Secret Auth

The bridge will automatically perform Double Puppeting if you enable [Shared Secret Auth](configuring-playbook-shared-secret-auth.md) for this playbook.

This is the recommended way of setting up Double Puppeting, as it's easier to accomplish, works for all your users automatically, and has less of a chance of breaking in the future.

#### Method 2: manually, by asking each user to provide a working access token

**Note**: This method for enabling Double Puppeting can be configured only after you've already set up bridging (see [Usage](#usage)).

When using this method, **each user** that wishes to enable Double Puppeting needs to follow the following steps:

- retrieve a Matrix access token for yourself. You can use the following command:

```
curl \
--data '{"identifier": {"type": "m.id.user", "user": "YOUR_MATRIX_USERNAME" }, "password": "YOUR_MATRIX_PASSWORD", "type": "m.login.password", "device_id": "Appservice-Kakaotalk", "initial_device_display_name": "Appservice-Kakaotalk"}' \
https://matrix.DOMAIN/_matrix/client/r0/login
```

- send the access token to the bot. Example: `login-matrix MATRIX_ACCESS_TOKEN_HERE`

- make sure you don't log out the `Appservice-Kakaotalk` device some time in the future, as that would break the Double Puppeting feature


## Usage

Start a chat with `@kakaotalkbot:YOUR_DOMAIN` (where `YOUR_DOMAIN` is your base domain, not the `matrix.` domain).

Send `login --save EMAIL_OR_PHONE_NUMBER` to the bridge bot to enable bridging for your Kakaotalk account. The `--save` flag may be omitted, if you'd rather not save your password.

After successfully enabling bridging, you may wish to [set up Double Puppeting](#set-up-double-puppeting), if you haven't already done so.
