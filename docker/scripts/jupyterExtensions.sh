#!/bin/sh

# Additional JupterLab extensions.
# See also plotinstall.sh

#*** Spell checker
# https://github.com/jupyterlab-contrib/spellchecker
# pip install jupyterlab-spellchecker
conda install --quiet --yes -c conda-forge jupyterlab-spellchecker

# May need to set too?
# jupyter server extension enable jupyterlab_spellchecker

#*** Panel/Lumen
# Note Lumen/Panel render from Holoviews extension if installed, but likely DON'T want this for general use, see https://discourse.jupyter.org/t/http-500-when-render-with-lumen/13163/3 and https://panel.holoviz.org/
#
# See also https://discourse.holoviz.org/t/what-does-the-render-with-panel-jupyter-lab-button-do/3039 - can use `jupyter serverextension enable panel.io.jupyter_server_extension`
# 
# Disable with `jupyter labextension disable @pyviz/jupyterlab_pyviz`
# But may be required for general HV use?
# jupyter labextension disable @pyviz/jupyterlab_pyviz

#*** Force rebuild
jupyter lab build