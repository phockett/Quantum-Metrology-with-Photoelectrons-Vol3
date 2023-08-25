# QM3 builds with Docker

## Method 1: Pull image from DockerHub

Docker images, including the full book source and all required packages, are [available from Docker hub](https://hub.docker.com/r/epsproc/quantum-met-vol3), simply run `docker pull epsproc/quantum-met-vol3` to pull a copy.
The Docker images contain the book source, along with all required packages and Jupyter Lab (based on the [Jupyter Docker Stacks Scipy image](https://jupyter-docker-stacks.readthedocs.io/en/latest/index.html)). Book source files are available in the container at `github/Quantum-Metrology-with-Photoelectrons-Vol3/`. For more details on the Jupyter Lab base container, see the [Jupyter Docker Stacks website](https://jupyter-docker-stacks.readthedocs.io/en/latest/index.html).


## Method 2: Build from Dockerfiles

Dockerfiles for a full environment build, including ePSproc, PEMtk, JupyterLab and JupyterBook, are in `/docker`.

There are two files, one for the base environment, and a second which adds ePSproc, PEMtk and QM3 files to this. They can be used to build an image as follows:

```bash
docker build . -f Dockerfile-qm3-base-pkgs -t quantum-met-vol3-base
docker build . -f Dockerfile-qm3-base-pkgs -t quantum-met-vol3
```

These match the images on DockerHub, with the caveat that one can modify the build chain - note, in particular, the choice of Github branches to pull ePSproc and QM3 source.


## Running a container

The  `docker run epsproc/quantum-met-vol3` to run with default settings (which uses port 8888 for JupyterLab). The Jupyter Lab interface will be available at http://localhost:8888, with default password `qm3`. (To specify a port at run time, add `-p <newPort>:8888` to the run command, e.g. `docker run -p 9999:8888 epsproc/quantum-met-vol3` to set port to 9999.) 


## Other options

### Terminal in container

Use `exec -it <container> bash` to attach to a running container, or `run -it <container> bash` to spin one up, and connect to the terminal.

E.g. for named container as above: `docker exec -it quantum-met-vol3 bash`.

### General run script

As per the [Jupyter Docker Stacks](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/common.html#start-sh) base container docs, the `start.sh` script can be used to execute processes other than Jupyter Lab startup, with the syntax `docker run -it --rm quantum-met-vol3 start.sh <command to execute>`. 

E.g. `docker run -it --rm quantum-met-vol3 start.sh ipython` will spin up a container and start an ipython session.


## Notes

For more details & options, see:

- [Jupyter Docker Stacks](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/running.html).
- [Dockerfile reference](https://docs.docker.com/engine/reference/builder/).
- [Docker Compose reference](https://docs.docker.com/compose/compose-file/compose-file-v3/).

For use with full JupyterHub deployment, see https://github.com/phockett/jupyterhub-docker.

For related tools and Docker builds, see the [Open Photoionization Docker Stacks](https://github.com/phockett/open-photoionization-docker-stacks).

