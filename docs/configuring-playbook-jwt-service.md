# Setting up JWT Service (optional)

The playbook can install and configure [JWT Service](https://github.com/element-hq/lk-jwt-service) for you.

LK-JWT-Service is currently used for a single reason: generate JWT tokens with a given identity for a given room, so that users can use them to authenticate against LiveKit SFU.

See the project's [documentation](https://github.com/element-hq/lk-jwt-service/) to learn more.

## Decide on a domain and path

By default, JWT Service is configured to be served on the Matrix domain (`sfu-jwt.DOMAIN`, controlled by the `matrix_jwt-service_hostname` variable).

This makes it easy to set it up, **without** having to adjust your DNS records manually.

If you'd like to run JWT Service on another hostname or path, use the `matrix_jwt-service_hostname` variable.

## Adjusting DNS records

If you've changed the default hostname, **you may need to adjust your DNS** records accordingly to point to the correct server.

Ensure that the following DNS names have a public IP/FQDN:
- `sfu-jwt.DOMAIN`

## Adjusting the playbook configuration

Add the following configuration to your `inventory/host_vars/matrix.DOMAIN/vars.yml` file:

```yaml
matrix_jwt_service_enabled: true

# Set a secure key for LiveKit authentication
matrix_element_call_livekit_dev_key: 'your-secure-livekit-key'
```

## Installing
After potentially adjusting DNS records and configuring the playbook, run the installation command again:
```yaml
ansible-playbook -i inventory setup.yml
```

## Usage
Once installed, a new `org.matrix.msc4143.rtc_foci` section is added to the element web client to point to your JWT service URL (e.g., `https://sfu-jwt.DOMAIN`).

## Additional Information

Refer to the JWT-Service documentation for more details on configuring and using JWT Service.