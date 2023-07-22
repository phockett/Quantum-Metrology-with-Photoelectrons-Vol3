---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.5
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

+++ {"tags": ["remove-cell"]}

**Initial OCS tests**

26/05/23, v1

- For OCS match expt. case, see https://phockett.github.io/ePSdata/OCS-preliminary/OCS_orbs8-11_AFBLMs_VM-ADMs_140122-JAKE_tidy-replot-200722_v5.html
- Downloader now in place.
- Keep everything in notebook for now (see template http://jake:9966/lab/tree/QM3/doc-source/part2/basic_fitting_numerics_intro_260423.ipynb), but should move file IO to OCS-specific script (don't need to show all of this). Some of this is already in main setup fitting demo script, but still have rather specific ADM settings.
- For ADMs and matE working from raw forms currently, may want to consolidate and tidy up for fitting-only case.
- Data gen should be optional.


WHAT THE FUCK IS GOING ON WITH THE DATA IO....

- For multiple files in same dir seems OK, but isn't.\
- For subdirs
   - Fails to scan them?  Only for ePSmultiJob class?
   - Mislabels orbs? WHERE IS THIS NUMBER COMING FROM?????? Modified recently, but not like this...

```
dataPath = fAllMatE['fListDownloaded'][0].parent
dataPath = Path('/home/jovyan/QM3/doc-source/part2/OCSfitting/')  # NOT WORKING AFTER FILE REORG....?????
dataPath = Path('/home/jovyan/QM3/doc-source/part2/OCSfitting/orb11')  # OK AFTER FILE REORG
# WHY IS THIS NOW LABELLED AS ORB14????????????????????????????????
```


TODO:

- Issues with selOpts consistency and settings, esp. for 'it' selection.
    - Working if NO IT selection made in selOpts.
    - IF single IT selected, IT is squeezed, setMatEFit() fails unless colDim is set (for display routine only?)
    - IF single IT selected, and IT dim readded manually, `data.afblmMatEfit()` fails unless run with `selDims={'it': 2}` added!
    - SHOULD BE ABLE to pass no squeeze to selOpts? Also pass to fit correctly! Maybe not fully wrapped as yet...

+++

(chpt:ocs-case-study)=
# Case study: Generalised bootstrapping for a linear heteronuclear scattering system, $OCS~(C_{\infty v})$

```{code-cell} ipython3

```

## Init and pulling data

Here the setup is mainly handled by some basic scripts, these follow the outline in the {{ PEMtk_docs }}, see in particular [the intro to fitting](https://pemtk.readthedocs.io/en/latest/fitting/PEMtk_fitting_basic_demo_030621-full_010922.html).

```{code-cell} ipython3
:tags: [hide-cell]

# Run default config - may need to set full path here
%run '../scripts/setup_notebook.py'

# Override plotters backend?
# plotBackend = 'pl'
```

```{code-cell} ipython3
# Pull data files as required from Github, note the path here is required

# from epsproc.util.io import getFilesFromGithub

# fDict, fAll = getFilesFromGithub(subpath='data/alignment/OCS_ADMs_28K_VM_070722', ref='dev')   # OK

# 26/05/23 - Monkeypatch version for debug
# Above should be fine after source updates
import requests
from epsproc.util import io
io.requests = requests 

dataName = 'OCSfitting'

fDictMatE, fAllMatE = io.getFilesFromGithub(subpath='data/photoionization/OCS_multiorb', dataName=dataName, ref='dev')  #, download=False)   # N2 matrix elements
fDictADM, fAllADM = io.getFilesFromGithub(subpath='data/alignment/OCS_ADMs_28K_VM_070722', dataName=dataName, ref='dev')  #, download=False)   # N2 alignment data
# Note this is missing script - should consolidate all to book repo?
# Note ref='dev' for OCS currently (dev branch

# Alternatively supply URLs directly for file downloader
# Pull N2 data from ePSproc Github repo
# URLs for test ePSproc datasets - n2
# For more datasets use ePSdata, see https://epsproc.readthedocs.io/en/dev/demos/ePSdata_download_demo_300720.html
# urls = {'n2PU':"https://github.com/phockett/ePSproc/blob/master/data/photoionization/n2_multiorb/n2_1pu_0.1-50.1eV_A2.inp.out",
#         'n2SU':"https://github.com/phockett/ePSproc/blob/master/data/photoionization/n2_multiorb/n2_3sg_0.1-50.1eV_A2.inp.out",
#         'n2ADMs':"https://github.com/phockett/ePSproc/blob/master/data/alignment/N2_ADM_VM_290816.mat",
#         'demoScript':"https://github.com/phockett/PEMtk/blob/master/demos/fitting/setup_fit_demo.py"}

# fList, fDict = io.getFilesFromURLs(urls, dataName=dataName)
```

### Load matrix elements

TODO: keys and jobNotes are currently set to be the same for all files in dir, although they are correctly read.
Should fix file IO or reorg files.

UPDATE: testing manual file reorg, OTHERWISE ALL FILES CONCATENATED IT SEEMS? ALTHOUGH NOT SHOWN IN FILELIST, but seeing duplicate Ekes and symmetries!!!!

```{code-cell} ipython3
# dataPath = fAllMatE['fListDownloaded'][0].parent
# dataPath = Path('/home/jovyan/QM3/doc-source/part2/OCSfitting/')  # NOT WORKING AFTER FILE REORG....?????
dataPath = Path('/home/jovyan/QM3/doc-source/part2/OCSfitting/orb11')  # OK AFTER FILE REORG
# WHY IS THIS NOW LABELLED AS ORB14????????????????????????????????

# Init class object
data = pemtkFit(fileBase = dataPath, verbose = 1)

# Read data files
# data.scanFiles(keyType='int')
data.scanFiles()
```

```{code-cell} ipython3
# data.data[0]['XS'].fileList
```

```{code-cell} ipython3
# data.data[1]['XS'].fileList
```

```{code-cell} ipython3
data.molSummary(dataKey='orb14')
```

```{code-cell} ipython3
# key='orb14'
# data.data[key]['jobNotes']  #['orbKey']


# FROM OLD PROCESSING - may need some of this again!
# # Fix labels for plots - currently have some mis-named files!

# # Set state labels
# v = ['C','B','A','X']
# sDict = {n:v[k] for k,n in enumerate(range(9,13))}

# for key in data.data.keys():
#     data.data[key]['jobNotes']['orbKey'] = key  # Existing orb key, from filename
#     data.data[key]['jobNotes']['orbGroup'] = int(key.strip('orb')) + 1   # Corrected orb group
# #     data.data[key]['jobNotes']['orbLabel'] = f"HOMO - {12 - int(key.strip('orb')) - 1}"
#     data.data[key]['jobNotes']['orbLabel'] = sDict[data.data[key]['jobNotes']['orbGroup']]
```

### Load alignment data

Here settings for OCS ADMs in raw format and conversion to expected type and normalisation.

```{code-cell} ipython3
# Load test ADMs from .mat files.
# Code adapted from N2 case, https://epsproc.readthedocs.io/en/latest/methods/geometric_method_dev_pt3_AFBLM_090620_010920_dev_bk100920.html#Test-compared-to-experimental-N2-AF-results...
#
# To check individual file contents just use `loadmat(file)`
# 

ADMtype = 'dat'
ADMscaleFactor = 1  # Try quick SF to circumvent thresholding issues in current code - should be renormed out in final Blms
                     # Tested for 100 - still some weird stuff happening, although very different weird stuff!
                     # 10 maybe a bit better? Or 2...?
                     # May also be issue with complex form for ADMs...? Testing setting real part only later

renorm = False  # Apply additional renorm factors?

from scipy.io import loadmat

# if ADMtype == 'mat':

#     # Original ADMs 14/01/22 - matlab files
#     ADMdataDir = Path('~/ePS/OCS/OCS_alignment_ADMs_VM_140122')
#     renorm = True  # Additional renormalisation by (2*K+1)/8*pi^2
    
# else:
#     # Updated ADMs from dat files
#     # Note these are also Matlab hdf5, but different var labels.
#     ADMdataDir = Path('~/ePS/OCS/OCS_ADMs_28K_VM_070722')
#     renorm = False  # Additional renormalisation by (2*K+1)/8*pi^2
    
# fList = ep.getFiles(fileBase =  ADMdataDir.expanduser(), fType='.'+ADMtype)

# From downloader
fList = fAllADM['fListDownloaded']


ADMs = []
ADMLabels = []

for f in fList:
    
    if ADMtype == 'mat':
        item = Path(f).name.rstrip('ocs.mat')  # Get & set variable name

    else:
        item = Path(f).name.split('_')[0]  # Get & set variable name
    
        
    if item == 'time':
        if ADMtype == 'mat':
            item = 'timeocs'
            
        t = loadmat(f)[item][0,:]
        
    elif item == 'c2t':
        c2t = loadmat(f)[item][:,0]
        
    else:
        # Should use re herer!
        if ADMtype == 'mat':
            K = int(item.strip('D'))
            item = item + 'ave'
        else:
#             try:
            K = int(item.strip('A')[0])
#             except:
#                 pass   # For now just skip cos^2 t term
            

#         ADMs.append(np.asarray([K,0,0,loadmat(f)[item][:,0]]))
#         ADMs.append([K,0,0,loadmat(f)[item][:,0]])
#         ADMs.append(loadmat(f)[item][:,0])
        ADMs.append(loadmat(f)[item][:,0]*ADMscaleFactor)
        ADMLabels.append([K,0,0])
        
            
            
# Add K = 0 (population) term?
# NOTE - may need additional renorm?
addPop = True
if addPop:
    if renorm:
        # ADMs.append(np.ones(t.size) * np.sqrt(4*np.pi))
        # ADMs.append(np.ones(t.size) / np.sqrt(4*np.pi))
        ADMs.append(np.ones(t.size) / (4*np.pi))
    
    else:
#         ADMs.append(np.ones(t.size))  # * np.sqrt(4*np.pi))  1/(4*pi)
        ADMs.append(np.ones(t.size) * 1/(8*np.pi**2))
        
    ADMLabels.append([0,0,0])
        
ADMLabels = np.array(ADMLabels)
```

```{code-cell} ipython3
# data.setADMs(ADMs = ADMs['ADM'], t=ADMs['time'].squeeze(), KQSLabels = ADMs['ADMlist'], addS = True)

data.setADMs(ADMs = ADMs, KQSLabels = ADMLabels, t=t)

if renorm:
    # ADMs = ADMs * (2*ADMs.K+1)/(8*np.pi**2)  # Additional renormalisation by (2*K+1)/8*pi^2
    data.data['ADM']['ADM'] = data.data['ADM']['ADM'] * 1/(4*np.pi)  # Norm from expt. case.
```

```{code-cell} ipython3
%matplotlib inline
# data.ADMplot()  # FAILS
data.ADMplot(keys = 'ADM')  # OK
# data.ADMplot(keys = 'ADM', dataType='ADM', backend='hv')  # FAILS, issue with assumed dims?
# data.BLMplot(dataType = dataType, xDim = xDim, Etype = Etype, col = col, **kwargs)
```

```{code-cell} ipython3
# HVplot example
data.data['ADM']['ADM'].unstack().squeeze().real.hvplot.line(x='t').overlay('K')
```

```{code-cell} ipython3
key = 'ADM'
dataType='ADM'
data.data[key][dataType].unstack().real.hvplot.line(x='t').overlay(['K','Q','S'])
```

```{code-cell} ipython3

```

### Polarisation geometry/ies

This wraps [ep.setPolGeoms](https://epsproc.readthedocs.io/en/dev/modules/epsproc.sphCalc.html#epsproc.sphCalc.setPolGeoms). This defaults to (x,y,z) polarization geometries. Values are set in `self.data['pol']`.

Note: if this is not set, the default value will be used, which is likely not very useful for the fit!

```{code-cell} ipython3
data.setPolGeoms()
data.data['pol']['pol']
```

### Subselect data

Currently handled in the class by setting `self.selOpts`, this allows for simple reuse of settings as required. Subselected data is set to `self.data['subset'][dataType]`, and is the data the fitting routine will use.

TODO: fix issues with squeeze here... adding 'it' selector to matE selOpts currently causes issues for fitting - should be able to pass 'sq':False and/or do better dim handling here?

```{code-cell} ipython3
# Settings for type subselection are in selOpts[dataType]

# E.g. Matrix element sub-selection
data.selOpts['matE'] = {'thres': 0.01, 'inds': {'Type':'L', 'Eke':10.1, 'it':2}, 'sq':False}
data.setSubset(dataKey = 'orb14', dataType = 'matE')  # Subselect from '1' dataset, matrix elements for HOMO

# Show subselected data
# data.data['subset']['matE']

# Tabulate the matrix elements
# Not showing as nice table for singleton case - pd.series vs. dataframe?
# data.matEtoPD(keys = 'subset', xDim = 'Sym', drop=False)

# And for the polarisation geometries...
data.selOpts['pol'] = {'inds': {'Labels': 'z'}}
data.setSubset(dataKey = 'pol', dataType = 'pol')

# And for the ADMs...
# SLICE version - was working, but not working July 2022, not sure if it's data types or Xarray version issue? Just get KeyErrors on slice.
# data.selOpts['ADM'] = {}   #{'thres': 0.01, 'inds': {'Type':'L', 'Eke':1.1}}
# data.setSubset(dataKey = 'ADM', dataType = 'ADM', sliceParams = {'t':[38, 44, 4]}) 

#********** HACKS/DEBUG
# Inds/mask version - seems more robust?
trange=[38, 44]  # Set range in ps for calc
tStep=4  # Set tStep for downsampling
tMask = (data.data['ADM']['ADM'].t>trange[0]) & (data.data['ADM']['ADM'].t<trange[1])
data.data[data.subKey]['ADM'] = data.data['ADM']['ADM'][:,tMask][:,::tStep]  # Set and update
print(f"ADMs: Selecting {data.data['subset']['ADM'].t.size} points from {data.data['ADM']['ADM'].t.size}")

# Fix issues with squeezed 'it' coord in single selection case
data.data[data.subKey]['matE'] = data.data[data.subKey]['matE'].expand_dims(dim='it')
```

```{code-cell} ipython3
data.data['subset']['matE']
```

## Compute AF-$\beta_{LM}$ and simulate data

With all the components set, some observables can be calculated. For testing, we'll also use this to simulate an experiemental trace...

Here we'll use `self.afblmMatEfit()`, which is also the main fitting routine, and essentially wraps `epsproc.afblmXprod()` to compute AF-$\beta_{LM}$s (for more details, see the [ePSproc method development docs](https://epsproc.readthedocs.io/en/dev/methods/geometric_method_dev_pt3_AFBLM_090620_010920_dev_bk100920.html)).

If called without reference data, the method returns computed AF-$\beta_{LM}$s based on the input subsets already created, and also a set of (product) basis functions generated - these can be examined to get a feel for the sensitivity of the geometric part of the problem, and will also be used in fitting to limit repetitive computation.

+++

### Compute AF-$\beta_{LM}$s

```{code-cell} ipython3
# Compute using class structure
# Q: does this use selOpts from above...?
# Q: Need to pass ADMs here too? Otherwise just get single t
# data.AFBLM(keys = keys, AKQS = ADMs, selDims = {'Type':'L'}, thres=None)

# data.AFBLM(keys = 'subset', thres=None, selDims = {'Type':'L'}, sq=False)   #, Etype='t', thresDims='t', selDims = {'Type':'L'})
```

```{code-cell} ipython3
# data.data['subset']['AFBLM']
```

```{code-cell} ipython3
# data.BLMplot(keys='subset',  Etype='t', col=None, thres=1e-4)
```

```{code-cell} ipython3
# Compute using fit wrapper - this should be simpler, but may need additional renorm?

# data.afblmMatEfit(data = None)  # OK
# BetaNormX, basis = data.afblmMatEfit()  # OK, uses default polarizations & ADMs as set in data['subset']
BetaNormX, basis = data.afblmMatEfit(selDims={'it': 2})   # Also need this with selOpts set, but dim readded, TO FIX!
# BetaNormX, basis = data.afblmMatEfit(ADM = data.data['subset']['ADM'])  # OK, but currently using default polarizations
# BetaNormX, basis = data.afblmMatEfit(ADM = data.data['subset']['ADM'], pol = data.data['pol']['pol'].sel(Labels=['x']))
# BetaNormX, basis = data.afblmMatEfit(ADM = data.data['subset']['ADM'], pol = data.data['pol']['pol'].sel(Labels=['x','y']))  # This fails for a single label...?
# BetaNormX, basis = data.afblmMatEfit(RX=data.data['pol']['pol'])  # This currently fails, need to check for consistency in ep.sphCalc.WDcalc()
                                                                    # - looks like set values and inputs are not consistent in this case? Not passing angs correctly, or overriding?
                                                                    # - See also recently-added sfError flag, which may cause additional problems.
```

### AF-$\beta_{LM}$s

+++

The returned objects contain the $\beta_{LM}$ parameters as an Xarray...

TODO: FIX IT - needs thresholding?

- YEP: OK with BLMplot with some non-default settings - should add these as defaults too depending on dims.
- BUT only showing unnorm Betas...?  Why? Option set for fitting case?
   - See updates below - issue is renorm by matrix elements to theoretical XS in afblm routine, which is incorrect if ADMs unnormed.
   - 30/05/23 Now added below (and updated renormL0 routine), may want to look more closely at ADMs too?
- Also need to set it=2 for calc, otherwise get -ve XS (although just phase issue).

```{code-cell} ipython3
# Line-plot with Xarray/Matplotlib
# Note there is no filtering here, so this includes some invalid and null terms
# BetaNormX.sel(Labels='A').real.squeeze().plot.line(x='t');
```

```{code-cell} ipython3
# Set data for simulation
data.setData('sim', BetaNormX)  # Set simulated data to master structure as "sim"
data.setSubset('sim','AFBLM')   # Set to 'subset' to use for fitting.

# Set basis functions
data.basis = basis
```

```{code-cell} ipython3
data.BLMplot(keys='sim', Etype='t', col=None, thres=1e-4)
```

```{code-cell} ipython3
data.BLMplot(keys='sim', Etype='t', col=None, thres=1e-4, backend='hv')
```

```{code-cell} ipython3
# Not plotting..? Missing config?
data.plots['BLMplot']['hv']
```

```{code-cell} ipython3
# # ep.plot.hvPlotters.setPlotters()
# ep.plot.hvPlotters.setPlotters(width=imgWidth, height=imgHeight)  # OK after rerunning setplotters...?
# import hvplot.xarray
# data.plots['BLMplot']['hv'].overlay(['l','m'])
```

```{code-cell} ipython3
# Add XS to rescale?
data.BLMplot(keys='sim', Etype='t', col=None, thres=1e-4, backend='hv', XS=True)
```

```{code-cell} ipython3
# BetaNormX.sel({'l':0}).sel({'m':0}).drop_vars('m').squeeze()   #, drop=True)  #.drop_vars('m')  #.squeeze()
# BetaNormX.sel({'l':0}).sel({'m':0}).drop('m')
```

```{code-cell} ipython3
# # Renormalise to B00? This is currently required for corrected beta parameters since only matrix elements are used in the default case

# # from epsproc.util.conversion import renormL0
# # # renormL0(BetaNormX)  # Currently fails, due to inplace opearation?

# BetaNormXRN = BetaNormX/BetaNormX.sel({'l':0}).sel({'m':0}).drop('m')

# # Set data for simulation
# data.setData('sim', BetaNormXRN)  # Set simulated data to master structure as "sim"
# data.setSubset('sim','AFBLM')   # Set to 'subset' to use for fitting.

# # data.BLMplot(keys='sim', Etype='t', col=None, thres=1e-4, backend='hv')

# data.BLMplot(keys='sim', Etype='t', col=None, thres=1e-4, backend='hv')
```

```{code-cell} ipython3

```

```{code-cell} ipython3
:tags: [remove-cell]

# 30/05/23 - source now fixed, should work on next build
# from epsproc.util.conversion import renormL0

# # renormL0(BetaNormX)  # Currently fails, due to inplace opearation?
# dataOut = BetaNormX.copy()
# # dataOut /= dataOut.sel({'L':0}).drop('M').squeeze()
# # dataOut = dataOut/dataOut.sel({'L':0}).drop('M').squeeze()
# # hasattr(dataOut,'l')
# dataOut = dataOut/dataOut.sel({'l':0}).drop('m').squeeze()  # OK!
# dataOut
```

## Setup fit...

```{code-cell} ipython3
data.subKey
```

```{code-cell} ipython3
# data.data[data.subKey]['matE']
```

```{code-cell} ipython3
# Init fitting from 
data.setMatEFit()  # Default case, note this expects 'it' to be present.
# data.setMatEFit(colDim='mu')
```

## Test fit for perfect case...

Expect to see symmetry limitations here...

```{code-cell} ipython3

```

```{code-cell} ipython3
# data.randomizeParams()  # Randomize input parameters if desired
                          # For method testing using known initial params is also useful
data.fit()
```

```{code-cell} ipython3
:tags: [hide-output]

# Check fit outputs - self.result shows results from the last fit
data.result
```

```{code-cell} ipython3
data.BLMfitPlot()
```

## Multiple fits...

1. Randomise params, but no noise added.
    - Analysis http://jake:9966/lab/tree/QM3/doc-source/part2/case-study-OCS_dataProc_090623.ipynb
    - Get many perfect results (chi^2 < 1e-22), and look perfect on BLM(t) plots too.
    - Need to add filtering by "vary=True/False" for large datasets, have many redundant params here! Currently uses `data.data['fits']['dfWide']` for analysis, which drops this info.
2. Add noise...
    - Used routine from http://jake/jupyter/user/paul/doc/tree/projects-share/manuscripts/MFrecon_review_2022/notebook_redux_090323/fitting_data_130621/PEMtk_fitting_demo_multi-fit_tests_130621-MFtests_120822-tidy-retest.ipynb, have better version elsewhere...? Stimpy test notebooks...? AH, yes - see `code-share/stimpy-docker-local/pemtk_fitting_runs_April2022/`
    - NEED TO DEPLOY ON FOCK, RAM limited on Jake at the moment.

```{code-cell} ipython3
# L-noise
# Routine from http://jake/jupyter/user/paul/doc/tree/projects-share/manuscripts/MFrecon_review_2022/notebook_redux_090323/fitting_data_130621/PEMtk_fitting_demo_multi-fit_tests_130621-MFtests_120822-tidy-retest.ipynb

# Add noise with np.random.normal
# https://numpy.org/doc/stable/reference/random/generated/numpy.random.normal.html
# data.data['subset']['AFBLM']

# import numpy as np
# mu, sigma = 0, 0.05  # Up to approx 10% noise (+/- 0.05)
# # creating a noise with the same dimension as the dataset (2,2) 
# noise = np.random.normal(mu, sigma, [data.data['subset']['AFBLM'].Labels.size, data.data['subset']['AFBLM'].l.size])
# # data.BLMfitPlot()

# # Set noise in Xarray & scale by l
# import xarray as xr
# noiseXR = xr.ones_like(data.data['subset']['AFBLM']) * noise
# # data.data['subset']['AFBLM']['noise'] = ((data.data['subset']['AFBLM'].t, data.data['subset']['AFBLM'].l), noise)
# # xr.where(noiseXR.l>0, noiseXR/noiseXR.l, noiseXR)
# noiseXR = noiseXR.where(noiseXR.l<1, noiseXR/(noiseXR.l))  # Scale by L

# data.data['subset']['AFBLM'] = data.data['subset']['AFBLM'] + noiseXR
# data.data['subset']['AFBLM'] = data.data['subset']['AFBLM'].where(data.data['subset']['AFBLM'].m == 0, 0)
```

```{code-cell} ipython3
# # t-noise
# # Routine from http://jake/jupyter/user/paul/doc/tree/code-share/stimpy-docker-local/pemtk_fitting_runs_April2022/PEMtk_fitting_dev_weights_runs_050522-run6_8-10-5_84_tpoints.ipynb

# # Add noise with np.random.normal
# # https://numpy.org/doc/stable/reference/random/generated/numpy.random.normal.html
# # data.data['subset']['AFBLM']

import numpy as np
mu, sigma = 0, 0.05  # Up to approx 10% noise (+/- 0.05)
# creating a noise with the same dimension as the dataset (2,2) 
noise = np.random.normal(mu, sigma, [data.data['subset']['AFBLM'].t.size, data.data['subset']['AFBLM'].l.size])
# data.BLMfitPlot()

# Set noise in Xarray & scale by l
import xarray as xr
noiseXR = xr.ones_like(data.data['subset']['AFBLM']) * noise * data.data['subset']['AFBLM'].max()  # FOR OCS ADDED * data.data['subset']['AFBLM'].max() to rescale noise, otherwise ~100%!  Issue is renorm (or not) of values with ADMs.
# data.data['subset']['AFBLM']['noise'] = ((data.data['subset']['AFBLM'].t, data.data['subset']['AFBLM'].l), noise)
# xr.where(noiseXR.l>0, noiseXR/noiseXR.l, noiseXR)
noiseXR = noiseXR.where(noiseXR.l<1, noiseXR/(noiseXR.l))  # Scale by L

data.data['subset']['AFBLM'] = data.data['subset']['AFBLM'] + noiseXR
data.data['subset']['AFBLM'] = data.data['subset']['AFBLM'].where(data.data['subset']['AFBLM'].m == 0, 0)

data.BLMfitPlot()
```

```{code-cell} ipython3
data.data['subset']['AFBLM'].max()
```

```{code-cell} ipython3
data.BLMfitPlot(keys=['sim','subset'])
```

```{code-cell} ipython3
data.multiFit(nRange = [0,10], num_workers =10)
```

```{code-cell} ipython3
data.writeFitData(outStem="OCS_10fit_1D-test_withNoise")
```

```{code-cell} ipython3
data.data.keys()
```

```{code-cell} ipython3
# data.multiFit(nRange = [100,500], num_workers =20)
data.multiFit(nRange = [10,500], num_workers =10)
data.writeFitData(outStem="OCS_500fit_1D-test_withNoise")
```

## QUICK LOOK

```{code-cell} ipython3
# Load data if required
dataPath = '~/QM3/doc-source/part2/OCSfitting/test_fits_1D'
dataFile = 'dataDump_1000fitTests_multiFit_noise_051021.pickle'
```

```{code-cell} ipython3
# Run basic stats
# TODO: add more outputs here & tidy up output formatting.
data.analyseFits()
```

```{code-cell} ipython3
# Basic histogram of fit sets
# Note this defaults to Holoviews/Bokeh for plotting, which produces an interactive plot.
# Set backend = 'mpl' if Holoviews is not available.

# 1st go 500 OCS fits this crashed... issue with # of matrix elements?
# data.fitHist()   
```

```{code-cell} ipython3

```
