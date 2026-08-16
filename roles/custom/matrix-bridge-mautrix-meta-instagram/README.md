<!--
SPDX-FileCopyrightText: 2024 - 2026 MDAD Contributors

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# matrix-mautrix-meta-instagram

This role installs the Instagram bridge developed in the [mautrix-meta](https://github.com/mautrix/meta) repository.

This role used to be auto-generated from the `matrix-bridge-mautrix-meta-messenger` role, back when a single mautrix-meta binary served both Messenger and Instagram depending on a `mode` configuration setting.
Since mautrix-meta v26.07, Instagram is a separate binary with its own container image (`ig-` prefixed tags) and its own configuration schema, so the two roles are maintained independently.
