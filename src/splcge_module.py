# Import packages
from pyomo.environ import *
import pandas as pd
import numpy as np
import pickle
from pyomo.opt import SolverResults
import time
import os



class SimpleCGE:
    """Pyomo port of splcge.gams from GAMS model library"""
    """Inputs: dat, solver """


    def __init__(self, dat):
        self.model_data(dat)
        self.model_abstract()
        #self.model_instance()

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
            return model.sam[i, 'HOH']

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
                          initialize=FF_init,
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

    def model_instance(self, verbose=""):
        self.instance = self.m.create_instance(self.data)
        self.instance.pf['LAB'].fixed = True
        
        if (verbose==""):
            print("Finished")
            
        elif (verbose=="print"):
            print("\nThis is the instance display: \n")
            self.instance.display()
            print("Finished")
            
        else:
            
            moment=time.strftime("%Y-%b-%d__%H_%M_%S",time.localtime())
            directory = (verbose)
            if not os.path.exists(directory):
                os.makedirs(directory)
                
            with open(verbose + "_instance_" + moment, 'w') as output_file:
                output_file.write("\nThis is the instance.display(): \n" )
                self.instance.display(ostream=output_file)
            print("Finished")


    def model_solve(self, mgr, solver, verbose=""):
        
        with SolverManagerFactory(mgr) as solver_mgr:
            results = solver_mgr.solve(self.instance, opt=solver)
            self.instance.solutions.store_to(results)

        if (verbose==""):
            print("Finished")
            
        elif (verbose=="print"):
            print("These are the solver results: \n")
            results.write()
            print("Finished")
            
        else:
            
            moment=time.strftime("%Y-%b-%d__%H_%M_%S",time.localtime())
            directory = (verbose)
            if not os.path.exists(directory):
                os.makedirs(directory)
                
            with open(verbose + "_results_" + moment, 'w') as output_file:
                output_file.write("These are the solver results: \n")
                results.write(ostream=output_file)
            print("Finished")
            
            
        
        
            

    def model_postprocess(self, options):
        self.instance.obj.display()
        self.instance.X.display()
        self.instance.px.display()
        self.instance.Z.display()
        

    def model_output(self, pathname, save_obj=True):
        moment=time.strftime("%Y-%b-%d__%H_%M_%S",time.localtime())
        directory = (pathname)
        if not os.path.exists(directory):
                os.makedirs(directory)
        for v in self.instance.component_objects(Var, active=True):
            with open(pathname + str(v) + moment + '.csv', 'w') as var_output:  
                varobject = getattr(self.instance, str(v))
                var_output.write ('{},{} \n'.format('Names', varobject ))
                for index in varobject:
                    var_output.write ('{},{} \n'.format(index, varobject[index].value))
        if save_obj==True:
            with open(pathname + "obj" + moment + ".csv", 'w') as obj_output:
                obj_output.write ('{},{}\n'.format("objective", value(self.instance.obj)))
    
    def model_save_results(self, pathname):
        moment=time.strftime("%Y-%b-%d__%H_%M_%S",time.localtime())
        directory = (pathname)
        if not os.path.exists(directory):
                os.makedirs(directory)
        myResults=SolverResults()
        self.instance.solutions.store_to(myResults)
        # myResults.write() #just a test to make sure myResults is populated with solution
        with open(pathname + 'saved_results_' + moment, 'wb') as pickle_output:
            pickle.dump(myResults, pickle_output)
    
    def model_load_results(self, pathname):
        with open(pathname, 'rb') as pkl_file:
            loadedResults = pickle.load(pkl_file)
            # loadedResults.write() #another test to make sure nothing is changing
            self.instance.solutions.load_from(loadedResults)
            # self.instance.display()
            
    
    
            
            


# Example calls:
    
# Define model and instantiate:
# test_cge = SimpleCGE("splcge.dat")

# Solve the model, using Minos solver on NEOS:
# test_cge.model_solve("neos", "minos")

# save results
# test_cge.model_save_results(r'./results/results_Results')
# other solvers: "ipopt", "knitro"

#output log file
#test_cge.model_solve("neos","minos",verbose=r'./test_directory/')

#create instance
#test_cge.model_instance(verbose=r'./instance_folder/')

# TODO:
# 1. Testing
#    - Test module instantiates same model as ConcreteModel()
#    - Test each function
# 2. Data import via DataPortal vs pandas vs AMPL format...
# 3. Updating model (e.g., change a paramater, add a constraint, ...)
# 4. Output: printing, saving results