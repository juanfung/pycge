# Import packages
from pyomo.environ import *
import pandas as pd
import numpy as np


class SimpleCGE:
    """Pyomo port of splcge.gams from GAMS model library"""
    """Inputs: dat, solver """


    def __init__(self, dat):
        self.model_data(dat)
        self.model_instance()

    def model_abstract(self):
        self.m = AbstractModel()
        
        # ----------------------------------------------- #
        #DEFINE SETS
        self.m.i = Set(doc='goods')
        self.m.h = Set(doc='factor')
        self.m.u = Set(doc='SAM entry')

        
        # ----------------------------------------------- #
        #DEFINE PARAMETERS
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
        
        def FF_init(model, h):
            return model.sam['HOH', h]
        
        self.m.FF = Param(self.m.h,
                          initilize=FF_init,
                          doc = 'factor endowment of the h-th factor')
        
        # --------------------------------------------- #
        # CALIBRATION
        
        def alpha_init(model, i):
            return model.X0[i] / sum(model.X0[j] for j in model.i) 
        
        self.m.alpha = Param(self.m.i,
                             initialize=alpha_init,
                             doc='share parameter in utility function')
        
        def beta_init(model, h, i):
            return model.F0[h, i] / sum(model.F0[k, i] for k in model.h)

        self.m.beta = Param(self.m.h, self.m.i,
                            initialize=beta_init,
                            doc='share parameter in production function')
        
        def b_init(model, i):
            return model.Z0[i] / np.prod([model.F0[h, i]**model.beta[h, i] for h in model.h])

        self.m.b = Param(self.m.i,
                         initialize=b_init,
                         doc='scale parameter in production function')
        
        # -----------------------------------------------------#
        #Define model system
        #DEFINE VARIABLES
        
        self.m.X = Var(self.m.i,
                       initialize=X0_init,
                       within=PositiveReals,
                       doc='household consumtion of the i-th good')
        
        self.m.F = Var(self.m.h, self.m.i,
                       initialize=F0_init,
                       within=PositiveReals,
                       doc='the h-th factor input by the j-th firm')
        
        self.m.Z = Var(self.m.i,
                       initialize=Z0_init,
                       within=PositiveReals,
                       doc='output of the j-th good')
        
        def p_init(model, v):
            return 1
        
        self.m.px = Var(self.m.i,
                        initialize=p_init,
                        within=PositiveReals,
                        doc='demand price of the i-th good')
        
        self.m.pz = Var(self.m.i,
                        initialize=p_init,
                        within=PositiveReals,
                        doc='supply price of the i-th good')
        
        #are these two (px and pz) supposed to be the exact same?
        
        self.m.pf = Var(self.m.h,
                        initialize=p_init,
                        within=PositiveReals,
                        doc='the h-th factor price')
        
        # ------------------------------------------------------ #
        # DEFINE EQUATIONS
        # define constraints
        
        def eqX_rule(model, i):
            return (model.X[i] == model.alpha[i] * sum(model.pf[h] * model.FF[h] / model.px[i] for h in model.h))
        
        self.m.eqX = Constraint(self.m.i,
                                rule=eqX_rule,
                                doc='household demand function')
        
        
       def eqpz_rule(model, i):
           return (model.Z[i] == model.b[i] * np.prod([model.F[h, i]**model.beta[h, i] for h in model.h]))
 
       self.m.eqpz = Constraint(self.m.i,
                                 rule=eqpz_rule,
                                 doc='production function')
       

        def eqF_rule(model, h, i):
            return (model.F[h, i] == model.beta[h, i] * model.pz[i] * model.Z[i] / model.pf[h])

        self.m.eqF = Constraint(self.m.h, self.m.i,
                                rule=eqF_rule,
                                doc='factor demand function')


        def eqpx_rule(model, i):
            return (model.X[i] == model.Z[i])

        self.m.eqpx = Constraint(self.m.i,
                                 rule=eqpx_rule,
                                 doc='good market clearning condition')


        def eqpf_rule(model, h):
            return (sum(model.F[h, j] for j in model.i) == model.FF[h])

        self.m.eqpf = Constraint(model.h,
                                 rule=eqpf_rule,
                                 doc='factor market clearning condition')


        def eqZ_rule(model, i):
            return (model.px[i] == model.pz[i])

        self.m.eqZ = Constraint(self.m.i,
                                rule=eqZ_rule,
                                doc='price equation')
        
        # ------------------------------------------------------- #
        # DEFINE OBJECTIVE


        def obj_rule(model):
            return np.prod([model.X[i]**model.alpha[i] for i in model.i])

        self.m.obj = Objective(rule=obj_rule,
                               sense=maximize,
                               doc='utility function [fictitious]')
        
        # ------------------------------------------------------- #
        # CREATE MODEL INSTANCE
        
        

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
        
        #Do we want the outputs the same as the demo/does it matter?

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
