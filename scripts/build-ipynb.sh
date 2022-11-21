#!/bin/sh

# Quick local build for QM3 book from source
#
# For more options see https://jupyterbook.org/en/stable/basics/build.html
#

# Set default path, or pass at CLI
# BASEPATH="${1:-~/QM3}"
BASEPATH="${1:-/home/jovyan/QM3}"
BUILDSOURCE="_ipynb_build"

cd $BASEPATH

echo Running Jupyter book builds from $BASEPATH - IPYNB ONLY VERSION

echo Copying ipynb source files from doc-source to $BUILDSOURCE
mkdir -p $BUILDSOURCE
# COPY only required files - easy to miss stuff here
# cp doc-source/* --parents $BUILDSOURCE
# cp doc-source/**/*.ipynb --parents $BUILDSOURCE
# COPY full dir, then remove .md
cp doc-source/ -r $BUILDSOURCE
echo Removing .md from subdirs using $BUILDSOURCE/doc-source/**/*.md 
rm $BUILDSOURCE/doc-source/**/*.md

# Clean - should set as option
# jupyter-book clean doc-source/

# *** Build HTML
export BUILDENV=html
jupyter-book build doc-source/
unset BUILDENV

# *** Build PDF
# jupyter-book build doc-source/ --builder pdflatex

# As above, but skip errors
# jupyter-book build --keep-going $BUILDSOURCE/doc-source/ --builder pdflatex

# Debug for missing refs. as Warnings - note this should also keep going, but doesn't and may get no PDF
# See https://jupyterbook.org/en/stable/basics/build.html#debug-your-books-build-process
# jupyter-book build -W -n --keep-going doc-source/ --builder pdflatex
