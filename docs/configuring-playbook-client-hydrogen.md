# Configuring Hydrogen (optional)

This playbook can install the [Hydrogen](https://github.com/element-hq/hydrogen-web) Matrix web client for you.
Hydrogen is a lightweight web client that supports mobile and legacy web browsers.
Hydrogen can be installed alongside or instead of Element.

## DNS

You need to add a `hydrogen.DOMAIN` DNS record so that Hydrogen can be accessed.
By default Hydrogen will use https://hydrogen.DOMAIN so you will need to create an CNAME record
for `hydrogen`. See [Configuring DNS](configuring-dns.md).

If you would like to use a different domain, add the following configuration to your `inventory/host_vars/matrix.DOMAIN/vars.yml` file (changing it to use your preferred domain):

```yaml
matrix_server_fqn_hydrogen: "helium.{{ matrix_domain }}"
```

## Adjusting the playbook configuration

To enable Hydrogen, add the following configuration to your `inventory/host_vars/matrix.DOMAIN/vars.yml` file:

```yaml
matrix_client_hydrogen_enabled: true
```

## Installing

After configuring the playbook, run the [installation](installing.md) command: `just install-all` or `just setup-all`
