---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.4
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Holoviews render tests
31/01/23

Working OK for wrapping Plotly surfaces (PAD plots, see various plotly test notebooks), but failing for Bokeh plots (2D matrix plots)...?

Ran into issue for density matrix plotting in theory chpt, see http://jake:9966/lab/tree/QM3/doc-source/part1/theory_observables_intro_211122.ipynb

Original code from MF recon manuscript, which pushed to static layout, see http://jake/jupyter/user/paul/doc/tree/code-share/stimpy-docker-local/MFPADs_recon_manuscript_dev_April_2022/MFrecon_manuscript_fig_generation_170422-Stimpy_MAIN-oldPkgs.ipynb. Note this has hvSave code, not sure if this made it elsewhere.

UPDATE 31/01/23 pm: worked on first build (for HTML output)... but not later? WTF? Actually, was OK eventually, just had to reload page and wait (issues with Ice Dragon rendering?). Still not working in main page however, maths bug issue?

+++

## Setup

```{code-cell} ipython3
:tags: [hide-cell]

# Run default config - may need to set full path here
%run '../scripts/setup_notebook.py'

# Override plotters backend?
# plotBackend = 'pl'
```

```{code-cell} ipython3
:tags: [hide-output]

# Setup symmetry-defined matrix elements using PEMtk

# Import class
from pemtk.sym.symHarm import symHarm

# Compute hamronics for Td, lmax=4
sym = 'D2h'
lmax=4

lmaxPlot = 2  # Set lmaxPlot for subselection on plots later.

# Glue items for later
glue("symHarmPGmatE", sym, display=False)
glue("symHarmLmaxmatE", lmax, display=False)
glue("symHarmBasislmaxPlot", lmaxPlot, display=False)

# TODO: consider different labelling here, can set at init e.g. dims = ['C', 'h', 'muX', 'l', 'm'] - 25/11/22 code currently fails for mu mapping, remap below instead
symObj = symHarm(sym,lmax)
# symObj = symHarm(sym,lmax,dims = ['Cont', 'h', 'muX', 'l', 'm'])

# To plot using ePSproc/PEMtk class, these values can be converted to ePSproc BLM data type...

# Run conversion - the default is to set the coeffs to the 'BLM' data type
dimMap = {'C':'Cont','mu':'muX'}
symObj.toePSproc(dimMap=dimMap)

# Run conversion with a different dimMap & dataType
dataType = 'matE'
# symObj.toePSproc(dimMap = {'C':'Cont','h':'it', 'mu':'muX'}, dataType=dataType)
symObj.toePSproc(dimMap = dimMap, dataType=dataType)
# symObj.toePSproc(dimMap = {'C':'Cont','h':'it'}, dataType=dataType)   # Drop mu > muX mapping for now
# symObj.coeffs[dataType]

# Example using data class (setup in init script)
data = pemtkFit()

# Set to new key in data class
dataKey = sym
data.data[dataKey] = {}

for dataType in ['matE','BLM']:
    data.data[dataKey][dataType] = symObj.coeffs[dataType]['b (comp)'].sum(['h','muX'])  # Select expansion in complex harmonics, and sum redundant dims
    data.data[dataKey][dataType].attrs = symObj.coeffs[dataType].attrs
```

```{code-cell} ipython3
# Compute basis functions for given matrix elements

# Set data
data.subKey = dataKey

# Using PEMtk - this only returns the product basis set as used for fitting
BetaNormX, basisProduct = data.afblmMatEfit(selDims={}, sqThres=False)

# Using ePSproc directly - this includes full basis return if specified
BetaNormX2, basisFull = ep.geomFunc.afblmXprod(data.data[data.subKey]['matE'], basisReturn = 'Full', selDims={}, sqThres=False)  #, BLMRenorm = BLMRenorm, **kwargs)

# The basis dictionary contains various numerical parameters, these are investigated below.
# See also the ePSproc docs at https://epsproc.readthedocs.io/en/latest/methods/geometric_method_dev_260220_090420_tidy.html
print(f"Product basis elements: {basisProduct.keys()}")
print(f"Full basis elements: {basisFull.keys()}")

# Use full basis for following sections
basis = basisFull
```

