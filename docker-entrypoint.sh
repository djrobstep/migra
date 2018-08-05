#!/usr/bin/env bash

set -e

if [ "$1" = 'migra' ]; then
	migra_command="$@"
	echo "${migra_command}"
fi

exec "$@"
