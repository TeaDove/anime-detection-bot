#!/usr/bin/env bash

set -e

CR_ID=$1

./compile_requirements.sh
docker login \
  --username iam \
  --password "$(yc iam create-token)" \
  cr.yandex

docker build . -t "cr.yandex/${CR_ID}/$2"
docker push "cr.yandex/${CR_ID}/$2"
