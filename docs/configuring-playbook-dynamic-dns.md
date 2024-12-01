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

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with `just` program are also available: `just run-tags install-all,start` or `just run-tags setup-all,start`

`just run-tags install-all,start` is useful for maintaining your setup quickly when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just run-tags setup-all,start`, or these components will still remain installed. For more information about `just` shortcuts, take a look at this page: [Running `just` commands](just.md)

## Additional Reading

Additional resources:

- https://matrix.org/docs/guides/free-small-matrix-server
