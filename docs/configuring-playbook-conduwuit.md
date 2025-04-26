<!--
SPDX-FileCopyrightText: 2025 Slavi Pantaleev
SPDX-FileCopyrightText: 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Configuring conduwuit (optional)

The playbook can install and configure the [conduwuit](https://conduwuit.puppyirl.gay/) Matrix server for you.

See the project's [documentation](https://conduwuit.puppyirl.gay/) to learn what it does and why it might be useful to you.

By default, the playbook installs [Synapse](https://github.com/element-hq/synapse) as it's the only full-featured Matrix server at the moment. If that's okay, you can skip this document.

💡 **Note**: conduwuit is a fork of [Conduit](./configuring-playbook-conduit.md), which the playbook also supports. See [Differences from upstream Conduit](https://conduwuit.puppyirl.gay/differences.html).

> [!WARNING]
> - **You can't switch an existing Matrix server's implementation** (e.g. Synapse -> conduwuit). Proceed below only if you're OK with losing data or you're dealing with a server on a new domain name, which hasn't participated in the Matrix federation yet.
> - **Homeserver implementations other than Synapse may not be fully functional**. The playbook may also not assist you in an optimal way (like it does with Synapse). Make yourself familiar with the downsides before proceeding
> - **the Conduwuit project appears to have been abandoned**. You may wish to install [Conduit](./configuring-playbook-conduit.md), or one of the Conduwuit successors (like [Continuwuity](configuring-playbook-continuwuity.md))

## Adjusting the playbook configuration

To use conduwuit, you **generally** need to adjust the `matrix_homeserver_implementation: synapse` configuration on your `inventory/host_vars/matrix.example.com/vars.yml` file as below:

```yaml
matrix_homeserver_implementation: conduwuit

# Registering users can only happen via the API,
# so it makes sense to enable it, at least initially.
matrix_conduwuit_config_allow_registration: true

# Generate a strong registration token to protect the registration endpoint from abuse.
# You can create one with a command like `pwgen -s 64 1`.
matrix_conduwuit_config_registration_token: ''
```

### Extending the configuration

There are some additional things you may wish to configure about the server.

Take a look at:

- `roles/custom/matrix-conduwuit/defaults/main.yml` for some variables that you can customize via your `vars.yml` file
- `roles/custom/matrix-conduwuit/templates/conduwuit.toml.j2` for the server's default configuration

There are various Ansible variables that control settings in the `conduwuit.toml` file.

If a specific setting you'd like to change does not have a dedicated Ansible variable, you can either submit a PR to us to add it, or you can [override the setting using an environment variable](https://conduwuit.puppyirl.gay/configuration.html#environment-variables) using `matrix_conduwuit_environment_variables_extension`. For example:

```yaml
matrix_conduwuit_environment_variables_extension: |
  CONDUWUIT_MAX_REQUEST_SIZE=50000000
  CONDUWUIT_REQUEST_TIMEOUT=60
```

## Creating the first user account

Unlike other homeserver implementations (like Synapse and Dendrite), conduwuit does not support creating users via the command line or via the playbook.

If you followed the instructions above (see [Adjusting the playbook configuration](#adjusting-the-playbook-configuration)), you should have registration enabled and protected by a registration token.

This should allow you to create the first user account via any client (like [Element Web](./configuring-playbook-client-element-web.md)) which supports creating users.

The **first user account that you create will be marked as an admin** and **will be automatically invited to an admin room**.


## Configuring bridges / appservices

For other homeserver implementations (like Synapse and Dendrite), the playbook automatically registers appservices (for bridges, bots, etc.) with the homeserver.

For conduwuit, you will have to manually register appservices using the [`!admin appservices register` command](https://conduwuit.puppyirl.gay/appservices.html#set-up-the-appservice---general-instructions) sent to the server bot account.

The server's bot account has a Matrix ID of `@conduit:example.com` (not `@conduwuit:example.com`!) due to conduwuit's historical legacy.
Your first user account would already have been invited to an admin room with this bot.

Find the appservice file you'd like to register. This can be any `registration.yaml` file found in the `/matrix` directory, for example `/matrix/mautrix-signal/bridge/registration.yaml`.

Then, send its content to the existing admin room:

    !admin appservices register

    ```
    as_token: <token>
    de.sorunome.msc2409.push_ephemeral: true
    receive_ephemeral: true
    hs_token: <token>
    id: signal
    namespaces:
      aliases:
      - exclusive: true
        regex: ^#signal_.+:example\.org$
      users:
      - exclusive: true
        regex: ^@signal_.+:example\.org$
      - exclusive: true
        regex: ^@signalbot:example\.org$
    rate_limited: false
    sender_localpart: _bot_signalbot
    url: http://matrix-mautrix-signal:29328
    ```

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-conduwuit`.
