# -*- coding: utf-8 -*-
"""
This is an example script to show some of the basic capabilities of PyCGE.

This example shows how easy it is to view and modify parameters. 
"""
import sys
sys.path.insert(0, '../pycge/')
from pycge.examples.splcge_model_def import SplModelDef
from pycge.PyCGE import PyCGE

# Choose which model to look at, and create a ModelDef object
spl_model = SplModelDef()


# Create a PyCGE object and load the ModelDef object into it
testcge = PyCGE(spl_model)


# Load the data by passing the path to the directory that contains it
testcge.model_data('../data/splcge_data_dir')


# Create a `base` instance and pass in a variable and index to fix the numeraire
testcge.model_instance('pf', 'CAP')


# Calibrate the `base` instance
testcge.model_calibrate('minos','neos')


# This allows the user to see all the params, their values, and what their docs
print('#===========original============#')
testcge.model_postprocess('params')

# Modify a parameters
testcge.model_modify_base('X0','MLK',0)

# View the params again, notice X0[MLK] is now set to 0
print('#===========X0[MLK] set to 0============#')
testcge.model_postprocess('params')

# By passing in `undo=True` a user can undo their last change
testcge.model_modify_base('X0','MLK',None,undo=True)

# View all params again. Notice that X0[MLK] was restored to its original value 
print('#===========after the "undo"============#')
testcge.model_postprocess('params')






