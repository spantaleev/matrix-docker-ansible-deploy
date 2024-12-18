# Setting up Email2Matrix (optional)

**Note**: email bridging can also happen via the [Postmoogle](configuring-playbook-bridge-postmoogle.md) bridge supported by the playbook. Postmoogle is much more powerful and easier to use, so we recommend that you use it, instead of Email2Matrix.

The playbook can install and configure [email2matrix](https://github.com/devture/email2matrix) for you.

See the project's [documentation](https://github.com/devture/email2matrix/blob/master/docs/README.md) to learn what it does and why it might be useful to you.

## Preparation

### DNS configuration

It's not strictly necessary, but you may increase the chances that incoming emails reach your server by adding an `MX` record for `matrix.example.com`, as described in the [Configuring DNS](configuring-dns.md) documentation page.

### Port availability

Ensure that port 25 is available on your Matrix server and open in your firewall.

If you have `postfix` or some other email server software installed, you may need to manually remove it first (unless you need it, of course).

If you really need to run an email server on the Matrix machine for other purposes, it may be possible to run Email2Matrix on another port (with a configuration like `matrix_email2matrix_smtp_host_bind_port: "127.0.0.01:2525"`) and have your other email server relay messages there.

For details about using Email2Matrix alongside [Postfix](http://www.postfix.org/), see [here](https://github.com/devture/email2matrix/blob/master/docs/setup_with_postfix.md).

### Creating a user

Before enabling Email2Matrix, you'd most likely wish to create a dedicated user (or more) that would be sending messages on the Matrix side. Take note of the user's ID as it needs to be specified as `MatrixUserId` on your `inventory/host_vars/matrix.example.com/vars.yml` file later.

Refer to [Registering users](registering-users.md) for ways to create a user. A regular (non-admin) user works best.

### Creating a shared room

After creating the sender user, you should create one or more Matrix rooms that you share with that user. It doesn't matter who creates and owns the rooms and who joins later (you or the sender user).

What matters is that both you and the sender user are part of the same room and that the sender user has enough privileges in the room to be able to send messages there.

Inviting additional people to the room is okay too.

Take note of each room's room ID (different clients show the room ID in a different place). You'll need the room ID when [configuring the playbook](#adjusting-the-playbook-configuration) below.

### Obtaining an access token for the sender user

In order for the sender user created above to be able to send messages to the room, we'll need to obtain an access token for it. Refer to the documentation on [how to obtain an access token](obtaining-access-tokens.md).

## Adjusting the playbook configuration

After doing the preparation steps above, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file (adapt to your needs):

```yaml
matrix_email2matrix_enabled: true

matrix_email2matrix_matrix_mappings:
  - MailboxName: "mailbox1"
    MatrixRoomId: "!qporfwt:{{ matrix_domain }}"
    MatrixHomeserverUrl: "{{ matrix_homeserver_url }}"
    MatrixUserId: "@email2matrix1:{{ matrix_domain }}"
    MatrixAccessToken: "MATRIX_ACCESS_TOKEN_HERE"
    IgnoreSubject: false
    IgnoreBody: false
    SkipMarkdown: false

  - MailboxName: "mailbox2"
    MatrixRoomId: "!aaabaa:{{ matrix_domain }}"
    MatrixHomeserverUrl: "{{ matrix_homeserver_url }}"
    MatrixUserId: "@email2matrix2:{{ matrix_domain }}"
    MatrixAccessToken: "MATRIX_ACCESS_TOKEN_HERE"
    IgnoreSubject: true
    IgnoreBody: false
    SkipMarkdown: true
```

where:

* MailboxName - local-part of the email address, through which emails are bridged to the room whose ID is defined with MatrixRoomId
* MatrixRoomId - internal ID of the room, to which received emails are sent as Matrix message
* MatrixHomeserverUrl - URL of your Matrix homeserver, through which to send Matrix messages. You can also set `MatrixHomeserverUrl` to the container URL where your homeserver's Client-Server API lives by using the `{{ matrix_addons_homeserver_client_api_url }}` variable
* MatrixUserId - the full ID of the sender user which sends bridged messages to the room. On this configuration it is `@email2matrix1:example.com` and `@email2matrix2:example.com` (where `example.com` is your base domain, not the `matrix.` domain)
* MatrixAccessToken - sender user's access token
* IgnoreSubject - if set to "true", the subject is not bridged to Matrix
* IgnoreBody - if set to "true", the message body is not bridged to Matrix
* SkipMarkdown - if set to "true", emails are bridged as plain text Matrix message instead of Markdown (actually HTML)

Refer to the official documentation [here](https://github.com/devture/email2matrix/blob/master/docs/configuration.md).

## Installing

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

**Notes**:

- The shortcut commands with the [`just` program](just.md) are also available: `just install-service email2matrix` or `just setup-all`

  `just install-service email2matrix` is useful for maintaining your setup quickly when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note `just setup-all` runs the `ensure-matrix-users-created` tag too.

- After installation, you may wish to send a test email to the email address assigned to `mailbox1` (default: `mailbox1@matrix.example.com`) to make sure that Email2Matrix works as expected.
