<!--
SPDX-FileCopyrightText: 2026 Slavi Pantaleev

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Reviewing role dependency updates

Renovate opens pull requests for Ansible role version updates instead of merging their branches
directly. Review the released role changes and the playbook wiring before merging; a role update may
need a playbook adaptation even when its role tests pass. Other dependency classes retain their
separate Renovate policies.

# Maintaining the Renovate runner

The self-hosted runner version is pinned in [`.github/workflows/renovate.yml`](../.github/workflows/renovate.yml). Renovate updates this pin and automerges passing updates according to [`.github/renovate.json`](../.github/renovate.json).

The `Renovate smoke test` workflow tests the candidate image on branch pushes and fork pull requests. It validates configuration and starts the real Renovate runtime to extract dependencies from the checked-out repository. It requires results from all eight managers currently used here, including the custom managers that update role versions, Molecule helper images, and Renovate itself, and rejects errors or missing completion logs. The containers have no network access, receive no credentials, and mount the checkout read-only.

Run the same check locally with Docker, Bash, and jq installed:

```sh
bin/renovate-smoke-test.sh
# Reproduce the broken image without changing the workflow pin:
bin/renovate-smoke-test.sh 44.64.0
```

Version `44.64.0` is deliberately excluded from runner updates: its APK datasource imports `tar`, which was only declared as a development dependency and is missing from the production image. It passed configuration validation and `--version`, then crashed at startup with exit code 0 ([incident log](https://github.com/spantaleev/matrix-docker-ansible-deploy/actions/runs/35090923781/job/104776805727)). The runner was reverted to `44.61.6`. Both production and the smoke test set `NODE_OPTIONS=--unhandled-rejections=strict` so unhandled startup failures return a failing exit code.

Upstream corrected the packaging in [Renovate PR #45699](https://github.com/renovatebot/renovate/pull/45699). A runner that crashes before processing the repository cannot discover its own replacement, so recovery requires manually changing the pin to a working version.

This smoke test would have blocked that upgrade. It does not exercise registry lookups, GitHub authentication, or branch/PR writes. For live integration checks, manually dispatch the `Renovate` workflow on `master` with `dry_run` enabled and `log_level` set to `debug`. That tests the pin already on `master`; it is not a pre-merge test of a candidate branch. Check the smoke-test result when manually merging runner upgrades too.
