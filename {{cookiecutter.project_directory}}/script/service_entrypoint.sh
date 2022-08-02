#!/bin/sh

set -e

echo "#######################"
echo "Connecting DB"
echo "#######################"

python ./pre_start/check_connection.py

# Environment
echo "###########################################################"
echo "MIGRATION: ${MIGRATION}"
echo "CREATE_INIT_DATA: ${CREATE_INIT_DATA}"
echo "APPLICATION_ENVIRONMENT: ${APPLICATION_ENVIRONMENT}"
echo "###########################################################"

if [ "$MIGRATION" = "true" ]; then
   echo "Doing db migration"
   aerich upgrade
fi

if [ "$CREATE_INIT_DATA" = "true" ]; then
   echo "Create initialize data"
   python ./pre_start/create_init_data.py
fi


# Evaluating passed command:
exec "$@"
