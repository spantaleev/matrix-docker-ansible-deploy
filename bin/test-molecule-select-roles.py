# SPDX-FileCopyrightText: 2026 Slavi Pantaleev
#
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Regression tests for the Molecule CI matrix; no Docker or Python packages needed."""

import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

# Importing the script should not leave __pycache__ in the repository.
sys.dont_write_bytecode = True
SCRIPT = Path(__file__).with_name("molecule-select-roles.py")
SPEC = importlib.util.spec_from_file_location("selector", SCRIPT)
selector = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(selector)


class SelectionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git = selector.Git(self.root)
        self.git.run("init", "--quiet", "--initial-branch=main")
        self.git.run("config", "user.name", "Molecule selector test")
        self.git.run("config", "user.email", "test@example.com")
        self.git.run("config", "commit.gpgsign", "false")
        self.roles = ["matrix-database", "matrix-livekit", "matrix-web"]
        self.write(selector.IMAGE_VARS, '\n'.join([
            '---',
            'molecule_shared_image_curl: "curl:1"',
            'molecule_shared_image_postgres: "postgres:1"',
            'molecule_shared_image_livekit: "livekit:1"',
        ]) + '\n')
        self.write("molecule-shared/requirements.yml", "roles: []\n")
        self.write("molecule-shared/tasks/postgres.yml", '{{ molecule_shared_image_postgres }}\n')
        self.write("molecule-shared/tasks/probe.yml", "molecule-shared/probe.py\n")
        self.write("molecule-shared/probe.py", "print('probe')\n")
        for role in self.roles:
            self.write(f"roles/custom/{role}/molecule/default/molecule.yml", "---\n")
            self.scenario(role, "verify.yml", '{{ molecule_shared_image_curl }}\n')
            self.scenario(role, "prepare.yml", "molecule-shared/vars.yml\n")
            self.path(f"roles/custom/{role}/molecule/default/requirements.yml").symlink_to(
                "../../../../../molecule-shared/requirements.yml"
            )
        self.scenario("matrix-database", "prepare.yml", "molecule-shared/vars.yml\nmolecule-shared/tasks/postgres.yml\n")
        self.scenario("matrix-livekit", "tasks/sfu.yml", '{{ molecule_shared_image_livekit }}\n')
        self.scenario("matrix-web", "tasks/probe.yml", "molecule-shared/tasks/probe.yml\n")
        self.base = self.commit()
        self.git.run("update-ref", "refs/remotes/origin/main", self.base)

    def path(self, name):
        return self.root / name

    def write(self, name, content):
        path = self.path(name)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)

    def scenario(self, role, name, content):
        self.write(f"roles/custom/{role}/molecule/default/{name}", content)

    def commit(self):
        self.git.run("add", "--all")
        self.git.run("commit", "--quiet", "--allow-empty", "-m", "Test fixture")
        return self.git.commit("HEAD")

    def bump(self, image):
        path = self.path(selector.IMAGE_VARS)
        path.write_text(path.read_text().replace(f'"{image}:1"', f'"{image}:2"'))

    def selected(self, base=None):
        self.commit()
        with contextlib.redirect_stderr(io.StringIO()):
            return selector.select_roles(self.git, base or self.base)

    def test_livekit_bump_only_runs_its_consumer(self):
        self.bump("livekit")
        self.assertEqual(self.selected(), ["matrix-livekit"])

    def test_postgres_bump_follows_shared_task(self):
        self.bump("postgres")
        self.assertEqual(self.selected(), ["matrix-database"])

    def test_curl_bump_runs_every_consumer(self):
        self.bump("curl")
        self.assertEqual(self.selected(), self.roles)

    def test_multiple_image_bumps_union_with_direct_role_changes(self):
        self.bump("livekit")
        self.bump("postgres")
        self.write("roles/custom/matrix-web/defaults/main.yml", "version: 2\n")
        self.assertEqual(self.selected(), self.roles)

    def test_direct_changes_ignore_roles_without_scenarios(self):
        self.write("roles/custom/matrix-web/defaults/main.yml", "version: 2\n")
        self.write("roles/custom/matrix-untested/defaults/main.yml", "version: 2\n")
        self.assertEqual(self.selected(), ["matrix-web"])

    def test_documentation_change_runs_nothing(self):
        self.write("docs/example.md", "Documentation\n")
        self.assertEqual(self.selected(), [])

    def test_image_pin_comments_and_quoting_do_not_run_scenarios(self):
        path = self.path(selector.IMAGE_VARS)
        path.write_text("# New comment\n" + path.read_text().replace('"', "'"))
        self.assertEqual(self.selected(), [])

    def test_shared_task_change_only_runs_consumers(self):
        self.write("molecule-shared/tasks/postgres.yml", '{{ molecule_shared_image_postgres }}\n# Changed\n')
        self.assertEqual(self.selected(), ["matrix-database"])

    def test_shared_fixture_change_follows_nested_references(self):
        self.write("molecule-shared/probe.py", "print('updated probe')\n")
        self.assertEqual(self.selected(), ["matrix-web"])

    def test_deleted_helper_uses_previous_consumers(self):
        self.path("molecule-shared/probe.py").unlink()
        self.write("molecule-shared/tasks/probe.yml", "# Probe removed\n")
        self.assertEqual(self.selected(), ["matrix-web"])

    def test_renamed_helper_unions_previous_and_current_consumers(self):
        self.path("molecule-shared/probe.py").rename(self.path("molecule-shared/new-probe.py"))
        self.write("molecule-shared/tasks/probe.yml", "# Probe moved\n")
        self.scenario("matrix-livekit", "tasks/new-probe.yml", "molecule-shared/new-probe.py\n")
        self.assertEqual(self.selected(), ["matrix-livekit", "matrix-web"])

    def test_deleted_role_is_not_selected(self):
        self.path("roles/custom/matrix-livekit/molecule/default/molecule.yml").unlink()
        self.assertEqual(self.selected(), [])

    def test_new_scenario_is_selected(self):
        self.write("roles/custom/matrix-new/molecule/default/molecule.yml", "---\n")
        self.assertEqual(self.selected(), ["matrix-new"])

    def test_global_changes_run_all(self):
        for name in sorted(selector.GLOBAL_FILES):
            with self.subTest(name=name):
                self.git.run("reset", "--hard", self.base)
                self.write(name, "# Infrastructure changed\n")
                self.assertEqual(self.selected(), self.roles)

    def test_unknown_shared_file_runs_all(self):
        self.write("molecule-shared/new-helper.yml", "---\n")
        self.assertEqual(self.selected(), self.roles)

    def test_unconsumed_image_bump_runs_all(self):
        self.scenario("matrix-livekit", "tasks/sfu.yml", "# No image reference\n")
        self.base = self.commit()
        self.bump("livekit")
        self.assertEqual(self.selected(), self.roles)

    def test_unsupported_pins_run_all(self):
        original = self.path(selector.IMAGE_VARS).read_text()
        for content in [
            '---\n' + original,
            original + 'other_setting: true\n',
            original + 'molecule_shared_image_new: "new:1"\n',
            original.replace('molecule_shared_image_livekit: "livekit:1"\n', ''),
            original + 'molecule_shared_image_curl: "curl:2"\n',
            original.replace('"livekit:1"', '"{{ another_variable }}"'),
        ]:
            with self.subTest(content=content):
                self.write(selector.IMAGE_VARS, content)
                self.assertEqual(self.selected(), self.roles)

    def test_missing_pins_run_all(self):
        self.path(selector.IMAGE_VARS).unlink()
        self.assertEqual(self.selected(), self.roles)

    def test_unresolved_references_run_all(self):
        for reference in [
            'molecule-shared/tasks/{{ helper }}.yml',
            'molecule-shared/{{ helper }}.yml',
            'molecule-shared/missing.yml',
            "{{ lookup('vars', 'molecule_shared_image_' + name) }}",
        ]:
            with self.subTest(reference=reference):
                self.scenario("matrix-web", "tasks/dynamic.yml", reference)
                self.bump("livekit")
                self.assertEqual(self.selected(), self.roles)

    def test_shared_reference_cycles_terminate(self):
        self.write("molecule-shared/tasks/postgres.yml", 'molecule-shared/tasks/postgres.yml\n{{ molecule_shared_image_postgres }}\n')
        self.assertEqual(self.selected(), ["matrix-database"])

    def test_comments_do_not_introduce_unresolved_references(self):
        self.scenario("matrix-web", "tasks/comments.yml", "# See molecule-shared/probe.py.\n# Helpers live in molecule-shared/.\n")
        self.base = self.commit()
        self.bump("livekit")
        self.assertEqual(self.selected(), ["matrix-livekit"])

    def test_symlinked_shared_helper_is_followed(self):
        self.path("molecule-shared/tasks/probe.yml").unlink()
        self.path("molecule-shared/tasks/probe.yml").symlink_to("../probe.py")
        self.base = self.commit()
        self.write("molecule-shared/probe.py", "print('changed')\n")
        self.assertEqual(self.selected(), ["matrix-web"])

    def test_invalid_comparison_runs_all(self):
        self.assertEqual(self.selected(base="missing-commit"), self.roles)

    def test_manual_dispatch_all_or_one_role(self):
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(selector.select_roles(self.git, None), self.roles)
        self.assertEqual(selector.select_roles(self.git, None, role="matrix-web"), ["matrix-web"])
        with self.assertRaises(ValueError):
            selector.select_roles(self.git, None, role="../outside")

    def test_event_comparison_bases(self):
        self.bump("livekit")
        head = self.commit()
        push = {"EVENT_NAME": "push", "DEFAULT_BRANCH": "main", "GITHUB_REF": "refs/heads/renovate/test"}
        for before in [self.base, "0" * 40, "unavailable", ""]:
            with self.subTest(before=before):
                self.assertEqual(selector.comparison_base(self.git, head, dict(push, BEFORE_SHA=before)), self.base)
        self.assertEqual(selector.comparison_base(self.git, head, {"EVENT_NAME": "pull_request", "BASE_SHA": self.base}), self.base)
        self.assertIsNone(selector.comparison_base(self.git, head, {"EVENT_NAME": "workflow_dispatch"}))
        self.assertIsNone(selector.comparison_base(self.git, head, dict(push, GITHUB_REF="refs/heads/main")))
        self.assertIsNone(selector.comparison_base(self.git, head, dict(push, DEFAULT_BRANCH="missing")))
        self.assertIsNone(selector.comparison_base(self.git, head, {"EVENT_NAME": "pull_request", "BASE_SHA": "missing"}))

    def test_cli_writes_github_output(self):
        self.bump("livekit")
        self.commit()
        output = self.path("github-output")
        output.write_text("previous=value\n")
        env = dict(os.environ, INPUT_ROLE="", GITHUB_OUTPUT=str(output))
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--base", self.base], cwd=self.root,
            env=env, capture_output=True, text=True, check=True,
        )
        self.assertEqual(json.loads(result.stdout), ["matrix-livekit"])
        self.assertEqual(output.read_text(), 'previous=value\nroles=["matrix-livekit"]\n')


if __name__ == "__main__":
    unittest.main()
