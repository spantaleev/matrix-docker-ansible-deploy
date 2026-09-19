# SPDX-FileCopyrightText: 2026 Slavi Pantaleev
#
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Select Molecule scenarios affected by a Git comparison, using only the stdlib.

Shared dependencies use literal molecule-shared/... paths and image variable names.
Follow these references transitively, in both revisions. This is deliberately not an
Ansible interpreter: unfamiliar image-pin syntax or unresolved dependencies run all
scenarios instead of risking an incomplete automerge gate.
"""

import argparse
import json
import os
import posixpath
import re
import subprocess
import sys
from pathlib import Path

IMAGE_VARS = "molecule-shared/vars.yml"
GLOBAL_FILES = {
    "molecule-shared/requirements.txt",
    "molecule-shared/requirements.yml",
    "molecule-shared/playbook-context.yml",
    ".github/workflows/molecule.yml",
    "bin/molecule-select-roles.py",
    "bin/test-molecule-select-roles.py",
}
SCENARIO = re.compile(r"roles/custom/([^/]+)/molecule/default/molecule\.yml$")
SHARED_PATH = re.compile(r"molecule-shared/[\w./-]+")
IMAGE_NAME = re.compile(r"\bmolecule_shared_image_\w+\b")
IMAGE_PIN = re.compile(r"(molecule_shared_image_\w+):\s*(['\"])([\w./:@+-]+)\2\s*(?:#.*)?$")


class Uncertain(Exception):
    """The change cannot safely be narrowed to particular scenarios."""


class Git:
    def __init__(self, root):
        self.root = root

    def run(self, *args, input=None):
        return subprocess.run(
            ["git", *args], cwd=self.root, input=input, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, check=True,
        ).stdout

    def commit(self, ref):
        return self.run("rev-parse", "--verify", "--end-of-options", f"{ref}^{{commit}}").decode().strip()

    def snapshot(self, ref):
        entries = {}
        for entry in self.run("ls-tree", "-rz", ref, "--", "roles/custom", "molecule-shared").split(b"\0"):
            if not entry:
                continue
            metadata, path = entry.decode().split("\t", 1)
            mode, kind, oid = metadata.split()
            if path.startswith("molecule-shared/") or "/molecule/" in path:
                if kind != "blob":
                    raise Uncertain(f"Unsupported Git entry: {path}")
                entries[path] = (mode, oid)

        # Read the blobs in one process; a subprocess per scenario file is slow.
        oids = list(dict.fromkeys(oid for mode, oid in entries.values()))
        data = self.run("cat-file", "--batch", input="".join(f"{oid}\n" for oid in oids).encode())
        blobs = {}
        offset = 0
        for oid in oids:
            end = data.index(b"\n", offset)
            size = int(data[offset:end].split()[2])
            blobs[oid] = data[end + 1:end + 1 + size].decode()
            offset = end + size + 2
        return {path: (mode, blobs[oid]) for path, (mode, oid) in entries.items()}


def comparison_base(git, head, env):
    """Preserve push/PR comparison semantics, including new Renovate branches."""
    try:
        if env.get("EVENT_NAME") == "pull_request":
            return git.commit(env["BASE_SHA"])
        if env.get("EVENT_NAME") == "push":
            before = env.get("BEFORE_SHA", "")
            if before and set(before) != {"0"}:
                try:
                    return git.commit(before)
                except subprocess.CalledProcessError:
                    pass
            default = env.get("DEFAULT_BRANCH", "")
            if default and env.get("GITHUB_REF") != f"refs/heads/{default}":
                return git.run("merge-base", head, f"refs/remotes/origin/{default}").decode().strip()
    except (KeyError, subprocess.CalledProcessError):
        pass
    return None


def image_pins(snapshot):
    """Accept only flat, quoted literal image pins; other YAML runs all scenarios."""
    if IMAGE_VARS not in snapshot or snapshot[IMAGE_VARS][0] == "120000":
        raise Uncertain("Missing or symlinked shared image pins")
    pins = {}
    document_started = False
    for line in snapshot[IMAGE_VARS][1].splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        if line == "---" and not pins and not document_started:
            document_started = True
            continue
        match = IMAGE_PIN.fullmatch(line)
        if not match or match[1] in pins:
            raise Uncertain("Unrecognized shared image-pin format")
        pins[match[1]] = match[3]
    if not pins:
        raise Uncertain("No shared image pins")
    return pins


def dependencies(snapshot, role):
    """Return file and variable dependencies, following shared files and symlinks.

    Scan all scenario files, including nested tasks and fixtures. Ignore full-line
    comments. Do not scan vars.yml's definitions: loading the mapping does not
    mean a scenario uses every image in it.
    """
    pending = [path for path in snapshot if path.startswith(f"roles/custom/{role}/molecule/")]
    files, variables = set(), set()
    while pending:
        path = pending.pop()
        if path in files:
            continue
        files.add(path)
        if path not in snapshot:
            raise Uncertain(f"Unresolved dependency: {path}")
        mode, content = snapshot[path]
        if mode == "120000":
            pending.append(posixpath.normpath(posixpath.join(posixpath.dirname(path), content)))
            continue
        if path == IMAGE_VARS:
            continue
        content = "\n".join(line for line in content.splitlines() if not line.lstrip().startswith("#"))
        references = SHARED_PATH.findall(content)
        if content.count("molecule-shared/") != len(references):
            raise Uncertain(f"Nonliteral shared dependency in {path}")
        pending.extend(references)
        names = IMAGE_NAME.findall(content)
        if content.count("molecule_shared_image_") != len(names):
            raise Uncertain(f"Nonliteral shared image variable in {path}")
        variables.update(names)
    return files, variables


def select_roles(git, base, head="HEAD", role=""):
    # Failure to enumerate the head must fail the job, never report an empty gate.
    paths = git.run("ls-tree", "-rz", "--name-only", head, "--", "roles/custom").decode().split("\0")
    available = {match[1] for path in paths if (match := SCENARIO.fullmatch(path))}
    if role:
        if role not in available:
            raise ValueError(f"No scenario at roles/custom/{role}/molecule/default")
        return [role]
    if not base:
        print("No comparison requested or available; testing every scenario", file=sys.stderr)
        return sorted(available)

    try:
        # Disable rename detection so both old and new paths contribute consumers.
        diff = git.run("diff", "--no-renames", "--name-only", "-z", base, head, "--")
        changed = set(diff.decode().split("\0")) - {""}
        if changed & GLOBAL_FILES:
            raise Uncertain("Test infrastructure changed: " + ", ".join(sorted(changed & GLOBAL_FILES)))
        selected = {path.split("/")[2] for path in changed if path.startswith("roles/custom/")}
        shared = {path for path in changed if path.startswith("molecule-shared/")}
        if shared:
            snapshots = [git.snapshot(base), git.snapshot(head)]
            changed_images = set()
            if IMAGE_VARS in shared:
                old, new = map(image_pins, snapshots)
                if old.keys() != new.keys():
                    raise Uncertain("Shared image variables added or removed")
                changed_images = {key for key in old if old[key] != new[key]}
                shared.remove(IMAGE_VARS)

            if shared or changed_images:
                consumers = {dependency: set() for dependency in shared | changed_images}
                for snapshot in snapshots:
                    for candidate in available:
                        files, variables = dependencies(snapshot, candidate)
                        for dependency in consumers.keys() & (files | variables):
                            consumers[dependency].add(candidate)
                for dependency, roles in sorted(consumers.items()):
                    if not roles:
                        raise Uncertain(f"No known consumers for {dependency}")
                    print(f"{dependency}: {len(roles)} scenario(s)", file=sys.stderr)
                    selected.update(roles)
        return sorted(selected & available)
    except (Uncertain, subprocess.CalledProcessError, UnicodeError) as exc:
        print(f"Testing every scenario: {exc}", file=sys.stderr)
        return sorted(available)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", help="Compare against this revision; otherwise use GitHub event variables")
    parser.add_argument("--head", default="HEAD", help="Revision to test (default: HEAD)")
    parser.add_argument("--role", default=os.environ.get("INPUT_ROLE", ""), help="Run one named role")
    args = parser.parse_args()
    git = Git(Path.cwd())
    base = args.base if args.base is not None else comparison_base(git, args.head, os.environ)
    roles = select_roles(git, base, args.head, args.role)
    result = json.dumps(roles, separators=(",", ":"))
    print(result)
    if output := os.environ.get("GITHUB_OUTPUT"):
        with open(output, "a") as stream:
            stream.write(f"roles={result}\n")


if __name__ == "__main__":
    main()
