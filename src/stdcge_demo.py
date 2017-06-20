# Pyomo port of stdcge.gms from GAMS Model Library


# ------------------------------------------- #
# Import packages
from pyomo.environ import *
import pandas as pd
import numpy as np
import time
import os


# ------------------------------------------- #
# MODEL OBJECT: "Container for problem"
# Create abstract model
model = AbstractModel()


# ------------------------------------------- #
# DEFINE SETS
model.i = Set(doc='goods')
model.h = Set(doc='factor')
model.u = Set(doc='SAM entry')


# ------------------------------------------- #
# DEFINE PARAMETERS
model.sam = Param(model.u, model.u, doc='social accounting matrix')

def Td0_init(model):
    return model.sam['GOV','HOH']


model.Td0 = Param(initialize=Td0_init,
                 doc='direct tax')

def Tz0_init(model, i):
    return model.sam['IDT', i]


model.Tz0 = Param(model.i, initialize=Tz0_init,
                 doc='production tax')

def Tm0_init(model, i):
    return model.sam['TRF', i]

model.Tm0 = Param(model.i, initialize=Tm0_init,
                 doc='import tariff')
#-------------------------------------------------#





def F0_init(model, h, i):
    return model.sam[h,i]


model.F0 = Param(model.h, model.i, initialize=F0_init,
                 doc='the h-th factor input by the j-th firm')

def Y0_init(model, i):
    return sum(model.F0[h, i] for h in model.h)
 

model.Y0 = Param(model.i, initialize=Y0_init,
                 doc='composite factor')

def X0_init(model, i, j):
    return model.sam[i, i]


model.X0 = Param(model.i, model.i, initialize=X0_init,
                 doc='intermediate input')

def Z0_init(model, i):
    return model.Y0 + sum(model.X0[i,i] for i in model.i)


model.Z0 = Param(model.i, initialize=Z0_init,
                 doc='output of the j-th good')

def M0_init(model, i):
    return model.sam['EXT', i]


model.M0 = Param(model.i, initialize=M0_init,
                 doc='imports')
#-------------------------------------------------#




def tauz_init(model, i):
    return model.Tz0/model.Z0


model.tauz = Param(model.i, initialize=tauz_init,
                 doc='production tax rate')

def taum_init(model, i):
    return model.Tm0/model.M0


model.taum = Param(model.i, initialize=taum_init,
                 doc='import tariff rate')


#-------------------------------------------------#
def Xp0_init(model, i):
    return model.sam[i, 'HOH']


model.Xp0 = Param(model.i, initialize=Xp0_init,
                 doc='household consumption of the i-th good')

def FF_init(model, h):
    return model.sam['HOH', h]


model.FF = Param(model.h, initialize=FF_init,
                 doc='factor endowment of the h-th factor')
#-------------------------------------------------#



def Xg0_init(model, i):
    return model.sam[i, 'GOV']


model.Xg0 = Param(model.i, initialize=Xg0_init,
                 doc='government consumption')

def Xv0_init(model, i):
    return model.sam[i, 'INV']


model.Xv0 = Param(model.i, initialize=Xv0_init,
                 doc='investment demand')

def E0_init(model, i):
    return model.sam[i, 'EXT']


model.E0 = Param(model.i, initialize=E0_init,
                 doc='exports')

def Q0_init(model, i):
    return model.Xp0 + model.Xg0 + model.Xv0 + sum(model.X0[i,i] for i in model.i)


model.Q0 = Param(model.i, initialize=Q0_init,
                 doc='Armingtons composite good')

def D0_init(model, i):
    return (1 + model.tauz)*model.Z0-model.E0


model.D0 = Param(model.i, initialize=D0_init,
                 doc='domestic good')

def Sp0_init(model):
    return model.sam['INV', 'HOH']


model.Sp0 = Param(initialize=Sp0_init,
                 doc='private saving')

def Sg0_init(model):
    return model.sam['INV','GOV']


model.Sg0 = Param(initialize=Sg0_init,
                 doc='government saving')

def Sf_init(model):
    return model.sam['INV','EXT']


model.Sf = Param(initialize=Sf_init,
                 doc='foreign saving in US dollars')
#----------------------------------------------------#
def pWe_init():
    return 1


model.pWe = Param(initialize=pWe_init,
                 doc='export price in US dollars')

def pWm_init():
    return 1


model.pWm = Param(initialize=pWm_init,
                 doc='import price in US dollars')






























