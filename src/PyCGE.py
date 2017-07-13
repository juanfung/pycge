# Import packages
from pyomo.environ import *
import pandas as pd
import numpy as np
import pickle
from pyomo.opt import SolverResults
import time
import os
from pyomo.opt import SolverStatus, TerminationCondition
import importlib




class PyCGE:
    """Pyomo port of splcge.gams from GAMS model library"""
    """Inputs: dat, solver """

# --------------------------------------------------------#
# LOAD MODEL
    def __init__(self, model_def):


        self.m = model_def.model()


    # -----------------------------------------------------#
    #LOAD DATA
    def model_data(self, data_dir = ''):
        
        if not data_dir.endswith("/") and data_dir != "":
            data_dir = data_dir + "/"
        
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


    def model_instance(self):
        
        try:
        
            self.base = self.m.create_instance(self.data)
            self.base.pf['LAB'].fixed = True
            
            print("BASE instance created. Call `model_postprocess` to output or `model_calibrate` to solve.")
        
        except:
            print("Unable to create BASE instance. Please make sure model and data are loaded")
              

    def model_sim (self):
        
        try:
            
            if self.base:
                
                try:
                
                    if self.base_results:
            
                        self.sim = self.m.create_instance(self.data)
                        self.sim.pf['LAB'].fixed = True
                        
                        print("SIM instance created. Note, this is currently the same as BASE. Call `model_modify_instance` to modify.")
                        
                except AttributeError:
                    print("You must calibrate first")
        
        except AttributeError:
            print("You must create BASE instance first.")
        
    
    def model_modify_instance(self,NAME,INDEX,VALUE,fix=True):

        try:
    
            _object = getattr(self.sim, NAME)
            print(_object[INDEX], "was originally", _object[INDEX].value)
            _object[INDEX].value = VALUE 
            print(_object[INDEX], " is now set to ", _object[INDEX].value)


            for v in self.sim.component_objects(Var, active=True):
                if str(v)==NAME:
                    varobject = getattr(self.sim, str(v))
                    if fix == True:
                        varobject[INDEX].fixed = True
                        print("Note, ", _object[INDEX], " is now fixed")
                    if fix == False:
                        varobject[INDEX].fixed = False
                        print("Note, ", _object[INDEX], " is NOT fixed")


            print("SIM updated. Call `model_postprocess` to output or `model_solve` to solve.")  
            
        except:
            print("Unable to modify instance. Please make sure SIM instance has already been created and that you are trying to access the correct component")
    


    def model_calibrate(self, mgr, solver):
        
        
        try:
            if self.base:
                try:
                    if self.base_results:
                        print('Model already calibrated. If a SIM has been created, call `model_solve` to solve it.')
                except AttributeError:
                        with SolverManagerFactory(mgr) as solver_mgr:
                            self.base_results = solver_mgr.solve(self.base, opt=solver)
                            self.base.solutions.store_to(self.base_results)
                        
                        print("Model solved. Call `model_postprocess` to output.")
                    
            
                        if (self.base_results.solver.status == SolverStatus.ok) and (self.base_results.solver.termination_condition == TerminationCondition.optimal):
                            print('Solution is optimal and feasible')
                        elif (self.base_results.solver.termination_condition == TerminationCondition.infeasible):
                            print("Model is infeasible")
                        else:
                            print ('WARNING. Solver Status: ', self.base_results.solver)  
        except AttributeError:
            print('You must create the BASE instance before you can solve it. Call `model_instance` first.')



    def model_solve(self, mgr, solver):

        try:
            if self.base_results:
                try:
                    if self.sim:
                        with SolverManagerFactory(mgr) as solver_mgr:
                            self.sim_results = solver_mgr.solve(self.sim, opt=solver)
                            self.sim.solutions.store_to(self.sim_results)
                        
                        print("Model solved. Call `model_postprocess` to output.")
                    
            
                        if (self.sim_results.solver.status == SolverStatus.ok) and (self.sim_results.solver.termination_condition == TerminationCondition.optimal):
                            print('Solution is optimal and feasible')
                        elif (self.sim_results.solver.termination_condition == TerminationCondition.infeasible):
                            print("Model is infeasible")
                        else:
                            print ('WARNING. Solver Status: ', self.sim_results.solver)
                except AttributeError:
                    print("You must create SIM instance before you can solve it. Call `model_sim` first.")
        except AttributeError:
            print("You must first calibrate the model. Call `model_calibrate`.")


    def model_compare(self):                       
    
        try:
            if self.base:
                try:
                    if self.sim:
                                        
                        try:
                            if self.base_results:
                                try:
                                    if self.sim_results:
                                        print("#===========HERE ARE THE DIFFERENCES==========#\
                                               #===========note: both models solved==========#")
                                except:
                                        print("#===========HERE ARE THE DIFFERENCES==========#\
                                               #===========note: base model solved===========#\
                                               #===========      sim model unsolved==========#")
                        except:
                            print("#===========HERE ARE THE DIFFERENCES==========#\
                                   #===========note: both models unsolved==========#") 
                        
                     
                        for n in self.sim.component_objects(Var, active=True):  
                            newobject = getattr(self.sim, str(n))
                            for o in self.base.component_objects(Var, active=True):
                                oldobject = getattr(self.base, str(o))
                                if str(n)==str(o):
                                    print(newobject)
                                    for newindex in newobject:
                                        for oldindex in oldobject:
                                            if newindex == oldindex:
                                                diff = oldobject[oldindex].value - newobject[newindex].value
                                                print(newindex, diff)
                        
                        
                        print("\nCalibrated Value of obj = ", value(self.base.obj))
                        print("\nSimulated Value of obj = ", value(self.sim.obj))
                        print("\nDifference of obj = ", value(self.base.obj) - value(self.sim.obj))   

                except AttributeError:
                    print("You have not created a SIM instance")
        except AttributeError:
            print("You have not created a BASE instance")


    def model_postprocess(self, object_name = "" , verbose="", base=True):
        if base == True:
            try:
                if (object_name==""):
                    print("please specify what you would like to output")
                
                elif (object_name=="instance"):
                    print_function(verbose, output=self.base.display, typename="instance")
                
                elif (object_name=="results"):
                    print_function(verbose, output=self.base_results.write, typename = "results")
                
                elif (object_name=="vars") or (object_name=="obj") or (object_name=="pickle"):
                    moment=time.strftime("%Y-%b-%d__%H_%M_%S",time.localtime())
                    if(verbose==""):
                        print("Please enter where to export to")
                    else:
                        directory = verbose
                        if not os.path.exists(directory):
                            print(directory, "directory did not exist so one was created")
                            os.makedirs(directory)
                            
                        check = os.path.abspath(os.path.join(directory, object_name))
                
                        if (object_name=="vars"):
                            print("Vars saved to: \n")
                            for v in self.base.component_objects(Var, active=True):
                                with open(check + str(v) + "_"+  moment + '.csv', 'w') as var_output:
                                    print(str(check + str(v) + "_"+  moment + '.csv'))
                                    varobject = getattr(self.base, str(v))
                                    var_output.write ('{},{} \n'.format('Names', varobject ))
                                    for index in varobject:
                                        var_output.write ('{},{} \n'.format(index, varobject[index].value))
            
                    
                        if(object_name=="obj"): 
                            with open(check + "obj_" + moment + ".csv", 'w') as obj_output:
                                obj_output.write ('{},{}\n'.format("objective", value(self.base.obj)))
                            print("Objective saved to: " + str(check + "obj_" + moment + ".csv"))
                
                        if(object_name=="pickle"):             
                            with open(check + 'saved_results_' + moment, 'wb') as pickle_output:
                                pickle.dump(self.base_results, pickle_output)
                            print("Pickled results object saved to:  " + str(check + 'saved_results_' + moment))
                    
                
                else:
                    print("Please enter a valid object_name" )
                    
            except AttributeError:
                print('Please make sure what you are trying to output has been created (base, base_results,)')
                
        if base == False:
            try:
                if (object_name==""):
                    print("please specify what you would like to output")
                
                elif (object_name=="instance"):
                    print_function(verbose, output=self.sim.display, typename="instance")
                
                elif (object_name=="results"):
                    print_function(verbose, output=self.sim_results.write, typename = "results")
                
                elif (object_name=="vars") or (object_name=="obj") or (object_name=="pickle"):
                    moment=time.strftime("%Y-%b-%d__%H_%M_%S",time.localtime())
                    if(verbose==""):
                        print("Please enter where to export to")
                    else: 
                        directory = verbose
                        if not os.path.exists(directory):
                            print(directory, "directory did not exist so one was created")
                            os.makedirs(directory)
                            
                        check = os.path.abspath(os.path.join(directory, object_name))
                
                        if (object_name=="vars"):
                            print("Vars saved to: \n")
                            for v in self.sim.component_objects(Var, active=True):
                                with open(check + str(v) + "_"+  moment + '.csv', 'w') as var_output:
                                    print(str(check + str(v) + "_"+  moment + '.csv'))
                                    varobject = getattr(self.base, str(v))
                                    var_output.write ('{},{} \n'.format('Names', varobject ))
                                    for index in varobject:
                                        var_output.write ('{},{} \n'.format(index, varobject[index].value))
            
                    
                        if(object_name=="obj"): 
                            with open(check + "obj_" + moment + ".csv", 'w') as obj_output:
                                obj_output.write ('{},{}\n'.format("objective", value(self.sim.obj)))
                            print("Objective saved to: " + str(check + "obj_" + moment + ".csv"))
                
                        if(object_name=="pickle"):             
                            with open(check + 'saved_results_' + moment, 'wb') as pickle_output:
                                pickle.dump(self.sim_results, pickle_output)
                            print("Pickled results object saved to:  " + str(check + 'saved_results_' + moment))
                            
            except AttributeError:
                print('Please make sure what you are trying to output has been created (sim, sim_results,)')
                    



    
    def model_load_results(self, pathname):
        
        if not os.path.exists(pathname):
            print(pathname, " does not exist. Please enter a valid path to the file you would like to load")
        
        else:
            
            try:

                with open(pathname, 'rb') as pkl_file:
                    loadedResults = pickle.load(pkl_file)
                    self.base.solutions.load_from(loadedResults)
                    print("results from: ", pathname, " were loaded to BASE instance")
            
            except:
                
                print("Unable to load file. Please make sure correct file is specified. Must be pickled.")
    
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
        
        check = os.path.abspath(os.path.join(directory, typename))
            
        with open(check + moment, 'w') as output_file:
            output_file.write("\nThis is the " + typename + "\n" )
            output(ostream=output_file)
        print("Output saved to: " + str(check + moment))

def model_welfare(PyCGE):
    # Solve for Hicksian equivalent variations
    print('\n----Welfare Measure----')
    ep0 = (value(PyCGE.base.obj)) /prod((PyCGE.base.alpha[i]/1)**PyCGE.base.alpha[i] for i in PyCGE.base.alpha)
    ep1 = (value(PyCGE.sim.obj)) / prod((PyCGE.base.alpha[i]/1)**PyCGE.base.alpha[i] for i in PyCGE.base.alpha)
    EV = ep1-ep0
    
    print('Hicksian equivalent variations: %.3f' % EV)