```{code-cell} ipython3
# DEMO CODE FROM http://jake/jupyter/user/paul/doc/tree/code-share/stimpy-docker-local/MFPADs_recon_manuscript_dev_April_2022/MFrecon_manuscript_fig_generation_170422-Stimpy_MAIN-oldPkgs.ipynb
# SEE ALSO DOCS, https://epsproc.readthedocs.io/en/dev/methods/density_mat_notes_demo_300821.html#Density-Matrices

# Import routines
from epsproc.calc import density

# Compose density matrix

# Set dimensions/state vector/representation
# These must be in original data, but will be restacked as necessary to define the effective basis space.
denDims = 'LM'  #, 'mu']
selDims = None  #{'Type':'L'}
pTypes=['r','i']
thres = 1e-4    # 0.2 # Threshold out l>3 terms if using full 'orb5' set.
normME = False
normDen = 'max'

# Calculate - Ref case
# matE = data.data['subset']['matE']
# Set data from master class
# k = 'orb5'  # N2 orb5 (SG) dataset
# k = 'subset'
k = sym
matE = data.data[k]['matE']
if normME:
    matE = matE/matE.max()

daOut, *_ = density.densityCalc(matE, denDims = denDims, selDims = selDims, thres = thres)  # OK

if normDen=='max':
    daOut = daOut/daOut.max()
elif normDen=='trace':
    daOut = daOut/(daOut.sum('Sym').pipe(np.trace)**2)  # Need sym sum here to get 2D trace
    
# daPlot = density.matPlot(daOut.sum('Sym'))
daPlot = density.matPlot(daOut.sum('Sym'), pTypes=pTypes)

# # Retrieved
# matE = data.data['agg']['matE']['compC']
# if normME:
#     matE = matE/matE.max()

# daOut2, *_ = density.densityCalc(matE, denDims = denDims, selDims = selDims, thres = thres)  # OK

# if normDen=='max':
#     daOut2 = daOut2/daOut2.max()
# elif normDen=='trace':
#     daOut2 = daOut2/(daOut2.sum('Sym').pipe(np.trace)**2)
    
# daPlot2 = density.matPlot(daOut2.sum('Sym'), pTypes=pTypes)   #.sel(Eke=slice(0.5,1.5,1)))


# # Compute difference
# daDiff = daOut.sum('Sym') - daOut2.sum('Sym')
# daDiff.name = 'Difference'
# daPlotDiff = density.matPlot(daDiff, pTypes=pTypes)

# #******** Plot
# daLayout = (daPlot.layout('pType') + daPlot2.opts(show_title=False).layout('pType').opts(show_title=False) + daPlotDiff.opts(show_title=False).layout('pType')).cols(1)  # No cols? AH - set to 1 works.
# # daLayout.opts(width=300, height=300)  # Doesn't work?
# daLayout.opts(hvPlotters.opts.HeatMap(width=300, frame_width=300, aspect='square', tools=['hover'], colorbar=True, cmap='coolwarm'))  # .opts(show_title=False)  # .opts(title="Custom Title")  #OK
```

```{code-cell} ipython3
# OPTIONAL PLOT SETTINGS?
# General size & range unless overridden
figSize = [700,300]
tRange = [3.8, 5.2]  # Set for axis slice, also for cmapping lims

# Update defaults
ep.plot.hvPlotters.setPlotters(width = figSize[0], height = figSize[1], snsStyle = 'white')
```

```{code-cell} ipython3
# Raw plot
daPlot
```

```{code-cell} ipython3
#******** Plot  with layout
from epsproc.plot import hvPlotters  # Additional plotting code
daLayout = (daPlot.layout('pType')).cols(1)  # No cols? AH - set to 1 works.
# daLayout.opts(width=300, height=300)  # Doesn't work?
daLayout.opts(hvPlotters.opts.HeatMap(width=300, frame_width=300, aspect='square', tools=['hover'], colorbar=True, cmap='coolwarm'))  # .opts(show_title=False)  # .opts(title="Custom Title")  #OK
```

