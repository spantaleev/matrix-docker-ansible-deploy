# Setting up ChatGPT (optional)

The playbook can install and configure [matrix-chatgpt-bot](https://github.com/matrixgpt/matrix-chatgpt-bot) for you.

Talk to [ChatGPT](https://openai.com/blog/chatgpt/) via your favourite Matrix client!

**Note**: [matrix-chatgpt-bot](https://github.com/matrixgpt/matrix-chatgpt-bot) is now an archived (**unmaintained**) project. Talking to ChatGPT (and many other LLM providers) can happen via the much more featureful [baibot](./configuring-playbook-bot-baibot.md) bot supported by the playbook.


## 1. Register the bot account

The playbook does not automatically create users for you. The bot requires an access token to be able to connect to your homeserver.

You **need to register the bot user manually** before setting up the bot.

Choose a strong password for the bot. You can generate a good password with a command like this: `pwgen -s 64 1`.

You can use the playbook to [register a new user](registering-users.md):

```
ansible-playbook -i inventory/hosts setup.yml --extra-vars='username=bot.chatgpt password=PASSWORD_FOR_THE_BOT admin=no' --tags=register-user
```


## 2. Get an access token and create encryption keys

Refer to the documentation on [how to obtain an access token](obtaining-access-tokens.md).

To make sure the bot can read encrypted messages, it will need an encryption key, just like any other new user. While obtaining the access token, follow the prompts to setup a backup key. More information can be found in the [element documentation](https://element.io/help#encryption6).


## 3. Adjusting the playbook configuration

Add the following configuration to your `inventory/host_vars/matrix.DOMAIN/vars.yml` file (adapt to your needs):

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

After configuring the playbook, run the [installation](installing.md) command again:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=install-all,start
```


## Usage

To use the bot, invite the `@bot.chatgpt:DOMAIN` to the room you specified in a config, after that start speaking to it, use the prefix if you configured one or mention the bot.

You can also refer to the upstream [documentation](https://github.com/matrixgpt/matrix-chatgpt-bot).
