---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.4
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

+++ {"tags": ["remove-cell"]}

Subsection for density matrix stuff
31/01/23

- Moved here from tensor formalism page to try and fix rendering issues. Also added setup stuff to replicate basis sets in that notebook. UPDATE: currently is working in HTML, but sometimes a bit flaky and appears/disappears on reload - issues with pulling display scripts?

- Also promoted to top-level section (not nested under tensor stuff) for generality.

- For additional rendering tests, see http://jake:9966/lab/tree/QM3/doc-source/tests/holoviews_render_tests_310123.ipynb

% 30/01/23 extended with notes from MF recon article.
% 10/02/23 added general intro & tidying up

+++ {"tags": []}

(sec:density-mat-basic)=
# Density matrix representation

+++

(sec:density-mat-intro)=
## General introduction

The general density operator, for a mixture of independent states $|\psi_{n} \rangle$, can be defined as (Eqn. 2.8 in Blum, Ref. {cite}`BlumDensityMat` [^blumFootnote]):

$$
\hat{\rho}=\sum_{n}W_{n}|\psi_{n}\rangle\langle\psi_{n}|
$$

Where $W_{n}$ defines the (statistical) weighting of each state $\psi_{n}$ in the mixture.

% Removed \boldsymbol{\rho} due to HTML rendering issues.

For a given basis set, $|\phi_{m}\rangle$, the states can be expanded and the matrix elements of $\rho$ defined (Eqns. 2.9 - 2.11 in Blum, Ref. {cite}`BlumDensityMat` [^blumFootnote]):

