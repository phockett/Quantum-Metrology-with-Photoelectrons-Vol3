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

**Symmetry intro for fitting routines for symmetry-based cases**

22/04/23

See also:

- dev code http://jake:9966/lab/tree/QM3/doc-source/part2/sym-fitting_dev_130423.ipynb
- PEMtk docs http://jake:9966/lab/tree/QM3/doc-source/part2/working_with_symmetry_PEMtk_notes_180423-v210423_tidy.ipynb

TODO:

- General fitting introduction? Here or in "numerics" section.
- Some tidying of methods... for PD conversion already have `epsproc.classes._IO.matEtoPD()` as wrapper for main data structure, but not for symmetry class.
- Comparison with ePS matrix elements just dropped in from "working with symmetry" doc, may want to reduce/tidy a bit, maybe hide outputs.
- Fix numbering for sym defined case - currently it=0 for 1st case, doesn't match ePS 1-index.
- Output formatting for lmfit params objects, see https://github.com/phockett/Quantum-Metrology-with-Photoelectrons-Vol3/issues/9

+++

(sect:basis-sets:fitting-intro)=
# Basis sets for fitting

In order to retrieve a set of matrix elements from experimental results, various physical properties of the system at hand are required. In particular, the symmetry of the system, the ionizing channel(s) of interest, and the properties of the ionizing radiation are all required to define the basis set used for fitting.

Numerically, there are two main methods to do this explored herein:

1. The use of symmetry to define the basis set, in terms of symmetry-allowed components.
1. The use of _ab initio_ calculations to define the basis functions, specifically {{ ePS_full }} matrix elements, in order to determine allowed components.

Manual creation of basis sets is also possible, and may be useful in some cases, particularly when exploring limiting cases.

+++

## Symmetry-defined basis sets

As illustrated in {numref}`Sect. %s <sec:theory:symmetry-intro>`, a set of symmetry-allowed continuum functions can be determined, corresponding to a given ionizing transition and specific dipole symmetries. Such a basis set defines the allowed matrix elements in terms of a set of symmetrized harmonics, and these can be used as a basis for fitting with only minimal knowledge of the system required.

+++

## Computationally-defined basis sets

In cases where photoionization calculations are available, the results can also be used to determine allowed basis components. Use of _ab initio_ computational results is, of course, useful for simulation as well as direct analysis, and may lead to a reduced basis set relative to the symmetry-defined case, since some components may be small and can be ignored. However, it does also require that substantial calculations are performed (or results are available, e.g. from {{ ePSdata_docs }}), and - potentially - may bias the matrix element analysis/retrieval in cases where the experimental results and computational results are significantly different.

+++

## Basis creation worked examples

In the following chapters basis functions are created for each case at hand, typically starting from _ab initio_ computational results (since these are required to simulate the sample data). Here a more detailed worked example is given to illustrate the basic methodology behind the assignments, the differences between the approaches, and highlight some issues of convention which may arise.

+++

### Simple case: $N_2~3\sigma_g^{-1}$ ionization

% Include char table here? UPDATE: now in note.

As a simple example, consider the case of a homonuclear diatomic ($D_{\infty h}$ {{ PG }}, cylindrically symmetric), and a totally symmetric case, e.g. the ionization of the $\Sigma_{g}^{+}$ {{ HOMO }} of $N_2$. For this example, 

- $\Gamma^{i} = \Gamma^{+} = \Gamma^{s} = \Sigma_{g}^{+}$. Note that, for single-electron ionization from a fully-occupied valence orbitals, the ion symmetry will correspond to the hole symmetry, hence the symmetry of the ionized orbital. This simple picture may break down for more complicated cases, e.g. if multi-electron effects or substantial nuclear motions are involved; for radical systems the overall symmetry of all partially-occupied orbitals must be accounted for.
- The dipole symmetries correspond to the Cartesian axes/translations given in the character tables, hence $\Sigma_{u}^{+} = (z)$ and $\Pi_{u} = (x,y)$ for $D_{\infty h}$. Note that, in this cylindrically symmetric case, the Cartesian $(x,y)$ components are spanned by the doubly-degenerate $\Pi_{u}$ irrep - physically this corresponds to the arbitrary orientation of these axes in the {{ MF }}.

