#!/bin/sh

# Quick local install for ePSproc and PEMtk
#

BASEPATH="${1:-~/github}"

cd $BASEPATH
pip install -e epsproc --user
pip install -e pemtk --user
