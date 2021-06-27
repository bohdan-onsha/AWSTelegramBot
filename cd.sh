#!/usr/bin/env bash
set -e
source ./venv/bin/activate

DEFAULT_DEPLOY_NAME="aws-telegram-bot"
BUNDLE_NAME=${DEFAULT_DEPLOY_NAME}_$(date +'%d%m%y.%H%M%S')
if [[ -z "$1" ]]
  then
    BUNDLE_NAME=${BUNDLE_NAME}_update
    syndicate build_bundle --bundle_name ${BUNDLE_NAME}
    syndicate update --bundle_name ${BUNDLE_NAME} --deploy_name ${DEFAULT_DEPLOY_NAME}
    exit 0
fi
BUNDLE_NAME=${BUNDLE_NAME}_deploy
syndicate build_bundle --bundle_name ${BUNDLE_NAME}
syndicate deploy --bundle_name ${BUNDLE_NAME} --deploy_name ${DEFAULT_DEPLOY_NAME}
tput bel