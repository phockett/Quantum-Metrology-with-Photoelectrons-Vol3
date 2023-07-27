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

(chpt:extracting-matrix-elements-overview)=
# Extracting matrix elements overview

In this part, various case studies are presented. To provide context, and ensure that the examples are transparent and can be run directly from the source notebooks, there are also chapters covering the general setup and configuration for the fitting routines. These are, unavoidably, rather technical and code-heavy, so readers only interested in the results should skip these sections. Additionally, these sections may be rather truncated in hard-copy (or PDF) versions of the text, but are available in full in the {{ book_HTML }} and source notebooks for readers that wish to perform their own calculations.

+++

````{margin}
```{warning}
As {ref}`noted elsewhere <sec:numerics:disclaimer>`, many components of the toolkit are still in active development, and some numerical details may change. This is particularly true for 3D alignment examples, which are here presented as new, and provisional, results.
```
````

+++

The layout for this part is as follows:

- Technical introductions
   - {numref}`Chapter %s: <sect:basis-sets:fitting-intro>` {ref}`sect:basis-sets:fitting-intro`: introduces methods for setting the basis set used for fitting, defined in terms of symmetrized harmonics.
   - {numref}`Chapter %s: <sect:basic-fit-setup>` {ref}`sect:basic-fit-setup`: introduces methods for setting up the data to fit, and running fits in various ways.
   
- Case studies
   - {numref}`Chapter %s: <chpt:n2-case-study>` {ref}`chpt:n2-case-study`: A "simple" 1D case, here the $D_{\infty h}$ molecular symmetry matches the rotational wavepacket and detection symmetry.
   - {numref}`Chapter %s: <chpt:ocs-case-study>` {ref}`chpt:ocs-case-study`: A more complicated example. In this case, $C_{\infty v}$, up-down symmetry is broken in the molecular frame. Fitting for various cases is explored, looking at 1D and 3D alignment.
   - {numref}`Chapter %s: <chpt:c2h4-case-study>` {ref}`chpt:c2h4-case-study`: The most general example of an asymmetric top system, in this case $C_2H_4$ (ethylene), $C_{2h}$. Again various cases and limitations are examined, for 1D and 3D alignment.
   
- Summary, conclusions and outlook
   - {numref}`Chapter %s: <chpt:case-study-summaries>` {ref}`chpt:case-study-summaries`: general overview of the case study results and conclusions.
   - {numref}`Chapter %s: <chpt:conclusions>` {ref}`chpt:conclusions`: General conclusions and outlook.

+++

## General notes on the case studies

The case studies presented herein represent various different types (classes or degrees-of-difficulty) of fitting problem. They are intended both to indicate ways to proceed in general, and also aim to address what is, and isn't, possible in these given cases. The simplest case, $N_2$, has been well-studied, and reconstruction of {{ RADMATE }} via the {{ BOOTSTRAP }} has proved successful in a range of valence ionization cases - see Ref. {cite}`marceau2017MolecularFrameReconstruction` for the initial experimental demonstration, and updated analysis using the {{ PEMtk_repo }} in Ref. {cite}`hockett2023TopicalReviewExtracting`, as well as {numref}`Chapter %s: <chpt:n2-case-study>` herein.

The more complex cases, involving 3D alignment, are new, and very much work-in-progress. The current state-of-the-art is presented herein, but it is of note that these results are provisional, and work is ongoing. In particular, there are a large range of fitting configuration options and parameters which have yet to be explored in these cases, which may significantly improve on the current results in terms of computational effort required, reliability of the fitting protocol, and size of the required dataset. Nonetheless, these new results are interesting and present a stepping-stone for studies on {{ RADMATE }} retrieval in complex systems, and a launching point for similar studies.

*Each case study has a setup script and associated data, which was used to create sample data and configure the {{ BOOTSTRAP }} in each case (the general procedure is outlined in {numref}`Chapter %s <sect:basic-fit-setup>`). However, since the fitting is computationally demanding, code execution for this is not run upon building the book - rather data files are used. Each case study therefore contains an initial setup stage which can be used to run fits, or load existing data, prior to analysis.*

Finally, it is of note that - as discussed in the {ref}`preamble on book versions <chpt:book-versions>` - output may be significantly truncated in some cases. Readers wishing to obtain all computational details should pull the source notebooks from {{ book_repo }}, or consult the online HTML version at {{ book_HTML }}.
