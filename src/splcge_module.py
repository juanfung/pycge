# Import packages
from pyomo.environ import *
import pandas as pd
import numpy as np


class SimpleCGE:
    """Pyomo port of splcge.gams from GAMS model library"""
    """Inputs: dat, solver """
    """this is the first test change"""

    def __init__(self, dat):
        self.model_data(dat)
        self.model_instance()

    def model_abstract(self):
        self.m = AbstractModel()
        # Define sets
        self.m.i = Set(doc='goods')
        self.m.h = Set(doc='factor')
        self.m.u = Set(doc='SAM entry')
        # Define parameters, variables, constraints, objective...
        self.m.sam = Param(self.m.u, self.m.u,
                           doc='social accounting matrix')

        def X0_init(model, i):
            # is it necessary to use self.m?
            return model[i, 'HOH']

        self.m.X0 = Param(self.m.i,
                          initialize=X0_init,
                          doc='hh consumption of i-th good')

        def F0_init(model, h, i):
            return model.sam[h, i]

        self.m.F0 = Param(self.m.h, self.m.i,
                          initialize=F0_init,
                          doc='h-th factor input by j-th firm')

        def Z0_init(model, i):
            return sum(model.F0[h, i] for h in model.h)

        self.m.Z0 = Param(self.m.i,
                          initialize=Z0_init,
                          doc='output of j-th good')

        def obj_rule(model):
            return np.prod([model.X[i]**model.alpha[i] for i in model.i])

        self.m.obj = Objective(rule=obj_rule,
                               sense=maximize,
                               doc='utility function [fictitious]')

        # TODO:
        # separate each of these steps into functions,
        # can then import function defs
        # def model_sets, def model_params, def model_contraints, def model_objective...
        # also: model_calibrate, model_sim, model_shock, ...

    def model_data(self, dat):
        self.data = dat
        # self.data = DataPortal()

    def model_instance(self):
        # TODO: unnecessary to self.instance?
        self.instance = self.m.create_instance(self.data)
        self.instance.pf['LAB'].fixed = True
        self.instance.pprint()  # to view the model instance

    def model_solve(self, mgr, solver):
        with SolverManagerFactory(mgr) as solver_mgr:
            results = solver_mgr.solve(self.instance, opt=solver)
            results.write()

    def model_postprocess(self, options):
        self.instance.obj.display()
        self.instance.X.display()
        self.instance.px.display()

    def model_output(self):
        # save results


# Example calls:
# Define model and instantiate:
# test_cge = SimpleCGE("splcge.dat")
# Solve the model, using Minos solver on NEOS:
# test_cge.model_solve("neos", "minos")
# other solvers: "ipopt", "knitro"

# TODO:
# 1. Testing
#    - Test module instantiates same model as ConcreteModel()
#    - Test each function
# 2. Data import via DataPortal vs pandas vs AMPL format...
# 3. Updating model (e.g., change a paramater, add a constraint, ...)
# 4. Output: printing, saving results
