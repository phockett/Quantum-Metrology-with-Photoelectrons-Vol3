#!/bin/bash

# Quick install script for ePSproc and PEMtk from Github, with options
# 04/11/22

# BASEPATH="${1:-~/github}"
#
# cd $BASEPATH
# pip install -e epsproc --user
# pip install -e pemtk --user

# Set options - code from https://www.redhat.com/sysadmin/arguments-options-bash-scripts
# Get the options
OPTIONS=""
BRANCH=""
while getopts ":hb:fnu" option; do
   case $option in
      h) # display Help
         Help
         exit;;
      b) # Add branch
         BRANCH=@$OPTARG;;
      f) # Add --force-reinstall
         OPTIONS+=" --force-reinstall";;
      n) # Add --no-deps
         # echo "Setting --no-deps";;   # OK
         OPTIONS+=" --no-deps";;      # OK in bash, FAILS in SH
         # OPTIONS2=" --no-deps";;        # OK
         # OPTIONS2="${OPTIONS} --no-deps";;  # OK
      u) # Add --user
         OPTIONS+=" --user";;
     \?) # Invalid option
         echo "Error: Invalid option"
         exit;;
   esac
done

# echo $OPTIONS
# echo $BRANCH
# echo pip install $OPTIONS git+https://github.com/phockett/ePSproc$BRANCH
# echo $OPTIONS2

# Basic install
# pip install --no-deps git+https://github.com/phockett/ePSproc@dev
# pip install --no-deps git+https://github.com/phockett/PEMtk
#
# FOR in-container user pkg updates this works:
# pip install --user --force-reinstall --no-deps git+https://github.com/phockett/ePSproc@dev

# Flag version
pip install $OPTIONS git+https://github.com/phockett/ePSproc$BRANCH
pip install $OPTIONS git+https://github.com/phockett/PEMtk
