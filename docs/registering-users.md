# Registering users

This documentation page tells you how to create user account on your Matrix server.

Table of contents:

- [Registering users](#registering-users)
	- [Registering users manually](#registering-users-manually)
	- [Managing users via a Web UI](#managing-users-via-a-web-ui)
	- [Letting certain users register on your private server](#letting-certain-users-register-on-your-private-server)
	- [Enabling public user registration](#enabling-public-user-registration)
	- [Adding/Removing Administrator privileges to an existing Synapse user](#addingremoving-administrator-privileges-to-an-existing-synapse-user)


## Registering users manually

You can do it via this Ansible playbook (make sure to edit the `<your-username>` and `<your-password>` part below):

```
ansible-playbook -i inventory/hosts setup.yml --extra-vars='username=<your-username> password=<your-password> admin=<yes|no>' --tags=register-user
```

**or** using the command-line after **SSH**-ing to your server (requires that [all services have been started](#starting-the-services)):

```
/matrix/synapse/bin/register-user <your-username> <your-password> <admin access: 0 or 1>
```

**Note**: `<your-username>` is just a plain username (like `john`), not your full `@<username>:<your-domain>` identifier.

**You can then log in with that user** via the Element service that this playbook has created for you at a URL like this: `https://element.<domain>/`.

-----

If you've just installed Matrix, **to finalize the installation process**, it's best if you proceed to [Configuring service discovery via .well-known](configuring-well-known.md)


## Managing users via a Web UI

To manage users more easily (via a web user-interace), you can install [Synapse Admin](configuring-playbook-synapse-admin.md).


## Letting certain users register on your private server

If you'd rather **keep your server private** (public registration closed, as is the default), and **let certain people create accounts by themselves** (instead of creating user accounts manually like this), consider installing and making use of [matrix-registration](configuring-playbook-matrix-registration.md).


## Enabling public user registration

To **open up user registration publicly** (usually **not recommended**), consider using the following configuration:

```yaml
matrix_synapse_enable_registration: true
```

and running the [installation](installing.md) procedure once again.

If you're opening up registrations publicly like this, you might also wish to [configure CAPTCHA protection](configuring-captcha.md).


## Adding/Removing Administrator privileges to an existing Synapse user

To change the admin privileges for a user, you need to run an SQL query like this against the `synapse` database:

```sql
UPDATE users SET admin=ADMIN_VALUE WHERE name = '@USER:DOMAIN'
```

where:

- `ADMIN_VALUE` being either `0` (regular user) or `1` (admin)
- `USER` and `DOMAIN` pointing to a valid user on your server

If you're using the integrated Postgres server and not an [external Postgres server](configuring-playbook-external-postgres.md), you can launch a Postgres into the `synapse` database by:

- running `/matrix/postgres/bin/cli` - to launch [`psql`](https://www.postgresql.org/docs/current/app-psql.html)
- running `\c synapse` - to change to the `synapse` database

You can then proceed to run the query above.

**Note**: directly modifying the raw data of Synapse (or any other software) could cause the software to break. You've been warned!
