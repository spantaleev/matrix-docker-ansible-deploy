FROM ghcr.io/devture/ansible:11.1.0-r0-0

# Install additional packages
RUN apk add --no-cache \
	pwgen

# Preserve command history across container restarts
RUN SNIPPET="export HISTFILE=/commandhistory/.ash_history" \
	&& echo "$SNIPPET" >> "/root/.profile"
