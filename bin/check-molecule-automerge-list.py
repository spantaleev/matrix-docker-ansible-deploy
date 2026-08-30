#!/usr/bin/env python3
"""Keeps Molecule-backed automerge rules in step with the available scenarios.

.github/renovate.json automerges patch bumps for every role with a scenario. A narrower list of
explicitly approved roles also automerges minor bumps. In both cases, the bump runs that role's
Molecule scenario before merging, so the reasoning only holds while the role actually has one.

The patch list must exactly match the scenarios. The minor list must be a subset of it: omission is
an explicit policy choice, while an extra entry would merge a minor bump without the required gate.
"""

import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
RENOVATE = REPO / ".github" / "renovate.json"
PATCH_RULE_MARKER = "bin/check-molecule-automerge-list.py (patch rule)"
MINOR_RULE_MARKER = "bin/check-molecule-automerge-list.py (minor rule)"


def find_rule(config: dict, marker: str) -> dict | None:
    rules = [r for r in config.get("packageRules", []) if marker in r.get("description", "")]
    if len(rules) != 1:
        print(f"Expected exactly one rule mentioning {marker}, found {len(rules)}.", file=sys.stderr)
        return None
    return rules[0]


def listed_roles(rule: dict, label: str) -> set[str] | None:
    listed = set()
    for name in rule.get("matchFileNames", []):
        parts = pathlib.PurePosixPath(name).parts
        if parts[:2] == ("roles", "custom") and parts[3:] == ("defaults", "main.yml"):
            listed.add(parts[2])
        else:
            print(f"Unexpected entry in the Molecule {label} automerge rule: {name}", file=sys.stderr)
            return None
    return listed


def main() -> int:
    with_scenario = {
        p.parts[-4] for p in (REPO / "roles" / "custom").glob("*/molecule/default/molecule.yml")
    }

    config = json.loads(RENOVATE.read_text())
    patch_rule = find_rule(config, PATCH_RULE_MARKER)
    minor_rule = find_rule(config, MINOR_RULE_MARKER)
    if patch_rule is None or minor_rule is None:
        return 1

    patch_roles = listed_roles(patch_rule, "patch")
    minor_roles = listed_roles(minor_rule, "minor")
    if patch_roles is None or minor_roles is None:
        return 1

    errors = False
    if set(patch_rule.get("matchUpdateTypes", [])) != {"patch"}:
        print("The Molecule patch automerge rule must match only patch updates.", file=sys.stderr)
        errors = True
    if set(minor_rule.get("matchUpdateTypes", [])) != {"minor"}:
        print("The Molecule minor automerge rule must match only minor updates.", file=sys.stderr)
        errors = True

    automerged_without_scenario = sorted(patch_roles - with_scenario)
    scenario_without_automerge = sorted(with_scenario - patch_roles)

    if automerged_without_scenario:
        print(
            "These roles automerge patch bumps but have no Molecule scenario, so nothing would\n"
            "exercise the bump before it merges. Remove them from the rule in\n"
            ".github/renovate.json, or give them a scenario:",
            file=sys.stderr,
        )
        for role in automerged_without_scenario:
            print(f"  {role}", file=sys.stderr)

    if scenario_without_automerge:
        print(
            "These roles have a Molecule scenario but are not in the automerge rule in\n"
            ".github/renovate.json, so their patch bumps still need a button press:",
            file=sys.stderr,
        )
        for role in scenario_without_automerge:
            print(f"  {role}", file=sys.stderr)

    minor_without_scenario = sorted(minor_roles - with_scenario)
    minor_without_patch = sorted(minor_roles - patch_roles)

    if minor_without_scenario:
        print(
            "These roles automerge minor bumps but have no Molecule scenario:",
            file=sys.stderr,
        )
        for role in minor_without_scenario:
            print(f"  {role}", file=sys.stderr)

    if minor_without_patch:
        print(
            "These roles automerge minor bumps but are missing from the patch rule:",
            file=sys.stderr,
        )
        for role in minor_without_patch:
            print(f"  {role}", file=sys.stderr)

    return 1 if any(
        [
            errors,
            automerged_without_scenario,
            scenario_without_automerge,
            minor_without_scenario,
            minor_without_patch,
        ]
    ) else 0


if __name__ == "__main__":
    sys.exit(main())
