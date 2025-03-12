<!--
SPDX-FileCopyrightText: 2019 - 2020 Aaron Raimist
SPDX-FileCopyrightText: 2019 Lyubomir Popov
SPDX-FileCopyrightText: 2020 - 2024 Slavi Pantaleev
SPDX-FileCopyrightText: 2020 MDAD project contributors
SPDX-FileCopyrightText: 2022 Dennis Ciba
SPDX-FileCopyrightText: 2022 Marko Weltzer
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Updating users passwords

## Option 1 (if you are using the integrated Postgres database):

**Notes**:
- Make sure to adjust `USERNAME_HERE` and `PASSWORD_HERE`
- For `USERNAME_HERE`, use a plain username like `alice`, not a full ID (`@alice:example.com`)

You can reset a user's password via the Ansible playbook:

```sh
ansible-playbook -i inventory/hosts setup.yml --extra-vars='username=USERNAME_HERE password=PASSWORD_HERE' --tags=update-user-password
```

**You can then log in with that user** via Element Web that this playbook has created for you at a URL like this: `https://element.example.com/`.

## Option 2 (if you are using an external Postgres server):

You can manually generate the password hash by using the command-line after **SSH**-ing to your server (requires that [all services have been started](installing.md#finalize-the-installation):

```sh
docker exec -it matrix-synapse /usr/local/bin/hash_password -c /data/homeserver.yaml
```

and then connecting to the Postgres server and executing:

```sql
UPDATE users SET password_hash = '<password-hash>' WHERE name = '@alice:example.com';
```

where `<password-hash>` is the hash returned by the docker command above.

## Option 3:

Use the Synapse User Admin API as described here: https://github.com/element-hq/synapse/blob/master/docs/admin_api/user_admin_api.rst#reset-password

This requires an [access token](obtaining-access-tokens.md) from a server admin account. *This method will also log the user out of all of their clients while the other options do not.*

If you didn't make your account a server admin when you created it, you can learn how to switch it now by reading about it in [Adding/Removing Administrator privileges to an existing user in Synapse](registering-users.md#addingremoving-administrator-privileges-to-an-existing-user-in-synapse).

### Example:

To set @alice:example.com's password to `correct_horse_battery_staple` you could use this curl command:

```sh
curl -XPOST -d '{ "new_password": "correct_horse_battery_staple" }' "https://matrix.example.com/_matrix/client/r0/admin/reset_password/@alice:example.com?access_token=ACCESS_TOKEN_HERE
```

Make sure to replace `ACCESS_TOKEN_HERE` with the access token of the server admin account.
