<!--
SPDX-FileCopyrightText: 2023 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2023 MDAD project contributors
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up matrix-bot-chatgpt (optional, unmaintained)

**Note**: [matrix-chatgpt-bot](https://github.com/matrixgpt/matrix-chatgpt-bot) is now an archived (**unmaintained**) project. Talking to ChatGPT (and many other LLM providers) can happen via the much more featureful [baibot](https://github.com/etkecc/baibot), which can be [installed using this playbook](configuring-playbook-bot-baibot.md). Consider using that bot instead of this one.

The playbook can install and configure [matrix-chatgpt-bot](https://github.com/matrixgpt/matrix-chatgpt-bot) for you.

Talk to [ChatGPT](https://openai.com/blog/chatgpt/) via your favourite Matrix client!

See the project's [documentation](https://github.com/matrixgpt/matrix-chatgpt-bot/blob/main/README.md) to learn what it does and why it might be useful to you.

## Prerequisites

### Obtain an OpenAI API key

To use the bot, you'd need to obtain an API key from [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys).

### Register the bot account

The playbook does not automatically create users for you. You **need to register the bot user manually** before setting up the bot.

Generate a strong password for the bot. You can create one with a command like `pwgen -s 64 1`.

You can use the playbook to [register a new user](registering-users.md):

```sh
ansible-playbook -i inventory/hosts setup.yml --extra-vars='username=bot.chatgpt password=PASSWORD_FOR_THE_BOT admin=no' --tags=register-user
```

### Obtain an access token and create encryption keys

The bot requires an access token to be able to connect to your homeserver. Refer to the documentation on [how to obtain an access token](obtaining-access-tokens.md).

> [!WARNING]
> Access tokens are sensitive information. Do not include them in any bug reports, messages, or logs. Do not share the access token with anyone.

To make sure the bot can read encrypted messages, it will need an encryption key, just like any other new user. While obtaining the access token, follow the prompts to setup a backup key. More information can be found in the [Element documentation](https://element.io/help#encryption6).

## Adjusting the playbook configuration

To enable the bot, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file. Make sure to replace `API_KEY_HERE` with the API key retrieved [here](#obtain-an-openai-api-key) and `ACCESS_TOKEN_HERE` with the access token created [here](#obtain-an-access-token-and-create-encryption-keys), respectively.

```yaml
matrix_bot_chatgpt_enabled: true

matrix_bot_chatgpt_openai_api_key: 'API_KEY_HERE'

# Uncomment and adjust this part if you'd like to use a username different than the default
# matrix_bot_chatgpt_matrix_bot_username_localpart: 'bot.chatgpt'

matrix_bot_chatgpt_matrix_access_token: 'ACCESS_TOKEN_HERE'

# Configuring the system prompt used, needed if the bot is used for special tasks.
# More information: https://github.com/mustvlad/ChatGPT-System-Prompts
matrix_bot_chatgpt_matrix_bot_prompt_prefix: 'Instructions:\nYou are ChatGPT, a large language model trained by OpenAI.'
```

### Extending the configuration

There are some additional things you may wish to configure about the bot.

Take a look at:

- `roles/custom/matrix-bot-chatgpt/defaults/main.yml` for some variables that you can customize via your `vars.yml` file

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

To use the bot, invite it to the room you specified on your `vars.yml` file (`/invite @bot.chatgpt:example.com` where `example.com` is your base domain, not the `matrix.` domain).

After the bot joins the room, you can send a message to it. When you do so, use the prefix if you configured it or mention the bot.

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-bot-chatgpt`.
