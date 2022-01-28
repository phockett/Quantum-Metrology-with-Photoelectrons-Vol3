[]{#anchor}Quantum Metrology with Photoelectrons Vol. 3: *Analysis
methodologies*

Notes for proposal (following outline doc “IOP ebook proposal form
v010920.docx”)

02/09/21, v1

General overview:\
Vol. 3. will focus on analysis techniques for quantum metrology with
photoelectrons, including:

-   Interpreting experimental data.
-   Extraction/reconstruction/determination of quantum mechanical
    properties (matrix elements, wavefunctions, density matrices) from
    experimental data.
-   Comparison of experimental and theoretical data.
-   New analysis methodologies & techniques.
-   Introduction to newly-developed software platform (see below).

Provisional contents:

**Part 1: theory & software** (general review & update of the topic,
including recent theory developments)

1.  Introduction

    a.  Topic overview.

    b.  Context of vol. 3 (following vols. 1 & 2).

    c.  Aims: Vol. 3 in the series will continue the exploration of
        > quantum metrology with photoelectrons, with a focus on
        > numerical analysis techniques, forging a closer link between
        > experimental and theoretical results, and making the
        > methodologies discussed directly accessible via a new software
        > platform/ecosystem.

2.  Quantum metrology software platform/ecosystem overview

    a.  Introduction to python packages for simulation, data analysis,
        > and open-data.

    b.  Photoelectron metrology toolkit (PEMtk) package/platform for
        > experimental data processing & analysis. (See
        > [*pemtk.readthedocs.io*](https://pemtk.readthedocs.io).)

    c.  ePSproc package for theory & simulation. (See
        > [*epsproc.readthedocs.io*](https://epsproc.readthedocs.io).)

    d.  ePSdata platform for data/results library
        > ([*https://phockett.github.io/ePSdata/about.html\#Motivation*](https://phockett.github.io/ePSdata/about.html#Motivation)).

3.  General method development: geometric tensor treatment of
    photoionization, fitting & matrix-inversion techniques

    a.  Theory development overview - tensor methods (e.g.
        > [*https://epsproc.readthedocs.io/en/latest/methods/geometric\_method\_dev\_pt3\_AFBLM\_090620\_010920\_dev\_bk100920.html*](https://epsproc.readthedocs.io/en/latest/methods/geometric_method_dev_pt3_AFBLM_090620_010920_dev_bk100920.html))

    b.  Direct molecular frame reconstruction via matrix-inversion
        > methods (see Gregory, Margaret, Paul Hockett, Albert Stolow,
        > and Varun Makhija. “Towards Molecular Frame Photoelectron
        > Angular Distributions in Polyatomic Molecules from Lab Frame
        > Coherent Rotational Wavepacket Evolution.” *Journal of Physics
        > B: Atomic, Molecular and Optical Physics* 54, no. 14 (July
        > 2021): 145601.[
        > ](https://doi.org/10.1088/1361-6455/ac135f)[*https://doi.org/10.1088/1361-6455/ac135f*](https://doi.org/10.1088/1361-6455/ac135f).)

4.  Numerical implementation & analysis platform tools

    a.  Tensor methods implementation in ePSproc/PEMtk.

    b.  Information content analysis (inc. basis-set exploration, e.g.
        > [*https://pemtk.readthedocs.io/en/latest/fitting/PEMtk\_fitting\_basis-set\_demo\_050621-full.html*](https://pemtk.readthedocs.io/en/latest/fitting/PEMtk_fitting_basis-set_demo_050621-full.html)
        > ), see also vol. 2, sect. 12.1.

    c.  Density matrix analysis. (e.g.
        > [*https://epsproc.readthedocs.io/en/dev/methods/density\_mat\_notes\_demo\_300821.html*](https://epsproc.readthedocs.io/en/dev/methods/density_mat_notes_demo_300821.html))

    d.  Generalised bootstrapping implementation in PEMtk (see vol. 2,
        > sects. 11.3 & 12.3)

**Part 2: numerical examples** (open-source worked examples using the
new software platform)

1.  Quantum metrology example: generalised bootstrapping for a
    homonuclear diatomic scattering system (N2)\*

    a.  Experimental data overview & simulation.

    b.  Matrix element extraction (bootstrap protocol, see vol. 2,
        > sects. 11.3 & 12.3) & statistical analysis.

    c.  Direct molecular frame reconstruction via matrix-inversion
        > methods.

    d.  Comparison of methods.

    e.  Information content/quantum information analysis. (See vol. 2,
        > sect. 12.1.)

2.  Quantum metrology example: generalised bootstrapping for a
    heteronuclear scattering system (CO)\*

    a.  Experimental data overview & simulation.

    b.  Matrix element extraction (bootstrap protocol, see vol. 2,
        > sects. 11.3 & 12.3) & statistical analysis.

    c.  Direct molecular frame reconstruction via matrix-inversion
        > methods.

    d.  Comparison of methods.

    e.  Information content/quantum information analysis. (See vol. 2,
        > sect. 12.1.)

3.  Quantum metrology example: generalised bootstrapping and
    matrix-inversion methods for a complex/general asymmetric top
    scattering system (C2H4 (ethylene))\*

    a.  Experimental data overview & simulation.

    b.  Matrix element extraction (bootstrap protocol, see vol. 2,
        > sects. 11.3 & 12.3) & statistical analysis.

    c.  Direct molecular frame reconstruction via matrix-inversion
        > methods.

    d.  Comparison of methods.

    e.  Information content/quantum information analysis.

4.  Future directions & outlook
5.  Summary & conclusions

\* Exact choice of “simple” and “complex” systems may change, but should
include a homonuclear diatomic and/or heteronuclear diatomic, and
symmetric and asymmetric top polyatomic systems. May also include an
atomic example.
