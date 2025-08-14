<!--
SPDX-FileCopyrightText: 2023 - 2025 MDAD project contributors
SPDX-FileCopyrightText: 2023 Kim Brose
SPDX-FileCopyrightText: 2024 - 2025 Slavi Pantaleev
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up Draupnir (optional)

The playbook can install and configure the [Draupnir](https://github.com/the-draupnir-project/Draupnir) moderation bot for you.

See the project's [documentation](https://the-draupnir-project.github.io/draupnir-documentation/) to learn what it does and why it might be useful to you.

This documentation page is about installing Draupnir in bot mode. As an alternative, you can run a multi-instance Draupnir deployment by installing [Draupnir in appservice mode](./configuring-playbook-appservice-draupnir-for-all.md) (called Draupnir-for-all) instead.

If your migrating from [Mjolnir](configuring-playbook-bot-mjolnir.md), skip to [this section](#migrating-from-mjolnir-only-required-if-migrating).

## Prerequisites

### Create a management room

Using your own account, create a new invite only room that you will use to manage the bot. This is the room where you will see the status of the bot and where you will send commands to the bot, such as the command to ban a user from another room.

> [!WARNING]
> Anyone in this room can control the bot so it is important that you only invite trusted users to this room.

It is possible to make the management room encrypted (E2EE). If doing so, then you need to enable the native E2EE support (see [below](#native-e2ee-support)).

Once you have created the room you need to copy the room ID so you can specify it on your `inventory/host_vars/matrix.example.com/vars.yml` file. In Element Web you can check the ID by going to the room's settings and clicking "Advanced". The room ID will look something like `!qporfwt:example.com`.

## End-to-End Encryption support

Decide whether you want to support having an encrypted management room or not. Draupnir can still protect encrypted rooms without encryption support enabled.

Refer to Draupnir's [documentation](https://the-draupnir-project.github.io/draupnir-documentation/moderator/managing-protected-rooms#protecting-encrypted-rooms) for more details about why you might want to care about encryption support for protected rooms.

### Disable Pantalaimon for Draupnir (since v2.0.0; optional)

It is known that running Draupnir along with Pantalaimon breaks all workflows that involve answering prompts with reactions.

If you are updating Draupnir from v1.x.x and have enabled Pantalaimon for it, you can disable Pantalaimon in favor of the native E2EE support. To disable Pantalaimon, remove the configuration `matrix_bot_draupnir_pantalaimon_use: true` from your `vars.yml` file.

**Note**: because the management room is still encrypted, disabling it without enabling the native E2EE support will break the management room.

### Native E2EE support

To enable the native E2EE support, you need to obtain an access token for Draupnir and set it on your `vars.yml` file.

Note that native E2EE requires a clean access token that has not touched E2EE so curl is recommended as a method to obtain it. **The access token obtained via Element Web does not work with it**. Refer to the documentation on [how to obtain an access token via curl](obtaining-access-tokens.md#obtain-an-access-token-via-curl).

To enable the native E2EE support, add the following configuration to your `vars.yml` file. Make sure to replace `CLEAN_ACCESS_TOKEN_HERE` with the access token you obtained just now.

```yaml
# Enables the native E2EE support
matrix_bot_draupnir_config_experimentalRustCrypto: true

# Access token which the bot will use for logging in.
# Comment out `matrix_bot_draupnir_login_native` when using this option.
matrix_bot_draupnir_config_accessToken: "CLEAN_ACCESS_TOKEN_HERE"
```

## Adjusting the playbook configuration

To enable the bot, add the following configuration to your `vars.yml` file. Make sure to replace `MANAGEMENT_ROOM_ID_HERE` with the one of the room which you have created earlier.

```yaml
# Enable Draupnir
matrix_bot_draupnir_enabled: true

# Uncomment and adjust this part if you'd like to use a username different than the default
# matrix_bot_draupnir_login: bot.draupnir

# Generate a strong password for the bot. You can create one with a command like `pwgen -s 64 1`.
# If creating the user on your own and using `matrix_bot_draupnir_config_accessToken` to login you can comment out this line.
matrix_bot_draupnir_password: PASSWORD_FOR_THE_BOT

# Comment out if using `matrix_bot_draupnir_config_experimentalRustCrypto: true` or `matrix_bot_draupnir_config_accessToken` to login.
matrix_bot_draupnir_login_native: true

matrix_bot_draupnir_config_managementRoom: "MANAGEMENT_ROOM_ID_HERE"
```

### Create and invite the bot to the management room

Before proceeding to the next step, run the playbook with the following command to create the bot user.

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,ensure-matrix-users-created
```

**Note**: the `ensure-matrix-users-created` playbook tag makes the playbook automatically create the bot's user account.

Then, invite the bot (`@bot.draupnir:example.com`) to its management room which you have created earlier.

### Make sure the account is free from rate limiting (optional, recommended)

If your homeserver's implementation is Synapse, you will need to prevent it from rate limiting the bot's account. **This is a highly recommended step. If you do not configure it, Draupnir performance will be degraded.**

This can be done using Synapse's [Admin APIs](https://element-hq.github.io/synapse/latest/admin_api/user_admin_api.html#override-ratelimiting-for-users). They can be accessed both externally and internally.

**Note**: access to the APIs is restricted with a valid access token, so exposing them publicly should not be a real security concern. Still, doing so is not recommended for additional security. See [official Synapse reverse-proxying recommendations](https://element-hq.github.io/synapse/latest/reverse_proxy.html#synapse-administration-endpoints).

The APIs can also be accessed via [Synapse Admin](https://github.com/etkecc/synapse-admin), a web UI tool you can use to administrate users, rooms, media, etc. on your Matrix server. The playbook can install and configure Synapse Admin for you. For details about it, see [this page](configuring-playbook-synapse-admin.md).

#### Add the configuration

To expose the APIs publicly, add the following configuration to your `vars.yml` file:

```yaml
matrix_synapse_container_labels_public_client_synapse_admin_api_enabled: true
```

#### Obtain an access token for admin account

Manual access to Synapse's Admin APIs requires an access token for a homeserver admin account. Refer to the documentation on [how to obtain an access token](obtaining-access-tokens.md).

> [!WARNING]
> Access tokens are sensitive information. Do not include them in any bug reports, messages, or logs. Do not share the access token with anyone.

#### Run the `curl` command

To disable rate limiting, run the following command on systems that ship curl. Before running it, make sure to replace:

- `ADMIN_ACCESS_TOKEN_HERE` with the access token of the admin account
- `example.com` with your base domain
- `@bot.draupnir:example.com` with the MXID of your Draupnir bot user

```sh
curl --header "Authorization: Bearer ADMIN_ACCESS_TOKEN_HERE" -X POST https://matrix.example.com/_synapse/admin/v1/users/@bot.draupnir:example.com/override_ratelimit
```

**Notes**:
- This does not work on outdated Windows 10 as curl is not available there.
- Even if the APIs are not exposed to the internet, you should still be able to run the command on the homeserver locally.

### Abuse Reports

Draupnir can receive reports in the management room.

The bot can intercept the report API endpoint of the client-server API, which requires integration with the reverse proxy in front of the homeserver. If you are using Traefik, this playbook can set this up for you:

```yaml
matrix_bot_draupnir_config_web_abuseReporting: true
```

### Enabling synapse-http-antispam support

Certain protections in Draupnir require the [synapse-http-antispam](https://github.com/maunium/synapse-http-antispam) module and a Synapse homeserver plus homeserver admin status to function. This module can be enabled in the playbook via setting `matrix_bot_draupnir_config_web_synapseHTTPAntispam_enabled` to `true` and making sure that Draupnir admin API access is enabled.

```yaml
# Enables the integration between Draupnir and synapse-http-antispam module.
matrix_bot_draupnir_config_web_synapseHTTPAntispam_enabled: true

# Enables draupnir to access Synapse admin APIs. This is required for the module functionality to take full effect.
matrix_bot_draupnir_admin_api_enabled: true
```

These protections need to be manually activated and consulting the [enabling protections](#enabling-built-in-protections) guide can be helpful or consulting upstream documentation.

<!--
NOTE: this is unsupported by the playbook due to the admin API being inaccessible from containers currently.

The other method polls an Synapse Admin API endpoint, hence it is available only if using Synapse and if the Draupnir user is an admin (see [above](#register-the-bot-account)). To enable it, set `pollReports: true` on `vars.yml` file as below.
-->

### Extending the configuration

There are some additional things you may wish to configure about the bot.

Take a look at:

- `roles/custom/matrix-bot-draupnir/defaults/main.yml` for some variables that you can customize via your `vars.yml` file. You can override settings (even those that don't have dedicated playbook variables) using the `matrix_bot_draupnir_configuration_extension_yaml` variable

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

Note that Draupnir supports E2EE natively, so you can enable it instead of Pantalaimon. It is recommended to consult the instruction [here](#native-e2ee-support).

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

- If you change the bot password (`matrix_bot_draupnir_password` in your `vars.yml` file) subsequently, the bot user's credentials on the homeserver won't be updated automatically. If you'd like to change the bot user's password, use a tool like [synapse-admin](configuring-playbook-synapse-admin.md) to change it, and then update `matrix_bot_draupnir_password` to let the bot know its new password.

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

Policy lists are maintained in Matrix rooms. Popular ones maintained in the public are:

- `#community-moderation-effort-bl:neko.dev`
- `#huginn-muninn-active-threats:feline.support`

You can tell Draupnir to subscribe to each of these by sending the following command to the Management Room: `!draupnir watch POLICY_LIST_ADDRESS_HERE` (e.g. `!draupnir watch #community-moderation-effort-bl:neko.dev`)

#### Creating your own policy lists and rules

We also recommend **creating your own policy lists** with the [list create](https://the-draupnir-project.github.io/draupnir-documentation/moderator/managing-policy-lists#using-draupnirs-list-create-command-to-create-a-policy-room) command.

You can do so by sending the following command to the Management Room: `!draupnir list create my-bans my-bans-bl`. This will create a policy list having a name (shortcode) of `my-bans` and stored in a public `#my-bans-bl:example.com` room on your server. As soon as you run this command, the bot will invite you to the policy list room.

A policy list does nothing by itself, so the next step is **adding some rules to your policy list**. Policies target a so-called `entity` (one of: `user`, `room` or `server`). These entities are mentioned on the [policy lists](https://the-draupnir-project.github.io/draupnir-documentation/concepts/policy-lists) documentation page and in the Matrix Spec [here](https://spec.matrix.org/v1.11/client-server-api/#mban-recommendation).

The simplest and most useful entity to target is `user`. Below are a few examples using the [ban command](https://the-draupnir-project.github.io/draupnir-documentation/moderator/managing-users#the-ban-command) and targeting users.

To create rules, you run commands in the Management Room (**not** in the policy list room).

- (ban a single user on a given homeserver): `!draupnir ban @charles:example.com my-bans Rude to others`
- (ban all users on a given homeserver by using a [wildcard](https://the-draupnir-project.github.io/draupnir-documentation/moderator/managing-users#wildcards)): `!draupnir ban @*:example.org my-bans Spam server, all users are fake`

As a result of running these commands, you may observe:

- Draupnir creating `m.policy.rule.user` state events in the `#my-bans-bl:example.com` room on your server
- applying these rules against all rooms that Draupnir is an Administrator in

You can undo bans with the [unban command](https://the-draupnir-project.github.io/draupnir-documentation/moderator/managing-users#the-unban-command).

### Enabling built-in protections

You can also **turn on various built-in [protections](https://the-draupnir-project.github.io/draupnir-documentation/protections)** like `JoinWaveShortCircuitProtection` ("If X amount of users join in Y time, set the room to invite-only").

To **see which protections are available and which are enabled**, send a `!draupnir protections` command to the Management Room.

To [**see the configuration options for a given protection**](https://the-draupnir-project.github.io/draupnir-documentation/protections/configuring-protections#displaying-the-protection-settings), send a `!draupnir protections show PROTECTION_NAME` (e.g. `!draupnir protections show JoinWaveShortCircuitProtection`).

To [**set a specific option for a given protection**](https://the-draupnir-project.github.io/draupnir-documentation/protections/configuring-protections#changing-protection-settings), send a command like this: `!draupnir protections config set PROTECTION_NAME OPTION VALUE` (e.g. `!draupnir protections config set JoinWaveShortCircuitProtection timescaleMinutes 30`).

To [**enable a given protection**](https://the-draupnir-project.github.io/draupnir-documentation/protections/block-invitations-on-server-protection#enabling-the-protection), send a command like this: `!draupnir protections enable PROTECTION_NAME` (e.g. `!draupnir protections enable JoinWaveShortCircuitProtection`).

To **disable a given protection**, send a command like this: `!draupnir protections disable PROTECTION_NAME` (e.g. `!draupnir protections disable JoinWaveShortCircuitProtection`).
