#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2026 Slavi Pantaleev
#
# SPDX-License-Identifier: AGPL-3.0-or-later

set -euo pipefail

repo_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

# An optional image version lets maintainers reproduce failures before changing the pin.
mapfile -t versions < <(
    sed -n "s/^  MATRIX_RENOVATE_VERSION: '\([^']*\)'$/\1/p" \
        "$repo_dir/.github/workflows/renovate.yml"
)
if (( ${#versions[@]} != 1 )) || [[ -z "${versions[0]}" ]]; then
    echo 'Could not resolve exactly one pinned Renovate version' >&2
    exit 1
fi
version="${1:-${versions[0]}}"
image="ghcr.io/renovatebot/renovate:$version"
log_file="$(mktemp)"
trap 'rm -f -- "$log_file"' EXIT

# Use the image's normal entrypoint for extraction, loading the real runtime.
# No credentials or network are needed for validation and dependency extraction.
docker_args=(
    --rm
    --network none
    --volume "$repo_dir:/workspace:ro"
    --workdir /workspace
    --env NODE_OPTIONS=--unhandled-rejections=strict
)

echo "Validating configuration with $image"
docker run "${docker_args[@]}" \
    --entrypoint renovate-config-validator \
    "$image" --strict

echo "Extracting dependencies with $image"
docker run "${docker_args[@]}" \
    --env LOG_LEVEL=info \
    --env LOG_FORMAT=json \
    "$image" --platform=local --dry-run=extract \
    | tee "$log_file"

# Exit status alone is insufficient: 44.64.0 crashed at startup but exited 0.
# Require completion and useful results from every manager used by this repository.
# The missing-token warning is expected: extraction needs no GitHub API access.
if ! jq --slurp --exit-status '
    all(.[]; .level < 50)
    and any(.[]; .msg == "Repository finished" and .repository == "local")
    and any(.[];
        .msg == "Dependency extraction complete"
        and (.stats.managers as $managers
            | all(["ansible-galaxy", "dockerfile", "github-actions", "mise", "nix", "pip_requirements", "pre-commit", "regex"][];
                $managers[.].depCount > 0))
    )
    and any(.[];
        .msg == "Extracted dependencies"
        and any(.packageFiles["ansible-galaxy"][]?;
            .packageFile == "requirements.yml" and (.deps | length) > 0)
        and any(.packageFiles.regex[]?;
            (.packageFile | startswith("roles/custom/")) and (.deps | length) > 0)
        and any(.packageFiles.regex[]?;
            .packageFile == "molecule-shared/vars.yml" and (.deps | length) > 0)
        and any(.packageFiles.regex[]?.deps[]?;
            .depName == "matrix-renovate-runner" and .datasource == "docker")
    )
' "$log_file"; then
    echo 'Renovate did not complete dependency extraction successfully' >&2
    exit 1
fi

echo "Renovate $version passed configuration validation and dependency extraction"
