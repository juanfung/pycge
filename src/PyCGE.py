# Import packages
from pyomo.environ import *
import pandas as pd
import numpy as np
import dill
from pyomo.opt import SolverResults
import time
import os
from pyomo.opt import SolverStatus, TerminationCondition
import importlib
import copy




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
        
        if not data_dir.endswith("/") and data_dir != "": #if the user forgot the slash at the end
            data_dir = data_dir + "/" #add one
        
        if (data_dir == ""): #if the user didnt enter a directory
            print("Please specify where you would like to load data from")
        

        
        elif not os.path.exists(data_dir): #if the directory does not exist
            print("please enter a valid data directory")
        
        else:
        
            data = DataPortal() #create data portal
            
            for filenames in os.listdir(data_dir): #go through files in directory
                if filenames.startswith("set"):                
    
                    dat_type,names,file_type = filenames.split('-') #break up the name (for example: set,i,csv)
                    data.load(filename = data_dir + filenames, format = 'set', set = names)  #load data              
                    print("File '" + filenames + "' was loaded into set: " + names) 
                    
                elif filenames.startswith("param"):
                    
                    dat_type,names,file_type = filenames.split('-') #break up the name (for example: param,sam,csv)
                    print("File '" + filenames + "' was loaded into param: " + names)            
    
                    data.load(filename = data_dir + filenames, param = names, format='array') #load data
                
                else: #if it doesn't start with "set" or "param"
                    print(filenames, " is not in the right format and was not loaded into DataPortal") 
                    
            self.data = data


    def model_instance(self, NAME, INDEX):
        
        try:
            if self.m: #if the model is loaded
                try:
                    if self.data: #if the data is loaded
        
                        self.base = self.m.create_instance(self.data) #create instance
                        test = False #create a flag to check if the NAME was ever found
                        for v in self.base.component_objects(Var, active=True): #go through variables
                            if str(v)==NAME: #find the variable the user entered
                                test = True #NAME was found
                                varobject = getattr(self.base, str(v)) #from that variable
                                try:
                                    varobject[INDEX].fixed = True #fix the index the user entered
                                    print("Note, ", NAME, INDEX, " is now fixed")
                                    print("BASE instance created. Call `model_postprocess` to output or `model_calibrate` to solve.")
                                except:
                                    print("index", INDEX, "does not exist for", NAME)
                        if test == False: #NAME was never found
                            print("variable", NAME, "does not exist")
                except:
                    print("data not loaded")
        
        except:
            print("model not loaded")
              

    def model_sim (self):
        
        try:
            
            if self.base: #if the base instance has been created
                
                try:
                
                    if self.base_results: #if the base instance has been calibrated
            
                        self.sim = copy.deepcopy(self.base) #create self.sim which is exactly the same as the self.base
                        
                        print("SIM instance created. Note, this is currently the same as BASE. Call `model_modify_instance` to modify.")
                        
                except AttributeError:
                    print("You must calibrate first")
        
        except AttributeError:
            print("You must create BASE instance first.")
        
    
    def model_modify_instance(self,NAME,INDEX,VALUE,fix=True):

        try:
            if self.sim: #if the sim instance has been created
                try: #make sure the component they are trying to access exists
                    _object = getattr(self.sim, NAME) #get the attribute the user entered
                    try:
                        print(_object[INDEX], "was originally", _object[INDEX].value)
                        _object[INDEX].value = VALUE #set the value to what the user entered
                        print(_object[INDEX], " is now set to ", _object[INDEX].value)
                        
                        for v in self.sim.component_objects(Var, active=True): #go through variabled
                            if str(v)==NAME: #if the component they entered was a variable
                                varobject = getattr(self.sim, str(v)) #get the entered variable
                                if fix == True:
                                    varobject[INDEX].fixed = True #fix it (default)
                                    print("Note, ", _object[INDEX], " is now fixed")
                                if fix == False:
                                    varobject[INDEX].fixed = False
                                    print("Note, ", _object[INDEX], " is NOT fixed")
    
    
                        print("SIM updated. Call `model_postprocess` to output or `model_solve` to solve.")
                    except AttributeError: #if INDEX does not exist
                        print(INDEX, "is not an index of", NAME)
                    except Exception as e: #if something else went wrong 
                        print(e)                    
                except AttributeError:
                    print(NAME, "does not exist in current instance")



        except AttributeError: #if sim instance does not exist
            print("Must first create sim instance. Call `model_sim`.")
    


    def model_calibrate(self, mgr, solver):
        
        
        try:
            if self.base: #if base instance has already been created
                try:
                    if self.base_results: #if base has already been calibrated
                        print('Model already calibrated. If a SIM has been created, call `model_solve` to solve it.')
                except AttributeError: #if the base has NOT already been calibrated
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
        except AttributeError: #if the user has not created the base instance yet
            print('You must create the BASE instance before you can solve it. Call `model_instance` first.')



    def model_solve(self, mgr, solver):

        try:
            if self.base_results: #if the base has already been calibrated
                try:
                    if self.sim: #if the sim instance has already been created
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
                except AttributeError: #if sim instance has not been created
                    print("You must create SIM instance before you can solve it. Call `model_sim` first.")
        except AttributeError: #if base has not been calibrated
            print("You must first calibrate the model. Call `model_calibrate`.")


    def model_compare(self):                       
    
        try:
            if self.base: #if base instance has been created
                try:
                    if self.sim: #if sim instance has been created
                                        
                        try:
                            if self.base_results: #if base has been solved
                                try:
                                    if self.sim_results: #if sim has been solved
                                        print("#===========HERE ARE THE DIFFERENCES==========#\
                                               #===========note: both models solved==========#")
                                except:
                                        print("#===========HERE ARE THE DIFFERENCES==========#\
                                               #===========note: base model solved===========#\
                                               #===========      sim model unsolved==========#")
                        except:
                            print("#===========HERE ARE THE DIFFERENCES==========#\
                                   #===========note: both models unsolved==========#") 
                        
                     
                        for n in self.sim.component_objects(Var, active=True):  #go through sim components
                            newobject = getattr(self.sim, str(n)) #get sim object
                            for o in self.base.component_objects(Var, active=True): #go through base components
                                oldobject = getattr(self.base, str(o)) #get base object
                                if str(n)==str(o): #if they are the same object (for example X == X)
                                    print(newobject) # print it
                                    for newindex in newobject: #go through sim indexes
                                        for oldindex in oldobject: #go through base indexes
                                            if newindex == oldindex: #if they are the same index (for example 'BRD' == 'BRD')
                                                diff = oldobject[oldindex].value - newobject[newindex].value #calculate the difference between the two
                                                if newobject[newindex].value != 0: #if the sim value does not equal 0 (to avoid division by 0)
                                                
                                                    per = (oldobject[oldindex].value / newobject[newindex].value) * 100 #caluculate percentage
                                                    print(newindex, "Difference = %.4f" % diff, "     Percentage = %.4f" % per) 
                                                else: #if it DOES equal zero
                                                    print(newindex, "Difference = %.4f" % diff, "     Note: ", newindex, "now = 0" )
                        
                        
                        print("\nCalibrated Value of obj = ", value(self.base.obj))
                        print("\nSimulated Value of obj = ", value(self.sim.obj))
                        print("\nDifference of obj = ", value(self.base.obj) - value(self.sim.obj))   

                except AttributeError:
                    print("You have not created a SIM instance")
        except AttributeError:
            print("You have not created a BASE instance")


    def model_postprocess(self, object_name = "" , verbose="", base=True):
        if base == True: # if you want to post process things from the base
            try:
                if (object_name==""): #make sure user enters something
                    print("please specify what you would like to output")
                
                elif (object_name=="instance"):
                    print_function(verbose, output=self.base.display, typename="instance") #call print funtion passing it the neccesary arguments
                
                elif (object_name=="results"):
                    print_function(verbose, output=self.base_results.write, typename = "results")#call print funtion passing it the neccesary arguments
                
                elif (object_name=="vars") or (object_name=="obj") or (object_name=="dill_instance"):
                    moment=time.strftime("%Y-%b-%d__%H_%M_%S",time.localtime()) #create moment
                    if(verbose==""):
                        print("Please enter where to export to")
                    else:
                        directory = verbose
                        if not os.path.exists(directory):
                            print(directory, "directory did not exist so one was created")
                            os.makedirs(directory)
                            
                        check = os.path.abspath(os.path.join(directory, object_name)) #creates a directory whether the user ends the path with a '/' or not
                
                        if (object_name=="vars"):
                            print("Vars saved to: \n") #let user know where they were saved to (pt. 1)
                            for v in self.base.component_objects(Var, active=True): #go through components
                                with open(check + str(v) + "_"+  moment + '.csv', 'w') as var_output: #create a file
                                    print(str(check + str(v) + "_"+  moment + '.csv'))#let user know where they were saved to (pt. 2)
                                    varobject = getattr(self.base, str(v)) #get attributes for variable
                                    var_output.write ('{},{} \n'.format('Names', varobject )) #write the headers for the file
                                    for index in varobject: #go through indexes
                                        var_output.write ('{},{} \n'.format(index, varobject[index].value))#write index and value for each var
            
                    
                        if(object_name=="obj"): 
                            with open(check + "obj_" + moment + ".csv", 'w') as obj_output: #create file
                                obj_output.write ('{},{}\n'.format("objective", value(self.base.obj)))
                            print("Objective saved to: " + str(check + "obj_" + moment + ".csv"))#let the user know where it was saved
                
                        if(object_name=="dill_instance"):
                            try:
                                if self.base_results:
                                    
                                    with open(check + '_base_' + moment, 'wb') as dill_output: #create file
                                        dill.dump(self.base, dill_output) #save results as a dill file
                                    print("Base instance saved to:  " + str(check + '_base_' + moment))#let user know where it was saved
                            except AttributeError:
                                print('You must calibrate base instance first')
                    
                
                else:
                    print("Please enter a valid object_name" )
                    
            except AttributeError:
                print('Please make sure what you are trying to output has been created (base, base_results,)')
                
        if base == False: # if you want to post process things from the sim (everything else is the same)
            try:
                if (object_name==""):
                    print("please specify what you would like to output")
                
                elif (object_name=="instance"):
                    print_function(verbose, output=self.sim.display, typename="instance")
                
                elif (object_name=="results"):
                    print_function(verbose, output=self.sim_results.write, typename = "results")
                
                elif (object_name=="vars") or (object_name=="obj") or (object_name=="dill_instance"):
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
                
                        if(object_name=="dill_instance"):
                            try:
                                if self.sim_results:
                                    
                                    with open(check + 'sim_' + moment, 'wb') as dill_output:
                                        dill.dump(self.sim, dill_output)
                                    print("Sim instance saved to:  " + str(check + '_sim_' + moment))
                            except AttributeError:
                                print('You must solve sim instance first')
                            
            except AttributeError:
                print('Please make sure what you are trying to output has been created (sim, sim_results,)')
                    



    
    def model_load_results(self, pathname, base=True):
        
        if not os.path.exists(pathname): #if the path does not exist
            print(pathname, " does not exist. Please enter a valid path to the file you would like to load")
        
        else: #if the path does exist
        
            with open(pathname, 'rb') as dill_file: #open it                    
                if base==True: #if you want to load the results to the base instance
                
                    self.base = dill.load(dill_file) #load it
                    print("base instance loaded") 

                else:

                    self.sim = dill.load(dill_file)
                    print("sim instance loaded")
                     

                
                

            

    
