#!/usr/bin/env bash

printf "\n> \e[93m\033[1mBuilding Docker image\e[0m\n\n"

set -e

ABSOLUTE_PATH=$(cd `dirname "${BASH_SOURCE[0]}"` && pwd)
cd ${ABSOLUTE_PATH}


BRANCH=${SOURCE_BRANCH:=$(git rev-parse --abbrev-ref HEAD)}
BRANCH=${BRANCH////-} # change `/` in a BRANCH name to be a `-`
BRANCH=${BRANCH//#/-} # change `#` in a BRANCH name to be a `-`

if [ "$BRANCH" == "master" ]; then
    TAG="latest"
else
    TAG="$BRANCH"
fi

DOCKER_IMAGE="djrobstep/migra:${TAG}"

printf "# Image: \e[1;37m${DOCKER_IMAGE}\e[0m\n\n"

docker buildx build --push --platform linux/arm64/v8,linux/amd64 -t ${DOCKER_IMAGE} .
