<!--
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara
SPDX-FileCopyrightText: 2024 Slavi Pantaleev

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up baibot (optional)

<p align="center">
	<img src="https://github.com/etkecc/baibot/raw/main/etc/assets/baibot.svg" alt="baibot logo" width="150" />
	<h1 align="center">baibot</h1>
</p>

🤖 [baibot](https://github.com/etkecc/baibot) (pronounced bye-bot) is a [Matrix](https://matrix.org/) bot developed by [etke.cc](https://etke.cc/) that exposes the power of [AI](https://en.wikipedia.org/wiki/Artificial_intelligence) / [Large Language Models](https://en.wikipedia.org/wiki/Large_language_model) to you. 🤖

It supports [OpenAI](https://openai.com/)'s [ChatGPT](https://openai.com/blog/chatgpt/) models, as many well as other [☁️ providers](https://github.com/etkecc/baibot/blob/main/docs/providers.md).

It's designed as a more private and [✨ featureful](https://github.com/etkecc/baibot/?tab=readme-ov-file#-features) alternative to [matrix-chatgpt-bot](./configuring-playbook-bot-chatgpt.md). See the [baibot](https://github.com/etkecc/baibot) project and its documentation for more information.

## Prerequisites

API access to one or more LLM [☁️ providers](https://github.com/etkecc/baibot/blob/main/docs/providers.md).

## Adjusting the playbook configuration

There are **a lot of configuration options** (some required, some possibly required, some optional), so they're **split into multiple sections below**:

<!-- no toc -->
- [Base configuration](#base-configuration)
- [👮‍♂️ Administrator configuration](#️-administrator-configuration)
- [👥 Initial users configuration](#-initial-users-configuration)
- [🤖 Configuring agents via Ansible](#-configuring-agents-via-ansible)
- [🤝 Configuring initial default handlers](#-configuring-initial-default-handlers)

Depending on your current `vars.yml` file and desired configuration, **you may require more than just the [base configuration](#base-configuration)**.

### Base configuration

To enable the bot, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_bot_baibot_enabled: true

# Uncomment and adjust this part if you'd like to use a username different than the default
# matrix_bot_baibot_config_user_mxid_localpart: baibot

# Generate a strong password for the bot. You can create one with a command like `pwgen -s 64 1`.
# If you'd like to change this password subsequently, see the details below.
matrix_bot_baibot_config_user_password: 'PASSWORD_FOR_THE_BOT'

# An optional passphrase to use for backing up and recovering the bot's encryption keys.
# You can create one with a command like `pwgen -s 64 1`.
#
# If set to null, the recovery module will not be used and losing your session/database
# will mean you lose access to old messages in encrypted room.
# It's highly recommended that you configure this to avoid losing access to encrypted messages.
#
# Changing this subsequently will also cause you to lose access to old messages in encrypted rooms.
# For details about changing this subsequently or resetting, see `defaults/main.yml` in the baibot role.
matrix_bot_baibot_config_user_encryption_recovery_passphrase: 'ANY_LONG_AND_SECURE_PASSPHRASE_STRING_HERE'

# An optional secret for encrypting the bot's session data (see `matrix_bot_baibot_data_path`).
# This must be 32-bytes (64 characters when HEX-encoded).
# Generate it with: `openssl rand -hex 32`
# Set to null or empty to avoid using encryption.
# Changing this subsequently requires that you also throw away all data (see `matrix_bot_baibot_data_path`)
matrix_bot_baibot_config_persistence_session_encryption_key: 'A_HEX_STRING_OF_64_CHARACTERS_HERE'

# An optional secret for encrypting bot configuration stored in Matrix's account data.
# This must be 32-bytes (64 characters when HEX-encoded).
# Generate it with: `openssl rand -hex 32`
# Set to null or empty to avoid using encryption.
# Changing this subsequently will make you lose your configuration.
matrix_bot_baibot_config_persistence_config_encryption_key: 'A_HEX_STRING_OF_64_CHARACTERS_HERE'
```

As mentioned above, **this may not be enough**. Continue with the configuration sections below.

### 👮‍♂️ Administrator configuration

This is an addition to the [base configuration](#base-configuration).

To specify who is considered a bot [👮‍♂️ Administrator](https://github.com/etkecc/baibot/blob/main/docs/access.md#administrators), you either need to specify `matrix_bot_baibot_config_access_admin_patterns` or `matrix_admin`. The latter is a single variable which affects all bridges and bots.

If `matrix_admin` is already configured in your `vars.yml` configuration, you can skip this section.

**If necessary**, add the following configuration to your `vars.yml` file:

```yaml
# Uncomment to add one or more admins to this bridge:
#
# matrix_bot_baibot_config_access_admin_patterns:
#   - "@*:example.com"
#   - "@admin:example.net"
#
# … unless you've made yourself an admin of all bots/bridges like this:
#
# matrix_admin: '@yourAdminAccount:{{ matrix_domain }}'
```

### 👥 Initial users configuration

By default, **all users on your homeserver are considered allowed users**. If that's OK, you can skip this section.

This is an addition to the [base configuration](#base-configuration).

To specify who is considered a bot [👥 User](https://github.com/etkecc/baibot/blob/main/docs/access.md#user), you may:

- define an **initial** value for `matrix_bot_baibot_config_initial_global_config_user_patterns` Ansible variable, as shown below
- configure the list at runtime via the bot's `!bai access set-users SPACE_SEPARATED_PATTERNS` command

Configuring `matrix_bot_baibot_config_initial_global_config_user_patterns` is optional, but it can be useful to pre-configure the bot with a list of users who should have access to the bot's features.

**Note**: Once initially configured, the allowed users list **cannot be managed via Ansible anymore**. It can only be managed subsequently via bot commands.

**If necessary**, add the following configuration to your `vars.yml` file:

```yaml
# Uncomment and adjust the bot users if necessary:
#
# Subsequent changes to `matrix_bot_baibot_config_initial_global_config_user_patterns` do not affect the bot's behavior.
# Once initially configured, the allowed users list is managed via bot commands, not via Ansible.
#
# matrix_bot_baibot_config_initial_global_config_user_patterns:
#   - "@*:{{ matrix_bot_baibot_config_homeserver_server_name }}"
```

### 🤖 Configuring agents via Ansible

You are **not required** to define agents [statically](https://github.com/etkecc/baibot/blob/main/docs/configuration/README.md#static-configuration) via Ansible. **To get started quickly**, you can **skip this section and define agents at runtime via chat commands** (following the bot's guidance).

Privileged users (like the [👮‍♂️ Administrator](#️-administrator-configuration), but potentially others too — see the upstream [🔒 access](https://github.com/etkecc/baibot/blob/main/docs/access.md) documentation) can **define agents dynamically at any time** via chat commands.

The Ansible role includes preset variables for easily enabling some [🤖 agents](https://github.com/etkecc/baibot/blob/main/docs/agents.md) on various [☁️ providers](https://github.com/etkecc/baibot/blob/main/docs/providers.md) (e.g. OpenAI, etc).

Besides the presets, the Ansible role also includes support for configuring additional statically-defined agents via the `matrix_bot_baibot_config_agents_static_definitions_custom` Ansible variable.

Agents defined statically and those created dynamically (via chat) are named differently, so **conflict cannot arise**.

Depending on your propensity for [GitOps](https://en.wikipedia.org/wiki/DevOps#GitOps), you may prefer to define agents statically via Ansible, or you may wish to do it dynamically via chat.

Before proceeding, we recommend reading the upstream documentation on [How to choose a provider](https://github.com/etkecc/baibot/blob/main/docs/providers.md#how-to-choose-a-provider). In short, it's probably best to go with [OpenAI](#openai).

#### Anthropic

You can statically-define a single [🤖 agent](https://github.com/etkecc/baibot/blob/main/docs/agents.md) instance powered by the [Anthropic provider](https://github.com/etkecc/baibot/blob/main/docs/providers.md#anthropic) with the help of the playbook's preset variables.

Here's an example **addition** to your `vars.yml` file:

```yaml
matrix_bot_baibot_config_agents_static_definitions_anthropic_enabled: true

matrix_bot_baibot_config_agents_static_definitions_anthropic_config_api_key: "YOUR_API_KEY_HERE"

# Uncomment and adjust this part if you'd like to use another text-generation agent
# matrix_bot_baibot_config_agents_static_definitions_anthropic_config_text_generation_model_id: claude-3-5-sonnet-20240620

# The playbook defines a default prompt for all statically-defined agents.
# You can adjust it in the `matrix_bot_baibot_config_agents_static_definitions_prompt` variable,
# or you can adjust it below only for the Anthropic agent.
# matrix_bot_baibot_config_agents_static_definitions_anthropic_config_text_generation_prompt: "{{ matrix_bot_baibot_config_agents_static_definitions_prompt }}"
```

If you'd like to use more than one model, take a look at the [Configuring additional agents (without a preset)](#configuring-additional-agents-without-a-preset) section below.

💡 You may also wish to use this new agent for [🤝 Configuring initial default handlers](#-configuring-initial-default-handlers).

#### Groq

You can statically-define a single [🤖 agent](https://github.com/etkecc/baibot/blob/main/docs/agents.md) instance powered by the [Groq provider](https://github.com/etkecc/baibot/blob/main/docs/providers.md#groq) with the help of the playbook's preset variables.

Here's an example **addition** to your `vars.yml` file:

```yaml
matrix_bot_baibot_config_agents_static_definitions_groq_enabled: true

matrix_bot_baibot_config_agents_static_definitions_groq_config_api_key: "YOUR_API_KEY_HERE"

# Specify the text-generation agent you'd like to use
matrix_bot_baibot_config_agents_static_definitions_groq_config_text_generation_model_id: "llama3-70b-8192"

# The playbook defines a default prompt for all statically-defined agents.
# You can adjust it in the `matrix_bot_baibot_config_agents_static_definitions_prompt` variable,
# or you can adjust it below only for the Groq agent.
# matrix_bot_baibot_config_agents_static_definitions_groq_config_text_generation_prompt: "{{ matrix_bot_baibot_config_agents_static_definitions_prompt }}"

# Uncomment and adjust this part if you're not happy with these speech-to-text defaults:
#
# matrix_bot_baibot_config_agents_static_definitions_groq_config_speech_to_text_enabled: true
# matrix_bot_baibot_config_agents_static_definitions_groq_config_speech_to_text_model_id: whisper-large-v3
```

Because this is a [statically](https://github.com/etkecc/baibot/blob/main/docs/configuration/README.md#static-configuration)-defined agent, it will be given a `static/` ID prefix and will be named `static/groq`.

If you'd like to use more than one model, take a look at the [Configuring additional agents (without a preset)](#configuring-additional-agents-without-a-preset) section below.

💡 You may also wish to use this new agent for [🤝 Configuring initial default handlers](#-configuring-initial-default-handlers).

#### Mistral

You can statically-define a single [🤖 agent](https://github.com/etkecc/baibot/blob/main/docs/agents.md) instance powered by the [🇫🇷 Mistral provider](https://github.com/etkecc/baibot/blob/main/docs/providers.md#mistral) with the help of the playbook's preset variables.

Here's an example **addition** to your `vars.yml` file:

```yaml
matrix_bot_baibot_config_agents_static_definitions_mistral_enabled: true

matrix_bot_baibot_config_agents_static_definitions_mistral_config_api_key: "YOUR_API_KEY_HERE"

# The playbook defines a default prompt for all statically-defined agents.
# You can adjust it in the `matrix_bot_baibot_config_agents_static_definitions_prompt` variable,
# or you can adjust it below only for the Mistral agent.
# matrix_bot_baibot_config_agents_static_definitions_mistral_config_text_generation_prompt: "{{ matrix_bot_baibot_config_agents_static_definitions_prompt }}"

# Uncomment and adjust this part if you're not happy with these defaults:
# matrix_bot_baibot_config_agents_static_definitions_mistral_config_text_generation_model_id: mistral-large-latest
```

Because this is a [statically](https://github.com/etkecc/baibot/blob/main/docs/configuration/README.md#static-configuration)-defined agent, it will be given a `static/` ID prefix and will be named `static/mistral`.

If you'd like to use more than one model, take a look at the [Configuring additional agents (without a preset)](#configuring-additional-agents-without-a-preset) section below.

💡 You may also wish to use this new agent for [🤝 Configuring initial default handlers](#-configuring-initial-default-handlers).

#### OpenAI

You can statically-define a single [🤖 agent](https://github.com/etkecc/baibot/blob/main/docs/agents.md) instance powered by the [OpenAI provider](https://github.com/etkecc/baibot/blob/main/docs/providers.md#openai) with the help of the playbook's preset variables.

The OpenAI provider is **only meant to be used with OpenAI's official API** and compatibility with other services (which do not fully adhere to the OpenAI API spec completely) is limited. **If you're targeting an OpenAI-compatible service**, use the [OpenAI Compatible](#openai-compatible) provider instead.

Here's an example **addition** to your `vars.yml` file:

```yaml
matrix_bot_baibot_config_agents_static_definitions_openai_enabled: true

matrix_bot_baibot_config_agents_static_definitions_openai_config_api_key: "YOUR_API_KEY_HERE"

# The playbook defines a default prompt for all statically-defined agents.
# You can adjust it in the `matrix_bot_baibot_config_agents_static_definitions_prompt` variable,
# or you can adjust it below only for the OpenAI agent.
# matrix_bot_baibot_config_agents_static_definitions_openai_config_text_generation_prompt: "{{ matrix_bot_baibot_config_agents_static_definitions_prompt }}"

# If you'd like to use another text-generation agent, uncomment and adjust:
# matrix_bot_baibot_config_agents_static_definitions_openai_config_text_generation_model_id: gpt-4.1
```

Because this is a [statically](https://github.com/etkecc/baibot/blob/main/docs/configuration/README.md#static-configuration)-defined agent, it will be given a `static/` ID prefix and will be named `static/openai`.

If you'd like to use more than one model, take a look at the [Configuring additional agents (without a preset)](#configuring-additional-agents-without-a-preset) section below.

💡 You may also wish to use this new agent for [🤝 Configuring initial default handlers](#-configuring-initial-default-handlers).

#### OpenAI Compatible

You can statically-define a single [🤖 agent](https://github.com/etkecc/baibot/blob/main/docs/agents.md) instance powered by the [OpenAI Compatible provider](https://github.com/etkecc/baibot/blob/main/docs/providers.md#openai-compatible) with the help of the playbook's preset variables.

This provider allows you to use OpenAI-compatible API services like [OpenRouter](https://github.com/etkecc/baibot/blob/main/docs/providers.md#openrouter), [Together AI](https://github.com/etkecc/baibot/blob/main/docs/providers.md#together-ai), etc.

Some of these popular services already have **shortcut** providers (see [supported providers](https://github.com/etkecc/baibot/blob/main/docs/providers.md#supported-providers) leading to this one behind the scenes — this make it easier to get started.

As of this moment, the playbook does not include presets for any of these services, so you'll need to [Configuring additional agents (without a preset)](#configuring-additional-agents-without-a-preset).

#### Configuring additional agents (without a preset)

The Ansible role may be lacking preset variables for some [☁️ provider](https://github.com/etkecc/baibot/blob/main/docs/providers.md), or you may wish to statically-define an agent on the same provider twice (or more) with different configuration.

It's possible to inject your own agent configuration using the `matrix_bot_baibot_config_agents_static_definitions_custom` Ansible variable.

You can also define providers at runtime, by chatting with the bot, so using Ansible is not a requirement.

Below is an an **example** demonstrating **statically-defining agents via Ansible without using presets**:

```yaml
matrix_bot_baibot_config_agents_static_definitions_custom:
  # This agent will use the GPT 3.5 model and will only support text-generation,
  # even though the `openai` provider could support other features (e.g. image-generation).
  - id: my-openai-gpt-3.5-turbo-agent
    provider: openai
    config:
        base_url: https://api.openai.com/v1
        api_key: "YOUR_API_KEY_HERE"
        text_generation:
          model_id: gpt-3.5-turbo-0125
          prompt: "{{ matrix_bot_baibot_config_agents_static_definitions_prompt }}"
          temperature: 1.0
          max_response_tokens: 4096
          max_context_tokens: 16385
        speech_to_text: null
        text_to_speech: null
        image_generation: null

  # This agent uses the `openai` provider, but adjusts the base URL, so that it points to some Ollama instance
  # (which supports an OpenAI-compatible API).
  - id: my-ollama-agent
    provider: openai
    config:
      base_url: http://ollama-service:1234/v1
      api_key: ""
      text_generation:
        model_id: "llama3.1:8b"
        prompt: "{{ matrix_bot_baibot_config_agents_static_definitions_prompt }}"
        temperature: 1.0
        max_response_tokens: 4096
        max_context_tokens: 128000
          speech_to_text: null
          text_to_speech: null
          image_generation: null
```

Because these are [statically](https://github.com/etkecc/baibot/blob/main/docs/configuration/README.md#static-configuration)-defined agents, they will be given a `static/` ID prefix and will be named `static/my-openai-gpt-3.5-turbo-agent` and `static/my-ollama-agent`, respectively.

💡 To figure out what to put in the `config` section, refer to the [☁️ provider](https://github.com/etkecc/baibot/blob/main/docs/providers.md) page, which contains **sample configuration YAML for each provider**.

As with any [🤖 agent](https://github.com/etkecc/baibot/blob/main/docs/agents.md), defining them means they exist. To actually make use of them, they need to be configured as handlers globally or in a specific room — see [Mixing & matching models](https://github.com/etkecc/baibot/blob/main/docs/features.md#mixing--matching-models).

💡 You may also wish to use these new agents for [🤝 Configuring initial default handlers](#-configuring-initial-default-handlers).

### 🤝 Configuring initial default handlers

This section is only useful if you're [🤖 Configuring agents via Ansible](#-configuring-agents-via-ansible), as it lets you put these agents to use as soon as the bot starts (by adjusting the bot's **initial global configuration**).

If you're not configuring agents via Ansible, you can skip this section.

This section is only useful the first time around. **Once initially configured the global configuration cannot be managed Ansible**, but only via bot commands.

baibot supports [various purposes](https://github.com/etkecc/baibot/blob/main/docs/features.md):

- [💬 text-generation](https://github.com/etkecc/baibot/blob/main/docs/features.md#-text-generation): communicating with you via text

- [🦻 speech-to-text](https://github.com/etkecc/baibot/blob/main/docs/features.md#-speech-to-text): turning your voice messages into text

- [🗣️ text-to-speech](https://github.com/etkecc/baibot/blob/main/docs/features.md#-text-to-speech): turning bot or users text messages into voice messages

- [🖌️ image-generation](https://github.com/etkecc/baibot/blob/main/docs/features.md#-image-generation): generating images based on instructions

- ❓ catch-all: special purposes, indicating use as a fallback (when no specific handler is configured)

[Mixing & matching models](https://github.com/etkecc/baibot/blob/main/docs/features.md#mixing--matching-models) is made possible by the bot's ability to have different [🤝 handlers](https://github.com/etkecc/baibot/blob/main/docs/configuration/handlers.md) configured for different purposes.

This configuration can be done as a global fallback, or per-room. Both of these [🛠️ configurations](https://github.com/etkecc/baibot/blob/main/docs/configuration/README.md) are managed at runtime (viat chat), but **the global configuration can have some initial defaults configured via Ansible**.

You can configure the **initial values** for these via Ansible, via the `matrix_bot_baibot_config_initial_global_config_handler_*` variables.

Example **additional** `vars.yml` configuration:

```yaml
# Note: these are initial defaults for the bot's global configuration.
# As such, changing any of these values subsequently has no effect on the bot's behavior.
# Once initially configured, the global configuration is managed via bot commands, not via Ansible.

matrix_bot_baibot_config_initial_global_config_handler_catch_all: static/openai

# In this example, there's no need to define any of these below.
# Configuring the catch-all purpose handler is enough.
matrix_bot_baibot_config_initial_global_config_handler_text_generation: null
matrix_bot_baibot_config_initial_global_config_handler_text_to_speech: null
matrix_bot_baibot_config_initial_global_config_handler_speech_to_text: null
matrix_bot_baibot_config_initial_global_config_handler_image_generation: null
```

**Note**: these are initial defaults for the bot's global configuration. As such, changing any of these values subsequently has no effect on the bot's behavior. **Once initially configured the global configuration cannot be managed Ansible**, but only via bot commands.

### Extending the configuration

There are some additional things you may wish to configure about the bot.

Take a look at:

- `roles/custom/matrix-bot-baibot/defaults/main.yml` for some variables that you can customize via your `vars.yml` file
- `roles/custom/matrix-bot-baibot/templates/config.yaml.j2` for the bot's default configuration. You can override settings (even those that don't have dedicated playbook variables) using the `matrix_bot_baibot_configuration_extension_yaml` variable

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

- If you change the bot password (`matrix_bot_baibot_config_user_password` in your `vars.yml` file) subsequently, the bot user's credentials on the homeserver won't be updated automatically. If you'd like to change the bot user's password, use a tool like [synapse-admin](configuring-playbook-synapse-admin.md) to change it, and then update `matrix_bot_baibot_config_user_password` to let the bot know its new password.

## Usage

To use the bot, invite it to any existing Matrix room (`/invite @baibot:example.com` where `example.com` is your base domain, not the `matrix.` domain).

If you're an allowed bot [👥 user](https://github.com/etkecc/baibot/blob/main/docs/access.md#user) (see [👥 Initial users configuration](#-initial-users-configuration)), the bot will accept your invitation and join the room.

After joining, the bot will introduce itself and show information about the [✨ features](https://github.com/etkecc/baibot/blob/main/docs/features.md) that are enabled for it.

If you've [🤖 configured one or more agents via Ansible](#-configuring-agents-via-ansible) and have [🤝 configured initial default handlers](#configuring-initial-default-handlers), the bot will immediately be able to make use of these agents for this new room. Otherwise, you will need to configure agents and/or handlers via chat commands.

Send `!bai help` to the bot in the room to see the available commands.

You can also refer to the upstream [baibot](https://github.com/etkecc/baibot) project's documentation.

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-bot-baibot`.

### Increase logging verbosity

The default logging level for this service is `info`. If you want to increase the verbosity to `debug` (or even `trace`), add the following configuration to your `vars.yml` file and re-run the playbook:

```yaml
# Adjust the bot's own logging level.
matrix_bot_baibot_config_logging_level_baibot: debug

# Adjust the logging level for the mxlink bot library used by the bot.
matrix_bot_baibot_config_logging_level_mxlink: debug

# Adjust the logging level for other libraries used by the bot.
# Having this set to a value other than "warn" can be very noisy.
matrix_bot_baibot_config_logging_level_other_libs: debug
```

**Alternatively**, you can use a single variable to set the logging level for all of the above (bot + all libraries):

```yaml
matrix_bot_baibot_config_logging: debug
```
