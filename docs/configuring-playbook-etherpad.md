# Setting up Etherpad (optional)

[Etherpad](https://etherpad.org) is an open source collaborative text editor that can be embedded in a Matrix chat room using the [Dimension integration manager](https://dimension.t2bot.io) or used as standalone web app.

When enabled together with the Jitsi audio/video conferencing system (see [our docs on Jitsi](configuring-playbook-jitsi.md)), it will be made available as an option during the conferences.

## Adjusting the playbook configuration

To enable Etherpad, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
etherpad_enabled: true

# Uncomment and adjust this part if you'd like to enable the admin web UI
# etherpad_admin_username: YOUR_USERNAME_HERE
# etherpad_admin_password: YOUR_PASSWORD_HERE
```

### Adjusting the Etherpad URL

By default, this playbook installs Etherpad on the `etherpad.` subdomain (`etherpad.example.com`) and requires you to [adjust your DNS records](#adjusting-dns-records).

By tweaking the `etherpad_hostname` and `etherpad_path_prefix` variables, you can easily make the service available at a **different hostname and/or path** than the default one.

Example additional configuration for your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
# Switch to the domain used for Matrix services (`matrix.example.com`),
# so we won't need to add additional DNS records for Etherpad.
etherpad_hostname: "{{ matrix_server_fqn_matrix }}"

# Expose under the /etherpad subpath
etherpad_path_prefix: /etherpad
```

## Adjusting DNS records

Once you've decided on the domain and path, **you may need to adjust your DNS** records to point the Etherpad domain to the Matrix server.

By default, you will need to create a CNAME record for `etherpad`. See [Configuring DNS](configuring-dns.md) for details about DNS changes.

If you've decided to reuse the `matrix.` domain, you won't need to do any extra DNS configuration.

## Installing

After configuring the playbook and potentially [adjusting your DNS records](#adjusting-dns-records), run the playbook with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,ensure-matrix-users-created,start
```

**Notes**:

- The `ensure-matrix-users-created` playbook tag makes the playbook automatically create the Etherpad admin user (`etherpad_admin_username`).

- The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

  `just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed.

- If you change the Etherpad admin user's password (`etherpad_admin_password` in your `vars.yml` file) subsequently, the admin user's credentials on the homeserver won't be updated automatically. If you'd like to change the admin user's password, use a tool like [synapse-admin](configuring-playbook-synapse-admin.md) to change it, and then update `etherpad_admin_password` to let the admin user know its new password.

## Usage

The Etherpad UI should be available at `https://etherpad.example.com`, while the admin UI (if enabled) should then be available at `https://etherpad.example.com/admin`.

If you've [decided on another hostname or path-prefix](#adjusting-the-etherpad-url) (e.g. `https://matrix.example.com/etherpad`), adjust these URLs accordingly before usage.

### Managing / Deleting old pads

If you want to manage and remove old unused pads from Etherpad, you will first need to able Admin access as described above.

Then from the plugin manager page (`https://etherpad.example.com/admin/plugins`, install the `adminpads2` plugin. Once installed, you should have a "Manage pads" section in the Admin web-UI.

### How to use Etherpad widgets without an integration manager (like Dimension)

This is how it works in Element Web, it might work quite similar with other clients:

To integrate a standalone Etherpad in a room, create your pad by visiting `https://etherpad.example.com`. When the pad opens, copy the URL and send a command like this to the room: `/addwidget URL`. You will then find your integrated Etherpad within the right sidebar in the `Widgets` section.

### Set Dimension default to the self-hosted Etherpad (optional)

If you decided to install [Dimension integration manager](configuring-playbook-dimension.md) alongside Etherpad, the Dimension administrator users can configure the default URL template.

The Dimension configuration menu can be accessed with the sprocket icon as you begin to add a widget to a room in Element Web. There you will find the Etherpad Widget Configuration action beneath the _Widgets_ tab.

#### Removing the integrated Etherpad chat

If you wish to disable the Etherpad chat button, you can do it by appending `?showChat=false` to the end of the pad URL, or the template.

Example: `https://etherpad.example.com/p/$roomId_$padName?showChat=false`

## Known issues

If your Etherpad widget fails to load, this might be due to Dimension generating a Pad name so long, the Etherpad app rejects it.

`$roomId_$padName` can end up being longer than 50 characters. You can avoid having this problem by altering the template so it only contains the three word random identifier `$padName`.
