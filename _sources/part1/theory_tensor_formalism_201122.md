---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.0
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

+++ {"tags": ["remove-cell"]}

Subsections for tensor formulation.

- 22/11/22: basics in place and all refs present.

TODO

- Numerical examples.
- Tidy up notation in some places.
- Full extended tensor formulation as per Appendix in MF recon paper? Probably should add in here.

+++ {"tags": []}

(sec:tensor-formulation)=
# Tensor formulation of photoionization

% A number of authors have treated MFPADs and related problems [REFS]; 
% see Appendix [\[sec:theory-lit\]](#sec:theory-lit){reference-type="ref" reference="sec:theory-lit"} for some examples. 
A number of authors have treated MFPADs and related problems [REFS]; herein, a geometric tensor based formalism is developed, which is close in spirit to the treatments given by Underwood and co-workers {cite}`Reid2000,Stolow2008,Underwood2000`, but further separates various sets of physical parameters into dedicated tensors; this allows for a unified theoretical and numerical treatment, where the latter computes properties as tensor variables which can be further manipulated and investigated. Furthermore, the tensors can readily be converted to a density matrix representation {cite}`BlumDensityMat,zareAngMom`, which is more natural for some quantities, and also emphasizes the link to quantum state tomography and other quantum information techniques. Much of the theoretical background, as well as application to aspects of the current problem, can be found in the textbooks of Blum {cite}`BlumDensityMat`
and Zare {cite}`zareAngMom`.

Within this treatment, the observables can be defined in a series of simplified forms, emphasizing the quantities of interest for a given problem. Some details are defined in the following subsections,
% and further detailed in Appendix [\[appendix:formalism\]](#appendix:formalism){reference-type="ref" reference="appendix:formalism"}.

+++

(sec:channel-funcs)=
## Channel functions

A simple form of the equations, amenable to fitting, is to write the observables in terms of "channel functions\", which define the ionization continuum for a given case and set of parameters $u$ (e.g. defined for the MF, or defined for a specific experimental configuration),

$$\beta_{L,M}^{u}=\sum_{\zeta,\zeta'}\varUpsilon_{L,M}^{u,\zeta\zeta'}\mathbb{I}^{\zeta\zeta'}$$ (eqn:channel-fns)

Where $\zeta,\zeta'$ collect all the required quantum numbers, and
define all (coherent) pairs of components. The term
$\mathbb{I}^{\zeta\zeta'}$ denotes the coherent square of the ionization
matrix elements:

$$\mathbb{I}^{\zeta,\zeta}=I^{\zeta}(\epsilon)I^{\zeta'*}(\epsilon)
$$ (eqn:I-zeta)

This is effectively a convolution equation (cf. refs. {cite}`Reid2000,gregory2021MolecularFramePhotoelectron`) with channel functions, for a given "experiment" $u$, summed over all terms $\zeta,\zeta'$. Aside from the change in notation (which is here chosen to match the formalism of Refs. {cite}`Gianturco1994, Lucchese1986,Natalense1999`), 
% see also Sect.[\[sec:mat-ele-conventions\]](#sec:mat-ele-conventions){reference-type="ref" reference="sec:mat-ele-conventions"}), 
these matrix elements are essentially identical to the simplified (radial) forms
$\mathbf{r}_{k,l,m}$ defined in Eqn. {eq}`eq:r-kllam`, in the case where $\zeta=k,l,m$. These complex matrix elements can also be equivalently defined in a magnitude, phase
form:

$$I^{\zeta}(\epsilon)\equiv\mathbf{r}_{\zeta}\equiv r_{\zeta}e^{i\phi_{\zeta}}$$(eqn:I-zeta-mag-phase)

This tensorial form is numerically implemented in the {{ ePSproc_repo }} codebase, and is in contradistinction to standard numerical routines in which the requisite terms are usually computed from vectorial and/or nested summations, which can be somewhat opaque to
detailed interpretation, and typically implement the full computation of the observables in one monolithic computational routine. The {{ PEMtk_repo }} codebase implements matrix element retrieval based on the tensor formalism, with pre-computation of all the geometric tensor components (channel functions) prior to a fitting protocol for matrix element analysis, essentially a fit to Eqn. {eq}`eqn:channel-fns`, with terms $I^{\zeta}(\epsilon)$ as the unknowns (in magnitude, phase form per {eq}`eqn:I-zeta-mag-phase`). The main computational cost of a tensor-based approach is that more RAM is required to store the full set of tensor variables; however, the method is computationally efficient since it is inherently parallel (as compared to a traditional, serial loop-based solution), hence may lead to significantly faster evaluation of observables. Furthermore, the method allows for the computational routines to match the formalism quite closely, and investigation of the properties of the channel functions for a given problem in general terms, as well as for specific experimental cases.

TODO: numerical examples here or below.
TODO: benchmarks, or link to them (see test fitting notebooks...?).

+++

(sec:full-tensor-expansion)= 
## Full tensor expansion

In more detail, the channel functions can be given as a set of tensors, defining each aspect of the problem.

For the MF:

$$\begin{aligned}
\beta_{L,-M}^{\mu_{i},\mu_{f}}(\epsilon) & = & (-1)^{M}\sum_{P,R',R}(2P+1)^{\frac{1}{2}}{E_{P-R}(\hat{e};\mu_{0})}\\
 & \times &\sum_{l,m,\mu}\sum_{l',m',\mu'}(-1)^{(\mu'-\mu_{0})}{\Lambda_{R',R}(R_{\hat{n}};\mu,P,R,R')B_{L,-M}(l,l',m,m')}\\
 & \times & I_{l,m,\mu}^{p_{i}\mu_{i},p_{f}\mu_{f}}(\epsilon)I_{l',m',\mu'}^{p_{i}\mu_{i},p_{f}\mu_{f}*}(\epsilon)\end{aligned}$$ (eq:BLM-tensor-MF)

And the LF/AF as:

$$\begin{aligned}
\bar{\beta}_{L,-M}^{\mu_{i},\mu_{f}}(E,t) & = & (-1)^{M}\sum_{P,R',R}{[P]^{\frac{1}{2}}}{E_{P-R}(\hat{e};\mu_{0})}\\
 & \times &\sum_{l,m,\mu}\sum_{l',m',\mu'}(-1)^{(\mu'-\mu_{0})}{\Lambda_{R'}(\mu,P,R')B_{L,S-R'}(l,l',m,m')}\\
 & \times &I_{l,m,\mu}^{p_{i}\mu_{i},p_{f}\mu_{f}}(\epsilon)I_{l',m',\mu'}^{p_{i}\mu_{i},p_{f}\mu_{f}*}(\epsilon)\sum_{K,Q,S}\Delta_{L,M}(K,Q,S)A_{Q,S}^{K}(t)\end{aligned}$$ (eq:BLM-tensor-AF)

In both cases a set of geometric tensor terms are required, 
% which are fully defined in Appendix [\[appendix:formalism\]](#appendix:formalism){reference-type="ref" reference="appendix:formalism"}; 
these terms provide details of:

-   ${E_{P-R}(\hat{e};\mu_{0})}$: polarization geometry & coupling with
    the electric field.

-   $B_{L,S-R'}(l,l',m,m')$: geometric coupling of the partial waves
    into the $\beta_{L,M}$ terms (spherical tensors).

-   $\Lambda_{R'}(\mu,P,R')$: frame couplings and rotations.

-   $\Delta_{L,M}(K,Q,S)$: alignment frame coupling.

-   $A_{Q,S}^{K}(t)$: ensemble alignment described as a set of axis
    distribution moments (ADMs).

And $I_{l,m,\mu}^{p_{i}\mu_{i},p_{f}\mu_{f}}(\epsilon)$ are the (radial)
dipole ionization matrix elements, as a function of energy $\epsilon$.
These matrix elements are essentially identical to the simplified forms
$r_{k,l,m}$ defined in Eqn. {eq}`eq:r-kllam`, except with additional indices to label
symmetry and polarization components defined by a set of partial-waves
$\{l,m\}$, for polarization component $\mu$ (denoting the photon angular
momentum components) and channels (symmetries) labelled by initial and
final state indexes ${p_{i}\mu_{i},p_{f}\mu_{f}}$. The notation here
follows that used by {{ ePS_full }}, and these matrix elements again represent the quantities to be obtained numerically from data analysis, or from an [ePolyScat (or similar) calculation](https://epsproc.readthedocs.io/en/latest/ePS_ePSproc_tutorial/ePS_tutorial_080520.html#Theoretical-background).

[Numerical example here, or already included above somewhere]

Note that, in this case as given, time-dependence arises purely from the
$A_{Q,S}^{K}(t)$ terms in the AF case, and the electric field term
currently describes only the photon angular momentum coupling, although
can in principle also describe time-dependent/shaped fields. Similarly,
a time-dependent initial state (e.g. a vibrational wavepacket) could
also describe a time-dependent MF case.

It should be emphasized, however, that the underlying physical
quantities are essentially identical in all the theoretical approaches,
with a set of coupled angular-momenta defining the geometrical part of
the photoionization problem, despite these differences in the details of
the theory and notation.

+++ {"tags": []}

(sec:density-mat-basic)=
## Density matrix representation

The density operator associated with the continuum state in
Eq. {eq}`eq:continuum-state-vec` is easily written as $\hat{\rho}=|\Psi_c\rangle\langle\Psi_c|$. In the channel function basis, this leads to a density matrix given by the radial matrix
elements:

% $$\mathbf{\rho}^{\zeta\zeta'} = \mathbb{I}^{\zeta,\zeta'}
% $$ (eqn:radial-density-mat)

$$\boldsymbol{\rho}^{\zeta\zeta'} = \mathbb{I}^{\zeta,\zeta'}
$$ (eqn:radial-density-mat)

Since the matrix elements characterise the scattering event, the density matrix provides an equivalent characterisation of the scattering event. 
% An example case is discussed in Sect. [\[sec:den-mat-N2\]](#sec:den-mat-N2){reference-type="ref" reference="sec:den-mat-N2"} (see Fig. [11](#998904){reference-type="ref" reference="998904"}); for more details, and further discussion, see Sect. [\[sec:density-mat-full\]](#sec:density-mat-full){reference-type="ref" reference="sec:density-mat-full"}.

Further discussion can also be found in the literature, see, e.g., Ref. {cite}`BlumDensityMat` for general discussion, Ref. {cite}`Reid1991` for application in pump-probe schemes.

TODO: numerical examples here
