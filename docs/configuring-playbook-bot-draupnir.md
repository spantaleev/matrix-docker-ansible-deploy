# Setting up Draupnir (optional)

The playbook can install and configure the [Draupnir](https://github.com/the-draupnir-project/Draupnir) moderation bot for you.

See the project's [documentation](https://the-draupnir-project.github.io/draupnir-documentation/) to learn what it does and why it might be useful to you.

This documentation page is about installing Draupnir in bot mode. As an alternative, you can run a multi-instance Draupnir deployment by installing [Draupnir in appservice mode](./configuring-playbook-appservice-draupnir-for-all.md) (called Draupnir-for-all) instead.

If your migrating from Mjolnir skip to [this section](#migrating-from-mjolnir-only-required-if-migrating).

## Prerequisites

### Create a management room

Using your own account, create a new invite only room that you will use to manage the bot. This is the room where you will see the status of the bot and where you will send commands to the bot, such as the command to ban a user from another room. Anyone in this room can control the bot so it is important that you only invite trusted users to this room.

If you make the management room encrypted (E2EE), then you need to enable the native E2EE support (see [below](#native-e2ee-support)).

Once you have created the room you need to copy the room ID so you can tell the bot to use that room. In Element Web you can do this by going to the room's settings, clicking Advanced, and then copying the internal room ID. The room ID will look something like `!qporfwt:example.com`.

Finally invite the `@bot.draupnir:example.com` account that the playbook will create for you to the management room. Please note that clients can issue a warning that your attempting to invite a user that doesnt have a profile and might not exist. This warning is expected as your inviting the bot before its user account exists.

## End-to-End Encryption support

Decide whether you want to support having an Encrypted management room or not. Draupnir can still protect encrypted rooms without encryption support enabled.

Refer to Draupnir's [Documentation](https://the-draupnir-project.github.io/draupnir-documentation/moderator/managing-protected-rooms#protecting-encrypted-rooms) for more information on why you might or might not care about encryption support for protected rooms.

**Note**: Draupnir does not support running with Pantalaimon as it would break all workflows that involve answering prompts with reactions.

### Native E2EE support

To enable the native E2EE support, you need to obtain an access token for Draupnir.

Note that native E2EE requires a clean access token that has not touched E2EE so curl is recommended as a method to obtain it. **The access token obtained via Element Web does not work with it**. Refer to the documentation on [how to obtain an access token via curl](obtaining-access-tokens.md#obtain-an-access-token-via-curl).

To enable the native E2EE support, add the following configuration to your `vars.yml` file:

```yaml
# Enables the native E2EE Support
matrix_bot_draupnir_enable_experimental_rust_crypto: true

# Access Token the bot uses to login.
# Comment out `matrix_bot_draupnir_login_native` when using this option.
matrix_bot_draupnir_access_token: "ACCESS_TOKEN_HERE"
```

## Adjusting the playbook configuration

To enable the bot, add the following configuration to your `vars.yml` file. Make sure to replace `MANAGEMENT_ROOM_ID_HERE`.

```yaml
# Enable Draupnir
matrix_bot_draupnir_enabled: true

# Uncomment and adjust this part if you'd like to use a username different than the default
# matrix_bot_draupnir_login: bot.draupnir

# Generate a strong password for the bot. You can create one with a command like `pwgen -s 64 1`.
# If creating the user on your own and using `matrix_bot_draupnir_access_token` to login you can comment out this line.
matrix_bot_draupnir_password: PASSWORD_FOR_THE_BOT

# Comment out if using `matrix_bot_draupnir_enable_experimental_rust_crypto: true` or `matrix_bot_draupnir_access_token` to login.
matrix_bot_draupnir_login_native: true

matrix_bot_draupnir_management_room: "MANAGEMENT_ROOM_ID_HERE"
```

Before Proceeding run the playbook with the following command to make sure the Draupnir user has been created.
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,ensure-matrix-users-created
```

### Make sure the account is free from rate limiting

If your homeserver's implementation is Synapse, you will need to prevent it from rate limiting the bot's account. **This is a heavily recomended step. If you do not configure it, Draupnir performance will be degraded.**

This can be done using Synapse's [Admin APIs](https://element-hq.github.io/synapse/latest/admin_api/user_admin_api.html#override-ratelimiting-for-users). They can be accessed both externally and internally.

To expose the APIs publicly, add the following configuration to your `vars.yml` file:

```yaml
matrix_synapse_container_labels_public_client_synapse_admin_api_enabled: true
```

The APIs can also be accessed via [Synapse Admin](https://github.com/etkecc/synapse-admin), a web UI tool you can use to administrate users, rooms, media, etc. on your Matrix server. The playbook can install and configure Synapse Admin for you. For details about it, see [this page](configuring-playbook-synapse-admin.md).

**Note**: access to the APIs is restricted with a valid access token, so exposing them publicly should not be a real security concern. Still, doing so is not recommended for additional security. See [official Synapse reverse-proxying recommendations](https://element-hq.github.io/synapse/latest/reverse_proxy.html#synapse-administration-endpoints).

To discharge rate limiting, run the following command on systems that ship curl (note that it does not work on outdated Windows 10). Even if the APIs are not exposed to the internet, you should still be able to run the command on the homeserver locally. Before running it, make sure to replace `@bot.draupnir:example.com` with the MXID of your Draupnir:

```sh
curl --header "Authorization: Bearer <access_token>" -X POST https://matrix.example.com/_synapse/admin/v1/users/@bot.draupnir:example.com/override_ratelimit
```

### Obtain an access token

Manual access to Synapse's Admin API requires an access token. Refer to the documentation on [how to obtain an access token](obtaining-access-tokens.md).

⚠️ **Warning**: Access tokens are sensitive information. Do not include them in any bug reports, messages, or logs. Do not share the access token with anyone.

### Abuse Reports

Draupnir can receive reports in the management room.

The bot can intercept the report API endpoint of the client-server API, which requires integration with the reverse proxy in front of the homeserver. If you are using Traefik, this playbook can set this up for you:

```yaml
matrix_bot_draupnir_abuse_reporting_enabled: true
```

<!--
NOTE: this is unsupported by the playbook due to the admin API being inaccessible from containers currently.

The other method polls an Synapse Admin API endpoint, hence it is available only if using Synapse and if the Draupnir user is an admin (see [above](#register-the-bot-account)). To enable it, set `pollReports: true` on `vars.yml` file as below. 
-->

### Extending the configuration

You can configure additional options by adding the `matrix_bot_draupnir_configuration_extension_yaml` variable.

For example, to change Draupnir's `acceptInvitesFromSpace` option to `!qporfwt:example.com`, add the following configuration to your `vars.yml` file:

```yaml
matrix_bot_draupnir_configuration_extension_yaml: |
  # Your custom YAML configuration goes here.
  # This configuration extends the default starting configuration (`matrix_bot_draupnir_configuration_yaml`).
  #
  # You can override individual variables from the default configuration, or introduce new ones.
  #
  # If you need something more special, you can take full control by
  # completely redefining `matrix_bot_draupnir_configuration_yaml`.
  acceptInvitesFromSpace: "!qporfwt:example.com"
```

### Migrating from Mjolnir (Only required if migrating)

Replace your `matrix_bot_mjolnir` config with `matrix_bot_draupnir` config. Also disable Mjolnir if you're doing migration.

Note that Pantalaimon is unsupported by Draupnir so it is recommended to consult the instructions to enable [the native E2EE support](#native-e2ee-support).

That is all you need to do due to that Draupnir can complete migration on its own.

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

You can refer to the upstream [documentation](https://the-draupnir-project.github.io/draupnir-documentation/) for additional ways to use and configure Draupnir and for a more detailed usage guide.

Below is a **non-exhaustive quick-start guide** for the impatient.

### Making Draupnir join and protect a room

Draupnir can be told to self-join public rooms, but it's better to follow this flow which works well for all kinds of rooms:

1. Invite the bot to the room manually ([inviting Draupnir to rooms](https://the-draupnir-project.github.io/draupnir-documentation/moderator/managing-protected-rooms#inviting-draupnir-to-rooms)). Before joining, the bot *may* ask for confirmation in the Management Room

2. [Give the bot permissions to do its job](#giving-draupnir-permissions-to-do-its-job)

3. Tell it to protect the room (using the [rooms command](https://the-draupnir-project.github.io/draupnir-documentation/moderator/managing-protected-rooms#using-the-draupnir-rooms-command)) by sending the following command to the Management Room: `!draupnir rooms add !qporfwt:example.com`

To have Draupnir provide useful room protection, you need do to a bit more work (at least the first time around). You may wish to [Subscribe to a public policy list](#subscribing-to-a-public-policy-list), [Create your own own policy and rules](#creating-your-own-policy-lists-and-rules) and [Enabling built-in protections](#enabling-built-in-protections).

### Giving Draupnir permissions to do its job

For Draupnir to do its job, you need to [give it permissions](https://the-draupnir-project.github.io/draupnir-documentation/moderator/managing-protected-rooms#giving-draupnir-permissions) in rooms it's protecting. This involves **giving it an Administrator power level**.

**We recommend setting this power level as soon as the bot joins your room** (and before you create new rules), so that it can apply rules as soon as they are available. If the bot is under-privileged, it may fail to apply protections and may not retry for a while (or until your restart it).

### Subscribing to a public policy list

We recommend **subscribing to a public [policy list](https://the-draupnir-project.github.io/draupnir-documentation/concepts/policy-lists)** using the [watch command](https://the-draupnir-project.github.io/draupnir-documentation/moderator/managing-policy-lists#using-draupnirs-watch-command-to-subscribe-to-policy-rooms).

Polcy lists are maintained in Matrix rooms. A popular policy list is maintained in the public `#community-moderation-effort-bl:neko.dev` room.

You can tell Draupnir to subscribe to it by sending the following command to the Management Room: `!draupnir watch #community-moderation-effort-bl:neko.dev`

#### Creating your own policy lists and rules

We also recommend **creating your own policy lists** with the [list create](https://the-draupnir-project.github.io/draupnir-documentation/moderator/managing-policy-lists#using-draupnirs-list-create-command-to-create-a-policy-room) command.

You can do so by sending the following command to the Management Room: `!draupnir list create my-bans my-bans-bl`. This will create a policy list having a name (shortcode) of `my-bans` and stored in a public `#my-bans-bl:example.com` room on your server. As soon as you run this command, the bot will invite you to the policy list room.

A policy list does nothing by itself, so the next step is **adding some rules to your policy list**. Policies target a so-called `entity` (one of: `user`, `room` or `server`). These entities are mentioned on the [policy lists](https://the-draupnir-project.github.io/draupnir-documentation/concepts/policy-lists) documentation page and in the Matrix Spec [here](https://spec.matrix.org/v1.11/client-server-api/#mban-recommendation).

The simplest and most useful entity to target is `user`. Below are a few examples using the [ban command](https://the-draupnir-project.github.io/draupnir-documentation/moderator/managing-users#the-ban-command) and targeting users.

To create rules, you run commands in the Management Room (**not** in the policy list room).

- (ban a single user on a given homeserver): `!draupnir ban @charles:example.com my-bans Rude to others`
- (ban all users on a given homeserver by using a [wildcard](https://the-draupnir-project.github.io/draupnir-documentation/moderator/managing-users#wildcards)): `!draupnir ban @*:example.org my-bans Spam server - all users are fake`

As a result of running these commands, you may observe:

- Draupnir creating `m.policy.rule.user` state events in the `#my-bans-bl:example.com` room on your server
- applying these rules against all rooms that Draupnir is an Administrator in

You can undo bans with the [unban command](https://the-draupnir-project.github.io/draupnir-documentation/moderator/managing-users#the-unban-command).

### Enabling built-in protections

You can also **turn on various built-in [protections](https://the-draupnir-project.github.io/draupnir-documentation/protections)** like `JoinWaveShortCircuit` ("If X amount of users join in Y time, set the room to invite-only").

To **see which protections are available and which are enabled**, send a `!draupnir protections` command to the Management Room.

To **see the configuration options for a given protection**, send a `!draupnir protections show PROTECTION_NAME` (e.g. `!draupnir protections show JoinWaveShortCircuit`).

To **set a specific option for a given protection**, send a command like this: `!draupnir config set PROTECTION_NAME.OPTION VALUE` (e.g. `!draupnir config set JoinWaveShortCircuit.timescaleMinutes 30`).

To **enable a given protection**, send a command like this: `!draupnir enable PROTECTION_NAME` (e.g. `!draupnir enable JoinWaveShortCircuit`).

To **disable a given protection**, send a command like this: `!draupnir disable PROTECTION_NAME` (e.g. `!draupnir disable JoinWaveShortCircuit`).
