FROM geerlingguy/docker-debian12-ansible:latest

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

RUN apt-get update && \
	apt-get install -y --no-install-recommends \
		python3-passlib \
		git \
		pwgen \
		openssh-client \
		curl && \
	rm -rf /var/lib/apt/lists/* && \
	rm -Rf /usr/share/doc && rm -Rf /usr/share/man && \
	apt-get clean

# Install Just
RUN curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s -- --to /usr/local/bin

# Preserve command history across container restarts
RUN SNIPPET="export PROMPT_COMMAND='history -a' && export HISTFILE=/commandhistory/.bash_history" \
    && echo "$SNIPPET" >> "/root/.bashrc"
