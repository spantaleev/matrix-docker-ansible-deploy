# Setting up Sygnal (optional)

The playbook can install and configure the [Sygnal](https://github.com/matrix-org/sygnal) push gateway for you.

See the project's [documentation](https://github.com/matrix-org/sygnal) to learn what it does and why it might be useful to you.

**Note**: most people don't need to install their own gateway. As Sygnal's [Notes for application developers](https://github.com/matrix-org/sygnal/blob/master/docs/applications.md) documentation says:

> It is not feasible to allow end-users to configure their own Sygnal instance, because the Sygnal instance needs the appropriate FCM or APNs secrets that belong to the application.

This optional playbook component is only useful to people who develop/build their own Matrix client applications themselves.


## Adjusting the playbook configuration

Add the following configuration to your `inventory/host_vars/matrix.DOMAIN/vars.yml` file (adapt to your needs):

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

matrix_aux_file_definitions:
  - dest: "{{ matrix_sygnal_data_path }}/my_key.p8"
    content: |
      some
      content
      here
    mode: '0600'
    owner: "{{ matrix_user_username }}"
    group: "{{ matrix_user_groupname }}"
```

For a more complete example of available fields and values they can take, see `roles/matrix-sygnal/templates/sygnal.yaml.j2` (or the [upstream `sygnal.yaml.sample` configuration file](https://github.com/matrix-org/sygnal/blob/master/sygnal.yaml.sample)).

Configuring [GCM/FCM](https://firebase.google.com/docs/cloud-messaging/) is easier, as it only requires that you provide some config values.

To configure [APNS](https://developer.apple.com/notifications/) (Apple Push Notification Service), you'd need to provide one or more certificate files.
To do that, the above example configuration:

- makes use of the `matrix-aux` role (and its `matrix_aux_file_definitions` variable) to make the playbook install files into `/matrix/sygnal/data` (the `matrix_sygnal_data_path` variable). See `roles/matrix-aux/defaults/main.yml` for usage examples. It also makes sure the files are owned by `matrix:matrix`, so that Sygnal can read them. Of course, you can also install these files manually yourself, if you'd rather not use `matrix-aux`.

- references these files in the Sygnal configuration (`matrix_sygnal_apps`) using a path like `/data/..` (the `/matrix/sygnal/data` directory on the host system is mounted into the `/data` directory inside the container)


## Installing

Don't forget to add `sygnal.<your-domain>` to DNS as described in [Configuring DNS](configuring-dns.md) before running the playbook.

After configuring the playbook, run the [installation](installing.md) command again:

```
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```


## Usage

To make use of your Sygnal installation, you'd need to build your own Matrix client application, which uses the same API keys (for [GCM/FCM](https://firebase.google.com/docs/cloud-messaging/)) and certificates (for [APNS](https://developer.apple.com/notifications/)) and is also pointed to `https://sygnal.DOMAIN` as the configured push server.

Refer to Sygnal's [Notes for application developers](https://github.com/matrix-org/sygnal/blob/master/docs/applications.md) document.
