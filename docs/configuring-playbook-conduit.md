# Configuring Conduit (optional)

By default, this playbook configures the [Synapse](https://github.com/matrix-org/synapse) Matrix server, but you can also use [Conduit](https://conduit.rs).

**NOTES**:

- **You can't switch an existing Matrix server's implementation** (e.g. Synapse -> Conduit). Proceed below only if you're OK with losing data or you're dealing with a server on a new domain name, which hasn't participated in the Matrix federation yet.

- **homeserver implementations other than Synapse may not be fully functional**. The playbook may also not assist you in an optimal way (like it does with Synapse). Make yourself familiar with the downsides before proceeding


## Installation

To use Conduit, you **generally** need the following additional `vars.yml` configuration:

```yaml
matrix_homeserver_implementation: conduit
```

However, since Conduit is difficult (see [famedly/conduit#276](https://gitlab.com/famedly/conduit/-/issues/276) and [famedly/conduit#354](https://gitlab.com/famedly/conduit/-/merge_requests/354)) when it comes to creating the first user account and does not support [registering users](registering-users.md) (via the command line or via the playbook) like Synapse and Dendrite do, we recommend the following flow:

1. Add `matrix_conduit_allow_registration: true` to your `vars.yml` the first time around, temporarily
2. Run the playbook (`ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start` - see [Installing](installing.md))
3. Create your first user via Element or any other client which supports creating users
4. Get rid of `matrix_conduit_allow_registration: true` from your `vars.yml`
5. Run the playbook again (`ansible-playbook -i inventory/hosts setup.yml --tags=setup-conduit,start` would be enough this time)
6. You can now use your server safely. Additional users can be created by messaging the internal Conduit bot


## Configuring bridges / appservices

Automatic appservice setup is currently unsupported when using conduit. After setting up the service as usual you may notice that it is unable to start.

You will have to manually register appservices using the the [register-appservice](https://gitlab.com/famedly/conduit/-/blob/next/APPSERVICES.md) command.

Find the `registration.yaml` in the `/matrix` directory, for example `/matrix/mautrix-signal/bridge/registration.yaml`, then pass the content to conduit:


    @conduit:your.server.name: register-appservice
    ```
    as_token: <token>
    de.sorunome.msc2409.push_ephemeral: true
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

