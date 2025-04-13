<!--
SPDX-FileCopyrightText: 2021 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2021 Alexandar Mechev
SPDX-FileCopyrightText: 2022 Cody Wyatt Neiman
SPDX-FileCopyrightText: 2023 Kuba Orlik
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up Beeper Linkedin bridging (optional)

The playbook can install and configure [beeper-linkedin](https://github.com/beeper/linkedin) for you, for bridging to [LinkedIn](https://www.linkedin.com/) Messaging. This bridge is based on the mautrix-python framework and can be configured in a similar way to the mautrix bridges.

See the project's [documentation](https://github.com/beeper/linkedin/blob/master/README.md) to learn what it does and why it might be useful to you.

## Prerequisite

### Enable Appservice Double Puppet or Shared Secret Auth (optional)

If you want to set up [Double Puppeting](https://docs.mau.fi/bridges/general/double-puppeting.html) (hint: you most likely do) for this bridge automatically, you need to have enabled [Appservice Double Puppet](configuring-playbook-appservice-double-puppet.md) or [Shared Secret Auth](configuring-playbook-shared-secret-auth.md) service for this playbook.

See [this section](configuring-playbook-bridge-mautrix-bridges.md#set-up-double-puppeting-optional) on the [common guide for configuring mautrix bridges](configuring-playbook-bridge-mautrix-bridges.md) for details about setting up Double Puppeting.

**Note**: double puppeting with the Shared Secret Auth works at the time of writing, but is deprecated and will stop working in the future.

## Adjusting the playbook configuration

To enable the bridge, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_beeper_linkedin_enabled: true
```

### Extending the configuration

There are some additional things you may wish to configure about the bridge.

See [this section](configuring-playbook-bridge-mautrix-bridges.md#extending-the-configuration) on the [common guide for configuring mautrix bridges](configuring-playbook-bridge-mautrix-bridges.md) for details about variables that you can customize and the bridge's default configuration, including [bridge permissions](configuring-playbook-bridge-mautrix-bridges.md#configure-bridge-permissions-optional), [encryption support](configuring-playbook-bridge-mautrix-bridges.md#enable-encryption-optional), [relay mode](configuring-playbook-bridge-mautrix-bridges.md#enable-relay-mode-optional), [bot's username](configuring-playbook-bridge-mautrix-bridges.md#set-the-bots-username-optional), etc.

**Note**: when following the guide to configure the bridge, make sure to replace `_mautrix_SERVICENAME_` in the variable names with `_beeper_linkedin_`.

## Installing

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

## Usage

To use the bridge, you need to start a chat with `@linkedinbot:example.com` (where `example.com` is your base domain, not the `matrix.` domain).

You then need to send `login YOUR_LINKEDIN_EMAIL_ADDRESS` to the bridge bot to enable bridging for your LinkedIn account.

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-beeper-linkedin`.

### Increase logging verbosity

The default logging level for this component is `WARNING`. If you want to increase the verbosity, add the following configuration to your `vars.yml` file and re-run the playbook:

```yaml
matrix_beeper_linkedin_logging_level: DEBUG
```

### Bridge asking for 2FA even if you don't have 2FA enabled

If you don't have 2FA enabled and are logging in from a strange IP for the first time, LinkedIn will send an email with a one-time code. You can use this code to authorize the bridge session. In my experience, once the IP is authorized, you will not be asked again.
