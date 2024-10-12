# Configuring Cinny (optional)

This playbook can install the [cinny](https://github.com/ajbura/cinny) Matrix web client for you.
Cinny is a web client focusing primarily on simple, elegant and secure interface.
Cinny can be installed alongside or instead of Element.

If you'd like Cinny to be installed, add the following to your configuration file (`inventory/host_vars/matrix.<your-domain>/vars.yml`):

```yaml
matrix_client_cinny_enabled: true
```

You will also need to add a DNS record so that Cinny can be accessed.
By default Cinny will use https://cinny.DOMAIN so you will need to create an CNAME record
for `cinny`. See [Configuring DNS](configuring-dns.md).

If you would like to use a different domain, add the following to your configuration file (changing it to use your preferred domain):

```yaml
 matrix_server_fqn_cinny: "app.{{ matrix_domain }}"
```
