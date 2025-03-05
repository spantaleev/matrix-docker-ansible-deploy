<!--
SPDX-FileCopyrightText: 2018 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2018 - 2025 MDAD project contributors
SPDX-FileCopyrightText: 2019 Aaron Raimist
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara
SPDX-FileCopyrightText: 2024 Dark Decoy

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Registering users

This documentation page tells you how to create user accounts on your Matrix server.

Table of contents:
- [Registering users](#registering-users)
	- [Registering users manually](#registering-users-manually)
	- [Managing users via a Web UI](#managing-users-via-a-web-ui)
	- [Letting certain users register on your private server](#letting-certain-users-register-on-your-private-server)
	- [Enabling public user registration](#enabling-public-user-registration)
	- [Adding/Removing Administrator privileges to an existing user](#addingremoving-administrator-privileges-to-an-existing-user)

## Registering users manually

**Notes**:
- Make sure to adjust `USERNAME_HERE` and `PASSWORD_HERE`
- For `USERNAME_HERE`, use a plain username like `alice`, not a full ID (`@alice:example.com`)
- Use `admin=yes` or `admin=no` depending on whether you wish to make the user an administrator of the Matrix server

After registering a user (using one of the methods below), **you can log in with that user** via the [Element Web](configuring-playbook-client-element-web.md) service that this playbook has installed for you at a URL like this: `https://element.example.com/`.

### Registering users via the Ansible playbook

It's best to register users via the Ansible playbook, because it works regardless of homeserver implementation (Synapse, Dendrite, etc) or usage of [Matrix Authentication Service](configuring-playbook-matrix-authentication-service.md) (MAS).

To register a user via this Ansible playbook:

```sh
just register-user USERNAME_HERE PASSWORD_HERE <admin access: yes or no>

# Example: `just register-user alice secret-password yes`
```

**or** by invoking `ansible-playbook` manually:

```sh
ansible-playbook -i inventory/hosts setup.yml --extra-vars='username=USERNAME_HERE password=PASSWORD_HERE admin=<yes|no>' --tags=register-user

# Example: ansible-playbook -i inventory/hosts setup.yml --extra-vars='username=alice password=secret-password admin=yes' --tags=register-user
```

Feel free to register as many users (for friends, family, etc.) as you want. Still, perhaps you should grant full administrative access to your user account only (with `admin=yes`), and others should be created with `admin=no`.

> [!WARNING]
> If you're registering users against Matrix Authentication Service, do note that it [still insists](https://github.com/element-hq/matrix-authentication-service/issues/1505) on having a verified email address for each user. Upon a user's first login, they will be asked to confirm their email address. This requires that email sending is [configured](./configuring-playbook-email.md). You can also consult the [Working around email deliverability issues](./configuring-playbook-matrix-authentication-service.md#working-around-email-deliverability-issues) section for more information.

### Registering users manually for Synapse

If you're using the [Synapse](configuring-playbook-synapse.md) homeserver implementation (which is the default), you can register users via the command-line after **SSH**-ing to your server (requires that [all services have been started](installing.md#install-matrix-server-and-services)):

```sh
/matrix/synapse/bin/register-user USERNAME_HERE PASSWORD_HERE <admin access: 0 or 1>

# Example: `/matrix/synapse/bin/register-user alice secret-password 1`
```

### Registering users manually for Dendrite

If you're using the [Dendrite](./configuring-playbook-dendrite.md) homeserver implementation, you can register users via the command-line after **SSH**-ing to your server (requires that [all services have been started](installing.md#install-matrix-server-and-services)):

```sh
/matrix/dendrite/bin/create-account USERNAME_HERE PASSWORD_HERE <admin access: 0 or 1>

# Example: `/matrix/dendrite/bin/create-account alice secret-password 1`
```

### Registering users manually for Matrix Authentication Service

If you're using the [Matrix Authentication Service](./configuring-playbook-matrix-authentication-service.md) and your existing homeserver (most likely [Synapse](./configuring-playbook-synapse.md)) is delegating authentication to it, you can register users via the command-line after **SSH**-ing to your server (requires that [all services have been started](installing.md#install-matrix-server-and-services)):

```sh
/matrix/matrix-authentication-service/bin/register-user USERNAME_HERE PASSWORD_HERE <admin access: 0 or 1>

# Example: `/matrix/matrix-authentication-service/bin/register-user alice secret-password 1`
```

This `register-user` script actually invokes the `mas-cli manage register-user` command under the hood. If you'd like more control over the registration process, consider invoking the `mas-cli` command directly:

```sh
/matrix/matrix-authentication-service/bin/mas-cli manage register-user --help
```

> [!WARNING]
> Matrix Authentication Service [still insists](https://github.com/element-hq/matrix-authentication-service/issues/1505) on having a verified email address for each user. Upon a user's first login, they will be asked to confirm their email address. This requires that email sending is [configured](./configuring-playbook-email.md). You can also consult the [Working around email deliverability issues](./configuring-playbook-matrix-authentication-service.md#working-around-email-deliverability-issues) section for more information.

## Managing users via a Web UI

To manage users more easily (via a web user-interace), you can install [Synapse Admin](configuring-playbook-synapse-admin.md).

> [!WARNING]
> If you're using [Matrix Authentication Service](configuring-playbook-matrix-authentication-service.md), note that user management via synapse-admin is not fully working yet. See the [Expectations](configuring-playbook-matrix-authentication-service.md#expectations) section for more information.

## Letting certain users register on your private server

If you'd rather **keep your server private** (public registration closed, as is the default), and **let certain people create accounts by themselves** (instead of creating user accounts manually like this), consider installing and making use of [matrix-registration](configuring-playbook-matrix-registration.md).

## Enabling public user registration

To **open up user registration publicly** (usually **not recommended**), add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

For Synapse:

```yaml
matrix_synapse_enable_registration: true
```

For Dendrite:

```yaml
matrix_dendrite_client_api_registration_disabled: false
```

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

**Notes**:

- The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

  `just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

- If you're opening up registrations publicly like this, you might also wish to [configure CAPTCHA protection](configuring-captcha.md).

## Adding/Removing Administrator privileges to an existing user

### Adding/Removing Administrator privileges to an existing user in Synapse

To change the admin privileges for a user in Synapse's local database, you need to run an SQL query like this against the `synapse` database:

```sql
UPDATE users SET admin=ADMIN_VALUE WHERE name = '@alice:example.com';
```

where:

- `ADMIN_VALUE` being either `0` (regular user) or `1` (admin)
- `USER` and `example.com` pointing to a valid user on your server

If you're using the integrated Postgres server and not an [external Postgres server](configuring-playbook-external-postgres.md), you can launch a Postgres into the `synapse` database by:

- running `/matrix/postgres/bin/cli` — to launch [`psql`](https://www.postgresql.org/docs/current/app-psql.html)
- running `\c synapse` — to change to the `synapse` database

You can then proceed to run the query above.

**Note**: directly modifying the raw data of Synapse (or any other software) could cause the software to break. You've been warned!

### Adding/Removing Administrator privileges to an existing user in Matrix Authentication Service

Promoting/demoting a user in Matrix Authentication Service cannot currently (2024-10-19) be done via the [`mas-cli` Management tool](./configuring-playbook-matrix-authentication-service.md#management).

You can do it via the [MAS Admin API](https://element-hq.github.io/matrix-authentication-service/api/index.html)'s `POST /api/admin/v1/users/{id}/set-admin` endpoint.
