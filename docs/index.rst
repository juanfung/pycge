.. pycge documentation master file, created by
   sphinx-quickstart on Wed May 31 12:14:09 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pycge's documentation!
=================================

Contents:

.. toctree::
   :maxdepth: 2

Getting Ready
---------------

This program is written in ``python 3`` and depends on the ```pyomo`` <http://www.pyomo.org>`_ 
package::

    pip install pyomo
    # install pyomo dependencies
    pyomo install-extras

See `<http://www.pyomo.org/installation/>`_ for more details on installation, 
and `the documentation <http://www.pyomo.org/documentation/>`_ for info on the package.

Small to moderately sized problems may be handles through the use of remote solvers
on the `NEOS Server <https://neos-server.org/neos/>`_, which is accessible by ``pyomo``.

To use a *local* solver, see below.

Before using this program, it is neccesary to prepare your data.
All data should be stored in a single directory with no other
files, other than the ones that will be used. All files should be .csv files and
should be named as follows: type-name-.csv

For example:


A file containing the set "h" should be named::

        set-h-.csv
     
While a file containing a parameter "sam" should be named::

        param-sam-.csv


Quick Start
------------

A quick summary of a standard workflow::

     # create model definition object
     testdef = ModelDef()
     # create pycge object
     testcge = PyCGE(testdef)
     # add data
     testcge.load_data(path/to/data)
     # create base instance
     testcge.model_instance()
     # calibrate base instance
     testcge.model_calibrate(mgr, solver) 
     # create sim instance to modify
     testcge.model_sim() 
     # modify sim instance
     testcge.model_modify_instance(...) # modify some value
     testcge.model_modify_instnace(...) # modify another value
     # solve sim instance
     testcge.model_solve(mgr, solver) 
     # compare base and sim equilibria
     testcge.model_compare(base, sim)

Read on for more details.

Getting Started
---------------
Define a model::

    test_def = ModelDef()

Create a model from a ``ModelDef``::

    test_cge = PyCGE(test_def)

Load the data::

    test_cge.model_data(directory/that/contains/data/files)


Instantiate the model::

    test_cge.model_instance()


Calibrate the Base Model
------------------------

The initial call to ``model_instance()`` creates a ``base`` model.
To calibrate the ``base`` model::

     test_cge.model_calibrate()

This call solves the ``base`` model. A successful calibration should return
equilibrium values equal to the initial values.

If calibration fails, check your data and your model definition.

Equilibrium Comparative Statics
-------------------------------

Once the ``base`` model is calibrated, we can simulate policy changes or shocks to
our economy and perform comparative statics (i.e., comparing the equilibria with and
without the policy change). 

First, create a ``sim`` instance::

     test_cge.model_sim()

This step creates a second instance called ``sim`` by copying the ``base`` instance. 

Now you can explore a policy change relative to ``base`` by modifying the ``sim`` 
instance (changing a parameter value or fixing a variable). 

To modify an instance::

    test_cge.model_modify_instance(NAME, INDEX, VALUE, fix=True)

where 
- ``NAME`` is a string (the name of the ``Var`` or ``Param`` to be modified) 
- ``INDEX`` is a string (the index where the modification will be made) 
- ``VALUE`` is numeric (the modification)

For example, to modify a variable ``X`` so that ``X[i] == 0``::

     test_cge.model_modify_instance('X', 'i', 0)

Note that the default for modifying a variable means *fixing* it at some value. 
To unfix a variable simply pass ``fix=False`` into the function call. 

Also note that in order to modify a two-dimensional parameter, it must be surrounded by parenthesis.
For example::
    test_cge.model_modify_instance('F0',('CAP','BRD'),0)

To solve the ``sim`` instance, e.g., 
using the Minos solver on `NEOS <neos-server.org/neos>`_::

    test_cge.model_solve("neos", "minos")

**Remark**: Other nonlinear solvers available on NEOS include
- ``"conopt" 
- "ipopt" 
- "knitro"``

To perform comparative statics::

     test_cge.model_compare(base, sim)

This returns the *difference* in equilibrium values between ``base`` and ``sim``.

Viewing an Instance or Results
------------------------------

To export anything::
    
    test_cge.model_postprocess(object_name="", verbose="")

- To output display of instance
    - ``object_name="instance"``
        - ``verbose="print"`` to print instance display
        - ``verbose="directory/name/"`` to export instance display in a file
        
- To output display of results
    - ``object_name="results"``
        - ``verbose="print"`` to print results display
        - ``verbose="directory/name/"`` to export results display in a file

- To output variables as a .csv file
    - ``object_name="vars"``
        - ``verbose="directory/name/"`` to export each variable in a file

- To output objective as a .csv file
    - ``object_name="obj"``
        - ``verbose="directory/name/"`` to export obj in a file

- To output dilled instance object (can later be loaded)
    - ``object_name="dill_instance"``
        - ``verbose="directory/name/"`` to export dilled instance object in a file
        
Updating
---------------

To load an instance object(with results attached) back in as ``base`` instance (set base=False to load as ``sim`` instance)::

    test_cge.model_load_instance(pathname = pathname/of/file/to/load, base=True)

Two or More Simulations
-------------------------

Currently, an object of class ``PyCGE`` can only have two instances associated with it,
``base`` and ``sim``. 

Calling ``model_sim`` always creates a new ``sim`` based on the ``base`` instance.
If you call ``model_modify_instance`` *after* solving ``sim``, you will overwrite the 
previous ``sim`` instance. 

If you want to analyze multiple policy changes or shocks (i.e., you want to analyze multiple
``sim`` instances) **and** you want to keep each ``sim`` instance, the easiest thing to do 
is to copy your existing object and perform the new simulation on the copy::

     import copy
     copy_cge = deepcopy(test_cge)
     copy_cge.model_sim()
     copy_cge.model_modify_instance()
     # etc.

Now you can perform comparative statics on two ``sim`` instances, one associated with the
``test_cge`` object and one associated with the ``copy_cge`` object. Both have the same 
``base`` instance but potentially differ in the ``sim`` instance. 

Local Solvers
--------------

TODO: Add info on installing Ipopt, etc.

Working With Model Definitions
------------------------------

A model definition is contained within a ``ModelDef`` class, and should be imported along with
``PyCGE``::

    import pycge
    from model_def import ModelDef

You may work with multiple ``ModelDef`` classes, e.g., ``ModelDef1``, ``ModelDef2``, and so on.
You may also edit an existing ``ModelDef`` and re-load it using ``importlib``::

    importlib.reload(ModelDef)




Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

