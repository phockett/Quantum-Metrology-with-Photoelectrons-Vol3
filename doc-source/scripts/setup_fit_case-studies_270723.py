# Setup demo fitting data for PEMtk testing - OCS VERSION
# 28/06/23
#
# Manual mods from current version https://github.com/phockett/PEMtk/blob/master/demos/fitting/setup_fit_demo.py for testing
#
# v1/N2 Follows approx first half of demo notebook https://pemtk.readthedocs.io/en/latest/fitting/PEMtk_fitting_basic_demo_030621-full.html
# Just removed plotting/output functions here for use in further testing.
#
#
# 05/07/23: 3D ADM test version only.
#
# 12/07/23: 3D ADM test version for C2H4 (plus 1st addition for this case).
#
# 27/07/23: general case study case.
#           Note individual case studies have settings in a few places (by config type).
#           Quite messy!
#
#           NOTE: should update to use self.AFBLM for basic calcs, already wraps core function & return.
#

print('*** Setting up demo fitting workspace and main `data` class object...')
print('Script: QM3 case studies')
print('For more details see https://pemtk.readthedocs.io/en/latest/fitting/PEMtk_fitting_basic_demo_030621-full.html')
print('To use local source code, pass the parent path to this script at run time, e.g. "setup_fit_demo ~/github"')
print('\n\n* Loading packages...')

# 03/04/23: updated to use argparse for multiple arg passing
# Note this keeps positional arg for modPath for back-compatibility.
import argparse

parser = argparse.ArgumentParser(description='Setup fitting workspace with module imports and test dataset. If not set default system paths will be used.')
parser.add_argument("modPathDefault", nargs='?', default=None, type=str, help='Module path (optional, positional) - deprecated, use -m flag for preference.')
parser.add_argument("-d", "--dataPath", type=str, help='Data path. Defaults to module path if not set.')
parser.add_argument("-m", "--modPathName", type=str, help='Module path (optional).')
parser.add_argument("-a", "--admFileName", type=str, help='Data file for ADMs (in dataPath).')
parser.add_argument("-c", "--case", type=str, help='Set for (default) QM3 case studies. Cases = "N2", "OCS" or "C2H4".')
parser.add_argument("-a3D", "--add3DADMs", type=str, help='Set for test 3D ADMs - adds to 1D ADM set. Pass "y" to apply.')
parser.add_argument("-n","--addNoise", type=str, help='Pass "y" to add noise to test data. Defaults to ~10%, set sigma manually to override.')
parser.add_argument("-s","--sigma", type=float, help='Sigma (spread) for Gaussian noise. Defaults to 0.05 (~10% noise), only applied if "--addNoise" is set.')
args = parser.parse_args()
# print(args)

modPath = args.modPathName if args.modPathName else args.modPathDefault
dataPath = args.dataPath if args.dataPath else None
admFileName = args.admFileName if args.admFileName else None
caseStudy = args.case if args.case else None
add3DtestADMs = args.add3DADMs if args.add3DADMs else None

# Add noise?  And set params.
addNoise = True if (args.addNoise == 'y') else False
sigma = args.sigma if args.sigma else 0.05
mu = 0
# print(f"Using input module path {modPath}, data path {dataPath}.")

# A few standard imports...

# +
import sys
import os
from pathlib import Path
import numpy as np
# import epsproc as ep
import xarray as xr

from datetime import datetime as dt
timeString = dt.now()

# Force inline graphics output from script (if called from a notebook)
# Solution from https://stackoverflow.com/a/58057468
get_ipython().magic('matplotlib inline')

# With passed arg
localFlag = False

if modPath:

    # Append to sys path
    modPath = Path(modPath)
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

    print(f"\n*** Required modules not found. Setup script will abort.")
    sys.exit()

# Set data path, defaults to Path(ep.__path__[0]).parent/'data'
# if len(args) > 2:
if dataPath:
    dataPath = Path(dataPath)
    epDemoDataPath = Path(dataPath)
    epDemoDataFlag = False
else:
    # Note this is set here from ep.__path__, but may not be correct in all cases - depends on where the Github repo is.
    epDemoDataPath = Path(ep.__path__[0]).parent/'data'
    epDemoDataFlag = True

# +
# Set HTML output style for Xarray in notebooks (optional), may also depend on version of Jupyter notebook or lab, or Xr
# See http://xarray.pydata.org/en/stable/generated/xarray.set_options.html
# if isnotebook():
# xr.set_options(display_style = 'html')
# -

# Set some plot options
# ep.plot.hvPlotters.setPlotters()

