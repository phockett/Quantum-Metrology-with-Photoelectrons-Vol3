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

(chpt:platformIntro)=
# Quantum metrology software platform/ecosystem overview

STUB

+++

% Adapted from MFrecon article, Numerical implementation sect.

In recent years, a unified Python codebase/ecosystem/platform has been in development to tackle various aspects of photoionization problems, including *ab initio* computations and experimental data handling, and (generalised) matrix element retrieval methods. The eponymous _Quantum Metrology with Photoelectrons_ platform is introduced here, and is used for the analysis herein. The main aim of the platform is to provide a unifying data platform, and analysis routines, for photoelectron metrology, including new methods and tools, as well as a unifying bridge between these and existing tools. {numref}`qm-platform-diag` provides a general overview of some of the main tools and tasks/layers.

As of late 2022, the new parts of the platform - primarily the {{ PEMtk_repo }} library - implement general data handling (although not a full experimental analysis toolchain), matrix element handling and retrieval, which will be the main topic of this volume.
In the future, it is hoped that the platform will be extended to other theoretical and experimental methods, including full experimental data handling.

(sect:platform:analysis)=
## Analysis components

The two main components of the platform for analysis tasks, as used herein, are:

-   The {{ PEMtk_repo }} (PEMtk) codebase aims to provide various general data handling routines for photoionization problems. At the time of writing, simulation of observables and fitting routines are implemented, along with some basic utility functions.
    Much of this is detailed herein, and more technical details and ongoing documentation case be found in the {{ PEMtk_docs }}.

-   The {{ ePSproc_full }} aims to provide methods for post-processing with *ab initio* radial dipole matrix
    elements from {{ ePS_full }}, or equivalent matrix elements from other sources (dedicated support for R-matrix results from [the RMT suite](https://gitlab.com/Uk-amor/RMT/rmt) {cite}`brown2020RMTRmatrixTimedependence,RmatrixRepo` is in development). 
    The core functionality includes the computation of AF and MF observables. Manual computation without known matrix elements is also possible, e.g. for investigating
    limiting cases, or data analysis and fitting - hence these routines also provide the backend functionality for PEMtk fitting routines. Again more technical details can be found in the {{ ePSproc_docs }}.

+++

```{figure} ../images/QM_unified_schema_wrapped_280820_gv.png
---
name: qm-platform-diag
---
Quantum metrology with photoelectrons ecosystem overview.
```

+++

Other tools listed in {numref}`qm-platform-diag` include:

* Quantum chemistry layer. The starting point for *ab initio* computations. For the examples herein, all computations made use of [Gamess ("The General Atomic and Molecular Electronic Structure System")](http://www.msg.ameslab.gov/gamess/) {cite}`gamess, Gordon` for electronic structure computations, and inputs to ePolyScat.
* {{ ePS_full }} is an open-source tool for numerical computation of electron-molecule scattering & photoionization by Lucchese & coworkers. All matrix elements used herein were obtained via ePS calculations. For more details see {{ ePS_manual }} and Refs. {cite}`Lucchese1986,Gianturco1994,Natalense1999,luccheseEPolyScatUserManual`.
    
* [ePSdata](https://phockett.github.io/ePSdata/about.html) is an open-data/open-science collection of ePS + ePSproc results {cite}`hockett2019EPSDataPhotoionization`.
    * ePSdata collects ePS datasets, post-processed via ePSproc (Python) in [Jupyter notebooks](https://jupyter.org), for a full open-data/open-science transparent pipeline.
    % * ePSdata is currently (Jan 2020) collecting existing calculations from 2010 - 2019, from the [femtolabs at NRC](http://femtolab.ca), with one notebook per ePS job.
    % * In future, ePSdata pages will be automatically generated from ePS jobs (via the ePSman toolset, currently in development), for immediate dissemination to the research community.
    * Source notebooks are available on the [Github project pages](https://github.com/phockett/ePSdata/), and notebooks + datasets via [Zenodo repositories](https://about.zenodo.org) (one per dataset). Each notebook + dataset is given a Zenodo DOI for full traceability, and notebooks are versioned on Github.
    * Note: ePSdata may also be linked or mirrored on the existing [ePolyScat Collected Results OSF project](https://osf.io/psjxt/), but will effectively supercede those pages.
    * All results are released under <a href=\"https://creativecommons.org/licenses/by-nc-sa/4.0/\">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 (CC BY-NC-SA 4.0)</a> license, and are part of our ongoing [Open Science initiative](http://femtolab.ca/?p=877).


A Docker-based distribution of various codes for tackling
photoionization problems is also available from the {{ open_photo_stacks_repo }}
project, which aims to make a range of these tools more accessible to
interested researchers, and currently includes Docker builds for `ePS`, `ePSproc` and `PEMtk`.

Note that, at the time of writing, rotational wavepacket simulation is
not yet implemented in the PEMtk suite, and these must be obtained via
other codes. An intial build of the `limapack` suite for rotational wavepacket simulations is currently part of the {{ open_photo_stacks_repo }}, but has yet to be tested.

```{code-cell} ipython3
For related tools and more Docker builds, see also the [Open Photoionization Docker Stacks repo](https://github.com/phockett/open-photoionization-docker-stacks)
```

```{code-cell} ipython3

```