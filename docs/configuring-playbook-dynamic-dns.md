# Setting up Dynamic DNS (optional)

The playbook can configure Dynamic DNS with [ddclient⁠](https://github.com/ddclient/ddclient) for you. It is a Perl client used to update dynamic DNS entries for accounts on Dynamic DNS Network Service Provider.

Most cloud providers / ISPs will charge you extra for a static IP address. If you're not hosting a highly reliable homeserver you can workaround this via dynamic DNS.

## Prerequisite

You'll need to get a username and password from your DNS provider. Please consult with the provider about how to retrieve them.

## Adjusting the playbook configuration

To enable dynamic DNS, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_dynamic_dns_enabled: true

matrix_dynamic_dns_domain_configurations:
  - provider: example.net
    protocol: dyndn2
    username: YOUR_USERNAME_HERE
    password: YOUR_PASSWORD_HERE
    domain: "{{ matrix_domain }}"
```

## Installing

After configuring the playbook, run the [installation](installing.md) command: `just install-all` or `just setup-all`

## Additional Reading

Additional resources:

- https://matrix.org/docs/guides/free-small-matrix-server