# ### Set & load parameters
#
# There are a few things that need to be configured for a given case...
#
# - Matrix elements (or (l,m,mu) indicies) to use.
# - Alignment distribution (ADMs).
# - Polarization geometry.
#
# In this demo, a real case will first be simulated with computational values, and then used to test the fitting routines.
#
#
# #### Matrix elements
#
# For fit testing, start with computational values for the matrix elements. These will be used to simulate data, and also to provide a list of parameters to fit later.

# +
# Set for ePSproc test data, available from https://github.com/phockett/ePSproc/tree/master/data
# Note this is set here from ep.__path__, but may not be correct in all cases.


# Multiorb data for normal module path
if epDemoDataFlag:
    dataPath = os.path.join(epDemoDataPath, 'photoionization', 'n2_multiorb')
    # dataPath = Path(epDemoDataPath, 'photoionization', 'n2_multiorb')

print(f'\n* Loading demo matrix element data from {dataPath}')

# TODO: add in some path error checking here or in scanFiles() - currently errors if no files found.
data = pemtkFit(fileBase = dataPath, verbose = 1)

# Read data files
# OCSorb = None
if caseStudy == 'OCS':
    # For OCS force 2 files only for flat file structure IO
    data.scanFiles(fileIn=[Path(dataPath,'OCS_survey.orb10_E0.1_2.0_30.1eV.inp.out').as_posix(), Path(dataPath,'OCS_survey.orb11_E0.1_2.0_30.1eV.inp.out').as_posix()])
    OCSorb = 'orb13'   # Set for orb13 (sigma, HOMO-1) or orb14 (pi, HOMO)
    
    data.molSummary(dataKey=OCSorb)

else:
    data.scanFiles()
    
data.jobsSummary()

# #### Alignment distribution moments (ADMs)
#
# The class [wraps ep.setADMs()](https://epsproc.readthedocs.io/en/dev/modules/epsproc.sphCalc.html#epsproc.sphCalc.setADMs). This returns an isotropic distribution by default, or values can be set explicitly from a list. Values are set in `self.data['ADM']`.
#
# Note: if this is not set, the default value will be used, which is likely not very useful for the fit!

# Default case
data.setADMs()

# Load time-dependent ADMs for N2 case
# Adapted from ePSproc_AFBLM_testing_010519_300719.m
from scipy.io import loadmat

# Set ADM data file
defaultN2ADMs = False
defaultOCSADMs = False

if not admFileName:
    admFileName = 'N2_ADM_VM_290816.mat'
    defaultN2ADMs = True
    print("*** Running with default N2 settings.")

if epDemoDataFlag:
    # ADMdataFile = os.path.join(epDemoDataPath, 'alignment', admFileName)
    ADMdataFile = Path(epDemoDataPath, 'alignment', admFileName)
else:
    # ADMdataFile = os.path.join(epDemoDataPath, admFileName)
    ADMdataFile = Path(epDemoDataPath, admFileName)
    
if ADMdataFile.stem.startswith("OCS"):
    defaultOCSADMs = True
    print("*** Running with default OCS settings.")
    
# Add case for multi-ADM files, e.g. OCS dataset
# if admFileName.startswith('A'):  # Pass 1st file only?
#    fList = ep.getFiles(fileBase =  ADMdataDir, fType='.dat')


# if not isinstance(admFileName, list):  # Pass as list

if ADMdataFile.is_file():   # Check if file, or assume dir below

    print(f'\n\n* Loading demo ADM data from file {ADMdataFile}...')

    try:
        ADMs = loadmat(ADMdataFile)
    except FileNotFoundError:
        print("\n*** ADM data file not found. Setup script will abort.")
        sys.exit()

    if defaultN2ADMs:
        # Set tOffset for calcs, 3.76ps!!!
        # This is because this is 2-pulse case, and will set t=0 to 2nd pulse (and matches defn. in N2 experimental paper)
        tOffset = -3.76
        ADMs['time'] = ADMs['time'] + tOffset
    
    # For this case using 'ADMs_8TW_120fs_5K.mat'
    # ADMs only, with K,S labels in array.
    if caseStudy=='C2H4':
        # ADMs in this case are labelled [K,S], but expect [K,Q,S] so fix this
        KQSLabels = ADMs['adms'][:,0:2]
        KQSLabels = np.c_[KQSLabels[:,0], np.zeros(KQSLabels.shape[0]), KQSLabels[:,1]]
        ADMs = ADMs['adms'][:,2:]
        
        # With fixed labels above
        data.setADMs(ADMs = ADMs, KQSLabels = KQSLabels)
        
        # Add -ve S
        key = 'ADM'
        dataType='ADM'
        mirrorDim = 'S'
        negDim = data.data[key][dataType].unstack().where(data.data[key][dataType].unstack()[mirrorDim]!=0, drop=True)
        negDim[mirrorDim] = -1 * negDim[mirrorDim]   # In place mod fails here... but currently working in afblm routine?  Weird.
        negDim = negDim.stack({'ADM':['K','Q','S']})
        negDim = negDim.where(negDim[mirrorDim].pipe(np.abs) <= negDim.K, drop=True)  # Clean up stacked coords.
        allS = xr.concat([data.data[key][dataType], negDim], dim='ADM')

        # Scale?
        ADMscaleFactor = 2*np.pi
        allS = allS *ADMscaleFactor
        
        # Set to main class
