# Setting up Fluffygate (optional)

The playbook can install and configure [Fluffygate](https://github.com/krille-chan/fluffygate), a simple Push Gateway for Fluffychat.

See the project's documentation to learn what it does and why it might be useful to you.

**Note**: most people don't need to install their own gateway. This optional playbook component is only useful to people who develop/build their own Matrix client applications themselves, as you'll need access to your own Firebase/FCM and APNS credentials.

## Adjusting the playbook configuration

To enable Fluffygate, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_fluffygate_enabled: true

# Basic app information
matrix_fluffygate_app_name: "Your App Name"
matrix_fluffygate_app_website: "https://example.com"

# Firebase/FCM configuration (for Android / IOS)
matrix_fluffygate_firebase_project: "your-firebase-project-id"
matrix_fluffygate_firebase_key: |
  {
    # Your Firebase service account key JSON content
  }

# Notification settings
matrix_fluffygate_notification_title: "{count} new messages"
matrix_fluffygate_notification_body: "{body}"

# Android specific notification options
matrix_fluffygate_android_notification_options:
  priority: high
  notification:
    sound: "default"
    icon: "notifications_icon"
    tag: "default_notification"

# APNS specific notification options (for iOS)
matrix_fluffygate_apns_notification_options:
  headers:
    apns-priority: "10"
  payload:
    aps:
      sound: "default"
      badge: "{count}"
      mutable-content: 1
```

For a complete list of available configuration options, see the `defaults/main.yml` file in the role.

### Required Configuration

The following settings are required and must be defined:
- `matrix_fluffygate_hostname`
- `matrix_fluffygate_path_prefix`
- `matrix_fluffygate_container_network`
- `matrix_fluffygate_app_name`
- `matrix_fluffygate_app_website`

### Adjusting the Fluffygate URL

By default, this playbook installs Fluffygate at the root path (`/`) of the configured hostname. You can customize both the hostname and path prefix using these variables:

```yaml
# Configure the hostname where Fluffygate will be served
matrix_fluffygate_hostname: "push.example.com"

# Configure a custom path prefix (must either be '/' or not end with a slash)
matrix_fluffygate_path_prefix: /push
```

### Traefik Integration

Fluffygate includes built-in support for Traefik as a reverse proxy. The following settings control this integration:

```yaml
# Enable/disable Traefik labels
matrix_fluffygate_container_labels_traefik_enabled: true

# Configure the Traefik network
matrix_fluffygate_container_labels_traefik_docker_network: "{{ matrix_fluffygate_container_network }}"

# Additional Traefik configuration
matrix_fluffygate_container_labels_traefik_rule: "Host(`{{ matrix_fluffygate_container_labels_traefik_hostname }}`)"
matrix_fluffygate_container_labels_traefik_priority: 0
matrix_fluffygate_container_labels_traefik_entrypoints: web-secure
```

## Adjusting DNS records

Once you've decided on the domain and path, **you may need to adjust your DNS** records to point the Fluffygate domain to the Matrix server.

By default, you will need to create a CNAME record for `push`. See [Configuring DNS](configuring-dns.md) for details about DNS changes.

If you've decided to reuse the `matrix.` domain, you won't need to do any extra DNS configuration.

## Installing

After configuring the playbook and adjusting your DNS records, run the installation command:

```bash
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

To install only Fluffygate, you can use:

```bash
ansible-playbook -i inventory/hosts setup.yml --tags=setup-fluffygate,start
```

## Usage

To make use of your Fluffygate installation:

1. Configure your Matrix client application to use your Fluffygate URL as the push gateway
2. Ensure your app uses the same Firebase/FCM credentials for Android notifications
3. Ensure your app uses the same APNS certificates/credentials for iOS notifications
4. Configure the notification templates and options as needed through the playbook variables

### Debugging

If you need to troubleshoot issues:

1. Enable debug logs by setting:
    ```yaml
    matrix_fluffygate_debug_logs: true
    ```

2. Check the container logs:
    ```bash
    docker logs matrix-fluffygate
    ```

## Uninstalling

To remove Fluffygate, first disable it in your `inventory/host_vars/matrix.example.com/vars.yml`:

```yaml
matrix_fluffygate_enabled: false
```

Then run the playbook:

```bash
ansible-playbook -i inventory/hosts setup.yml --tags=setup-fluffygate,start
```

This will stop the service and remove all associated files.
