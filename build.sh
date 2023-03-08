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
function package_build() {
    cd build-package
    virtualenv -p python3.8 reference_models
    source ./reference_models/bin/activate
    make build_package
}

## MAIN
cd "$(dirname "$0")"

case ${1-local} in
 CI)
  package_build
  ;;
 *)
  local_docker
  ;;
esac
