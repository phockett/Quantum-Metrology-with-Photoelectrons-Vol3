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

```{code-cell} ipython3
!date
```

+++ {"tags": []}

## Links and refs

See https://jupyterbook.org/en/stable/content/references.html

+++

- Label sections with `(some-label)=`, no spaces!
- `{numref}` for numbered ref with custom text: {numref}`Chapter %s <chpt:platformIntro>` (always works in PDF, need to [set numbered sections for HTML](https://jupyterbook.org/en/stable/content/references.html#reference-numbered-sections))
- `{ref}` for named ref: {ref}`chpt:platformIntro`
- Combined for full number and name: {numref}`Chapter %s: <chpt:platformIntro>` {ref}`chpt:platformIntro`
- Nested as a link? {numref}`Chapter %s: [](chpt:platformIntro)<chpt:platformIntro>`
- Section number: {numref}`Sect. %s <sec:dynamics-intro>`
   - This is failing...?  Test {ref}`sect:theory:observables` and {numref}`Sect. %s <sect:theory:observables>`
   - Issue with nested docs, or just numbering? 
   - Unnested case test: {ref}`sec:intro-context` and {numref}`Sect. %s <sec:intro-context>`
   - Ah, OK - fails if nesting skips levels (although HTML render is OK). See https://jupyterbook.org/en/stable/structure/sections-headers.html#how-headers-and-sections-map-onto-to-book-structure
- Figs, only need numref for Fig. XX style, e.g. {numref}`fig-pads-example`

Note style guide uses `:` separators, these are changed to `-` in HTML output links. Shouldn't generally be a problem?

Note: sometimes cross-refs fail, usually seem OK after a clean build. Might be bug with nested file case?
Note PDF: may also need to run **multiple** times (as per usual) to fix missing cross-refs.

+++

### Substitution tests

See https://jupyterbook.org/en/stable/content/content-blocks.html?highlight=substitutions#substitutions-and-variables-in-markdown

For global subs define in `_config.yml`. Uses Jinja on backend.

Basic: {{ test_sub }}

Sub test with URL: {{ PEMtk_repo }}

Sub test with maths: {{ BLM }} (working if esc \ in maths defn).

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

NOTE: ACCIDENTALLY defining nested maths, e.g. `$$\begin{equation}...` is OK in notebook, but produces lots of build errors, look out for  `! You can't use `\eqno' in math mode.` SHOULD ADD pre-commit Latex checks?

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

**Issues with mathbf and hats (PDF output only)**

$$1: \hat{\Gamma}(\boldsymbol{\mathbf{E}}) = \hat{\mathbf{\mu}}.\boldsymbol{\mathbf{E}}$$

$$2: \hat{\Gamma}(\boldsymbol{\mathbf{E}}) = \mathbf{\mu}.\boldsymbol{\mathbf{E}}$$

$$3: \hat{\Gamma}(\boldsymbol{\mathbf{E}}) = \mu.\boldsymbol{\mathbf{E}}$$

$$4: \hat{\Gamma}(\boldsymbol{\mathbf{E}}) = \bm{\mu}.\boldsymbol{\mathbf{E}}$$

$$5: \hat{\Gamma}(\boldsymbol{\mathbf{E}}) = \boldsymbol{\mu}.\boldsymbol{\mathbf{E}}$$

$$6: \hat{\Gamma}(\boldsymbol{\mathbf{E}}) = \hat{\boldsymbol{\mu}}.\boldsymbol{\mathbf{E}}$$

Without bm package, 3 - 6 are all OK. 'mathbf' seems to be an issue? Missing fonts - renders as a '?' in a square and gives error like `! Extended mathchar used as mathchar (14799967).`?

With bm package, only 3 works (and 4 renders as $\mu0$)

LOOKS LIKE using \boldsymbol and avoiding \mathbf and \bm seems best? Can't see any other obviously missing pkgs in latex build (cf. MF recon .tex), although clearly this is not usually a problem.

See https://tex.stackexchange.com/questions/381604/bold-math-with-hat and https://tex.stackexchange.com/questions/3238/bm-package-versus-boldsymbol

Probably just reformat in this case? Some of this might be Lyx, or other original source formatting? (Or VM?)

Note unicode-math (per solution https://tex.stackexchange.com/questions/431013/error-extended-mathchar-used-as-mathchar-when-using-bm) is set by Jupyter book already.


In HTML build, with macro fix for bm in `_config.py`, all work fine.

```
mathjax_config:
      tex:
        macros:
            # Fix for \bm, see https://github.com/mathjax/MathJax/issues/1219#issuecomment-341059843
            "bm": ["\\boldsymbol{#1}",1]
            
```

PDF build (22/11/22) fixed for photoionization theory sect. with:

No `\bm` case (i.e. not set in `_config.py` for latex preamble), subs as:

- \hat{\mathbf{\mu}} >> \hat{\boldsymbol{\mu}}

- \boldsymbol{\mathbf{E}} >> \boldsymbol{\mathrm{E}}. May only be an issue if bm loaded? Ah, yes - this is OK without bm, but get errors at `\bm` of course.

- \bm >> \boldsymbol, have this only for \bm{r} it seems, may want \mathrm here too? NEED TO LOOK CAREFULLY - can use former in general (scalar) case (or just plain r), latter in vector case.

+++

$$\mathbf{\hat{\mu}}$$

+++

**More possible issues with hats and fonts**

Getting broken PDF builds with error ```! Internal error: bad native font flag in `map_char_to_glyph'```

Seems to be triggered by AF channel func eqn (although find in Jupyter and HTML):

$$
\bar{\varUpsilon}_{L,M}^{u,\zeta\zeta'}=(-1)^{M}[P]^{\frac{1}{2}}E_{P-R}(\hat{e};\mu_{0})(-1)^{(\mu'-\mu_{0})}\bar{\Lambda}_{R'}(\mu,P,R')B_{L,S-R'}(l,l',m,m')\Delta_{L,M}(K,Q,S)A_{Q,S}^{K}(t)
$$ (eq:channelFunc-AF-defn)

Bar or hat?  See https://tex.stackexchange.com/questions/63244/internal-error-bad-native-font-flag-xelatex-fontspec-newtxmath-libertine

YES - bar, $\bar{\varUpsilon}$ fails, but $\varUpsilon$ is OK.

Adding to preamble as suggested FAILS (also tried some other fixes!)

```
        % ** Testing more maths stuff, from https://tex.stackexchange.com/questions/578375/mathcal-incompatible-with-unicode-math
        % \usepackage{unicode-math}
        % \setmathfont{XITS Math}[Scale = MatchUppercase ]
        % \setmathfont{Latin Modern Math}[range = {cal,bfcal},Scale = MatchUppercase ]
        % ** Similar from https://tex.stackexchange.com/questions/227033/why-cant-i-use-my-font-with-unicode-math
        % \usepackage{unicode-math}
        % \setmathfont{Latin Modern Math}
        % \usepackage{mathspec}
        % \setmathfont(Latin,Digits,Greek){Latin Modern Sans}
        % \setmathrm{Latin Modern Sans}
        % ** Per https://github.com/wspr/unicode-math/issues/400 
        % \usepackage[mathbf=sym]{unicode-math}
```        

Changing Latex builder in `_config.yml` also not helping (or not working - might need clean build?).

See also https://tex.stackexchange.com/questions/159785/caveats-of-newtxmath-and-fontspec-together, suggests   \usepackage[no-math]{fontspec}

MAY NEED TO CHANGE SPHINX PART OF PREAMBLE FOR THIS? This already loads some extensions - specifically fontspec - before user-specced stuff, so get latex package options clash errors.

WORK AROUND - $\bar{\varUpsilon_{L,M}}$ is OK, AS IS $\bar{\varUpsilon_{}}$ **USE THIS VERSION**

+++

## Quotes

In quick tests just noticed that "" seems to work fine in both HTML and Latex output - not sure why for the latter. Might be UTF8 smart-quotes in Latex? Not sure if this is good, see https://tex.stackexchange.com/questions/52351/quote-marks-are-backwards-using-texmaker-pdflatex

+++

Tests:

- "Normal quotes"
- ``Latex style''
- "with escape\"
- ``Alt latex style"

Looks like only normal quotes are consistent over build types. Should check in Sphinx docs?

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
