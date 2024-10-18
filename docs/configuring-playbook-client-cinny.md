# Configuring Cinny (optional)

This playbook can install the [cinny](https://github.com/ajbura/cinny) Matrix web client for you.
Cinny is a web client focusing primarily on simple, elegant and secure interface.
Cinny can be installed alongside or instead of Element.

## DNS

You need to add a `cinny.example.com` DNS record so that Cinny can be accessed.
By default Cinny will use https://cinny.example.com so you will need to create an CNAME record
for `cinny`. See [Configuring DNS](configuring-dns.md).

If you would like to use a different domain, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file (changing it to use your preferred domain):

```yaml
matrix_server_fqn_cinny: "app.{{ matrix_domain }}"
```

## Adjusting the playbook configuration

To enable Cinny, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_client_cinny_enabled: true
```

## Installing

After configuring the playbook, run the [installation](installing.md) command: `just install-all` or `just setup-all`