#         key = 'ADM'
#         dataType='ADM'
        data.data[key][dataType] = allS
#         data.data[key][dataType].unstack().real.hvplot.line(x='t').overlay(['K','Q','S']) 
        
        
    else:

        data.setADMs(ADMs = ADMs['ADM'], t=ADMs['time'].squeeze(), KQSLabels = ADMs['ADMlist'], addS = True)

    
else:
    print(f'\n\n* Loading demo ADM data from dir {ADMdataFile}...')
    
    # 25/06/23 - OCS version with fixed renorm - just use 2pi scale factor
    ADMscaleFactor = 2*np.pi 
    addPop = True
    
    # Get files from dir
    # THIS ASSUMES set of .dat files, A20, A40... per OCS dataset.
    ADMtype = 'dat'
    fList = ep.getFiles(fileBase =  Path(ADMdataFile).expanduser(), fType='.'+ADMtype)

    ADMs = []
    ADMLabels = []

    for f in fList:

        item = Path(f).name.split('_')[0]  # Get & set variable name

        if item == 'time':
            t = loadmat(f)[item][0,:]

        elif item == 'c2t':
            c2t = loadmat(f)[item][:,0]

        else:            
            K = int(item.strip('A')[0])
            ADMs.append(loadmat(f)[item][:,0]*ADMscaleFactor)
            ADMLabels.append([K,0,0])


    # Add K = 0 (population) term?
    # NOTE - may need additional renorm?
    if addPop:
        # ADMs.append(np.ones(t.size) * (1/(4*np.pi)) * ADMscaleFactor)        
        # ADMs.append(np.ones(t.size) * 0.5)       # This and above give A00=0.5 
        ADMs.append(np.ones(t.size))     # A00=1, doesn't make any difference to Betas?
        ADMLabels.append([0,0,0])

    ADMLabels = np.array(ADMLabels)
    
    data.setADMs(ADMs = ADMs, KQSLabels = ADMLabels, t=t)
    

# For 3D test case, add linear ramp ADMs
if add3DtestADMs:
    print('*** Adding 3D test ADMs...')
    tPoints = data.data['ADM']['ADM'].t.size

    inputADMs = [[2,2,0, *np.linspace(-0.1,0.1,tPoints)], 
                 [2,2,0, *np.linspace(-0.1,0.1,tPoints)],
                 [2,-2,0, *np.linspace(-0.1,0.1,tPoints)],
                 [2,2,2, *np.linspace(0,0.1,tPoints)],
                 [2,-2,-2, *np.linspace(0,0.1,tPoints)],
                 [1,-1,-1, *np.linspace(0,0.1,tPoints)],
                 [1,1,1, *np.linspace(0,0.1,tPoints)]]

    ADM3D = ep.setADMs(ADMs = inputADMs, t=t, name="3D")  # TODO WRAP TO CLASS (IF NOT ALREADY!)

    # Add ADMs
    # ADMall = xr.merge([ADMs, ADM3D]).to_array().sum('variable')  # OK after renaming input arrays
    data.data['ADM']['ADM'] = xr.concat([data.data['ADM']['ADM'], ADM3D], dim='ADM')  # Also works, note different ordering of ADM dim in this case
    
data.data['ADM']['ADM']


# ### Polarisation geometry/ies
#
# This wraps [ep.setPolGeoms](https://epsproc.readthedocs.io/en/dev/modules/epsproc.sphCalc.html#epsproc.sphCalc.setPolGeoms). This defaults to (x,y,z) polarization geometries. Values are set in `self.data['pol']`.
#
# Note: if this is not set, the default value will be used, which is likely not very useful for the fit!
#

data.setPolGeoms()


# ### Subselect data
#
# Currently handled in the class by setting `self.selOpts`, this allows for simple reuse of settings as required. Subselected data is set to `self.data['subset'][dataType]`, and is the data the fitting routine will use.
# Settings for type subselection are in selOpts[dataType]

print(f'\n* Subselecting data...')