Following Eq. {eq}`eq:ionization-symm-electronic`, the allowed components (irreducible representations) can be determined by hand making use of character and direct product tables:

\begin{eqnarray}
\Gamma^{+}\otimes\Gamma^{e}\otimes\Gamma_{\mathrm{dipole}}\otimes\Gamma^{i} & \supseteq & \Sigma_{g}^{+}\\
\Sigma_{g}^{+}\otimes\Gamma^{e}\otimes\begin{array}{c}
\Pi_{u}~(x,y)\\
\Sigma_{u}^{+}~(z)
\end{array}\otimes\Sigma_{g}^{+} & \supseteq & \Sigma_{g}^{+}\\
\Sigma_{g}^{+}\otimes\Gamma^{e}\otimes\begin{array}{c}
\Pi_{u}~(x,y)\\
\Sigma_{u}^{+}~(z)
\end{array} & \supseteq & \Sigma_{g}^{+}\\
\Gamma^{e}\otimes\begin{array}{c}
\Pi_{u}~(x,y)\\
\Sigma_{u}^{+}~(z)
\end{array} & \supseteq & \Sigma_{g}^{+}
\end{eqnarray}

+++

```{admonition} Group theory character tables and related
Character tables, direct product tables and related information can be found at various sources online, or in textbooks, e.g. Refs. {cite}`Atkins2006, gelessusCharacterTablesChemically, katzerCharacterTablesPoint`. For $D_{\infty h}$ the pages at [symmetry.jacobs-university.de](http://symmetry.jacobs-university.de/cgi-bin/group.cgi?group=1001&option=4) provide a good quick reference; for extended tables [including spherical harmonic symmetries and direct products the pages from G. Katzers are useful](http://www.gernot-katzers-spice-pages.com/character_tables/index.html).
```

+++

Hence the allowed continuum components are given by:

\begin{equation}
\Gamma^{e}=\begin{array}{c}
\Pi_{u}~(x,y)\\
\Sigma_{u}^{+}~(z)
\end{array}
\end{equation}

As indicated above, this case is split by symmetry into a "parallel" and "perpendicular" continua, accessed by the $z$ or $(x,y)$ dipole components in the {{ MF }} respectively. In the {{ LF }} or {{ AF }} these continua can be mixed according to the polarization state and geometry of the ionizing radiation, and the molecular alignment ({{ ADMs }}).

+++

The total scattering state symmetry is often also used to label continuum states, and is given by $\Gamma_{\mathrm{scat}}=\Gamma^{+}\otimes\Gamma^{e}$:

\begin{equation}
\Gamma_{\mathrm{scat}}=\Sigma_{g}^{+}\otimes\begin{array}{c}
\Pi_{u}~(x,y)\\
\Sigma_{u}^{+}~(z)
\end{array}=\begin{array}{c}
\Pi_{u}~(x,y)\\
\Sigma_{u}^{+}~(z)
\end{array}
\end{equation}

This is identical to $\Gamma^{e}$ in this simple case.

+++

### Degenerate case example: $N_2~3\pi_u^{-1}$ ionization

For more complicated cases, multiple symmetry components may be found. For example, the ionization from a $\Pi_u$ orbital, e.g. $N_2$ {{ HOMO }}-1.

In this case, $\Gamma^{+} = \Pi_u$, and - working through the direct products as above - yields the allowed continuum components:

\begin{equation}
\Gamma^{e}=\begin{array}{c}
\Sigma_{g}^{+} + \Delta_{g}~(x,y)\\
\Pi_{g}~(z)
\end{array}
\end{equation}

And total scattering state symmetries:

\begin{equation}
\Gamma_{\mathrm{scat}}=\Pi_{u}\otimes\begin{array}{c}
\Sigma_{g}^{+} + \Delta_{g}~(x,y)\\
\Pi_{g}~(z)
\end{array}=\begin{array}{c}
\Pi_{u} + \Delta_{u} + \Phi_{u}~(x,y)\\
\Sigma_{u}^{+} + \Sigma_{u}^{-} + \Delta_{u}~(z)
\end{array}
\end{equation}

