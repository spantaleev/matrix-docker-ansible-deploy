# Setting up matrix-bot-chatgpt (optional, unmaintained)

**Note**: [matrix-chatgpt-bot](https://github.com/matrixgpt/matrix-chatgpt-bot) is now an archived (**unmaintained**) project. Talking to ChatGPT (and many other LLM providers) can happen via the much more featureful [baibot](https://github.com/etkecc/baibot), which can be installed using [this playbook](configuring-playbook-bot-baibot.md). Consider using that bot instead of this one.

The playbook can install and configure [matrix-chatgpt-bot](https://github.com/matrixgpt/matrix-chatgpt-bot) for you.

Talk to [ChatGPT](https://openai.com/blog/chatgpt/) via your favourite Matrix client!

## 1. Register the bot account

The playbook does not automatically create users for you. The bot requires an access token to be able to connect to your homeserver.

You **need to register the bot user manually** before setting up the bot.

Choose a strong password for the bot. You can generate a good password with a command like this: `pwgen -s 64 1`.

You can use the playbook to [register a new user](registering-users.md):

```sh
ansible-playbook -i inventory/hosts setup.yml --extra-vars='username=bot.chatgpt password=PASSWORD_FOR_THE_BOT admin=no' --tags=register-user
```

## 2. Get an access token and create encryption keys

Refer to the documentation on [how to obtain an access token](obtaining-access-tokens.md).

To make sure the bot can read encrypted messages, it will need an encryption key, just like any other new user. While obtaining the access token, follow the prompts to setup a backup key. More information can be found in the [Element documentation](https://element.io/help#encryption6).

## 3. Adjusting the playbook configuration

Add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file (adapt to your needs):

```yaml
matrix_bot_chatgpt_enabled: true

# Obtain a new API key from https://platform.openai.com/account/api-keys
matrix_bot_chatgpt_openai_api_key: ''

# This is the default username
# matrix_bot_chatgpt_matrix_bot_username_localpart: 'bot.chatgpt'

# Matrix access token (from bot user above)
# see: https://webapps.stackexchange.com/questions/131056/how-to-get-an-access-token-for-element-riot-matrix
matrix_bot_chatgpt_matrix_access_token: ''

# Configuring the system promt used, needed if the bot is used for special tasks.
# More information: https://github.com/mustvlad/ChatGPT-System-Prompts
matrix_bot_chatgpt_matrix_bot_prompt_prefix: 'Instructions:\nYou are ChatGPT, a large language model trained by OpenAI.'

```

You will need to get tokens for ChatGPT.

## 4. Installing

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

To use the bot, invite the `@bot.chatgpt:example.com` to the room you specified in a config, after that start speaking to it, use the prefix if you configured one or mention the bot.

You can also refer to the upstream [documentation](https://github.com/matrixgpt/matrix-chatgpt-bot).
