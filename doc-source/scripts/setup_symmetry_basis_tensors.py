# Setup symmetry-defined matrix elements using PEMtk

# Basic routine for Quantum Metrology Vol. 3 demo case.
# See Sect. 3.3 for further notes
#
# 27/07/23   v2   Now includes symmetry selection routines and full assignments for matE case to enable AFBLM computation.

# Imports
import epsproc as ep
import numpy as np

# Import classes
from pemtk.fit.fitClass import pemtkFit
from pemtk.sym.symHarm import symHarm

# 13/04/23: updated to use argparse for multiple arg passing
# Note this keeps default case to match previous hard-coded symmetry (D2h).
# Note also that D2h case includes .sum(['h','muX']) (for redundant dims)
# For now this is OMITTED in all other cases.
# 21/07/23: DEBUG version for testing with info content page, now broken.
#           Likely issue with full sym selection routines?
import argparse

parser = argparse.ArgumentParser(description='Setup symmetrized harmonics and basis functions. Default case runs for sym=D2h, lmax=4, lmaxPlot=2.')
parser.add_argument("-s","--sym", type=str, default='D2h', help="Symmetry to use, default=D2h. Allowed cases: ['Ci', 'Cs', 'Cnv', 'Dn', 'Dnh', 'Dnd', 'Td', 'O', 'Oh', 'I', 'Ih']")
# Can set choices to list, but will need to subs all n?
# For allowed cases, see https://pemtk.readthedocs.io/en/latest/sym/pemtk_symHarm_demo_160322_tidy.html#Create-class-&-compute-harmonics
# choices=['Ci', 'Cs', 'Cnv', 'Dn', 'Dnh', 'Dnd', 'Td', 'O', 'Oh', 'I', 'Ih']
parser.add_argument("-lm","--lmax", type=int, default=4, help='Maximum l, default=4.')
parser.add_argument("-lp","--lmaxPlot", type=int, default=2, help='Maximum l for plotting only, default=2 (not used directly in script).')
parser.add_argument("-pc","--phaseConvention", type=str, default='S', help='Phase convention for basis set generation, default="S" (standard).')
args = parser.parse_args()

# Set args
sym = args.sym
lmax= args.lmax
lmaxPlot = args.lmaxPlot  # Set lmaxPlot for subselection on plots later.
phaseConvention=args.phaseConvention

# Compute harmonics
print('*** Setting up basis set for symmetry-defined matrix elements, see Quantum Metrology Vol. 3 Sect. 3.3...\n')

print(f"Set symmetry={sym}, lmax={lmax}")


# TODO: consider different labelling here, can set at init e.g. dims = ['C', 'h', 'muX', 'l', 'm'] - 25/11/22 code currently fails for mu mapping, remap below instead
symObj = symHarm(sym,lmax)
# symObj = symHarm(sym,lmax,dims = ['Cont', 'h', 'muX', 'l', 'm'])

# To plot using ePSproc/PEMtk class, these values can be converted to ePSproc BLM data type...

# Run conversion - the default is to set the coeffs to the 'BLM' data type
dimMap = {'C':'Cont','mu':'muX'}
symObj.toePSproc(dimMap=dimMap)

# Run conversion with a different dimMap & dataType
dataType = 'matE'
# symObj.toePSproc(dimMap = {'C':'Cont','h':'it', 'mu':'muX'}, dataType=dataType)
symObj.toePSproc(dimMap = dimMap, dataType=dataType)
# symObj.toePSproc(dimMap = {'C':'Cont','h':'it'}, dataType=dataType)   # Drop mu > muX mapping for now
# symObj.coeffs[dataType]

# Example using data class (setup in init script)
data = pemtkFit()

# Set to new key in data class
dataKey = sym
data.data[dataKey] = {}

for dataType in ['matE','BLM']:
    
    
    # Special cases...
    if sym=='D2h':
        data.data[dataKey][dataType] = symObj.coeffs[dataType]['b (comp)'].sum(['h','muX'])  # Select expansion in complex harmonics, and sum redundant dims
    
    # General case
    else:
        data.data[dataKey][dataType] = symObj.coeffs[dataType]['b (comp)']
    
    data.data[dataKey][dataType].attrs = symObj.coeffs[dataType].attrs

    


# *** Compute basis functions for given matrix elements
# Updated 27/07/23 - now includes symmetry selection routines for matrix elements.
#                    If missing, get null BLMs, but can fix manually by setting mu
#                    e.g. data.data[data.subKey]['matE']['mu']=[0] 

