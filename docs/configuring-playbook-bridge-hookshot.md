# Setting up Hookshot (optional)

The playbook can install and configure [matrix-hookshot](https://github.com/Half-Shot/matrix-hookshot) for you.

See the project's [documentation](https://half-shot.github.io/matrix-hookshot/hookshot.html) to learn what it does and why it might be useful to you.


## Setup Instructions

Refer to the [official instructions](https://half-shot.github.io/matrix-hookshot/setup.html) to learn what the individual options do.

1. For each of the services (GitHub, GitLab, JIRA, generic webhooks) fill in the respected variables `matrix_hookshot_service_*` listed in [main.yml](roles/matrix-bridge-hookshot/defaults/main.yml) as required.
2. If you've already installed Matrix services using the playbook before, you'll need to re-run it (`--tags=setup-all,start`). If not, proceed with [configuring other playbook services](configuring-playbook.md) and then with [Installing](installing.md). Get back to this guide once ready.
3. Refer to the [official instructions](https://half-shot.github.io/matrix-hookshot/usage.html) to start bridging things.

Other configuration options are available via the `matrix_hookshot_configuration_extension_yaml` variable.
