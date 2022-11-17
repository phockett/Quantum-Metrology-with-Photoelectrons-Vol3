# Setup notebook for Quantum Metrology Vol. 3

# Based on PEMtk fitting demo script, see https://github.com/phockett/PEMtk/blob/master/demos/fitting/setup_fit_demo.py
# Setup demo fitting data for PEMtk testing
# Follows approx first half of demo notebook https://pemtk.readthedocs.io/en/latest/fitting/PEMtk_fitting_basic_demo_030621-full.html
# Just removed plotting/output functions here for use in further testing.

print('*** Setting up notebook with standard Quantum Metrology Vol. 3 imports...')
print('For more details see https://pemtk.readthedocs.io/en/latest/fitting/PEMtk_fitting_basic_demo_030621-full.html')
print('To use local source code, pass the parent path to this script at run time, e.g. "setup_fit_demo ~/github"')
print('\n\n* Loading packages...')

# Some definitions for local use

#*** Plotly glue wrapper - NOTE THIS FAILS IF RUN LATER IN IMPORT CHAIN, likely to do with Panel config?
# See https://github.com/executablebooks/jupyter-book/issues/1815
# From https://github.com/holoviz/panel/blob/master/panel/pane/plotly.py
from myst_nb import glue
import panel as pn
pn.extension('plotly')

def gluePlotly(name,fig, **kwargs):
    """Wrap Plotly object with Panel and glue()"""
    return glue(name, pn.pane.Plotly(fig, **kwargs), display=False)


# A few standard imports...

# +
import sys
import os
from pathlib import Path
# import numpy as np
# import epsproc as ep
# import xarray as xr

from datetime import datetime as dt
timeString = dt.now()

import numpy as np
import xarray as xr
import pandas as pd

# -

# And local module imports. This should work either for installed versions (e.g. via `pip install`), or for test code via setting the base path below to point at your local copies.

# +
# For module testing, include path to module here, otherwise use global installation
# print(globals())
# NOTE - this currently doesn't pick up preset modPath case in notebook? Not sure why - something incorrect in scoping here.

# With passed arg
args = sys.argv
localFlag = False

if len(args) > 1:
    modPath = Path(args[1])

    # Append to sys path
    sys.path.append((modPath/'ePSproc').as_posix())
    sys.path.append((modPath/'PEMtk').as_posix())

    localFlag = True


try:
    # ePSproc
    import epsproc as ep

    # Import fitting class
    from pemtk.fit.fitClass import pemtkFit

# Default case
# if not 'modPath' in locals():
except ImportError as e:
    if localFlag:
        print(f"\n*** Couldn't import local packages from root {modPath}.")
    else:
        print(f"\n*** Couldn't import packages, are ePSproc and PEMtk installed? For local copies, pass parent path to this script.")


# Set data path
# Note this is set here from ep.__path__, but may not be correct in all cases - depends on where the Github repo is.
# epDemoDataPath = Path(ep.__path__[0]).parent/'data'



# +
# Set HTML output style for Xarray in notebooks (optional), may also depend on version of Jupyter notebook or lab, or Xr
# See http://xarray.pydata.org/en/stable/generated/xarray.set_options.html
# if isnotebook():
# xr.set_options(display_style = 'html')
# -

# Set some plot options
ep.plot.hvPlotters.setPlotters()

# # Some definitions for local use

# #*** Plotly glue wrapper
# # See https://github.com/executablebooks/jupyter-book/issues/1815
# # From https://github.com/holoviz/panel/blob/master/panel/pane/plotly.py
# from myst_nb import glue
# import panel as pn
# pn.extension('plotly')

# def gluePlotly(name,fig, **kwargs):
#     """Wrap Plotly object with Panel and glue()"""
#     return glue(name, pn.pane.Plotly(fig, **kwargs), display=False)

# Quick display for versions info - may want to push to a dedicated cell in final version
import scooby
scooby.Report(additional=['xarray','plotly','holoviews','pandas','epsproc','pemtk',])

os.system("jupyter-book --version")

# TODO: add GH version info