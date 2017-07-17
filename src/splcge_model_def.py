# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 15:58:43 2017

@author: cmb11
"""
from pyomo.environ import *

import numpy as np





class SplModelDef:

    
    def model(self):
    
    # ----------------------------------------------- #
    #DEFINE MODEL


        self.m = AbstractModel()
        
        
    # ----------------------------------------------- #
    #DEFINE SETS       

        
        self.m.i = Set(doc='goods')
        self.m.h = Set(doc='factor')
        self.m.u = Set(doc='SAM entry')
        
        
    # ----------------------------------------------- #
    #DEFINE PARAMETERS, CALIBRATION, VARIABLES       

    
        # ----------------------------------------------- #
        #PARAMETERS 
        self.m.sam = Param(self.m.u, self.m.u, 
                           doc='social accounting matrix', mutable = True)


        def X0_init(model, i):
            return model.sam[i, 'HOH']

        self.m.X0 = Param(self.m.i,
                          initialize=X0_init,
                          doc='hh consumption of i-th good', mutable = True)

        def F0_init(model, h, i):
            return model.sam[h, i]

        self.m.F0 = Param(self.m.h, self.m.i,
                          initialize=F0_init,
                          doc='h-th factor input by j-th firm', mutable = True)

        def Z0_init(model, i):
            return sum(model.F0[h, i] for h in model.h)

        self.m.Z0 = Param(self.m.i,
                          initialize=Z0_init,
                          doc='output of j-th good', mutable = True)
        
        def FF_init(model, h):
            return model.sam['HOH', h]
        
        self.m.FF = Param(self.m.h,
                          initialize=FF_init,
                          doc = 'factor endowment of the h-th factor', mutable = True)
        
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
        #VARIABLES
        self.m.X = Var(self.m.i,
                       initialize=X0_init,
                       within=PositiveReals,
                       doc='household consumption of the i-th good')
        
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

        
        self.m.pf = Var(self.m.h,
                        initialize=p_init,
                        within=PositiveReals,
                        doc='the h-th factor price')
    
    # ------------------------------------------------------ #
    # DEFINE CONSTRAINTS

        
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

        self.m.eqpf = Constraint(self.m.h,
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
    # ----------------------------------------------- #
    #PRINT THAT EVERYTHING WAS LOADED  

        print("splcge model loaded")
        return self.m