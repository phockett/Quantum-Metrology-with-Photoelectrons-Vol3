#!/bin/sh

# Quick local build for QM3 book from source
#
# 23/11/22: #Version for full rebuild, HTML & PDF, to clean dir tree.
#
# For more options see https://jupyterbook.org/en/stable/basics/build.html
#
# TODO: may want to add ghpages push here (for git config see https://gist.github.com/qin-yu/bc26a2d280ee2e93b2d7860a1bfbd0c5)
# OR: set Git for output upload only & GH actions for deploy - probably cleaner. ("_latest_build" in .gitignore for now)
#

# Set default path, or pass at CLI
# BASEPATH="${1:-~/QM3}"
BASEPATH="${1:-/home/jovyan/QM3}"
BUILDSOURCE="_latest_build"
SOURCE="doc-source"

cd $BASEPATH

echo "Running FULL Jupyter book builds from $BASEPATH - Clean builds and copy version"

# *** Build HTML
export BUILDENV=html
BUILDDIR=$BUILDSOURCE
REFDIR=$BUILDSOURCE/$BUILDENV

echo "*** Copying source files from doc-source to $BUILDDIR"
if [ -d "$BUILDDIR" ]; then rm -Rf $BUILDDIR; fi
mkdir -p $BUILDDIR
# COPY only required files - easy to miss stuff here
# cp doc-source/* --parents $BUILDSOURCE
# cp doc-source/**/*.ipynb --parents $BUILDSOURCE
# COPY full dir, then remove .md
cp $SOURCE/ -r $BUILDDIR
# echo Removing .md from subdirs using $BUILDSOURCE/doc-source/**/*.md 
# rm $BUILDSOURCE/doc-source/**/*.md

# Clean - should set as option
echo "*** Cleaning $BUILDDIR"
jupyter-book clean $BUILDDIR/$SOURCE/

echo "*** Building $BUILDENV"
jupyter-book build $BUILDDIR/$SOURCE/

echo "*** Copying $BUILDDIR/$SOURCE/_build/$BUILDENV to $REFDIR"
mkdir -p $REFDIR
cp $BUILDDIR/$SOURCE/_build/$BUILDENV/* -r $REFDIR

unset BUILDENV

# *** Build PDF

# *** Build HTML
export BUILDENV=pdf
BUILDDIR=$BUILDSOURCE
REFDIRHTML=$REFDIR
REFDIR=$BUILDSOURCE/$BUILDENV

# Clean - should set as option
echo "*** Cleaning $BUILDDIR"
jupyter-book clean $BUILDDIR/$SOURCE/

echo "*** Building $BUILDENV"
# jupyter-book build $BUILDDIR/$SOURCE/

# PDF build and skip errors - run x3 to ensure refs etc.
jupyter-book build --keep-going $BUILDDIR/$SOURCE/ --builder pdflatex
jupyter-book build --keep-going $BUILDDIR/$SOURCE/ --builder pdflatex
jupyter-book build --keep-going $BUILDDIR/$SOURCE/ --builder pdflatex

# Debug for missing refs. as Warnings - note this should also keep going, but doesn't and may get no PDF
# See https://jupyterbook.org/en/stable/basics/build.html#debug-your-books-build-process
# jupyter-book build -W -n --keep-going doc-source/ --builder pdflatex

echo "*** Copying $BUILDDIR/$SOURCE/_build/latex to $REFDIR"
mkdir -p $REFDIR
cp $BUILDDIR/$SOURCE/_build/latex/* -r $REFDIR

echo "*** Copying $BUILDDIR/$SOURCE/_build/latex/*.pdf to $REFDIRHTML/pdf"
mkdir -p $REFDIRHTML/pdf
cp $BUILDDIR/$SOURCE/_build/latex/QM3.pdf $REFDIRHTML/pdf

unset BUILDENV

echo "TODO: config GH actions for deploy from this dir."
echo "   To deploy manually, run './scripts/deploy_ghpages-latest.sh .'"