if caseStudy=='N2':
    print(f"*** Setting for {caseStudy} case study.")
    # E.g. Matrix element sub-selection
    data.selOpts['matE'] = {'thres': 0.01, 'inds': {'Type':'L', 'Eke':1.1}}
    data.setSubset(dataKey = 'orb5', dataType = 'matE')  # Subselect from 'orb5' dataset, matrix elements


    # And for the polarisation geometries...
    data.selOpts['pol'] = {'inds': {'Labels': 'z'}}
    data.setSubset(dataKey = 'pol', dataType = 'pol')

    # And for the ADMs...
    data.selOpts['ADM'] = {}   #{'thres': 0.01, 'inds': {'Type':'L', 'Eke':1.1}}
    data.setSubset(dataKey = 'ADM', dataType = 'ADM', sliceParams = {'t':[4, 5, 4]})
    
elif caseStudy=='OCS':
    print(f"*** Setting for {caseStudy} case study.")
    # Settings for type subselection are in selOpts[dataType]

    # Matrix element sub-selection - currently configured for orb13 or 14
    # Pi-HOMO
    if OCSorb == 'orb14':
        data.selOpts['matE'] = {'thres': 0.01, 'inds': {'Type':'L', 'Eke':10.1, 'it':2}, 'sq':False}
        data.setSubset(dataKey = 'orb14', dataType = 'matE')  # Subselect from '1' dataset, matrix elements for HOMO
        # Fix issues with squeezed 'it' coord in single selection case
        data.data[data.subKey]['matE'] = data.data[data.subKey]['matE'].expand_dims(dim='it')
    else:
        # Sigma-HOMO-1
        data.selOpts['matE'] = {'thres': 0.01, 'inds': {'Type':'L', 'Eke':10.1}, 'sq':False}
        data.setSubset(dataKey = OCSorb, dataType = 'matE')  # Subselect from '1' dataset, matrix elements for HOMO

    
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
    # trange=[38, 44]  # Set range in ps for calc
    # tStep=4  # Set tStep for downsampling
    # tMask = (data.data['ADM']['ADM'].t>trange[0]) & (data.data['ADM']['ADM'].t<trange[1])
    # data.data[data.subKey]['ADM'] = data.data['ADM']['ADM'][:,tMask][:,::tStep]  # Set and update
    # print(f"ADMs: Selecting {data.data['subset']['ADM'].t.size} points from {data.data['ADM']['ADM'].t.size}")
    #
    # TEST FOR 2 ranges...
    #
    # Selection & downsampling - adapted from https://epsproc.readthedocs.io/en/latest/methods/geometric_method_dev_pt3_AFBLM_090620_010920_dev_bk100920.html#Test-compared-to-experimental-N2-AF-results...
    # See PEMtk for updated routines, https://pemtk.readthedocs.io/en/latest/fitting/PEMtk_fitting_basic_demo_030621-full.html#Subselect-data
    # See Xarray docs for basics https://xarray.pydata.org/en/stable/user-guide/indexing.html#indexing-with-dimension-names

    # trange={'main':[38, 44],'quater':[18,22]}  # Set range in ps for calc, dict with multiple entries
    # tStep=4  # Set tStep for downsampling

    # With dict
    trange={'main':[38, 44],'quarter':[18,22]}  # Set range in ps for calc, dict with multiple entries
    tStep=4  # Set tStep for downsampling
    
    tMaskAll = xr.zeros_like(data.data['ADM']['ADM'].t).astype(bool)
    # tMaskAll.data.astype(bool)
    for k,v in trange.items():
    #     tMask = xr.zeros_like(ADMs.t)
        tMask = (data.data['ADM']['ADM'].t>v[0]) & (data.data['ADM']['ADM'].t<v[1])

    #     trange['tMask'] = {k:tMask}

        tMaskAll = tMaskAll + tMask


    # data.data['ADM'] = {'ADM': ADMs[:,tMaskAll][:,::tStep]}   # Set and update
    data.data[data.subKey]['ADM'] = data.data['ADM']['ADM'][:,tMaskAll][:,::tStep]
    print(f"ADMs: Selecting {data.data['subset']['ADM'].t.size} points from {data.data['ADM']['ADM'].t.size}")

    
elif caseStudy == 'C2H4':
    # Settings for type subselection are in selOpts[dataType]

    # E.g. Matrix element sub-selection
