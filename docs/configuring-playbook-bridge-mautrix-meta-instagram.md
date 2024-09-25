# Setting up Instagram bridging via Mautrix Meta (optional)

The playbook can install and configure the [mautrix-meta](https://github.com/mautrix/meta) Messenger/Instagram bridge for you.

Since this bridge component can bridge to both [Messenger](https://messenger.com/) and [Instagram](https://instagram.com/) and you may wish to do both at the same time, the playbook makes it available via 2 different Ansible roles (`matrix-bridge-mautrix-meta-messenger` and `matrix-bridge-mautrix-meta-instagram`). The latter is a reconfigured copy of the first one (created by `just rebuild-mautrix-meta-instagram` and `bin/rebuild-mautrix-meta-instagram.sh`).

This documentation page only deals with the bridge's ability to bridge to Instagram. For bridging to Facebook/Messenger, see [Setting up Messenger bridging via Mautrix Meta](configuring-playbook-bridge-mautrix-meta-messenger.md).


## Migrating from the old mautrix-instagram bridge

If you've been using the [mautrix-instagram](./configuring-playbook-bridge-mautrix-instagram.md) bridge, **you'd better get rid of it first** or the 2 bridges will be in conflict:

- both trying to use `@instagrambot:YOUR_DOMAIN` as their username. This conflict may be resolved by adjusting `matrix_mautrix_instagram_appservice_bot_username` or `matrix_mautrix_meta_instagram_appservice_username`
- both trying to bridge the same DMs

To do so, send a `clean-rooms` command to the management room with the old bridge bot (`@instagrambot:YOUR_DOMAIN`).

This would give you a list of portals and groups of portals you may purge. Proceed with sending commands like `clean recommended`, etc.

Then, consider disabling the old bridge in your configuration, so it won't recreate the portals when you receive new messages.


## Configuration

Most simply, you can enable the bridge with the following playbook configuration:

```yaml
matrix_mautrix_meta_instagram_enabled: true
```

Before proceeding to [re-running the playbook](./installing.md), you may wish to adjust the configuration further. See below.

### Bridge permissions

By default, any user on your homeserver will be able to use the bridge.

Different levels of permission can be granted to users:

- `relay` - Allowed to be relayed through the bridge, no access to commands
- `user` - Use the bridge with puppeting
- `admin` - Use and administer the bridge

The permissions are following the sequence: nothing < `relay` < `user` < `admin`.

The default permissions are set via `matrix_mautrix_meta_instagram_bridge_permissions_default` and are somewhat like this:
```yaml
matrix_mautrix_meta_instagram_bridge_permissions_default:
  '*': relay
  YOUR_DOMAIN: user
  '{{ matrix_admin }}': admin
```

If you don't define the `matrix_admin` in your configuration (e.g. `matrix_admin: @user:YOUR_DOMAIN`), then there's no admin by default.

You may redefine `matrix_mautrix_meta_instagram_bridge_permissions_default` any way you see fit, or add extra permissions using `matrix_mautrix_meta_instagram_bridge_permissions_custom` like this:

```yaml
matrix_mautrix_meta_instagram_bridge_permissions_custom:
  '@YOUR_USERNAME:YOUR_DOMAIN': admin
```

You may wish to look at `roles/custom/matrix-bridge-mautrix-meta-instagram/templates/config.yaml.j2` to find more information on the permissions settings and other options you would like to configure.

## Set up Double Puppeting

If you'd like to use [Double Puppeting](https://docs.mau.fi/bridges/general/double-puppeting.html) (hint: you most likely do), you have 2 ways of going about it.

### Method 1: automatically, by enabling Appservice Double Puppet

The bridge will automatically perform Double Puppeting if you enable the [Appservice Double Puppet](configuring-playbook-appservice-double-puppet.md) service for this playbook.

Enabling [Appservice Double Puppet](configuring-playbook-appservice-double-puppet.md) is the recommended way of setting up Double Puppeting, as it's easier to accomplish, works for all your users automatically, and has less of a chance of breaking in the future.

### Method 2: manually, by asking each user to provide a working access token

**Note**: This method for enabling Double Puppeting can be configured only after you've already set up bridging (see [Usage](#usage)).

When using this method, **each user** that wishes to enable Double Puppeting needs to follow the following steps:

- retrieve a Matrix access token for yourself. Refer to the documentation on [how to do that](obtaining-access-tokens.md).

- send the access token to the bot. Example: `login-matrix MATRIX_ACCESS_TOKEN_HERE`

- make sure you don't log out the session for which you obtained an access token some time in the future, as that would break the Double Puppeting feature


## Usage

You then need to start a chat with `@instagrambot:YOUR_DOMAIN` (where `YOUR_DOMAIN` is your base domain, not the `matrix.` domain).
