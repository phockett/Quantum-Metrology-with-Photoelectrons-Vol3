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

# Formatting tests

For directives and how-tos see:

- General Jupyter Book intro: https://jupyterbook.org/en/stable/content/myst.html
- https://jupyterbook.org/en/stable/content/index.html
- https://myst-parser.readthedocs.io/en/latest/faq/index.html (includes direct rst directive for native rst/Sphinx blocks).

Only outstanding point is use of raw latex? Is this possible...?

+++ {"tags": []}

## Links and refs

See https://jupyterbook.org/en/stable/content/references.html

+++

- `{numref}` for numbered ref with custom text: {numref}`Chapter %s <chpt:platformIntro>` (always works in PDF, need to [set numbered sections for HTML](https://jupyterbook.org/en/stable/content/references.html#reference-numbered-sections))
- `{ref}` for named ref: {ref}`chpt:platformIntro`
- Combined for full number and name: {numref}`Chapter %s: <chpt:platformIntro>` {ref}`chpt:platformIntro`
- Nested as a link? {numref}`Chapter %s: [](chpt:platformIntro)<chpt:platformIntro>`
- Section number: {numref}`Sect. %s <sec:dynamics-intro>`

Note style guide uses `:` separators, these are changed to `-` in HTML output links. Shouldn't generally be a problem?

+++

### Substitution tests

See https://jupyterbook.org/en/stable/content/content-blocks.html?highlight=substitutions#substitutions-and-variables-in-markdown

For global subs define in `_config.yml`. Uses Jinja on backend.

Basic: {{ test_sub }}

Sub test with URL: {{ PEMtk_repo }}

+++ {"tags": []}

## Maths

See https://jupyterbook.org/en/stable/content/math.html and https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#syntax-math

Direct case should also work with `amsmath` option on, see https://myst-parser.readthedocs.io/en/latest/syntax/optional.html#syntax-amsmath

`$$` style seems best? Otherwise doesn't render in notebook and/or labels not working (for direct latex case).

E.g.

$$
\begin{align}
  w_{t+1} = (1 + r_{t+1}) s(w_t) + y_{t+1}
\end{align}
$$ (my_other_label)

Latex labels NOT used in this case however it seems (see MyST-Parser issue https://github.com/executablebooks/MyST-Parser/issues/202)

+++

"Directive" form doesn't render in JupyterLab

```{math}
:label: my_label
w_{t+1} = (1 + r_{t+1}) s(w_t) + y_{t+1}
```

+++

Test blocks - here all render OK in HTML output, but link defined in latex only fails (but OK in PDF?).

NOTE: **defining both latex and md label seems OK in HTML output, but fails in PDF builds - JUST USE MD STYLE**

\begin{align}
\bar{I}(\epsilon,t,\theta,\phi)=\sum_{L=0}^{2n}\sum_{M=-L}^{L}\bar{\beta}_{L,M}(\epsilon,t)Y_{L,M}(\theta,\phi)
\label{eq:AF-PAD-general}
\end{align}

```{math}
:label: eq:AF-PAD-general2
\begin{align}
\bar{I}(\epsilon,t,\theta,\phi)=\sum_{L=0}^{2n}\sum_{M=-L}^{L}\bar{\beta}_{L,M}(\epsilon,t)Y_{L,M}(\theta,\phi)
\label{eq:AF-PAD-general2}
\end{align}
```

$$
\begin{align}
\bar{I}(\epsilon,t,\theta,\phi)=\sum_{L=0}^{2n}\sum_{M=-L}^{L}\bar{\beta}_{L,M}(\epsilon,t)Y_{L,M}(\theta,\phi)
\label{eq:AF-PAD-general3}
\end{align}
$$ (eq:AF-PAD-general3)


A link to no 1: {eq}`eq:AF-PAD-general`

A link to no 2: {eq}`eq:AF-PAD-general2`

A link to no 3: {eq}`eq:AF-PAD-general3`

+++

**Testing \boldsymbol** and similar

Seem to be getting inconsistent behaviour in HTML outputs, see https://github.com/phockett/Quantum-Metrology-with-Photoelectrons-Vol3/issues/4 for ongoing debugging.

- `\boldsymbol` generally not working in HTML (but OK in JupyterLab).
- `\bm` generally not working anywhere.
- Both seem OK in PDF outputs.

With single `$`

$\boldsymbol{\mathbf{E}}$

$\mathbf{E}$

$\boldsymbol{E}$ or $\mathbf{E}$ or $\bm{E}$ should be equivalent.

+++

With `$$`

$$\hat{\Gamma}(\boldsymbol{\mathbf{E}}) = \hat{\mathbf{\mu}}.\boldsymbol{\mathbf{E}}$$

+++

$$\Psi_\mathbf{k}(\bm{r})\equiv\left<\bm{r}|\mathbf{k}\right> = \sum_{lm}Y_{lm}(\mathbf{\hat{k}})\psi_{lm}(\bm{r},k)
\label{eq:elwf}$$

+++

## Figs

+++

### Fig testing (from code output)

See https://jupyterbook.org/en/stable/content/code-outputs.html#images and  https://myst-nb.readthedocs.io/en/latest/render/format_code_cells.html#images-and-figures

Easiest to add to cell metadata (?), or via in-line style in MD version.

UPDATE: for Plotly use wrapper with glue, see https://github.com/phockett/Quantum-Metrology-with-Photoelectrons-Vol3/issues/2. In `setup_notebook.py`, then use `gluePlotly(name,figObj)` in code to set.

E.g. in MD version

```{code-cell} ipython3
---
render:
  figure:
    align: center
    caption: This is a figure caption from metadata.
    name: pads-demo-test
tags: []
---
# import epsproc as ep

# Set specific LM coeffs by list with setBLMs, items are [l,m,value]
from epsproc.sphCalc import setBLMs

BLM = setBLMs([[0,0,1],[1,1,1],[2,2,1]])   # Note different index
# BLM

# Set the backend to 'pl' for an interactive surface plot with Plotly
ep.sphFromBLMPlot(BLM, facetDim='t', plotFlag = True, backend = 'pl');
```

In notebook this appears as cell metadata (NOTE, use "render", not "mystnb" as base tag!):

```
{
    "render": {
        "figure": {
            "name": "pads-demo-test",
            "align": "center",
            "caption": "This is a figure caption from metadata."
        }
    }
}

```

**NOTE this only seems to work for caption and named refs, and missed Fig. XX. (As per https://jupyterbook.org/en/stable/content/figures.html#figures)**

- Testing various options for metadata settings didn't help, although seemed easy to break parsing?
- Only seems to work for simple cases, e.g. cell outputting single Matplotlib figure?

MAY NEED TO USE glue for this, see https://jupyterbook.org/en/stable/content/executable/output-insert.html#gluing-numbers-plots-and-tables

Glue working OK for more complicated case, e.g. below with pads figure (similar method with metadata only didn't work for this case).

```{code-cell} ipython3
# Generate figure & glue
import epsproc as ep

# Set specific LM coeffs by list with setBLMs, items are [l,m,value]
from epsproc.sphCalc import setBLMs

BLM = setBLMs([[0,0,1],[1,1,1],[2,2,1]])
# BLM = setBLMs([[0,0,1,1,1],[1,1,1,0.5,0.2],[2,2,1,1,0.2]])   # Note different index
# BLM

# Set the backend to 'pl' for an interactive surface plot with Plotly
# This shows output, but fig caption not working?
# ep.sphFromBLMPlot(BLM, facetDim='t', plotFlag = True, backend = 'pl');

# Try glue...
from myst_nb import glue

# Set the backend to 'pl' for an interactive surface plot with Plotly
# NOTE PL FIG RETURN BROKEN FOR THIS CASE
dataPlot, figObj = ep.sphFromBLMPlot(BLM, facetDim='t', plotFlag = False, backend = 'pl');
# >>> NEED to use this too
figObj = ep.sphSumPlotX(dataPlot,facetDim='t', plotFlag = False, backend = 'pl')

glue("testPlot", figObj[0], display=False)
```

Glue figure with markdown:

```{glue:figure} testPlot
:figwidth: 300px
:name: "fig-boot"

This is a **caption**.
```

NOTES:

- In testing in notebook with Plotly PADs outputs this renders output directly at glue() command (although shouldn't), although OK in HTML output. (Exception was a single plot case, which did work OK.)
- Plotly outputs currently not working in PDF for Theory chpt. (15/11/22)? Although may be due to other build-chain errors in current case, TBC, since they were previously OK in test notebook output.

+++

### Fig testing (from file)

+++

As a figure, see https://jupyterbook.org/en/stable/content/figures.html


```{figure} ../images/QM_unified_schema_wrapped_280820_gv.png
---
name: qm-platform-diag-test
---
Here is my figure caption!

```




This seems to work

+++ {"tags": []}

### Fig testing (from URL)

Seemed to work OK for both HTML and PDF output, although did get some build errors in latter case. For PDF, image copied locally to hashed-named file, so probably not ideal (and seems to break build...?).

Markdown image link

![Photoelectron metrology platform diagram](https://raw.githubusercontent.com/phockett/PEMtk/4eec9217203bfd1aee13bd8b64952dc1ac5fef89/docs/doc-source/figs/QM_unified_schema_wrapped_280820.gv.png)

+++

As a figure, see https://jupyterbook.org/en/stable/content/figures.html

```{figure} https://raw.githubusercontent.com/phockett/PEMtk/4eec9217203bfd1aee13bd8b64952dc1ac5fef89/docs/doc-source/figs/QM_unified_schema_wrapped_280820.gv.png
---
height: 300px
name: directive-fig
---
Here is my figure caption!
```

+++

## Testing raw latex...

Both options fail in PDF and HTML export tests.

BETTER: JUST USE PANDOC FOR EXTENDED LATEX SECTIONS > Markdown. Will generally only need to fix minor issues (formatting and citations) in most cases anyway, if maths works.

For MyST markdown...?

- RST to MySt with Pandoc: https://github.com/executablebooks/rst2myst/issues/2 and https://github.com/executablebooks/rst-to-myst

+++

Code cell with `%%latex`

```{code-cell} ipython3
%%latex

\bf{This is a test} \\
It allows latex $\alpha=\beta$ and test:

\begin{equation}
\alpha = \beta
\end{equation}
% this is a latex comment
```

Cell below marked as raw > latex in metadata.

```{raw-cell}
:raw_mimetype: text/latex
:tags: []

\bf{This is a test} \\
It allows latex $\alpha=\beta$ and test:

\begin{equation}
\alpha = \beta
\end{equation}
% this is a latex comment
```

With `{latex}` directive

```{latex} 
\bf{This is a test}
```

+++

With MyST-rst wrapper - this appears in PDF output, but not HTML. Also bold sticks for rest of output!

```{eval-rst}
.. raw:: latex

    \bf{This is a test} \\
    It allows latex $\alpha=\beta$ and test:

    \begin{equation}
    \alpha = \beta
    \end{equation}
    % this is a latex comment

```

+++

Testing maths only - OK in notebook, and all output forms too.

\begin{equation}
\alpha = \beta
\end{equation}

+++

## Include

Working.

+++

Include with `{include}` directive:

```{include} testInclude.txt
```

```{code-cell} ipython3

```