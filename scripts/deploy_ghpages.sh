#!/bin/sh

# Quick deploy from local build for QM3 book from source
# See https://jupyterbook.org/en/stable/publish/gh-pages.html#option-2-automatically-push-your-build-files-with-ghp-import
# For more options see https://jupyterbook.org/en/stable/basics/build.html
#

# Set default path, or pass at CLI
# BASEPATH="${1:-~/QM3}"
BASEPATH="${1:-/home/jovyan/QM3}"

cd $BASEPATH

echo Deploying to GH pages from $BASEPATH
ghp-import -n -p -f ../doc-source/_build/html