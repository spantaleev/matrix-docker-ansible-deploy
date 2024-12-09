# Setting up Appservice Webhooks bridging (optional, deprecated)

**Note**: This bridge has been deprecated. We recommend not bothering with installing it. While not a 1:1 replacement, the bridge's author suggests taking a look at [matrix-hookshot](https://github.com/matrix-org/matrix-hookshot) as a replacement, which can also be installed using [this playbook](configuring-playbook-bridge-hookshot.md). Consider using that bridge instead of this one.

The playbook can install and configure [matrix-appservice-webhooks](https://github.com/turt2live/matrix-appservice-webhooks) for you. This bridge provides support for Slack-compatible webhooks.

See the project's [documentation](https://github.com/turt2live/matrix-appservice-webhooks/blob/master/README.md) to learn what it does and why it might be useful to you.

## Adjusting the playbook configuration

To enable the bridge, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_appservice_webhooks_enabled: true
matrix_appservice_webhooks_api_secret: '<your_secret>'

# Uncomment to increase the verbosity of logging via `journalctl -fu matrix-appservice-webhooks.service`
# matrix_appservice_webhooks_log_level: 'verbose'

# As of Synapse 1.90.0, uncomment to enable the backwards compatibility (https://matrix-org.github.io/synapse/latest/upgrade#upgrading-to-v1900) that this bridge needs.
# Note: This deprecated method is considered insecure.
#
# matrix_synapse_configuration_extension_yaml: |
#   use_appservice_legacy_authorization: true
```

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

## Usage

To use the bridge, you need to invite the bridge bot user to your room in either way.

- Send `/invite @_webhook:example.com` (**Note**: Make sure you have administration permissions in your room)
- Add the bridge bot to a private channel (personal channels imply you being an administrator)

You then need to send a message to the bridge bot in order to receive a private message including the webhook link:

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
