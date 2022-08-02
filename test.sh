#! /bin/bash

set -e

set -x

# Remove old project if exist
rm -rf ./Testing-Project
# Cookiecutter create project
#! Note: Project name can not change, Must modify .drone.yml file if change this
cookiecutter --no-input -f ./ project_name="Testing Project"

# Change to Testing Project
#! Note: This can not change
cd ./Testing-Project

pip install --upgrade pip poetry

poetry export -f requirements.txt --output requirements.txt --without-hashes --dev

pip install --no-cache-dir --upgrade -r requirements.txt

# DB Migration
aerich upgrade
# Create test init data
python ./tests/create_test_init_data.py
# Pytest
pytest