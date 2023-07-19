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

Subsection for density matrix stuff
31/01/23

- Moved here from tensor formalism page to try and fix rendering issues. Also added setup stuff to replicate basis sets in that notebook. UPDATE: currently is working in HTML, but sometimes a bit flaky and appears/disappears on reload - issues with pulling display scripts?

- Also promoted to top-level section (not nested under tensor stuff) for generality.

- For additional rendering tests, see http://jake:9966/lab/tree/QM3/doc-source/tests/holoviews_render_tests_310123.ipynb

- Working from Density matrix ePSproc notes, http://jake:9966/lab/tree/code-share/github-share/ePSproc/docs/doc-source/methods/density_mat_notes_demo_300821.ipynb and MF recon article notes (Tex, and http://jake/jupyter/user/paul/doc/tree/code-share/stimpy-docker-local/MFPADs_recon_manuscript_dev_April_2022/MFrecon_manuscript_fig_generation_170422-Stimpy_MAIN-oldPkgs.ipynb, basis of demo code herein)

30/01/23 extended with notes from MF recon article.

10/02/23 added general intro & tidying up. Fixed some notation (may still need some work, and/or adding to photoionization intro part), and fidelity part. TODO: check numerics with noise make sense there.

19/07/23 reviewing with minor mods.

- Issue with sym setup script? Throwing some errors.
  - Now tidied in script (not required here), but should debug.
- Text OK and tidied up a bit, still some debug stuff to remove.

TODO:

- More on irreducible tensors vs. density mat? See Blum Chpt. 4 and Zare, also previous notes. SHould be able to add some theory and numerics here, maybe a subsection for this? Feels like there might be some interesting relations here...
   - L,M representation and diagonality? See p135 - although maybe obvious?
   - Rotation properties and complete basis, symmetries.
   - Sect 4.6.5 for spatial properties
   - Sect 4.8 for notation and conventions
   - Subspace projections as summations, reduced density matrices, p64
- Floor noise example to zero? Should be more physical than having -ve values allowed?
- See QuTip for more stuff, e.g. entropy and distance metrics, https://qutip.org/docs/latest/apidoc/functions.html#module-qutip.metrics. Should be able to use directly on numerical matrices?

+++

(sec:density-mat-basic)=
# Density matrix representation

+++

(sec:density-mat-intro)=
## General introduction

For a general introduction, and discussion of density matrix techniques and applications in AMO physics, see Blum's textbook _Density Matrix Theory and Applications_ {cite}`BlumDensityMat`, which is referred to extensively herein. The general density operator, for a mixture of independent states $|\psi_{n}\rangle$, can be defined as per Eqn. 2.8 in Blum {cite}`BlumDensityMat`:

$$
\hat{\rho}=\sum_{n}W_{n}|\psi_{n}\rangle\langle\psi_{n}|
$$

Where $W_{n}$ defines the (statistical) weighting of each state $\psi_{n}$ in the mixture.

% Removed \boldsymbol{\rho} due to HTML rendering issues.

For a given basis set, $|\phi_{m}\rangle$, the states can be expanded and the matrix elements of $\rho$ defined as per Eqns. 2.9 - 2.11 in Blum {cite}`BlumDensityMat`:

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


% [^blumFootnote]: For general discussion of density matrix techniques and applications in AMO physics, see Blum's textbook _Density Matrix Theory and Applications_ {cite}`BlumDensityMat`, which is referred to extensively herein.

+++

% TODO: numerical examples here
% TODO: decide on notation, \Psi_c == \mathbf{k}?
% 30/01/23 extended with notes from MF recon article.
% 10/02/23 added general intro & tidying up

(sec:density-mat-intro)=
## Continuum density matrices

% May want to move to Sect. 3.2 and add some more details?
In general, the discussion herein will focus on the photoelectron properties and generally assume a single final ion, and associated free-electron state of interest, hence the final state (Eq. {eq}`eq:continuum-state-vec`) can be simplified to $|\Psi_f\rangle\equiv|\mathbf{k}\rangle$. This is equivalent to a "pure state" in density matrix terminology, which can then expanded (coherently) in an appropriate representation (basis). Following this, the density operator associated with the continuum state can be written as $\hat{\rho}=|\Psi_f\rangle\langle\Psi_f|\equiv|\mathbf{k}\rangle\langle\mathbf{k}|$. Making use of the tensor notation introduced in {numref}`Sect. %s <sec:tensor-formulation>`, the final continuum state can then be expanded as a density matrix in the $\zeta\zeta'$ representation (with the observable dimensions $\{L,M\}$ explicitly included in the density matrix), which will also be dependent on the choice of {{ GAMMACHANNEL }} (hence "experiment" $u$); the density matrix can then be given as:

