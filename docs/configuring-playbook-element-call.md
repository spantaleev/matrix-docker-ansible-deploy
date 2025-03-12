# Setting up Element Call (optional)

The playbook can install and configure [Element Call](https://github.com/vector-im/element-call) for you.

Element Call is a WebRTC-based video and voice calling platform that integrates with Matrix clients such as Element Web. It provides secure, decentralized communication with support for video calls, audio calls, and screen sharing.

See the project's [documentation](https://github.com/vector-im/element-call) to learn more.

## Decide on a domain and path

By default, Element Call is configured to be served on the Matrix domain (`call.DOMAIN`, controlled by the `matrix_element_call_hostname` variable).

This makes it easy to set it up, **without** having to adjust your DNS records manually.

If you'd like to run Element Call on another hostname or path, use the `matrix_element_call_hostname` and `matrix_element_call_path_prefix` variables.

## Adjusting DNS records

If you've changed the default hostname, **you may need to adjust your DNS** records accordingly to point to the correct server.

Ensure that the following DNS names have a public IP/FQDN:
- `call.example.com`
- `sfu.example.com`
- `sfu-jwt.example.com`

## Adjusting the playbook configuration

NOTE: Enabling Element Call will automatically enable the [LiveKit JWT Service](configuring-playbook-livekit-jwt-service.md) and Livekit Server services.


Add the following configuration to your `inventory/host_vars/matrix.DOMAIN/vars.yml` file:

```yaml
matrix_element_call_enabled: true
```

## Installing

After configuring the playbook and potentially [adjusting your DNS records](#adjusting-dns-records), run the [installation](installing.md) command: `just install-all` or `just setup-all`

## Usage

Once installed, Element Call integrates seamlessly with Matrix clients like [Element Web](configuring-playbook-client-element-web.md). When the Element Call service is installed, the `/.well-known/matrix/client` file is also updated. A new `org.matrix.msc4143.rtc_foci` section is added to point to your LiveKit JWT service URL (e.g., `https://matrix.example.com/lk-jwt-service`).

Additionally, the `/.well-known/element/element.json` file is created to help Element clients discover the Element Call URL (e.g., `https://call.example.com`).

## Required Firewall and Port Forwarding Rules

To ensure the services function correctly, the following firewall rules and port forwarding settings are required:

LiveKit:

- Forward UDP ports 50100:50120 to the Docker instance running LiveKit.
- Forward TCP port 7881 to the Docker instance running LiveKit.

Element Call:

- Forward TCP port 443 to the server running Traefik (for Element Call).

Ensure these ports are open and forwarded appropriately to allow traffic to flow correctly between the services.

## Additional Information

Refer to the Element Call documentation for more details on configuring and using Element Call.
