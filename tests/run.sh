#!/usr/bin/env bash

set -ex

cd $(dirname $0)/..

export GOOGLE_CLOUD_PROJECT=${GOOGLE_CLOUD_PROJECT:-gumo-datastore-test}
export DATASTORE_EMULATOR_HOST=${DATASTORE_EMULATOR_HOST:-127.0.0.1:8082}

pytest -v --junit-xml=test-reports/results.xml tests
