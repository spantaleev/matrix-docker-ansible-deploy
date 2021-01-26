# Installing

If you've [configured your DNS](configuring-dns.md) and have [configured the playbook](configuring-playbook.md), you can start the installation procedure.

Run this as-is to set up a server:

```bash
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all
```

**Note**: if you don't use SSH keys for authentication, but rather a regular password, you may need to add `--ask-pass` to the above (and all other) Ansible commands.

**Note**: if you **do** use SSH keys for authentication, **and** use a non-root user to *become* root (sudo), you may need to add `-K` (`--ask-become-pass`) to the above (and all other) Ansible commands.

The above command **doesn't start any services just yet** (another step does this later - below).

Feel free to **re-run this setup command any time** you think something is off with the server configuration.


## Things you might want to do after installing

After installing, but before starting the services, you may want to do additional things like:

- [Importing an existing SQLite database (from another Synapse installation)](importing-synapse-sqlite.md) (optional)

- [Importing an existing Postgres database (from another installation)](importing-postgres.md) (optional)

- [Importing `media_store` data files from an existing Synapse installation](importing-synapse-media-store.md) (optional)


## Starting the services

When you're ready to start the Matrix services (and set them up to auto-start in the future):

```bash
ansible-playbook -i inventory/hosts setup.yml --tags=start
```

Now that services are running, you need to **finalize the installation process** (required for federation to work!) by [Configuring Service Discovery via .well-known](configuring-well-known.md)


## Things to do next

If you have started services and **finalized the installation process** (required for federation to work!) by [Configuring Service Discovery via .well-known](configuring-well-known.md), you can:

- [check if services work](maintenance-checking-services.md)
- or [create your first Matrix user account](registering-users.md)
- or [set up additional services](configuring-playbook.md#other-configuration-options) (bridges to other chat networks, bots, etc.)
- or learn how to [upgrade services when new versions are released](maintenance-upgrading-services.md)
- or learn how to [maintain your server](faq.md#maintenance)
- or join some Matrix rooms:
  * via the *Explore rooms* feature in Element or some other client, or by discovering them using this [matrix-static list](https://view.matrix.org). Note: joining large rooms may overload small servers.
  * or come say Hi in our support room - [#matrix-docker-ansible-deploy:devture.com](https://matrix.to/#/#matrix-docker-ansible-deploy:devture.com). You might learn something or get to help someone else new to Matrix hosting.
- or help make this playbook better by contributing (code, documentation, or [coffee/beer](https://liberapay.com/s.pantaleev/donate))