```{code-cell} ipython3
# Test with glue

glue("glueTest", daPlot, display=False)
```

```{glue:figure} glueTest
---
name: "fig-glueTest"
---
Raw output to glue.
```

+++

Normal glue fails for PDF output (but OK for HTML).

Feb 2023: Now have wrapper glueHV() for this...

```{code-cell} ipython3
# Test with glueHV()

glueHV("glueTestGHV", daPlot)
glueHV("realOnlyGHV", daPlot.select(pType='Real'))
```

```{glue:figure} glueTestGHV
---
name: "fig-glueTestGHV"
---
Raw output to glueHV.
```

+++

```{glue:figure} realOnlyGHV
---
name: "fig-realOnlyGHV"
---
Real only output to glueHV.
```

+++

## Test new glue wrapper/decorator (09/02/23)

See https://realpython.com/primer-on-python-decorators/

09/02/23: basically working, but for Holomaps may have issues with stacked dims. Also seems to change/force cmap on save? TBC.

UPDATE: now implemented in `setup_notebook.py` too.

```{code-cell} ipython3
# def superglue(func):
def glueDecorator(func):
    '''Decorator for glue() with interactive plot types forced to static for PDF builds.'''
    
    def glueWrapper(name,fig,**kwargs):
        
        # Set names for file out
        # Note imgFormat and imgPath should be set globally, or passed as kwargs.
        imgFile = f'{name}.{imgFormat}'
        imgFile = os.path.join(imgPath,imgFile)
        
        # Set glue() output according to fig type and build env.
        # Note buildEnv should be set globally, or passed as a kwarg.
        if buildEnv != 'pdf':
            return func(name, fig, display=False)  # For non-PDF builds, use regular glue()
        
        else:
            # Holoviews object
            # NOTE this may give unexpected results in some cases for Holomaps - may want to force flatten?
            # Note for Bokeh backend may need additional pkgs, selenium, firefox and geckodriver
            # See https://holoviews.org/user_guide/Plots_and_Renderers.html#saving-and-rendering
            if 'holoviews' in str(type(fig)):
                # Force render and glue
                hv.save(fig, imgFile, fmt=imgFormat)
                
            elif 'plotly' in str(type(fig)):
                fig.write_image(imgFile,format=imgFormat)  # See https://plotly.com/python/static-image-export/
                
            
            # Glue static render
            return func(name, Image(imgFile), display=False)
        
        
    return glueWrapper
```

```{code-cell} ipython3
glue = glueDecorator(glue)
```

```{code-cell} ipython3
glue("glueTestDec", daPlot)
```

```{glue:figure} glueTestDec
---
name: "fig-glueTestDec"
---
Raw output to glue decorated with superglue().
```

```{code-cell} ipython3
daLayout = (daPlot.layout('pType')).cols(1)
glue("glueTestDecLayout", daLayout)
```

```{glue:figure} glueTestDecLayout
---
name: "fig-glueTestDecLayout"
---
Raw layout to glue decorated with superglue().
```

```{code-cell} ipython3
type(daLayout)
```

## Check Plotly compatibility

For original tests see http://jake:9966/lab/tree/QM3/doc-source/tests/plotly_pdf_export_test_181122.ipynb

```{code-cell} ipython3
# Test from https://github.com/executablebooks/jupyter-book/issues/1410#issuecomment-984661412
import plotly.graph_objects as go
# import plotly.io as pio
# pio.renderers.default = "png"  # This works for PDF export, but also forces png in HTML case.
ifig = go.Figure(go.Scatter(x=[1,2], y=[1,2]))
ifig.show()
```

```{code-cell} ipython3
type(ifig)
```

```{code-cell} ipython3
glue("glueTestPlotly", ifig)
```

```{glue:figure} glueTestPlotly
---
name: "fig-glueTestPlotly"
---
Plotly figure to glue decorated with superglue().
```
