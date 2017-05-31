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
Define a model and instantiate with data ``splcge.dat``::

    test_cge = SimpleCGE("splcge.dat")

To solve the model, using the Minos solver on `NEOS <neos-server.org/neos>`_::

    test_cge.model_solve("neos", "minos")

Other nonlinear solvers available on NEOS: Ipopt, Knitro


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