#     data.selOpts['matE'] = {'thres': 0.1, 'inds': {'Type':'L', 'Eke':6}, 'sq':False}  # Tested in 6189238, seemed WORSE than 0.01 case
    data.selOpts['matE'] = {'thres': 0.01, 'inds': {'Type':'L', 'Eke':6}, 'sq':False}
    data.setSubset(dataKey = 'orb8', dataType = 'matE')  # Subselect from '1' dataset, matrix elements for HOMO

    # And for the polarisation geometries...
    data.selOpts['pol'] = {'inds': {'Labels': 'z'}}
    data.setSubset(dataKey = 'pol', dataType = 'pol')

    # And for the ADMs...
    # SLICE version - was working, but not working July 2022, not sure if it's data types or Xarray version issue? Just get KeyErrors on slice. WORKING FOR INT INDEX CASE OK.
    data.selOpts['ADM'] = {}   #{'thres': 0.01, 'inds': {'Type':'L', 'Eke':1.1}}
#     data.setSubset(dataKey = 'ADM', dataType = 'ADM', sliceParams = {'t':[420, 520, 5]}) 
    # data.setSubset(dataKey = 'ADM', dataType = 'ADM', sliceParams = {'t':[420, 520, 5]})   # 21 t-points
    # data.setSubset(dataKey = 'ADM', dataType = 'ADM', sliceParams = {'t':[370, 560, 5]})   # 39 t-points
    data.setSubset(dataKey = 'ADM', dataType = 'ADM', sliceParams = {'t':[220, 580, 5]})   # 73 t-points, two K=2 large features
    


else:
    print(f"*** No case study defined, setting for defaults.")
    
    # E.g. Matrix element sub-selection
    data.selOpts['matE'] = {'thres': 0.01, 'inds': {'Type':'L'}}
    data.setSubset(dataKey = list(data.data.keys())[0], dataType = 'matE')  # Subselect from 'orb5' dataset, matrix elements


    # And for the polarisation geometries...
    data.selOpts['pol'] = {'inds': {'Labels': 'z'}}
    data.setSubset(dataKey = 'pol', dataType = 'pol')

    # And for the ADMs...
    data.selOpts['ADM'] = {}   #{'thres': 0.01, 'inds': {'Type':'L', 'Eke':1.1}}
    tRange = [data.data['ADM']['ADM'].t[0], data.data['ADM']['ADM'].t[60], 4]  # Set first 0:60 in steps
    # data.setSubset(dataKey = 'ADM', dataType = 'ADM', sliceParams = {'t':[4, 5, 4]})
    data.setSubset(dataKey = 'ADM', dataType = 'ADM', sliceParams = {'t':tRange})
    
    
    
# ## Compute AF-$\beta_{LM}$ and simulate data
#
# With all the components set, some observables can be calculated. For testing, we'll also use this to simulate an experiemental trace...
#
# Here we'll use `self.afblmMatEfit()`, which is also the main fitting routine, and essentially wraps `epsproc.afblmXprod()` to compute AF-$\beta_{LM}$s (for more details, see the [ePSproc method development docs](https://epsproc.readthedocs.io/en/dev/methods/geometric_method_dev_pt3_AFBLM_090620_010920_dev_bk100920.html)).
#
# If called without reference data, the method returns computed AF-$\beta_{LM}$s based on the input subsets already created, and also a set of (product) basis functions generated - these can be examined to get a feel for the sensitivity of the geometric part of the problem, and will also be used in fitting to limit repetitive computation.

# ### Compute AF-$\beta_{LM}$s

print(f'\n* Calculating AF-BLMs...')

#************** FOR 3D ADMs case
# Testing fixed case - in setPhaseConventions() some of these are correlated, and set from `phaseCons['genMatEcons']['negm']` - does it matter here?
# NOTE THIS MAYBE INCORRECT, see https://github.com/phockett/ePSproc/issues/26#issuecomment-1640541159
# But OK for general fit testing
from epsproc.geomFunc.geomCalc import setPhaseConventions
phaseConsTest = setPhaseConventions(phaseConvention = 'E')
phaseConsTest['afblmCons']['negM'] = True

# Test ADMs now set above.
# if add3DtestADMs:
#     tPoints = data.data['ADM']['ADM'].t.size

#     inputADMs = [[2,2,0, *np.linspace(-0.1,0.1,tPoints)], 
#                  [2,2,0, *np.linspace(-0.1,0.1,tPoints)],
#                  [2,-2,0, *np.linspace(-0.1,0.1,tPoints)],
#                  [2,2,2, *np.linspace(0,0.1,tPoints)],
#                  [2,-2,-2, *np.linspace(0,0.1,tPoints)],
#                  [1,-1,-1, *np.linspace(0,0.1,tPoints)],
#                  [1,1,1, *np.linspace(0,0.1,tPoints)]]

#     ADM3D = ep.setADMs(ADMs = inputADMs, t=t, name="3D")  # TODO WRAP TO CLASS (IF NOT ALREADY!)

