# Setting up synapse-auto-compressor (optional)

The playbook can install and configure [synapse_auto_compressor](https://github.com/matrix-org/rust-synapse-compress-state/#automated-tool-synapse_auto_compressor) for you.

It's a CLI tool that automatically compresses Synapse's `state_groups` database table in the background.

See the project's [documentation](https://github.com/matrix-org/rust-synapse-compress-state/#automated-tool-synapse_auto_compressor) to learn what it does and why it might be useful to you.


## Adjusting the playbook configuration

Add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_synapse_auto_compressor_enabled: true
```


## Installing

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with `just` program are also available: `just run-tags install-all,start` or `just run-tags setup-all,start`

`just run-tags install-all,start` is useful for maintaining your setup quickly when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just run-tags setup-all,start`, or these components will still remain installed. For more information about `just` shortcuts, take a look at this page: [Running `just` commands](just.md)

## Usage

After installation, `synapse_auto_compressor` will run automatically every day at `00:00:00` (as defined in `matrix_synapse_auto_compressor_calendar` by default).

## Manually start the tool

For testing your setup it can be helpful to not wait until 00:00. If you want to run the tool immediately, log onto the server and run `systemctl start matrix-synapse-auto-compressor`. Running this command will not return control to your terminal until the compression run is done, which may take a long time. Consider using [tmux](https://en.wikipedia.org/wiki/Tmux) if your SSH connection is unstable.
