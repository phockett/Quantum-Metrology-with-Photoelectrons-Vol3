---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.7
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

- 27/07/23: v1 from existing demo cases plus new dataset.
- 28/07/23: complete analysis in place up to MF PAD plotting, this needs some additional work (subselection issues). Tested only with minimal N2 dataset so far.
    - UPDATE: Density mat and MF PADs now working.
- 29/07/23: OCS chapter from current N2 draft case, still a bit messy. 
    - Mods to setup cell. Working with OCS script config and dataset 6189229
    - NO MODS, but may want to add same again for 1D case?

+++

(chpt:ocs-case-study)=
# Case study: Generalised bootstrapping for a linear heteronuclear scattering system, $OCS~(C_{\infty v})$

In this chapter, the full code and analysis details of the case study for $OCS$ are given, including obtaining required data, running fits and analysis routines. For more details on the routines, see the {{ PEMtk_docs }}; for the analysis see particularly the [fit fidelity and analysis page](https://pemtk.readthedocs.io/en/latest/fitting/PEMtk_analysis_demo_150621-tidy.html), and [molecular frame analysis data processing page](https://pemtk.readthedocs.io/en/latest/topical_review_case_study/matrix_element_extraction_MFrecon_PEMtk_180722-dist.html) (full analysis for Ref. {cite}`hockett2023TopicalReviewExtracting`, illustrating the $N_2$ case).

+++

## General setup

In the following code cells (see source notebooks for full details) the general setup routines (as per the outline in {numref}`Chpt. %s <sect:basic-fit-setup>` are executed via a configuration script with presets for the case studies herein.

Additionally, the routines will either run fits, or load existing data if available. Since fitting can be computationally demanding, it is, in general, recommended to approach large fitting problems carefully.

+++

````{margin}
```{admonition} General note on fitting

Computational outputs in this chapter are significantly truncated in the PDF, and some simplified plots are used; see source notebooks (via {{ book_repo }}) or {{ book_HTML }} for full details.

```
````

```{code-cell} ipython3
# Configure settings for case study

# Set case study by name
fitSystem='OCS'
fitStem=f"fit_withNoise_orb13"

# Add noise?
addNoise = 'y'
mu, sigma = 0, 0.05  # Up to approx 10% noise (+/- 0.05)

# Batching - number of fits to run between data dumps
batchSize = 10

# Total fits to run
nMax = 10
```

```{code-cell} ipython3
:tags: [hide-output]

# Run default config - may need to set full path here

%run '../scripts/setup_notebook.py'

# Set outputs for notebook or PDF (skips Holoviews plots unless glued)
# Note this is set to default 'pl' in script above
if buildEnv == 'pdf':
    paramPlotBackend = 'sns'    # For category plots with paramPlot
else:
    paramPlotBackend = 'hv'
    
# plotBackend = 'sns'    # For category plots with paramPlot
```

```{code-cell} ipython3
# Pull data from web (OCS case)
from epsproc.util.io import getFilesFromGithub

# Set dataName (will be used as download subdir)
dataName = 'OCSfitting'
# OCS matrix elements
fDictMatE, fAllMatE = getFilesFromGithub(subpath='data/photoionization/OCS_multiorb', dataName=dataName, ref='dev')
# OCS alignment data
fDictADM, fAllADM = getFilesFromGithub(subpath='data/alignment/OCS_ADMs_28K_VM_070722', dataName=dataName, ref='dev')
```

```{code-cell} ipython3
:tags: [hide-output]

# Fitting setup including data generation and parameter creation

# Set datapath, 
dataPath = Path(Path.cwd(),dataName)

# Run general config script with dataPath set above
%run "../scripts/setup_fit_case-studies_270723.py" -d {dataPath} -a {dataPath} -c {fitSystem} -n {addNoise} --sigma {sigma}
```

## Load existing fit data or run fits

Note that running fits may be quite time-consuming and computationally intensive, depending on the size of the size of the problem. The default case here will run a small batch for testing if there is no existing data found on the `dataPath`, otherwise the data is loaded for analysis.

```{code-cell} ipython3
# Look for existing Pickle files on path
dataFiles = list(dataPath.expanduser().glob('*.pickle'))

if not dataFiles:
    print("No data found, executing minimal fitting run...")
    
    # Run fit batch - single
    # data.multiFit(nRange = [n,n+batchSize-1], num_workers=batchSize)

    # Run fit batches with checkpoint files
    for n in np.arange(0,nMax,batchSize):
        print(f'*** Running batch [{n},{n+batchSize-1}], {dt.now().strftime("%d%m%y_%H-%M-%S")}')

        # Run fit batch
        data.multiFit(nRange = [n,n+batchSize-1], num_workers=batchSize)

        # Dump data so far
        data.writeFitData(outStem=f"{fitSystem}_{n+batchSize-1}_{fitStem}")
        
        print(f'Finished batch [{n},{n+batchSize-1}], {dt.now().strftime("%d%m%y_%H-%M-%S")}')
        print(f'Written to file {fitSystem}_{n+batchSize-1}_{fitStem}')

else:
    dataFileIn = dataFiles[-1]   # Add index to select file, although loadFitData will concat multiple files
                                    # Note that concat currently only works for fixed batch sizes however.
    print(f"Set dataFiles: {dataFileIn}")
    data.loadFitData(fList=dataFileIn, dataPath=dataPath)   #.expanduser())
    
    data.BLMfitPlot(keys=['subset','sim'])
    
    # # Check ADMs
    # data.data['subset']['ADM'].unstack().where(data.data['subset']['ADM'].unstack().K>0) \
    #     .real.hvplot.line(x='t').overlay(['K','Q','S'])
    
```

```{code-cell} ipython3
# Check ADMs
data.data['subset']['ADM'].unstack().where(data.data['subset']['ADM'].unstack().K>0) \
    .real.hvplot.line(x='t').overlay(['K','Q','S'])
```

```{code-cell} ipython3
:tags: [hide-output]

# Fits appear as integer indexed items in the main data structure.
data.data.keys()
```

## Post-processing and data overview

Post-processing involves aggregation of all the fit run results into a single data structure. This can then be analysed statistically and examined for for best-fit results. In the statistical sense, this is essentailly a search for candidate {{ RADMATE }}, based on the assumption that some of the minima found in the $chi^2$ hyperspace will be the true results. Even if a clear global minima does not exist, searching for candidate {{ RADMATE }} sets based on clustering of results and multiple local minima is still expected to lead to viable candidates provided that the information content of the dataset is sufficient. However, as discussed elsewhere (see {numref}`Sect. %s <sect:numerics:fitting-strategies>`), in some cases this may not be the case, and other limitations may apply (e.g. certain parameters may be undefined), or additional data required for unique determination of the {{ RADMATE }}.

For more details on the analysis routines, see the {{ PEMtk_docs }}, particularly the [fit fidelity and analysis page](https://pemtk.readthedocs.io/en/latest/fitting/PEMtk_analysis_demo_150621-tidy.html), and [molecular frame analysis data processing page](https://pemtk.readthedocs.io/en/latest/topical_review_case_study/matrix_element_extraction_MFrecon_PEMtk_180722-dist.html) (full analysis for Ref. {cite}`hockett2023TopicalReviewExtracting`, illustrating the $N_2$ case).

```{code-cell} ipython3
# General stats & post-processing to data tables
data.analyseFits()
```

```{code-cell} ipython3
# The BLMsetPlot routine will output aggregate fit results.
# Here the spread can be taken as a general indication of the uncertainty of 
# the fitting, and indicate whether the fit is well-characterised/the information 
# content of the data is sufficient.
data.BLMsetPlot(xDim = 't', thres=1e-6)  # With xDim and thres set, for more control over outputs
```

```{code-cell} ipython3
# Write aggregate datasets to HDF5 format
# This is more robust than Pickled data, but PEMtk currently only support output for aggregate (post-processed) fit data.

data.processedToHDF5(dataPath = dataPath, outStem = dataFileIn.name, timeStamp=False)
```

```{code-cell} ipython3
# Histogram fit results (reduced chi^2 vs. fit index)
# This may be quite slow for large datasets, setting limited ranges may help

# Use default auto binning
# data.fitHist()

# Example with range set
data.fitHist(thres=1.11e-4, bins=100)
```

Here bands in the $\chi^2$ dimension can indicate groupings (local minima) are consistently found. Assuming each grouping is a viable fit candidate parameter set, these can then be explored in further detail.

+++

## Data exploration

The general aim in this procedure is to ascertain whether there was a good spread of parameters explored, and a single (or few sets) of best-fit results. There are a few procedures and helper methods for this...

+++

### View results

Single results sets can be viewed in the main data structure, indexed by #.

```{code-cell} ipython3
# Check keys
fitNumber = 2
data.data[fitNumber].keys()
```

Here `results` is an [lmFit object](https://lmfit.github.io/lmfit-py/intro.html), which includes final fit results and information, and `AFBLM` contains the model (fit) output.

An example is shown below. Of particular note here is which parameters have `vary=True` - these are included in the fitting - and if there is a column `expression`, which indicates any parameters defined to have specific relationships (see {numref}`Chpt. %s <sect:basis-sets:fitting-intro>`). Any correlations found during fitting are also shown, which can also indicate parameters which are related (even if this is not predefined or known a priori).

```{code-cell} ipython3
:tags: [hide-output]

# Show some results
data.data[fitNumber]['results']
```

## Classify candidate sets

To probe the minima found, the `classifyFits` method can be used. This bins results into "candidate" groups, which can then be examined in detail.

```{code-cell} ipython3
# Run with defaults
# data.classifyFits()

# For more control, pass bins
# Here the minima is set at one end, and a %age range used for bins
minVal = data.fitsSummary['Stats']['redchi']['min']    
binRangePC = 1e-5
data.classifyFits(bins = [minVal, minVal + binRangePC*minVal , 20])
```

## Explore candidate result sets

Drill-down on a candidate set of results, and examine values and spreads. For more details see {{ PEMtk_docs }}, especially the [analysis routines page](https://pemtk.readthedocs.io/en/latest/fitting/PEMtk_fitting_multiproc_class_analysis_141121-tidy.html). (See also {numref}`Sect. %s <sect:platform:pythonEcosystem>` for details on the plotting libaries implemented here.)

+++

### Raw results

Plot spreads in magnitude and phase parameters. Statistical plots are available for Seaborn and Holoviews backends, with some slightly different options.

```{code-cell} ipython3
# From the candidates, select a group for analysis
selGroup = 'A'
```

```{code-cell} ipython3
# paramPlot can be used to check the spread on each parameter.
# Plots use Seaborn or Holoviews/Bokeh
# Colour-mapping is controlled by the 'hue' paramter, additionally pass hRound for sig. fig control.
# The remap setting allows for short-hand labels as set in data.lmmu

paramType = 'm' # Set for (m)agnitude or (p)hase parameters
hRound = 14 # Set for cmapping, default may be too small (leads to all grey cmap on points)

data.paramPlot(selectors={'Type':paramType, 'redchiGroup':selGroup}, hue = 'redchi', 
               backend=paramPlotBackend, hvType='violin', 
               returnFlag = True, hRound=hRound, remap = 'lmMap');
```

```{code-cell} ipython3
paramType = 'p' # Set for (m)agnitude or (p)hase parameters
data.paramPlot(selectors={'Type':paramType, 'redchiGroup':selGroup}, hue = 'redchi', backend=paramPlotBackend, hvType='violin', 
               returnFlag = True, hRound=hRound, remap = 'lmMap'); 
```

### Phases, phase shifts & corrections

Depending on how the fit was configured, phases may be defined in different ways. To set the phases relative to a speific parameter, and wrap to a specified range, use the `phaseCorrection()` method. This defaults to using the first parameter as a reference phase, and wraps to $-\pi:\pi$. The phase-corrected values are output to a new Type, 'pc', and a set of normalised magnitudes to 'n'. Additional settings can be passed for more control, as shown below.

```{code-cell} ipython3
:tags: [hide-output]

# Run phase correction routine
# Set absFlag=True for unsigned phases (mapped to 0:pi)
# Set useRef=False to set ref phase as 0, otherwise the reference value is set.
phaseCorrParams={'absFlag':True, 'useRef':False}
data.phaseCorrection(**phaseCorrParams)  
```

Examine new data types...

```{code-cell} ipython3
paramType = 'n'
data.paramPlot(selectors={'Type':paramType, 'redchiGroup':selGroup}, hue = 'redchi', 
               backend=paramPlotBackend, hvType='violin', kind='box',
               returnFlag = True, hRound=hRound, remap = 'lmMap');
```

```{code-cell} ipython3
paramType = 'pc'
data.paramPlot(selectors={'Type':paramType, 'redchiGroup':selGroup}, hue = 'redchi', 
               backend=paramPlotBackend, hvType='violin', kind='box',
               returnFlag = True, hRound=hRound, remap = 'lmMap');
```

## Parameter estimation & fidelity

For case studies, the fit results can be directly compared to the known input parameters. This should give a feel for how well the data defines the matrix elements (parameters) in this case. In general, probing the correlations and spread of results, and comparing to other (unfitted) results is required to estimate fidelity, see {{ QM12 }} for further discussion.

+++

### Best values and statistics

To get a final parameter set and associated statistics, based on a subset of the fit results, the `paramsReport()` method is available. If reference data is available, as for the case studies herein, the `paramsCompare()` method can also be used to compare with the reference case.

```{code-cell} ipython3
:tags: [hide-output]

# Parameter summary
data.paramsReport(inds = {'redchiGroup':selGroup})
```

```{code-cell} ipython3
:tags: [hide-output]

# Parameter comparison
# Note this uses phaseCorrParams as set previously for consistency
data.paramsCompare(phaseCorrParams=phaseCorrParams)
```

```{code-cell} ipython3
# Display above results With column name remapping to (l,m) labels only

# With Pandas functionality
data.paramsSummaryComp.rename(columns=data.lmmu['lmMap'])

# With utility method
# summaryRenamed = pemtk.fit._util.renameParams(data.paramsSummaryComp, data.lmmu['lmMap']) 
# summaryRenamed
```

```{code-cell} ipython3
# Plot values vs. reference cases
# NOTE - experimental code, not yet consolidated and wrapped in PEMtk

paramType = 'm'

# Set new DataFrame including "vary" info (missing in default case)
pDict = 'dfWideTest'
# Try using existing function with extra index set...
data._setWide(indexDims = ['Fit','Type','chisqrGroup','redchiGroup','batch', 'vary'], dataWide='dfWideTest')

# plotData = data.paramPlot(dataDict = pDict, selectors={'vary':True, 'Type':'m', 'redchiGroup':selGroup}, hue = 'chisqr', backend='hv', hvType='violin', returnFlag = True, plotScatter=True, remap = 'lmMap', hRound = 12) 
# NO REMAP CASE
plotData = data.paramPlot(dataDict = pDict, selectors={'vary':True, 'Type':paramType, 'redchiGroup':selGroup}, hue = 'chisqr', 
                          backend='hv', hvType='violin', returnFlag = True, plotScatter=True, hRound=hRound)  #, remap='lmMap') 
p1 = data.data['plots']['paramPlot']
# p2 = dataTestSub.hvplot.scatter(x='Param',y='value', marker='o', size=200, color='green')

# Plot ref params... CURRENTLY NOT IN paraPlot(), and that also expects fit data so can't reuse directly here.

dataTest = data.data['fits']['dfRef'].copy()
# data.paramPlot(dataDict = 'dfRef')

# Set axis remap
# dataTest.replace({'Param':data.lmmu['lmMap']}, inplace=True)

# Subset
dataTestSub = data._subsetFromXS(selectors = {'Type':paramType}, data = dataTest)  
p2 = dataTestSub.hvplot.scatter(x='Param',y='value', marker='dash', size=500, color='red')

# p1+p2   # Overlays fail with "NotImplementedError: Iteration on Elements is not supported." Issue with plot types? FIXED - issues was non-plot return from paramPlot()!
p1*p2
```

## Using the reconstructed matrix elements

The results tables are accessible directly, and there are also methods to reformat the best fit results for use in further calculations.

```{code-cell} ipython3
# self.paramsSummary contains the results above as Pandas Dataframe, usual Pandas methods can be applied.
data.paramsSummary['data'].describe()
```

```{code-cell} ipython3
# To set matrix elements from aggregate fit results, use `seetAggMatE` for Pandas
data.setAggMatE(simpleForm = True)
data.data['agg']['matEpd']
```

```{code-cell} ipython3
# To set matrix elements from aggregate fit results, use `aggToXR` for Xarray
# data.aggToXR(refKey = 'orb5', returnType = 'ds', conformDims=True)   # use full ref dataset
data.aggToXR(refKey = 'subset', returnType = 'ds', conformDims=True)   # Subselected matE
```

```{code-cell} ipython3
data.data['agg']['matE']
```

### Density matrices

New (experimental) code for density matrix plots and comparison. See {numref}`Sect. %s <sec:density-mat-basicsec:density-mat-basic>` for discussion. Code adapted from the {{ PEMtk_docs }} [MF reconstruction page](https://pemtk.readthedocs.io/en/latest/topical_review_case_study/matrix_element_extraction_MFrecon_PEMtk_180722-dist.html#Density-matrix-plottinghttps://pemtk.readthedocs.io/en/latest/topical_review_case_study/matrix_element_extraction_MFrecon_PEMtk_180722-dist.html#Density-matrix-plotting), original analysis for Ref. {cite}`hockett2023TopicalReviewExtracting`, illustrating the $N_2$ case.

```{code-cell} ipython3
# import numpy as np

def unsignedPhase(da):
    """Convert to unsigned phases."""
    # Set mag, phase
    mag = da.pipe(np.abs)
    phase = da.pipe(np.angle)  # Returns np array only!
    
    # Set unsigned
    magUS = mag.pipe(np.abs)
#     phaseUS = phase.pipe(np.abs)  
    phaseUS = np.abs(phase)
    
    # Set complex
    compFixed = magUS * np.exp(1j* phaseUS)
#     return mag,phase
    return compFixed
```

```{code-cell} ipython3
# v2 - as v1, but differences for unsigned phase case & fix labels
# 26/07/22: messy but working. Some labelling tricks to push back into matPlot() routine

# Import routines
from epsproc.calc import density


# Compose density matrix

# Set dimensions/state vector/representation
# These must be in original data, but will be restacked as necessary to define the effective basis space.
denDims = ['LM', 'mu']
selDims = {'Type':'L'}
pTypes=['r','i']
thres = 1e-2    # 0.2 # Threshold out l>3 terms if using full 'orb5' set.
normME = False
normDen = 'max'
usPhase = True # Use unsigned phases?

# Calculate - Ref case
# matE = data.data['subset']['matE']
# Set data from master class
# k = 'orb5'  # N2 orb5 (SG) dataset
k = 'subset'
matE = data.data[k]['matE']
if normME:
    matE = matE/matE.max()

if usPhase:
    matE = unsignedPhase(matE)
    
daOut, *_ = density.densityCalc(matE, denDims = denDims, selDims = selDims, thres = thres)  # OK

if normDen=='max':
    daOut = daOut/daOut.max()
elif normDen=='trace':
    daOut = daOut/(daOut.sum('Sym').pipe(np.trace)**2)  # Need sym sum here to get 2D trace
    
# daPlot = density.matPlot(daOut.sum('Sym'))
daPlot = density.matPlot(daOut.sum('Sym'), pTypes=pTypes)

# Retrieved
matE = data.data['agg']['matE']['compC']
selDims = {'Type':'compC'}  # For stacked DS case need to set selDims again here to avoid null data selection below.
if normME:
    matE = matE/matE.max()
    
if usPhase:
    matE = unsignedPhase(matE)
    
daOut2, *_ = density.densityCalc(matE, denDims = denDims, selDims = selDims, thres = thres)  # OK

if normDen=='max':
    daOut2 = daOut2/daOut2.max()
elif normDen=='trace':
    daOut2 = daOut2/(daOut2.sum('Sym').pipe(np.trace)**2)
    
daPlot2 = density.matPlot(daOut2.sum('Sym'), pTypes=pTypes)   #.sel(Eke=slice(0.5,1.5,1)))


# Compute difference
if usPhase:
    daDiff = unsignedPhase(daOut.sum('Sym')) - unsignedPhase(daOut2.sum('Sym'))

else:
    daDiff = daOut.sum('Sym') - daOut2.sum('Sym')

daDiff.name = 'Difference'
daPlotDiff = density.matPlot(daDiff, pTypes=pTypes)



#******** Plot
daLayout = (daPlot.redim(pType='Component').layout('Component').relabel('(a) Reference density matrix (unsigned phases)') + daPlot2.opts(show_title=False).layout('pType').opts(show_title=True).relabel('(b) Reconstructed') + 
                daPlotDiff.opts(show_title=False).layout('pType').opts(show_title=True).relabel('(c) Difference')).cols(1)  
daLayout.opts(ep.plot.hvPlotters.opts.HeatMap(width=300, frame_width=300, aspect='square', tools=['hover'], colorbar=True, cmap='coolwarm'))  # .opts(show_title=False)  # .opts(title="Custom Title")  #OK



# Notes on titles... see https://holoviews.org/user_guide/Customizing_Plots.html
#
# .relabel('Test') and .opts(title="Custom Title") OK for whole row titles
#
# daPlot2.opts(show_title=False).layout('pType').opts(show_title=True).relabel('Recon')  Turns off titles per plot, then titles layout
#
# .redim() to modify individual plot group label (from dimension name) 
```

If the reconstruction is good, the differences (fidelity) should be on the order of the experimental noise level/reconstruction uncertainty, around 10% in the case studies herein.

+++ {"tags": ["hide-output"]}

### Plot MF PADs

Routines as per https://pemtk.readthedocs.io/en/latest/topical_review_case_study/MFPAD_replotting_from_file_190722-dist.html - currently not working. Seems to be some difference in dim stacking/assignment now...? Might be Python/Xarray version change, or PEMtk/ePSproc implementation.

```{code-cell} ipython3
:tags: [hide-output]

dataIn = data.data['agg']['matE'].copy()

# # Restack for MFPAD plotter
# from epsproc.util.listFuncs import dataTypesList

# refDims = dataTypesList()
# refDims = refDims['matE']['def']
# dataStacked = dataIn.stack(refDims(sType='sDict'))
# dataStacked

# # Style 1: if full ref dataset included (with Eke dim)
# # Create empty ePSbase class instance, and set data
# # Can then use existing  padPlot() routine for all data
# from epsproc.classes.base import ePSbase
# dataTest = ePSbase(verbose = 1)

# aList = [i for i in dataIn.data_vars]  # List of arrays

# # Loop version & propagate attrs
# dataType = 'matE'
# for item in aList:
#     if item.startswith('orb'):
#         selType='L'
#     else:
#         selType = item
        
#     dataTest.data[item] = {dataType : dataIn[item].sel({'Type':selType})}

# Style 2: single Eke dim case
# Create empty ePSbase class instance, and set data
# Can then use existing  padPlot() routine for all data
from epsproc.classes.base import ePSbase
dataTest = ePSbase(verbose = 1)

aList = [i for i in dataIn.data_vars]  # List of arrays

# Loop version & propagate attrs
dataType = 'matE'
for item in aList:
    if item.startswith('sub'):
        dataTest.data[item] = {dataType : dataIn[item]}
    else:
        selType = item
        dataTest.data[item] = {dataType : dataIn[item].sel({'Type':selType})}
        
    # Push singleton Eke value to dim for plotter
    dataTest.data[item][dataType] = dataTest.data[item][dataType].expand_dims('Eke')
    
```

```{code-cell} ipython3
aList
```

```{code-cell} ipython3
item='compC'
dataType='matE'
dataTest.data[item][dataType]
```

```{code-cell} ipython3
:tags: [hide-output]

# Set polarization geoms from Euler angles

# import numpy as np
# import epsproc as ep

# Set Euler angs to include diagonal pol case
pRot = [0, 0, np.pi/2, 0]
tRot = [0, np.pi/2, np.pi/2, np.pi/4]
cRot = [0, 0, 0, 0]
labels = ['z','x','y', 'd']
eulerAngs = np.array([labels, pRot, tRot, cRot]).T   # List form to use later, rows per set of angles


# Should also use MFBLM function below instead of numeric version?
# Numeric version is handy for direct surface and difference case.
R = ep.setPolGeoms(eulerAngs = eulerAngs)
# R

# Basic version - working, but get separate plots per set.
# UPDATE: use this to generate all raw figures, then restack plotly objects below

Erange=[10,11,1]  # Set for a single E-point

# Comparison and diff
pKey = [i for i in dataIn.data_vars if i!='comp']  # List of arrays
dataTest.mfpadNumeric(keys=pKey, R = R)   # Compute MFPADs for each set of matrix elements using numerical routine
# ep.mfpad

dataTest.data['diff'] = {'TX': dataTest.data['subset']['TX'].sum('Sym')-dataTest.data['compC']['TX'].sum('Sym')}  # Add sum over sym to force matching dims
pKey.extend(['diff'])

# Plot
print(f"\n*** Plotting for keys = {pKey}, one per row ***\n")  # Note plot labels could do with some work!
dataTest.padPlot(keys=pKey, Erange=Erange, backend='pl',returnFlag=True, plotFlag=True) # Generate plotly polar surf plots for each dataset
```

```{code-cell} ipython3
# Check max differences (abs values)
maxDiff = dataTest.data['diff']['plots']['TX']['pData'].sum(['Theta','Phi']).max(dim='Eke')
maxDiff.to_pandas()
```

```{code-cell} ipython3
# Check case without phase correction too - this should indicate poor agreement in general
pKey = 'comp'
dataTest.mfpadNumeric(keys=pKey, R = R) 
dataTest.padPlot(keys=pKey, Erange=Erange, backend='pl',returnFlag=True, plotFlag=True) # Generate plotly polar surf plots for each dataset
```

```{code-cell} ipython3
:tags: [remove-cell]

# SKIP THIS - output very slow!
# TODO: fix plot labelling above.

# Version for unified plotting - stack individual plots to grid
# See https://plotly.com/python/subplots
# And https://plot.ly/python/3d-subplots

saveFigs = True
from datetime import datetime as dt
timeString = dt.now()

import plotly.graph_objects as go
from plotly.subplots import make_subplots

#*** Set gridding
# rc = [int(np.ceil(rc[0])), int(np.ceil(rc[1]))]
rc=[4,4]  # All data
# rc=[2,2]  # Test set
showscale = False

#*** Set data norms
# norm = None #
norm = 'global'

Rmax = 1.1
padding = 0.1
aRanges = dict(range=[-(Rmax + padding), Rmax+padding])
aspect = 'cube' # 'auto' # 'cube'   # 'auto' with no ranges is pretty good, or set ranges & use cube (otherwise get distorted shapes)

#*** Set camera
# Camera settings, https://plotly.com/python/3d-camera-controls/
# camera = dict(eye=dict(x=2, y=2, z=0.1))

# Defaults
# Default parameters which are used when `layout.scene.camera` is not provided
# camera = dict(
#     up=dict(x=0, y=0, z=1),
#     center=dict(x=0, y=0, z=0),
#     eye=dict(x=1.25, y=1.25, z=1.25)
# )

# Slightly lower... plus x-rotation
camera = dict(
    up=dict(x=0, y=0, z=1),
    center=dict(x=0, y=0, z=0),
    # eye=dict(x=0.8, y=1.25, z=0.8)  # Not bad... bit close?
    eye=dict(x=0.8, y=1.5, z=0.8)
)


#*** Set subplots
pType = {'type':'surface'}
specs = [[pType] * rc[1] for i in range(rc[0])]  # Set specs as 2D list of dicts.

# titles = [f"{facetDim}: {item.item()}" for item in dataPlot[facetDim]]
titles = []
colTitles =  [f'Pol({item.upper()})' for item in dataTest.data['subset']['TX'].Labels.values[0:rc[1]].tolist()]
# rowTitles = ['Mean', 'Mean phase-corrected', 'Ref', 'Diff(Ref - PC)']
rowTitles = ['Ref', 'Mean phase-corrected', 'Diff(Ref - PC)', 'Mean']

# pKey = [pKey[2], pKey[0:1], pKey[3]]  # ['comp', 'compC', 'orb5', 'diff']
pKey = ['subset', 'compC', 'diff', 'comp']   # Row ordering

fig = make_subplots(rows=rc[0], cols=rc[1], specs=specs, subplot_titles=titles, 
                    column_titles = colTitles, row_titles = rowTitles,
                    vertical_spacing = 0.05) # Note basic row/whitespace control here
fig.update_layout(height=1200, width=1200)

# Loop & grid from existing objects
n=0
for rInd in range(1,rc[0]+1):
    for cInd in range(1,rc[1]+1):
        
        # print(f'{rInd},{cInd}')
        trace = dataTest.data[pKey[rInd-1]]['plots']['TX']['polar'][0].data[cInd-1]
        
        fig.add_trace(go.Surface(x=trace['x'], y=trace['y'], z=trace['z'], colorscale='Viridis', showscale=showscale),
                    row=rInd, col=cInd)
        
        # Set string for "scene" (axis) object to update - will be labelled scene1, scene2... by Plotly.
        n=n+1
        sceneN = f'scene{n}'
        if norm == 'global':
            # Try looping... OK with dict unpacking... huzzah!
            # NOTE Scene indexing starts at 1, so do this after n increments
            # options = dict(xaxis = aRanges, yaxis = aRanges, zaxis = aRanges, aspectmode='cube')
            options = dict(xaxis = aRanges, yaxis = aRanges, zaxis = aRanges, aspectmode=aspect, camera=camera)

        else:
            # options = dict(aspectmode='cube')
            # options = dict(aspectmode='auto')  # Better for scaling up details?
            options = dict(aspectmode=aspect, camera=camera)

        fig.update_layout(**{sceneN:options})  # No effect of aspect here? auto/cube/data/manual


# fig.show()   # fig.show() quite slow for multiple surface plots - export & viewing seems better!
if saveFigs:
    fName = f'dataDump_1000fitTests_multiFit_noise_051021_MFPADs_{timeString.strftime("%d%m%y")}'
    fig.write_html(f'{fName}.html')
    fig.write_image(f'{fName}.png')
```

```{code-cell} ipython3
:tags: [remove-cell]

# Optional plot in notebook
# fig.show()   # Interactive plot - maybe quite slow

# Show image
Image(f'{fName}.png')
```

+++ {"tags": ["remove-cell"]}

# SCRATCH

```{code-cell} ipython3
:tags: [remove-cell]

data.lmmu  #['lmMap']
```

```{code-cell} ipython3
:tags: [remove-cell]

data.paramsSummaryComp.columns
```

```{code-cell} ipython3
remap = 'lmMap'
data.paramsSummaryComp.replace({'Param':data.lmmu[remap]}, inplace=False)
```

```{code-cell} ipython3
:tags: [remove-cell]

data.paramFidelity()
```

```{code-cell} ipython3

```
