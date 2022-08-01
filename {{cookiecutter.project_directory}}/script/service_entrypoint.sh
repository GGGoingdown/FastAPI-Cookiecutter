#!/bin/sh

set -e

echo "Do somehting in the entrypoint"

# Evaluating passed command:
exec "$@"
