# Setting up Appservice Double Puppet (optional)

Appservice Double Puppet is a homeserver appservice through which bridges (and potentially other services) can impersonate any user on the homeserver.

This is useful for performing [double-puppeting](https://docs.mau.fi/bridges/general/double-puppeting.html) via the [appservice method](https://docs.mau.fi/bridges/general/double-puppeting.html#appservice-method-new). The Appservice Double Puppet service is an implementation of this approach.

Previously, bridges supported performing [double-puppeting](https://docs.mau.fi/bridges/general/double-puppeting.html) with the help of the [Shared Secret Auth password provider module](./configuring-playbook-shared-secret-auth.md), but this old and hacky solution has been superseded by this Appservice Double Puppet method.

## Adjusting the playbook configuration

To enable the Appservice Double Puppet service, add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yml
matrix_appservice_double_puppet_enabled: true
```

## Installing

After configuring the playbook, run the [installation](installing.md) command: `just install-all` or `just setup-all`

## Usage

When enabled, double puppeting will automatically be enabled for all bridges that support double puppeting via the appservice method.