def print_function (verbose="", output = "", typename=""): #this is called from the `model_postprocess` function
    
    if (verbose==""):
        print("Please specify how you would like to output")            
    elif (verbose=="print"):
        print("\nThis is the " + typename + "\n") #either instance or results
        output() #either `self.base_results.write()` or `self.base.display()`
        print("Output printed")            
    else:            
        moment=time.strftime("%Y-%b-%d__%H_%M_%S",time.localtime()) #create moment
        directory = (verbose) #not really useful other, but makes more sense later on
        if not os.path.exists(directory): #if it doesnt exist
            print(verbose, "directory did not exist so one was created")
            os.makedirs(directory)
        
        check = os.path.abspath(os.path.join(directory, typename)) #makes sure directory ends in '/'
            
        with open(check + moment, 'w') as output_file:
            output_file.write("\nThis is the " + typename + "\n" ) #write header for file
            output(ostream=output_file) #write to file
        print("Output saved to: " + str(check + moment)) #let the user know where it is saved

def model_welfare(PyCGE):
    # Solve for Hicksian equivalent variations
    print('\n----Welfare Measure----')
    ep0 = (value(PyCGE.base.obj)) /prod((PyCGE.base.alpha[i]/1)**PyCGE.base.alpha[i] for i in PyCGE.base.alpha)
    ep1 = (value(PyCGE.sim.obj)) / prod((PyCGE.base.alpha[i]/1)**PyCGE.base.alpha[i] for i in PyCGE.base.alpha)
    EV = ep1-ep0
    
    print('Hicksian equivalent variations: %.3f' % EV)

