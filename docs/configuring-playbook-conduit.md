<!--
SPDX-FileCopyrightText: 2022 - 2025 Slavi Pantaleev
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Configuring Conduit (optional)

The playbook can install and configure the [Conduit](https://conduit.rs) Matrix server for you.

See the project's [documentation](https://docs.conduit.rs/) to learn what it does and why it might be useful to you.

By default, the playbook installs [Synapse](https://github.com/element-hq/synapse) as it's the only full-featured Matrix server at the moment. If that's okay, you can skip this document.

💡 **Note**: The playbook also supports installing a (currently) faster-moving Conduit fork called [conduwuit](./configuring-playbook-conduwuit.md).

> [!WARNING]
> - **You can't switch an existing Matrix server's implementation** (e.g. Synapse -> Conduit). Proceed below only if you're OK with losing data or you're dealing with a server on a new domain name, which hasn't participated in the Matrix federation yet.
> - **Homeserver implementations other than Synapse may not be fully functional**. The playbook may also not assist you in an optimal way (like it does with Synapse). Make yourself familiar with the downsides before proceeding

## Adjusting the playbook configuration

To use Conduit, you **generally** need to adjust the `matrix_homeserver_implementation: synapse` configuration on your `inventory/host_vars/matrix.example.com/vars.yml` file as below:

```yaml
matrix_homeserver_implementation: conduit
```

### Extending the configuration

There are some additional things you may wish to configure about the server.

Take a look at:

- `roles/custom/matrix-conduit/defaults/main.yml` for some variables that you can customize via your `vars.yml` file
- `roles/custom/matrix-conduit/templates/conduit.toml.j2` for the server's default configuration

If you'd like to have your own different configuration, feel free to copy and paste the original files into your inventory (e.g. in `inventory/host_vars/matrix.example.com/`) and then change the specific host's `vars.yml` file like this:

```yaml
matrix_conduit_template_conduit_config: "{{ playbook_dir }}/inventory/host_vars/matrix.example.com/conduit.toml.j2"
```

## Creating the first user account

Since it is difficult to create the first user account on Conduit (see [famedly/conduit#276](https://gitlab.com/famedly/conduit/-/issues/276) and [famedly/conduit#354](https://gitlab.com/famedly/conduit/-/merge_requests/354)) and it does not support [registering users](registering-users.md) (via the command line or via the playbook) like Synapse and Dendrite do, we recommend the following procedure:

1. Add `matrix_conduit_allow_registration: true` to your `vars.yml` the first time around, temporarily
2. Run the playbook (`ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start` — see [Installing](installing.md))
3. Create your first user via Element Web or any other client which supports creating users
4. Get rid of `matrix_conduit_allow_registration: true` from your `vars.yml`
5. Run the playbook again (`ansible-playbook -i inventory/hosts setup.yml --tags=setup-conduit,start` would be enough this time)
6. You can now use your server safely. Additional users can be created by messaging the internal Conduit bot

## Configuring bridges / appservices

For other homeserver implementations (like Synapse and Dendrite), the playbook automatically registers appservices (for bridges, bots, etc.) with the homeserver.

For Conduit, you will have to manually register appservices using the the [register-appservice](https://gitlab.com/famedly/conduit/-/blob/next/APPSERVICES.md) command.

Find the `registration.yaml` in the `/matrix` directory, for example `/matrix/mautrix-signal/bridge/registration.yaml`, then pass the content to Conduit:

    @conduit:example.com: register-appservice
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

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-conduit`.
