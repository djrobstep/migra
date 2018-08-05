#!/usr/bin/env bash

set -e

if [ "$1" = 'migra' ]; then
	if [ "${MIGRA_LOG_COMMAND}" = 'true' ]; then
		migra_command="$@"
		echo "${migra_command}"
	fi
fi

exec "$@"
