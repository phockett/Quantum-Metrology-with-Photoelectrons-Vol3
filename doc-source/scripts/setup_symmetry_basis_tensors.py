# Setup symmetry-defined matrix elements using PEMtk

# Basic routine for Quantum Metrology Vol. 3 demo case.
# See Sect. 3.3 for further notes

# Imports
import epsproc as ep
import numpy as np

# Import classes
from pemtk.fit.fitClass import pemtkFit
from pemtk.sym.symHarm import symHarm

# 13/04/23: updated to use argparse for multiple arg passing
# Note this keeps default case to match previous hard-coded symmetry (Td).
import argparse

parser = argparse.ArgumentParser(description='Setup symmetrized harmonics and basis functions. Default case runs for sym=D2h, lmax=4, lmaxPlot=2.')
parser.add_argument("--sym", type=str, default='D2h', help="Symmetry to use, default=D2h. Allowed cases: ['Ci', 'Cs', 'Cnv', 'Dn', 'Dnh', 'Dnd', 'Td', 'O', 'Oh', 'I', 'Ih']")
# Can set choices to list, but will need to subs all n?
# For allowed cases, see https://pemtk.readthedocs.io/en/latest/sym/pemtk_symHarm_demo_160322_tidy.html#Create-class-&-compute-harmonics
# choices=['Ci', 'Cs', 'Cnv', 'Dn', 'Dnh', 'Dnd', 'Td', 'O', 'Oh', 'I', 'Ih']
parser.add_argument("--lmax", type=int, default=4, help='Maximum l, default=4.')
parser.add_argument("--lmaxPlot", type=int, default=2, help='Maximum l for plotting only, default=2 (not used directly in script).')
args = parser.parse_args()

# Set args
sym = args.sym
lmax= args.lmax
lmaxPlot = args.lmaxPlot  # Set lmaxPlot for subselection on plots later.

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
    data.data[dataKey][dataType] = symObj.coeffs[dataType]['b (comp)'].sum(['h','muX'])  # Select expansion in complex harmonics, and sum redundant dims
    data.data[dataKey][dataType].attrs = symObj.coeffs[dataType].attrs
    
    
    
    
#*** Compute basis functions for given matrix elements

# Set data
data.subKey = dataKey

# Using PEMtk - this only returns the product basis set as used for fitting
BetaNormX, basisProduct = data.afblmMatEfit(selDims={}, sqThres=False)
BetaNorm = BetaNormX  # Set alias

# Using ePSproc directly - this includes full basis return if specified
BetaNormX2, basisFull = ep.geomFunc.afblmXprod(data.data[data.subKey]['matE'], basisReturn = 'Full', selDims={}, sqThres=False)  #, BLMRenorm = BLMRenorm, **kwargs)
BetaNorm2 = BetaNormX2  # Set alias

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

# Using PEMtk - this only returns the product basis set as used for fitting
# TODO: add names/notes to returned Xarrays
BetaNormLinearADMs, basisProductLinearADMs = data.afblmMatEfit(selDims={}, sqThres=False)