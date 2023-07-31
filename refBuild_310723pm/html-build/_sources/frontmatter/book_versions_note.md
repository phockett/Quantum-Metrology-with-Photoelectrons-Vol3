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

(chpt:book-versions)=
# A note on book versions, formats and conventions

## Versions

This book exists in multiple formats, which are not all equal:

1. Jupyter notebooks. The original form, interactive computational notebooks includes text, executable code and full outputs. Source notebooks are available via {{ book_repo }}.

2. HTML pages. Compiled from the notebooks, include interactive figures and most computational outputs. The HTML version is available at {{ book_HTML }}.

3. PDF and hard-copy. Standard static outputs, compiled from the notebooks. In this form some computational outputs are truncated or omitted for brevity and readability. Since some formats may not support hyperlinks, URLs to external references are also usually included in the bibliography - note that these may not always be the *full* URLs linked in the main text, and may only list the main index page of a given site in some cases. Some figures may also be omitted.

## Conventions

````{margin}
```{note}
In many cases where there is significant truncation of the presentation in the PDF, a note like this may be included.

E.g. *Full tabulations of the parameters available in HTML or notebook formats only.*
```
````

+++

Code (Python) appears in formatted cells, with comments, and outputs below the cell:

```{code-cell} ipython3
# Example comment in code
value = 3*3
print(f'This is a code cell, value={value}')
```

In HTML and PDF formats some code cells that appear in the source notebooks may be hidden or removed, or have outputs hidden or removed. This is usually for brevity - e.g. to remove additional code-only examples that are only useful when working directly on the code, or repeated code - or to hide additional formatting commands required only for Jupyter Book builds. All code cells are annotated to indicate their contents.

```{code-cell} ipython3
:tags: [hide-cell, hide-output]

# This is a hidden code cell (will not appear in PDF versions)
import numpy as np

value = 2+np.pi
print(f'This is a hidden code cell, with hidden output, value={value}')
```

Code-related terms in the text, e.g. the names of functions, packages etc., usually appear as in-line blocks, e.g. `Numpy`, and may additionally be linked to relevant web resources, e.g. [`Numpy`](https://numpy.org/).

For more details on the aims, tools and build-chain, see {numref}`Sect. %s <sec:intro-technical-notes>`.

## Formatting

In some cases additional formatting is required for defining Jupter Notebook to HTML and PDF outputs (via the Jupyter Book build-chain, see {numref}`Sect. %s <sec:intro-technical-notes>`), in particular [the `glue` command](https://jupyterbook.org/en/stable/content/executable/output-insert.html) is used for formatting figure outputs with captions. In general use these are not required, but will transparently display figures when executed in the Jupyter Lab environment. Note that glued tables from `Pandas` DataFrames are not nicely rendered in the HTML format, but interactive HTML output is usually include too, although this may be hidden in the cell above the glued table.

(sec:numerics:disclaimer)=
## Numerics

At the time of writing the main code-bases used in this work (see {numref}`Sect. %s <chpt:platformIntro>` are still in active development, bugs, inconsistencies and errors cannot, therefore, be ruled out in the numerical examples. However, the case for 1D alignment and reconstruction has been well-tested in the past (e.g. Refs. {cite}`marceau2017MolecularFrameReconstruction,hockett2022TopicalReviewMFpreprint,hockett2023TopicalReviewExtracting`), so is expected to be accurate; cases with 3D alignment are presented in a provisional context, with caveats as above, although the general methodology as demonstrated is robust.

```{code-cell} ipython3

```
