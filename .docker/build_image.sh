#!/usr/bin/env bash

echo -e "Building gridworld_agent:lastest image"

DOCKER_BUILDKIT=1 \
docker build --pull --rm -f ./.docker/Dockerfile \
--build-arg BUILDKIT_INLINE_CACHE=1 \
--network host \
--tag gridworld_agent:latest .