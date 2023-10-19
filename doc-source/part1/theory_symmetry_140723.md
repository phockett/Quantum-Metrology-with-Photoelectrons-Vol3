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

Subsections for photoionization theory

- 14/07/23 
    - Symmetry moved to separate section
    - Text/formalism review in progress...
    
- 22/04/23 Added symmetry section, and numerical example for selection rules only.
   - `\boldsymbol` rendering broken in current builds for Photoionization Theory page (Firefox), possibly since adding computational example with symmetry? Rendering OK in Ice Dragon however. Sigh.
- 22/11/22 Basics in place, needs some work and numerical examples to add.

---

% TODO: render tests. This is working in JupyterLab on Bemo (inc. \boldsymbol). NOW fixed as per below, issues with PDF builds too.

% TODO: decide on notation, and make a comment on it vs. Vol 1.

% TODO: revise text. Mostly from MF recon with some mods. May want to add some numerical examples directly here?

TODO: fix/generalise intro theory and also update notation for LF vs. MF case above, or discuss. May be better to remove some of this and just refer to Vol. 1?

+++ {"tags": ["remove-cell"]}

---

Rendering issues notes (hidden cell)

Build fixed for no `\bm` case, subs as:

- \hat{\mathbf{\mu}} >> \hat{\boldsymbol{\mu}}

- \boldsymbol{\mathbf{E}} >> \boldsymbol{\mathrm{E}}. May only be an issue if bm loaded? Ah, yes - this is OK without bm, but get errors at `\bm` of course.

- \bm >> \boldsymbol, have this only for \bm{r} it seems, may want \mathrm here too? NEED TO LOOK CAREFULLY - can use former in general (scalar) case (or just plain r), latter in vector case.

- \mathbf{\rho} >>> \boldsymbol{\rho} (OK in HTML, not in PDF)

$$1: \hat{\Gamma}(\boldsymbol{\mathbf{E}}) = \hat{\mathbf{\mu}}.\boldsymbol{\mathbf{E}}$$

$$2: \hat{\Gamma}(\boldsymbol{\mathbf{E}}) = \mathbf{\mu}.\boldsymbol{\mathbf{E}}$$

$$3: \hat{\Gamma}(\boldsymbol{\mathbf{E}}) = \mu.\boldsymbol{\mathbf{E}}$$

$$4: \hat{\Gamma}(\boldsymbol{\mathbf{E}}) = \bm{\mu}.\boldsymbol{\mathbf{E}}$$

$$5: \hat{\Gamma}(\boldsymbol{\mathbf{E}}) = \boldsymbol{\mu}.\boldsymbol{\mathbf{E}}$$

$$6: \hat{\Gamma}(\boldsymbol{\mathbf{E}}) = \hat{\boldsymbol{\mu}}.\boldsymbol{\mathbf{E}}$$

Without bm package, 3 - 6 are all OK. 'mathbf' seems to be an issue?  Missing fonts - renders as a '?' in a square and gives error like `! Extended mathchar used as mathchar (14799967).`?

With bm package, only 3 works (and 4 renders as $\mu0$)

$$7: \hat{\Gamma}(\boldsymbol{\mathbf{E}}) = \mathbf{\hat{\mu}}.\boldsymbol{\mathbf{E}}$$

With bm package also issues with $\boldsymbol{\mathbf{E}}$, gives `! Improper alphabetic constant`. Is $\boldsymbol{\mathrm{E}}$ OK? In previous vol have $\mathbf{r}$ for vector case, and plain $r$ otherwise.

---

+++

(sec:theory:symmetry-intro)=
# Symmetry in photoionization

Symmetry in photoionization is discussed in detail in {{ QM1 }} (Sect. 2.2.3.3). Herein a brief review is given, with a focus on using symmetry in matrix element retrieval problems. For further details, see {{ QM1 }}; for a more general discussion of symmetry in molecular spectroscopy see the textbook by  Bunker and Jensen {cite}`bunkerMolSymm`, and the specific case of photoionization is expanded on in the work of Signorell and Merkt {cite}`Signorell1997`. (For application to symmetrized harmonics see {numref}`Sect. %s <sec:theory:sym-harm-into>`.)

+++

