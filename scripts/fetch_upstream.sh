#!/bin/sh
# Fetch pinned upstream repos into .upstream/<KEY>. See PLAN.md 1.1.
set -eu

cd "$(dirname "$0")/.."

pins() {
    cat <<'PINS'
SP https://github.com/obra/superpowers v7.0.1 2ce8aa15d05bd57213e6f746f953aafb7ded7a8b
MP https://github.com/mattpocock/skills v1.3.2 d1478fcb140db0b93c0c8df17bcfd311844749d0
KA https://github.com/multica-ai/andrej-karpathy-skills - 2c606141936f1eeef17fa3043a72095b4765b9c2
AA https://github.com/msitarzewski/agency-agents - b37b5bb33b78f2c1d6567d98e25ca818e3259219
GS https://github.com/garrytan/gstack v1.91.318.0 1bd2330350a6aa978f5c91de3c0be97004d0617b
DBT https://github.com/dbt-labs/dbt-agent-skills - b8facde20b7a92c40ce3e6b86b71c4b92aa44040
GCP https://github.com/google/skills - 92776fbf3875a5ee7424124e398956a998483056
TF https://github.com/hashicorp/agent-skills - bc6b14b77481c3cbfbb06a0166be7245ed45798c
PINS
}

outdated() {
    pins | while read -r key url ref sha; do
        tag=$(git ls-remote --tags --refs --sort=-v:refname "$url" |
            head -n 1 | sed 's|.*refs/tags/||')
        head_sha=$(git ls-remote "$url" HEAD | cut -f1)
        [ -n "$tag" ] || tag=none
        if [ "$ref" = "-" ]; then shown=$(echo "$sha" | cut -c1-7)
        else shown=$ref; fi
        state=BEHIND
        if [ "$ref" = "$tag" ] || [ "$sha" = "$head_sha" ]; then
            state=UP-TO-DATE
        fi
        echo "$key pinned $shown newest-tag $tag head" \
            "$(echo "$head_sha" | cut -c1-7) $state"
    done
}

fetch() {
    mkdir -p .upstream
    pins | while read -r key url ref sha; do
        dir=.upstream/$key
        have=$(git -C "$dir" rev-parse HEAD 2>/dev/null || true)
        if [ "$have" != "$sha" ]; then
            rm -rf "$dir"
            mkdir -p "$dir"
            git -C "$dir" init -q
            git -C "$dir" remote add origin "$url"
            if [ "$ref" = "-" ]; then
                git -C "$dir" fetch -q --depth 1 origin "$sha"
            else
                git -C "$dir" fetch -q --depth 1 origin tag "$ref"
            fi
            git -C "$dir" checkout -q --detach FETCH_HEAD
            got=$(git -C "$dir" rev-parse HEAD)
            if [ "$got" != "$sha" ]; then
                echo "$key tag moved: $ref"
                exit 1
            fi
        fi
        echo "$key $ref $sha"
    done
}

if [ "${1:-}" = "--outdated" ]; then outdated; else fetch; fi
