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
    - Added mods from VM, 
        - 3.12 - should be starred.
        - 3.13 - should be 3.8 abs squared. (REWROTE FOR NOW, but want coherence here, may want to show both forms...?)
    - Compilation in updated Docker builds (3d-140723 container) seems to fix `\boldsymbol` issue, with OR WITHOUT symmetry section in same doc.
    - Spellchecker broken in this build?
    
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

(sec:dynamics-intro)=
# Photoionization dynamics

The core physics of photoionization has been covered extensively in the literature, and only a very brief overview is provided here with sufficient detail to introduce the metrology/reconstruction/retrieval problem; the reader is referred to {{ QM1 }} (and references therein) for further details and general discussion.
 
%  ## General forms  - Promoted to full section now symmetry section has moved.

Photoionization can be described by the coupling of an initial state of the system to a particular final state (photoion(s) plus free photoelectron(s)), coupled by an electric field/photon. Very generically, this can be written as a matrix element $\langle\Psi_f|\hat{\Gamma}(\boldsymbol{\mathbf{E}})|\Psi_i\rangle$, where $\hat{\Gamma}(\boldsymbol{\mathbf{E}})$ defines the light-matter coupling operator (depending on the electric field $\boldsymbol{\mathbf{E}}$), and $\Psi_i$, $\Psi_f$ the total wavefunctions of the initial and final states respectively.

+++

There are many flavours of this fundamental light-matter interaction, depending on system and coupling. For metrology, the focus is currently on the simplest case of single-photon absorption, in the weak field (or perturbative), dipolar regime, resulting in a single photoelectron. (For more discussion of various approximations in photoionzation, see Refs. {cite}`Seideman2002, Seideman2001`.) In this case the core physics is well defined, and tractable (albeit non-trivial), via the separation of matrix elements into radial (energy) and angular-momentum (geometric) terms pertaining to couplings between various elements of the problem; the retrieval of such matrix elements is then a well-defined problem in general, achieved by making use of the analytic geometric terms in combination with fitting methodologies for the unknown radial matrix elements, and this is the approach explored herein. Again, more extensive background and discussion can be found in {{ QM1 }}, and references therein. Note, however, that whilst the general approach taken here is sound, many outstanding questions remain regarding the information content required for such an approach to be successful, and if other limitations prevent a unique set of solutions to be found in a given case (e.g. symmetry restrictions, phase ambiguities) - such questions are explored further herein, particularly in the case studies presented {{ PARTII }}.

% [TODO: Add some more refs here?]

The basic case also provides a strong foundation for extension into more complex light-matter interactions, in particular cases with shaped laser-fields (i.e. a time-dependent coupling $\hat{\Gamma}(\boldsymbol{\mathbf{E,t}})$) and multi-photon processes (which require multiple matrix elements, and/or different approximations). Note, however, that non-perturbative (strong field) light-matter interactions are, typically, not amenable to description in a separable picture in this manner. In such cases the laser field, molecular and continuum properties are strongly coupled, and are typically treated numerically in a fully time-dependent manner (although some separation of terms may work in some cases, depending on the system and interaction(s) at hand).

Underlying the photoelecton observables is the photoelectron continuum state $\left|\mathbf{k}\right>$, prepared via photoionization. The photoelectron momentum vector is denoted generally by
$\boldsymbol{\mathbf{k}}=k\mathbf{\hat{k}}$, in the molecular frame ({{ MF }}). The ionization matrix elements associated with this transition provide the set of quantum amplitudes completely defining the final continuum scattering state,

$$\left|\Psi_f\right> = \sum{\int{\left|\Psi_{+};\bf{k}\right>\left<\Psi_{+};\mathbf{k}|\Psi_f\right> d\bf{k}}},
$$ (eq:continuum-state-vec)

where the sum is over states of the molecular ion $\left|\Psi_{+}\right>$. The number of ionic states accessed depends on the nature of the ionizing pulse and interaction. For the dipolar case,

$$\hat{\Gamma}(\boldsymbol{\mathbf{E}}) = \hat{\boldsymbol{\mu}}.\boldsymbol{\mathbf{E}}$$ (eq:def-dipole-operator)

+++

Hence,

$$\left<\Psi_{+};\mathbf{k}|\Psi_f\right> =\langle\Psi_{+};\,\mathbf{k}|\hat{\boldsymbol{\mu}}.\boldsymbol{\mathbf{E}}|\Psi_{i}\rangle
$$ (eq:matE-dipole)

