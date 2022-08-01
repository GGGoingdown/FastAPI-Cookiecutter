#!/bin/sh

set -e

echo "Connecting DB"

python ./app/pre_start.py

# Environment
echo "#######################"
echo "MIGRATION: ${MIGRATION}"
echo "#######################"

if [ "$MIGRATION" = "true" ]; then
   echo "Doing db migration"
   aerich upgrade
fi



# Evaluating passed command:
exec "$@"
