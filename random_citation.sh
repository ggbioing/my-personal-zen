#!/usr/bin/env bash
cat ./books/*.md | grep "^-" | shuf | head -n1 | sed 's/\. /\.\n/g' | sed 's/, /,\n/g'
