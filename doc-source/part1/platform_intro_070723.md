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

v 07/11/22

- STUB
- Adapted from MFrecon article, Numerical implementation sect.

v 07/07/23

- Reviewing and expanding.

+++

(chpt:platformIntro)=
# Quantum metrology software platform/ecosystem overview

+++

In recent years, a unified Python codebase/ecosystem/platform has been in development to tackle various aspects of photoionization problems, including *ab initio* computations and experimental data handling, and (generalised) matrix element retrieval methods. The eponymous _Quantum Metrology with Photoelectrons_ platform is introduced here, and is used for the analysis herein. The main aim of the platform is to provide a unifying data platform, and analysis routines, for photoelectron metrology, including new methods and tools, as well as a unifying bridge between these and existing tools. {numref}`qm-platform-diag` provides a general overview of some of the main tools and tasks/layers.

As of late 2022, the new parts of the platform - primarily the {{ PEMtk_repo }} library - implement general data handling (although not a full experimental analysis toolchain), matrix element handling and retrieval, which will be the main topic of this volume.
In the future, it is hoped that the platform will be extended to other theoretical and experimental methods, including full experimental data handling.

(sect:platform:analysis)=
## Analysis components

The two main components of the platform for analysis tasks, as used herein, are:

-   The {{ PEMtk_repo }} (PEMtk) codebase aims to provide various general data handling routines for photoionization problems. At the time of writing, simulation of observables and fitting routines are implemented, along with some basic utility functions.
    Much of this is detailed herein, and more technical details and ongoing documentation case be found in the {{ PEMtk_docs }}.

