#!/bin/sh

# Script to run `frontman` in a separate virtual environment to avoid conflicts with the project's
# dependencies.

scripts_path=$(dirname $0)
frontman_venv_path="$scripts_path/../.venv_frontman"

if [ ! -d $frontman_venv_path ]; then
	python3.12 -m venv $frontman_venv_path
	. "$frontman_venv_path/bin/activate"
	pip install frontman
else
	. "$frontman_venv_path/bin/activate"
fi

python -m frontman "$@"
