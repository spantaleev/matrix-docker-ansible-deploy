<!--
SPDX-FileCopyrightText: 2023 Nikita Chernyi
SPDX-FileCopyrightText: 2023 Slavi Pantaleev
SPDX-FileCopyrightText: 2024 - 2025 Suguru Hirahara

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Setting up synapse-auto-compressor (optional)

The playbook can install and configure [synapse_auto_compressor](https://github.com/matrix-org/rust-synapse-compress-state/#automated-tool-synapse_auto_compressor) for you.

It's a CLI tool that automatically compresses Synapse's `state_groups` database table in the background.

See the project's [documentation](https://github.com/matrix-org/rust-synapse-compress-state/blob/master/README.md#automated-tool-synapse_auto_compressor) to learn what it does and why it might be useful to you.

## Adjusting the playbook configuration

Add the following configuration to your `inventory/host_vars/matrix.example.com/vars.yml` file:

```yaml
matrix_synapse_auto_compressor_enabled: true
```

### Edit the schedule (optional)

By default the task will around 0 a.m. every day based on the `matrix_synapse_auto_compressor_schedule` variable with a randomized delay of 6 hours (controlled by the `matrix_synapse_auto_compressor_schedule_randomized_delay_sec` variable). It is defined in the format of systemd timer calendar.

To edit the schedule, add the following configuration to your `vars.yml` file (adapt to your needs):

```yaml
matrix_synapse_auto_compressor_schedule: "*-*-* 00:00:00"

# Consider adjusting the randomized delay or setting it to 0 to disable randomized delays.
# matrix_synapse_auto_compressor_schedule_randomized_delay_sec: 6h
```

### Extending the configuration

There are some additional things you may wish to configure about the component.

Take a look at:

- `roles/custom/matrix-synapse-auto-compressor/defaults/main.yml` for some variables that you can customize via your `vars.yml` file

## Installing

After configuring the playbook, run it with [playbook tags](playbook-tags.md) as below:

<!-- NOTE: let this conservative command run (instead of install-all) to make it clear that failure of the command means something is clearly broken. -->
```sh
ansible-playbook -i inventory/hosts setup.yml --tags=setup-all,start
```

The shortcut commands with the [`just` program](just.md) are also available: `just install-all` or `just setup-all`

`just install-all` is useful for maintaining your setup quickly ([2x-5x faster](../CHANGELOG.md#2x-5x-performance-improvements-in-playbook-runtime) than `just setup-all`) when its components remain unchanged. If you adjust your `vars.yml` to remove other components, you'd need to run `just setup-all`, or these components will still remain installed. Note these shortcuts run the `ensure-matrix-users-created` tag too.

## Usage

After installation, `synapse_auto_compressor` will run automatically every day at `00:00:00` (as defined in `matrix_synapse_auto_compressor_schedule` by default).

### Manually start the task

Sometimes it can be helpful to execute compression as you'd like, avoiding to wait until 00:00, like when you test your configuration.

If you want to execute it immediately, log in to the server with SSH and run `systemctl start matrix-synapse-auto-compressor`.

This will not return until the compression is done, so it can possibly take a long time. Consider using [tmux](https://en.wikipedia.org/wiki/Tmux) if your SSH connection is unstable.

## Troubleshooting

As with all other services, you can find the logs in [systemd-journald](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html) by logging in to the server with SSH and running `journalctl -fu matrix-synapse-auto-compressor`.
