#!/bin/bash -eux
function error_exit {
    echo "$1" >&2   ## Send message to stderr. Exclude >&2 if you don't want it that way.
    exit "${2:-1}"  ## Return a code specified by $2 or 1 by default.
}

# this runs on host os e.g MAC/Windows
function local_docker() {
  return
}

# This runs inside a linux docker container
function docker_build() {
    cd all
    virtualenv -p python3.6 reference_models
    source ./reference_models/bin/activate
    pip install -r requirements.txt
    service docker start
    make setup-build-space && make train-pipeline && make create-routes-all && make build-container
    docker tag c12e/model-server c12e/certifai-reference-models
    docker push c12e/certifai-reference-models
}

## MAIN
cd "$(dirname "$0")"
VERSION=$(git describe --long --always --dirty --match='v*.*' | sed 's/v//; s/-/./')
echo "##### BUILDING ${VERSION} ######"

case ${1-local} in
 CI)
  docker_build
  ;;
 *)
  local_docker
  ;;
esac
