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

+++ {"tags": ["remove-cell"]}

17/07/23

- Added stub for this.

TO DO:

- Theory from MF recon paper and OCS notes (https://phockett.github.io/ePSdata/OCS-preliminary/OCS_orbs8-11_AFBLMs_VM-ADMs_140122-JAKE_tidy-replot-200722_v5.html)
- Numerical examples and visualisation.
  - 19/07/23 added text & OCS vis. Note plotting broken in pre 17/07/23 builds.
              May want to switch to N2 for demo?
              Also note P(theta) distributions may need A000/2pi?  Not sure - should integrate to one I think.
              UPDATE: test build didn't work properly, need to use subselected ADMs for script-loaded case?
              May want to switch to N2 case for simplicity.
  - TRY OLDER MATPLOTLIB VERSION - working in Stimpy build.
  - UPDATE: 
      - actually, it's the molplot setup part that's failing in newer builds, can ignore for now.
      - BUT only on a rerun of the notebook, seems related to when %matplotlib inline is called, and what is in the buffer...?
      - Working in current build after `pip install matplotlib==3.5`, although still getting inconsistent behaviour with Mol Plot (which seems to be the source of the issues). Go with this for now.
      - 22/07/23, working v3.5.3 BUT ONLY with `%matplotlib inline` included at beginning of ADM plotting cell, otherwise get callback errors again. Weird. UPDATE: looks like Arrow3D issue, see note to fix https://github.com/phockett/Quantum-Metrology-with-Photoelectrons-Vol3/issues/11
      - 22/07/23, added some extra plot tests and GLUE tests (to finish).
      - 29/07/23, switched to N2 case, more interesting for plots. STILL NEEDS A TIDY.

+++

(sect:theory:alignment)=
# Molecular alignment

## A very brief introduction to molecular alignment

The term {term}`molecular alignment` can be used, in general, to define any case where the {{ MF }} is specified relative to the {{ LF }} in some way - for instance if the molecular symmetry axis is constrained to the {{ LF }} $z$-axis. Herein, it is generally used more specifically, to refer to the case of a (time-dependent) aligned molecular ensemble in gas-phase experiments (e.g. as illustrated in {numref}`fig-bootstrap-concept-outline`). Any such axis distribution, in which there is a defined arrangement of axes created in the {{ LF }}, can be discussed, and characterised, in terms of the axis distribution moments ({{ ADMs }}), which have already been introduced passing in {numref}`Sect. %s <sec:tensor-formulation>`. More specifically, {{ ADMs }} are coefficients in a multipole expansion, usually in terms of {{ WIGNERD }}, of the molecular axis probability distribution. In this section some additional definitions are given, along with numerical examples. 

The creation of an aligned ensemble in the gas phase can be achieved via a single, or sequence of, N-photon transitions, or strong-field mediated techniques. Of the latter, adiabatic and non-adiabatic alignment methods are particularly powerful, and make use of a strong, slowly-varying or impulsive laser field respectively. (Here the "slow" and "impulsive" time-scales are defined in relation to molecular rotations, roughly on the ps time-scale, with ns and fs laser fields corresponding to the typical slow and fast control fields.) In the former case, the molecular axis, or axes, will gradually align along the electric-field vector(s) while the field is present. In the latter, impulsive case, a broad rotational wavepacket ({{ RWP }}) can be created, initiating complex rotational dynamics including field-free revivals of ensemble alignment. For further general discussion, there is a rich literature on molecular alignment available, see, for instance, Refs. {cite}`Stapelfeldt2003,hasegawa2015NonadiabaticMolecularAlignment, koch2019QuantumControlMolecular,nielsen2022Helium` for reviews and further introductory materials, and further discussion in the current context can be found in {{ QM12 }} and Refs. {cite}`Reid2000, Underwood2000, Ramakrishna2012, Ramakrishna2013, hockett2015GeneralPhenomenologyIonization, hockett2023TopicalReviewExtracting` and references therein.

For {{ RADMATE }} retrieval problems based on {{ RWP }} methods, the absolute degree of alignment may - or may not - be critical in a given case. The sampling of a range of *different* alignments, however, is vital, since this directly feeds into the information content of the measurements (see {numref}`Sect. %s <sec:theory:AF-alignment-term>` and {numref}`Sect. %s <sec:info-content>`). In the case-studies of {{ PARTII }}, the {{ ADMs }} are assumed to be known, but in general these must be determined from experimental data, this is discussed in {numref}`Sect. %s <sect:numerics:alignment-retrieval>`.

+++

## Alignment distribution moments (ADMs)

The parametrization of an aligned distribution can be given generally by an expansion in {{ WIGNERD }}:

$$ 
P(\Omega,t) = \sum_{K,Q,S} A^K_{Q,S}(t)D^K_{Q,S}(\Omega)
$$ (eqn:P-omega-t)

Where $P(\Omega,t)$ is the full axis distribution probability, expanded for a set of {{ EULER }} $\Omega$, and the expansion parameters $A^K_{Q,S}(t)$ are the {{ ADMs }}.

This reduces to the 2D case if $S=0$, which can equivalently be described as an expansion in spherical harmonics (note that the normalisation of the {{ ADMs }} may be different in this case):

$$ 
P(\theta,\phi,t) = \sum_{K,Q} A^K_{Q,0}(t)D^K_{Q,0}(\Omega) = \sum_{K,Q} A^K_{Q}(t)Y_{K,Q}(\Omega)
$$ (eqn:P-omega-t-2D)

In the examples given in {numref}`Sect. %s <sec:tensor-formulation>`, some arbitrary choices of $A^K_{Q,S}(t)$ were demonstrated to investigate their effects on the tensor basis sets; in the case-studies presented in {{ PARTII }} realistic {{ ADMs }} are used for specific fitting problems. In practice this equates to (accurately) simulating rotational wavepackets, hence obtaining the corresponding $A_{Q,S}^{K}(t)$ parameters (expectation values), as a function of laser fluence and rotational temperature. (Given experimental data, a 2D uncertainty (or error) surface in these two fundamental quantities can then be obtained from a linear regression for each set of $A_{Q,S}^{K}(t)$, see Ref. {cite}`hockett2023TopicalReviewExtracting` for further introductory discussion on this point.) Note that, as discussed in {numref}`Sect. %s <sect:platform:general>`, computation of molecular alignment is not yet implemented in the {{ PEMtk_repo }}, so values must be obtained from other codes. {{ ADMs }} used herein were all computed with codes developed by V. Makhija {cite}`Makhija2014`, and are available from the {{ ePSproc_repo }} repo on Github.

+++

## Numerical setup

For illustrative purposes, the {{ ADMs }} used for the $OCS$ fitting example are here loaded and used to compute $P(\Omega,t)$.

```{code-cell} ipython3
:tags: [hide-output, hide-cell]

# %matplotlib inline

# Pass custom img config for notebook
# import os
# os.environ['IMGWIDTH']='750'
# Run default config - may need to set full path here
%run '../scripts/setup_notebook.py'

# Run OCS setup script - may need to set full path here
# ADMfile = 'ADMs_8TW_120fs_5K.mat'
# dataPath = Path('../part2/OCSfitting')
# dataPath = Path('/home/jovyan/QM3/doc-source/part2/OCSfitting')

# Run general config script with dataPath set above
# %run {dataPath/"setup_fit_demo_OCS.py"} -d {dataPath} -a {dataPath} -c "OCS"

# 29/07/23 - updated scripts
fitSystem='N2'
dataName = 'n2fitting'
dataPath = Path(Path.cwd().parent,'part2',dataName)

# Run general config script with dataPath set above
%run "../scripts/setup_fit_case-studies_270723.py" -d {dataPath} -c {fitSystem}
```

```{code-cell} ipython3
:tags: [hide-cell, hide-output]

# The general config script sets an ADM Xarray, and a downsampled version in 'subset'
print(data.data['subset']['ADM'].dims)

# Tidy up t-coords for demo case, set to reduced d.p.
data.data['subset']['ADM']['t'] = data.data['subset']['ADM'].t.pipe(np.round, decimals=3)

print('*** Set reduced t-coords for demo case')
print(data.data['subset']['ADM'].t)
```

```{code-cell} ipython3
:tags: [remove-cell]

# Quick plot for subselected ADMs (setup in the script), 
# using basic plotter
data.ADMplot(keys = data.subKey)
```

```{code-cell} ipython3
# Quick plot for subselected ADMs (setup in the script), using hvplot
# data.data['subset']['ADM'].unstack().squeeze().real.hvplot.line(x='t').overlay('K')

# As above, but plot K>0 terms only, and keep 'Q','S' indexes (here all =0)
data.data['subset']['ADM'].unstack().where(data.data['subset']['ADM'].unstack().K>0) \
        .real.hvplot.line(x='t').overlay(['K','Q','S']).opts(width=700)
```

## Compute $P(\theta,\Phi,t)$ distributions

For 1D and 2D cases, the full axis distributions can be expanded in spherical harmonics and plotted using {{ PEMtk_repo }} class methods. This is briefly illustrated below. Note that expansions in {{ WIGNERD }} are not currently supported by these routines.

```{code-cell} ipython3
# NOTE - need this in some builds if Matplotlib has call-back errors.
%matplotlib inline  
# Plot P(theta,t) with summation over phi dimension
# Note the plotting function automatically expands the ADMs in spherical harmonics
dataKey = 'subset'
data.padPlot(keys = dataKey, dataType='ADM', Etype = 't', pStyle='grid', reducePhi='sum', returnFlag = True)

# And GLUE for display later with caption
# Object return not working here? Try plt.gca() instead.
glue("PthetaGrid", plt.gca())
```

```{code-cell} ipython3
# GLUE TESTING ONLY

# # Glue figure for display
# figObj = data.data[dataKey]['plots']['ADM']['grid']

# # And GLUE for display later with caption
# gluePlotly("PthetaGrid", figObj)

# dir(figObj)
# # figObj.draw(renderer=None)
# from matplotlib import pyplot as plt
# plt.show()

# Test hv plot version
# subset.plot(x='Theta', y=Etype, col=list({*facetDimsCheck}-{Etype})[0], robust=True)
# data.data[dataKey]['plots']['ADM']['pData'].plot(x='Theta', y='t', robust=True)
norm = data.data[dataKey]['plots']['ADM']['pData'].max()
# (data.data[dataKey]['plots']['ADM']['pData']/norm).hvplot(x='Theta', y='t', cmap='vlag')
(data.data[dataKey]['plots']['ADM']['pData']/norm).hvplot(y='Theta', x='t', cmap='vlag')
# pObj = plt.gca()
```

```{code-cell} ipython3
# glue("PthetaGrid", pObj)
```

```{code-cell} ipython3
data.data[dataKey]['ADM'].t
```

```{code-cell} ipython3
tPlot
```

```{code-cell} ipython3
# Plot full axis distributions at selected time-steps
# tPlot = [39.402, 40.791, 42.18]  # Manual setting for baseline case, and at max and min K=2 times. OCS
tPlot = [4.018, 4.254, 4.49] # N2

# Alternatively, plot at selected times by index slice
# Note that selDims below requires labels (not index inds)
# tPlot = data.data[dataKey]['ADM'].t[::5]  # OCS
# tPlot = data.data[dataKey]['ADM'].t[0:7:3] # N2

# Plot
ep.plot.hvPlotters.setPlotters(width=1200, height=600)   # Force plot dims for HTML render (avoids subplot clipping issues)
data.padPlot(keys = dataKey, dataType='ADM', Etype = 't', pType='a', 
             returnFlag = True, selDims={'t':tPlot}, backend='pl')
```

+++ {"tags": ["remove-cell"]}

## Alignment metrics
