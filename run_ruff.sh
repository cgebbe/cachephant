#!/usr/bin/env bash

# NOTE: from https://github.com/astral-sh/ruff/discussions/3594

set -euo pipefail

function main() {
    local target="${1:-.}"
    local rule
    for rule in $(ruff check "$target" --statistics | sort --reverse | awk '{print $2}'); do
        echo "$rule"
        ruff check --select "$rule" --exit-zero "$target"
        echo
    done

}

main "$@"