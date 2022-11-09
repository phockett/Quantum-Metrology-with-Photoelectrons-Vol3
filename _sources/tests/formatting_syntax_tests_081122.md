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

+++

### Substitution tests

See https://jupyterbook.org/en/stable/content/content-blocks.html?highlight=substitutions#substitutions-and-variables-in-markdown

For global subs define in `_config.yml`. Uses Jinja on backend.

Basic: {{ test_sub }}

Sub test with URL: {{ PEMtk_repo }}

+++

## Fig testing (from file)

+++

As a figure, see https://jupyterbook.org/en/stable/content/figures.html

```{figure} ../images/QM_unified_schema_wrapped_280820_gv.png
---
name: qm-platform-diag-test
---
Here is my figure caption!
```

+++ {"tags": []}

## Fig testing (from URL)

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
