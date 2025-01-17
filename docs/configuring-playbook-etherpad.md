# Setting up Etherpad (optional)

The playbook can install and configure [Etherpad](https://etherpad.org) for you.

Etherpad is an open source collaborative text editor. It can not only be integrated with Element clients ([Element Web](configuring-playbook-client-element-web.md)/Desktop, Android and iOS) as a widget, but also be used as standalone web app.

When enabled together with the Jitsi audio/video conferencing system (see [our docs on Jitsi](configuring-playbook-jitsi.md)), it will be made available as an option during the conferences.

## Adjusting DNS records

By default, this playbook installs Etherpad on the `etherpad.` subdomain (`etherpad.example.com`) and requires you to create a CNAME record for `etherpad`, which targets `matrix.example.com`.

When setting, replace `example.com` with your own.

## Adjusting the playbook configuration

To enable Etherpad, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
etherpad_enabled: true

# Uncomment and adjust this part if you'd like to enable the admin web UI
# etherpad_admin_username: YOUR_USERNAME_HERE
# etherpad_admin_password: YOUR_PASSWORD_HERE
```

### Adjusting the Etherpad URL (optional)

By tweaking the `etherpad_hostname` and `etherpad_path_prefix` variables, you can easily make the service available at a **different hostname and/or path** than the default one.

Example additional configuration for your `vars.yml` file:

```yaml
# Switch to the domain used for Matrix services (`matrix.example.com`),
# so we won't need to add additional DNS records for Etherpad.
etherpad_hostname: "{{ matrix_server_fqn_matrix }}"

# Expose under the /etherpad subpath
etherpad_path_prefix: /etherpad
```

After changing the domain, **you may need to adjust your DNS** records to point the Etherpad domain to the Matrix server.

If you've decided to reuse the `matrix.` domain, you won't need to do any extra DNS configuration.

### Configure the default text (optional)

You can also edit the default text on a new pad with the variable `etherpad_default_pad_text`.

To do so, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
# Note: the whole text (all of its belonging lines) under the variable needs to be indented with 2 spaces.
etherpad_default_pad_text: |
  Welcome to Etherpad!

  This pad text is synchronized as you type, so that everyone viewing this page sees the same text. This allows you to collaborate seamlessly on documents!

  Get involved with Etherpad at https://etherpad.org
```

### Extending the configuration

There are some additional things you may wish to configure about the component.

Take a look at:

- [etherpad role](https://github.com/mother-of-all-self-hosting/ansible-role-etherpad)'s [`defaults/main.yml`](https://github.com/mother-of-all-self-hosting/ansible-role-etherpad/blob/main/defaults/main.yml) for some variables that you can customize via your `vars.yml` file. You can override settings (even those that don't have dedicated playbook variables) using the `etherpad_configuration_extension_json` variable

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

If you've [decided on another hostname or path-prefix](#adjusting-the-etherpad-url-optional) (e.g. `https://matrix.example.com/etherpad`), adjust these URLs accordingly before using it.

### Managing / Deleting old pads

If you want to manage and remove old unused pads from Etherpad, you will first need to create the Etherpad admin user as described above.

After logging in to the admin web UI, go to the plugin manager page, and install the `adminpads2` plugin.

Once the plugin is installed, you should have a "Manage pads" section in the UI.

### Integrating a Etherpad widget in a room

**Note**: this is how it works in Element Web. It might work quite similar with other clients:

To integrate a standalone Etherpad in a room, create your pad by visiting `https://etherpad.example.com`. When the pad opens, copy the URL and send a command like this to the room: `/addwidget URL`. You will then find your integrated Etherpad within the right sidebar in the `Widgets` section.
