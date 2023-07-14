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

C2H4 fitting notes

12/07/23 setting up

- Data 
    - MatE https://phockett.github.io/ePSdata/C2H4_1.0-100.0eV/C2H4_1.0-100.0eV_orb8_B3u.html, also in ePSproc (was in `data/photoionization`, now moved to `data/photoionization/C2H4` to allow for downloader to work - otherwise pulls data AND subdirs).
    - ADMs from Varun, as per MG's C2H4 work. Now pushed to ePSproc, `data/alignment/C2H4_ADMs_8TW_120fs_VM`.
- Setup
    - QM3 container, http://jake:9966/lab/tree/QM3/doc-source/part2/case-study-C2H4_130723-setupTests.ipynb
    - Script (Fock), http://jake/jupyter/user/paul/doc/tree/fock-docker/QM3-docker/part2/C2H4fitting/setup_fit_demo_C2H4-3D-test_120723.py
- Test fits now running on Fock.

+++

(chpt:c2h4-case-study)=
# Case study: Generalised bootstrapping for a general asymmetric top scattering system, $C_2H_4~(D_{2h})$

```{code-cell} ipython3

```
