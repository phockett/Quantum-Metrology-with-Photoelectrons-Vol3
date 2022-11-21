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

% TODO: remove this from theory pt 1 and continue here.

% TODO: render tests. This is working in JupyterLab on Bemo (inc. \boldsymbol).

% TODO: decide on notation, and make a comment on it vs. Vol 1.

% TODO: revise text. Mostly from MF recon with some mods. May want to add some numerical examples directly here?

+++ {"tags": []}

(sec:dynamics-intro)=
## Photoionization dynamics

The core physics of photoionization has been covered extensively in the literature, and only a very brief overview is provided here with sufficient detail to introduce the metrology/reconstruction/retrieval problem; the reader is referred to Vol. 1 {cite}`hockett2018QMP1` (and refs. therein) for further details and general discussion.

% the literature listed in Appendix [\[sec:theory-lit\]](#sec:theory-lit){reference-type="ref" reference="sec:theory-lit"} for further details and general discussion.
% Technical details of the formalism applied for the reconstruction techniques discussed herein can be found in Sect. [\[sec:tensor-formulation\]](#sec:tensor-formulation){reference-type="ref" reference="sec:tensor-formulation"}.

Photoionization can be described by the coupling of an initial state of the system to a particular final state (photoion(s) plus free photoelectron(s)), coupled by an electric field/photon. Very generically, this can be written as a matrix element $\langle\Psi_i|\hat{\Gamma}(\boldsymbol{\mathbf{E}})|\Psi_f\rangle$, where $\hat{\Gamma}(\boldsymbol{\mathbf{E}})$ defines the light-matter coupling operator (depending on the electric field $\boldsymbol{\mathbf{E}}$), and $\Psi_i$, $\Psi_f$ the total wavefunctions of the initial and final states respectively.

+++

There are many flavours of this fundamental light-matter interaction, depending on system and coupling. For metrology, the focus is currently on the simplest case of single-photon absorption, in the weak field (or purturbative), dipolar regime, resulting in a single photoelectron. (For
more discussion of various approximations in photoionzation, see Refs. {cite}`Seideman2002, Seideman2001`.) In this case the core physics is well defined, and tractable (albeit non-trivial), via the separation of matrix elements into radial (energy) and angular-momentum (geometric) terms pertaining to couplings between various elements of the problem; the retrieval of such matrix elements is a well-defined problem, making use of analytic terms in combination with fitting methodologies as explored herein. Again, more extensive background and discussion can be found in {{ QM1 }}, and references therein. [Add some more refs here?]

The basic case also provides a strong foundation for extension into more complex light-matter interactions, in particular cases with shaped laser-fields (i.e. a time-dependent coupling $\hat{\Gamma}(\boldsymbol{\mathbf{E,t}})$) and multi-photon processes (which require multiple matrix elements). Note, however, that non-perturbative (strong field) light-matter interactions are, typically, not amenable to description in a separable picture in this manner. In such cases the laser field, molecular and continuum properties are strongly coupled, and are typically treated numerically in a fully time-dependent manner (although some separation of terms may work in some cases).

Underlying the photoelecton observables is the photoelectron continuum state $\left|\mathbf{k}\right>$, prepared via photoionization. The photoelectron momentum vector is denoted generally by
$\boldsymbol{\mathbf{k}}=k\mathbf{\hat{k}}$, in the MF. The ionization matrix elements associated with this transition provide the set of quantum amplitudes completely defining the final continuum scattering state,

$$\left|\Psi_f\right> = \sum{\int{\left|\Psi_{+};\bf{k}\right>\left<\Psi_{+};\mathbf{k}|\Psi_f\right> d\bf{k}}},
$$ (eq:continuum-state-vec)

where the sum is over states of the molecular ion $\left|\Psi_{+}\right>$. The number of ionic states accessed depends on the nature of the ionizing pulse and interaction. For the dipolar case,

$$\hat{\Gamma}(\boldsymbol{\mathbf{E}}) = \hat{\mathbf{\mu}}.\boldsymbol{\mathbf{E}}$$

+++

Hence,

$$\left<\Psi_{+};\mathbf{k}|\Psi_f\right> =\langle\Psi_{+};\,\mathbf{k}|\hat{\mathbf{\mu}}.\boldsymbol{\mathbf{E}}|\Psi_{i}\rangle
$$ (eq:matE-dipole)

Where the notation implies a perturbative photoionization event from an initial state $i$ to a particular ion plus electron state following absorption of a photon $h\nu$, $|\Psi_{i}\rangle+h\nu{\rightarrow}|\Psi_{+};\boldsymbol{\mathbf{k}}\rangle$, and $\hat{\mu}.\boldsymbol{\mathbf{E}}$ is the usual dipole interaction term {cite}`qOptics`, which includes a sum over all electrons $s$ defined in position space as $\mathbf{r_{s}}$:

$$\hat{\mu}=-e\sum_{s}\mathbf{r_{s}}
$$ (eq:dipole-operator)

+++

The position space photoelectron wavefunction is typically expressed in
the "partial wave" basis, expanded as (asymptotic) continuum
eignstates of orbital angular momentum, with angular momentum components
$(l,m)$ (note lower case notation for the partial wave components, distinct from upper-case for the similar terms $(L,M)$ in the observables),

$$\Psi_\mathbf{k}(\bm{r})\equiv\left<\bm{r}|\mathbf{k}\right> = \sum_{lm}Y_{lm}(\mathbf{\hat{k}})\psi_{lm}(\bm{r},k)
$$ (eq:elwf)

where $\bm{r}$ are MF electronic coordinates and
$Y_{lm}(\mathbf{\hat{k}})$ are the spherical harmonics.

Similarly, the ionization dipole matrix elements can be separated
generally into radial (energy-dependent or 'dynamical' terms) and
geometric (angular momentum) parts (this separation is essentially the
Wigner-Eckart Theorem, see Ref. {cite}`zareAngMom` for general discussion),
and written generally as (using notation similar to {cite}`Reid1991`):

$$\langle\Psi_{+};\,\mathbf{k}|\hat{\mathbf{\mu}}.\boldsymbol{\mathbf{E}}|\Psi_{i}\rangle = \sum_{lm}\gamma_{l,m}\mathbf{r}_{k,l,m}
$$ (eq:r-kllam)

+++

Provided that the geometric part of the matrix elements $\gamma_{l,m}$ -
which includes the geometric rotations into the LF arising from the dot
product in Eq. [\[eq:r-kllam\]](#eq:r-kllam){reference-type="ref"
reference="eq:r-kllam"} and other angular-momentum coupling terms - are
know, knowledge of the so-called radial (or reduced) dipole matrix
elements, at a given $k$ thus equates to a full description of the
system dynamics (and, hence, the observables).

For the simplest treatment, the radial matrix element can be
approximated as a 1-electron integral involving the initial electronic
state (orbital), and final continuum photoelectron wavefunction:

$$\mathbf{r}_{k,l,m}=\int\psi_{lm}(\bm{r},k)\bm{r}\Psi_{i}(\bm{r})d\bm{r}
$$ (eq:r-kllam-integral)

+++

% TODO: fix refs below

As noted above, the geometric terms $\gamma_{l,m}$ are analytical
functions which can be computed for a given case - minimally requiring
knowledge of the molecular symmetry and polarization geometry, although
other factors may also play a role (see Sect.
[\[sec:full-tensor-expansion\]](#sec:full-tensor-expansion){reference-type="ref"
reference="sec:full-tensor-expansion"} for details).

% TODO: add some numerical examples here?

The photoelectron angular distribution (PAD) at a given $(\epsilon,t)$
can then be determined by the squared projection of
$\left|\Psi_f\right>$ onto a specific state
$\left|\Psi_{+};\bf{k}\right>$ (see Sect.
[\[sec:theoretical-techniques\]](#sec:theoretical-techniques){reference-type="ref"
reference="sec:theoretical-techniques"}), and therefore the amplitudes
in Eq. [\[eq:r-kllam\]](#eq:r-kllam){reference-type="ref"
reference="eq:r-kllam"} also determine the observable anisotropy
parameters $\beta_{L,M}(\epsilon,t)$ (Eqn.
[\[eq:AF-PAD-general\]](#eq:AF-PAD-general){reference-type="ref"
reference="eq:AF-PAD-general"}). (Note that the photoelectron energy
$\epsilon$ and momentum $k$ are used somewhat interchangeably herein,
with the former usually preferred in reference to observables.) Note,
also, that in the treatment above there is no time-dependence
incorporated in the notation; however, a time-dependent treatment
readily follows, and may be incorporated either as explicit
time-dependent modulations in the expansion of the wavefunctions for a
given case, or implicitly in the radial matrix elements. Examples of the
former include, e.g. a rotational or vibrational wavepacket, or a
time-dependent laser field. The rotational wavepacket case is discussed
herein (see Sect.
[\[sec:full-tensor-expansion\]](#sec:full-tensor-expansion){reference-type="ref"
reference="sec:full-tensor-expansion"}). The radial matrix elements are
a sensitive function of molecular geometry and electronic configuration
in general, hence may be considered to be responsive to molecular
dynamics, although they are formally time-independent in a
Born-Oppenheimer basis - for further general discussion and examples see
Ref. [@wu2011TimeresolvedPhotoelectronSpectroscopy]; discussions of more
complex cases with electronic and nuclear dynamics can be found in Refs.
[@arasaki2000ProbingWavepacketDynamics; @Seideman2001; @Suzuki2001; @Stolow2008].

Typically, for reconstruction experiments, a given measurement will be
selected to simplify this as much as possible by, e.g., populating only
a single ionic state (or states for which the corresponding observables
are experimentally energetically-resolvable), and with a bandwidth
$d\bf{k}$ which is small enough such that the matrix elements can be
assumed constant. Importantly, the angle-resolved observables are
sensitive to the magnitudes and (relative) phases of these matrix
elements, and can be considered as angular interferograms (Fig.
[1](#781808){reference-type="ref" reference="781808"} top right).

```{code-cell} ipython3

```