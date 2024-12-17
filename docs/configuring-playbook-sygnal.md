# Setting up the Sygnal push gateway (optional)

The playbook can install and configure the [Sygnal](https://github.com/matrix-org/sygnal) push gateway for you.

See the project's [documentation](https://github.com/matrix-org/sygnal/blob/master/README.md) to learn what it does and why it might be useful to you.

**Note**: most people don't need to install their own gateway. As Sygnal's [Notes for application developers](https://github.com/matrix-org/sygnal/blob/master/docs/applications.md) documentation says:

> It is not feasible to allow end-users to configure their own Sygnal instance, because the Sygnal instance needs the appropriate FCM or APNs secrets that belong to the application.

This optional playbook component is only useful to people who develop/build their own Matrix client applications themselves.

## Adjusting the playbook configuration

To enable Sygnal, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_sygnal_enabled: true

# You need at least 1 app defined.
# The configuration below is incomplete. Read more below.
matrix_sygnal_apps:
  com.example.myapp.ios:
    type: apns
    keyfile: /data/my_key.p8
    # .. more configuration ..
  com.example.myapp.android:
    type: gcm
    api_key: your_api_key_for_gcm
    # .. more configuration ..

aux_file_definitions:
  - dest: "{{ matrix_sygnal_data_path }}/my_key.p8"
    content: |
      some
      content
      here
    mode: '0600'
    owner: "{{ matrix_user_username }}"
    group: "{{ matrix_user_groupname }}"
```

For a more complete example of available fields and values they can take, see `roles/custom/matrix-sygnal/templates/sygnal.yaml.j2` (or the [upstream `sygnal.yaml.sample` configuration file](https://github.com/matrix-org/sygnal/blob/master/sygnal.yaml.sample)).

Configuring [GCM/FCM](https://firebase.google.com/docs/cloud-messaging/) is easier, as it only requires that you provide some config values.

To configure [APNS](https://developer.apple.com/notifications/) (Apple Push Notification Service), you'd need to provide one or more certificate files. To do that, the above example configuration:

- makes use of the [`aux` role](https://github.com/mother-of-all-self-hosting/ansible-role-aux) (and its `aux_file_definitions` variable) to make the playbook install files into `/matrix/sygnal/data` (the `matrix_sygnal_data_path` variable). See [`defaults/main.yml` file](https://github.com/mother-of-all-self-hosting/ansible-role-aux/blob/main/defaults/main.yml) of the `aux` role for usage examples. It also makes sure the files are owned by `matrix:matrix`, so that Sygnal can read them. Of course, you can also install these files manually yourself, if you'd rather not use `aux`.

- references these files in the Sygnal configuration (`matrix_sygnal_apps`) using a path like `/data/..` (the `/matrix/sygnal/data` directory on the host system is mounted into the `/data` directory inside the container)

### Adjusting the Sygnal URL

By default, this playbook installs Sygnal on the `sygnal.` subdomain (`sygnal.example.com`) and requires you to [adjust your DNS records](#adjusting-dns-records).

By tweaking the `matrix_sygnal_hostname` and `matrix_sygnal_path_prefix` variables, you can easily make the service available at a **different hostname and/or path** than the default one.

Example additional configuration for your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
# Switch to the domain used for Matrix services (`matrix.example.com`),
# so we won't need to add additional DNS records for Sygnal.
matrix_sygnal_hostname: "{{ matrix_server_fqn_matrix }}"

# Expose under the /sygnal subpath
matrix_sygnal_path_prefix: /sygnal
```

## Adjusting DNS records

Once you've decided on the domain and path, **you may need to adjust your DNS** records to point the Sygnal domain to the Matrix server.

By default, you will need to create a CNAME record for `sygnal`. See [Configuring DNS](configuring-dns.md) for details about DNS changes.

If you've decided to reuse the `matrix.` domain, you won't need to do any extra DNS configuration.

## Installing

After configuring the playbook and potentially [adjusting your DNS records](#adjusting-dns-records), run the playbook with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

## Usage

To make use of your Sygnal installation, you'd need to build your own Matrix client application, which uses the same API keys (for [GCM/FCM](https://firebase.google.com/docs/cloud-messaging/)) and certificates (for [APNS](https://developer.apple.com/notifications/)) and is to your Sygnal URL endpoint (e.g. `https://sygnal.example.com`).

Refer to Sygnal's [Notes for application developers](https://github.com/matrix-org/sygnal/blob/master/docs/applications.md) document.
