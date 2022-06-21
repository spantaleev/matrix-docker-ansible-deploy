# A role to install the [ntfy](https://ntfy.sh) push-notification server.

The ntfy server and clients implement self-hosted support push notifications
from Matrix (and other) servers to Android (and other) clients, using the
[UnifiedPush](https://unifiedpush.org) standard.

This role installs ntfy server in Docker.  It is intended to support push
notifications, via UnifiedPush, from the Matrix and Matrix-related services
that are installed alongside it to any clients that support UnifiedPush.

This role is not intended to support other features of the ntfy server and
clients.


# Using the ntfy role

Configure the role by adding settings in your Ansible inventory.

The only required setting is to enable ntfy:

    matrix_ntfy_enabled: true

The default domain for ntfy is `ntfy.<matrix_domain>`.  This can be changed
with the `matrix_server_fqn_ntfy` variable:

    matrix_server_fqn_ntfy: "my-ntfy.{{ matrix_domain }}"

Other ntfy settings can be configured by adding extra arguments to the
docker run command, e.g.:

    matrix_ntfy_container_extra_arguments:
      - '--env=NTFY_LOG_LEVEL=DEBUG'


# TODO

- Documentation.
- Self-check.
- Mount the ntfy database to disk so subscriptions persist across restarts.
- Authentication?
