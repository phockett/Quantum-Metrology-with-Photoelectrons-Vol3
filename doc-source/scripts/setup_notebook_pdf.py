DON'T USE - now fixed by env var passing in setup_notebook_main.py

# Pull main script, will usually be run on notebook path
# TODO: fix paths!
#       Quick fix with Path below, from https://stackoverflow.com/a/51149057
#       FAILING with syntax errors? Weird...
# TODO: test force exec, doesn't force on sequential build?

# exec("../scripts/setup_notebook_main.py")

print("\n*** Running PDF setup defaults")
# Set Plotly render
import plotly.io as pio
pio.renderers.default = "png" 


from pathlib import Path 
script_dir=Path(__file__).parent 
main_script_path=(script_dir / 'setup_notebook_main.py').resolve()
print(main_script_path)

# exec(main_script_path.as_posix())  # Failing with path?

# More robust...? From https://stackoverflow.com/a/6357418
# with open(main_script_path, "rb") as source_file:
#     code = compile(source_file.read(), main_script_path, "exec")
# exec(code, globals, locals)  # This fails?

# Simpler form
with open(main_script_path, "rb") as infile:
    exec(infile.read())

    
# print("\n*** Running PDF setup defaults")
# # Set Plotly render
# import plotly.io as pio
# pio.renderers.default = "png" 