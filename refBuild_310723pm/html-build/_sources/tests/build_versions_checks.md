---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.7
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Build versions and config tests

+++

## Versions

```{code-cell} ipython3
import scooby
scooby.Report(additional=['pemtk','epsproc','xarray', 'pandas', 'scipy', 'matplotlib','jupyterlab','plotly','holoviews'])
```

```{code-cell} ipython3
!jupyter-book --version
```

```{code-cell} ipython3
!jupyter --version
```

## Docker build env

To do

+++

## Book versions

```{code-cell} ipython3
QMpath = '/home/jovyan/QM3'
!git -C {QMpath} branch
!git -C {QMpath} log --format="%H" -n 1
```

```{code-cell} ipython3
# Check current remote commits
!git ls-remote --heads https://github.com/phockett/Quantum-Metrology-with-Photoelectrons-Vol3
```

## Github pkg versions

Note - can't get versions for local pip installs from repo(?).

```{code-cell} ipython3
from pathlib import Path
import epsproc as ep
ep.__file__
```

```{code-cell} ipython3
# Check current Git commit for local ePSproc version - NOTE THIS ONLY WORKS FOR INSTALLED FROM GIT CLONES
# from pathlib import Path
# import epsproc as ep
!git -C {Path(ep.__file__).parent} branch
!git -C {Path(ep.__file__).parent} log --format="%H" -n 1
```

```{code-cell} ipython3
# Check current remote commits
!git ls-remote --heads https://github.com/phockett/ePSproc
```

```{code-cell} ipython3
# Check current remote commits
!git ls-remote --heads https://github.com/phockett/PEMtk
```

## Full conda env

```{code-cell} ipython3
!conda list
```

```{code-cell} ipython3

```
