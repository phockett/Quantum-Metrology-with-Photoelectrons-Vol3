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

24/07/23: July 2023 final revisions in progress...

- Updated intro paras, general intro but might be a bit repetitious... may be better to push into subsect on fitting, which already covers much of this? Or meld into a "general discussion" type intro subsection?
- Removed "Adaptation and fitting for different reconstruction protocols" section, and put in "Implementation in PEMtk" section instead - covers a little on fitting methods, although bit basic and similar to Sect. 2.5 notes, so may want to extend and/or consolidate.
- Added some stuff to "fitting strategies" section, mainly from QM2, could do with some more work but passable.

+++

(chpt:numerical-details)=
# Numerical methodologies for extracting matrix elements

Following the tensor notation outline in {numref}`Sect. %s <sec:tensor-formulation>`, the complete quantum metrology of a photoionization event (a.k.a. a "complete" photoionization experiment) can be characterized as recovery of the matrix elements $I^{\zeta}(\epsilon)$ (per Eqs. {eq}`eqn:channel-fns`, {eq}`eqn:I-zeta`) from the experimental measurements or, equivalently, the density matrix $\mathbf{\rho}^{\zeta\zeta'}$ (Eqs. {eq}`eqn:full-density-mat` - {eq}`eqn:beta-density-mat`). In general, such a recovery or reconstruction may be possible provided the {{ GAMMACHANNEL }} are known, and the information content of the measurements is sufficient; it is, however, also possible that restrictions in any given case may preclude reconstruction, or restrict the level of recovery possible (e.g. to a lower symmetry group, or certain subsets of {{ RADMATE }}) or fidelity of such a reconstruction. (For further discussion and background, see Refs. {cite}`Reid2003,kleinpoppen2013perfect` and {{ QM1 }}.)

Of particular import for {{ RADMATE }} retrieval is the phase-sensitive nature of the observables ({numref}`Sect. %s <sect:theory:observables>`), which is required in order to obtain phase information on the {{ PARTIALWAVES }}. In this context, {{ PADs }} can also be considered as *angular interferograms*, and reconstruction can be considered conceptually similar to other phase-retrieval problems, e.g. optical field recovery with techniques such as FROG {cite}`trebino2000FrequencyResolvedOpticalGating`, and general quantum tomography {cite}`MauroDAriano2003`.


As introduced previously ({numref}`Sect. %s <sec:main-intro:bootstrapping>`), the focus herein is the development and testing of the *generalised {{ BOOTSTRAP }}*, based on time-resolved {{ RWP }} photoionization experiments. A general outline of the simplest 2-stage version of this protocol is shown in {numref}`fig-bootstrap-fitting-diag`. In this scheme, the {{ GAMMACHANNEL }} are assumed to be known, and the {{ ADMs }} assumed to be accurately computable: these are, in general, required to determine the {{ RADMATE }} in this protocol. 

% For schemes making use of molecular alignment, or other control methods, the contribution of the control parameters to the {{ GAMMACHANNEL }} must, therefore, be accounted for. In general, these contributions may be computed and/or obtained from experiment. For the rotational wavepacket ({{ RWP }}) case, this can be considered as the requirement that the the molecular axis distributions ({{ ADMs }}) must be determined, and this is a necessary prerequisite for reconstruction of the {{ RADMATE }}. 

An extended outline comparing some similar approaches is shown in {numref}`fig-general-fitting-diag`; of particular note here is the possibility for retrieval directly from {{ MF }} measurements. Alternative, but conceptually similar, protocols involving different control parameters (as distinct from the {{ RWP }} and {{ MF }} cases), may also be also be used, see {{ QM12 }} for examples. For protocols making use of control methods, the key requirement is for the contribution of the control parameters to the observable, and associated coupling to the {{ GAMMACHANNEL }} to be accurately accounted for. In general, these contributions may be computed and/or obtained from experiment depending on the scheme used. One advantage of the {{ RWP }} case is that the {{ RWP }} can be accurately computed, and the determination of the corresponding molecular alignment ({{ ADMs }}) from an experiment can be treated as a reduced-dimensionality linear signal retrieval problem. As indicated in {numref}`fig-bootstrap-fitting-diag`, this stage is separable, and forms *level 1* of the {{ BOOTSTRAP }}. In this procedure sets of computed {{ ADMs }} form the basis set for the fitting (as a function of laser fluence and rotational temperature), allowing the accurate determination of the experimentally-achieved alignment; this is discussed further in {numref}`Sect. %s <sect:numerics:alignment-retrieval>`. *Level 2* involves non-linear data fitting, making use of the {{ ADMs }} and the {{ GAMMACHANNEL }}, in order to compute observables, and obtaining the {{ RADMATE }} as the fitted parameters; this is discussed further in {numref}`Sect. %s <sect:numerics:matE-retrieval>`. [^tDepFootnote] 


[^tDepFootnote]: As noted elsewhere: here the {{ RADMATE }} are assumed to be time-independent, although that may not be the case for the most complicated examples including vibronic dynamics, see {{ QM2 }} for further discussion on this point.

+++ {"tags": ["remove-cell"]}

{figure} flow_charts_MFrecon/bootstrap_flowchart_290822.gv.png
FAILS FOR PDF, although OK in HTML - needs to be in ../images to be copied to build dir for latex...?

+++

```{figure} ../images/bootstrap_flowchart_290822.gv.png
---
name: fig-bootstrap-fitting-diag
---
Outline of the 2-stage generalised bootstrap {{ RADMATE }} retrieval protocol ({numref}`Sect. %s <sec:main-intro:bootstrapping>`). In this case, level 1 outlines the determination of {{ ADMs }}, and level 2 "bootstaps" from this to recover {{ RADMATE }} and {{ MF }} observables. Grey inverted trapezoids indicate required inputs to the protocol, green trapezoids indicate the retrieved quantities.
```

+++

```{figure} ../images/all_protocol_flowchart_290822.gv.png
---
name: fig-general-fitting-diag
---
Comparison of similar {{ RADMATE }} retrieval protocols, illustrating (left) pure {{ MF }} case; (middle) generalised bootstrap protocol; (right) matrix inversion protocol (see Ref. {cite}`gregory2021MolecularFramePhotoelectron`).  Grey inverted trapezoids indicate required inputs to the protocol, green trapezoids indicate the retrieved quantities. For the retrieval from the {{ MF }} measurements case, no {{ RWP }} and associated {{ ADMs }} are required. For the matrix inversion protocol, {{ MF }} observables are recovered, but not {{ RADMATE }}, although the latter may be possible by subsequent analysis of the {{ MF }}-{{ PADs }}.
```

+++

(sec:numerics:fitting-methodologies)=
## Fitting methodologies

In general, the extraction of parameters from a data set can be viewed as a general minimization (fitting) problem. This type of treatment is versatile, and can be multi-stage depending on the complexity of the problem. For the generalised bootstrapping method, the treatment of photoionization data is split into two types of fit, as shown in {numref}`fig-bootstrap-fitting-diag`. Firstly, a linear fitting stage to retrieve the molecular axis distribution, characterised by a set of {{ ADMs }} (see {numref}`Sect. %s <sec:theory:AF-alignment-term>` for details); secondly, a non-linear fitting stage to retrieve the complex-valued matrix elements.

In terms of the data, the 1st stage can be written as:

$$
\bar{\beta}_{L,M}^{u}(\epsilon,t)=\sum_{K,Q,S}A_{Q,S}^{K}(t)\bar{C}_{KQS}^{LM}(\epsilon)
$$ (eqn:beta-convolution-C)

And the 2nd stage as per Eqs. {eq}`eqn:channel-fns` and {eq}`eq:BLM-tensor-AF` for the AF case:

$$
\bar{\beta}_{L,M}^{u}(\epsilon,t)=\sum_{\zeta,\zeta'}\bar{\varUpsilon_{}}_{L,M}^{u,\zeta\zeta'}(t)\mathbb{I}^{\zeta\zeta'}(\epsilon)
$$

In these forms, the terms are: 

1. $A_{Q,S}^{K}(t)$, the set of {{ ADMs }} defining the molecular alignment, and associated parameters $\bar{C}_{KQS}^{LM}(\epsilon)$.
2. $\bar{\varUpsilon_{}}_{L,M}^{u,\zeta\zeta'}(t)$, the channel functions in the {{ AF }} (Eq. {eq}`eq:BLM-tensor-AF`, and matrix elements $\mathbb{I}^{\zeta\zeta'}(\epsilon)$.

Hence stage (2) relies on the inputs of stage (1), i.e. the {{ ADMs }}; and the parameters in stage (1) can be determined via fitting the data (linear regression) making use of computed sets of $A_{Q,S}^{K}(t)$ as a function of experimental parameters (laser fluence and rotational temperature). In this case, a range of {{ ADMs }} ("basis sets") are computed, and the best match to the experimental data chosen - more details are discussed in {numref}`Sect. %s <sect:numerics:alignment-retrieval>`. In a similar manner, the 2nd stage makes use of a known basis set - the {{ GAMMACHANNEL }} - but a non-linear fit is required to determine the set of matrix elements, see {numref}`Sect. %s <sect:numerics:matE-retrieval>`.

Finally, it is also of note that, although the case herein focusses on rotational wavepackets as a control parameter, the same general approach can be applied to other cases, e.g. fitting {{ MF }}-{{ PADs }} directly (for which only the 2nd stage is required), fitting {{ PADs }} obtained via rotational state-resolved transitions, with shaped laser pulses and so on, as detailed in {{ QM12 }}. Although only rotational wavepacket cases are illustrated in this work (see {{ PARTII }}), by suitable choice of dataset and channel functions many other experimental schemes may be modelled and analysed; the {{ PEMtk_repo }} is designed with  this flexibility in mind.

+++

(sect:numerics:alignment-retrieval)=
### Computation and linear fitting for alignment characterisation

% Moderately adapted from MF recon manuscript - may want to rework further and add some numerical examples here (or elsewhere).

Efforts to align and orient molecules in recent decades have led to detailed studies of the rotational dynamics of molecules after interaction with a non-resonant femtosecond laser pulse. A significant outcome of these studies has been the development of a reliable model capable of accurate simulations of rotational wavepacket dynamics that quantitatively agree with experimental results. By measurement of a signal from a time evolving rotational wavepacket, this ability to accurately simulate the wavepacket dynamics can be used to reconstruct the measured signal in the {{ MF }}. Since in this case the time resolved measurement constitutes a set of measurements of the same quantity from a variety of molecular axes distributions (sets of {{ ADMs }}), it is reasonable to conclude that if the axes distributions are known, and provided a large enough space of orientations is explored by the molecule over the experimental time window, the {{ MF }} signal should be extractable. 

This is relatively straight forward for a signal that is a single number (scalar) in the {{ MF }} for a given polarization of the light, such as the photoionization yield. Such a signal may, in general, be expressed as an expansion,

$$
S(\theta,\chi)=\sum_{jk}C_{jk}D^{j}_{0k}(\theta,\chi),
$$ (eq:mfrealsig)

where $\theta$ and $\chi$ are the {{ MF }} spherical polar and azimuthal angles of the linearly polarized electric field vector generating the signal ({numref}`Sect. %s <sec:frame-definitions>`); $C_{jk}$ are unknown expansion coefficients; and $D^{j}_{0k}$ are the {{ WIGNERD }}, a basis on the space of orientations. A time resolved measurement of $S$ from a rotational wavepacket is the quantum expectation value of this expression,

$$
\langle S \rangle(t) = \sum_{jk}C_{jk}\langle D^{j}_{0k} \rangle (t).
$$ (eq:St-Cjk)

Since the rotational wavepacket can be accurately simulated, the $\langle D^{j}_{0k} \rangle (t)$ are considered known. From the measurement of a time resolved signal $\langle S \rangle(t)$, the unknown coefficients $C_{jk}$ can be determined by linear regression, and the molecular frame signal in Eq. {eq}`eq:mfrealsig` constructed. In this form the method was initially applied to strong field ionization and dubbed Orientation Reconstruction through Rotational Coherence Spectroscopy (ORRCS) {cite}`makhija2016ORRCS,wang2017ORRCS`.
It has since been applied to strong field ionization of various molecules {cite}`sandor2018ORRCS,sandor2019ORRCS,wangjam2021ORRCS`,
strong field dissociation {cite}`lam2020ORRCS` and few-photon ionization {cite}`lam2022ORRCS`.[^alignmentReconFootnote]

[^alignmentReconFootnote]: A large range of other experimental methods have also addressed alignment and orientation dependence and retrieval, other recent examples include Coulomb-explosion imaging {cite}`Underwood2015`, high-harmonic spectroscopy {cite}`he2018RealTimeObservationMolecular, he2020MeasuringRotationalTemperature`, optical imaging {cite}`Loriot2008` and rotational echo spectroscopy {cite}`wang2022RotationalEchoSpectroscopy`, see Refs. {cite}`Ramakrishna2013,koch2019QuantumControlMolecular` for further discussion.

The case of PADs is a more challenging one, since they are not generally described by Eq. {eq}`eq:mfrealsig`. Instead, both {{ AF }} and {{ MF }}-{{ PADs }} are determined by the {{ RADMATE }}, as discussed in {numref}`Chpt. %s <chpt:theory>`. However, the correspondence of the problem with an equation of the form of Eq. {eq}`eq:St-Cjk` - essentially a convolution - can be made. This is discussed in detail in Ref. {cite}`Underwood2000`. In the current case Eqs. {eq}`eqn:channel-fns` and {eq}`eq:BLM-tensor-AF` can be rewritten in a similar form to Eq. {eq}`eq:St-Cjk` by explicitly separating out the {{ ADMs }} $A_{Q,S}^{K}(t)$ and collapsing all other terms. The case of photoionization from a time-dependent ensemble can then be reparameterized as indicated in Eq. {eq}`eqn:beta-convolution-C`. Here the set of axis distribution moments can thus be viewed as modulating all observables $\beta_{L,M}^{u}(t)$. The unknowns, $\bar{C}_{KQS}^{LM}$ and axis distribution moments $A_{Q,S}^{K}(t)$, can be retrieved in a similar manner to that discussed for the simpler scalar observable case above (Eq. {eq}`eq:St-Cjk`), i.e. via linear regression with {{ RWP }}. 

In practice this equates to (accurately) simulating {{ RWP }}s, hence obtaining the corresponding $A_{Q,S}^{K}(t)$ parameters (expectation values), as a function of laser fluence and rotational temperature. Given experimental data, a 2D uncertainty (or error) surface in these two fundamental quantities can then be obtained from a linear regression for each set of $A_{Q,S}^{K}(t)$. The closest set of parameters to the experimental case is then determined by selection of the best results (smallest uncertainty) from such a parameter-space mapping, which constitutes determination of both the rotational wavepacket (hence $A_{Q,S}^{K}(t)$) and $\bar{C}_{KQS}^{LM}(\epsilon)$. Optimally, the corresponding physical properties can be cross-checked with other experimental estimates for additional confirmation of the fidelity of the protocol, although this may not always be possible. Note that, in this case, the photoionization dynamics are phenomenologically described by the real parameters $\bar{C}_{KQS}^{LM}$, but details of the matrix elements are not obtained directly.
% ; however, these parameters can be further used for the matrix inversion method (Sect. \ref{sec:matrix-inv-intro}), and are formally defined therein (Eqn. \ref{eq:C-AF}).

At the time of writing, computation of {{ RWP }}s and this stage of the {{ BOOTSTAP }} analysis is not implemented in the {{ PEMtk_repo }}, although is planned for the near future, and has been demonstrated in practice {cite}`marceau2017MolecularFrameReconstruction`. The examples in {{ PARTII }} instead make use of computed {{ ADMs }} directly, essentially corresponding to the assumption that level 1 of the {{ BOOTSTRAP }} was successful. Given accurate {{ RWP }}s, a successful fit to experimental data is generally assumed to be a given outcome, as this stage of the analysis requires only linear fitting in a two-parameter basis space.

% 22/08/22 - removed this for now, but could incorporated into Sect 4.1.1
% The authors of this manuscript, with a number of collaborators, demonstrated that these matrix elements can also be retrieved for one-photon ionisation of N$_2$ by time resolved measurements of LFPADs from a rotational wavepacket. This method is focus of sections X and Y (\textbf{refer to apprpriate section(s)!}) below, with additional details and results provided on the case of radial matrix element extraction for N$_2$.   In follow up work, it was shown that for molecules with $D_{nh}$ point group symmetry the retrieval of the MFPAD is possible directly, bypassing the radial matrix elements.


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

+++

(sect:numerics:matE-retrieval)=
### Non-linear fitting for matrix elements

The nature of the photoionization problem suggests that a fitting approach can work, in general, which can be expressed (for example) in the standard way as a (non-linear) least-squares minimization problem:

$$
\chi^{2}(\mathbb{I}^{\zeta\zeta'})=\sum_{u}\left[\beta^{u}_{L,M}(\epsilon,t;\mathbb{I}^{\zeta\zeta'})-\beta^{u}_{L,M}(\epsilon,t)\right]^{2}
$$ (eq:chi2-I)

where $\beta^{u}_{L,M}(\epsilon,t;\mathbb{I}^{\zeta\zeta'})$ denotes  the values from a model function, computed for a given set of (complex) matrix elements $\mathbb{I}^{\zeta\zeta'}$, and $\beta^{u}_{L,M}(\epsilon,t)$ the experimentally-measured parameters, for a given configuration $u$. Implicit in the notation is that the matrix elements are independent of $u$ (or otherwise averaged over $u$). Once the matrix elements are obtained in this manner then {{ MF }} observables, for any arbitrary $u$, can be calculated. Generally fitting routines do not handle complex-valued functions, so the fitting parameter space is usually defined by parameters in magnitude-phase form (Eq. {eq}`eqn:I-zeta-mag-phase`; see also discussion in {numref}`Sect. %s <sec:channel-funcs>`)

% An example of such a protocol - specifically one based on time-domain measurements and making use of a rotational wavepacket - is shown in Fig. \ref{781808}, %, as previously discussed, 
% and the practical realisation of such a methodology is the topic of Sect. \ref{sec:bootstrapping} (see also Refs. \cite{hockett2018QMP2,marceau2017MolecularFrameReconstruction} for further discussion). As discussed in Sect. \ref{sec:MF-recon-expt}, other choices of experimental measurements may also be made, for instance direct MF measurements or frequency-domain measurements, some representative examples from the literature are given in Sect. \ref{sec:CompleteLit}. 
% [23/08/22 HERE - move to expt section? Also intro complete expts better elsewhere?]

Although in principle a very general approach, outstanding questions with such protocols remain, in particular fit uniqueness and reproducibility, the optimal measurement space $u$ - or associated information content $M_u$ - for any given case or measurement schema, how well they will scale to larger problems (more matrix elements/partial waves), the most efficient fitting methodologies/strategies, and so forth. In general, determination of {{ RADMATE }} is *not* expected to be trivial, nor to always be successful, due to the complexity of the problem; one significant issue is the topology of the $\chi^2$ hypersurface, which is of $2N-1$ dimensions (where $N$ is the number of {{ RADMATE }}), and may contain may local minima. Exploration of these questions for various exemplar systems is the topic of the {{ PARTII }}, and further general discussion can be found in {{ QM12 }}, see in particular {{ QM2 }} Sect. 8.2.2.

% (Again, see Refs. \cite{hockett2018QMP2,marceau2017MolecularFrameReconstruction} for further discussion.)

+++

% 24/07/23 - added this for general discussion, but maybe only really repeats Sect. 2.3 stuff, so should consider more carefully.

(sect:numerics:implementation-details)=
### Implementation in PEMtk

As outlined in {numref}`Sect. %s <sect:platform:pythonEcosystem>` and {numref}`Sect. %s <sect:platform:general>`, {{ PEMtk_repo }} uses the {{ lmfit }} to implement general fitting routines, along with the {{ ePSproc_full }} for computation of the required basis sets and observables. The latter has already been illustrated in {numref}`Chpt. %s <chpt:theory>`, and the illustration of the former is the subject of {{ PARTII }}. However, in these demonstrations only the {{ RWP }} case is investigated, and analysis routines used only a standard Levenberg-Marquardt least-squares minimization method.

More generally, it is of note that the routines are written to be (somewhat) general and modular, such that other optimization methods may readily be implemented - either via [those already supported](https://lmfit.github.io/lmfit-py/fitting.html) by {{ lmfit }} (e.g. Levenberg-Marquardt, basinhopping, Nelder-Mead and so on - see the {{ lmfit }} documentation for supported methods), or by making use of other fitting libraries and methodologies. 

Similarly, modification of the routines to other retrieval schemes should be fairly easy, and usually requires only:

1. a function which computes the required basis set (e.g. {{ GAMMACHANNEL }})  
2. observables for the problem at hand. 

Examples are given in {{ PARTII }} for the *generalised {{ BOOTSTRAP }}*, and {{ MF }}-{{ PAD }} based retrieval is also implemented in the codebase. For further details see the {{ PEMtk_docs }}, particularly the [fitting model backends](https://pemtk.readthedocs.io/en/latest/fitting/PEMtk_fitting_backends_demo_010922.html) and [fitting MF and other datasets](https://pemtk.readthedocs.io/en/latest/fitting/PEMtk_fitting_demo_multi-fit_tests_130621-MFtests_120822-tidy-retest.html) pages.

+++ {"tags": ["remove-cell"]}

% 24/07/23 - removed this cell, integrated above.

(sect:numerics-other-protocols)=
### Adaptation and fitting for different reconstruction protocols

% TODO: move some text from above here, and expand a bit on methods, backends and basis sets - now have working for MF case.

% SEE SECT. 4.3 in MFRECON manuscript. May add numerical example to PART 2?

% NOW ADDED A NOTE TO sect:platform:general:
%    * Only the {{ BOOTSTRAP }} is currently implemented in {{ PEMtk_repo }}, along with associated analysis routines. However, the routines were written to be general and modular, so modification of the routines to other retrieval schemes should be fairly easy, and usually requires only (a) a function which computes the required basis set (e.g. {{ GAMMACHANNEL }})  and (b) observables for the problem at hand. Examples are given in {{ PARTII }} for the *generalised {{ BOOTSTRAP }}*, and {{ MF }}-{{ PAD }} based retrieval is also implemented in the codebase. For further details see the {{ PEMtk_docs }}, particularly the [fitting model backends](https://pemtk.readthedocs.io/en/latest/fitting/PEMtk_fitting_backends_demo_010922.html) and [fitting MF and other datasets](https://pemtk.readthedocs.io/en/latest/fitting/PEMtk_fitting_demo_multi-fit_tests_130621-MFtests_120822-tidy-retest.html) pages.

% MAY WANT TO MOVE/ADD this to PARTII somewhere, maybe include some of the numerics directly

As already noted in {numref}`Sect. %s <sect:platform:general>`, only the {{ BOOTSTRAP }} is currently implemented in {{ PEMtk_repo }}, along with associated analysis routines. However, the routines were written to be general and modular, so modification of the routines to other retrieval schemes should be fairly easy, and usually requires only (a) a function which computes the required basis set (e.g. {{ GAMMACHANNEL }})  and (b) observables for the problem at hand. Examples are given in {{ PARTII }} for the *generalised {{ BOOTSTRAP }}*, and {{ MF }}-{{ PAD }} based retrieval is also implemented in the codebase. For further details see the {{ PEMtk_docs }}, particularly the [fitting model backends](https://pemtk.readthedocs.io/en/latest/fitting/PEMtk_fitting_backends_demo_010922.html) and [fitting MF and other datasets](https://pemtk.readthedocs.io/en/latest/fitting/PEMtk_fitting_demo_multi-fit_tests_130621-MFtests_120822-tidy-retest.html) pages.

+++

(sect:numerics:fitting-strategies)=
## Fitting strategies

% Notes on stats, repeated fitting etc. here? Now illustrated in Part 2, but no formalism given. See also QM1/2...?

% Basis set choices are also introduced later.

% 24/07/23 - added some basic notes, may be easier to discuss with examples in PART II?

The overall approach to complex non-linear fitting incorporates a number of aspects, broadly "fitting strategies", which may influence the likelyhood of a successful {{ RADMATE }} retrieval, and/or the time required to achieve this result:

1. The choice of numerical fitting method ({numref}`Sect. %s <sect:numerics:implementation-details>`).
2. The choice of dataset to analyse (and/or the choice of experimental measurement).
3. Additional statistical and/or other meta-analysis.

At the time of writing, work is ongoing in all these areas, and the illustrations in {{ PARTII }} herein include further notes regarding limitations or expectations for specific cases. Clearly, there are many choices numerically, and detailed investigation is required to determine the optimal strategy in any given case (this is examined partially in {{ PARTII }} in terms of limiting cases by symmetry). Emerging data analysis methods may also be useful here, in particular GPU-based routines and specialist high-dimensional space fitting methods.

One aspect that is intrinsic to these examples, but has not been discussed elsewhere, is the meta-analysis of the retrieved {{ RADMATE }}. This is discussed generally in {{ QM2 }} Sect. 8.2.2, and implemented numerically in the examples in {{ PARTII}} herein. The general aim in this type of analysis is to ascertain whether a given set of retrieved parameters is accurate and unique in a given case. Naturally, for test cases with synthetic data (as in {{ PARTII }}), testing against the known input {{ RADMATE }} is the best solution and provides the most stringent test for the applicability of the retrieval method - but this is, of course, not generally useful for experimental datasets. Instead, as per previous analysis cases (see {{ QM2 }}), a statistical (or "numerical experiment") approach can be used. In this type of approach, a number of fits $n$ (typically on the order of $10^2$-$10^4$) are run independently, with different seed parameters and/or different input data (cf. Monte Carlo methods, and statistical bootstrap methods), and the set of results analysed for consistency and uniqueness over the retrieved parameter sets. As outined in {{ QM2 }} (updated to match the notation herein), "Each fit yields a solution set $\mathbb{I}^{\zeta\zeta'}(n)$, with a final value of $\chi^{2}(\mathbb{I}^{\zeta\zeta'}(n))$. Analysis of the fitted parameters $\chi^{2}(\mathbb{I}^{\zeta\zeta'})$ can be employed to probe the behaviour of the fitting algorithm, and also to gain information on how well the experimental data defines each fitted parameter. Although it is non-trivial to visualize the full $\chi^{2}$ hypersurface, aspects can be probed by plotting histograms and correlation plots of the fitted parameters. A large scatter in the value of a given fit parameter over a range of fits to the same data suggests a poorly defined parameter; a consistent result meanwhile shows that a particular parameter is well defined by the dataset. The experimental data can show different sensitivities to different parameters depending on the type of ionizing transitions present, because different transitions will (according to the magnitude of the geometrical parameters and symmetry constraints [i.e. {{ GAMMACHANNEL }} herein]) be more sensitive to certain partial-waves. Additionally, the presence of multiple minima in the fit may be revealed by the presence of more than one feature in the histogram, reflecting more than one "best" fit result, while correlations appearing between supposedly uncorrelated parameters can indicate emergent behaviours in the high-dimensional space or - more prosaically - issues with the fitting methodology or coding."

The same approach is taken in the case-studies of {{ PARTII }}, which include statistical analysis to determine the "correct" {{ RADMATE }} from a set of non-linear fits, and associated uncertainties, again with the hope of illustrating general methods.



```{code-cell} ipython3

```