$$
| \psi_{n} \rangle = \sum_{m'} a_{m'}^{(n)}| \phi_{m'}\rangle
$$

$$
\hat{\rho}=\sum_{n}\sum_{mm'}W_{n}a_{m'}^{(n)}a_{m}^{(n)*}|\phi_{m'}\rangle\langle\phi_{m}|
$$  (eqn:density-mat-outer-prod)

And the matrix elements - _the density matrix_ - given explicitly as:

$$
\rho_{i,j}=\langle\phi_{i}|\hat{\rho}|\phi_{j}\rangle=\sum_{n}W_{n}a_{i}^{(n)}a_{j}^{(n)*}
$$ (eqn:density-mat-generic)

For all pairs of basis states $(i,j)$. This defines the density matrix in the $\{|\phi_n\rangle\}$ _representation_ (basis space). Of particular note here is that the mixed states are assumed to be incoherent (independent), whilst the basis expansion is coherent. 


[^blumFootnote]: For general discussion of density matrix techniques and applications in AMO physics, see Blum's textbook `Density Matrix Theory and Applications` {cite}`BlumDensityMat`, which is referred to extensively herein.

+++ {"tags": []}

% TODO: numerical examples here
% TODO: decide on notation, \Psi_c == \mathbf{k}?
% 30/01/23 extended with notes from MF recon article.
% 10/02/23 added general intro & tidying up

(sec:density-mat-intro)=
## Continuum density matrices

% May want to move to Sect. 3.2 and add some more details?
In general, the discussion herein will focus on the photoelectron properties and generally assume a single final ion, and associated free-electron state of interest, hence the final state (Eq. {eq}`eq:continuum-state-vec`) can be simplified to $|\Psi_f\rangle\equiv|\mathbf{k}\rangle$. This is equivalent to a "pure state" in density matrix terminology, which can then expanded (coherently) in an appropriate representation (basis). Following this, the density operator associated with the continuum state can be written as $\hat{\rho}=|\Psi_f\rangle\langle\Psi_f|\equiv|\mathbf{k}\rangle\langle\mathbf{k}|$. Making use of the tensor notation introduced in {numref}`Sect. %s <sec:tensor-formulation>`, the final continuum state can then be expanded as a density matrix in the $\zeta\zeta'$ representation (with the observable dimensions $\{L,M\}$ explicitly included in the density matrix), which will also be dependent on the choice of channel functions ($u$), can then be given as:

$$
{\rho}_{L,M}^{u,\zeta\zeta'}=\varUpsilon_{L,M}^{u,\zeta\zeta'}\mathbb{I}^{\zeta,\zeta'}
$$ (eqn:full-density-mat)

Here the density matrix can be interpreted as the final, LF/AF or MF density matrix (depending on the channel functions used), incorporating both the intrinsic and extrinsic effects (i.e. all channel couplings and radial matrix elements for the given measurement), with dimensions dependent on the unique sets of quantum numbers required - in the simplest case, this will just be a set of partial waves $\zeta = \{l,m\}$. 

In the channel function basis, a radial, or reduced, form of the density matrix can also be constructed, and is given by the coherent product of the radial matrix elements (as defined in Eq. {eq}`eqn:I-zeta`):

% Safe version - no bold
$$
\rho^{\zeta\zeta'} = \mathbb{I}^{\zeta,\zeta'}
$$ (eqn:radial-density-mat)

This form encodes purely intrinsic (molecular scattering) photoionization dynamics (thus characterises the scattering event), whilst the full form ${\rho}_{L,M}^{u,\zeta\zeta'}$ of Eq. {eq}`eqn:full-density-mat` includes any additional effects incorporated via the channel functions. For reconstruction problems, it is usually the reduced form of Eq. {eq}`eqn:radial-density-mat` that is of interest, since the remainder of the problem is already described analytically by the channel functions $\varUpsilon_{L,M}^{u,\zeta\zeta'}$. In other words, the retrieval of the radial matrix elements $\mathbb{I}^{\zeta,\zeta'}$ and the radial density matrix $\rho^{\zeta\zeta'}$ are equivalent, and both can be viewed as completely describing the photoionization dynamics.

The $L,M$ notation for the full density matrix ${\rho}_{L,M}^{u,\zeta\zeta'}$ (Eq. {eq}`eqn:full-density-mat`) indicates here that these dimensions should not be summed over, hence the tensor coupling into the $\beta_{L,M}^{u}$ parameters can also be written directly in terms of the density matrix (cf. Eq. {eq}`eqn:channel-fns`):

$$
\beta_{L,M}^{u}=\sum_{\zeta,\zeta'}{\rho}_{L,M}^{u,\zeta\zeta'}
$$ (eqn:beta-density-mat)

In fact, this form arises naturally since the $\beta_{L,M}^{u}$ terms are the state multipoles (geometric tensors) defining the system, which can be thought of as a coupled basis equivalent of the density matrix representations (see, e.g., Ref. {cite}`BlumDensityMat`, Chpt. 4.).

In a more traditional notation (following Eq. {eq}`eq:continuum-state-vec`, see also Ref. {cite}`gregory2022LaboratoryFrameDensitya`), the density operator can be expressed as:

$$
\rho(t) =\sum_{LM}\sum_{KQS}A^{K}_{QS}(t)\sum_{\zeta\zeta^{\prime}}\varUpsilon_{L,M}^{u,\zeta\zeta'}|\zeta,\Psi_+\rangle\langle\zeta,\Psi_+|\mu_q\rho_i\mu_{q\prime}^{*}|\zeta^{\prime},\Psi_+\rangle\langle\zeta^{\prime},\Psi_+|
$$ (eqn:full-density-mat-traditional)

with $\rho_i = |\Psi_i\rangle\langle\Psi_i|$. This is, effectively, equivalent to an expansion in the various tensor operators defined in the channel function notation above (Eq. {eq}`eqn:full-density-mat`), but in a standard state-vector notation. Note, also, that this form explicitly defines the initial state of the system as a density matrix $\rho_i$, and explicitly allows for time-dependence via the {{ ADMsymbol }} term. (For further discussion of the use of density matrices in other specific cases, see {{ QM1 }}, particularly Chpts. 2 & 3, and refs. therein.)

The main benefit of a (continuum) density matrix representation in the current work is as a rapid way to visualize the phase relations between the photoionization matrix elements (the off-diagonal density matrix elements), and the ability to quickly check the overall pattern of the elements, hence confirm that no phase-relations are missing and orthogonality relations are fulfilled - some numerical examples are given below. Since the method for computing the density matrices is also numerically equivalent to a tensor outer-product, density matrices and visualizations can also be rapidly composed for other properties of interest, e.g. the various channel functions defined herein, providing another complementary methodology and tool for investigation. (Further examples can be found in the {{ ePSproc_docs }}, as well as in the literature, see, e.g., Ref. {cite}`BlumDensityMat` for general discussion, Ref. {cite}`Reid1991` for application in pump-probe schemes.) 

Furthermore, as noted above, the density matrix elements provide a complete description of the photoionization event, and hence make clear the equivalence of the "complete" photoionization experiments (and associated continuum reconstruction methods) discussed herein, with general quantum tomography schemes {cite}`MauroDAriano2003`. The density matrix can also be used as the starting point for further analysis based on standard density matrix techniques - this is discussed, for instance, in Ref. {cite}`BlumDensityMat`, and can also be viewed as a bridge between traditional methods in spectroscopy and AMO physics, and more recent concepts in the quantum information sciences (see, e.g., Refs. {cite}`Tichy2011a,Yuen-Zhou2014` for recent discussions in this context).

+++ {"tags": []}

## Numerical setup

This follows the setup in {numref}`Sect. %s <sec:tensor-formulation>` {ref}`sec:tensor-formulation`, using a symmetry-based set of basis functions for demonstration purposes. (Repeated code is hidden in PDF version.)

```{code-cell} ipython3
:tags: [hide-cell]

# Run default config - may need to set full path here
%run '../scripts/setup_notebook.py'

# Override plotters backend?
# plotBackend = 'pl'
```

```{code-cell} ipython3
:tags: [hide-cell]

# Setup symmetry-defined matrix elements using PEMtk

# Import class
from pemtk.sym.symHarm import symHarm

# Compute hamronics for Td, lmax=4
sym = 'D2h'
lmax=4

lmaxPlot = 2  # Set lmaxPlot for subselection on plots later.

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
```

```{code-cell} ipython3
:tags: [remove-cell]

# # Compute basis functions for given matrix elements

# # Set data
# data.subKey = dataKey

# # Using PEMtk - this only returns the product basis set as used for fitting
# BetaNormX, basisProduct = data.afblmMatEfit(selDims={}, sqThres=False)

# # Using ePSproc directly - this includes full basis return if specified
# BetaNormX2, basisFull = ep.geomFunc.afblmXprod(data.data[data.subKey]['matE'], basisReturn = 'Full', selDims={}, sqThres=False)  #, BLMRenorm = BLMRenorm, **kwargs)

# # The basis dictionary contains various numerical parameters, these are investigated below.
# # See also the ePSproc docs at https://epsproc.readthedocs.io/en/latest/methods/geometric_method_dev_260220_090420_tidy.html
# print(f"Product basis elements: {basisProduct.keys()}")
# print(f"Full basis elements: {basisFull.keys()}")

# # Use full basis for following sections
# basis = basisFull
```

## Compute a density matrix

A basic density matrix computation routine is implemented in the {{ ePSproc_full }}. This makes use of input tensor arrays, and computes the density matrix as an outer-product of the defined dimension(s). The numerics essentially compute the outer product from the specified dimensions, which can be written generally as per Eqns. {eq}`eqn:density-mat-outer-prod`, {eq}`eqn:density-mat-generic`, where $a_{i}^{(n)}a_{j}^{(n)*}$ are the values along the specified dimensions/state vector/representation. These dimensions must be in input arrays, but will be restacked as necessary to define the effective basis space. For instance, from the ionization matrix element demonstrated herein, setting `[l,m]` would select the $|\zeta\rangle = |l,m\rangle$ basis (equivalently `LM`, since the dimensions are already stacked in the ionization matrix elements). Setting `['LM','mu']` would set the $|\zeta\rangle = |l,m,\mu\rangle$ as the basis vector and so forth, where $|\zeta\rangle$ is used as a generic state vector denoting all required quantum numbers.

Note, however, that this selection is purely based on the numerics, which compute the outer product $|\zeta\rangle\langle\zeta'|$ to form the density matrix, hence does not guarantee a well-formed density matrix in the strictest sense (depending on the basis set), although will always present a basis state correlation matrix of sorts. A brief example, for the {glue:text}`symHarmPGmatE` defined matrix element is given below; for more examples see the {{ ePSproc_docs }}.

```{code-cell} ipython3
:tags: [hide-output]

# DEMO CODE FROM http://jake/jupyter/user/paul/doc/tree/code-share/stimpy-docker-local/MFPADs_recon_manuscript_dev_April_2022/MFrecon_manuscript_fig_generation_170422-Stimpy_MAIN-oldPkgs.ipynb
# SEE ALSO DOCS, https://epsproc.readthedocs.io/en/dev/methods/density_mat_notes_demo_300821.html#Density-Matrices

# Import routines
from epsproc.calc import density

# Compose density matrix

# Set dimensions/state vector/representation
# These must be in original data, but will be restacked as necessary to define the effective basis space.
denDims = 'LM'  #, 'mu']
selDims = None  #{'Type':'L'}
pTypes=['r','i']
thres = 1e-4    # 0.2 # Threshold out l>3 terms if using full 'orb5' set.
normME = False
normDen = 'max'

# Calculate - Ref case
# matE = data.data['subset']['matE']
# Set data from master class
# k = 'orb5'  # N2 orb5 (SG) dataset
# k = 'subset'
k = sym
matE = data.data[k]['matE'].copy()
if normME:
    matE = matE/matE.max()

daOut, *_ = density.densityCalc(matE, denDims = denDims, selDims = selDims, thres = thres)  # OK

if normDen=='max':
    daOut = daOut/daOut.max()
elif normDen=='trace':
    daOut = daOut/(daOut.sum('Sym').pipe(np.trace)**2)  # Need sym sum here to get 2D trace
    
# daPlot = density.matPlot(daOut.sum('Sym'))
daPlot = density.matPlot(daOut.sum('Sym'), pTypes=pTypes)

# Glue figure for later - real part only in this case
glue("denMatD2hRealOnly", daPlot.select(pType='Real'))
```

```{glue:figure} denMatD2hRealOnly
---
name: "fig-denMatD2hRealOnly"
---
Example density matrix, computed from matrix elements defined purely by {glue:text}`symHarmPGmatE` symmetry. Note in this case only the real part is non-zero.
```

+++

## Visualising matrix element reconstruction fidelity with density matrices

To demonstrate the use of the density matrix representation as a means to test similarity or fidelity between two sets of matrix elements, a trial set of matrix elements can be derived from the original set used above, plus random noise, and the differences in the density matrices directly computed. An example is shown in {numref}`fig-denMatD2hCompExample`; in this example 10\% noise has been added to the original (input) matrix elements, and the resultant density matrix computed. The difference matrix ({numref}`fig-denMatD2hCompExample`(c)) then provides the fidelity between the original and noisy case. In testing reconstructions, this type of analysis thus provides a quick means to test reconstruction results vs. known inputs. Although this case is only illustrated for real density matrices, a similar analysis can be used for the imaginary (or phase) components, thus coherences can also be quickly visualised in this manner.

% TODO: ref later sections here, and/or MF recon manuscript, Sect 4.1.5 & Fig 11.

```{code-cell} ipython3
:tags: [hide-output]

# Trial matrix element for comparison
matE = data.data[k]['matE'].copy()

# Add random noise, +/- 5%
matE = matE + matE*(np.random.rand(*list(matE.shape)) - 0.5) * 0.2

if normME:
    matE = matE/matE.max()

daOut2, *_ = density.densityCalc(matE, denDims = denDims, selDims = selDims, thres = thres)  # OK

if normDen=='max':
    daOut2 = daOut2/daOut2.max()
elif normDen=='trace':
    daOut2 = daOut2/(daOut2.sum('Sym').pipe(np.trace)**2)
    
daPlot2 = density.matPlot(daOut2.sum('Sym'), pTypes=pTypes)   #.sel(Eke=slice(0.5,1.5,1)))


# Compute difference
daDiff = daOut.sum('Sym') - daOut2.sum('Sym')
daDiff.name = 'Difference'
daPlotDiff = density.matPlot(daDiff, pTypes=pTypes)

# #******** Plot
# daLayout = (daPlot.layout('pType') + daPlot2.opts(show_title=False).layout('pType').opts(show_title=False) + daPlotDiff.opts(show_title=False).layout('pType')).cols(1)  # No cols? AH - set to 1 works.
# daLayout = (daPlot.select(pType='Real') + daPlot2.opts(show_title=False).select(pType='Real').opts(show_title=False) + daPlotDiff.opts(show_title=False).select(pType='Real')).cols(1)  # No cols? AH - set to 1 works.
# daLayout.opts(width=300, height=300)  # Doesn't work?
# daLayout.opts(hv.opts.HeatMap(width=300, frame_width=300, aspect='square', tools=['hover'], colorbar=True, cmap='coolwarm'))  # .opts(show_title=False)  # .opts(title="Custom Title")  #OK

# Additional formatting options for PDF vs. HTML outputs.
# TODO: improve/set global options + label figures.
nCols = 1
try:
    if buildEnv == 'pdf':
        nCols = 2
except:
    pass

# Layout for real parts, with custom titles.
daLayout = (daPlot.select(pType='Real').opts(title="(a) Original") + daPlot2.select(pType='Real').opts(title="(b) With noise") 
            + daPlotDiff.select(pType='Real').opts(title="(c) Difference (fidelity)")).cols(nCols)  # No cols? AH - set to 1 works.

# Glue layout
glue("denMatD2hCompExample",daLayout.opts(hv.opts.HeatMap(aspect='square', tools=['hover'], colorbar=True, cmap='coolwarm')))
```

```{code-cell} ipython3
:tags: [remove-cell]

daLayout
```

```{glue:figure} denMatD2hCompExample
---
name: "fig-denMatD2hCompExample"
---
Example density matrices, computed from matrix elements defined purely by {glue:text}`symHarmPGmatE` symmetry. Here the panels show (a) the original density matrix, (b) values with +/- 10% random noise, (c) the difference matrix, which indicates the fidelity of the noisy state relative to the original matrix elements.
```

```{code-cell} ipython3
!date
```

+++ {"tags": ["remove-cell"]}

## SCRATCH

```{code-cell} ipython3
:tags: [remove-cell]

type(daPlot)
```

```{code-cell} ipython3
:tags: [remove-cell]

isinstance(daPlot, hv.core.spaces.HoloMap)
```

```{code-cell} ipython3
:tags: [remove-cell]

isinstance(daPlot, hv.core.spaces)
```

```{code-cell} ipython3
:tags: [remove-cell]

type(daPlot.select(pType='Real'))
```

```{code-cell} ipython3
:tags: [remove-cell]

'holoviews' in str(type(daPlot.select(pType='Real')))
```

```{code-cell} ipython3
:tags: [remove-cell]

type(glue)
```

```{code-cell} ipython3
:tags: [remove-cell]

def superglue(func):
    '''Decorator for glue() with interactive plot types forced to static for PDF builds.'''
    
    def glueWrapper(name,fig,**kwargs):
        
        # Set names for file out
        # Note imgFormat and imgPath should be set globally, or passed as kwargs.
        imgFile = f'{name}.{imgFormat}'
        imgFile = os.path.join(imgPath,imgFile)
        
        # Set glue() output according to fig type and build env.
        # Note buildEnv should be set globally, or passed as a kwarg.
        if buildEnv != 'pdf':
            return func(name, fig, display=False)  # For non-PDF builds, use regular glue()
        
        else:
            # Holoviews object
            # Note for Bokeh backend may need additional pkgs, selenium, firefox and geckodriver
            # See https://holoviews.org/user_guide/Plots_and_Renderers.html#saving-and-rendering
            if 'holoviews' in str(type(fig)):
                # Force render and glue
                hv.save(fig, imgFile, fmt=imgFormat)
                
            elif 'plotly' in str(type(fig)):
                fig.write_image(imgFile,format=imgFormat)  # See https://plotly.com/python/static-image-export/
                
            
            # Glue static render
            return func(name, Image(imgFile), display=False)
        
        
    return glueWrapper
```

```{code-cell} ipython3
:tags: [remove-cell]

glue = superglue(glue)
```

```{code-cell} ipython3
:tags: [remove-cell]

glue("glueTestDec", daPlot)
```

+++ {"tags": ["remove-cell"]}

```{glue:figure} glueTestDec
---
name: "fig-glueTestDec"
---
Raw output to glue decorated with superglue().
```

```{code-cell} ipython3
:tags: [remove-cell]

# Quick decorator example from https://www.geeksforgeeks.org/function-wrappers-in-python/

import time


def timeis(func):
	'''Decorator that reports the execution time.'''

	def wrap(*args, **kwargs):
		start = time.time()
		result = func(*args, **kwargs)
		end = time.time()
		
		print(func.__name__, end-start)
		return result
	return wrap

@timeis
def countdown(n):
	'''Counts down'''
	while n > 0:
		n -= 1

countdown(5)
countdown(1000)
```

```{code-cell} ipython3
:tags: [remove-cell]

hv.core.options.Store.loaded_backends()
```

```{code-cell} ipython3
:tags: [remove-cell]

daLayout = (daPlot.layout('pType')).cols(1)
```

```{code-cell} ipython3
:tags: [remove-cell]

type(daLayout)
```

```{code-cell} ipython3
:tags: [remove-cell]

print(daLayout)
```