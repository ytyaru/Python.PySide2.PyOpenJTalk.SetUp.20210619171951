#!/usr/bin/env bash
set -Ceu
#---------------------------------------------------------------------------
# a
# CreatedAt: 2021-06-18
#---------------------------------------------------------------------------
Run() {
	THIS="$(realpath "${BASH_SOURCE:-0}")"; HERE="$(dirname "$THIS")"; PARENT="$(dirname "$HERE")"; THIS_NAME="$(basename "$THIS")"; APP_ROOT="$PARENT";
	cd "$HERE"
#	python3 -m venv env
	. "$HERE/env/bin/activate"
#	pip install remi
#	pip install pysimpleguiweb
#	pip freeze > requirements.txt
#	pip install -r requirements.txt
	python3 run.py
}
Run "$@"
