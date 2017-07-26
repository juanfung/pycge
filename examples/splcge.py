# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 11:20:51 2017

@author: cmb11
"""
import sys
sys.path.insert(0, '../src/')
from splcge_model_def import SplModelDef
from PyCGE import PyCGE

spl_model = SplModelDef()

testcge = PyCGE(spl_model)

testcge.model_data('../data/splcge_data_dir')

testcge.model_instance('pf', 'CAP')

testcge.model_calibrate('minos','neos')

testcge.model_postprocess('params')

testcge.model_modify_base('X0','MLK',0)

testcge.model_modify_base('X0','BRD',0)

testcge.model_modify_base('X0','MLK',None,undo=True)

testcge.model_postprocess('params')

testcge.model_postprocess('dill_instance', 'saved_instances')





