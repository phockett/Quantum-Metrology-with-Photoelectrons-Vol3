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

# Run default config - may need to set full path here
%run '../scripts/setup_notebook.py'

# Run OCS setup script - may need to set full path here
# ADMfile = 'ADMs_8TW_120fs_5K.mat'
# dataPath = Path('../part2/OCSfitting')
dataPath = Path('/home/jovyan/QM3/doc-source/part2/OCSfitting')

# Run general config script with dataPath set above
%run {dataPath/"setup_fit_demo_OCS.py"} -d {dataPath} -a {dataPath} -c "OCS"
```

```{code-cell} ipython3
data.data.keys()
```

```{code-cell} ipython3
data.data['ADM']['ADM'].unstack().squeeze().real.hvplot.line(x='t').overlay('K')
```

```{code-cell} ipython3
data.data['subset']['ADM'].unstack().squeeze().real.hvplot.line(x='t').overlay('K')
```

## Compute $P(\theta,\Phi,t)$ distributions

For 1D and 2D cases, the full axis distributions can be expanded in spherical harmonics and plotted using {{ PEMtk_repo }} class methods. This is briefly illustrated below. Note that expansions in {{ WIGNERD }} are not currently supported by these routines.

```{code-cell} ipython3
# Broken in jupyterlab_epsproc_dev:180523
# Working in updated 3D builds.
# NOTE: broken in latest Matplotlib v3.7.1, but OK in v3.4.3
#       get "Error in callback <function _draw_all_if_interactive at 0x7f38ec7c7d90> (for post_execute):" and
#       get "TypeError: Arrow3D.draw() missing 1 required positional argument: 'renderer'" 
# Axis distributions P(theta) vs. t (summed over phi)
# Pt = data.padPlot(keys = 'ADM', dataType='ADM', Etype = 't', pStyle='grid', reducePhi='sum', returnFlag = True)  #, facetDims=['t', 'Eke'])

%matplotlib inline
dataKey = 'subset'
# Pt = data.padPlot(keys = dataKey, dataType='ADM', Etype = 't', pType='a', 
#                   pStyle='grid', reducePhi='sum', returnFlag = True)  #, backend='mpl', facetDims=['t', None])  # squeeze=True, facetDims=['t', 'Eke'])  # Real plot to check values OK.

Pt = data.padPlot(keys = dataKey, dataType='ADM', Etype = 't', pStyle='grid', reducePhi='sum', returnFlag = True)  #, facetDims=['t', 'Eke'])
```

```{code-cell} ipython3
# The returned data array contains the plotted values
# Pt

data.data['subset']['plots']['ADM']['grid']
```

```{code-cell} ipython3
tAxis = tAxis = data.data[dataKey]['ADM'].t
data.padPlot(keys = dataKey, dataType='ADM', Etype = 't', pType='a', returnFlag = True, selDims={'t':tAxis[1:30:5]}, backend='pl')
```

+++ {"tags": ["remove-cell"]}

## Alignment metrics

+++ {"tags": ["remove-cell"]}

## SCRATCH

% FROM MF RECON MANUSCRIPT

For gas phase experiments, the most common methods involve creating some form of alignment or orientation \footnote{In the technical sense, alignment retains 
% \textbf{inversion symmetry in the LF, while orientation typically implies reduction of the LF symmetry to match the molecular point group symmetry}.
inversion symmetry in the LF, while orientation typically implies reduction of the LF symmetry to match the molecular point group symmetry. The term "orientation" is used herein as synonymous with the MF for an arbitrary molecular system, but in some cases - e.g. homonuclear diatomics - alignment may be sufficient for observation of MF observables.} 
in the gas phase molecular ensemble, which defines a relationship between the LF and MF. In general, measurements made from such an ensemble can be termed as corresponding to ``the aligned frame (AF)", and may still involve averaging over some DOFs; in the 
% \textbf{classical} 
classical limit of perfect orientation, the AF and MF are conformal/indistinguishable. 

Perhaps the simplest AF technique is the creation of alignment via a single-photon pump process (as used in many resonance-enhanced mulit-photon ionization (REMPI) type experimental schemes, which may even be rotational-state selected); in this case a parallel or perpendicular transition moment will create a $\cos^2(\theta)$ or $\sin^2(\theta)$ distribution, respectively, of the corresponding molecular axis. Any such axis distribution, in which there is a defined arrangement of axes created in the LF, can be discussed, and characterised, in terms of the axis distribution moments (ADMs). ADMs are coefficients in a multipole expansion, in terms of Wigner D-Matrix Elements (see Sect. \ref{sec:full-tensor-expansion}), of the molecular axis probability distribution. These are spherical tensors, equivalent to density matrix elements \cite{BlumDensityMat}. Many authors have address aspects of this problem in the past in frequency-domain work, see, for instance, the textbooks of Zare \cite{zareAngMom} and Blum \cite{BlumDensityMat}, treatments for various experimental cases in Refs. \cite{Docker1988,Dubs1989,Greene1983}, and application in complete photoionization experiments in Refs. \cite{Leahy1991,hockett2009RotationallyResolvedPhotoelectron}.
% \textbf{Wigner D-Matrix Elements}.)

Further control can be gained via a single, or sequence of, N-photon transitions, or strong-field mediated techniques. Of the latter, adiabatic and non-adiabatic alignment methods are particularly powerful, and make use of a strong, slowly-varying or impulsive laser field respectively. (Here the ``slow" and ``impulsive" time-scales are defined in relation to molecular rotations, roughly on the ps time-scale, with ns and fs laser fields corresponding to the typical slow and fast control fields.) In the former case, the molecular axis, or axes, will gradually align along the electric-field vector(s) while the field is present. In the latter, impulsive case, a broad rotational wavepacket (RWP) can be created, initiating complex rotational dynamics including field-free revivals of ensemble alignment. Both techniques are powerful, but multiple laser fields are typically required in order to control more than one molecular axis, leading to relatively complex experimental requirements. The absolute degree of alignment obtained in a given case is also dependent on a number of intrinsic and experimental properties, including the molecular polarisability 
% \textbf{and moment of inertia} 
and moment of inertia tensors, rotational temperature and separability of the rotational degrees of freedom from other DOFs (loosely speaking, this can be considered in terms of the stiffness of the molecule). Recent studies of molecules embedded in Helium droplets have addressed some of these issues, achieving stronger and longer lived 3D alignment. These studies also examined several complications associated with coupling between molecular and droplet DOFs.   Therefore, although general in principle, in practice not all molecular targets are amenable to ``good" (i.e. a high degree of) alignment. For more general details, see, for example, Refs. \cite{koch2019QuantumControlMolecular,Stapelfeldt2003,nielsen2022Helium}, and for applications in photoionization see Sect. \ref{sec:theory-lit}.

Whilst gas phase alignment experiments can become rather complex, multi-pulse affairs, they are increasingly popular in the AMO community for a number of possible reasons. Conceptually and experimentally, they are a relatively tractable extension to existing techniques. They are interesting experiments in their own right, and, practically, they are usually feasible with existing high-power pulsed laser sources in the ns to fs regime. Alignment techniques have been combined with a range of different probes, including non-linear and high-harmonic optical probes, as well as photoionization-based methods - for recent reviews see \cite{hasegawa2015NonadiabaticMolecularAlignment,koch2019QuantumControlMolecular}.
