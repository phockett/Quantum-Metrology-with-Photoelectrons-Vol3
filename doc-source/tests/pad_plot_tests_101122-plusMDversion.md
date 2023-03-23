---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.4
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# PAD plotting tests from MD

With MD sidecar to test.

Note output NOT rendered unless `execute_notebooks` set.

OR use `build-ipynb.sh` script, which copies doc-source then strips .md files prior to build. (Crude, but basically working.)

```{code-cell} ipython3

```

```{code-cell} ipython3
import epsproc as ep

# Set specific LM coeffs by list with setBLMs, items are [l,m,value]
from epsproc.sphCalc import setBLMs

BLM = setBLMs([[0,0,1],[1,1,1],[2,2,1]])   # Note different index
# BLM

# Set the backend to 'pl' for an interactive surface plot with Plotly
ep.sphFromBLMPlot(BLM, facetDim='t', plotFlag = True, backend = 'pl', camR=0.8);
```

```{code-cell} ipython3
# Check current Git commit for local ePSproc version
# NOTE this only works for local repo copies, not if git installed via Pip
from pathlib import Path
!git -C {Path(ep.__file__).parent} branch
!git -C {Path(ep.__file__).parent} log --format="%H" -n 1
```

```{code-cell} ipython3
Path(ep.__file__)
```

```{code-cell} ipython3
# Check current remote commits
!git ls-remote --heads https://github.com/phockett/ePSproc
```

```{code-cell} ipython3

```
