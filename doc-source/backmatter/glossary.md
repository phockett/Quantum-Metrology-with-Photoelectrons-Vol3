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

# Glossary

+++

```{glossary}

MF
  Molecular frame (MF) - coordinate system referenced to the molecule, usually with the z-axis corresponding to the highest symmetry axis.


LF
  Laboratory or lab frame (LF) - coordinate system referenced to the laboratory frame, usually with the z-axis corresponding to the laser field polarization. For circularly or elliptically polarized light the propagation direction is conventionally used for the z-axis. In some cases a different z-axis may be chosen, e.g. as defined by a detector.


AF
  Aligned frame (AF) - coordinate system referenced to molecular alignment axis or axes. For 1D alignment, the z-axis usually corresponds to the alignment field polarization, and hence may be identical to the standard {{ LF }} definition. For high degrees of (3D) alignment the AF may approach the {{ MF }} in the ideal case, although will usually be limited by the symmetry of the system.


PADs
  Photoelectron angular distributions (PADs), often with a prefix denoting the reference frame, e.g. LFPADs, MFPADs (sometimes also hypenated, e.g. LF-PADs). Usage is often synonymous with the associated {{ betas }} (or "betas").


anisotropy paramters
  Expansion parameters {{ BLM }} for an expansion in spherical harmonics (or similar basis sets of angular momentum functions in polar coordinates), e.g. Eq. {eq}`eq:AF-PAD-general`. Often referred to simply as "beta parameters", and may be dependent on various properties, e.g. $\beta_{L,M}(\epsilon,t...)$. Herein upper-case $L,M$ usually refer to observables or the general case, whilst lower-case $(l,m)$ usually refer specifically to the photoelectron wavefunction partial waves, and $(l,\lambda)$ usually denote these terms referenced specifically to the molecular frame.


ADMs
  Expansion parameters {{ ADMsymbol }} for describing a molecular ensemble alignment described as a set of axis distribution moments, usually expanded as Wigner rotation matrix element, spherical harmonics or Legendre polynomial functions.


Axis distribution moments
  See {{ ADMs }}.


MS
  Molecular symmetry group. Symmetry group classification of a molecule, isomorphic to the point group in rigid molecules. See Bunker and Jensen {cite}`bunkerMolSymm` for discussion.


PG
  Point group. Symmetry group classification of a molecule, strictly only applicable to rigid systems. See {{ MS }} for more general case.
  
  
HOMO
  Highest occupied molecular orbital. Short-hand for the outermost (highest energy) valence orbital, also often used in the form HOMO-n to number lower-lying orbitals in reverse energetic order, e.g. HOMO-1 for the penultimate valence orbital.
  

VMI
  Velocity-map imaging. Experimental technique for measuring energy and angle-resolved photoelectron "images".
  

RWP
  Rotational wavepacket. A purely rotational wavepacket (superposition of rotational eigenstates) in a molecular system, typically created via cascaded Raman interaction with a (relatively) strong IR pulse ($>10^{12}$~Wcm$^{-2}$). The resulting time-dependent molecular axis distribution can be described by a set of {{ ADMs }}.


```

```{code-cell} ipython3

```
