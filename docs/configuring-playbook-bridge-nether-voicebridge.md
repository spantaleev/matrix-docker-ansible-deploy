<!--
SPDX-FileCopyrightText: 2026 Jason LaGuidice

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up Nether Voice Bridge (optional)

The playbook can install and configure [nether-voicebridge](https://nether.codes/nether/nether-voicebridge), a bridge that connects Discord voice channels to Matrix rooms, using [LiveKit](https://livekit.io/) for the Matrix side of the audio.

Unlike text bridges, this bridge does not relay chat messages — it bridges **audio only**, making Discord voice participants audible in the Matrix room's call and vice versa.

## Prerequisites

Before enabling this bridge you must have:

1. **The lk-jwt service and a LiveKit SFU.** The bridge discovers both from the `org.matrix.msc4143.rtc_foci` entry in your homeserver's `.well-known/matrix/client`; the JWT service alone is not enough. You don't need to enable these yourself: enabling this role automatically enables the playbook's lk-jwt service and LiveKit server (via `matrix_rtc_enabled`). The playbook will error during deploy if the JWT service has been explicitly disabled.

2. **One or more Discord puppet bot tokens.** Each token is a separate Discord application created at [discord.com/developers/applications](https://discord.com/developers/applications). For each bot:
   - Create a new application and enable the **Bot** feature.
   - Enable the `GUILDS` and `GUILD_VOICE_STATES` intents.
   - Generate and copy the bot token.
   - Invite the bot to every Discord server (guild) it will bridge, with permissions: **Connect**, **Speak**, **Use Voice Activity**, **Change Nickname**.

3. **One or more bridged room pairs.** For each Discord voice channel you want to bridge:
   - A Discord guild ID (right-click server icon → *Copy Server ID*).
   - A Discord channel ID (right-click voice channel → *Copy Channel ID*).
   - A Matrix room whose power levels allow level-0 users to send `org.matrix.msc3401.call.member` state events (the ghosts join as ordinary users). If this permission is not set correctly the ghosts may fail to join
   - If the room is invite-only or restricted, invite the bridge bot (`@nether-voicebridge_bot:example.com`) first.
   - The internal Matrix room ID in `!roomid:domain` form (fetching varies based on your Matrix client).

## Adjusting the playbook configuration

Add the following to your `vars.yml` configuration file:

```yaml
matrix_nether_voicebridge_enabled: true

# One or more Discord bot tokens (the shared puppet pool)
matrix_nether_voicebridge_puppet_tokens:
  - "YOUR_DISCORD_BOT_TOKEN_1"
  - "YOUR_DISCORD_BOT_TOKEN_2"

# One or more Discord channel ↔ Matrix room mappings
matrix_nether_voicebridge_bridges:
  - name: "lobby"
    discord_guild_id: "YOUR_DISCORD_SERVER_ID"
    discord_channel_id: "YOUR_DISCORD_VOICE_CHANNEL_ID"
    matrix_room_id: "!yourroomid:example.com"
```

## How the puppet pool works

The bridge allocates puppet bots dynamically, per (bot, Discord server): one bot can be in voice channels on several servers at the same time, so the pool limit applies to each server separately, not across all bridges.

Each Matrix call participant gets their own puppet bot in the Discord voice channel, named after them. Puppets are allocated per call participant.

In each Discord server, you need:

pool size ≥ the sum, over that server's active bridged channels, of max(1, Matrix call participants)

### Overflow

Anyone past the available bots is mixed into the first joiner's audio, and the participant is renamed `<prefix>Overflow` while that is happening. When a bot frees up, the participant who has been in overflow the longest gets it.

If a channel needs a bot and none is free, the bridge may take a spare non-anchor bot from the channel with the most slack. The participant who loses their bot drops into overflow.

## Puppet nickname prefix

Puppets are the bots that represent Matrix participants on Discord. Discord users see Matrix participants identified by a prefix on their voice channel nickname. The default is `[Matrix] `. To change it set the following in your `vars.yaml`:

```yaml
matrix_nether_voicebridge_puppet_nickname_prefix: "[Matrix] "
```

## Multiple guilds and channels

Add more entries to `matrix_nether_voicebridge_bridges` to bridge additional channel pairs from the same process. All bridges share the puppet token pool — invite all bots to all guilds you plan to bridge, and size the pool for each guild as described above. If bridging multiple channels within the same guild, repeat the full pattern (including reusing the guild ID) for each channel to be bridged.

```yaml
matrix_nether_voicebridge_bridges:
  - name: "lobby"
    discord_guild_id: "111111111111111111"
    discord_channel_id: "222222222222222222"
    matrix_room_id: "!abc:example.com"
  - name: "gaming"
    discord_guild_id: "111111111111111111"
    discord_channel_id: "333333333333333333"
    matrix_room_id: "!xyz:example.com"
```

## Advanced configuration

To override the lk-jwt or LiveKit SFU endpoints, or force media E2EE on or off for a specific bridge, add a `livekit` dictionary to that bridge. Its entries are rendered into that bridge's `[bridge.livekit]` table:

```yaml
matrix_nether_voicebridge_bridges:
  - name: "lobby"
    discord_guild_id: "YOUR_DISCORD_SERVER_ID"
    discord_channel_id: "YOUR_DISCORD_VOICE_CHANNEL_ID"
    matrix_room_id: "!yourroomid:example.com"
    livekit:
      media_e2ee: false
```

For anything else, `matrix_nether_voicebridge_configuration_extension_toml` appends raw TOML to the end of `config.toml`. Since it comes after the last bridge's `[bridge.livekit]` table, use it only for additional tables, and do not repeat `[bridge.livekit]`

To enable verbose logging:

```yaml
matrix_nether_voicebridge_rust_log: "nether_voicebridge=debug,nvb_discord=debug,nvb_matrix_rtc=debug"
```

## Self-building the container image

The prebuilt image from `nether.codes/nether/nether-voicebridge` is used by default. To build from source instead:

```yaml
matrix_nether_voicebridge_container_image_self_build: true
```

## Homeserver compatibility

The bridge works with all homeservers that support appservices. For Synapse the configuration is completed automatically by the playbook. For other homeservers like Conduwuit, Continuwuity, or Tuwunel the appservice must be registered manually after installation by the playbook by messaging the server's admin room. Use the contents of the generated `registration.yaml` (by default at `/matrix/matrix-nether-voicebridge/config/registration.yaml` on the server) to complete the setup process.

## Installing

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```
