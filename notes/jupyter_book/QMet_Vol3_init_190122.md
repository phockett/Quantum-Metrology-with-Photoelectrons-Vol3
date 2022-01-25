---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.13.6
kernelspec:
  display_name: Python [conda env:root] *
  language: python
  name: conda-root-py
---

# Quantum Metrology with Photoelectron Vol. 3 Initial Setup
19/01/22

As per normal, see also https://jupyterbook.org/start/publish.html

Repo: https://github.com/phockett/Quantum-Metrology-with-Photoelectrons-Vol3

+++

## Local config (Jake)

```{code-cell} ipython3
!hostname
```

```{code-cell} ipython3
%cd ~/github
```

```{code-cell} ipython3
!git clone git@github.com:phockett/Quantum-Metrology-with-Photoelectrons-Vol3.git
```

```{code-cell} ipython3
!ls
```

## Create template

+++

Basic template generated with, e.g., `jupyter-book create mynewbook/`. For mroe complex case, use cookiecutter...

+++

At CLI with cookie cutter (first requires `pip install cookiecutter`).

```
(jbookTestv2) paul@jake:~/notebooks/jupyterBook_2022$ jupyter-book create mynewbook-ccTest/ --cookiecutter
author_name [Captain Jupyter]: Paul Hockett
github_username [paulhockett]: phockett
book_name [My Book]: Quantum Metrology with Photoelectrons Vol. 3
book_slug [quantum_metrology_with_photoelectrons_vol._3]:     
book_short_description [This cookiecutter creates a simple boilerplate for a Jupyter Book.]: Quantum metrology with photoelectrons volume 3, open source executable book.
version ['0.1.0']: 
Select open_source_license:
1 - MIT license
2 - BSD license
3 - ISC license
4 - Apache Software License 2.0
5 - GNU General Public License v3
6 - None
Choose from 1, 2, 3, 4, 5, 6 [1]: 5
Select include_ci:
1 - github
2 - gitlab
3 - no
Choose from 1, 2, 3 [1]: 1

===============================================================================

Your book template can be found at

    /mnt/femtobackSSHFS/DriveSyncShare/code-share/jake-notebooks/jupyterBook_2022/mynewbook-ccTest/quantum_metrology_with_photoelectrons_vol._3/

===============================================================================

(jbookTestv2) paul@jake:~/notebooks/jupyterBook_2022$ ls mynewbook-ccTest/
quantum_metrology_with_photoelectrons_vol._3
(jbookTestv2) paul@jake:~/notebooks/jupyterBook_2022$ ls mynewbook-ccTest/quantum_metrology_with_photoelectrons_vol._3/
CONDUCT.md  CONTRIBUTING.md  LICENSE  quantum_metrology_with_photoelectrons_vol._3  README.md  requirements.txt

```

+++

This looks good, so copy to Github project with a few mods...

```
(jbookTestv2) paul@jake:~/notebooks/jupyterBook_2022/mynewbook-ccTest/quantum_metrology_with_photoelectrons_vol._3$ mv quantum_metrology_with_photoelectrons_vol._3/ doc-source
(jbookTestv2) paul@jake:~/notebooks/jupyterBook_2022/mynewbook-ccTest$ cp -r quantum_metrology_with_photoelectrons_vol._3/* ~/github/Quantum-Metrology-with-Photoelectrons-Vol3/

```

```{code-cell} ipython3
!ls ~/github/Quantum-Metrology-with-Photoelectrons-Vol3/
```

## Build

```{code-cell} ipython3
# Build test
# condaEnv = 'jbookTest'
condaEnv = 'jbookTestv2'
# condaEnv = 'qe-mini-example'
bookRoot = '~/github/Quantum-Metrology-with-Photoelectrons-Vol3/doc-source'

# HTML
!conda run -n {condaEnv} jupyter-book build {bookRoot}

# !conda run -n {condaEnv} jupyter-book build ./mynewbook --builder pdflatex
```

```{code-cell} ipython3
# Test gh-pages branch push...
ghp-import -n -p -f _build/html
```

## TODO

+++

TODO:

- Push to GH. DONE.
- Setup actions. Basic set from CookieCutter in place. DONE. Note this is set for gh-pages branch push, go with that for now.
- Make notes dir and move this there! DONE.
- More testing for writing & formats.
- Modify project setup...
- Travis (or other?) for testing and CI.

```{code-cell} ipython3

```
