#!/usr/bin/env bash
WD="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cat "${WD}"/books/*.md | grep "^-" | shuf | head -n1 | sed -E 's/([\.,:;])/\1\n/g'
