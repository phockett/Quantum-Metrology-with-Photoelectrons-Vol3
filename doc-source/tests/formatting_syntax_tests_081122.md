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

+++

## Testing raw latex...

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

## Include

+++

Include with `{include}` directive:

```{include} testInclude.txt
```

```{code-cell} ipython3

```
