# Setting up Cactus Comments (optional)

The playbook can install and configure [Cactus Comments](https://cactus.chat) for you.

Cactus Comments is a **federated comment system** built on Matrix. The role allows you to self-host the system.
It respects your privacy, and puts you in control.

See the project's [documentation](https://cactus.chat/docs/getting-started/introduction/) to learn what it
does and why it might be useful to you.


## Configuration

Add the following block to your `vars.yaml` and make sure to exchange the tokens to randomly generated values.

```ỳaml
#################
## Cactus Chat ##
#################

matrix_cactus_comments_enabled: true

# To allow guest comments without users needing to log in, you need to have guest registration enabled.
# To do this you need to uncomment one of the following lines (depending if you are using synapse or dentrite as a homeserver)
# If you don't know which one you use: The default is synapse ;)
# matrix_synapse_allow_guest_access: true
# matrix_dentrite_allow_guest_access
```

## Installing

After configuring the playbook, run the [installation](installing.md) command again:

```
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```


## Usage

To learn how to use cactus comments message @bot.cactusbot:your-homeserver.com and type `help` or have a look in the [documentation](https://cactus.chat/docs/getting-started/quick-start/).
