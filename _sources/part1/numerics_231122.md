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

Numerical details to go here? Further details of the numerical implementations - base packages, conventions and refs - to go here or in appendix?

OR NEST in software overview?

- 27/04/23 adding text based on MF recon manuscript, and fitting intro stuff now in place in Part 2. NOTE also chpt. 2 now has general software intro, so keep this more specific.
- 23/11/22 basic stub. See Observables section for some mentions already, also Appendix 9.5 in MF recon manuscript.

To include here:

- More on simulation? E.g. example for N2, currently in fitting chpt, but don't show/discuss ADMs or observables in much detail.
- Fitting methodologies. FLOW CHARTS - on Bemo?
- More on ab initio methods? Not really the main focus however.

RENAME CHPT?  Maybe "Numerical methodologies for extracting matrix elements"?

+++

(chpt:numerical-details)=
# Numerical methodologies for extracting matrix elements

Following the tensor notation outline in {numref}`Sect. %s <sec:tensor-formulation>`, the complete quantum metrology of a photoionization event (aka. a "complete" photoionization experiment) can be characterized as recovery of the matrix elements $I^{\zeta}(\epsilon)$ (per Eqs. {eq}`eqn:channel-fns`, {eq}`eqn:I-zeta`) from the experimental measurements or, equivalently, the density matrix $\mathbf{\rho}^{\zeta\zeta'}$ (Eqs. {eq}`eqn:full-density-mat` - {eq}`eqn:beta-density-mat`). (For further discussion and background, see Refs. {cite}`Reid2003,kleinpoppen2013perfect` and {{ QM1 }}.) This may be possible provided the channel functions are known, and the information content of the measurements is sufficient. 

For schemes making use of molecular alignment, or other control methods, the contribution of these parameters to the channel functions must, therefore, be accounted for. In general, these contributions may be computed and/or obtained from experiment. For the rotational wavepacket case, this can be considered as the requirement for the determination of the molecular axis distributions ({{ ADMs }}): this can be treated as a reduced-dimensionality MF signal retrieval problem, with sets of computed {{ ADMs }} forming the basis set for the fitting, and this forms the first step in both the generalised bootstrapping method explored herein. (Note here that the matrix elements are assumed to be time-independent, although that may not be the case for the most complicated examples including vibronic dynamics, see {{ QM2 }} for further discussion on this point.) 

% (Sect. \ref{sec:bootstrapping}) and matrix inversion techniques (Sect. \ref{sec:matrix-inv-intro}).

% For the rotational wavepacket case, this is discussed in Sect. \ref{sec:RWPs}. 

Of particular import for matrix element retrieval is the phase-sensitive nature of the observables ({numref}`Sect. %s <sect:theory:observables>`), which is required in order to obtain partial wave phase information. {{ PADs }} can also be considered as angular interferograms, and reconstruction can be considered conceptually similar to other phase-retrieval problems, e.g. optical field recovery with techniques such as FROG {cite}`trebino2000FrequencyResolvedOpticalGating`, and general quantum tomography {cite}`MauroDAriano2003`. 

+++ {"tags": ["remove-cell"]}

{figure} flow_charts_MFrecon/bootstrap_flowchart_290822.gv.png
FAILS FOR PDF, although OK in HTML - needs to be in ../images to be copied to build dir for latex...?

+++

```{figure} ../images/bootstrap_flowchart_290822.gv.png
---
name: fig-bootstrap-fitting-diag
---
Outline of the 2-stage generalised bootstrap matrix element retrieval protocol.
```

+++

## Fitting methodologies

In general, the extraction of parameters from a data set can be viewed as a general minimization (fitting) problem. This type of treatment is versatile, and can be multi-stage depending on the complexity of the problem. For the generalised bootstrapping method, the treatment of photoionization data is split into two types of fit, as shown in {numref}`fig-bootstrap-fitting-diag`. Firstly, a linear fitting stage to retrieve the molecular axis distribution, characterised by a set of {{ ADMs }} (see {numref}`Sect. %s <sec:theory:AF-alignment-term>` for details); secondly, a non-linear fitting stage to retrieve the complex-valued matrix elements.

In terms of the data, the 1st stage can be written as:

$$
\bar{\beta}_{L,M}^{u}(\epsilon,t)=\sum_{K,Q,S}A_{Q,S}^{K}(t)\bar{C}_{KQS}^{LM}(\epsilon)
$$ (eqn:beta-convolution-C)

And the 2nd stage as per Eqs. {eq}`eqn:channel-fns` and {eq}`eq:BLM-tensor-AF` for the AF case:

$$
\bar{\beta}_{L,M}^{u}(\epsilon,t)=\sum_{\zeta,\zeta'}\bar{\varUpsilon}_{L,M}^{u,\zeta\zeta'}(t)\mathbb{I}^{\zeta\zeta'}(\epsilon)
$$

In these forms, the terms are: 

1. $A_{Q,S}^{K}(t)$, the set of {{ ADMs }} defining the molecular alignment, and associated parameters $\bar{C}_{KQS}^{LM}(\epsilon)$.
2. $\bar{\varUpsilon}_{L,M}^{u,\zeta\zeta'}(t)$, the channel functions in the {{ AF }} (Eq. {eq}`eq:BLM-tensor-AF`, and matrix elements $\mathbb{I}^{\zeta\zeta'}(\epsilon)$.

Hence stage (2) relies on the inputs of stage (1), i.e. the {{ ADMs }}; and the parameters in stage (1) can be determined via fitting the data (linear regression) making use of computed sets of $A_{Q,S}^{K}(t)$ as a function of experimental parameters (laser fluence and rotational temperature). In this case, a range of {{ ADMs }} "basis sets" are computed, and the best match to the experimental data chosen - more details are discussed in Sect. XX. In a similar manner, the 2nd stage makes use of a known basis set - the channel functions - but a non-linear fit is required to determine the set of matrix elements, see Sect. XX.

Finally, it is also of note that, although the case herein focusses on rotational wavepackets as a control parameter, the same general approach can be applied to other cases, e.g. fitting {{ MF }} {{ PADs }} directly (for which only the 2nd stage is required), fitting {{ PADs }} obtained via rotational state-resolved transitions, with shaped laser pulses and so on, as detailed in {{ QM12 }}. Although only rotational wavepacket cases are illustrated in this work (see {numref}`Chpt. %s <sec:extracting-matrix-elements-overview>`), by suitable choice of dataset and channel functions many other experimental schemes may be modelled and analysed; the {{ PEMtk_repo }} is designed with  this flexibility in mind.

+++

### Computation and linear fitting for alignment characterisation

% Moderately adapted from MF recon manuscript - may want to rework further and add some numerical examples here (or elsewhere).

Efforts to align and orient molecules in recent decades have
% discussed in the previous sections necessarily 
led to detailed studies of the rotational dynamics of molecules after interaction with a non-resonant femtosecond laser pulse. A significant outcome of these studies has been the development of a reliable model capable of accurate simulations of rotational wavepacket dynamics that quantitatively agree with experimental results [REFS]. By measurement of a signal from a time evolving rotational wavepacket, this ability to accurately simulate the wavepacket dynamics can be used to reconstruct the measured signal in the molecular frame. Since in this case the time resolved measurement constitutes a set of measurements of the same quantity from a variety of molecular axes distributions, it is reasonable to conclude that if the axes distributions are known, and provided a large enough space of orientations is explored by the molecule over the experimental time window, the molecular frame signal should be extractable. 

This is relatively straight forward for a signal that is a single number (scalar) in the MF for a given polarization of the light, such as the photoionization yield. Such a signal may, in general, be expressed as an expansion,

$$4
S(\theta,\chi)=\sum_{jk}C_{jk}D^{j}_{0k}(\theta,\chi),
$$ (eq:mfrealsig)

where $\theta$ and $\chi$ are the MF spherical polar and azimuthal angles of the linearly polarized electric field vector generating the signal; $C_{jk}$ are unknown expansion coefficients; and $D^{j}_{0k}$ are the Wigner D-Matrix elements, a basis on the space of orientations. A time resolved measurement of $S$ from a rotational wavepacket is the quantum expectation value of this expression,

$$
\langle S \rangle(t) = \sum_{jk}C_{jk}\langle D^{j}_{0k} \rangle (t).
$$ (eq:St-Cjk)

Since the rotational wavepacket can be accurately simulated, the $\langle D^{j}_{0k} \rangle (t)$ are considered known. The time resolved signal $\langle S \rangle(t)$ being measured, the unknown coefficients $C_{jk}$ can be determined by linear regression, and the molecular frame signal in Eqn.~\ref{eq:mfrealsig} constructed. In this form the method was initially applied to strong field ionization and dubbed Orientation Reconstruction through Rotational Coherence Spectroscopy (ORRCS) {cite}`makhija2016ORRCS,wang2017ORRCS`.
It has since been applied to strong field ionization of various molecules {cite}`sandor2018ORRCS,sandor2019ORRCS,wangjam2021ORRCS`,
strong field dissociation {cite}`lam2020ORRCS` and few-photon ionization {cite}`lam2022ORRCS`. 
% 09/03/23: Added below for referee, where refs he2018RealTimeObservationMolecular, he2020MeasuringRotationalTemperature,wang2022RotationalEchoSpectroscopy were per referee recommendations.
(A large range of other experimental methods have also addressed alignment and orientation dependence and retrieval, other recent examples include Coulomb-explosion imaging {cite}`Underwood2015`, high-harmonic spectroscopy {cite}`he2018RealTimeObservationMolecular, he2020MeasuringRotationalTemperature`, optical imaging {cite}`Loriot2008` and rotational echo spectroscopy {cite}`wang2022RotationalEchoSpectroscopy`, see Refs. {cite}`Ramakrishna2013,koch2019QuantumControlMolecular` for further discussion.)

% The case of PADs is a more challenging one, since they are not generally described by Eq.~\ref{eq:mfrealsig}. Instead, both LFPADs and MFPADs are determined by the radial dipole matrix elements as described above (\textbf{refer to section 3 here!}). The authors of this manuscript, with a number of collaborators, demonstrated that these matrix elements can also be retrieved for one-photon ionisation of N$_2$ by time resolved measurements of LFPADs from a rotational wavepacket. This method is focus of sections X and Y (\textbf{refer to apprpriate section(s)!}) below, with additional details and results provided on the case of radial matrix element extraction for N$_2$.   In follow up work, it was shown that for molecules with $D_{nh}$ point group symmetry the retrieval of the MFPAD is possible directly, bypassing the radial matrix elements. 

The case of PADs is a more challenging one, since they are not generally described by Eqn.~\ref{eq:mfrealsig}. Instead, both {{ AF }} and {{ MF }} {{ PADs }} are determined by the radial dipole matrix elements. However, the correspondence of the problem with an equation of the form of Eqn. \ref{eq:St-Cjk} - essentially a convolution - can be made. This is discussed in detail in Ref. {cite}`Underwood2000`. In the current case Eqs. {eq}`eqn:channel-fns` and {eq}`eq:BLM-tensor-AF` can be rewritten in a similar form to Eq. {eq}`eq:St-Cjk` by explicitly separating out the axis distribution moments $A_{Q,S}^{K}(t)$ and collapsing all other terms. The case of photoionization from a time-dependent ensemble can then be reparameterized as indicated in Eq. {eq}`eqn:beta-convolution-C`.

% (cf. also Eqn. \ref{eq:BLM-tensor-AF}):

% \begin{equation}
% \beta_{L,M}^{u}(t)=\sum_{K,Q,S}(\sum_{\zeta,\zeta'}\bar{\varUpsilon}_{L,M}^{u,\zeta\zeta'}\mathbb{I}^{\zeta\zeta'})A_{Q,S}^{K}(t)

% \label{eqn:beta-convolution}
% \end{equation}

% Where $\bar{\varUpsilon}$ is as per Eqn. \ref{eqn:channel-fns} except for the omission of the ADMs. 
% and the case of photoionization from a time-dependent ensemble can be reparametrized as:

% \begin{equation}
% \bar{\beta}_{L,M}^{u}(\epsilon,t)=\sum_{K,Q,S}\bar{C}_{KQS}^{LM}(\epsilon)A_{Q,S}^{K}(t)
% \label{eqn:beta-convolution-C}
% \end{equation}

% [NOTE: this now preempts the matrix inversion formalism, so may want to change this, or that, to avoid repetition] UPDATE - now fixed notation and refer to that eqn instead of duplicating.

Here the set of axis distribution moments can thus be viewed as modulating all observables $\beta_{L,M}^{u}(t)$. The unknowns, $\bar{C}_{KQS}^{LM}$ and axis distribution moments $A_{Q,S}^{K}(t)$, can be retrieved in a similar manner to that discussed for the simpler scalar observable case above, i.e. via linear regression with simulated rotational wavepackets. 

In practice this equates to (accurately) simulating rotational wavepackets, hence obtaining the corresponding $A_{Q,S}^{K}(t)$ parameters (expectation values), as a function of laser fluence and rotational temperature. Given experimental data, a 2D uncertainty (or error) surface in these two fundamental quantities can then be obtained from a linear regression for each set of $A_{Q,S}^{K}(t)$. The closest set of parameters to the experimental case is then determined by selection of the best results (smallest uncertainty) from such a parameter-space mapping, which constitutes determination of both the rotational wavepacket (hence $A_{Q,S}^{K}(t)$) and $\bar{C}_{KQS}^{LM}(\epsilon)$. Optimally, the corresponding physical properties can be cross-checked with other experimental estimates for additional confirmation of the fidelity of the protocol, although this may not always be possible. Note that, in this case, the photoionization dynamics are phenomenologically described by the real parameters $\bar{C}_{KQS}^{LM}$, but details of the matrix elements are not obtained directly.
% ; however, these parameters can be further used for the matrix inversion method (Sect. \ref{sec:matrix-inv-intro}), and are formally defined therein (Eqn. \ref{eq:C-AF}).

% 22/08/22 - removed this for now, but could incorporated into Sect 4.1.1
% The authors of this manuscript, with a number of collaborators, demonstrated that these matrix elements can also be retrieved for one-photon ionisation of N$_2$ by time resolved measurements of LFPADs from a rotational wavepacket. This method is focus of sections X and Y (\textbf{refer to apprpriate section(s)!}) below, with additional details and results provided on the case of radial matrix element extraction for N$_2$.   In follow up work, it was shown that for molecules with $D_{nh}$ point group symmetry the retrieval of the MFPAD is possible directly, bypassing the radial matrix elements. 

```{code-cell} ipython3
# Numerical examples of ADMs and rotational wavepackets here? Some also now in fitting basis set chpt.
```

### Non-linear fitting for matrix elements

The nature of the photoionization problem suggests that a fitting approach can work, in general, which can be expressed (for example) in the standard way as a (non-linear) least-squares minimization problem:

$$
\chi^{2}(\mathbb{I}^{\zeta\zeta'})=\sum_{u}\left[\beta^{u}_{L,M}(\epsilon,t;\mathbb{I}^{\zeta\zeta'})-\beta^{u}_{L,M}(\epsilon,t)\right]^{2}
$$ (eq:chi2-I)

where $\beta^{u}_{L,M}(\epsilon,t;\mathbb{I}^{\zeta\zeta'})$ denotes  the values from a model function, computed for a given set of (complex) matrix elements $\mathbb{I}^{\zeta\zeta'}$, and $\beta^{u}_{L,M}(\epsilon,t)$ the experimentally-measured parameters, for a given configuration $u$. Implicit in the notation is that the matrix elements are independent of $u$ (or otherwise averaged over $u$). Once the matrix elements are obtained in this manner then {{ MF }} observables, for any arbitrary $u$, can be calculated. Generally fitting routines do not handle complex-valued functions, so the fitting parameter space is usually defined by parameters in magnitude-phase form (Eq. {eq}`eqn:I-zeta-mag-phase`; see also discussion in {numref}`Sect. %s <sec:channel-funcs>`)

% An example of such a protocol - specifically one based on time-domain measurements and making use of a rotational wavepacket - is shown in Fig. \ref{781808}, %, as previously discussed, 
% and the practical realisation of such a methodology is the topic of Sect. \ref{sec:bootstrapping} (see also Refs. \cite{hockett2018QMP2,marceau2017MolecularFrameReconstruction} for further discussion). As discussed in Sect. \ref{sec:MF-recon-expt}, other choices of experimental measurements may also be made, for instance direct MF measurements or frequency-domain measurements, some representative examples from the literature are given in Sect. \ref{sec:CompleteLit}. 
% [23/08/22 HERE - move to expt section? Also intro complete expts better elsewhere?]

Although in principle a very general approach, outstanding questions with such protocols remain, in particular fit uniqueness and reproducibility, the optimal measurement space $u$ - or associated information content $M_u$ - for any given case or measurement schema, and how well they will scale to larger problems (more matrix elements/partial waves). Exploration of these questions for various exemplar systems is the topic of the latter part of this book (see {numref}`Chpt. %s <sec:extracting-matrix-elements-overview>`).

% (Again, see Refs. \cite{hockett2018QMP2,marceau2017MolecularFrameReconstruction} for further discussion.)

```{code-cell} ipython3
# Numerical example here? May skip this, since it's in latter chpts.
```

## Fitting strategies

Notes on stats, repeated fitting etc. here? Now illustrated in Part 2, but no formalism given. See also QM1/2...?

Basis set choices are also introduced later.
