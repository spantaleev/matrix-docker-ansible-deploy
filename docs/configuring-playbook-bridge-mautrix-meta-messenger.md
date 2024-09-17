# Setting up Messenger bridging via Mautrix Meta (optional)

The playbook can install and configure the [mautrix-meta](https://github.com/mautrix/meta) Messenger/Instagram bridge for you.

Since this bridge component can bridge to both [Messenger](https://messenger.com/) and [Instagram](https://instagram.com/) and you may wish to do both at the same time, the playbook makes it available via 2 different Ansible roles (`matrix-bridge-mautrix-meta-messenger` and `matrix-bridge-mautrix-meta-instagram`). The latter is a reconfigured copy of the first one (created by `just rebuild-mautrix-meta-instagram` and `bin/rebuild-mautrix-meta-instagram.sh`).

This documentation page only deals with the bridge's ability to bridge to Facebook Messenger. For bridging to Instagram, see [Setting up Instagram bridging via Mautrix Meta](configuring-playbook-bridge-mautrix-meta-instagram.md).


## Migrating from the old mautrix-facebook bridge

If you've been using the [mautrix-facebook](./configuring-playbook-bridge-mautrix-facebook.md) bridge, it's possible to migrate the database using [instructions from the bridge documentation](https://docs.mau.fi/bridges/go/meta/facebook-migration.html) (advanced).

Then you may wish to get rid of the Facebook bridge. To do so, send a `clean-rooms` command to the management room with the old bridge bot (`@facebookbot:YOUR_DOMAIN`).

This would give you a list of portals and groups of portals you may purge. Proceed with sending commands like `clean recommended`, etc.

Then, consider disabling the old bridge in your configuration, so it won't recreate the portals when you receive new messages.


## Configuration

Most simply, you can enable the bridge with the following playbook configuration:

```yaml
matrix_mautrix_meta_messenger_enabled: true
```

Before proceeding to [re-running the playbook](./installing.md), you may wish to adjust the configuration further. See below.

### Bridge mode

As mentioned above, the [mautrix-meta](https://github.com/mautrix/meta) bridge supports multiple modes of operation.
The bridge can pull your Messenger messages via 3 different methods:

- (`facebook`) Facebook via `facebook.com`
- (`facebook-tor`) Facebook via `facebookwkhpilnemxj7asaniu7vnjjbiltxjqhye3mhbshg7kx5tfyd.onion` ([Tor](https://www.torproject.org/)) - does not currently proxy media downloads
- (default) (`messenger`) Messenger via `messenger.com` - usable even without a Facebook account

You may switch the mode via the `matrix_mautrix_meta_messenger_meta_mode` variable. The playbook defaults to the `messenger` mode, because it's most universal (every Facebook user has a Messenger account, but the opposite is not true).

Note that switching the mode (especially between `facebook*` and `messenger`) will intentionally make the bridge use another database (`matrix_mautrix_meta_facebook` or `matrix_mautrix_meta_messenger`) to isolate the 2 instances. Switching between Tor and non-Tor may be possible without dataloss, but your mileage may vary. Before switching to a new mode, you may wish to de-configure the old one (send `help` to the bridge bot and unbridge your portals, etc.).


### Bridge permissions

By default, any user on your homeserver will be able to use the bridge.

Different levels of permission can be granted to users:

- `relay` - Allowed to be relayed through the bridge, no access to commands
- `user` - Use the bridge with puppeting
- `admin` - Use and administer the bridge

The permissions are following the sequence: nothing < `relay` < `user` < `admin`.

The default permissions are set via `matrix_mautrix_meta_messenger_bridge_permissions_default` and are somewhat like this:
```yaml
matrix_mautrix_meta_messenger_bridge_permissions_default:
  '*': relay
  YOUR_DOMAIN: user
  '{{ matrix_admin }}': admin
```

If you don't define the `matrix_admin` in your configuration (e.g. `matrix_admin: @user:YOUR_DOMAIN`), then there's no admin by default.

You may redefine `matrix_mautrix_meta_messenger_bridge_permissions_default` any way you see fit, or add extra permissions using `matrix_mautrix_meta_messenger_bridge_permissions_custom` like this:

```yaml
matrix_mautrix_meta_messenger_bridge_permissions_custom:
  '@YOUR_USERNAME:YOUR_DOMAIN': admin
```

You may wish to look at `roles/custom/matrix-bridge-mautrix-meta-messenger/templates/config.yaml.j2` to find more information on the permissions settings and other options you would like to configure.

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

You then need to start a chat with `@messengerbot:YOUR_DOMAIN` (where `YOUR_DOMAIN` is your base domain, not the `matrix.` domain).

You then need to send a `login` command and follow the bridge bot's instructions.

Given that the bot is configured in `messenger` [bridge mode](#bridge-mode) by default, you will need to log in to [messenger.com](https://messenger.com/) (not `facebook.com`!) and obtain the cookies from there as per [the bridge's authentication instructions](https://docs.mau.fi/bridges/go/meta/authentication.html).
