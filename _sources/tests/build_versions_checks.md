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

% TODO: update with more info via API, e.g. https://www.baeldung.com/ops/docker-engine-api-container-info - needs some setup.

```{code-cell} ipython3
# Container name from within running container (from https://stackoverflow.com/a/64790547)
!dig -x `ifconfig eth0 | grep 'inet' | awk '{print $2}'` +short | cut -d'.' -f1
```

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

% Note - can't get versions for local pip installs from repo(?).
% May need to run git config in container first, e.g. `git config --global --add safe.directory /home/jovyan/github/ePSproc` etc.

```{code-cell} ipython3
from pathlib import Path
import epsproc as ep
ep.__file__
```

```{code-cell} ipython3
import pemtk as pm
pm.__file__
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
# Check current Git commit for local ePSproc version - NOTE THIS ONLY WORKS FOR INSTALLED FROM GIT CLONES
# from pathlib import Path
# import epsproc as ep
!git -C {Path(pm.__file__).parent} branch
!git -C {Path(pm.__file__).parent} log --format="%H" -n 1
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
+++

<!-- Manually inject MathJax to ensure side-bar formatting OK. Code copied from working pages (which include maths) -->
<script>window.MathJax = {"tex": {"macros": {"bm": ["\\boldsymbol{#1}", 1]}}, "options": {"processHtmlClass": "tex2jax_process|mathjax_process|math|output_area"}}</script>
<script defer="defer" src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