#     # Add ADMs
#     # ADMall = xr.merge([ADMs, ADM3D]).to_array().sum('variable')  # OK after renaming input arrays
#     data.data['ADM']['ADM'] = xr.concat([data.data['ADM']['ADM'], ADM3D], dim='ADM')  # Also works, note different ordering of ADM dim in this case

# # UPDATE master
# # With dict
# # trange={'main':[38, 44],'quarter':[18,22]}  # Set range in ps for calc, dict with multiple entries
# # tStep=4  # Set tStep for downsampling

# # tMaskAll = xr.zeros_like(data.data['ADM']['ADM'].t).astype(bool)
# # # tMaskAll.data.astype(bool)
# # for k,v in trange.items():
# # #     tMask = xr.zeros_like(ADMs.t)
# #     tMask = (data.data['ADM']['ADM'].t>v[0]) & (data.data['ADM']['ADM'].t<v[1])

# # #     trange['tMask'] = {k:tMask}

# #     tMaskAll = tMaskAll + tMask


# # data.data['ADM'] = {'ADM': ADMs[:,tMaskAll][:,::tStep]}   # Set and update
# data.data[data.subKey]['ADM'] = data.data['ADM']['ADM'][:,tMaskAll][:,::tStep]
# print(f"ADMs updated for 3D case: Selecting {data.data['subset']['ADM'].t.size} points from {data.data['ADM']['ADM'].t.size}")



# data.afblmMatEfit(data = None)  # OK
if not caseStudy=="OCS" or caseStudy=="C2H4":
    BetaNormX, basis = data.afblmMatEfit()  # OK, uses default polarizations & ADMs as set in data['subset']
    # BetaNormX, basis = data.afblmMatEfit(ADM = data.data['subset']['ADM'])  # OK, but currently using default polarizations
    # BetaNormX, basis = data.afblmMatEfit(ADM = data.data['subset']['ADM'], pol = data.data['pol']['pol'].sel(Labels=['x']))
    # BetaNormX, basis = data.afblmMatEfit(ADM = data.data['subset']['ADM'], pol = data.data['pol']['pol'].sel(Labels=['x','y']))  # This fails for a single label...?
    # BetaNormX, basis = data.afblmMatEfit(RX=data.data['pol']['pol'])  # This currently fails, need to check for consistency in ep.sphCalc.WDcalc()
                                                                        # - looks like set values and inputs are not consistent in this case? Not passing angs correctly, or overriding?
                                                                        # - See also recently-added sfError flag, which may cause additional problems.

else:
    if (caseStudy=='OCS') and (OCSorb == 'orb14'):
        # For OCS case study
        BetaNormX, basis = data.afblmMatEfit(selDims={'it': 2}, phaseConvention=phaseConsTest)   # Also need this with selOpts set, but dim readded, TO FIX!
    else:
        BetaNormX, basis = data.afblmMatEfit(phaseConvention=phaseConsTest)
            
            
# ### AF-$\beta_{LM}$s

# The returned objects contain the $\beta_{LM}$ parameters as an Xarray...

# BetaNormX



# ## Fitting the data
#
# In order to fit data, and extract matrix elements from an experimental case, we'll use the [lmfit library](https://lmfit.github.io/lmfit-py/intro.html). This wraps core Scipy fitting routines with additional objects and methods, and is further wrapped for this specific class of problems in `pemtkFit` class we're using here.

# ### Set the data to fit
#
# Here we'll use the values calculated above as our test data. This currently needs to be set as `self.data['subset']['AFBLM']` for fitting.

# +
# data.data['subset']['AFBLM'] = BetaNormX  # Set manually

data.setData('sim', BetaNormX)  # Set simulated data to master structure as "sim"
data.setSubset('sim','AFBLM')   # Set to 'subset' to use for fitting.

# -

# Set basis functions
data.basis = basis

# ### Setting up the fit parameters
#
# In this case, we can work from the existing matrix elements to speed up parameter creation, although in practice this may need to be approached ab initio - nonetheless, the method will be the same, and the ab initio case detailed later.

# Input set, as defined earlier
# data.data['subset']['matE'].pd

print('\n*Setting  up fit parameters (with constraints)...')
# data.setMatEFit()  # Need to fix self.subset usage
# data.setMatEFit(data.data['subset']['matE'])  #, Eke=1.1) # Some hard-coded things to fix here! Now roughly working.

