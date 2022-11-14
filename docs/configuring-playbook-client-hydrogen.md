# Configuring Hydrogen (optional)

This playbook can install the [Hydrogen](https://github.com/vector-im/hydrogen-web) Matrix web client for you.
Hydrogen is a lightweight web client that supports mobile and legacy web browsers.
Hydrogen can be installed alongside or instead of Element.

If you'd like Hydrogen to be installed, add the following to your configuration file (`inventory/host_vars/matrix.<your-domain>/vars.yml`):

```yaml
matrix_client_hydrogen_enabled: true
```

You will also need to add a DNS record so that Hydrogen can be accessed. 
By default Hydrogen will use https://hydrogen.DOMAIN so you will need to create an CNAME record
for `hydrogen`. See [Configuring DNS](configuring-dns.md).

If you would like to use a different domain, add the following to your configuration file (changing it to use your preferred domain):

```yaml
 matrix_server_fqn_hydrogen: "helium.{{ matrix_domain }}"
```