In general, for the dipole matrix element to be non-zero the direct product of the initial state, final state and dipole operator symmetries must contain the totally symmetric representation of the molecular symmetry ({{ MS }}) group, which is isomorphic to the point group ({{ PG }}) in rigid molecules. This general case can be written as:

$$
\Gamma_{rve}^{f}\otimes\Gamma_{dipole}\otimes\Gamma_{rve}^{i}\supset\Gamma^{s}
$$ (eq:rovib-selection-symm)

Where $\Gamma_{rve}$ is the rovibronic symmetry of the system (i.e. total symmetry excluding spin), with the $i/f$ superscript denoting
initial and final states respectively. $\Gamma^{s}$ is the totally symmetric representation in the appropriate molecular symmetry group,
and $\Gamma_{dipole}$ is the symmetry of the dipole operator.

For the specific case of photoionization the final state is split into the symmetry species of the ion and the photoelectron {cite}`Signorell1997`:

$$
\Gamma^{e}\otimes\Gamma_{rve}^{+}\otimes\Gamma_{dipole}\otimes\Gamma_{rve}^{i}\supset\Gamma^{s}
$$ (eq:ionization-symm)

This is, essentially, a statement of the limiting case of Eq. {eq}`eq:matE-dipole` (see also alternative forms of Eqs. {eq}`eq:r-kllam`, {eq}`eq:r-kllam-integral`), which defines the symmetry requirements for the overlap integral to be non-zero (although does not indicate that it will be non-zero for a given system).

In the reconstruction experiments discussed herein, this general form can be often be further simplified. In particular, assuming a full Born-Oppenheimer separation of dynamics, the problem can be treated within the static {{ PG }} of the system, and only the electronic state symmetries need to be taken into account. In practice, this treatment is appropriate for cases with separable rotational wavepackets, and may also be a reasonable approximation for cases with vibronic wavepackets in cases where the nuclear excursions are relatively small and/or can be treated as linear combinations over a set of symmetrized basis functions. Within this approximation the general symmetry requirements can be written as:

$$
\Gamma^{e(X)}\otimes\Gamma_{e}^{+}\otimes\Gamma_{dipole}\otimes\Gamma_{e}^{i}\supset\Gamma^{s}
$$ (eq:ionization-symm-electronic)

And $\Gamma^{e(X)}$ indicates that the continuum symmetries are expressed in a basis of symmetrized harmonics ({numref}`Sect. %s <sec:theory:sym-harm-into>`). From Eq. {eq}`eq:ionization-symm-electronic`, the set of allowed matrix elements for a given ionization event can be expressed, in terms of the allowed set of symmetrized harmonics $X_{hl}^{\Gamma\mu*}(\theta,\phi)$, or (equivalently) the usual partial wave basis expressed in spherical harmonics $Y_{l,\lambda}(\theta,\phi)$, and a set of associated symmetrization coefficients $b_{hl\lambda}^{\Gamma\mu}$.

A brief numerical example is given below, and a more detailed treatment for a range of photoionization cases forms the second half of the book, see {numref}`Chapter %s <chpt:extracting-matrix-elements-overview>` for details.

% Note {ref} with name fails for nested sections.
% {ref}`sec:extracting-matrix-elements-overview` for details.

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

# Compute hamronics for Td, lmax=4
sym = 'D2h'
lmax=4

symObj = symHarm(sym,lmax)

# Allowed terms and mappings are given in 'dipoleSyms'
symObj.dipole['dipoleSyms']
```

```{code-cell} ipython3
# Setting the symmetry for the neutral and ion allows direct products to be computed, 
# and allowed terms to be determined.

sNeutral = 'A1g'
sIon = 'B2u'

symObj.directProductContinuum([sNeutral, sIon])

# Results are pushed to self.continuum, in dictionary and Pandas DataFrame formats, 
# and can be manipulated using standard functionality.
# The subset of allowed values are also set to a separate DataFrame and list.
symObj.continuum['allowed']['PD']
```

```{code-cell} ipython3
# Ylm basis table with the Character values limited to those defined 
# in self.continuum['allowed']['PD'] Target column
symObj.displayXlm(symFilter = True)  
```

```{code-cell} ipython3

```
