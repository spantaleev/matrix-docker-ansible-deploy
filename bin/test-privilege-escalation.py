#!/usr/bin/env python3
# SPDX-FileCopyrightText: NONE
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Check playbook entry points using empty roles and no fact modules.

Usage: python3 bin/test-privilege-escalation.py [ANSIBLE_BIN_DIRECTORY]
Requires PyYAML in the Python environment running this script.
No installed roles, sudo, SSH or Docker are required.
These checks validate inventory and task ordering, not authentication or account switching.
"""

import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import tempfile

import yaml


def run(repo, ansible_bin):
    with tempfile.TemporaryDirectory(prefix="privilege-") as temporary:
        scratch = Path(temporary)
        env = {key: value for key, value in os.environ.items() if not key.startswith("ANSIBLE_")}
        env.update(ANSIBLE_HOME=str(scratch / "home"),
                   ANSIBLE_LOCAL_TEMP=str(scratch / "local-tmp"),
                   ANSIBLE_REMOTE_TEMP=str(scratch / "remote-tmp"),
                   ANSIBLE_CONFIG=str(scratch / "ansible.cfg"),
                   ANSIBLE_NOCOLOR="1", PYTHONDONTWRITEBYTECODE="1", TMPDIR=str(scratch))
        (scratch / "ansible.cfg").write_text("[defaults]\nretry_files_enabled=False\n")
        sources = [repo / "setup.yml", repo / "jitsi_jvb.yml"]
        replacement = re.search(r"`(ansible_ssh_user=username[^`]*)`", (repo / "examples/hosts").read_text())
        if replacement is None:
            raise AssertionError("Cannot find the documented non-root SSH login example in examples/hosts")
        documented_login = dict(part.split("=", 1) for part in shlex.split(replacement.group(1)))
        # name, host variables, extra variables, CLI options, expected success
        cases = [
            ("root-login", {"ansible_ssh_user": "root"}, {}, [], True),
            ("documented-nonroot-login", documented_login, {}, [], True),
            ("method-and-credentials", {"ansible_become_method": "su",
                                        "ansible_become_password": "FAKE_PASSWORD"}, {}, [], True),
            ("copied-inventory", {"ansible_ssh_user": "operator", "ansible_become": True,
                                  "ansible_become_user": "root"}, {}, [], False),
            ("force-on", {"ansible_become": True}, {}, [], False),
            ("force-off", {"ansible_become": False}, {}, [], False),
            ("force-user", {"ansible_become_user": "root"}, {}, [], False),
            ("sudo-alias", {"ansible_sudo_user": "root"}, {}, [], False),
            ("su-alias", {"ansible_su_user": "root"}, {}, [], False),
            ("extra-vars", {}, {"ansible_become_user": "root"}, [], False),
            ("plain-inventory-keys", {"become": False, "become_user": "ignored"}, {}, [], True),
            ("check-valid", {}, {}, ["--check"], True),
            ("check-invalid", {"ansible_become": True}, {}, ["--check"], False),
            ("limit", {"ansible_become": True}, {}, ["--limit", "localhost"], False),
            ("target-override", {"ansible_become": True}, {"target": "fixture_targets"}, [], False),
            ("skip-service-tag", {"ansible_become": True}, {}, ["--skip-tags", "setup-all"], False),
            ("skip-always", {"ansible_become": True}, {}, ["--skip-tags", "always"], True),
            ("start-at-task", {"ansible_become": True}, {}, ["--start-at-task", "Selected task sentinel"], True),
        ]
        forbidden = [
            "ansible_become", "ansible_become_user", "ansible_sudo_user", "ansible_su_user",
            "ansible_doas_user", "ansible_dzdo_user", "ansible_ksu_user", "ansible_machinectl_user",
            "ansible_pbrun_user", "ansible_pfexec_user", "ansible_run0_user", "ansible_sesu_user",
        ]
        validation = "matrix_playbook_privilege_escalation_validation_enabled"
        # name, host variables, group variables, extra variables, CLI options, expected success
        cases = [(name, host, {}, extra, options, success)
                 for name, host, extra, options, success in cases]
        for variable in forbidden:
            value = True if variable == "ansible_become" else "root"
            for scope in ("host", "group", "extra"):
                host, group, extra = {}, {}, {}
                {"host": host, "group": group, "extra": extra}[scope][variable] = value
                cases.append((scope + "-" + variable, host, group, extra, [], False))
        cases.extend([
            ("password-alias", {"ansible_become_pass": "FAKE_PASSWORD"}, {}, {}, [], True),
            ("flags-and-wrapper", {"ansible_become_flags": "-E",
                                   "ansible_become_exe": "/not-executed"}, {}, {}, [], True),
            ("custom-alias-uncovered", {"ansible_fixture_user": "root"}, {}, {}, [], True),
            ("host-vars-file", {}, {}, {}, [], False),
            ("group-vars-file", {}, {}, {}, [], False),
            ("message-several", {"ansible_become": False, "ansible_sesu_user": "root"},
             {"ansible_doas_user": "root"}, {"ansible_become_user": "root"}, [], False),
            ("validation-disabled-clean", {validation: False}, {}, {}, [], True),
            ("host-false-over-group-true", {"ansible_become_user": "root", validation: False},
             {validation: True}, {}, [], True),
            ("extra-false-over-host-true", {"ansible_become_user": "root", validation: True},
             {}, {validation: False}, [], True),
            ("extra-true-over-host-false", {"ansible_become_user": "root", validation: False},
             {}, {validation: True}, [], False),
            ("two-host-one-bad", {"ansible_become_user": "root"}, {}, {}, [], False),
            ("two-host-bad-opted-out", {"ansible_become_user": "root", validation: False},
             {}, {}, [], True),
        ])
        for scope in ("host", "group", "extra"):
            for label, value, success in (("false", False, True), ("string-false", "false", True),
                                          ("true", True, False), ("string-true", "true", False)):
                host, group, extra = {"ansible_become_user": "root"}, {}, {}
                {"host": host, "group": group, "extra": extra}[scope][validation] = value
                cases.append(("validation-" + scope + "-" + label, host, group, extra, [], success))
        count = 0
        for number, source in enumerate(sources):
            fixture = scratch / str(number)
            fixture.mkdir()
            (fixture / "host_vars").mkdir()
            (fixture / "group_vars").mkdir()
            text = source.read_text()
            plays = yaml.safe_load(text)
            # The no-module fixture cannot prove real account switching. Keep the main
            # play's explicit root defaults covered independently of inventory tests.
            if plays[-1].get("become") is not True or plays[-1].get("become_user") != "root":
                raise AssertionError("Main play must set become: true and become_user: root: " + str(source))
            role_names = []
            for play in plays:
                for role in play.get("roles", []):
                    name = role if isinstance(role, str) else role["role"]
                    tasks = fixture / "roles" / name / "tasks"
                    tasks.mkdir(parents=True, exist_ok=True)
                    (tasks / "main.yml").write_text("[]\n")
                    role_names.append(name)
            if not role_names:
                raise AssertionError("No roles found in playbook: " + str(source))
            (fixture / "roles" / role_names[0] / "tasks/main.yml").write_text(
                "- name: Role sentinel\n  ansible.builtin.debug:\n    msg: 'ROLE_BODY_REACHED {{ inventory_hostname }}'\n"
                "  tags: [always]\n")
            # Keep production bytes, including automatic fact gathering. An empty facts
            # module list makes that task controller-only without disabling its ordering.
            (fixture / "play.yml").write_text(text + "\n  tasks:\n"
                "    - name: Selected task sentinel\n      ansible.builtin.debug:\n"
                "        msg: 'SELECTED_TASK_REACHED {{ inventory_hostname }}'\n      tags: [privilege-fixture]\n")
            for name, host_vars, group_vars, extra_vars, options, success in cases:
                hosts = {"localhost": host_vars}
                mixed = name.startswith("two-host-")
                if mixed:
                    hosts["good"] = {"ansible_connection": "local", "ansible_host": "localhost"}
                inventory = {"all": {"vars": {"ansible_facts_modules": [],
                                              "ansible_facts_parallel": False, **group_vars}, "children": {
                    # Populate only the main play's own group, so a validation play aimed
                    # at another group cannot pass.
                    group: {"hosts": hosts if group in str(plays[-1]["hosts"]) or group == "fixture_targets" else {}}
                    for group in ("matrix_servers", "jitsi_jvb_servers", "fixture_targets")}}}
                if name == "target-override" and "target" in str(plays[-1]["hosts"]):
                    for group in inventory["all"]["children"]:
                        if group != "fixture_targets":
                            inventory["all"]["children"][group]["hosts"] = {}
                file_vars = {}
                for scope, filename in (("host", "host_vars/localhost.yml"), ("group", "group_vars/all.yml")):
                    variables_file = fixture / filename
                    if variables_file.exists():
                        variables_file.unlink()
                    if name == scope + "-vars-file":
                        file_vars = {variable: True if variable == "ansible_become" else "root"
                                     for variable in forbidden}
                        variables_file.write_text(yaml.safe_dump(file_vars))
                (fixture / "inventory.json").write_text(json.dumps(inventory))
                command = [str(ansible_bin / "ansible-playbook"), "--connection=local", "-i",
                           str(fixture / "inventory.json"), str(fixture / "play.yml"),
                           "--tags", "privilege-fixture", "-e", json.dumps(extra_vars), *options]
                result = subprocess.run(command, env=env, cwd=fixture, text=True,
                                        capture_output=True, timeout=45)
                output = result.stdout + result.stderr
                label = source.name + "[" + str(number) + "]/" + name
                if success:
                    passed = result.returncode == 0 and "SELECTED_TASK_REACHED" in output
                    if name not in ("skip-always", "start-at-task"):
                        passed = passed and "ROLE_BODY_REACHED" in output and "Gathering Facts" in output
                else:
                    defined = {**group_vars, **host_vars, **file_vars, **extra_vars}
                    expected_names = [variable for variable in forbidden if variable in defined]
                    message = re.search(r"Remove (.*?) wherever you define them", output)
                    passed = (result.returncode == 2 and message is not None
                              and message.group(1) == ", ".join(expected_names)
                              and "\\n" not in output[output.index("overrides are defined"):].split("\n", 1)[0])
                    if mixed:
                        facts = output.split("TASK [Gathering Facts]", 1)[-1].split("TASK [", 1)[0]
                        passed = (passed and "ROLE_BODY_REACHED good" in output
                                  and "SELECTED_TASK_REACHED good" in output
                                  and "ROLE_BODY_REACHED localhost" not in output
                                  and "SELECTED_TASK_REACHED localhost" not in output
                                  and "ok: [good]" in facts and "ok: [localhost]" not in facts)
                    else:
                        passed = (passed and "Gathering Facts" not in output
                                  and "ROLE_BODY_REACHED" not in output and "SELECTED_TASK_REACHED" not in output)
                if mixed and success:
                    passed = (passed and all(marker + " " + host in output
                              for marker in ("ROLE_BODY_REACHED", "SELECTED_TASK_REACHED")
                              for host in ("localhost", "good")))
                passed = passed and "[DEPRECATION WARNING]" not in output
                if not passed:
                    raise AssertionError(label + "\n" + repr(command) + "\n" + output)
                print("PASS " + label, flush=True)
                count += 1
        print(str(count) + " cases passed", flush=True)


if __name__ == "__main__":
    executable = shutil.which("ansible-playbook")
    if len(sys.argv) == 1 and executable is None:
        sys.exit("Install ansible-core or pass ANSIBLE_BIN_DIRECTORY as the first argument")
    binaries = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(executable).parent
    run(Path(__file__).resolve().parent.parent, binaries.resolve())