In this case, the direct product results give multiple components for each continua. However, since the continuum wavefunction is already defined for multiple components, as given by $\Gamma^{e}$, only the first $\Gamma_{\mathrm{scat}}$ symmetry is required as a unique label here. In this case, therefore, $\Gamma_{\mathrm{scat}} = \Pi_{u}~(x,y)$ and $\Gamma_{\mathrm{scat}} =\Sigma_{u}^{+}~(z)$ suffice to label the total scattering states.

+++

### Defining symmetrized harmonics

In the examples above, the allowed irreducible representations are defined by hand from direct product tables for illustrative purposes. But - by hand - it is tedious to categorize/define the allow spherical harmonics and linear combinations (see {numref}`Sect. %s <sec:theory:sym-harm-into>` and references therein for more details). With the {{ PEMtk_repo }}, both the direct products illustrated above, and the determination of associated spherical harmonics, can be automated and the full basis set rapidly defined numerically. This was illustrated briefly in {numref}`Sect. %s <sec:theory:symmetry-intro>`, and is extended here for the example cases above.

+++

Computationally, the cylindrically-symmetric $\infty$ groups can be approximated by a high-order group, e.g. $D_{\infty h} \approx D_{10h}$. (For a cross-check, see the [full tables and direct products online](http://www.gernot-katzers-spice-pages.com/character_tables/D10h.html).)  Here the notational convention is $A1 = \Sigma^{+}$, $A2 = \Sigma^{-}$, $E1 = \Pi$, $E2 = \Delta$ and so forth (see the [$D_{\infty h}$ character table](http://symmetry.jacobs-university.de/cgi-bin/group.cgi?group=1001&option=4) for more details).

```{code-cell} ipython3
:tags: [hide-cell]

# Run default config - may need to set full path here
%run '../scripts/setup_notebook.py'

# Override plotters backend?
# plotBackend = 'pl'
```

```{code-cell} ipython3
# Example following symmetrized harmonics demo

# Import class
from pemtk.sym.symHarm import symHarm

# Compute hamronics for D10h, lmax=4
sym = 'D10h'
lmax=4

symObjA1g = symHarm(sym,lmax)

# Allowed terms and mappings are given in 'dipoleSyms'
# symObj.dipole['dipoleSyms']
```

```{code-cell} ipython3
:tags: [hide-output]

# Setting the symmetry for the neutral and ion allows direct products to be computed, and allowed terms to be determined.

sNeutral = 'A1g'
sIonSG = 'A1g'

symObjA1g.directProductContinuum([sNeutral, sIonSG])

# Results are pushed to self.continuum, in dictionary and Pandas DataFrame formats, and can be manipulated using standard functionality.
# The subset of allowed values are also set to a separate DataFrame and list.

# Glue figure for later - real part only in this case
# Also clean up axis labels from default state labels ('LM' and 'LM_p' in this case).
glue("dipoleTermsD10hA1g", symObjA1g.continuum['allowed']['PD'])
```

```{glue:figure} dipoleTermsD10hA1g
---
name: "fig-dipoleTermsD10hA1g"
---
Dipole-allowed continuum symmetries ("Target") for $D_{10h}$, $A_{1g}$ ionization.
```

```{code-cell} ipython3
:tags: [hide-output]

# Setting the symmetry for the neutral and ion allows direct products to be computed, and allowed terms to be determined.

sNeutral = 'A1g'
sIonPU = 'E1u'

# Define new object for E1u case
symObjE1u = symHarm(sym,lmax)
symObjE1u.directProductContinuum([sNeutral, sIonPU])

# Results are pushed to self.continuum, in dictionary and Pandas DataFrame formats, and can be manipulated using standard functionality.
# The subset of allowed values are also set to a separate DataFrame and list.

# Glue table for later
glue("dipoleTermsD10hE1u", symObjE1u.continuum['allowed']['PD'])
```

```{glue:figure} dipoleTermsD10hE1u
---
name: "fig-dipoleTermsD10hE1u"
---
Dipole-allowed continuum symmetries ("Target") for $D_{10h}$, $E_{1u}$ ionization.
```

+++

The allowed terms can be further expressed in terms of the spherical harmonic components.

```{code-cell} ipython3
# Basis table with the Character values limited to those defined in self.continuum['allowed']['PD'] Target column
symObjE1u.displayXlm(symFilter = True, YlmType='comp') 
```

(sec:basis-sets:mapping-params)=
### Mapping symmetrized harmonics to fit parameters

The final preparatory steps for tackling a specific retrieval problem is to map the allowed channels to photoionization matrix elements - including the assignment of any missing terms - and from these to fitting paramters. The matrix elements are currently defined in the {{ PEMtk_repo }} and the {{ ePSproc_full }} following the definitions in {{ ePS_full }}, and the symmetry-defined cases can be remapped to this format. (Further information can be found in the {{ PEMtk_docs }}.) For a comparison with _ab initio_ matrix elements, see {numref}`Sect. %s <sec:basis-sets:comparison-with-abinitio>`.

1. For symmetry-defined basis sets, these must first be mapped to an ePSproc data structure, although this step is not necessary when working from _ab initio_ basis sets. This is explored in {numref}`Sect. %s <sec:basis-sets:remapping-to-ePS>`.
1. From a given basis set, the parameters used for fitting data are determined. This converts the parameters to `lmfit` objects in magnitude-phase form, and (optionally) sets various symmetry relations and constraints. This is explored in {numref}`Sect. %s <sec:basis-sets:remapping-to-fittingParams>`.

Further examples can be found in the remainder of this text, and also in the {{ PEMtk-docs }}.

+++

(sec:basis-sets:remapping-to-ePS)=
#### Remapping to ePolyScat definitions

In the remapping, the code attempts to assign all the symmetries matching ePolyScat definitions from the direct products.

The terms are:

1. `Cont` is the continuum (free electron) symmetry, $\Gamma^{e}$.
1. `Targ` is the target state symmetry, $\Gamma^{+}$.
1. `Total` is the overall symmetry of the scattering state, $\Gamma_{\mathrm{scat}}=\Gamma^{+}\otimes\Gamma^{e}$.

+++

Additionally, the current default remapping changes some of the terms defined by the symmetrized harmonics routines and conventions:

- Symmetry `C` > `Cont` (continuum symmetry label in ePSproc)
- Index `h` > `it` (degeneracy index in ePSproc)
- Index `mu` > `muX` (to avoid confusion with photon index `mu` in ePSproc)

Note, in particular, that $\mu$ is - unfortunately - the photon polarization term in the conventional photoionization equations, but also used in the standard definition of the symmetrized harmonics as a degeneracy index. In some cases, the symmetrization indicies $\mu$ or $h$ may be redundant, and can be dropped or summed over, but care must be taken here to avoid breaking the symmetry of the simplified basis set. 

Finally, the remapping adds additional labels used by {{ ePS_full }}, but which are not necessarily required in general:

- `Type`: for ePolyScat results, this labels length or velocity gauge results; this is assigned as `U` (unassigned) in the conversion.
- `Eke`: the photoelectron kinetic energy, for the basis states this is just set to 0.
- `mu`: this is set to NaN by the main routine; if the ionizing channel symmetries are defined these values (the photon polarization) can be determined from the dipole-allowed terms, and this is done by the `assignSymMuTerms()` method, as illustrated below.

```{code-cell} ipython3
# Run conversion with a different dimMap & dataType - note this includes all symmetries, and both real and complex harmonic basis sets
dataType = 'matE'

# With custom dim mapping (optional)...
dimMap = {'C':'Cont', 'mu':'it'}   # Default dimMap = {'C':'Cont','h':'it', 'mu':'muX'}  # TBC - decide on default here.
# dimMap = {'C':'Cont','h':'it', 'mu':'muX'}  # Default case

# Map to ePSproc definitions
symObjA1g.toePSproc(dataType=dataType, dimMap=dimMap)

# To assign specific terms, use self.assignMissingSym
# Note this can take a single value, or a list which must match the size of the Sym multiindex defined in the Xarray dataset.
symObjA1g.assignMissingSym('Targ', sIonSG)

# To define terms from produts, use self.assignMissingSymProd
symObjA1g.assignMissingSymProd()

# To attempt to assign mu values (by symmetry), use self.assignSymMuTerms()
symObjA1g.assignSymMuTerms()

# Show Pandas table of results
symObjA1g.coeffs['symAllowed']['PD'].fillna('')
```

```{code-cell} ipython3
# Plot values
%matplotlib inline
daPlot, daPlotpd, legendList, gFig =  ep.lmPlot(symObjA1g.coeffs['symAllowed']['XR']['b (comp)'], xDim={'LM':['l','m']}, sumDims='h')   #, cmap=cmap, mDimLabel='m');  # linear ADM case
```

(sec:basis-sets:remapping-to-fittingParams)=
#### Mapping to fitting parameters (and reduction)

Finally, the basis set of matrix elements can be set to a set of fitting parameters. In this case, as detailed in **SECT XX**, the parameters are mapped to magnitude-phase form; additionally, the fitting routine allows for the definition of relationships between the parameters. This provides a way to reduce the effective size of the basis set to only the unique values, with other terms defined purely by their symmetry relations. Consequently, degenerate cases, as detailed above, as well as cases with defined phase relations, can be efficiently reduced to a smaller basis set for fitting.

The automated routine currently checks for the following relationships: identity (equal complex values), magnitude and phase equality, complex rotations by $\pm\pi$, and matrix elements are grouped by symmetry (specifically `Cont`) and `l` prior to pair-wise testing. For more control, additional functions can be passed. Alternatively, the automatic setting can be skipped and/or relationships redefined. This provides a way to test if the symmetry-definitions are manifest in experimental data, rather than imposing them during fitting, or to explore other possible correlations between fitted parameters. Note, however, that in some cases the number of unique parameters in an unsymmetrized case may be large, so care should also be taken to ensure that fit results are meaningful in such cases (e.g. by employing a sufficiently large dataset, and testing for reproducibility).

```{code-cell} ipython3
# Default matrix element relationship tests are set by symCheckDefns
from pemtk.fit._sym import symCheckDefns

symCheckDefns()
```

**Automated assignment from defined matrix elements**

```{code-cell} ipython3
from pemtk.fit.fitClass import pemtkFit

# Example using data class (setup in init script)
data = pemtkFit()

# Set to new key in data class
dataKey = sym
data.data[dataKey] = {}

# Assign allowed matrix elements to fit object

# General case
# for dataType in ['matE']:   #,'BLM']:
      
#     # Special cases...
#     if sym=='D2h':
#         data.data[dataKey][dataType] = symObj.coeffs[dataType]['b (comp)'].sum(['h','muX'])  # Select expansion in complex harmonics, and sum redundant dims
    
#     # General case
#     else:
#         data.data[dataKey][dataType] = symObj.coeffs[dataType]['b (comp)']
    
#     data.data[dataKey][dataType].attrs = symObj.coeffs[dataType].attrs

# Specific case
dataType = 'matE'
data.data[dataKey][dataType] = symObjA1g.coeffs['symAllowed']['XR']['b (comp)'].sum('h')
data.data[dataKey][dataType].attrs = symObjA1g.coeffs['symAllowed']['XR'].attrs
```

```{code-cell} ipython3
# Update selection with options
# E.g. Matrix element sub-selection
# data.selOpts['matE'] = {'thres': 0.01, 'inds': {'Type':'U','Cont':'A1'}}
data.selOpts['matE'] = {'thres': 0.01, 'inds': {'Type':'U'}}
data.setSubset(dataKey = sym, dataType = 'matE')  #, resetSelectors=True)  # Subselect from 'orb5' dataset, matrix elements

# And for the polarisation geometries...
# data.selOpts['pol'] = {'inds': {'Labels': 'z'}}
# data.setSubset(dataKey = 'pol', dataType = 'pol')
```

```{code-cell} ipython3
:tags: [hide-output]

# Set matrix elements to fitting parameters
# Running for the default case will attempt to automatically set the relations between matrix elements according to symmetry.
data.setMatEFit()
```

```{code-cell} ipython3
display(data.params)
```

```{code-cell} ipython3
data.params._repr_html_()
```

```{code-cell} ipython3
:tags: [hide-cell]

# Glue table for later
# glue("fittingParamsD10hA1g", data.params)   # Shows plain text in HTML output, data dump in PDF render.

# May want pretty_print?
# data.params.pretty_print(precision=3)

# Need wrapper here otherwise get plain text in current HTML builds, and print(data.params) in PDF version (no data.params._repr_latex_())
glue("fittingParamsD10hA1g", display(data.params._repr_html_()))
```

```{glue:figure} fittingParamsD10hA1g
---
name: "fig-fittingParamsD10hA1g"
---
Fitting parameters as assigned for $D_{10h}$, $A_{1g}$ ionization. Note the `vary` column, which defines the symmetry-unique values for fitting, whilst the `expression` column indicates the relationships of the non-unique values to the floated parameters.
```

+++

**Modifying fitting basis parameters**

A brief illustration of defining constraints is given below, for more details see the {{ PEMtk_docs }}, particularly the [basic fitting guide](https://pemtk.readthedocs.io/en/latest/fitting/PEMtk_fitting_basic_demo_030621-full_010922.html#Setting-parameter-relations/constraints). For more details on the base lmfit parameters class that is used here, see the {{ lmfit }}, particularly the documentation on [parameters](https://lmfit.github.io/lmfit-py/parameters.html) and [constraints](https://lmfit.github.io/lmfit-py/constraints.html).

```{code-cell} ipython3
:tags: [hide-output]

# Set parameters with NO constraints set (except a reference phase)
data.setMatEFit(paramsCons = None)
```

```{code-cell} ipython3
:tags: [hide-output]

# To add manual constraints
# Set param constraints as dict
# Any basic mathematical relations can be set here, see https://lmfit.github.io/lmfit-py/constraints.html
paramsCons = {}
paramsCons['m_A2u_0_A1g_A2u_1_0_0_0'] = '5*m_A2u_0_A1g_A2u_3_0_0_0'

# Missing settings will generate an error message
paramsCons['test'] = 'p_PU_SG_PU_3_1_n1_1'

# Init parameters with specified constraints
data.setMatEFit(paramsCons = paramsCons)
```

```{code-cell} ipython3
# Individual parameters can be addressed by name, and properties modified using lmfit's `.set()` method.

data.params['m_E1u_0_A1g_E1u_1_n1_n1_0']
```

```{code-cell} ipython3
data.params['m_E1u_0_A1g_E1u_1_n1_n1_0'].set(value = 1.36)
data.params['m_E1u_0_A1g_E1u_1_n1_n1_0'].set(vary = False)
data.params['m_E1u_0_A1g_E1u_1_n1_n1_0']
```

```{code-cell} ipython3
:tags: [hide-output]

# The full set can always be checked via self.params
data.params
```

```{code-cell} ipython3
:tags: [hide-output]

# The full mapping of parameter names and indexes is given in self.lmmu
data.lmmu
```

```{code-cell} ipython3
:tags: [remove-cell]

# TODO - improve/consolidate tabulation!

# Tabulate the matrix elements
# Not showing as nice table for singleton case - pd.series vs. dataframe?
data.matEtoPD(keys = 'subset', xDim = 'Sym', drop=False, printTable=False)
```

```{code-cell} ipython3
:tags: [remove-cell]

# data.data['subset']['matESub'].pd
```

```{code-cell} ipython3
:tags: [remove-cell]

# data.data['subset']['matE']
```

**Manually setting fitting basis**

To modify and/or set a basis set manually, the same functions can be used with different inputs and/or options. A few examples are given here, see the {{ PEMtk_docs }} for more information.

```{code-cell} ipython3
# TODO: needs container rebuild for updated PEMtk code 25/04/23

# # Manual configuration of matrix elements
# # from pemtk.fit.fitClass import pemtkFit

# # Example using data class (setup in init script)
# dataManual = pemtkFit()

# # Manual setting for matrix elements
# # See API docs at https://epsproc.readthedocs.io/en/dev/modules/epsproc.util.setMatE.html
# data.setMatE(data = [[0,0, *np.ones(10)], [2,0, *np.linspace(0,1,EPoints)], [4,0, *np.linspace(0,0.5,EPoints)]], dataNames=['l','m'])
```

(sec:basis-sets:comparison-with-abinitio)=
## Comparison with symmetry-defined and computational matrix elements

+++

For comparison of a given symmetry-defined basis set with sample _ab initio_ calculations using {{ ePS_full }} calculations, results can be computed locally or pulled from the web. Some sample/test datasets can be found as part of the [ePSproc repo](https://github.com/phockett/ePSproc/tree/master/data), which includes $N_2$. Further {{ ePS_full }} datasets are available from the {{ ePSdata_repo }}, and [data can be pulled using the python ePSdata interface](https://epsproc.readthedocs.io/en/dev/demos/ePSdata_download_demo_300720.html).

In the following, the test case above for $N_2~3\sigma_g^{-1}$ ionization is illustrated. Note that this comparison shows the results of a full _ab initio_ computation of the matrix elements (Eq. {eq}`eq:matE-dipole`) versus the symmetry-allowed harmonics and associated $b_{hl\lambda}^{\Gamma\mu}$ parameters (Eq. {eq}`eq:symHarm-defn`). In the former case, the $b_{hl\lambda}^{\Gamma\mu}$ are incorporated into the numerical results, but the full angular momentum selection rules and dipole integrals are also included; in the latter case the $b_{hl\lambda}^{\Gamma\mu}$ parameters serve to define the allowed matrix elements, and symmetry relations (e.g. phase, rotations and degeneracy), but _do not_ include any other effects. Hence the comparison here indicates whether the symmetry-defined basis set is sufficient for a matrix element reconstruction, but it may contain terms which are zero in practice, or otherwise drop out from the complete photoionization treatment.

```{code-cell} ipython3
# Pull N2 data from ePSproc Github repo
import wget
from pathlib import Path

# URLs for test ePSproc datasets - n2
# For more datasets use ePSdata, see https://epsproc.readthedocs.io/en/dev/demos/ePSdata_download_demo_300720.html
urls = {'n2PU':"https://github.com/phockett/ePSproc/blob/master/data/photoionization/n2_multiorb/n2_1pu_0.1-50.1eV_A2.inp.out",
        'n2SU':"https://github.com/phockett/ePSproc/blob/master/data/photoionization/n2_multiorb/n2_3sg_0.1-50.1eV_A2.inp.out"}

# Set data dir
dataPath = Path(Path.cwd(), 'n2Data')

# Create and pull files if dir not present (NOTE doesn't check per file here)
if not dataPath.is_dir():
    dataPath.mkdir()

    # Pull files with wget
    for k,v in urls.items():
        wget.download(v+'?raw=true',out=dataPath.as_posix())  # For Github add '?raw=true' to URL


# List files
list(dataPath.glob('*.out'))
```

```{code-cell} ipython3
# Import data - PEMtk object
# For more details on ePSproc usage see https://epsproc.readthedocs.io/en/dev/demos/ePSproc_class_demo_161020.html

# from epsproc.classes.multiJob import ePSmultiJob
# from epsproc.classes.base import ePSbase
# from pemtk.fit.fitClass import pemtkFit

# Instantiate class object.
# Minimally this needs just the dataPath, if verbose = 1 is set then some useful output will also be printed.
data = pemtkFit(fileBase=dataPath, verbose = 1)

# ScanFiles() - this will look for data files on the path provided, and read from them.
data.scanFiles()
```

% NOTE hide-input set for cells below, OK in HTML, but omits cell AND output in PDF builds? May need to glue output too, or might be HTML display issue?

```{code-cell} ipython3
:tags: [hide-input]

# Tabulate some demo matrix elements
singleEdata = ep.matEleSelector(data.data['orb5']['matE'], inds={'Eke':slice(0.001,1,1),'Type':'L'}, thres=1e-3)  #, drop=False, sq=False)   # CURRENTLY ALWAYS DROPPING TYPE HERE
# singleEdata = ep.matEleSelector(data.data['orb6']['matE'], inds={'Eke':slice(0.001,1,1)}, thres=1e-3)  
# singleEdata = data.Esubset(key='orb6',dataType='matE',Erange=[0,1,1],Etype='Eke')

matEPD, _ = ep.multiDimXrToPD(singleEdata, colDims = 'Cont', thres=1e-4)  #, squeeze=False, dropna=False)
# matEPD.fillna('')


# Compare results
# For side-by-side tables, code adapted from https://stackoverflow.com/a/50899244

from IPython.display import display_html 

# Full case
# # df1 = symBasis.coeffs['symAllowed']['PD'].droplevel('h').droplevel('Type').sort_index().fillna('')   # .sort_index(level='it', sort_remaining=False)
# df1 = symBasis.coeffs['symAllowed']['PD'].droplevel('Type').sort_index().fillna('')   # .sort_index(level='it', sort_remaining=False)
# df2 = matEPD.fillna('').sort_index().sort_index(level='Total', ascending=[False]).sort_index(axis=1, ascending=False)  # Swap sym label ordering to match symmetry case. Note ascenting=[False] for multindex case single level only.

# df1_styler = df1.style.set_table_attributes("style='display:inline'").set_caption('<b>Symmetry basis</b>')
# df2_styler = df2.style.set_table_attributes("style='display:inline'").set_caption('<b>ePS basis</b>')

# display_html(df1_styler._repr_html_()+df2_styler._repr_html_(), raw=True)


# Check specific symmetry sets...

# df1['A1g'].dropna()
syms = ['A2u','SU']
# syms = ['E1u','PU']
# df1 = symBasis.coeffs['symAllowed']['PD'].droplevel('Type').sort_index()[syms[0]].dropna().to_frame()
df1 = symObjA1g.coeffs['symAllowed']['PD'].droplevel('h').droplevel('Type').sort_index()[syms[0]].dropna().to_frame()
df2 = matEPD.sort_index().sort_index(level='Total', ascending=[False]).sort_index(axis=1, ascending=False)[syms[1]].dropna().to_frame()

df1_styler = df1.style.set_table_attributes("style='display:inline'").set_caption('<b>Symmetry basis</b>')
df2_styler = df2.style.set_table_attributes("style='display:inline'").set_caption('<b>ePS basis</b>')

display_html(df1_styler._repr_html_()+df2_styler._repr_html_(), raw=True)
```

Here the basis sets are identical, aside from the difference in $l_{max}$.

```{code-cell} ipython3
:tags: [hide-input]

# Check specific sets...

# df1['A1g'].dropna()
syms = ['E1u','PU']
# df1 = symBasis.coeffs['symAllowed']['PD'].droplevel('Type').sort_index()[syms[0]].dropna().to_frame()
df1 = symObjA1g.coeffs['symAllowed']['PD'].droplevel('h').droplevel('Type').sort_index()[syms[0]].dropna().to_frame()
df2 = matEPD.sort_index().sort_index(level='Total', ascending=[False]).sort_index(axis=1, ascending=False)[syms[1]].dropna().to_frame()

df1_styler = df1.style.set_table_attributes("style='display:inline'").set_caption('<b>Symmetry basis</b>')
df2_styler = df2.style.set_table_attributes("style='display:inline'").set_caption('<b>ePS basis</b>')

display_html(df1_styler._repr_html_()+df2_styler._repr_html_(), raw=True)
```

Here the symmetry-defined basis has two degenerate continuua, `it=0,1`, with a phase rotation applied between them. For `it=0` the $\pm m$ terms are anti-phase, whilst for `it=1` they are in-phase (all negative). For the ePS basis, only the anti-phase component is present, and is further reduced to terms with $m$ and $mu$ of opposite sign. These differences are due to additional restrictions imposed by angular momentum selection rules, which are not included in the symmetry-defined case.

+++

In general, the current mappings should be suitable for simulation and reconstruction, but care should be taken to:

1. Confirm symmetry and angular momentum relations for a given case.
1. Apply additional transformations for comparison if comparison with computational results is required.
1. Add degeneracy factors if required (otherwise will be subsumed into matrix element values).

% TODO: address some of these points in this notebook.

+++ {"tags": ["remove-cell"]}

## Format scratch

```{code-cell} ipython3
:tags: [remove-cell]

# R example from https://discourse.jupyter.org/t/jupyter-to-latex-how-to-render-tables/14968/2
function RawBlock (raw)
  if raw.format:match 'html' then
    return pandoc.read(raw.text, 'html').blocks
  end
end
```

```{code-cell} ipython3
:tags: [remove-cell]

import pandoc
```

```{code-cell} ipython3
:tags: [remove-cell]

!pandoc --help
```

```{code-cell} ipython3

```
