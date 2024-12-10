# Setting up Beeper Linkedin bridging (optional)

The playbook can install and configure [beeper-linkedin](https://github.com/beeper/linkedin) for you, for bridging to [LinkedIn](https://www.linkedin.com/) Messaging. This bridge is based on the mautrix-python framework and can be configured in a similar way to the other mautrix bridges

See the project's [documentation](https://github.com/beeper/linkedin/blob/master/README.md) to learn what it does and why it might be useful to you.

## Adjusting the playbook configuration

To enable the bridge, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_beeper_linkedin_enabled: true
```

There are some additional things you may wish to configure about the bridge before you continue.

Encryption support is off by default. If you would like to enable encryption, add the following to your `vars.yml` file:

```yaml
matrix_beeper_linkedin_bridge_encryption_allow: true
matrix_beeper_linkedin_bridge_encryption_default: true
```

If you would like to be able to administrate the bridge from your account it can be configured like this:

```yaml
matrix_beeper_linkedin_configuration_extension_yaml: |
  bridge:
    permissions:
      '@alice:{{ matrix_domain }}': admin
```

You may wish to look at `roles/custom/matrix-bridge-beeper-linkedin/templates/config.yaml.j2` to find other things you would like to configure.

## Installing

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,ensure-matrix-users-created,start
```

**Notes**:

- The `ensure-matrix-users-created` playbook tag makes the playbook automatically create the bot's user account.

- The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

  `just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed.

## Set up Double Puppeting by enabling Appservice Double Puppet or Shared Secret Auth

The bridge automatically performs Double Puppeting if [Appservice Double Puppet](configuring-playbook-appservice-double-puppet.md) or [Shared Secret Auth](configuring-playbook-shared-secret-auth.md) service is configured and enabled on the server for this playbook.

Enabling [Appservice Double Puppet](configuring-playbook-appservice-double-puppet.md) is the recommended way of setting up Double Puppeting, as it's easier to accomplish, works for all your users automatically, and has less of a chance of breaking in the future.

Enabling double puppeting by enabling the [Shared Secret Auth](configuring-playbook-shared-secret-auth.md) service works at the time of writing, but is deprecated and will stop working in the future.

## Usage

To use the bridge, you need to start a chat with `@linkedinbot:example.com` (where `example.com` is your base domain, not the `matrix.` domain).

Send `login YOUR_LINKEDIN_EMAIL_ADDRESS` to the bridge bot to enable bridging for your LinkedIn account.

If you run into trouble, check the [Troubleshooting](#troubleshooting) section below.

After successfully enabling bridging, you may wish to [set up Double Puppeting](#set-up-double-puppeting-by-enabling-appservice-double-puppet-or-shared-secret-auth), if you haven't already done so.

## Troubleshooting

### Bridge asking for 2FA even if you don't have 2FA enabled

If you don't have 2FA enabled and are logging in from a strange IP for the first time, LinkedIn will send an email with a one-time code. You can use this code to authorize the bridge session. In my experience, once the IP is authorized, you will not be asked again.
