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

Info content theory subsection.

May ditch this unless it can be extended usefully? Should recon section be before this?

- 22/11/22 Basics in place. Needs work.
- For updates, see dev work http://jake:9966/lab/tree/code-share/jupyter-shared/PEMtk_dev_2022/basisSets/PEMtk_fitting_basis-set_demo_050621-full-revisit-Jake_040822.ipynb
- 15/02/23 revisiting and expanding...
- 20/07/23 revisiting
    - NOT WORKING IN CURRENT BUILDS... getting null values for all BLMs?  Change in defaults/assumptions somewhere to fix.
    - Added thres=None, but doesn't seem to fix.
    - Results in fitting notebook (file:///mnt/jakeSSHFS/home/paul/buildTmp/2023-07-19_15-19-50/html-build/part2/sym-fitting-intro_220423.html) seem OK, so maybe issue with subselection or sym choice here? Could also be phase cons... TBC...
    - 27/07/23: Now debugged. Issue was missing labels in (old-style) conversion to matrix elements. Now updated with full symmetry selection routines in 'scripts/setup_symmetry_basis_tensors.py'.

+++

(sec:info-content)= 
# Information content & sensitivity

A useful tool in considering the possibility of matrix element retrieval is the response, or sensitivity, of the experimental observables to the matrix elements of interest. Aspects of this have already been explored in {numref}`Sect. %s <sec:tensor-formulation>`, where consideration of the various geometric tensors (or geometric basis set) provided a route to investigating the coupling - hence sensitivity - of various parameters into product terms. In particular the tensor products discussed in {numref}`Sect. %s <sec:theory:tensor-products>`, including the full channel (response) functions $\varUpsilon_{L,M}^{u,\zeta\zeta'}$ ({eq}`eq:channelFunc-MF-defn` and {eq}`eq:channelFunc-AF-defn`), can be used to examine the overall sensitivity of a given measurement to the underlying observables. By careful consideration of the problem at hand, experiments may then be tailored for particular cases based on these sensitivities. A related question, is how a given experimental sensitivity might be more readily quantified, and interpreted, for reconstruction problems, in a simpler manner. In general, this can be termed as the _information content_ of the measurement(s); an important aspect of such a metric is that it should be readily interpretable and, ideally, related to whether a reconstruction will be possible in a given case (this has, for example, been considered by other authors for specific cases, e.g. Refs. {cite}`Schmidtke2000,Ramakrishna2012`).
%, and ideally without too much theoretical study. 
Work in this direction is ongoing, and some thoughts are given below. In particular, the use of the observable $\beta_{L,M}$ presents an experimental route to (roughly) define a form of information content, whilst metrics derived from channel functions or density matrices may present a more rigorous theoretical route to a useful parameterization of information content.

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
:tags: [hide-cell]

%matplotlib inline
# May need this in some build envs.
```

(sec:expt-info-content)=
## Experimental information content

As discussed in {{ QM2 }}, the information content of a single observable might be regarded as simply the number of contributing $\beta_{L,M}$ parameters. In set notation:

$$M=\mathrm{n}\{\beta_{L,M}\}$$ (eq:BLM-set)

where $M$ is the information content of the measurement, defined as
$\mathrm{n}\{...\}$ the cardinality (number of elements) of the set of
contributing parameters. A set of measurements, made for some
experimental variable $u$, will then have a total information content:

$$M_{u}=\sum_{u}\mathrm{n}\{\beta_{L,M}^{u}\}$$

In the case where a single measurement contains multiple $\beta_{L,M}$,
e.g. as a function of energy $\epsilon$ or time $t$, the information
content will naturally be larger:

$$\begin{aligned}
M_{u,\epsilon,t} & = & \sum_{u,\epsilon,t}\mathrm{n}\{\beta_{L,M}^{u}(\epsilon,t)\}\\
 & = & M_{u}\times M_{\epsilon,t}\end{aligned}$$

where the second line pertains if each measurement has the same native
information content, independent of $u$. It may be that the variable $k$
is continuous (e.g. photoelectron energy), but in practice it will
usually be discretized in some fashion by the measurement.

In terms of purely experimental methodologies, a larger $M_{u}$ clearly
defines a richer experimental measurement which explores more of the
total measurement space spanned by the full set of
$\{\beta_{L,M}^{u}(k,t)\}$. However, in this basic definition a larger
$M_{u}$ does not necessarily indicate a higher information content for
quantum retrieval applications. The reason for this is simply down to
the complexity of the problem (cf. Eq. {eq}`eqn:channel-fns`), in which many couplings define the sensitivity of the observable to the underlying system properties of
interest. In this sense, more measurements, and larger $M$, may only add
redundancy, rather than new information.

From a set of numerical results, it is relatively trivial to investigate some of these properties as a function of various constraints, using standard Python functionality, as shown in the code blocks below. For example, $M$ can be determined numerically as the number of elements in the dataset, the number of _unique_ elements, the number of elements within a certain range or above a threshold, and so on.

% These make use of the demo cases (defined by symmetry) as previously defined.

```{code-cell} ipython3
# For the basic case, the data (Xarray object) can be queried, and relevant dimensions investigated

print(f"Available dimensions: {BetaNorm.dims}")

# Show BLM dimension details from Xarray dataset
display(BetaNorm.BLM)
```

```{code-cell} ipython3
# Note, however, that the indexes may not always be physical, depending on how the data has been composed and cleaned up.
# For example, the above has l=0, m=+/-1 cases, which are non-physical.

# Clean array to remove terms |m|>l, and display
# BetaNorm.BLM.where(np.abs(BetaNorm.BLM.m)<=BetaNorm.BLM.l,drop=True)
# BetaNorm.where(np.abs(BetaNorm.m)<=BetaNorm.l,drop=True)

cleanBLMs(BetaNorm).BLM
```

```{code-cell} ipython3
# Thresholding can also be used to reduce the results
ep.matEleSelector(BetaNorm, thres=1e-4).BLM
```

```{code-cell} ipython3
# The index can be returned as a Pandas object, and statistical routines applied...
# For example, nunique() will provide the number of unique values.

thres=1e-4

print(f"Original array M={BetaNorm.BLM.indexes['BLM'].nunique()}")
# print(f"Cleaned array M={BetaNorm.BLM.where(np.abs(BetaNorm.BLM.m)<=BetaNorm.BLM.l,drop=True).size}")
print(f"Cleaned array M={cleanBLMs(BetaNorm).BLM.size}")
print(f"Thresholded array (thres={thres}), M={ep.matEleSelector(BetaNorm, thres=thres).BLM.indexes['BLM'].nunique()}")
```

```{code-cell} ipython3
:tags: [remove-cell]

# PD stats from multi-index... 
# Note this is not particularly useful for coords only
BetaNorm.BLM.indexes['BLM'].to_frame().describe()
```

```{code-cell} ipython3
:tags: [remove-cell]

# Convert full dataset to PD dataframe and describe.
BetaNormPD,_ = ep.util.multiDimXrToPD(BetaNorm.squeeze().real, thres=None, colDims='t', dropna=False)   #colDims={'BLM':['l','m']})  #, squeeze=True)
BetaNormPD.describe().to_frame()
```

For more complicated cases, with $u>1$, e.g. time-dependent measurements, interrogating the statistics of the observables may also be an interesting avenue to explore. The examples below investigate this for the example "linear ramp" {{ ADMs }} case. Here the statistical analysis is, potentially, a measure of the useful/non-redundant information content, for instance the range or variance in a particular observable can be analysed, as can the number of unique values and so forth.

```{code-cell} ipython3
BetaNorm
```

```{code-cell} ipython3
BetaNormLinearADMs, basisProductLinearADMs = data.afblmMatEfit(selDims={}, sqThres=False, phaseCons='S')
BetaNormLinearADMs.max()
```

```{code-cell} ipython3
# Convert to PD and tabulate with epsproc functionality
# Note restack along 't' dimension
BetaNormLinearADMsPD, _ = ep.util.multiDimXrToPD(BetaNormLinearADMs.squeeze().real, thres=1e-4, colDims='t')

# Basic describe with Pandas, see https://pandas.pydata.org/docs/user_guide/basics.html#summarizing-data-describe
# This will give properties per t
BetaNormLinearADMsPD.describe()   #([pd.unique])   #(['nunique'])
```

```{code-cell} ipython3
# Basic describe with Pandas, see https://pandas.pydata.org/docs/user_guide/basics.html#summarizing-data-describe
# By transposing the input array, this will give properties per BLM
BetaNormLinearADMsPD.T.describe()
```

For further insight and control, specific aggregation functions and criteria can be specified. For instance, it may be interesting to look at the number of unique values to a certain precision (e.g. depending on experimental uncertainties), or consider deviation of values from the mean.

```{code-cell} ipython3
# Round values to 1 d.p., then apply statistical methods
BetaNormLinearADMsPD.round(1).agg(['min','max','var','count','nunique'])
```

```{code-cell} ipython3
# Define demean function and apply (from https://stackoverflow.com/a/26110278)
demean = lambda x: x - x.mean()

# Compute differences from mean
BetaNormLinearADMsPD.transform(demean,axis='columns')  #.round(1).agg(['min','max','var','count','nunique'])   # OK, matches above case.
```

```{code-cell} ipython3
# Apply statistical functions to differences from mean.
BetaNormLinearADMsPD.transform(demean,axis='columns').round(1).agg(['min','max','var','count','nunique'])
```

In this case the analysis suggests that $t=4,5$ contain minimal, and redundant, information, whilst $t=0,3,6$ are also of low total information content. However, this analysis is not necessarily absolutely definitive, since some nuances may be lost in this basic statistical analysis, particularly for weaker channels.

For a more detailed analysis, other standard analysis tools can be deployed. For instance, the covariance matrix can be investigated, given by $K_{i,j}=\textrm{cov}[X_{i},X_{j}]=\langle(X_{i}-\langle X_{i}\rangle)(X_{j}-\langle X_{j}\rangle)\rangle$. For the linear ramp case this analysis is not particularly useful, but will become more informative for more complicated cases.

```{code-cell} ipython3
# Compute covariance matrix with Pandas
# Note this is the pairwise covariance of the columns, 
# see https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.cov.html
covMat = BetaNormLinearADMsPD.cov()

# Plot with holoviews
figObj = covMat.hvplot.heatmap(cmap='viridis')
```

```{code-cell} ipython3
:tags: [hide-cell, hide-output]

# Glue figure
glue("covMatBLMExample", figObj)   #covMat.hvplot.heatmap(cmap='viridis'))
```

```{glue:figure} covMatBLMExample
---
name: "fig-covMatBLMExample"
---
Example $\beta_\{L,M\}(t)$ covariance matrix, see text for details.
```

```{code-cell} ipython3
:tags: [hide-cell]

# Seaborn also has nice cluster plotting routines, which include sorting by similarity
import seaborn as sns
sns.clustermap(covMat)
```

```{code-cell} ipython3
:tags: [remove-cell]

covMat
```

+++ {"tags": ["remove-cell"]}

**Following are as above but for (L,M) dimension)**

```{code-cell} ipython3
:tags: [remove-cell]

import seaborn as sns
sns.clustermap(BetaNormLinearADMsPD.T.cov().fillna(0))
```

```{code-cell} ipython3
:tags: [remove-cell]

BetaNormLinearADMsPD.transform(demean,axis='columns').round(1).T.agg(['min','max','var','count','nunique'])
```

```{code-cell} ipython3
:tags: [remove-cell]

BetaNormLinearADMsPD
```

```{code-cell} ipython3
:tags: [remove-cell]

BetaNormLinearADMsPD.mean(axis='columns')
```

+++ {"tags": ["remove-cell"]}

**BELOW VERY ROUGH - check old dev notebook for better...**

```{code-cell} ipython3
:tags: [remove-cell]

# Examine unique values at a given level of difference/rounding
# pd.cut(BetaNormLinearADMsPD, 10)

# Use cut - not very useful here, maybe better with agg?
testCut = BetaNormLinearADMsPD.apply(pd.cut, args=[10])
testCut
# testCut.agg('count')
# testCut.agg('unique')
```

```{code-cell} ipython3
:tags: [remove-cell]

BetaNormLinearADMsPD
```

```{code-cell} ipython3
:tags: [remove-cell]

# BetaNormLinearADMs

# Convert/tabulate - NOTE SQUEEZE NOT WORKING for multiDimXrToPD here...?
# testBasisPD, testBasisRS = ep.util.multiDimXrToPD(BetaNormLinearADMs, thres=1e-4, colDims='t', squeeze=True)
testBasisPD, testBasisRS = ep.util.multiDimXrToPD(BetaNormLinearADMs.squeeze().real, thres=1e-4, colDims='t', squeeze=True)

# Basic describe - see pemtk functionality? Only set for fit results?
# testBasisPD.T.agg('count')
testBasisPD.T.describe()   #([pd.unique])   #(['nunique'])
```

```{code-cell} ipython3
:tags: [remove-cell]

testBasisPD.round(1).agg(['min','max','var','count','nunique'])
```

```{code-cell} ipython3
:tags: [remove-cell]

testBasisPD.T.nunique()
```

```{code-cell} ipython3
:tags: [remove-cell]

# BetaNormX.BLM.indexes['BLM']  #.unqiue()
# pd.unique(BetaNormX.BLM.indexes['BLM'])
# dir(BetaNormX.BLM.indexes['BLM'])   #.agg('count')

BetaNorm = BetaNormX

# 
BetaNorm.BLM

# A basic 
BetaNorm.BLM.indexes['BLM'].nunique()
```

```{code-cell} ipython3
:tags: [remove-cell]

BetaNormX
```

## Information content from channel functions

A more complete accounting of information content would, therefore, also
include the channel couplings, i.e. sensitivity/dependence of the
observable to a given system property, in some manner. For the case of a
time-dependent measurement, arising from a rotational wavepacket, this
can be written as:

$$M_{u}=\mathrm{n}\{\varUpsilon_{L,M}^{u}(\epsilon,t)\}$$

In this case, each $(\epsilon,t)$ is treated as an independent
measurement with unique information content, although there may be
redundancy as a function of $t$ depending on the nature of the
rotational wavepacket and channel functions.
% - this is explored further in Sect. [\[sec:bootstrapping-info-sensitivity\]](#sec:bootstrapping-info-sensitivity){reference-type="ref" reference="sec:bootstrapping-info-sensitivity"}. 
(Note this is in
distinction to previously demonstrated cases where the time-dependence
was created from a shaped laser-field, and was integrated over in the
measurements, which provided a coherently-multiplexed case, see refs.
{cite}`hockett2014CompletePhotoionizationExperiments,hockett2015CompletePhotoionizationExperiments,hockett2015CoherentControlPhotoelectron` for details.)

In the numerical examples below, this is considered in terms of the full channel (response) functions $\varUpsilon_{L,M}^{u,\zeta\zeta'}$ as defined in {eq}`eq:channelFunc-MF-defn` and {eq}`eq:channelFunc-AF-defn` (see {numref}`Sect. %s <sec:theory:tensor-products>`). Numerically, the routines follow from those already introduced above for exploring the information content of $\beta_{L,M}$ terms, with the caveat that there are more dimensions to handle in the channel functions, indexed by the relevant set of quantum numbers $\{\zeta,\zeta'\}$ - these can be included in the criteria for determination of $M$, or selected or summed over as desired.

% Numerical example...

```{code-cell} ipython3
# Define a set of channel functions to test
channelFuncs = (basisProductLinearADMs['BLMtableResort'] * basisProductLinearADMs['polProd'])

# For illustrative purposes, define a subset to use for analysis
channelFuncsSubset = channelFuncs.sel(Labels='A').sel({'S-Rp':0,'mu':0,'mup':0})  #.sel(L=2)

# Check dimensions
print(f"Available dimensions: {channelFuncs.dims}")
print(f"Subset dimensions: {channelFuncsSubset.dims}")
```

````{margin}
```{note}
Full tabulations of the parameters available in HTML or notebook formats only.
```
````

```{code-cell} ipython3
:tags: [hide-output]

# Convert to PD and tabulate with epsproc functionality
# Note restack along 't' dimension
channelFuncsSubsetPD, _ = ep.util.multiDimXrToPD(channelFuncsSubset.squeeze().real, thres=1e-4, colDims='t')

# Basic describe with Pandas, see https://pandas.pydata.org/docs/user_guide/basics.html#summarizing-data-describe
# This will give properties per t
# channelFuncsSubsetPD.describe()   #([pd.unique])   #(['nunique'])

# Round values to 1 d.p., then apply statistical methods
# channelFuncsSubsetPD.round(1).agg(['min','max','var','count','nunique'])  # Compute per t

channelFuncsSubsetPD.T.round(2).agg(['min','max','var','count','nunique']).T  #[0:100]  # Compute per basis index and display


# Plotting tests with hvplot wrapper - interesting, but lacking fine control so far...
# channelFuncsSubsetPD.T.round(1).agg(['min','max','var','count','nunique']).T.hvplot.hist('nunique', by=['L','M'], subplots=True).cols(1)
# channelFuncsSubsetPD.T.round(3).agg(['min','max','var','count','nunique']).T.hvplot.hist('nunique', by=['l','lp'])
# channelFuncsSubsetPD.T.round(3).agg(['min','max','var','count','nunique']).T.hvplot.hist('nunique', by=['l','lp'], subplots=True).cols(2)
# channelFuncsSubsetPD.T.round(2).agg(['min','max','var','count','nunique']).T.hvplot.hist('nunique', by=['L','l','lp'], subplots=True)
# channelFuncsSubsetPD.T.round(2).agg(['min','max','var','count','nunique']).T.hvplot.heatmap(x='nunique',y='L', by=['L','l','lp'], subplots=True)

# Holomap version - not working in notebook currently? Gives controls, but plot not responding...
# channelFuncsSubsetPD.T.round(2).agg(['min','max','var','count','nunique']).T.hvplot.hist('nunique', by=['L','l','lp'], groupby=['L','l','lp'])
```

For the higher-dimensional case, it is useful to plot terms relative to all quantum numbers. For example, in a similar manner to the basis set explorations of {numref}`Sect. %s <sec:theory:tensor-products>`, related properties such as the distance from the mean can be examined with `lmPlot()`. And, as previously demonstrated, other properties, such as the covariance, may be examined and plotted.

```{code-cell} ipython3
# channelFuncsSubsetPD.transform(demean,axis='columns') 
# cmap=None   # cmap = None for default. 'vlag' good?
# cmap = 'vlag'

# De-meaned channel functions
channelFuncsDemean = channelFuncsSubsetPD.transform(demean,axis='columns')

# Plot using lmPlot routine - note this requires conversion to Xarray data type first.
daPlot, daPlotpd, legendList, gFig =  ep.lmPlot(channelFuncsDemean.to_xarray().to_array('t')
                                                , xDim='t', cmap=cmap, mDimLabel='m'); 
```

```{code-cell} ipython3
# Full covariance mapping along all dims
sns.clustermap(channelFuncsSubsetPD.T.cov().fillna(0))
```

```{code-cell} ipython3
:tags: [remove-cell]

channelFuncsSubsetPD
```

```{code-cell} ipython3
:tags: [remove-cell]

channelFuncsSubsetPD.transform(demean,axis='columns').to_xarray().to_array('t')
```

## Information content from density matrices

```{code-cell} ipython3

```
