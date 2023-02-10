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

Info content theory subsection.

May ditch this unless it can be extended usefully?

- 22/11/22 Basics in place. Needs work.

+++

(sec:info-content)= 
# Information content


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
M_{u} & = & \sum_{u,k,t}\mathrm{n}\{\beta_{L,M}^{u}(\epsilon,t)\}\\
 & = & M_{u}\times M\end{aligned}$$

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
