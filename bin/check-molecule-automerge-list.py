#!/usr/bin/env python3
"""Keeps the Molecule patch-automerge rule in step with the roles that have a scenario.

.github/renovate.json automerges patch bumps for roles listed by file name, on the grounds that
the bump runs that role's Molecule scenario before merging. That reasoning only holds while the
role actually has one.

The dangerous direction is a role keeping automerge after losing its scenario: bumps would then
merge with nothing exercising them. The harmless direction - a role gaining a scenario without
being added - only means a missed opportunity, but it is reported too, since it is usually an
oversight rather than a decision.
"""

import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
RENOVATE = REPO / ".github" / "renovate.json"
MARKER = "bin/check-molecule-automerge-list.py"


def main() -> int:
    with_scenario = {
        p.parts[-4] for p in (REPO / "roles" / "custom").glob("*/molecule/default/molecule.yml")
    }

    config = json.loads(RENOVATE.read_text())
    rules = [r for r in config.get("packageRules", []) if MARKER in r.get("description", "")]

    if len(rules) != 1:
        print(f"Expected exactly one rule mentioning {MARKER}, found {len(rules)}.", file=sys.stderr)
        return 1

    listed = set()
    for name in rules[0].get("matchFileNames", []):
        parts = pathlib.PurePosixPath(name).parts
        if parts[:2] == ("roles", "custom") and parts[3:] == ("defaults", "main.yml"):
            listed.add(parts[2])
        else:
            print(f"Unexpected entry in the automerge rule: {name}", file=sys.stderr)
            return 1

    automerged_without_scenario = sorted(listed - with_scenario)
    scenario_without_automerge = sorted(with_scenario - listed)

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

    return 1 if (automerged_without_scenario or scenario_without_automerge) else 0


if __name__ == "__main__":
    sys.exit(main())
