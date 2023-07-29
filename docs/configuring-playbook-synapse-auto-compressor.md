# Setting up synapse_auto_compressor

The playbook can install and configure [synapse_auto_compressor](https://github.com/matrix-org/rust-synapse-compress-state/#automated-tool-synapse_auto_compressor) for you.

It's a CLI tool that automatically compresses Synapse's `state_groups` database table in the background.

See the project's [documentation](https://github.com/matrix-org/rust-synapse-compress-state/#automated-tool-synapse_auto_compressor) to learn what it does and why it might be useful to you.


## Adjusting the playbook configuration

Add the following configuration to your `inventory/host_vars/matrix.DOMAIN/vars.yml` file:

```yaml
matrix_synapse_auto_compressor_enabled: true
```


## Installing

After configuring the playbook, run the [installation](installing.md) command again:

```
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```


## Usage

After installation, `synapse_auto_compressor` will run automatically every day at `00:00:00` (as defined in `matrix_synapse_auto_compressor_calendar` by default).

## Manually start the tool

For testing your setup it can be helpful to not wait until 00:00. If you want to run the tool immediately, log onto the server
and run `systemctl start matrix-synapse-auto-compressor`. Running this command will not return control to your terminal until the compression run is done, which may take a long time.
Consider using [tmux](https://en.wikipedia.org/wiki/Tmux) if your SSH connection is unstable.
