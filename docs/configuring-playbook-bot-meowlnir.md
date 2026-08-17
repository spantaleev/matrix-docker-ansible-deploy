<!--
SPDX-FileCopyrightText: 2026 Slavi Pantaleev

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up Meowlnir (optional)

The playbook can install and configure the [Meowlnir](https://github.com/maunium/meowlnir) moderation bot for you.

See the project's [documentation](https://docs.mau.fi/meowlnir/) to learn what it does and why it might be useful to you.

Meowlnir is an alternative to [Draupnir](configuring-playbook-bot-draupnir.md) and [Mjolnir](configuring-playbook-bot-mjolnir.md). It speaks the same [policy list](https://the-draupnir-project.github.io/draupnir-documentation/concepts/policy-lists) protocol, so it can subscribe to the same community ban lists, but it differs from them in a few ways that may matter to you:

- It runs as an **appservice** and hosts **multiple bots**, each with its own management room. They live in Meowlnir's database, not its configuration file, but you still [declare them in your `vars.yml` file](#declaring-bots).
- It can **override a policy coming from a list you do not control**, via unban policies combined with the ordering of your watched lists. See [Overriding a policy from someone else's list](#overriding-a-policy-from-someone-elses-list).
- It is written in Go and is optimized for Synapse, using its database and admin APIs directly.

Meowlnir and Draupnir can run side by side, but not usefully in the *same* room: whichever bot you are migrating away from still watches the same community lists, so it re-applies the very bans your unban policies remove. Migrate room by room. See [Trialling Meowlnir alongside another bot](#trialling-meowlnir-alongside-another-bot).

## Prerequisites

### Postgres

Meowlnir stores its state in a Postgres database. The playbook creates one for you automatically when using the integrated Postgres server.

### Adjusting DNS records

**No DNS changes are necessary.** Meowlnir is reached by the homeserver over the container network, and the paths it optionally serves publicly (abuse reports and the policy server) are routed on your existing `matrix.example.com` domain.

## Adjusting the playbook configuration

To enable Meowlnir, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_bot_meowlnir_enabled: true
```

### Declaring bots

That gets the service running, but Meowlnir does nothing until it has at least one bot. Declare the ones you want and the playbook creates them for you:

```yaml
matrix_bot_meowlnir_bots_custom:
  - username: meowlnir_bot
    displayname: Meowlnir
    avatar_url: ""
    management_room_auto_create: true
    management_rooms: []
    # Left out, the initial managers default to `matrix_bot_meowlnir_initial_managers`,
    # which is defined in terms of `matrix_admin`.
    # Uncomment to override that for this bot, or if neither variable is set.
    # initial_managers:
    #   - "@alice:example.com"
    #   - "@bob:example.com"
```

| Field | Required | Notes |
|---|---|---|
| `username` | yes | The localpart of the bot's Matrix user. Awkward to change later, so choose it carefully. |
| `displayname` | yes | The name shown in rooms. Safe to change at any time. |
| `avatar_url` | yes | An `mxc://` URI, or `""` for no avatar. |
| `management_room_auto_create` | yes | Whether the playbook creates the bot's management room. Mutually exclusive with a non-empty `management_rooms`. |
| `management_rooms` | yes | Rooms you have created yourself, `[]` when auto-creating. See [Supplying your own management room](#supplying-your-own-management-room). |
| `initial_managers` | no | Who to invite to an auto-created room. Defaults to the instance-wide list below. |

Usernames have to start with `meowlnir_` (the value of `matrix_bot_meowlnir_user_prefix`), so that bots fall inside the user namespace the homeserver lets Meowlnir operate.

Changing `displayname` or `avatar_url` and re-running updates the bot in place. The comparison is against Meowlnir's own record, so profile edits made directly from a Matrix client are not reverted.

#### Initial managers

With `management_room_auto_create: true`, the playbook creates each bot's management room and invites its initial managers to it. You only need to accept the room invitation.

`matrix_admin` is a single playbook variable which affects all bridges and bots, so setting it is usually a better move than setting anything specific to this role — **if it is already configured in your `vars.yml` file, there is nothing to do here**. If neither `matrix_admin` nor `matrix_bot_meowlnir_initial_managers` are set, the playbook would tell you about it.

A per-bot `initial_managers` replaces the instance-wide list. Declaring it empty means nobody, which fails the run for a bot relying on `management_room_auto_create`.

The list is consulted only while the room is being created. Adding a name to it later invites nobody, because the room already exists — invite and promote further moderators from inside the room instead, as described in [Who can command a bot](#who-can-command-a-bot).

#### Rooms the playbook creates

The bot creates the room with the `trusted_private_chat` preset, which gives every invitee the standing to command it. This is an additional room creator on room versions supporting [MSC4289](https://github.com/matrix-org/matrix-spec-proposals/pull/4289) (like v12) and power level 100 on older room versions. Creator status cannot be revoked subsequently.

The room's encryption follows `matrix_bot_meowlnir_config_encryption_enable`, and its name and topic come from `matrix_bot_meowlnir_management_room_name` and `matrix_bot_meowlnir_management_room_topic`.

### Supplying your own management room

If you would rather own the room outright, create it yourself and declare it instead. The bot is then merely an administrator in a room you created:

```yaml
matrix_bot_meowlnir_bots_custom:
  - username: meowlnir_bot
    displayname: Meowlnir
    avatar_url: ""
    management_room_auto_create: false
    management_rooms:
      - id: "!qporfwt:example.com"
        encrypted: false
```

An empty, invite-only room is fine. The order matters, because **each step depends on the one before it**:

1. Declare the room and run the playbook. Do not invite the bot beforehand.
2. The playbook creates the bot and tells Meowlnir about the room. Meowlnir would try to join right away, but will fail for invite-only rooms (a harmless error in the log).
3. Invite the bot. It accepts the invitation, because the room is already marked as a management room for it.
4. Give it power level 50 or more (ideally 100), so that it can store its protected rooms and watched lists there.

Meowlnir supports several management rooms per bot, and `encrypted` is set per room. Marking a room encrypted only means something when [End-to-End Encryption support](#end-to-end-encryption-support) is switched on, which it is not by default.

### Who can command a bot

**Management room membership alone is not enough**, which is different from what [Draupnir](configuring-playbook-bot-draupnir.md) does, where everyone in the management room can issue commands.

Meowlnir decides who may drive a bot from power levels in its management room: anyone who can send the `fi.mau.meowlnir.watched_lists` state event (power level 50 by default), plus the room's creators.

### Bots which are no longer declared

The bot list (`matrix_bot_meowlnir_bots_custom`) is authoritative. Removing entries from there will make the playbook unregister them with the Meowlnir instance.

Removal only adjusts Meowlnir's own records. A removed bot's Matrix user remains activated and stays in the rooms it had joined. A removed management room leaves the room and the bot's membership in it intact - it's just that Meowlnir stops taking commands there.

Removal happens under the same `ensure-matrix-users-created` tag that creates bots. It's one Ansible tag for "synchronizing the bots state" (creation, changes, and removal).

To turn removal off entirely, set `matrix_bot_meowlnir_bots_pruning_enabled: false`. As a safety measure, the playbook refuses to prune when *no* bots are declared at all; override that with `matrix_bot_meowlnir_bots_pruning_on_empty_roster_enabled: true`.

### Trialling Meowlnir alongside another bot

Meowlnir has a dry-run mode in which it does everything except take moderation actions:

```yaml
matrix_bot_meowlnir_config_meowlnir_dry_run: true
```

> [!WARNING]
> Dry run does not cover the [synapse-http-antispam](#enabling-synapse-http-antispam-support) integration. It suppresses actions Meowlnir takes itself (bans, server ACLs, rejecting pending invites), but the verdicts it hands back to Synapse still block invites and joins. Leave that integration off while trialling.

Do not expect dry run to preview what Meowlnir would do in rooms another policy-list bot already moderates. Meowlnir only acts on users who are *in* a room, and the other bot has already removed everyone its lists match, so the preview comes out empty. Dry run also skips the power level check described under [Protecting a room](#protecting-a-room), so it will not surface a permissions problem either.

### Abuse reports

Meowlnir can intercept the report endpoints of the client-server API, so that abuse reports are delivered to a management room. This requires integration with the reverse proxy in front of the homeserver, which the playbook sets up for you when using Traefik:

```yaml
matrix_bot_meowlnir_config_reporting_enabled: true

# The management room that receives the reports.
matrix_bot_meowlnir_config_meowlnir_report_room: "!qporfwt:example.com"
```

Only the `v3` report endpoints are routed to Meowlnir. Requests to the legacy `r0` endpoints continue to reach the homeserver, because Meowlnir does not serve them.

### Enabling synapse-http-antispam support

Meowlnir can block invites and joins before they happen. This requires the [synapse-http-antispam](https://github.com/maunium/synapse-http-antispam) module, which the playbook can enable for you:

```yaml
matrix_bot_meowlnir_synapse_http_antispam_enabled: true

# The management room whose policies the module consults.
matrix_bot_meowlnir_synapse_http_antispam_management_room_id: "!qporfwt:example.com"
```

> [!WARNING]
> The playbook wires the module up to a single consumer, so this cannot be enabled at the same time as `matrix_bot_draupnir_config_web_synapseHTTPAntispam_enabled`. The playbook fails the run if both are enabled.

With the module in place, you can also block invitations to specific users outright, which is useful for accounts that attract spam:

```yaml
matrix_bot_meowlnir_config_antispam_block_invites_to_custom:
  - "@alice:example.com"
```

Such an invitation can still be let through case by case with the `!allow-invite` command.

### End-to-End Encryption support

To let Meowlnir's bots participate in encrypted rooms:

```yaml
matrix_bot_meowlnir_config_encryption_enable: true
```

When using Synapse, the playbook turns on the experimental features this depends on (`msc2409_to_device_messages_enabled` and `msc3202_transaction_extensions`) for you.

### Policy server (MSC4284)

Meowlnir can act as a [policy server](https://github.com/matrix-org/matrix-spec-proposals/pull/4284), letting rooms ask it to vet events before they are accepted:

```yaml
matrix_bot_meowlnir_policy_server_enabled: true
```

This exposes `/_matrix/policy` on your Matrix federation endpoint, so that other servers participating in a room can reach it.

That only stands the policy server up, though — no room is put behind it until you say so from the management room:

```
!policyserver enable !qporfwt:example.com
```

Given no room, `enable` applies to every protected room. Rooms which are not protected are skipped, with `Skipped ... as it is not a protected room`, so [protect a room](#protecting-a-room) before enabling it here. `!policyserver` on its own reports whether the policy server is available and prints its public key, and `!policyserver disable` reverses the change.

The playbook derives a stable signing key for you from `matrix_homeserver_generic_secret_key`. If you would rather use an independently generated one, produce it with the command below and set it as `matrix_bot_meowlnir_config_policy_server_signing_key`:

```sh
python3 -c "import os, base64; print('ed25519 policy_server ' + base64.b64encode(os.urandom(32)).decode().rstrip('='))"
```

### Synapse admin API access (optional)

A few of Meowlnir's features go through Synapse's admin API, not the client-server API — suspending or deactivating users, and deleting rooms during a takedown. Those calls require the caller to be a Synapse **server admin**, which bots are not by default, so they come back as `M_FORBIDDEN` ("You are not a server admin"). Nothing else is affected: bans, server ACLs, protecting rooms and watching policy lists all go through the client-server API, where a sufficient power level is the only requirement.

To grant that access, point each bot at a token belonging to a server admin:

```yaml
matrix_bot_meowlnir_config_meowlnir_admin_tokens:
  "@meowlnir_bot:example.com": "ADMIN_TOKEN_HERE"
```

The key is the bot the token is used for; the token itself belongs to an administrator account, not to the bot.

If you have more than one management room, note that room bans are only processed in the one named by `matrix_bot_meowlnir_config_meowlnir_room_ban_room`, and ignored elsewhere.

Where the token comes from depends on how your homeserver authenticates. Ordinarily you [obtain an access token](obtaining-access-tokens.md) for an account which is a Synapse server admin. When [Matrix Authentication Service](configuring-playbook-matrix-authentication-service.md) is enabled, Synapse no longer decides who is an admin, so the token has to be issued by MAS with admin privileges:

```sh
/matrix/matrix-authentication-service/bin/mas-cli manage issue-compatibility-token --yes-i-want-to-grant-synapse-admin-privileges alice
```

Note that bot users are created by the appservice and are not known to Matrix Authentication Service, so the token cannot be issued for the bot itself — use an administrator account.

### Access to the Synapse database (optional)

Some room takedown features rely on Meowlnir reading room IDs directly from the Synapse database. Upstream expects a user with read-only permissions, which the playbook does not create. Enabling the integration below hands Meowlnir the same credentials Synapse itself uses, which also grant write access:

```yaml
matrix_bot_meowlnir_synapse_database_integration_enabled: true
```

If you would rather not do that, create a read-only Postgres user yourself and point Meowlnir at it with `matrix_bot_meowlnir_synapse_database_uri`.

### Adopting an existing Meowlnir installation

If you already run Meowlnir outside the playbook and want to bring it under this role, two things need attention before the first run.

Your bots exist in Meowlnir's database but not in your `vars.yml` file, and [pruning](#bots-which-are-no-longer-declared) is on by default, so the first run would remove them. Declare them in `matrix_bot_meowlnir_bots_custom` — with `management_room_auto_create: false` and their existing rooms under `management_rooms` — or set `matrix_bot_meowlnir_bots_pruning_enabled: false`.

If the installation uses encryption, also copy the `pickle_key` from its old configuration file into `matrix_bot_meowlnir_config_encryption_pickle_key`. The crypto store cannot be read with a different key than it was written with, so leaving the playbook's default in place costs your bots their existing encryption sessions.

### Extending the configuration

There are some additional things you may wish to configure about the bot.

Take a look at:

- `roles/custom/matrix-bot-meowlnir/defaults/main.yml` for some variables that you can customize via your `vars.yml` file. You can override settings (even those that don't have dedicated playbook variables) using the `matrix_bot_meowlnir_configuration_extension_yaml` variable

> [!WARNING]
> Do not set any of Meowlnir's secrets to the literal value `generate`. Meowlnir re-runs its configuration upgrader on every start, so a `generate` placeholder would produce a brand new secret on every restart. The playbook derives stable values for you, and fails the run if it finds a `generate` placeholder.

## Installing

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,ensure-matrix-users-created,start
```

With `management_room_auto_create`, you then have an invitation waiting for you — accept it and start sending commands. If you supplied the management room yourself, carry on from step 3 of [Supplying your own management room](#supplying-your-own-management-room): invite the bot, then give it power level 50 or more.

**Notes**:

- The `ensure-matrix-users-created` tag is what creates the bots declared in `matrix_bot_meowlnir_bots_custom`, registers their management rooms, and removes the ones you no longer declare. It deliberately does not run as part of `setup-all`, so that installing onto a server whose database you are about to restore from a backup does not write anything.

- Re-running is safe and idempotent, so adding a bot later is a matter of extending the list and running the same command again.

- The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

## Usage

You can refer to the upstream [documentation](https://docs.mau.fi/meowlnir/) for a more detailed usage guide.

Below is a **non-exhaustive quick-start guide** for the impatient.

### Inspecting and driving Meowlnir directly

The playbook drives Meowlnir's management API for you based on `matrix_bot_meowlnir_bots_custom`, which is the recommended way. For anything it does not cover, helper scripts are installed under `/matrix/meowlnir/bin`, which find the management secret and reach the API inside the container:

```sh
# Show the bots, their management rooms, protected rooms and watched policy lists
/matrix/meowlnir/bin/meowlnir-bots

# Call any endpoint: meowlnir-api <METHOD> <PATH> [JSON body]
/matrix/meowlnir/bin/meowlnir-api GET /_meowlnir/v1/bots

# Create another management room for an existing bot, with the given users able to command it there
/matrix/meowlnir/bin/meowlnir-create-management-room meowlnir_bot @alice:example.com

# Ask the homeserver who Meowlnir's appservice token belongs to.
# A 401 response means the homeserver is running without Meowlnir's appservice registration, which is also what Meowlnir's own "Failed to connect to homeserver" log messages usually mean.
/matrix/meowlnir/bin/meowlnir-whoami
```

`meowlnir-create-management-room` prints the new room's ID, which you then register with `meowlnir-api PUT /_meowlnir/v1/management_room/<room ID>`.

See the upstream [bot creation documentation](https://docs.mau.fi/meowlnir/bot-create.html) for the full set of endpoints. Bear in mind that bots you create this way are not declared in your `vars.yml` file, so the next playbook run will remove them again (see [Bots which are no longer declared](#bots-which-are-no-longer-declared)).

If you have enabled encryption, each bot also needs verifying once. That step is left manual because it returns a recovery key you need to store somewhere safe:

```sh
/matrix/meowlnir/bin/meowlnir-api POST /_meowlnir/v1/bot/meowlnir_bot/verify '{"generate": true}'
```

### Protecting a room

Invite the bot to a room, give it a power level high enough to act (see below), and then tell it to protect the room by sending this command to its management room:

```
!rooms protect !qporfwt:example.com
```

Meowlnir refuses to protect a room unless its power level reaches that room's own `ban` and `redact` levels (50 in a default room). That is only enough for user bans, though: writing `m.room.server_acl` usually requires 100, and without it the server rules in your watched lists have no effect — which is most of what a list like [CME](https://matrix.to/#/%23community-moderation-effort-bl:neko.dev) carries. **Give the bot power level 100** unless you only care about user bans.

Set the power level *before* protecting the room. Meowlnir re-sends server ACLs when it starts and when a watched list changes, but not when its own power level goes up subsequently, so raising it afterwards leaves the room without ACLs until you restart the bot (`systemctl restart matrix-bot-meowlnir` or via the playbook's Ansible `start` tag).

### Subscribing to a policy list

Policy lists are maintained in Matrix rooms. Popular public ones are:

- `#community-moderation-effort-bl:neko.dev`
- `#huginn-muninn-active-threats:feline.support`

Subscribe to one by sending the following command to the management room:

```
!lists subscribe #community-moderation-effort-bl:neko.dev cme
```

The last argument is a shortcode, which you use to refer to the list in later commands.

### Overriding a policy from someone else's list

This is the main capability Meowlnir has that Draupnir does not.

When several watched lists carry a policy for the same user, **the first match wins**, and "first" means the order in which the lists are watched. So to be able to override a community list's ban, your own list has to come before it.

`!lists subscribe` appends, which makes subscription order the precedence order. Subscribe to your own list first, and to community lists afterwards:

```
!lists create my-ban-exceptions
!lists subscribe #community-moderation-effort-bl:neko.dev cme
```

> [!NOTE]
> If you have already subscribed in the wrong order, fixing it means editing the `fi.mau.meowlnir.watched_lists` state event in the management room by hand. Newer Meowlnir releases (than `v0.2606.0`) add `!lists subscribe … --insert-before <shortcode>`, which will make reordering a single command.

You can then publish an unban policy into your own list, which takes precedence over the community list's ban:

```
!add-unban my-bans @alice:example.com false-positive
```

> [!NOTE]
> Unlike `!ban`, the `!add-unban` command does not treat its reason as a trailing argument, so a reason containing spaces is discarded. Use a single word (or hyphenate) until that is fixed upstream.

> [!IMPORTANT]
> An unban policy stops a ban from being **re-applied**; it does not undo one that is already in place unless Meowlnir applied it itself and still has it on record. A ban placed by a human moderator, or by the Draupnir or Mjolnir you are migrating away from, stays. Unban such a user once by hand — from then on the policy keeps them unbanned, while you remain subscribed to the list that banned them.

Use `!match @alice:example.com` to see which policies currently apply to a user and which list each came from.

> [!NOTE]
> Unban policies use a Meowlnir-specific recommendation (`fi.mau.meowlnir.unban`) which is not part of the Matrix specification. If you publish your policy list for other people to subscribe to, subscribers running Draupnir or Mjolnir will ignore your unban policies.

There is also a blunter, server-wide escape hatch for policies that are too wide to tolerate at all — `matrix_bot_meowlnir_config_meowlnir_hacky_rule_filter_custom`, which makes Meowlnir ignore any policy matching the listed entities.

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by running a command like `journalctl -fu matrix-bot-meowlnir`.

If bots appear to do nothing, check that they have an Administrator power level in the rooms they are meant to protect, and that the room has been added with `!rooms protect`.

If commands in a management room get no reply at all, check the bot's power level *there* too — it needs at least 50 to record its own configuration.

A bare `!lists` returns nothing in a management room which has never had a policy list. That is an upstream bug and it clears as soon as you subscribe to one; `!lists subscribe` works from the start.
