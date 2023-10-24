# Quantum Metrology with Photoelectrons Vol. 3: *Analysis methodologies*

By Paul Hockett with Varun Makhija

Quantum Metrology with Photoelectrons Volume 3: *Analysis
methodologies*, an open source executable book. This repository contains the source documents (mainly Jupyter Notebooks in Python) and notes for the book, as of July 2023 the first draft is complete, and the [current HTML build can be found online](https://phockett.github.io/Quantum-Metrology-with-Photoelectrons-Vol3/). The book is due to be published in late 2023, and by IOP Press - see below for more details.

[![Jupyter Book Badge](https://jupyterbook.org/badge.svg)](https://phockett.github.io/Quantum-Metrology-with-Photoelectrons-Vol3/)
[![DOI](https://zenodo.org/badge/449878450.svg)](https://zenodo.org/badge/latestdoi/449878450)


## About the books

Photoionization is an interferometric process, in which multiple paths can contribute to the final continuum photoelectron wavefunction. At the simplest level, interferences between different final angular momentum states are manifest in the energy and angle resolved photoelectron spectra: metrology schemes making use of these interferograms are thus phase-sensitive, and provide a powerful route to detailed understanding of photoionization. In these cases, the continuum wavefunction (and underlying scattering dynamics) can be characterised. At a more complex level, such measurements can also provide a powerful probe for other processes of interest, leading to a more general class of quantum metrology built on phase-sensitive photoelectron imaging.  Since the turn of the century, the increasing availability of photoelectron imaging experiments, along with the increasing sophistication of experimental techniques, and the availability of computational resources for analysis and numerics, has allowed for significant developments in such photoelectron metrology.

![QMbooks](https://github.com/phockett/Quantum-Metrology-with-Photoelectrons-Vol3/blob/postSubmissionUpdates/notes/cover_art/mock_covers_3vol_230823.png?raw=true)

- Volume I covers the core physics of photoionization, including a range of computational examples. The material is presented as both reference and tutorial, and should appeal to readers of all levels. ISBN 978-1-6817-4684-5, http://iopscience.iop.org/book/978-1-6817-4684-5 (IOP Press, 2018)

- Volume II explores applications, and the development of quantum metrology schemes based on photoelectron measurements. The material is more technical, and will appeal more to the specialist reader. ISBN 978-1-6817-4688-3, http://iopscience.iop.org/book/978-1-6817-4688-3 (IOP Press, 2018)

Additional online resources for Vols. I & II can be found on [OSF](https://osf.io/q2v3g/wiki/home/) and [Github](https://github.com/phockett/Quantum-Metrology-with-Photoelectrons).

- Volume III in the series continues this exploration, with a focus on numerical analysis techniques, forging a closer link between experimental and theoretical results, and making the methodologies discussed directly accessible via new software. The book is due for publication by IOP in 2023; this volume is also open-source, with a live HTML version at https://phockett.github.io/Quantum-Metrology-with-Photoelectrons-Vol3/ and source available at https://github.com/phockett/Quantum-Metrology-with-Photoelectrons-Vol3.


## Technical details

This repository contains:

- `doc-source` the source documents (mainly Jupyter Notebooks in Python)
- `notes` additional notes for the book, 
- gh-pages branch contains the current HTML build, available at https://phockett.github.io/Quantum-Metrology-with-Photoelectrons-Vol3/

The project has been setup to use the [Jupyter Book](https://jupyterbook.org/) build-chain (which uses Sphinx on the back-end) to generate HTML and Latex outputs for publication from source Jupyter notebooks & markdown files. 

The work *within* the book will make use of the [Photoelectron Metrology Toolkit](https://pemtk.readthedocs.io/en/latest/about.html) platform for working with experimental & theoretical data.

For further technical details, [see Chpt. 2 in the book](https://phockett.github.io/Quantum-Metrology-with-Photoelectrons-Vol3/part1/platform_intro_070723.html).

![Photoelectron metrology platform diagram](https://raw.githubusercontent.com/phockett/PEMtk/4eec9217203bfd1aee13bd8b64952dc1ac5fef89/docs/doc-source/figs/QM_unified_schema_wrapped_280820.gv.png)


### Running code examples

Each Jupyter notebook (`*.ipynb`) can be treated as a stand-alone computational document. These can be run/used/modified independently with an appropriately setup python environment, for details [see Chpt. 2 in the book](https://phockett.github.io/Quantum-Metrology-with-Photoelectrons-Vol3/part1/platform_intro_070723.html#installation-and-environment-set-up).

### Docker builds

Docker images, including the full book source and all required packages, are [available from Docker hub](https://hub.docker.com/r/epsproc/quantum-met-vol3), simply run `docker pull epsproc/quantum-met-vol3` to pull a copy, then `docker run epsproc/quantum-met-vol3` to run with default settings (which uses port 8888 for JupyterLab). The Jupyter Lab interface will be available at http://localhost:8888, with default password `qm3`. (To specify a port at run time, add `-p <newPort>:8888` to the run command, e.g. `docker run -p 9999:8888 epsproc/quantum-met-vol3` to set port to 9999.)

The Docker images contain the book source, along with all required packages and Jupyter Lab (based on the [Jupyter Docker Stacks Scipy image](https://jupyter-docker-stacks.readthedocs.io/en/latest/index.html)). Book source files are available in the container at `github/Quantum-Metrology-with-Photoelectrons-Vol3/`. For more details on the Jupyter Lab base container, see the [Jupyter Docker Stacks website](https://jupyter-docker-stacks.readthedocs.io/en/latest/index.html).

For the source Dockerfiles and additional notes, [see `/docker` in the QM3 github repository](https://github.com/phockett/Quantum-Metrology-with-Photoelectrons-Vol3/tree/main/docker).

Archived versions can also be found on Zenodo: [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.8286020.svg)](https://doi.org/10.5281/zenodo.8286020)

### Building the book

The full book can also be built from source in a suitably configured environment ([see Chpt. 2 in the book](https://phockett.github.io/Quantum-Metrology-with-Photoelectrons-Vol3/part1/platform_intro_070723.html#installation-and-environment-set-up)):

1. Clone this repository
2. Run `pip install -r requirements.txt` (it is recommended you do this within a virtual environment)
3. (Optional) Edit the books source files located in the `doc-source/` directory
4. Run `jupyter-book clean doc-source/` to remove any existing builds
5. Run `jupyter-book build doc-source/`

A fully-rendered HTML version of the book will be built in `doc-source/_build/html/`.


## Credits

This project is created using the open source [Jupyter Book project](https://jupyterbook.org/) and the [executablebooks/cookiecutter-jupyter-book template](https://github.com/executablebooks/cookiecutter-jupyter-book).

To add: build env & main software packages (see automation for this...)
