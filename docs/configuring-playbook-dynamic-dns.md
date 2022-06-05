# Dynamic DNS

## Setup

Most cloud providers / ISPs will charge you extra for a static IP address. If you're
not hosting a highly reliable homeserver you can workaround this via dynamic DNS. To
set this up, you'll need to get the username/password from your DNS provider. For
google domains, this process is described [here](https://support.google.com/domains/answer/6147083).
After you've gotten the proper credentials you can add the following config to your `inventory/host_vars/matrix.DOMAIN/vars.yml`:

```yaml
matrix_dynamic_dns_enabled: true

matrix_dynamic_dns_domain_configurations:
  - provider: domains.google.com
    protocol: dyndn2
    username: XXXXXXXXXXXXXXXX
    password: XXXXXXXXXXXXXXXX
    domain: "{{ matrix_domain }}"
```


## Additional Reading

Additional resources:

- https://matrix.org/docs/guides/free-small-matrix-server


## Jitsi behind a NAT

Keep in mind when using dynamic DNS you might run into the problem of having [no video or audio with more than 2 users](https://github.com/EtienneHenger/matrix-docker-ansible-deploy/blob/f2293f61eebe49f47d7bb42363ed4f6b0fa9eb5a/docs/configuring-playbook-jitsi.md#L166).