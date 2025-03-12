# Setting up LiveKit (optional)

The playbook can install and configure [LiveKit](https://github.com/livekit/livekit) for you.

LiveKit is an open source project that provides scalable, multi-user conferencing based on WebRTC. It's designed to provide everything you need to build real-time video audio data capabilities in your applications.

See the project's [documentation](https://github.com/livekit/livekit) to learn more.

## Decide on a domain and path

By default, LiveKit is configured to be served on the Matrix domain (`sfu.example.com`, controlled by the `livekit_server_hostname` variable).

This makes it easy to set it up, **without** having to adjust your DNS records manually.

If you'd like to run Livekit on another hostname or path, use the `livekit_server_hostname` variable.

## Adjusting DNS records

If you've changed the default hostname, **you may need to adjust your DNS** records accordingly to point to the correct server.

Ensure that the following DNS names have a public IP/FQDN:
- `sfu.example.com`

## Adjusting the playbook configuration

Add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
livekit_server_enabled: true

# Set a secure key for LiveKit authentication
livekit_server_dev_key: 'your-secure-livekit-key'
```

## Installing

After configuring the playbook and potentially [adjusting your DNS records](#adjusting-dns-records), run the [installation](installing.md) command: `just install-all` or `just setup-all`

## Usage
Once installed, and in conjunction with Element Call and JWT Service, Livekit will become the WebRTC backend for all Element client calls.

## Required Firewall and Port Forwarding Rules

To ensure the services function correctly, the following firewall rules and port forwarding settings are required:

LiveKit:

- Forward UDP ports 50100:50200 to the Docker instance running LiveKit.
- Forward TCP port 7881 to the Docker instance running LiveKit.

Ensure these ports are open and forwarded appropriately to allow traffic to flow correctly between the services.

## Additional Information

Refer to the Livekit documentation for more details on configuring and using Livekit.
