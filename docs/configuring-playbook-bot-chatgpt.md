# Setting up ChatGPT (optional)

The playbook can install and configure [matrix-chatgpt-bot](https://github.com/matrixgpt/matrix-chatgpt-bot) for you.

Talk to ChatGPT via your favourite Matrix client!


## 1. Register the bot account

The playbook does not automatically create users for you. The bot requires an access token to be able to connect to your homeserver.

You **need to register the bot user manually** before setting up the bot.

Choose a strong password for the bot. You can generate a good password with a command like this: `pwgen -s 64 1`.

You can use the playbook to [register a new user](registering-users.md):

```
ansible-playbook -i inventory/hosts setup.yml --extra-vars='username=bot.chatgpt password=PASSWORD_FOR_THE_BOT admin=no' --tags=register-user
```


## 2. Get an access token

Refer to the documentation on [how to obtain an access token](obtaining-access-tokens.md).


## 3. Adjusting the playbook configuration

Add the following configuration to your `inventory/host_vars/matrix.DOMAIN/vars.yml` file (adapt to your needs):

```yaml
matrix_bot_chatgpt_enabled: true
# See instructions on
# https://www.npmjs.com/package/chatgpt
matrix_bot_chatgpt_openai_email: ''
matrix_bot_chatgpt_openai_password: ''
matrix_bot_chatgpt_openai_login_type: google
# With the @ and :DOMAIN, ie @SOMETHING:DOMAIN
matrix_bot_chatgpt_matrix_bot_username: '@bot.chatgpt:{{ matrix_domain }}'
# Matrix access token (from bot user above)
# see: https://webapps.stackexchange.com/questions/131056/how-to-get-an-access-token-for-element-riot-matrix
matrix_bot_chatgpt_matrix_access_token: ''
matrix_bot_chatgpt_matrix_default_prefix: '!chatgpt '
matrix_bot_chatgpt_matrix_default_prefix_reply: false
matrix_bot_chatgpt_matrix_whitelist: ':{{ matrix_domain }}'
```

You will need to get tokens for ChatGPT.


## 4. Installing

After configuring the playbook, run the [installation](installing.md) command again:

```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

**Notes**:

- if you change the bot password (`matrix_bot_chatgpt_matrix_password` in your `vars.yml` file) subsequently, the bot user's credentials on the homeserver won't be updated automatically. If you'd like to change the bot user's password, use a tool like [synapse-admin](configuring-playbook-synapse-admin.md) to change it, and then update `matrix_bot_chatgpt_matrix_password` to let the bot know its new password


## Usage

To use the bot, invite the `@bot.chatgpt:DOMAIN` to the room you specified in a config, after that start speaking to it, use the prefix if you configured one or mention the bot.

You can also refer to the upstream [documentation](https://github.com/matrixgpt/matrix-chatgpt-bot).
