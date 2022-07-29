#!/bin/sh

set -e

# Environment
echo "#######################"
echo "MIGRATION: ${MIGRATION}"
echo "#######################"

if [ "$MIGRATION" = "true" ]; then
   echo "Doing db migration"
fi

echo "Do somehting in the entrypoint"

# Evaluating passed command:
exec "$@"
