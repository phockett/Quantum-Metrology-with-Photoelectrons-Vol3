#!/bin/sh

# Quick local build for QM3 book from source
#
# For more options see https://jupyterbook.org/en/stable/basics/build.html
#

# Set default path, or pass at CLI
# BASEPATH="${1:-~/QM3}"
BASEPATH="${1:-/home/jovyan/QM3}"

cd $BASEPATH

echo Running Jupyter book builds from $BASEPATH

# Clean - should set as option
# jupyter-book clean doc-source/

# Build HTML
jupyter-book build doc-source/

# Build PDF
# jupyter-book build doc-source/ --builder pdflatex

# As above, but skip errors
jupyter-book build --keep-going doc-source/ --builder pdflatex

# Debug for missing refs. as Warnings - note this should also keep going, but doesn't and may get no PDF
# See https://jupyterbook.org/en/stable/basics/build.html#debug-your-books-build-process
# jupyter-book build -W -n --keep-going doc-source/ --builder pdflatex
