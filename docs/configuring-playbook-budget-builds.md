# Tips for deploying Matrix on a Budget

## Dynamic DNS

Most cloud providers / ISPs will charge you extra for a static IP address. If you're
not hosting a highly reliable homeserver you can workaround this via dynamic DNS. To
set this up, you'll need to get the username/password from your DNS provider. For
google domains, this process is described [here](https://support.google.com/domains/answer/6147083).
After you've gotten the proper credentials you can add the following config to your inventory/host_vars/matrix.DOMAIN/vars.yml:

```
matrix_dynamic_dns_username: XXXXXXXXXXXXXXXX
matrix_dynamic_dns_password: XXXXXXXXXXXXXXXX
matrix_dynamic_dns_provider: 'domains.google.com'
```

## Additional Reading

Additional resources:

- https://matrix.org/docs/guides/free-small-matrix-server