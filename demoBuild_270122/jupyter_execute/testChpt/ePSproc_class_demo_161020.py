#!/usr/bin/env python
# coding: utf-8

# # ePSproc base and multijob class intro
# 16/10/20
# 
# As of Oct. 2020, v1.3.0-dev, basic data classes are now implemented, and are now the easiest/preferred method for using ePSproc (as opposed to calling core functions directly, as [illustrated in the functions guide](https://epsproc.readthedocs.io/en/latest/demos/ePSproc_demo_Aug2019.html)).
# 
# A brief intro and guide to use is given here.
# 
# 

# Aims:
#     
# - Provide unified data architecture for ePSproc, ePSdata and PEMtk.
# - Wrap plotting and computational functions for ease of use.
# - Handle multiple datasets inc. comparitive plots.

# ## Setup

# In[1]:


# For module testing, include path to module here, otherwise use global installation
local = True

if local:
    import sys
    if sys.platform == "win32":
        modPath = r'D:\code\github\ePSproc'  # Win test machine
        winFlag = True
    else:
        modPath = r'/home/femtolab/github/ePSproc/'  # Linux test machine
        winFlag = False

    sys.path.append(modPath)

# Base
import epsproc as ep

# Class dev code
from epsproc.classes.multiJob import ePSmultiJob
from epsproc.classes.base import ePSbase


# ## ePSbase class
# 
# The ePSbase class wraps most of the core functionality, and will handle all ePolyScat output files in a single data directory. In general, we'll assume:
# 
# - an ePS *job* constitutes a single ionization event/channel (ionizing orbital) for a given molecule, stored in one or more output files.
# - the data dir contains one or more files, where each file will contain a set of symmetries and energies, with either
#    - one file per ionizing event. In this case, each file will equate to one job, and one entry in the class datastructure.
#    - a single ionizing event, where each file contains a different set of energies for the given event (*energy chunked* fileset). In this case, the files will be stacked, and the dir will equate to one job and one entry in the class datastructure.
#    
# The class datastructure is (currently) a set of dictionaries, with entries per job as above, and various data for each job. In general the data is [stored in Xarrays](http://xarray.pydata.org/en/stable/why-xarray.html).
# 
# The `multiJob` class extends the base class with reading from multple directories.
#    
# 

# ### Load data
# 
# Firstly, set the data path, instantiate a class object and load the data.

# In[2]:


# Set for ePSproc test data, available from https://github.com/phockett/ePSproc/tree/master/data
# Here this is assumed to be on the epsproc path
import os
dataPath = os.path.join(sys.path[-1], 'data', 'photoionization', 'n2_multiorb')


# In[3]:


# Instantiate class object.
# Minimally this needs just the dataPath, if verbose = 1 is set then some useful output will also be printed.
data = ePSbase(dataPath, verbose = 1)


# In[4]:


# ScanFiles() - this will look for data files on the path provided, and read from them.
data.scanFiles()


# In this case, two files are read, and each file is a different ePS job - here the $3\sigma_g^{-1}$ and $1\pi_u^{-1}$ channels in N2. The keys for the job are also used as the job names.

# ### Basic info & plots
# 
# A few basic methods to summarise the data...

# In[5]:


# Summarise jobs, this will also be output by scanFile() if verbose = 1 is set, as illustrated above.
data.jobsSummary()


# In[6]:


# Molecular info
# Note that this is currently assumed to be the same for all jobs in the data dir.
data.molSummary()


# ### Plot cross-sections and betas
# 
# These are taken from the `GetCro` segments in the ePS output files, and correspond to results for an isotropic ensemble of molecules, i.e. observables in the lab frame (LF) for 1-photon ionization (see [the ePS tutorial for more details](https://epsproc.readthedocs.io/en/latest/ePS_ePSproc_tutorial/ePS_tutorial_080520.html#Theoretical-background)).

# In[7]:


# Minimal method call will plot cross-sections for all ePS jobs found in the data directory.
data.plotGetCro()


# In[8]:


# Plot beta parameters with the 'BETA' flag
data.plotGetCro(pType = 'BETA')


# TODO: fix labelling here.

# ### Compute MFPADs
# 
# The class currently wraps just the [basic numerical routine for MFPADs](https://epsproc.readthedocs.io/en/latest/demos/ePSproc_demo_Aug2019.html#Calculate-MFPADs). This defaults to computing MFPADs for all energies and $(z,x,y)$ polarization geometries (where the z-axis is the molecular symmetry axis, and corresponds to the molecular structure plot shown above).

# In[9]:


# Compute MFPADs...
data.mfpadNumeric()


# To plot it's advisable to set an enery slice, `Erange = [start, stop, step]`, since MFPADs are currently shown as individual plots in the default case, and there may be a lot of them.
# 
# We'll also just set for a single key here, otherwise all jobs will be plotted.

# In[10]:


