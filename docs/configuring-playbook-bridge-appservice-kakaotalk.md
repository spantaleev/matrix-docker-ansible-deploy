# Setting up Appservice Kakaotalk bridging (optional)

The playbook can install and configure [matrix-appservice-kakaotalk](https://src.miscworks.net/fair/matrix-appservice-kakaotalk) for you, for bridging to [Kakaotalk](https://www.kakaocorp.com/page/service/service/KakaoTalk?lang=ENG). This bridge is based on [node-kakao](https://github.com/storycraft/node-kakao) (now unmaintained) and some [mautrix-facebook](https://github.com/mautrix/facebook) code.

See the project's [documentation](https://src.miscworks.net/fair/matrix-appservice-kakaotalk/src/branch/master/README.md) to learn what it does and why it might be useful to you.

⚠️ **Warning**: there have been recent reports (~2022-09-16) that **using this bridge may get your account banned**.

## Prerequisite (optional)

### Enable Shared Secret Auth

If you want to set up [Double Puppeting](https://docs.mau.fi/bridges/general/double-puppeting.html) (hint: you most likely do) for this bridge automatically, you need to have enabled [Shared Secret Auth](configuring-playbook-shared-secret-auth.md) for this playbook.

See [this section](configuring-playbook-bridge-mautrix-bridges.md#set-up-double-puppeting-optional) on the [common guide for configuring mautrix bridges](configuring-playbook-bridge-mautrix-bridges.md) for details about setting up Double Puppeting.

**Note**: double puppeting with the Shared Secret Auth works at the time of writing, but is deprecated and will stop working in the future.

## Adjusting the playbook configuration

To enable the bridge, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_appservice_kakaotalk_enabled: true
```

### Extending the configuration

There are some additional things you may wish to configure about the bridge.

Take a look at:

- `roles/custom/matrix-bridge-appservice-kakaotalk/defaults/main.yml` for some variables that you can customize via your `vars.yml` file
- `roles/custom/matrix-bridge-appservice-kakaotalk/templates/config.yaml.j2` for the bridge's default configuration. You can override settings (even those that don't have dedicated playbook variables) using the `matrix_appservice_kakaotalk_configuration_extension_yaml` variable

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

To use the bridge, you need to start a chat with `@kakaotalkbot:example.com` (where `example.com` is your base domain, not the `matrix.` domain).

You then need to send `login --save EMAIL_OR_PHONE_NUMBER` to the bridge bot to enable bridging for your Kakaotalk account. The `--save` flag may be omitted, if you'd rather not save your password.
