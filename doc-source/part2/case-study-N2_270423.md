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

(chpt:n2-case-study)=
# Case study: Generalised bootstrapping for a homonuclear diatomic scattering system, $N_2~(D_{\infty h})$

+++

## General setup

In the following code cells (see source notebooks for full details) the general setup routines (as per the outline in {numref}`Chpt. %s <sect:basic-fit-setup>` are executed via a configuration script with presets for the case studies herein.

Additionally, the routines will either run fits, or load existing data if available. Since fitting can be computationally demanding, it is, in general, recommended to approach large fitting problems carefully.

```{code-cell} ipython3
# Configure settings for case study

# Set case study by name
fitSystem='N2'
fitStem=f"fit_withNoise_orb5"

# Add noise?
addNoise = True
mu, sigma = 0, 0.05  # Up to approx 10% noise (+/- 0.05)

# Batching - number of fits to run between data dumps
batchSize = 40

# Total fits to run
nMax = 1200
```

```{code-cell} ipython3
# FOCK RUNS - no web access, so skip this part.

# # Pull data files as required from Github, note the path here is required

# # from epsproc.util.io import getFilesFromGithub

# # fDict, fAll = getFilesFromGithub(subpath='data/alignment/OCS_ADMs_28K_VM_070722', ref='dev')   # OK

# # 26/05/23 - Monkeypatch version for debug
# # Above should be fine after source updates
# import requests
# from epsproc.util import io
# io.requests = requests 

# dataName = 'OCSfitting'

# fDictMatE, fAllMatE = io.getFilesFromGithub(subpath='data/photoionization/OCS_multiorb', dataName=dataName, ref='dev')  #, download=False)   # N2 matrix elements
# fDictADM, fAllADM = io.getFilesFromGithub(subpath='data/alignment/OCS_ADMs_28K_VM_070722', dataName=dataName, ref='dev')  #, download=False)   # N2 alignment data
# # Note this is missing script - should consolidate all to book repo?
# # Note ref='dev' for OCS currently (dev branch

# # Alternatively supply URLs directly for file downloader
# # Pull N2 data from ePSproc Github repo
# # URLs for test ePSproc datasets - n2
# # For more datasets use ePSdata, see https://epsproc.readthedocs.io/en/dev/demos/ePSdata_download_demo_300720.html
# # urls = {'n2PU':"https://github.com/phockett/ePSproc/blob/master/data/photoionization/n2_multiorb/n2_1pu_0.1-50.1eV_A2.inp.out",
# #         'n2SU':"https://github.com/phockett/ePSproc/blob/master/data/photoionization/n2_multiorb/n2_3sg_0.1-50.1eV_A2.inp.out",
# #         'n2ADMs':"https://github.com/phockett/ePSproc/blob/master/data/alignment/N2_ADM_VM_290816.mat",
# #         'demoScript':"https://github.com/phockett/PEMtk/blob/master/demos/fitting/setup_fit_demo.py"}

# # fList, fDict = io.getFilesFromURLs(urls, dataName=dataName)
```

```{code-cell} ipython3

```
