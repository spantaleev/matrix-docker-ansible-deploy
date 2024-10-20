# Setting up Heisenbridge (optional)

**Note**: bridging to [IRC](https://en.wikipedia.org/wiki/Internet_Relay_Chat) can also happen via the [matrix-appservice-irc](configuring-playbook-bridge-appservice-irc.md) bridge supported by the playbook.

The playbook can install and configure [Heisenbridge](https://github.com/hifi/heisenbridge) - the bouncer-style [IRC](https://en.wikipedia.org/wiki/Internet_Relay_Chat) bridge for you.

See the project's [README](https://github.com/hifi/heisenbridge/blob/master/README.md) to learn what it does and why it might be useful to you. You can also take a look at [this demonstration video](https://www.youtube.com/watch?v=nQk1Bp4tk4I).

## Configuration

To enable Heisenbridge, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_heisenbridge_enabled: true

# Setting the owner is optional as the first local user to DM `@heisenbridge:your-homeserver` will be made the owner.
# If you are not using a local user you must set it as otherwise you can't DM it at all.
matrix_heisenbridge_owner: "@you:your-homeserver"

# Uncomment to enable identd on host port 113/TCP (optional)
# matrix_heisenbridge_identd_enabled: true
```

For a more complete list of variables that you could override, see the [`defaults/main.yml` file](../roles/custom/matrix-bridge-heisenbridge/defaults/main.yml) of the Heisenbridge Ansible role.

### Adjusting the Heisenbridge URL

By default, this playbook installs Heisenbridge on the `matrix.` subdomain, at the `/heisenbridge` path (https://matrix.example.com/heisenbridge). It would handle media requests there (see the [release notes for Heisenbridge v1.15.0](https://github.com/hifi/heisenbridge/releases/tag/v1.15.0)).

This makes it easy to install it, because it **doesn't require additional DNS records to be set up**. If that's okay, you can skip this section.

By tweaking the `matrix_heisenbridge_hostname` and `matrix_heisenbridge_path_prefix` variables, you can easily make the service available at a **different hostname and/or path** than the default one.

Example additional configuration for your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
# Change the default hostname and path prefix
matrix_heisenbridge_hostname: heisenbridge.example.com
matrix_heisenbridge_path_prefix: /
```

## Adjusting DNS records

If you've changed the default hostname, **you may need to adjust your DNS** records to point the Heisenbridge domain to the Matrix server.

See [Configuring DNS](configuring-dns.md) for details about DNS changes.

If you've decided to use the default hostname, you won't need to do any extra DNS configuration.

## Installing

After configuring the playbook, run the [installation](installing.md) command: `just install-all` or `just setup-all`

## Usage

After the bridge is successfully running just DM `@heisenbridge:your-homeserver` to start setting it up.
Help is available for all commands with the `-h` switch.
If the bridge ignores you and a DM is not accepted then the owner setting may be wrong.

You can also learn the basics by watching [this demonstration video](https://www.youtube.com/watch?v=nQk1Bp4tk4I).

If you encounter issues or feel lost you can join the project room at [#heisenbridge:vi.fi](https://matrix.to/#/#heisenbridge:vi.fi) for help.
