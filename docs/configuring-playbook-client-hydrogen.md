# Setting up Hydrogen (optional)

The playbook can install and configure the [Hydrogen](https://github.com/element-hq/hydrogen-web) Matrix web client for you.

Hydrogen is a lightweight web client that supports mobile and legacy web browsers. It can be installed alongside or instead of Element Web.

## Adjusting DNS records

By default, this playbook installs Hydrogen on the `hydrogen.` subdomain (`hydrogen.example.com`) and requires you to create a CNAME record for `hydrogen`, which targets `matrix.example.com`.

When setting, replace `example.com` with your own.

## Adjusting the playbook configuration

To enable Hydrogen, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_client_hydrogen_enabled: true
```

### Adjusting the Hydrogen URL (optional)

By tweaking the `matrix_client_hydrogen_hostname` and `matrix_client_hydrogen_path_prefix` variables, you can easily make the service available at a **different hostname and/or path** than the default one.

Example additional configuration for your `vars.yml` file:

```yaml
# Switch to the domain used for Matrix services (`matrix.example.com`),
# so we won't need to add additional DNS records for Hydrogen.
matrix_client_hydrogen_hostname: "{{ matrix_server_fqn_matrix }}"

# Expose under the /hydrogen subpath
matrix_client_hydrogen_path_prefix: /hydrogen
```

After changing the domain, **you may need to adjust your DNS** records to point the Hydrogen domain to the Matrix server.

If you've decided to reuse the `matrix.` domain, you won't need to do any extra DNS configuration.

## Installing

After configuring the playbook and potentially [adjusting your DNS records](#adjusting-dns-records), run the playbook with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.
