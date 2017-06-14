.. pycge documentation master file, created by
   sphinx-quickstart on Wed May 31 12:14:09 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pycge's documentation!
=================================

Contents:

.. toctree::
   :maxdepth: 2


Getting Started
---------------
Define a model with data ``splcge.dat``::

    test_cge = SimpleCGE("splcge.dat")

Instantiate the model::

    test_cge.model_instance()

To solve the model, using the Minos solver on `NEOS <neos-server.org/neos>`_::

    test_cge.model_solve("neos", "minos")

- Other nonlinear solvers available on NEOS: Ipopt, Knitro

Viewing
---------------

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

To modify an instance (a "shock")::

    test_cge.pyomo_modify_instance()



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

