#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 MASH project contributors
# SPDX-FileCopyrightText: 2026 Slavi Pantaleev
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# Installs the Ansible roles pinned in a requirements file, without throwing away local changes.
#
# agru replaces an installed role whenever its version differs from the pinned one (and ansible-galaxy with `--force`
# always does), losing any changes made to it. This script decides which roles really need to be (re)installed
# and only passes those to the installer:
#
# - missing roles are installed
# - roles at another version than the pinned one are replaced, unless they have local changes
#   (detected by comparing their contents with a checksum recorded when this script installed them)
# - roles which are symlinks or contain a `.git` directory are managed by a developer and never touched
#
# With `--all-requirements-path` (a requirements file listing all roles the playbook knows about),
# installed roles which are listed there, but not in the requirements file, are deleted, unless they have local changes.
# Roles which are not listed in either file (e.g. a new role being developed) are never touched.

import argparse
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile

try:
    import yaml
except ImportError:
    sys.exit(
        "Installing roles requires the PyYAML Python library. "
        "Install it with your package manager (e.g. `python3-yaml` or `python-yaml`) or pip."
    )

parser = argparse.ArgumentParser(
    description="Installs the Ansible roles pinned in a requirements file, without throwing away local changes"
)
parser.add_argument(
    "--requirements-path",
    help="Path to the requirements file with the roles to install",
    required=True,
)
parser.add_argument(
    "--all-requirements-path",
    help="Path to a requirements file with all known roles. Installed roles listed there, but not in --requirements-path, are deleted",
)
parser.add_argument(
    "--roles-path", help="Path to the directory to install roles into", required=True
)
parser.add_argument(
    "--state-path",
    help="Path to the file recording the checksums of installed roles",
    required=True,
)
parser.add_argument(
    "--installer",
    choices=("auto", "agru", "ansible-galaxy"),
    default="auto",
    help="Tool to install roles with (auto: agru if available, otherwise ansible-galaxy)",
)
parser.add_argument(
    "--force",
    action="store_true",
    help="Also replace and delete roles with local changes",
)
parser.add_argument(
    "--quiet",
    action="store_true",
    help="Do not report anything when all roles are already up to date",
)

args = parser.parse_args()

# Written by agru and ansible-galaxy into each role they install
INSTALL_INFO_RELATIVE_PATH = os.path.join("meta", ".galaxy_install_info")


def load_yaml_file(path):
    with open(path, "r") as file:
        return yaml.safe_load(file) or []


def load_state(path):
    if not os.path.isfile(path):
        return {}
    with open(path, "r") as file:
        return (yaml.safe_load(file) or {}).get("roles", {})


def save_state(path, roles):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    temporary_path = path + ".tmp"
    with open(temporary_path, "w") as file:
        yaml.safe_dump({"roles": roles}, file, sort_keys=True)
    os.replace(temporary_path, path)


def is_managed_by_developer(role_path):
    return os.path.islink(role_path) or os.path.exists(os.path.join(role_path, ".git"))


def installed_version(role_path):
    """Returns the version recorded by the installer, or None if the role was not installed by one."""
    info_path = os.path.join(role_path, INSTALL_INFO_RELATIVE_PATH)
    if not os.path.isfile(info_path):
        return None
    with open(info_path, "r") as file:
        info = yaml.safe_load(file) or {}
    version = info.get("version")
    return None if version is None else str(version)


def checksum(role_path):
    """Returns a checksum of the role's files: their paths, contents, executable bits and symlink targets."""
    digest = hashlib.sha256()
    for directory_path, directory_names, file_names in os.walk(role_path):
        directory_names.sort()
        for name in sorted(file_names):
            path = os.path.join(directory_path, name)
            relative_path = os.path.relpath(path, role_path)
            digest.update(relative_path.encode() + b"\0")
            if os.path.islink(path):
                digest.update(b"link\0" + os.readlink(path).encode() + b"\0")
                continue
            digest.update(b"x\0" if os.stat(path).st_mode & 0o111 else b"-\0")
            with open(path, "rb") as file:
                for chunk in iter(lambda: file.read(1024 * 1024), b""):
                    digest.update(chunk)
            digest.update(b"\0")
    return digest.hexdigest()


