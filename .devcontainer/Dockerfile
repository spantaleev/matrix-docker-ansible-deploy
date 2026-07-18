# SPDX-FileCopyrightText: 2025 Jonah Aragon
#
# SPDX-License-Identifier: AGPL-3.0-or-later

FROM ghcr.io/devture/ansible:14.0.0-r0-0

# Install additional packages
RUN apk add --no-cache \
	pwgen

# Preserve command history across container restarts
RUN SNIPPET="export HISTFILE=/commandhistory/.ash_history" \
	&& echo "$SNIPPET" >> "/root/.profile"
