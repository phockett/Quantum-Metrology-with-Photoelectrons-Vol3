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

+++

## Testing raw latex...

Both options fail in PDF and HTML export tests.

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

With MyST-rst wrapper

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

Testing maths only

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