Where the notation implies a perturbative photoionization event from an initial state $i$ to a particular ion plus electron state following absorption of a photon $h\nu$, $|\Psi_{i}\rangle+h\nu{\rightarrow}|\Psi_{+};\boldsymbol{\mathbf{k}}\rangle$, and $\hat{\mu}.\boldsymbol{\mathbf{E}}$ is the usual dipole interaction term {cite}`qOptics`, which includes a sum over all electrons $s$ defined in position space as $\mathbf{r_{s}}$:

$$\hat{\mu}=-e\sum_{s}\mathbf{r_{s}}
$$ (eq:dipole-operator)

+++

The position space photoelectron wavefunction is typically expressed as a {term}`partial wave expansion`, expanded as (asymptotic) continuum
eignstates of orbital angular momentum, with angular momentum components
$(l,m)$,

$$\Psi_\mathbf{k}(\boldsymbol{r})\equiv\left<\boldsymbol{r}|\mathbf{k}\right> = \sum_{lm}Y_{lm}(\mathbf{\hat{k}})\psi_{lm}(\boldsymbol{r},k)
$$ (eq:elwf)

where $\boldsymbol{r}$ are MF electronic coordinates and
$Y_{lm}(\mathbf{\hat{k}})$ are the spherical harmonics. Note the lower-case notation for the partial wave angular-momentum components, distinct from upper-case for the similar terms $(L,M)$ in the observables ({ref}`Sect. %s <sect:theory:observables>`).

Similarly, the ionization dipole matrix elements can be separated
generally into radial (energy-dependent or 'dynamical' terms) and
geometric (angular momentum) parts (this separation is essentially the
Wigner-Eckart Theorem, see Ref. {cite}`zareAngMom` for general discussion),
and written generally as (using notation similar to {cite}`Reid1991`):

$$\langle\Psi_{+};\,\mathbf{k}|\hat{\boldsymbol{\mu}}.\boldsymbol{\mathbf{E}}|\Psi_{i}\rangle = \sum_{lm}\gamma_{l,m}\mathbf{r}_{k,l,m}
$$ (eq:r-kllam)

+++

Provided that the geometric part of the matrix elements $\gamma_{l,m}$ -
which includes the geometric rotations into the {{ LF }} arising from the dot
product in Eq. {eq}`eq:r-kllam` and other angular-momentum coupling terms - are
know, knowledge of the so-called radial (or reduced) dipole matrix
elements, at a given $k$ thus equates to a full description of the
system dynamics (and, hence, the observables). Determination of these radial matrix elements - which are complex quantities with magnitudes and phases - is the aim of the reconstruction methodologies discussed herein (see {numref}`Sect. %s <chpt:numerical-details>`).

For the simplest treatment, the radial matrix element can be
approximated as a 1-electron integral involving the initial electronic
state (orbital), and final continuum photoelectron wavefunction:

$$\mathbf{r}_{k,l,m}=\int\psi_{lm}^{*}(\boldsymbol{r},k)\boldsymbol{r}\Psi_{i}(\boldsymbol{r})d\boldsymbol{r}
$$ (eq:r-kllam-integral)

+++

% TODO: fix refs below

As noted above, the geometric terms $\gamma_{l,m}$ are analytical
functions which can be computed for a given case - minimally requiring
knowledge of the molecular symmetry and polarization geometry, although
other factors may also play a role (see {numref}`Sect. %s <sec:full-tensor-expansion>` for details).

% TODO: add some numerical examples here?
% TODO: general form to link to BLM expansion.

The photoelectron angular distribution ({{ PADs }}) at a given $(\epsilon,t)$
can then be determined by the squared projection of
$\left|\Psi_f\right>$ onto a specific state
$\left|\Psi_{+};\bf{k}\right>$; very generally this can be written in terms of the energy and angle-resolved observable, which arises as the coherent square:

% $$
% I(\epsilon,\theta,\phi)=\langle\Psi_{f}|\Psi_{f}\rangle
% $$ (eq:matE-sq-general)

$$
I(\epsilon,\theta,\phi)=\left<\Psi_f|\Psi_{+};\mathbf{k}\right>\left<\Psi_{+};\mathbf{k}|\Psi_f\right>
$$ (eq:matE-sq-general)

Expansion in terms of the components of the matrix elements as detailed above then yields a separation into radial and angular components (see {{ QM1 }}, Sect. 2.1 for a full derivation), which can be written (at a single energy) as (following Eq. 2.45 of {{ QM1 }}):