def has_local_changes(name, role_path, state):
    """Tells whether the role was changed since this script installed it.

    Roles without a recorded checksum (installed before this script, or by another tool) are considered unchanged.
    """
    recorded = state.get(name)
    if recorded is None or recorded.get("version") != installed_version(role_path):
        return False
    return recorded.get("checksum") != checksum(role_path)


warnings_count = 0


def warn(message):
    global warnings_count
    warnings_count += 1
    print("[WARNING] " + message, file=sys.stderr, flush=True)


def install(role_definitions, roles_path, installer):
    """Installs the given roles, which must not be present in roles_path."""
    if installer == "auto":
        installer = "agru" if shutil.which("agru") else "ansible-galaxy"

    with tempfile.NamedTemporaryFile("w", suffix=".yml", delete=False) as file:
        yaml.safe_dump(role_definitions, file)
        requirements_path = file.name
    try:
        if installer == "agru":
            command = ["agru", "-r", requirements_path, "-p", roles_path, "-no-tui"]
        else:
            print(
                "[NOTE] You are using the standard ansible-galaxy tool to install roles, which is slow and lacks other features. "
                "We recommend installing the 'agru' tool to speed up the process: https://github.com/etkecc/agru#where-to-get",
                flush=True,
            )
            command = ["ansible-galaxy", "install", "-r", requirements_path, "-p", roles_path, "--force"]
        result = subprocess.run(command)
        if result.returncode != 0:
            sys.exit("Installing roles failed ({0} exited with code {1})".format(installer, result.returncode))
    finally:
        os.unlink(requirements_path)


role_definitions = load_yaml_file(args.requirements_path)
known_role_names = {definition["name"] for definition in role_definitions}
if args.all_requirements_path is not None:
    known_role_names |= {definition["name"] for definition in load_yaml_file(args.all_requirements_path)}

state = load_state(args.state_path)
os.makedirs(args.roles_path, exist_ok=True)

to_install = []
to_delete = []
for definition in role_definitions:
    name = definition["name"]
    role_path = os.path.join(args.roles_path, name)
    pinned_version = str(definition["version"])

    if not os.path.lexists(role_path):
        to_install.append(definition)
        continue
    if is_managed_by_developer(role_path):
        continue

    version = installed_version(role_path)
    if version == pinned_version:
        continue

    if version is None:
        reason = "was not installed by agru or ansible-galaxy"
    elif has_local_changes(name, role_path, state):
        reason = "has local changes"
    else:
        reason = None

    if reason is not None and not args.force:
        warn(
            "{0} {1}, so it was not replaced with {2}. Run `just roles --force` to replace it.".format(
                role_path, reason, pinned_version
            )
        )
        continue

    to_delete.append(role_path)
    to_install.append(definition)

required_role_names = {definition["name"] for definition in role_definitions}
for name in sorted(known_role_names - required_role_names):
    role_path = os.path.join(args.roles_path, name)
    if not os.path.lexists(role_path) or is_managed_by_developer(role_path):
        continue
    if installed_version(role_path) is None:
        # Most likely put there by hand, so leave it alone
        continue
    if has_local_changes(name, role_path, state) and not args.force:
        warn(
            "{0} is no longer used, but has local changes, so it was not deleted. Run `just roles --force` to delete it.".format(
                role_path
            )
        )
        continue
    to_delete.append(role_path)
    print("Deleting {0}, which is no longer used".format(role_path), flush=True)

for role_path in to_delete:
    shutil.rmtree(role_path)
    state.pop(os.path.basename(role_path), None)

if len(to_install) > 0:
    print(
        "Installing {0} role(s): {1}".format(
            len(to_install), ", ".join(definition["name"] for definition in to_install)
        ),
        flush=True,
    )
    install(to_install, args.roles_path, args.installer)
    for definition in to_install:
        role_path = os.path.join(args.roles_path, definition["name"])
        state[definition["name"]] = {
            "version": installed_version(role_path),
            "checksum": checksum(role_path),
        }
elif len(to_delete) == 0 and warnings_count == 0 and not args.quiet:
    print("All roles are up to date.")

# Forget roles which are gone
state = {name: recorded for name, recorded in state.items() if os.path.isdir(os.path.join(args.roles_path, name))}
save_state(args.state_path, state)
