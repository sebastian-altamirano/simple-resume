#!/bin/bash

# Script to run `frontman` in a separate virtual environment to avoid conflicts with the project's
# dependencies.

set -e

activate_venv() {
  venv_path="$1"
  if [ -d "$venv_path/bin" ]; then
    source "$venv_path/bin/activate"  # Linux and macOS
  else
    source "$venv_path/Scripts/activate"  # Windows
  fi
}

scripts_path=$(dirname $0)
frontman_venv_path="$scripts_path/../.venv_frontman"

if [ ! -d "$frontman_venv_path" ]; then
	python -m venv $frontman_venv_path
	activate_venv "$frontman_venv_path"
	pip install frontman
else
	activate_venv "$frontman_venv_path"
fi

python -m frontman "$@"
