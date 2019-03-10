# Installing

If you've [configured your DNS](configuring-dns.md) and have [configured the playbook](configuring-playbook.md), you can start the installation procedure.

Run this as-is to set up a server:

```bash
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all
```

This **doesn't start any services just yet** (another step does this later - below).

Feel free to **re-run this any time** you think something is off with the server configuration.


## Things you might want to do after installing

After installing, but before starting the services, you may want to do additional things like:

- [Importing an existing SQLite database (from another installation)](importing-sqlite.md) (optional)

- [Importing an existing Postgres database (from another installation)](importing-postgres.md) (optional)

- [Importing `media_store` data files from an existing installation](importing-media-store.md) (optional)


## Starting the services

When you're ready to start the Matrix services (and set them up to auto-start in the future):

```bash
ansible-playbook -i inventory/hosts setup.yml --tags=start
```

Now that the services are running, you might want to:

- **finalize the installation process** (required for federation to work!) by [Configuring Service Discovery via .well-known](configuring-well-known.md)
- or [create your first user account](registering-users.md)
- or [set up the Dimension Integrations Manager](configuring-playbook-dimension.md)
- or [check if services work](maintenance-checking-services.md)
- or learn how to [upgrade your services when new versions are released](maintenance-upgrading-services.md)
