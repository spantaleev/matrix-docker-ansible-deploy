# Installing

If you've [configured your DNS](configuring-dns.md) and have [configured the playbook](configuring-playook.md), you can start the installation procedure.

Run this as-is to set up a server:

```bash
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all
```

This **doesn't start any services just yet** (another step does this later - below).

Feel free to **re-run this any time** you think something is off with the server configuration.


# Things you might want to do after installing

After installing, but before starting the services, you may want to do additional things like:

- [Importing an existing SQLite database (from another installation)](importing-sqlite.md) (optional)

- [Restoring `media_store` data files from an existing installation](restoring-media-store.md) (optional)


# Starting the services

When you're ready to start the Matrix services (and set them up to auto-start in the future):

```bash
ansible-playbook -i inventory/hosts setup.yml --tags=start
```

Now that the services are running, you might want to [create your first user account](registering-users.md)