-   The {{ ePSproc_full }} aims to provide methods for post-processing with *ab initio* radial dipole matrix
    elements from {{ ePS_full }}, or equivalent matrix elements from other sources (dedicated support for R-matrix results from [the RMT suite](https://gitlab.com/Uk-amor/RMT/rmt) {cite}`brown2020RMTRmatrixTimedependence,RmatrixRepo` is in development, for an overview of *ab initio* methods/packages see Ref. {cite}`dowek2022TrendsAngleresolvedMolecular`). 
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

(sect:platform:otherTools)=
## Additional tools

Other tools listed in {numref}`qm-platform-diag` include:

* Quantum chemistry layer. The starting point for *ab initio* computations. Many tools are available, but for the examples herein, all computations made use of [Gamess ("The General Atomic and Molecular Electronic Structure System")](http://www.msg.ameslab.gov/gamess/) {cite}`gamess, Gordon` for electronic structure computations, and inputs to ePolyScat.
   * For a python-based approach, various packages are available, e.g. [PySCF](https://pyscf.org), [PyQuante](https://pyquante.sourceforge.net/), [Psi](https://psicode.org) can be used for electronic structure calculation, although note that some {{ ePSproc_repo }} routines currently require Gamess files (specifically for visualisation of orbitals).
   * A range of other python tools are available, including [cclib](https://cclib.github.io/) for file handling and conversion, [Chemlab](https://chemlab.readthedocs.io) for molecule wavefunction visualisations, see further notes below.
* {{ ePS_full }} is an open-source tool for numerical computation of electron-molecule scattering & photoionization by Lucchese & coworkers. All matrix elements used herein were obtained via ePS calculations. For more details see {{ ePS_manual }} and Refs. {cite}`Lucchese1986,Gianturco1994,Natalense1999`.
    
* {{ ePSdata_docs }} is an open-data/open-science collection of ePS + ePSproc results.
    * ePSdata collects ePS datasets, post-processed via ePSproc (Python) in [Jupyter notebooks](https://jupyter.org), for a full open-data/open-science transparent pipeline.
    % * ePSdata is currently (Jan 2020) collecting existing calculations from 2010 - 2019, from the [femtolabs at NRC](http://femtolab.ca), with one notebook per ePS job.
    % * In future, ePSdata pages will be automatically generated from ePS jobs (via the ePSman toolset, currently in development), for immediate dissemination to the research community.
    * Source notebooks are available on the {{ ePSdata_repo }} [Github project repository](https://github.com/phockett/ePSdata/), and notebooks + datasets via {{ ePSdata_zenodo }}. Each notebook + dataset is given a Zenodo DOI for full traceability, and notebooks are versioned on Github.
    * Note: ePSdata may also be linked or mirrored on the existing [ePolyScat Collected Results OSF project](https://osf.io/psjxt/), but will effectively supercede those pages.
    * All results are released under [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 (CC BY-NC-SA 4.0) license](https://creativecommons.org/licenses/by-nc-sa/4.0/), and are part of an ongoing [Open Science initiative](http://femtolab.ca/?p=877).

+++

(sect:platform:pythonEcosystem)=
## Python ecosystem (backends, libraries and packages)

The core analysis tools, which constitute the {{ PEMtk_repo }} platform, are themselves built with the aid of a range of open-source python packages/libraries which handle various backend functionality. Notably, they make use of the following key packages:

* General functionality makes use of the usual `Scientific Python` stack, in particular: 
   * `Numpy` for general numerical methods and data types.
   * `pandas` for statistical methods, and various tabulation and sorting tasks.
   * `Scipy` for some special functions and computational routines, particularly spherical harmonics and fitting routines (see below).
* General tensor handling and manipulation makes use of the Xarray library {cite}`hoyer2017XarrayNDLabeled,XarrayDocumentation`.
* Angular momentum functions (Wigner D and 3js) are currently implemented directly, or via the Spherical Functions library {cite}`boyle2022SphericalFunctions`, and have been tested for consistency with the definitions in Zare (for details see [the ePSproc docs](https://epsproc.readthedocs.io/en/latest/tests/Spherical_function_testing_Aug_2019.html) {cite}`ePSprocDocs`). The Spherical Functions library also uses `numpy_quaternion` which implements a quaternion datatype in Numpy.
* Spherical harmonics are defined with the usual physics conventions: orthonormalised, and including the Condon-Shortley phase. Numerically they are implemented directly or via SciPy's `sph_harm` function (see [the SciPy docs for details](https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.sph_harm.html) {cite}`SciPyDocumentation`. Further manipulation and conversion between different normalisations can be readily implemented with the SHtools library {cite}`wieczorek2018SHToolsToolsWorking,SHtoolsGithub`.
* Non-linear optimization (fitting) is handled via the [lmfit library](https://lmfit.github.io/lmfit-py/index.html), which implements and/or wraps a range of non-linear fitting routines in Python {cite}`LMFITDocumentation, newville2014LMFITNonLinearLeastSquare`; for the Levenberg-Marquardt least-squares minimization method used herein this wraps [Scipy's `least_squares` functionality](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.least_squares.html), which therefore constituted the core minimization routine {cite}`SciPyDocumentation` for the demonstration cases.
* Symmetry functionality, specifically computing symmetrized harmonics $X_{hl}^{\Gamma\mu*}(\theta,\phi)$ (see {eq}`eq:AF-PAD-general`), makes use of `libmsym` {cite}`johansson2017AutomaticProcedureGeneratinga, johansson2022LibmsymGithub` (symmetry coefficients) and `SHtools` {cite}`wieczorek2018SHToolsToolsWorking,SHtoolsGithub` (general spherical harmonic handling and conversion). 
% For worked examples, see \href{https://pemtk.readthedocs.io/en/latest/sym/pemtk_symHarm_demo_160322_tidy.html}{the PEMtk docs} \cite{hockett2021PEMtkDocs}. It is hoped that this will be a useful tool for tackling photoionization problems more generally, without \textit{a priori} knowledge of the matrix elements for a given system.
* Some specialist (optional) tools also make use of additional libraries, although these are not required for basic use; in particular:
   * For 3D orbital visualizations with {{ ePSproc_repo }}: [pyvista](https://docs.pyvista.org/) for 3D plotting (which itself is built on VTK), [cclib](https://cclib.github.io/) for electronic structure file handling and conversion, and methods based on [Chemlab](https://chemlab.readthedocs.io) for molecule wavefunction (orbital) computation from electronic structure files are all used on the backend.
   * For general plotting a range of tools are used, or can be used, including [`Matplotlib`](https://matplotlib.org/) (basic plotting, including `Xarray` plotters), [`Holoviews`](https://holoviews.org/) (data handling and interactive plotting, wraps various backends), [`Bokeh`](https://bokeh.org/) (implemented via Holoviews), [`Plotly`](https://plotly.com/) (mainly used for spherical polar plotting), and [`Seaborn`](https://seaborn.pydata.org/) (for statistical and some specialist plots).
   * [`Numba`](https://numba.pydata.org/) is used for numerical acceleration in some routines, although remains mainly experimental in `ePSproc` at the time of writing (an exception to this is the Spherical Functions library, which does make full use of Numba acceleration).


% See MFrecon Sect. 9.5. Some of this may also go in Chpt. 4, but more likely computational examples in there?

Further comments, including conventions and numerical examples, can be found in Chpt. XX.

+++

(sect:platform:docker)=
## Docker deployments

A Docker-based distribution of various codes for tackling
photoionization problems is also available from the {{ open_photo_stacks_repo }}
project, which aims to make a range of these tools more accessible to
interested researchers, and fully cross-platform/portable. The project currently includes Docker builds for `ePS`, `ePSproc` and `PEMtk`.


(sect:platform:general)=
## General discussion

Note that, at the time of writing, rotational wavepacket simulation is
not yet implemented in the PEMtk suite, and these must be obtained via
other codes. An intial build of the `limapack` suite for rotational wavepacket simulations is currently part of the {{ open_photo_stacks_repo }}, but has yet to be tested.

```{code-cell} ipython3

```