data.padPlot(keys = 'orb5', Erange = [5, 10, 4])

#TODO: fix plot layout!


# To view multiple results in a more concise fashion, a Cartesian gridded output is also available.

# In[11]:


data.padPlot(keys = 'orb5', Erange = [5, 10, 4], pStyle='grid')


# In[12]:


# Various other args can be passed...

# Set a plotting backend, currently 'mpl' (Matplotlib - default) or 'pl' (Plotly - interactive, but may give issues in some environments)
backend = 'pl'

# Subselect on dimensions, this is set as a dictionary for Xarray selection (see http://xarray.pydata.org/en/stable/indexing.html#indexing-with-dimension-names)
selDims = {'Labels':'z'}  # Plot z-pol case only.

data.padPlot(Erange = [5, 10, 4], selDims=selDims, backend = backend)


# ### Compute $\beta_{LM}$ parameters
# 
# For computation of $\beta_{LM}$ parameters the class wraps functions from `epsproc.geom`, which implement a tensor method. This is quite fast, although memory heavy, so may not be suitable for very large problems. (See the [method development pages for more info](https://epsproc.readthedocs.io/en/latest/methods/geometric_method_dev_260220_090420_tidy.html), more concise notes to follow).
# 
# - Functions are provided for MF and AF problems (which is the general case, and will equate to the LF case for an unaligned ensemble). 
# - For the MF the class wraps `ep.geom.mfblmXprod`, see the [method development page for more info](https://epsproc.readthedocs.io/en/latest/methods/geometric_method_dev_pt2_170320_v140420.html), more concise notes to follow.
# - For the AF the class wraps `ep.geom.afblmXprod`, see the [method development page for more info](https://epsproc.readthedocs.io/en/latest/methods/geometric_method_dev_pt3_AFBLM_090620_010920_dev_bk100920.html), more concise notes to follow.
# 
# 

# #### Compute MF $\beta_{LM}$ and PADs
# 
# Here's a quick demo for the default MF cases, which will give parameters corresponding to the $(z,x,y)$ polarization geometries computed by the numerical routine above.

# In[13]:


data.MFBLM()


# Plotting still needs to improve... but ep.lmPlot() is a robust way to plot everything.

# In[14]:


# data.BLMplot(dataType = 'MFBLM')  # HORRIBLE OUTPUT at the moment!!!
data.lmPlot(dataType = 'MFBLM')


# Line-plots are available with the `BLMplot` method, although this currently only supports the Matplotlib backend, and may have problems with dims in some cases (work in progress!).

# In[15]:


data.BLMplot(dataType='MFBLM', thres = 1e-2)  # Passing a threshold value here will remove any spurious BLM parameters.


# Polar plots are available for these distributions using the `padPlot()` method if the `dataType` is passed.

# In[16]:


data.padPlot(keys = 'orb5', Erange = [5, 10, 4], dataType='MFBLM')


# #### Compute LF/AF $\beta_{LM}$ and PADs
# 
# Here's a quick demo for the default AF case (isotropic distribution, hence == LF case).

# In[17]:


data.AFBLM()


# Plotting still needs to improve... but ep.lmPlot() is a robust way to plot everything.

# In[18]:


# data.BLMplot(dataType = 'MFBLM')  # HORRIBLE OUTPUT at the moment!!!
data.lmPlot(dataType = 'AFBLM')


# Line-plots are available with the `BLMplot` method, although this currently only supports the Matplotlib backend, and may have problems with dims in some cases (work in progress!).

# In[19]:


data.BLMplot(dataType='AFBLM', thres = 1e-2)  # Passing a threshold value here will remove any spurious BLM parameters.


# Polar plots are available for these distributions using the `padPlot()` method.

# In[20]:


data.padPlot(keys = 'orb5', Erange = [5, 10, 4], dataType='AFBLM')

# NOTE - seem to have an inconsistency with (x,y) pol geometries here - should check source code & fix. Likely due to mix-up in frame defns., i.e. probably mixing LF and MF pol geom defn. - TBC.


# ## Additions

# ### Plot styles for line-plots
# 
# To set to Seaborn plotting style, use `ep.hvPlotters.setPlotters()` (note this will be set for all plots after loading, unless overriden). Seaborn must be installed for this to function.
# 
# For more on Seaborn styles, see [the Seaborn docs](https://seaborn.pydata.org/tutorial/aesthetics.html).

# In[21]:


from epsproc.plot import hvPlotters
hvPlotters.setPlotters()

data.plotGetCro()


# ### Matrix element plotting
# 
# For a full view of the computational results, use the `lmPlot()` method with the default, which correspond to `dataType=matE`.

# In[22]:


data.lmPlot()


# The default here plots abs values, but the same routine can be set for phase plotting.

# In[23]:


data.lmPlot(pType='phase')


# ## Versions

# In[24]:


import scooby
scooby.Report(additional=['epsproc', 'xarray', 'jupyter'])

