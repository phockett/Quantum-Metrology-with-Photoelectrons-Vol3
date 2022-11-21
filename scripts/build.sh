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
export BUILDENV=html
jupyter-book build doc-source/
unset BUILDENV

# Build PDF
# jupyter-book build doc-source/ --builder pdflatex

# As above, but skip errors - NOTE THIS MAY NOT rerun notebooks?
export BUILDENV=pdf  # Not working, see  https://github.com/phockett/Quantum-Metrology-with-Photoelectrons-Vol3/issues/1
# cp doc-source/scripts/setup_notebook_pdf.py doc-source/scripts/setup_notebook.py 
jupyter-book build --keep-going doc-source/ --builder pdflatex
unset BUILDENV
# cp doc-source/scripts/setup_notebook_main.py doc-source/scripts/setup_notebook.py 

# Debug for missing refs. as Warnings - note this should also keep going, but doesn't and may get no PDF
# See https://jupyterbook.org/en/stable/basics/build.html#debug-your-books-build-process
# jupyter-book build -W -n --keep-going doc-source/ --builder pdflatex