# With constraints
# Set param constraints as dict
# paramsCons = {}
# paramsCons['m_PU_SG_PU_1_n1_1'] = 'm_PU_SG_PU_1_1_n1'
# paramsCons['p_PU_SG_PU_1_n1_1'] = 'p_PU_SG_PU_1_1_n1'
#
# paramsCons['m_PU_SG_PU_3_n1_1'] = 'm_PU_SG_PU_3_1_n1'
# paramsCons['p_PU_SG_PU_3_n1_1'] = 'p_PU_SG_PU_3_1_n1'
#
# data.setMatEFit(paramsCons = paramsCons)

# With auto setting (from existing matrix elements)
data.setMatEFit()

if caseStudy=="C2H4":
#     # Manual mods for missing expressions
#     # ACTUALLY MIGHT BE PHASE ISSUE? Mags identical, but phases not, maybe missing correct check in symChecks for this case?
#     for pType in ['m']:    #,'p']:
#         data.params[f'{pType}_AG_B3U_B3U_0_0_1_1'].expr = f'{pType}_AG_B3U_B3U_0_0_n1_1'
#         data.params[f'{pType}_AG_B3U_B3U_2_0_1_1'].expr = f'{pType}_AG_B3U_B3U_2_0_n1_1'
#         data.params[f'{pType}_AG_B3U_B3U_2_n2_1_1'].expr = f'{pType}_AG_B3U_B3U_2_n2_n1_1 '
#         data.params[f'{pType}_AG_B3U_B3U_4_0_1_1'].expr = f'{pType}_AG_B3U_B3U_4_0_n1_1'
#         data.params[f'{pType}_AG_B3U_B3U_4_n2_1_1'].expr = f'{pType}_AG_B3U_B3U_4_n2_n1_1'
#         data.params[f'{pType}_AG_B3U_B3U_4_n4_1_1'].expr = f'{pType}_AG_B3U_B3U_4_n4_n1_1'
#         data.params[f'{pType}_AG_B3U_B3U_6_0_1_1'].expr = f'{pType}_AG_B3U_B3U_6_0_n1_1'

#         data.params[f'{pType}_B1G_B3U_B2U_2_2_n1_1'].expr = f'{pType}_B1G_B3U_B2U_2_n2_n1_1'
#         data.params[f'{pType}_B1G_B3U_B2U_4_2_n1_1'].expr = f'{pType}_B1G_B3U_B2U_4_n2_n1_1'

#         data.params[f'{pType}_B2G_B3U_B1U_2_1_0_1'].expr = f'{pType}_B2G_B3U_B1U_2_n1_0_1'
#         data.params[f'{pType}_B2G_B3U_B1U_4_1_0_1'].expr = f'{pType}_B2G_B3U_B1U_4_n1_0_1'
#         data.params[f'{pType}_B2G_B3U_B1U_4_3_0_1'].expr = f'{pType}_B2G_B3U_B1U_4_n3_0_1'

    # Quick hack for 0.1 case
    pType='m'
    if data.selOpts['matE']['thres'] == 0.01:
        data.params[f'{pType}_AG_B3U_B3U_0_0_1_1'].expr = f'{pType}_AG_B3U_B3U_0_0_n1_1'
        data.params[f'{pType}_AG_B3U_B3U_2_0_1_1'].expr = f'{pType}_AG_B3U_B3U_2_0_n1_1'
        data.params[f'{pType}_AG_B3U_B3U_2_n2_1_1'].expr = f'{pType}_AG_B3U_B3U_2_n2_n1_1 '
        data.params[f'{pType}_AG_B3U_B3U_4_0_1_1'].expr = f'{pType}_AG_B3U_B3U_4_0_n1_1'
        data.params[f'{pType}_AG_B3U_B3U_4_n2_1_1'].expr = f'{pType}_AG_B3U_B3U_4_n2_n1_1'
        data.params[f'{pType}_AG_B3U_B3U_4_n4_1_1'].expr = f'{pType}_AG_B3U_B3U_4_n4_n1_1'
        data.params[f'{pType}_AG_B3U_B3U_6_0_1_1'].expr = f'{pType}_AG_B3U_B3U_6_0_n1_1'

        data.params[f'{pType}_B1G_B3U_B2U_2_2_n1_1'].expr = f'{pType}_B1G_B3U_B2U_2_n2_n1_1'
        data.params[f'{pType}_B1G_B3U_B2U_4_2_n1_1'].expr = f'{pType}_B1G_B3U_B2U_4_n2_n1_1'

        data.params[f'{pType}_B2G_B3U_B1U_2_1_0_1'].expr = f'{pType}_B2G_B3U_B1U_2_n1_0_1'
        data.params[f'{pType}_B2G_B3U_B1U_4_1_0_1'].expr = f'{pType}_B2G_B3U_B1U_4_n1_0_1'
        data.params[f'{pType}_B2G_B3U_B1U_4_3_0_1'].expr = f'{pType}_B2G_B3U_B1U_4_n3_0_1'
        
    else:
        data.params[f'{pType}_AG_B3U_B3U_0_0_1_1'].expr = f'{pType}_AG_B3U_B3U_0_0_n1_1'
        data.params[f'{pType}_AG_B3U_B3U_2_0_1_1'].expr = f'{pType}_AG_B3U_B3U_2_0_n1_1'
        data.params[f'{pType}_AG_B3U_B3U_2_n2_1_1'].expr = f'{pType}_AG_B3U_B3U_2_n2_n1_1 '
        data.params[f'{pType}_AG_B3U_B3U_4_0_1_1'].expr = f'{pType}_AG_B3U_B3U_4_0_n1_1'
        data.params[f'{pType}_AG_B3U_B3U_4_n2_1_1'].expr = f'{pType}_AG_B3U_B3U_4_n2_n1_1'
        # data.params[f'{pType}_AG_B3U_B3U_4_n4_1_1'].expr = f'{pType}_AG_B3U_B3U_4_n4_n1_1'
        # data.params[f'{pType}_AG_B3U_B3U_6_0_1_1'].expr = f'{pType}_AG_B3U_B3U_6_0_n1_1'

        data.params[f'{pType}_B1G_B3U_B2U_2_2_n1_1'].expr = f'{pType}_B1G_B3U_B2U_2_n2_n1_1'
        data.params[f'{pType}_B1G_B3U_B2U_4_2_n1_1'].expr = f'{pType}_B1G_B3U_B2U_4_n2_n1_1'

        data.params[f'{pType}_B2G_B3U_B1U_2_1_0_1'].expr = f'{pType}_B2G_B3U_B1U_2_n1_0_1'
        data.params[f'{pType}_B2G_B3U_B1U_4_1_0_1'].expr = f'{pType}_B2G_B3U_B1U_4_n1_0_1'
        # data.params[f'{pType}_B2G_B3U_B1U_4_3_0_1'].expr = f'{pType}_B2G_B3U_B1U_4_n3_0_1'
        
    # Test changing max vals...
    for item in data.params:
        if item.startswith('m_'):
            data.params[item].max = 2.0

