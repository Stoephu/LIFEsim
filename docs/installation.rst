Installation (Linux and Mac OS)
===============================

LIFEsim is available for installation from |github|. It is compatible with Python 3.8.

.. Hint:: **Installation on Mac OS**

   We recommend the usage of a package manager for mac (e.g. |Conda|). Follow the installation
   instruction given by the respective package manager, making sure that you use the correct
   version of python (3.8).

   Open a terminal window and activate conda by running

   .. code-block:: console

      $ conda activate

Virtual Environment
-------------------

It is highly recommended to install LIFEsim in a *virtual environment*. This ensures installed
packages and changes made do not affect other projects on a system. The package dependencies of
LIFEsim are best managed with a package manager like pip.

As a first step, *virtualenv* is installed with pip

.. code-block:: console

   $ pip install virtualenv

Then a virtual environment in the folder ``new_folder`` is created in the current directory

.. code-block:: console

   $ virtualenv -p python3.8 new_folder

.. Hint:: You might need to deactivate the conda base

   .. code-block:: console

      $ conda deactivate

To activate and deactivate your new virtual environment use the following statement respectively

.. code-block:: console

   $ source path_to_new_folder/new_folder/bin/activate

Check that you are using the correct python version.

.. code-block:: console

   $ python --version
   Python 3.8.X

.. code-block:: console

   $ deactivate

Download from PyPI (Recommended)
--------------------------------

First, activate the virtual environment as shown above. LIFEsim can be installed from PyPI using
the pip command.

.. code-block:: console

   $ pip install lifesim

LIFEsim need a modified version of the package |SpectRes| to run. It can also be installed using
pip. Run

.. code-block:: console

   $ pip install git+https://github.com/fdannert/SpectRes.git

Download from Github
--------------------

Navigate to the directory in which you desire to place the LIFEsim repository. Then clone the
repository from Github by executing

.. code-block:: console

   $ git clone https://github.com/fdannert/LIFEsim.git

.. Hint:: If ``git`` is not installed on your system run

   .. code-block:: console

      $ sudo apt install git

The dependencies required by LIFEsim can be installed with

.. code-block:: console

   $ pip install -r LIFEsim/requirements.txt

To upgrade already installed dependencies to LIFEsim requirements run

.. code-block:: console

   $ pip install --upgrade -r LIFEsim/requirements.txt

.. Important::
   LIFEsim need a modified version of the package |SpectRes| to run. Please install it via the
   following procedure.

   First, make sure that you are in the directory where you want to install SpectRes. Then run

   .. code-block:: console

      $ git clone https://github.com/fdannert/SpectRes.git

The last step is point the Python install of your virtual environment to LIFEsim and SpectRes.
Please do so by running

.. code-block:: console

   $ echo "export PYTHONPATH='$PYTHONPATH:/path_to_LIFEsim/LIFEsim/:/path_to_SpectRes/SpectRes/'" >> path_to_new_folder/new_folder/bin/activate

Testing the Installation
------------------------

To test the installation, open a new console and activate the virtual environment as above. Then
open Python and import LIFEsim with

.. code-block:: console

   $ python

.. code-block:: python

   >>> import lifesim

If the import statement executes, the installation has been successful. As an extra test run

.. code-block:: python

   >>> lifesim.util.constants.c
   299792000.0

This should return the speed of light in [m s
:math:`^{-1}`
].

.. Hint:: If the ``import lifesim`` command fails, the reason is likely that the the ``PYTHONPATH``
   is not set correctly. To check for this please run in Python (started with the virtual
   environment active as above)

   .. code-block:: python

      >>> import sys
      >>> sys.path

   If the path to LIFEsim ``'/path_to_LIFEsim/LIFEsim/'`` is not returned in the results, please
   open the file ``path_to_new_folder/new_folder/bin/activate`` with a text editor of your choice.
   Then make sure that the last line of the file reads

   .. code-block:: none

      export PYTHONPATH=':/path_to_LIFEsim/LIFEsim/'

    The same test can be performed if SpectRes does not import.


.. |github| raw:: html

   <a href="https://github.com/fdannert/LIFEsim" target="_blank">Github</a>

.. |SpectRes| raw:: html

   <a href="https://github.com/ACCarnall/SpectRes" target="_blank">SpectRes</a>

.. |Homebrew| raw:: html

   <a href="https://brew.sh" target="_blank">Homebrew</a>

.. |Conda| raw:: html

   <a href="https://conda.io/projects/conda/en/latest/user-guide/install/index.html" target="_blank">Miniconda</a>
