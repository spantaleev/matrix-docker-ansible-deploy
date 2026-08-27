<!--
SPDX-FileCopyrightText: 2026 Slavi Pantaleev

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Molecule testing for roles

Roles in `roles/custom/` can carry a [Molecule](https://ansible.readthedocs.io/projects/molecule/) scenario, which installs the role into a container and then checks that the component actually came up with the configuration the role rendered.

Not every role has one yet. Roles without a scenario are simply not tested.

## Running a scenario

```sh
just molecule                                    # list roles that have a scenario
just molecule matrix-alertmanager-receiver       # run one
just molecule matrix-alertmanager-receiver converge   # any molecule subcommand
```

The first run creates a virtualenv in `var/molecule-venv/` (gitignored) from `molecule-shared/requirements.txt`. Docker must be working, and a run takes minutes because it pulls container images.

`MOLECULE_DISTRO` selects the base image; it defaults to `ubuntu2604`.

Molecule is deliberately **not** part of the `prek` hooks. A run is far too slow to sit in front of a commit, and it needs Docker. Run it when you have touched a role; CI runs it too, asynchronously.

## What CI runs

`.github/workflows/molecule.yml` does not run every scenario on every push — with one repository holding every role, that would be unaffordable. Its first job works out which roles the push actually touched, keeps the ones that have a scenario, and builds the job matrix from those. A documentation change runs nothing.

When the diff base cannot be determined (a new branch, a force push), it falls back to running every scenario, which errs toward testing too much rather than too little. `workflow_dispatch` accepts an optional role name.

## Writing a scenario

Start from `roles/custom/matrix-alertmanager-receiver/molecule/default/` — it is the reference. Four things differ from a standalone role's scenario, all of them consequences of these roles living inside a playbook:

### The playbook's context has to be supplied

The role reads variables that `matrix-base` and `group_vars/matrix_servers` would normally provide. The set is small — `matrix_base_data_path`, `matrix_domain`, `matrix_user_name`, `matrix_group_name`, `matrix_user_uid`, `matrix_user_gid` — and belongs in the scenario's `group_vars`, rather than including `matrix-base`, which does much more than a role scenario needs.

### The `matrix` user and group must exist first

The roles' file tasks set `owner:` and `group:` by name, and Ansible resolves those through the passwd database, so `prepare.yml` has to create them before the role runs.

### Most components need a homeserver to be present

Many of these components contact the homeserver while starting up, and exit if it is unreachable — `matrix-alertmanager-receiver`, for example, fetches `/_matrix/client/v3/joined_rooms` to resolve its room mapping and exits with a failure if that call fails.

A stub is enough, and is what the reference scenario stands up. The point of these scenarios is to prove that **the component starts and does not choke on the configuration the role rendered** — not to exercise real bridging. A scenario should never need a credential or an account on a third-party network; that is the line where it stops being a test of this repository.

### `verify.yml` is a separate play

Role defaults are out of scope there, so any path it reads has to be pinned in the scenario's `group_vars`. Deliberately do **not** pin the component's version that way: read it from the role's `defaults/main.yml` with `include_vars`, so the assertion compares the running image against what the role ships rather than against the scenario itself.

## Shared files

`molecule-shared/` holds what would otherwise be duplicated into every role:

- `requirements.txt` — the Python packages, for both CI and `just molecule`.
- `requirements.yml` — the external Ansible roles and collections the scenarios need. Each scenario symlinks its own `molecule/default/requirements.yml` at this file: Molecule checks for a requirements file at that default path before it will install anything, so pointing at the shared one through `requirements-file` alone is silently ignored.
- `vars.yml` — helper container images used for probing, pinned once. They carry `# renovate:` annotations and a custom manager in `.github/renovate.json` keeps them current.

A helper image is used to reach a role's container over its own container network. That indirection is deliberate: the roles publish no host port, matching a real deployment, and publishing one for the test would collide between scenarios running in parallel.

## Making a scenario worth having

A suite that only waits for the systemd unit to become `active` proves very little: these units carry `Restart=always`, so a container crash-looping on a bad configuration still reports `active`. Check the restart counter alongside it, and probe something the component can only answer correctly if the role's configuration reached it.

Give the scenario values that differ from both the role's defaults and the component's own defaults. Otherwise a passing assertion cannot distinguish "the role configured this" from "it would have happened anyway".

Then try to break it. If a scenario cannot be made to fail by deliberately breaking the thing it checks, it is not testing that thing.

## Running more than one scenario at once

`bin/molecule.sh` points `ANSIBLE_HOME` at `var/molecule-ansible-home/<role>/`, so each role gets
its own copy of the Galaxy collections and roles.

This is not an optimisation - it is a correctness fix. Scenarios install their dependencies with
`force: true`, so two runs sharing `~/.ansible` re-extract the same collections underneath each
other. The symptom is a collection that was working moments earlier going missing mid-play:

```
the connection plugin 'community.docker.docker' was not found
```

If you see that, a concurrent run took the collection out from under you.

`ANSIBLE_HOME` is left alone if you have already set it, and is unset in CI - each role runs in its
own job there, so there is nothing to collide with.

The directories are disposable; `var/` is gitignored. Delete `var/molecule-ansible-home/` to force
a fresh install.

## Reclaiming the disk space

`just molecule-clean` removes what the runs leave under `var/`.

Two things live there. The per-role Ansible homes are ~7 MB each, rewritten on every run rather
than grown, so they are bounded by the number of roles that have a scenario. The shared virtualenv
is the bulk of it, over 500 MB, and is recreated on the next run at the cost of a `pip install`.

`--idle-days N` restricts it to what has not been touched in N days, which is what makes it safe to
run unattended. `--yes` skips the confirmation.
