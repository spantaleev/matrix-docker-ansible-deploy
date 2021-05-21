# Setting up Heisenbridge (optional)

**Note**: bridging to [IRC](https://en.wikipedia.org/wiki/Internet_Relay_Chat) can also happen via the [matrix-appservice-irc](configuring-playbook-bridge-appservice-irc.md) bridge supported by the playbook.

The playbook can install and configure [Heisenbridge](https://github.com/hifi/heisenbridge) - the bouncer-style [IRC](https://en.wikipedia.org/wiki/Internet_Relay_Chat) bridge for you.

See the project's [README](https://github.com/hifi/heisenbridge/blob/master/README.md) to learn what it does and why it might be useful to you.

## Configuration

Below are the common configuration options that you may want to set, exhaustive list is in [the bridge's defaults var file](../roles/matrix-bridge-heisenbridge/defaults/main.yml).

At a minimum, you only need to enable the bridge to get it up and running (`inventory/host_vars/matrix.DOMAIN/vars.yml`):

```yaml
matrix_heisenbridge_enabled: true

# set owner (optional)
matrix_heisenbridge_owner: "@you:your-homeserver"

# to enable identd on host port 113/TCP (optional)
matrix_heisenbridge_identd_enabled: true
```

That's it! A registration file is automatically generated during the setup phase.

Setting the owner is optional as the first local user to DM `@heisenbridge:your-homeserver` will be made the owner.
If you are not using a local user you must set it as otherwise you can't DM it at all.

## Usage

After the bridge is successfully running just DM `@heisenbridge:your-homeserver` to start setting it up.
Help is available for all commands with the `-h` switch.
If the bridge ignores you and a DM is not accepted then the owner setting may be wrong.

If you encounter issues or feel lost you can join the project room at [#heisenbridge:vi.fi](https://matrix.to/#/#heisenbridge:vi.fi) for help.
