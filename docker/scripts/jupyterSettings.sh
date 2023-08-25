#!/bin/bash

# Configure some Jupyter options.
# 25/10/22
#
# Mainly sets open IP for connection. This shouldn't be necessary in Docker, but can sometimes get repeated "Replacing stale connection" and kernel disconnects without, may be an Nginx issue.
# See https://discourse.jupyter.org/t/troubleshoot-terminal-hangs-on-launch-docker-image-fails-in-linux-works-in-macos/2829/4
# And https://github.com/jupyter/notebook/issues/625
# And https://jupyter-server.readthedocs.io/en/latest/operators/public-server.html#running-a-public-notebook-server
#
# Optional:
# - Set a hashed password here.
# - Config any other options.
#
# 29/05/23 - added some updates, NEEDS TESTING.
# 12/07/23 - set password to "qm3" for book builds.

# Set Jupyter server options
jupyter server --generate-config -y
sed -e "s/# c.ServerApp.ip = 'localhost'/c.ServerApp.ip = '*'/" /home/jovyan/.jupyter/jupyter_server_config.py > /home/jovyan/.jupyter/jupyter_server_config-2.py
# sed -e "s/# c.ServerApp.password = ''/c.ServerApp.password = 'u'<set a hashed password here>'/" /home/jovyan/.jupyter/jupyter_server_config.py.test > /home/jovyan/.jupyter/jupyter_server_config.py.test2
# sed -e "s/# c.ServerApp.password = ''/c.ServerApp.password = 'u'argon2:\\$argon2id\\$v=19\\$m=10240,t=10,p=8\\$qNnFiyTBNqgY\\+i4OaDU\\+Ww\\$B2N/hEO689onY0qVTuXx5fo8ehXpwyCCpwmt0oeAH0w'/" /home/jovyan/.jupyter/jupyter_server_config-2.py > /home/jovyan/.jupyter/jupyter_server_config-3.py

# Password = qm3
sed -e "s/# c.ServerApp.password = ''/c.ServerApp.password = u'sha1:7b532ec196cd:59943c3fc152f159d70161d07846b1abee5f3188'/" /home/jovyan/.jupyter/jupyter_server_config-2.py > /home/jovyan/.jupyter/jupyter_server_config-3.py
mv /home/jovyan/.jupyter/jupyter_server_config-3.py /home/jovyan/.jupyter/jupyter_server_config.py
# 15/05/23 - this no longer seems to work, Jupyter throws error with password line on start. But looks identical to case set in login screen?
# Rebuild needed?
# 29/05/23 - noticed extra ' before u in config file, may have been the issue, possibly now fixed above.

# 16/05/23 Also need these? Getting a lot of drops of kernel and container, and Tornado HTTP errors in logs. Config options changed?
# c.ServerApp.allow_origin = '*'
# c.ServerApp.allow_remote_access = True

# 29/05/23 - testing port settings, may have been source of drops...?
# Had this set on Stimpy version, but not in this script!
# c.ServerApp.port = 8888
sed -e "s/# c.ServerApp.port = 0/c.ServerApp.port = 8888/" /home/jovyan/.jupyter/jupyter_server_config.py > /home/jovyan/.jupyter/jupyter_server_config-test1.py


# Also note that
# In logs: 'ip' has moved from NotebookApp to ServerApp. This config will be passed to ServerApp. Be sure to update your config before our next release.


# Set Jupyter notebook options
jupyter notebook --generate-config -y
sed -e "s/# c.NotebookApp.allow_origin = ''/c.NotebookApp.allow_origin =  '*'/" /home/jovyan/.jupyter/jupyter_notebook_config.py > /home/jovyan/.jupyter/jupyter_notebook_config-2.py
mv /home/jovyan/.jupyter/jupyter_notebook_config-2.py /home/jovyan/.jupyter/jupyter_notebook_config.py

# Copy reference settings
cp -r /home/jovyan/.jupyter /home/jovyan/.jupyter_ref-build
