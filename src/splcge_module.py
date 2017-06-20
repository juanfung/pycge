# Import packages
from pyomo.environ import *
import pandas as pd
import numpy as np
import pickle
from pyomo.opt import SolverResults
import time
import os
from pyomo.opt import SolverStatus, TerminationCondition
import splcge_model_def



class SimpleCGE:
    """Pyomo port of splcge.gams from GAMS model library"""
    """Inputs: dat, solver """


    def __init__(self):

        # -----------------------------------------------------#
        #ABSTRACT MODEL DEF
        splcge_model_def.Model_Def.model_abstract(self)     #define model
        splcge_model_def.Model_Def.model_sets(self)         #define sets
        splcge_model_def.Model_Def.model_param(self)        #define params/calibration/variables
        splcge_model_def.Model_Def.model_constraints(self)  #define constraints 
        splcge_model_def.Model_Def.model_obj(self)          #define objective
        splcge_model_def.Model_Def.check(self)              #print that everything was loaded
        


        # TODO:
        # separate each of these steps into functions,
        # can then import function defs
        # def model_sets, def model_params, def model_contraints, def model_objective...
        # also: model_calibrate, model_sim, model_shock, ...


    # -----------------------------------------------------#
    #LOAD DATA
    def model_data(self, data_dir = ''):
        
        if (data_dir == ""):
            print("Please specify where you would like to load data from")
        
        elif not os.path.exists(data_dir):
            print("please enter a valid data directory")
        
        else:
        
            data = DataPortal()
            
            for filenames in os.listdir(data_dir):
                if filenames.startswith("set"):                
    
                    dat_type,names,file_type = filenames.split('-')
                    data.load(filename = data_dir + filenames, format = 'set', set = names)                
                    print("File '" + filenames + "' was loaded into set: " + names)
                    
                elif filenames.startswith("param"):
                    
                    dat_type,names,file_type = filenames.split('-')
                    print("File '" + filenames + "' was loaded into param: " + names)             
    
                    data.load(filename = data_dir + filenames, param = names, format='array')
                
                else:
                    print(filenames, " is not in the right format and was not loaded into DataPortal")
                    
            self.data = data


    # -----------------------------------------------------#
    #CREATE INSTANCE
    def model_instance(self):
        
        try:
        
            self.instance = self.m.create_instance(self.data)
            self.instance.pf['LAB'].fixed = True
            
            print("Instance created. Call `model_postprocess` to output.")
        
        except:
            print("Unable to create instance. Please make sure data is loaded")
               
        
    # -----------------------------------------------------#
    #MODIFY INSTANCE    
    def pyomo_modify_instance(self, options=None, model=None, instance=None):
        
        try:
        
            self.instance.X['BRD'].value = 10.0
            self.instance.X['BRD'].fixed = True
        
            print("Instance updated. Call `model_postprocess` to output.")  
            
        except:
            print("Unable to modify instance. Please make sure a 'calibration' instance as already been created")
    

    # -----------------------------------------------------#
    #SOLVE
    def model_solve(self, mgr, solver):
               
        with SolverManagerFactory(mgr) as solver_mgr:
            self.results = solver_mgr.solve(self.instance, opt=solver)
            self.instance.solutions.store_to(self.results)
        
        print("Model solved. Call `model_postprocess` to output.")
        

        if (self.results.solver.status == SolverStatus.ok) and (self.results.solver.termination_condition == TerminationCondition.optimal):
            print('Solution is optimal and feasible')
        elif (self.results.solver.termination_condition == TerminationCondition.infeasible):
            print("Model is infeasible")
        else:
            print ('WARNING. Solver Status: ',  self.result.solver.status)

            
    # -----------------------------------------------------#
    #OUTPUT
    def model_postprocess(self, object_name = "" , verbose=""):
                           
        if (object_name==""):
            print("please specify what you would like to output")
        
        elif (object_name=="instance"):
            print_function(verbose, output=self.instance.display, typename="instance")
        
        elif (object_name=="results"):
            print_function(verbose, output=self.results.write, typename = "results")
        
        elif (object_name=="vars") or (object_name=="obj") or (object_name=="pickle"):
            moment=time.strftime("%Y-%b-%d__%H_%M_%S",time.localtime())
            if(verbose==""):
                print("Please enter where to export to")
            else: 
                if not os.path.exists(verbose):
                    print(verbose, "directory did not exist so one was created")
                    os.makedirs(verbose)
        
                if (object_name=="vars"):
                    print("Vars saved to: \n")
                    for v in self.instance.component_objects(Var, active=True):
                        with open(verbose + str(v) + "_"+  moment + '.csv', 'w') as var_output:
                            print(str(verbose + str(v) + "_"+  moment + '.csv'))
                            varobject = getattr(self.instance, str(v))
                            var_output.write ('{},{} \n'.format('Names', varobject ))
                            for index in varobject:
                                var_output.write ('{},{} \n'.format(index, varobject[index].value))
    
            
                if(object_name=="obj"): 
                    with open(verbose + "obj_" + moment + ".csv", 'w') as obj_output:
                        obj_output.write ('{},{}\n'.format("objective", value(self.instance.obj)))
                    print("Objective saved to: " + str(verbose + "obj_" + moment + ".csv"))
        
                if(object_name=="pickle"):             
                    with open(verbose + 'saved_results_' + moment, 'wb') as pickle_output:
                        pickle.dump(self.results, pickle_output)
                    print("Pickled results object saved to:  " + str(verbose + 'saved_results_' + moment))
            
        
        else:
            print("Please enter a valid object_name" )



    # -----------------------------------------------------#
    #IMPORT RESULTS OBJECT    
    def model_load_results(self, pathname):
        
        if not os.path.exists(pathname):
            print(pathname, " does not exist. Please enter a valid path to the file you would like to load")
        
        else:
            
            try:

                with open(pathname, 'rb') as pkl_file:
                    loadedResults = pickle.load(pkl_file)
                    self.instance.solutions.load_from(loadedResults)
                    print("results from: ", pathname, " were loaded to instance")
            
            except:
                
                print("Unable to load file. Please make sure correct file is specified. Must be pickled.")


# -----------------------------------------------------#
#PRINT    
def print_function (verbose="", output = "", typename=""):
    
    if (verbose==""):
        print("Please specify how you would like to output")            
    elif (verbose=="print"):
        print("\nThis is the " + typename + "\n")
        output()
        print("Output printed")            
    else:            
        moment=time.strftime("%Y-%b-%d__%H_%M_%S",time.localtime())
        directory = (verbose)
        if not os.path.exists(directory):
            print(verbose, "directory did not exist so one was created")
            os.makedirs(directory)
            
        with open(verbose + typename + moment, 'w') as output_file:
            output_file.write("\nThis is the " + typename + "\n" )
            output(ostream=output_file)
        print("Output saved to: " + str(verbose + typename + moment))