$$
I(\theta,\phi;\,k)=\sum_{ll'}\sum_{\lambda\lambda'}\sum_{mm'}\gamma_{\alpha\alpha_{+}l\lambda ml'\lambda'm'}\boldsymbol{r}_{kl\lambda}\boldsymbol{r}_{kl'\lambda'}e^{i(\eta_{l\lambda}(k)-\eta_{l'\lambda'}(k))}Y_{lm}(\hat{k})Y_{l'm'}^{*}(\hat{k})
$$ (eq:I-reduced-LF-2_45-vol1)

% TODO: fix/generalise this, also update notation for LF vs. MF case above, or discuss. May be better to remove some of this and just refer to Vol. 1?

In this form $\alpha$ denotes all other quantum numbers required to define the initial state, and $\alpha_{+}$ the final state of the molecular ion. The radial matrix elements $\boldsymbol{r}_{kl\lambda}$, denote an integral over the radial part of the wavefunctions, in this case labelled by the {{ MF }} quantum numbers, and the associated scattering phase is given by $\eta_{l\lambda}(k)$ (i.e. the matrix elements are written in magnitude-phase form, rather than complex form). The $\gamma$ term denotes a general set of geometric paramters arising from the coherent square. A tensor form is also given herein, see {numref}`Sect. %s <sec:full-tensor-expansion>`, and includes a full breakdown of these terms and details of numerical implementations. 

Comparison of Eq. {eq}`eq:I-reduced-LF-2_45-vol1` with Eq. {eq}`eq:AF-PAD-general` indicates that the amplitudes
in Eq. {eq}`eq:r-kllam` also determine the observable {{ betas }} $\beta_{L,M}(\epsilon,t)$ (Eq.
{eq}`eq:AF-PAD-general`), which basically collect all the terms in Eq. {eq}`eq:I-reduced-LF-2_45-vol1` and the product over spherical harmonics, into a resultant set of $(L,M)$ parameters which describe the observable {{ PADs }}. (Note that the photoelectron energy
$\epsilon$ and momentum $k$ are used somewhat interchangeably herein,
with the former usually preferred in reference to observables.) Further discussion of the observables, including computation and form of these observables, can be found in {numref}`Sect. %s: <sect:theory:observables>`

The radial matrix elements - hence observables - are
a sensitive function of molecular geometry and electronic configuration
in general, as they depend on the overlap of the initial and final state wavefunctions, which includes the ionization continuum (scattering wavefunction) of the photoelectron.
Hence, they may be considered to be responsive to molecular
dynamics as well as photoionization dynamics, although they are formally time-independent in a
Born-Oppenheimer basis. For further general discussion and examples see
Ref. {cite}`wu2011TimeresolvedPhotoelectronSpectroscopy` and {{ QM1 }}; discussions of more
complex cases with electronic and nuclear dynamics can be found in Refs.
{cite}`arasaki2000ProbingWavepacketDynamics,Seideman2001,Suzuki2001,Stolow2008`.

Note, also, that in the treatment above there is no time-dependence
incorporated in the notation; however, a time-dependent treatment
readily follows, and may be incorporated either as explicit
time-dependent modulations in the expansion of the wavefunctions for a
given case, or implicitly in the radial matrix elements. Examples of the
former include, e.g. a rotational or vibrational wavepacket, or a
time-dependent laser field. The rotational wavepacket case is discussed
herein (see {numref}`Sect. %s <sec:full-tensor-expansion>`). 


Typically, for reconstruction experiments, a given measurement will be
selected to simplify this as much as possible by, e.g., populating only
a single ionic state (or states for which the corresponding observables
are experimentally energetically-resolvable), and with a bandwidth
$d\bf{k}$ which is small enough such that the matrix elements can be
assumed constant over the observation window. Importantly, the angle-resolved observables are
sensitive to the magnitudes and (relative) phases of these matrix
elements - as emphasised in the magnitude-phase form of Eq. {eq}`eq:I-reduced-LF-2_45-vol1` - and can be considered as angular interferograms. It is the interferometric nature of the {{ PADs }} which enables a phase-sensitive reconstruction protocol to be pursued.

+++

% TODO: explicitly write out general form and discuss a bit further, inc. link to observables and tensor form later.
% 30/11/22 Added general form as per eq. 2.45 in QM1, but may want to modify a bit, esp. LF vs. AF notation to match channel funcs later.

```{code-cell} ipython3

```
