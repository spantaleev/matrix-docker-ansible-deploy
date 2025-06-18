<!--
SPDX-FileCopyrightText: 2020 - 2023 MDAD project contributors
SPDX-FileCopyrightText: 2020 Björn Marten
SPDX-FileCopyrightText: 2020 Slavi Pantaleev
SPDX-FileCopyrightText: 2020 iLyas Bakouch
SPDX-FileCopyrightText: 2022 Kim Brose
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up Appservice Webhooks bridging (optional, deprecated)

**Note**: This bridge has been deprecated. We recommend not bothering with installing it. While not a 1:1 replacement, the bridge's author suggests taking a look at [matrix-hookshot](https://github.com/matrix-org/matrix-hookshot) as a replacement, which can also be [installed using this playbook](configuring-playbook-bridge-hookshot.md). Consider using that bridge instead of this one.

The playbook can install and configure [matrix-appservice-webhooks](https://github.com/turt2live/matrix-appservice-webhooks) for you. This bridge provides support for Slack-compatible webhooks.

See the project's [documentation](https://github.com/turt2live/matrix-appservice-webhooks/blob/master/README.md) to learn what it does and why it might be useful to you.

## Adjusting the playbook configuration

To enable the bridge, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_appservice_webhooks_enabled: true
matrix_appservice_webhooks_api_secret: '<your_secret>'

# As of Synapse 1.90.0, uncomment to enable the backwards compatibility (https://matrix-org.github.io/synapse/latest/upgrade#upgrading-to-v1900) that this bridge needs.
# Note: This deprecated method is considered insecure.
#
# matrix_synapse_configuration_extension_yaml: |
#   use_appservice_legacy_authorization: true
```

### Extending the configuration

There are some additional things you may wish to configure about the bridge.

Take a look at:

- `roles/custom/matrix-bridge-appservice-webhooks/defaults/main.yml` for some variables that you can customize via your `vars.yml` file
- `roles/custom/matrix-bridge-appservice-webhooks/templates/config.yaml.j2` for the bridge's default configuration. You can override settings (even those that don't have dedicated playbook variables) using the `matrix_appservice_webhooks_configuration_extension_yaml` variable

## Installing

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

## Usage

To use the bridge, you need to invite the bridge bot user to your room in either way.

- Send `/invite @_webhook:example.com` (**Note**: Make sure you have administration permissions in your room)
- Add the bridge bot to a private channel (personal channels imply you being an administrator)

You then need to send a message to the bridge bot to receive a private message including the webhook link:

```
!webhook
```

The JSON body for posting messages will have to look like this:

```json
{
    "text": "Hello world!",
    "format": "plain",
    "displayName": "My Cool Webhook",
    "avatar_url": "http://i.imgur.com/IDOBtEJ.png"
}
```

You can test this via curl like so:

```sh
curl --header "Content-Type: application/json" \
--data '{
"text": "Hello world!",
"format": "plain",
"displayName": "My Cool Webhook",
"avatar_url": "http://i.imgur.com/IDOBtEJ.png"
}' \
<the webhook link you've gotten from the bridge bot>
```

### Setting Webhooks with Dimension integration manager

If you're using the [Dimension integration manager](configuring-playbook-dimension.md), you can configure the Webhooks bridge with it.

To configure it, open the Dimension integration manager, and go to "Settings" and "Bridges", then select edit action for "Webhook Bridge".

On the UI, press "Add self-hosted Bridge" button and populate "Provisioning URL"  and "Shared Secret" values from `/matrix/appservice-webhooks/config/config.yaml` file's homeserver URL value and provisioning secret value, respectively.

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-appservice-webhooks`.

### Increase logging verbosity

The default logging level for this component is `info`. If you want to increase the verbosity, add the following configuration to your `vars.yml` file and re-run the playbook:

```yaml
# Valid values: info, verbose
matrix_appservice_webhooks_log_level: 'verbose'
```