$$
{\rho}_{L,M}^{u,\zeta\zeta'}=\varUpsilon_{L,M}^{u,\zeta\zeta'}\mathbb{I}^{\zeta,\zeta'}
$$ (eqn:full-density-mat)

Here the density matrix can be interpreted as the final, {{ LF }}/{{ AF }} or {{ MF }} density matrix (depending on the {{ GAMMACHANNEL }} used), incorporating both the intrinsic and extrinsic effects (i.e. all channel couplings and radial matrix elements for the given measurement), with dimensions dependent on the unique sets of quantum numbers required - in the simplest case, this will just be a set of partial waves $\zeta = \{l,m\}$. 

In the channel function basis, a radial, or reduced, form of the density matrix can also be constructed, and is given by the coherent product of the radial matrix elements (as defined in Eq. {eq}`eqn:I-zeta`):

% Safe version - no bold
$$
\rho^{\zeta\zeta'} = \mathbb{I}^{\zeta,\zeta'}
$$ (eqn:radial-density-mat)

This form encodes purely intrinsic (molecular scattering) photoionization dynamics (thus characterises the scattering event), whilst the full form ${\rho}_{L,M}^{u,\zeta\zeta'}$ of Eq. {eq}`eqn:full-density-mat` includes any additional effects incorporated via the channel functions. For reconstruction problems, it is usually the reduced form of Eq. {eq}`eqn:radial-density-mat` that is of interest, since the remainder of the problem is already described analytically by the {{ GAMMACHANNEL }} $\varUpsilon_{L,M}^{u,\zeta\zeta'}$. In other words, the retrieval of the radial matrix elements $\mathbb{I}^{\zeta,\zeta'}$ and the radial density matrix $\rho^{\zeta\zeta'}$ are equivalent, and both can be viewed as completely describing the photoionization dynamics.

The $L,M$ notation for the full density matrix ${\rho}_{L,M}^{u,\zeta\zeta'}$ (Eq. {eq}`eqn:full-density-mat`) indicates here that these dimensions should not be summed over, hence the tensor coupling into the $\beta_{L,M}^{u}$ parameters can also be written directly in terms of the density matrix (cf. Eq. {eq}`eqn:channel-fns`):

$$
\beta_{L,M}^{u}=\sum_{\zeta,\zeta'}{\rho}_{L,M}^{u,\zeta\zeta'}
$$ (eqn:beta-density-mat)

In fact, this form arises naturally since the $\beta_{L,M}^{u}$ terms are the state multipoles (geometric tensors) defining the system, which can be thought of as a coupled basis equivalent of the density matrix representations (see, e.g., Ref. {cite}`BlumDensityMat`, Chpt. 4.).

In a more traditional notation (following Eq. {eq}`eq:continuum-state-vec`, see also Ref. {cite}`gregory2022LaboratoryFrameDensitya`), the density operator can be expressed as:

$$
\rho(t) =\sum_{LM}\sum_{KQS}A^{K}_{QS}(t)\sum_{\zeta\zeta^{\prime}}\varUpsilon_{L,M}^{u,\zeta\zeta'}|\zeta,\Psi_+\rangle\langle\zeta,\Psi_+|\mu_q\rho_i\mu_{q\prime}^{*}|\zeta^{\prime},\Psi_+\rangle\langle\zeta^{\prime},\Psi_+|
$$ (eqn:full-density-mat-traditional)

This is, effectively, equivalent to an expansion in the various tensor operators defined in the channel function notation above (Eq. {eq}`eqn:full-density-mat`), but in a standard state-vector notation. Note, also, that this form explicitly defines the initial state of the system as a density matrix $\rho_i = |\Psi_i\rangle\langle\Psi_i|$, and explicitly allows for time-dependence via the {{ ADMsymbol }} term. (For further discussion of the use of density matrices in other specific cases, see {{ QM1 }}, particularly Chpts. 2 & 3, and refs. therein.)

The main benefit of a (continuum) density matrix representation in the current work is as a rapid way to visualize the phase relations between the photoionization matrix elements (the off-diagonal density matrix elements), and the ability to quickly check the overall pattern of the elements, hence confirm that no phase-relations are missing and orthogonality relations are fulfilled - some numerical examples are given below. Since the method for computing the density matrices is also numerically equivalent to a tensor outer-product, density matrices and visualizations can also be rapidly composed for other properties of interest, e.g. the various {{ GAMMACHANNEL }} defined herein, providing another complementary methodology and tool for investigation. (Further examples can be found in the {{ ePSproc_docs }}, as well as in the literature, see, e.g., Ref. {cite}`BlumDensityMat` for general discussion, Ref. {cite}`Reid1991` for application in pump-probe schemes.) 

Furthermore, as noted above, the density matrix elements provide a complete description of the photoionization event, and hence make clear the equivalence of the "complete" photoionization experiments (and associated continuum reconstruction methods) discussed herein, with general quantum tomography schemes {cite}`MauroDAriano2003`. The density matrix can also be used as the starting point for further analysis based on standard density matrix techniques - this is discussed, for instance, in Ref. {cite}`BlumDensityMat`, and can also be viewed as a bridge between traditional methods in spectroscopy and AMO physics, and more recent concepts in the quantum information sciences (see, e.g., Refs. {cite}`Tichy2011a,Yuen-Zhou2014` for recent discussions in this context). A brief numerical diversion in this direction is given in {numref}`Sect. %s <sect:theory:denmat:qutip>`, which illustrates the use of the {{ qutipFull }} with the density matrix results derived herein.

+++

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

%run '../scripts/setup_symmetry_basis_tensors.py'
```

```{code-cell} ipython3
:tags: [remove-cell]

# 19/07/23 - this needs debugging, but skipped for now!
# Not sure what has changed - might be issue with dim names?
# ep.geomFunc.afblmXprod(data.data[data.subKey]['matE'], basisReturn = 'Full', selDims={}, sqThres=False)
```

```{code-cell} ipython3
:tags: [remove-cell]

# Now run in script above

# # Setup symmetry-defined matrix elements using PEMtk

# # Import class
# from pemtk.sym.symHarm import symHarm

# # Compute hamronics for Td, lmax=4
# sym = 'D2h'
# lmax=4

# lmaxPlot = 2  # Set lmaxPlot for subselection on plots later.

# # TODO: consider different labelling here, can set at init e.g. dims = ['C', 'h', 'muX', 'l', 'm'] - 25/11/22 code currently fails for mu mapping, remap below instead
# symObj = symHarm(sym,lmax)
# # symObj = symHarm(sym,lmax,dims = ['Cont', 'h', 'muX', 'l', 'm'])

# # To plot using ePSproc/PEMtk class, these values can be converted to ePSproc BLM data type...

# # Run conversion - the default is to set the coeffs to the 'BLM' data type
# dimMap = {'C':'Cont','mu':'muX'}
# symObj.toePSproc(dimMap=dimMap)

# # Run conversion with a different dimMap & dataType
# dataType = 'matE'
# # symObj.toePSproc(dimMap = {'C':'Cont','h':'it', 'mu':'muX'}, dataType=dataType)
# symObj.toePSproc(dimMap = dimMap, dataType=dataType)
# # symObj.toePSproc(dimMap = {'C':'Cont','h':'it'}, dataType=dataType)   # Drop mu > muX mapping for now
# # symObj.coeffs[dataType]

# # Example using data class (setup in init script)
# data = pemtkFit()

# # Set to new key in data class
# dataKey = sym
# data.data[dataKey] = {}

# for dataType in ['matE','BLM']:
#     data.data[dataKey][dataType] = symObj.coeffs[dataType]['b (comp)'].sum(['h','muX'])  # Select expansion in complex harmonics, and sum redundant dims
#     data.data[dataKey][dataType].attrs = symObj.coeffs[dataType].attrs
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

A basic density matrix computation routine is implemented in the {{ ePSproc_full }}. This makes use of input tensor arrays, and computes the density matrix as an outer-product of the defined dimension(s). The numerics essentially compute the outer product from the specified dimensions, which can be written generally as per Eqs. {eq}`eqn:density-mat-outer-prod`, {eq}`eqn:density-mat-generic`, where $a_{i}^{(n)}a_{j}^{(n)*}$ are the values along the specified dimensions/state vector/representation. These dimensions must be in input arrays, but will be restacked as necessary to define the effective basis space, and all coherent pairs will be computed. 

For instance, considering the ionization matrix elements demonstrated herein, setting indexes (quantum numbers) as `[l,m]` will select the $|\zeta\rangle = |l,m\rangle$ basis, hence define the density operator as $\hat{\rho} = |\zeta\rangle \langle\zeta'| = |l,m\rangle\langle l',m'|$ and the corresponding density matrix elements $\rho^{\zeta,\zeta'}=\langle\zeta|\hat{\rho}|\zeta'\rangle=a_{l,m}a_{l',m'}^{*}$. Similarly, setting `['l','m','mu']` will set the $|\zeta\rangle = |l,m,\mu\rangle$ as the basis vector and so forth, where $|\zeta\rangle$ is used as a generic state vector denoting all required quantum numbers. Additionally, other quantum numbers/dimensions can be kept, summed or selected from the input tensors prior to computation, thus density matrices can be readily computed as a function of other parameters, or averaged, according to the properties of interest, experimental parameters and observables.

Note, however, that this selection is purely based on the numerics, which compute the outer product along the defined dimensions $|\zeta\rangle\langle\zeta'|$ to form the density matrix, hence does not guarantee a well-formed density matrix in the strictest sense (depending on the basis set), although will always present a basis state correlation matrix of sorts. A brief example, for the {glue:text}`symHarmPGmatE` defined matrix element is given below; for more examples see the {{ ePSproc_docs }}.

```{code-cell} ipython3
:tags: [hide-output]

# See the docs for more, 
# https://epsproc.readthedocs.io/en/dev/methods/density_mat_notes_demo_300821.html

# Import routines for density calculation and plotting
from epsproc.calc import density

#*** Compose density matrix

# Set dimensions/state vector/representation
# These must be in original data, but will be restacked as 
# necessary to define the effective basis space.

# Set dimensions for density matrix. Note stacked dims are OK, in this case LM = {l,m}
denDims = 'LM'  
selDims = None  # Select on any other dimensions?
sumDims = None  # Sum over any other dimensions? 
                # (Set sumDims=True to sum over all dims except denDims.)
pTypes=['r','i'] # Plotting types 'r'=real, 'i'=imaginary
thres = 1e-4    # Threshold for outputs (otherwise set to zero and/or dropped from result)
normME = False  # Normalise matrix elements before computing?
normDen = 'max' # Method to normalise density matrix

# Calculate - Ref case
k = sym
matE = data.data[k]['matE'].copy()  # Set data from main class instance by key

# Normalise input matrix elements?
if normME:
    matE = matE/matE.max()

#*** Compute density matrix for given parameters
# See demo at:
#   https://epsproc.readthedocs.io/en/latest/methods/density_mat_notes_demo_300821.html
# API docs:
#   https://epsproc.readthedocs.io/en/latest/modules/epsproc.calc.density.html#epsproc.calc.density.densityCalc
daOut, *_ = density.densityCalc(matE, denDims = denDims, selDims = selDims, thres = thres)

# Renormlise output?
if normDen=='max':
    daOut = daOut/daOut.max()
elif normDen=='trace':
    # Need sym sum here to get 2D trace
    daOut = daOut/(daOut.sum('Sym').pipe(np.trace)**2)  

# Plot density matrix with Holoviews
# Note sum over 'Sym' dimension to flatten plot to (l,m) dims only.
daPlot = density.matPlot(daOut.sum('Sym'), pTypes=pTypes)
```

```{code-cell} ipython3
:tags: [hide-output, hide-cell]

# Glue figure for later - real part only in this case
# Also clean up axis labels from default state labels ('LM' and 'LM_p' in this case).
glue("denMatD2hRealOnly", daPlot.select(pType='Real').opts(xlabel='L,M', ylabel="L',M'"))
```

```{glue:figure} denMatD2hRealOnly
---
name: "fig-denMatD2hRealOnly"
---
Example density matrix, computed from matrix elements defined purely by {glue:text}`symHarmPGmatE` symmetry. Note in this case only the real part is non-zero. Axes labels give terms $\{L,M\}$ and $\{L',M'\}$.
```

+++

## Visualising matrix element reconstruction fidelity with density matrices

To demonstrate the use of the density matrix representation as a means to test similarity or fidelity between two sets of matrix elements, a trial set of matrix elements can be derived from the original set used above, plus random noise, and the differences in the density matrices directly computed. An example is shown in {numref}`fig-denMatD2hCompExample`; in this example up to 10\% random noise has been added to the original (input) matrix elements, and the resultant density matrix computed. The difference matrix ({numref}`fig-denMatD2hCompExample`(c)) then provides the fidelity between the original and noisy case. In testing retrieval methodologies, this type of analysis thus provides a quick means to test reconstruction results vs. known inputs. Although this case is only illustrated for real density matrices, a similar analysis can be used for the imaginary (or phase) components, thus coherences can also be quickly visualised in this manner.

% TODO: ref later sections here, and/or MF recon manuscript, Sect 4.1.5 & Fig 11.

```{code-cell} ipython3
:tags: [hide-output]

#*** Set trial matrix element for comparison with the original case computed above
matE = data.data[k]['matE'].copy()

if normME:
    matE = matE/matE.max()
    
# Add random noise, +/- 10%
# Note this is applied to normalised matE
# For the normalised case this results in a standard deviation in the difference 
# density matrix elements of ~sqrt(2*(0.1^2) + 2*0.1) = 0.2
# (Derived from basic error propagation, ignoring the actual values - 
#  see https://en.wikipedia.org/wiki/Propagation_of_uncertainty#Example_formulae.)
noise = 0.1
SD = np.sqrt(4*(noise**2))
# Set range to random values +/-1 * noise
matE_noise = matE + matE*((np.random.rand(*list(matE.shape)) - 0.5) * 2*noise)  

# Compute density matrix
daOut_noise, *_ = density.densityCalc(matE_noise, denDims = denDims, selDims = selDims, thres = thres)

# Renormlise output?
if normDen=='max':
    daOut_noise = daOut_noise/daOut_noise.max()
elif normDen=='trace':
    daOut_noise = daOut_noise/(daOut_noise.sum('Sym').pipe(np.trace)**2)
    
daPlot_noise = density.matPlot(daOut_noise.sum('Sym'), pTypes=pTypes)

# Compute differences
daDiff = daOut.sum('Sym') - daOut_noise.sum('Sym')
daDiff.name = 'Difference'
daPlotDiff = density.matPlot(daDiff, pTypes=pTypes)

print(f'Noise = {noise}, SD (approx) = {SD}')
maxDiff = daDiff.max().values
print(f'Max difference = {maxDiff}')

#*** Layout plot from Holoviews objects for real parts, with custom titles.
daLayout = (daPlot.select(pType='Real').opts(title="(a) Original", xlabel='L,M', ylabel="L',M'") 
            + daPlot_noise.select(pType='Real').opts(title="(b) With noise", 
                xlabel='L,M', ylabel="L',M'") 
            + daPlotDiff.select(pType='Real').opts(title="(c) Difference (fidelity)", 
                xlabel='L,M', ylabel="L',M'"))
```

```{code-cell} ipython3
:tags: [hide-output, hide-cell]

# Glue plot

# Additional formatting options for PDF vs. HTML outputs.
nCols = 1
if buildEnv == 'pdf':
    nCols = 2

# Glue layout
glue("denMatD2hCompExample",daLayout.cols(nCols).opts(hv.opts.HeatMap(cmap='coolwarm')))

# Glue values
glue("denDiffMax",round(float(maxDiff.real),3))
glue("denSD",SD)
```

```{glue:figure} denMatD2hCompExample
---
name: "fig-denMatD2hCompExample"
---
Example density matrices, computed from matrix elements defined purely by {glue:text}`symHarmPGmatE` symmetry. Here the panels show (a) the original density matrix, (b) density matrix computed with +/- 10% random noise added to the original matrix elements, (c) the difference matrix, which indicates the fidelity of the noisy case relative to the original case. For normalised density matrices the 10% noise case translates to a standard deviation $\sigma\approx${glue:text}`denSD` on the differences; the maximum error in the test case as illustrated ={glue:text}`denDiffMax`.
```

+++

(sect:theory:denmat:qutip)=
## Working with density matrices with QuTiP library functions

From the numerical density matrix, a range of other standard properties can be computed - of particular interest are likely to be various standard quantities such as the trace, Von Neuman entropy and so forth. Naturally these can be computed numerically directly from the relevant formal definitions; however, many of the fundamentals are already implemented in other libraries, and numerical representations can be passed directly to such libraries. In particular, {{ qutipFull }} implements a range of standard functions, metrics, transforms and utility functions for working with state vectors and density matrices. A brief numerical example is given below, see {{ qutipDocs }} for more possibilities.

+++

### Convert numerical arrays to QuTiP objects

```{code-cell} ipython3
:tags: [hide-cell]

# Import QuTip
from qutip import *

# Wrap density matrices to QuTip objects
# Note sum('Sym') to ensure 2D matrix, and .data to pass Numpy data array only
pa = Qobj(daOut.sum('Sym').data)    # Reference continuum density matrix
pb = Qobj(daOut_noise.sum('Sym').data)  # Noisy case

# QuTip objects have data as Numpy arrays, and render as typeset matrices in a notebook
# DEBUG NOTE 22/04/23 - QuTip matrix latex output currently causing PDF build errors, so set hide output for testing.
# See https://github.com/phockett/Quantum-Metrology-with-Photoelectrons-Vol3/issues/8
pa
```

### Fidelity metric

Fidelity between two density matrices $\rho_{a},\rho_{b}$ can be defined as per Refs. {cite}`benatti2010QuantumInformationComputation, nielsen2010QuantumComputationQuantum`: 

$F(\rho_{a},\rho_{b})=\operatorname{Tr} {\sqrt {{\sqrt {\rho_{a}}}\rho_{b} {\sqrt {\rho_{a}}}}}$

This is implemented by the `fidelity` function in {{ qutipFull }}. Of note in this test case is that the resultant is close to limiting-case value of $F(\rho_{a},\rho_{b})=1$ for the test case herein, despite the added noise and some per-element disparities as shown in   {numref}`fig-denMatD2hCompExample`(c). This reflects the conceptual difference between an element-wise evaluation of the differences, vs. a formal scalar metric.

% $F(\rho,\sigma )=\left(\operatorname{tr} {\sqrt {{\sqrt {\rho }}\sigma {\sqrt {\rho }}}}\right)^{2}$
% Wiki defn. from https://en.wikipedia.org/wiki/Fidelity_of_quantum_states
% Cite nielsen2010QuantumComputationQuantum

```{code-cell} ipython3
# Test fidelity, =1 if trace-normalised
print(f"Fidelity (a,a) = {fidelity(pa,pa)}")
print(f"Trace = {pa.tr()}")
print(f"Trace-normed fidelity = {fidelity(pa,pa)/pa.tr()}")
```

```{code-cell} ipython3
# Test fidelity vs noisy case
print(f"Fidelity (a,b) = {fidelity(pa,pb)}")
print(f"Trace a = {pa.tr()}, Trace b = {pb.tr()}")
print(f"Trace-normed fidelity = {fidelity(pa/pa.tr(),pb/pb.tr())}")
```

```{code-cell} ipython3
# This can also be computed rapidly with lower-level QuTip functionality...

# Compute inner term, note .sqrtm() for square root.
inner = pa.sqrtm() * pa * pa.sqrtm()

# Compute fidelity
inner.sqrtm().tr()
```

+++ {"tags": ["remove-cell"]}

### Von Neuman entropy
% Not sure if this is interesting as yet... see S3.1 in benatti2010QuantumInformationComputation

```{code-cell} ipython3
:tags: [remove-cell]

entropy_vn(pa/pa.tr())
```

```{code-cell} ipython3
:tags: [remove-cell]

entropy_vn(pb/pb.tr())
```

```{code-cell} ipython3
:tags: [remove-cell]

entropy_vn(pa/pa.tr()) - entropy_vn(pb/pb.tr())
```

+++ {"tags": ["remove-cell"]}

### Relative entropy

% Not sure if this is interesting as yet... see S3.2 in benatti2010QuantumInformationComputation
% inf for (A,B) case here?

```{code-cell} ipython3
:tags: [remove-cell]

entropy_relative(pa/pa.tr(),pa/pa.tr())  # Indentical case = 0
```

```{code-cell} ipython3
:tags: [remove-cell]

entropy_relative(pa/pa.tr(),pb/pb.tr())
```

+++ {"tags": ["remove-cell"]}

## SCRATCH

```{code-cell} ipython3
:tags: [remove-cell]

break
```

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
