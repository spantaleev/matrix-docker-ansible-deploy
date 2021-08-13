# Registering users

This documentation page tells you how to create user account on your Matrix server.

Table of contents:

- [Registering users](#registering-users)
	- [Registering users manually](#registering-users-manually)
	- [Managing users via a Web UI](#managing-users-via-a-web-ui)
	- [Letting certain users register on your private server](#letting-certain-users-register-on-your-private-server)
	- [Enabling public user registration](#enabling-public-user-registration)
	- [Adding/Removing Administrator privileges to an existing user](#addingremoving-administrator-privileges-to-an-existing-user)


## Registering users manually

You can do it via this Ansible playbook (make sure to edit the `<your-username>` and `<your-password>` part below):

```
ansible-playbook -i inventory/hosts setup.yml --extra-vars='username=<your-username> password=<your-password> admin=<yes|no>' --tags=register-user
```

**or** using the command-line after **SSH**-ing to your server (requires that [all services have been started](#starting-the-services)):

```
/usr/local/bin/matrix-synapse-register-user <your-username> <your-password> <admin access: 0 or 1>
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


## Adding/Removing Administrator privileges to an existing user

The script `/usr/local/bin/matrix-change-user-admin-status` may be used to change a user's admin privileges.

* log on to your server with ssh
* execute with the username and 0/1 (0 = non-admin | 1 = admin)

```
/usr/local/bin/matrix-change-user-admin-status <username> <0/1>
```