# For matrix elements, some other terms are required
# To assign specific terms, use self.assignMissingSym
# Note this can take a single value, or a list which must match the size of the Sym multiindex defined in the Xarray dataset.
print('*** Assigning matrix elements and computing betas...')

sNeutral = 'A1g'
sIonSG = 'A1g'

print(f'Set channels neutral sym={sNeutral}, ion sym={sIonSG}')

symObj.directProductContinuum([sNeutral, sIonSG])
symObj.assignMissingSym('Targ', sIonSG)

# To define terms from produts, use self.assignMissingSymProd
symObj.assignMissingSymProd()

# To attempt to assign mu values (by symmetry), use self.assignSymMuTerms()
symObj.assignSymMuTerms()

# Show Pandas table of results
display(symObj.coeffs['symAllowed']['PD'].fillna(''))

# Set data
matEkey = 'symAllowed'
dataType = 'matE'
data.data[matEkey] = {}
data.data[matEkey][dataType] = symObj.coeffs['symAllowed']['XR']['b (comp)']
data.subKey = matEkey

# Using PEMtk - this only returns the product basis set as used for fitting
BetaNormX, basisProduct = data.afblmMatEfit(selDims={}, sqThres=False, thres=None,phaseConvention=phaseConvention)
BetaNorm = BetaNormX  # Set alias

# 19/07/23 - removed this part as throwing errors in new build. Not sure why, seems to be key issue?
# Working OK in tensor demo notebook however?
# Using ePSproc directly - this includes full basis return if specified
# BetaNormX2, basisFull = ep.geomFunc.afblmXprod(data.data[data.subKey]['matE'], basisReturn = 'Full', selDims={}, sqThres=False)  #, BLMRenorm = BLMRenorm, **kwargs)
# BetaNorm2 = BetaNormX2  # Set alias

# # The basis dictionary contains various numerical parameters, these are investigated below.
# # See also the ePSproc docs at https://epsproc.readthedocs.io/en/latest/methods/geometric_method_dev_260220_090420_tidy.html
# print(f"Product basis elements: {basisProduct.keys()}")
# print(f"Full basis elements: {basisFull.keys()}")

# # Use full basis for following sections
# basis = basisFull

# 20/07/23 - working version, needed thres=None? Must have been change in defaults that caused the issue
# Using ePSproc directly - this includes full basis return if specified
# See the docs for more details, https://epsproc.readthedocs.io
# 21/07/23 - reinstated phaseConvention
BetaNormX2, basisFull = ep.geomFunc.afblmXprod(data.data[data.subKey]['matE'], 
                                               basisReturn = 'Full', 
                                               thres=None, selDims={}, sqThres=False,
                                               phaseConvention=phaseConvention)

# The basis dictionary contains various numerical parameters, these are investigated below.
# See also the ePSproc docs at https://epsproc.readthedocs.io/en/latest/methods/geometric_method_dev_260220_090420_tidy.html
print(f"Product basis elements: {basisProduct.keys()}")
print(f"Full basis elements: {basisFull.keys()}")

# Use full basis for following sections
basis = basisFull

#*** Compute results for aligned case with test ADMs
# Set ADMs for increasing alignment (linear ramp)...
print("\n*** Setting trial results for linear ramp ADMs.")
tPoints = 10
inputADMs = [[0,0,0, *np.ones(tPoints)],     # * np.sqrt(4*np.pi)],  # Optional multiplier for normalisation
             [2,0,0, *np.linspace(0,1,tPoints)], 
             [4,0,0, *np.linspace(0,0.5,tPoints)],
             [6,0,0, *np.linspace(0,0.3,tPoints)],
             [8,0,0, *np.linspace(0,0.2,tPoints)]]

# AKQS = ep.setADMs(ADMs = inputADMs)  # TODO WRAP TO CLASS (IF NOT ALREADY!)

# Set data - set example ADMs to data structure & subset for calculation
data.setADMs(ADMs = inputADMs)
data.setSubset(dataKey = 'ADM', dataType = 'ADM')

print('Computing BLMs for linear ramp case...')
# Using PEMtk - this only returns the product basis set as used for fitting
# TODO: add names/notes to returned Xarrays
BetaNormLinearADMs, basisProductLinearADMs = data.afblmMatEfit(selDims={}, sqThres=False, phaseConvention=phaseConvention)
