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

+++ {"tags": []}

# Bibliography

% Testing full bib generation.

% Note on per-doc bibs with `unsrt`: IF USING PER-DOCUMENT THIS MESSES UP PDF REFS, get repeated ref numbering as per each doc - way to specify this for HTML builds only? Maybe append notebook cell at processing (cf. ePSdata methods), or fix in latex post-processing, natch. Nothing obvious in quite google search.

% However, manually generating full bib here does produce correctly-numbered list (but might not match individual docs!).

% 10/11/22 Full page actually works quite nicely in HTML too, although missing back-links. Best plan to leave off individual docs for now, for consistency over HTML and PDF, but can add in via preprocessing later as footer if desired.

+++

% Per document case.
```{bibliography}
:filter: docname in docnames
:style: unsrt
```

+++

% Full book bib (NOTE this is added automatically to PDF build, so heading may appear twice if including this page)
```{bibliography}
:style: unsrt
```

```{code-cell} ipython3

```
