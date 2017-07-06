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

     # create object
     testcge = SimpleCGE()
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

    test_cge = SimpleCGE()

Load the data::

    test_cge.model_data(directory/that/contains/data/files)


Instantiate the model::

    test_cge.model_instance()


Calibrate the base model
------------------------

The initial call to ``model_instance()`` creates a ``base`` model.
To calibrate the ``base`` model::

     test_cge.model_calibrate()

This call solves the ``base`` model. A successful calibration should return
equilibrium values equal to the initial values.

If calibration fails, check your data and your model definition.

Equilibrium comparative statics
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

Viewing an instance or results
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

- To output pickled results object (can later be used to load back into an instance)
    - ``object_name="pickle"``
        - ``verbose="directory/name/"`` to export pickled results object in a file
        
Updating
---------------

To load a results object back into an instance::

    test_cge.model_load_results(pathname = pathname/of/file/to/load)

Two or more simulations
-------------------------

Currently, an object of class `SimpleCGE` can only have two instances associated with it,
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

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

