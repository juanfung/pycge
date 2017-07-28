# -*- coding: utf-8 -*-
"""
This is an example script to show some of the basic capabilities of PyCGE.

This examples will compare two policy changes.
Abolishing Tarrifs (to incentivize imports) Vs. Abolishing Production Taxes (to incentivize production)
At the end of the script a welfare measure for each policy will be printed out to help decision makes evaluate the value of each.

"""

import sys
sys.path.insert(0, '../pycge/')
from pycge.examples.stdcge_model_def import StdModelDef
from pycge.PyCGE import PyCGE



# Choose which model to look at, and create a ModelDef object
std_model = StdModelDef()

# Create a PyCGE object and load the ModelDef object into it
testcge = PyCGE(std_model)

# Load the data by passing the path to the directory that contains it
testcge.model_data('../data/stdcge_data_dir')

# Create a `base` instance and pass in a variable and index to fix the numeraire
testcge.model_instance('pf', 'CAP')

# Calibrate the `base` instance
testcge.model_calibrate('minos','neos')

# Create a `sim` instance. This, right now, is exactly the same as the `base` instance
testcge.model_sim()


# Now a copy of the first PyCGE object can be made
# This will save the user having to perform all previous steps again
import copy
copycge = copy.deepcopy(testcge)


# This is the first policy change
# Modify the sim instance to set import tarrifs to 0 for each good
testcge.model_modify_sim('taum','BRD',0)
testcge.model_modify_sim('taum','MLK',0)

# Solve the `sim` instance
testcge.model_solve('minos','neos')

# Compare the equilibrium values between `base` and `sim`
testcge.model_postprocess('compare','print')




# This is the second policy change
# Modify the sim instance to set production taxes to 0 for each good
copycge.model_modify_sim('tauz','BRD',0)
copycge.model_modify_sim('tauz','MLK',0)

# Solve the `sim` instance
copycge.model_solve('minos','neos')

# Compare the equilibrium values between `base` and `sim`
copycge.model_postprocess('compare','print')




# This is an example of how one can use results to perform calculations such as computing EV
def model_welfare(PyCGE):
    # Solve for Hicksian equivalent variations
    print('\n----Welfare Measure----')
    ep0 = (value(PyCGE.base.obj)) /prod((PyCGE.base.alpha[i]/1)**PyCGE.base.alpha[i] for i in PyCGE.base.alpha)
    ep1 = (value(PyCGE.sim.obj)) / prod((PyCGE.base.alpha[i]/1)**PyCGE.base.alpha[i] for i in PyCGE.base.alpha)
    EV = ep1-ep0
    
    print('Hicksian equivalent variations: %.3f' % EV)


# Time to see the value of each policy change
print('----------------------------------------')
print("\nAbolish tarrifs")
model_welfare(testcge)

print("\nAbolish taxes")
model_welfare(copycge)

