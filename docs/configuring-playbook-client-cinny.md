# Setting up Cinny (optional)

The playbook can install and configure the [Cinny](https://github.com/ajbura/cinny) Matrix web client for you.

Cinny is a web client focusing primarily on simple, elegant and secure interface. It can be installed alongside or instead of [Element Web](./configuring-playbook-client-element-web.md).

💡 **Note**: the latest version of Cinny is also available on the web, hosted by 3rd parties. If you trust giving your credentials to the following 3rd party Single Page Applications, you can consider using it from there and avoiding the (small) overhead of self-hosting:

- [app.cinny.in](https://app.cinny.in), hosted by the [Cinny](https://cinny.in/) developers

## Adjusting DNS records

By default, this playbook installs Cinny on the `cinny.` subdomain (`cinny.example.com`) and requires you to create a CNAME record for `cinny`, which targets `matrix.example.com`.

When setting, replace `example.com` with your own.

## Adjusting the playbook configuration

To enable Cinny, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_client_cinny_enabled: true
```

### Adjusting the Cinny URL (optional)

By tweaking the `matrix_client_cinny_hostname` variable, you can easily make the service available at a **different hostname** than the default one.

Example additional configuration for your `vars.yml` file:

```yaml
# Switch to a different domain (`app.example.com`) than the default one (`cinny.example.com`)
matrix_client_cinny_hostname: "app.{{ matrix_domain }}"

# Expose under the /cinny subpath
# matrix_client_cinny_path_prefix: /cinny
```

After changing the domain, **you may need to adjust your DNS** records to point the Cinny domain to the Matrix server.

**Note**: while there is a `matrix_client_cinny_path_prefix` variable for changing the path where Cinny is served, overriding it is [not possible](https://github.com/spantaleev/matrix-docker-ansible-deploy/issues/3701), because Cinny requires an application rebuild (with a tweaked build config) to be functional under a custom path. You'd need to serve Cinny at a dedicated subdomain.

## Installing

After configuring the playbook and [adjusting your DNS records](#adjusting-dns-records), run the playbook with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.