if addNoise:
    print(f'\n*** Adding Gaussian noise, mu={mu}, sigma={sigma}')
#     mu, sigma = 0, 0.05  # Up to approx 10% noise (+/- 0.05)
    # creating a noise with the same dimension as the dataset (2,2) 
    noise = np.random.normal(mu, sigma, [data.data['subset']['AFBLM'].t.size, data.data['subset']['AFBLM'].l.size])
    # data.BLMfitPlot()

    # Set noise in Xarray & scale by l
    noiseXR = xr.ones_like(data.data['subset']['AFBLM']) * noise * data.data['subset']['AFBLM'].max()  # FOR OCS ADDED * data.data['subset']['AFBLM'].max() to rescale noise, otherwise ~100%!  Issue is renorm (or not) of values with ADMs.
    # data.data['subset']['AFBLM']['noise'] = ((data.data['subset']['AFBLM'].t, data.data['subset']['AFBLM'].l), noise)
    # xr.where(noiseXR.l>0, noiseXR/noiseXR.l, noiseXR)
    noiseXR = noiseXR.where(noiseXR.l<1, noiseXR/(noiseXR.l))  # Scale by L

    data.data['subset']['AFBLM'] = data.data['subset']['AFBLM'] + noiseXR
    data.data['subset']['AFBLM'] = data.data['subset']['AFBLM'].where(data.data['subset']['AFBLM'].m == 0, 0)
            

print('\n\n*** Setup demo fitting workspace OK.')

# Plot data
from matplotlib import pyplot as plt
data.BLMfitPlot(keys=['subset','sim'])
plt.title(f'{caseStudy}: Simulated data, and subset for fitting.')

# This sets `self.params` from the matrix elements, which are a set of (real) parameters for lmfit, as [a Parameters object](https://lmfit.github.io/lmfit-py/parameters.html).
#
# Note that:
#
# - The input matrix elements are converted to magnitude-phase form, hence there are twice the number as the input array, and labelled `m` or `p` accordingly, along with a name based on the full set of QNs/indexes set.
# - One phase is set to `vary=False`, which defines a reference phase. This defaults to the first phase item.
# - Min and max values are defined, by default the ranges are 1e-4<mag<5, -pi<phase<pi.
# - No relationships between the parameters are set by default (apart from the single fixed phase), but can be set manually, [see section below](http://127.0.0.1:8888/lab/workspaces/pemtk#Setting-parameter-relations).
