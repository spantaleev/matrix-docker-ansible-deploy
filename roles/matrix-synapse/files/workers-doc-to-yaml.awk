#!/usr/bin/awk
# Hackish approach to get a machine-readable list of current matrix
# synapse REST API endpoints from the official documentation at
# https://github.com/matrix-org/synapse/raw/master/docs/workers.md
#
# invoke in shell with:
# URL=https://github.com/matrix-org/synapse/raw/master/docs/workers.md
# curl -L ${URL} | awk -f workers-doc-to-yaml.awk -

function worker_stanza_append(string) {
    worker_stanza = worker_stanza string
}

function line_is_endpoint_url(line) {
    # probably API endpoint if it starts with white-space and ^ or /
    return (line ~ /^ +[\^\/].*\//)
}

# Put YAML marker at beginning of file.
BEGIN {
    print "---"
    endpoint_conditional_comment = "  # FIXME: ADDITIONAL CONDITIONS REQUIRED: to be enabled manually\n"
}

# Enable further processing after the introductory text.
# Read each synapse worker section as record and its lines as fields.
/Available worker applications/ {
    enable_parsing = 1
    # set record separator to markdown section header
    RS = "\n### "
    # set field separator to newline
    FS = "\n"
}

# Once parsing is active, this will process each section as record.
enable_parsing {
    # Each worker section starts with a synapse.app.X headline
    if ($1 ~ /synapse\.app\./) {

        # get rid of the backticks and extract worker type from headline
        gsub("`", "", $1)
        gsub("synapse.app.", "", $1)
        worker_type = $1

        # initialize empty worker stanza
        worker_stanza = ""

        # track if any endpoints are mentioned in a specific section
        worker_has_urls = 0

        # some endpoint descriptions contain flag terms
        endpoints_seem_conditional = 0

        # also, collect a list of available workers
        workers = (workers ? workers "\n" : "") "  - " worker_type

        # loop through the lines (2 - number of fields in record)
        for (i = 1; i < NF + 1; i++) {
            # copy line for gsub replacements
            line = $i

            # end all lines but the last with a linefeed
            linefeed = (i < NF - 1) ? "\n" : ""

            # line starts with white-space and a hash: endpoint block headline
            if (line ~ /^ +#/) {

                # copy to output verbatim, normalizing white-space
                gsub(/^ +/, "", line)
                worker_stanza_append("  " line linefeed)

            } else if (line_is_endpoint_url(line)) {

                # mark section for special output formatting
                worker_has_urls = 1

                # remove leading white-space
                gsub(/^ +/, "", line)
                api_endpoint_regex = line

                # FIXME: https://github.com/matrix-org/synapse/issues/new
                # munge inconsistent media_repository endpoint notation
                if (api_endpoint_regex == "/_matrix/media/") {
                    api_endpoint_regex = "^" line
                }

                # FIXME: https://github.com/matrix-org/synapse/issues/7530
                # https://github.com/spantaleev/matrix-docker-ansible-deploy/pull/456#issuecomment-719015911
                if (api_endpoint_regex == "^/_matrix/client/(r0|unstable)/auth/.*/fallback/web$") {
                    worker_stanza_append("  # FIXME: possible bug with SSO and multiple generic workers\n")
                    worker_stanza_append("  # see https://github.com/matrix-org/synapse/issues/7530\n")
                    worker_stanza_append("  # " api_endpoint_regex linefeed)
                    continue
                }

                # disable endpoints which specify complications
                if (endpoints_seem_conditional) {
                    # only add notice if previous line didn't match
                    if (!line_is_endpoint_url($(i - 1))) {
                        worker_stanza_append(endpoint_conditional_comment)
                    }
                    worker_stanza_append("  # " api_endpoint_regex linefeed)
                } else {
                    # output endpoint regex
                    worker_stanza_append("  - " api_endpoint_regex linefeed)
                }

            # white-space only line?
            } else if (line ~ /^\w*$/) {

                if (i > 3 && i < NF) {
                    # print white-space lines unless 1st or last line in section
                    worker_stanza_append(line linefeed)
                }

            # nothing of the above: the line is regular documentation text
            } else {

                # include this text line as comment
                worker_stanza_append("  # " line linefeed)

                # and take note of words hinting at additional conditions to be met
                if (line ~ /\<[Ii]f\>|\<[Ff]or\>/) {
                    endpoints_seem_conditional = 1
                }
            }
        }

        if (worker_has_urls) {
            print "\nmatrix_synapse_workers_" worker_type "_endpoints:"
            print worker_stanza
        } else {
            # include workers without endpoints as well for reference
            print "\n# " worker_type " worker (no API endpoints) ["
            print worker_stanza
            print "# ]"
        }
    }
}

END {
    print "\nmatrix_synapse_workers_avail_list:"
    print workers | "sort"
}

# vim: tabstop=4 shiftwidth=4 expandtab autoindent
