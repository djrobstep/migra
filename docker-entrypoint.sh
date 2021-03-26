#!/usr/bin/env sh

set -e

if [ "$1" = 'migra' ]; then
	if [ "${MIGRA_LOG_COMMAND}" = 'true' ]; then
		echo "$*"
	fi
fi

exec "$@"
