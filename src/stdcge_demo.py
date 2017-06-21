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
    return model.Y0[i] + sum(model.X0[i,i] for i in model.i)


model.Z0 = Param(model.i, initialize=Z0_init,
                 doc='output of the j-th good')

def M0_init(model, i):
    return model.sam['EXT', i]


model.M0 = Param(model.i, initialize=M0_init,
                 doc='imports')


def tauz_init(model, i):
    return model.Tz0[i]/model.Z0[i]


model.tauz = Param(model.i, initialize=tauz_init,
                 doc='production tax rate')

def taum_init(model, i):
    return model.Tm0[i]/model.M0[i]


model.taum = Param(model.i, initialize=taum_init,
                 doc='import tariff rate')


def Xp0_init(model, i):
    return model.sam[i, 'HOH']


model.Xp0 = Param(model.i, initialize=Xp0_init,
                 doc='household consumption of the i-th good')

def FF_init(model, h):
    return model.sam['HOH', h]


model.FF = Param(model.h, initialize=FF_init,
                 doc='factor endowment of the h-th factor')


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
    return model.Xp0[i] + model.Xg0[i] + model.Xv0[i] + sum(model.X0[i,i] for i in model.i)


model.Q0 = Param(model.i, initialize=Q0_init,
                 doc='Armingtons composite good')

def D0_init(model, i):
    return (1 + model.tauz[i])*model.Z0[i]-model.E0[i]


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

def pWe_init(model):
    return 1


model.pWe = Param(initialize=pWe_init,
                 doc='export price in US dollars')

def pWm_init(model):
    return 1


model.pWm = Param(initialize=pWm_init,
                 doc='import price in US dollars')

# ------------------------------------------- #
# CALIBRATION


def sigma_init(model, i):
    return 2


model.sigma = Param(model.i, initialize=sigma_init,
                    doc='elasticity of substitution')

def psi_init(model, i):
    return 2

model.psi = Param(model.i, initialize=psi_init,
                    doc='elasticity of transformation')

def eta_init(model, i):
    return (model.sigma[i] - 1) / model.sigma[i]

model.eta = Param(model.i, initialize=eta_init,
                    doc='substitution elasticity parameter')

def phi_init(model, i):
    return (model.psi[i] + 1) / model.psi[i]

model.phi = Param(model.i, initialize=phi_init,
                    doc='transformation elasticity parameter')

def alpha_init(model, i):
    return (model.Xp0[i])/ sum(model.Xp0[i] for i in model.i)

model.alpha = Param(model.i, initialize=alpha_init,
                    doc='share parameter in utility func.')
    
def beta_init(model, h, i):
    return (model.F0[h, i]) / sum(model.Xg0[i] for i in model.i)

model.beta = Param(model.h, model.i,  initialize=beta_init,
                    doc='share parameter in production func.')
    
def b_init(model, i):
    return model.Y0[i] / np.prod([model.F0[h, i]**model.beta[h, i] for h in model.h])

model.b = Param(model.i, initialize=b_init,
                    doc='scale parameter in production func.')
    
def ax_init(model, i, j):
    return model.X0[i,j] / model.Z0[j]

model.ax = Param(model.i, model.i, initialize=ax_init,
                    doc='intermediate input requirement coeff.')
    
def ay_init(model,i):
    return model.Y0[i]/model.Z0[i]
    
model.ay = Param(model.i, initialize=ay_init,
                    doc=' composite fact. input req. coeff.')
    
def mu_init(model, i):
    return model.Xg0[i] / sum(model.Xg0[i] for i in model.i)
    
model.mu = Param(model.i, initialize=mu_init,
                    doc=' government consumption share')
    
def lambd_init (model, i):
    return model.Xv0[i] / (model.Sp0 + model.Sg0 + model.Sf)
    
model.lambd = Param(model.i, initialize=lambd_init,
                    doc='investment demand share')
    
def deltam_init(model, i):
    return (1+model.taum[i]*model.M0[i]**(1-model.eta[i])) / ((1+model.taum[i])*model.M0[i]**(1-model.eta[i]) + model.D0[i]**(1-model.eta[i]))
    
model.deltam = Param(model.i, initialize=deltam_init,
                    doc='share par. in Armington func.')
    
def deltad_init(model, i):
    return model.D0[i]**(1-model.eta[i]) / ((1+model.taum[i])*model.M0[i]**(1-model.eta[i]) + model.D0[i]**(1-model.eta[i]))
    
model.deltad = Param(model.i, initialize=deltad_init,
                    doc='share par. in Armington func.')
    
def gamma_init(model, i):
    return model.Q0[i] / (model.deltam[i]*model.M0[i]**model.eta[i]+model.deltad[i]*model.D0[i]**model.eta[i])**(1/model.eta[i])
       
model.gamma = Param(model.i, initialize=gamma_init,
                    doc='scale par. in Armington func.')
     
def  xid_init(model, i):
    return model.D0[i]**(1-model.phi[i])/(model.E0[i]**(1-model.phi[i])+model.D0[i]**(1-model.phi[i]))
    
model.xid = Param(model.i, initialize=xid_init,
                    doc='share par. in transformation func.')
    
def xie_init(model, i):
    return model.E0[i]**(1-model.phi[i])/(model.E0[i]**(1-model.phi[i])+model.D0[i]**(1-model.phi[i]))
 
model.xie = Param(model.i, initialize=xie_init,
                    doc='share par. in transformation func.')
       
def theta_init(model, i):
    return model.Z0[i] / (model.xie[i]*model.E0[i]**model.phi[i]+model.xid[i]*model.D0[i]**model.phi[i]**(1/model.phi[i]))
   
model.theta = Param(model.i, initialize=theta_init,
                    doc='scale par. in transformation func.')
     
def ssp_init(model):
    return model.Sp0/sum(model.FF[h] for h in model.h)
    
model.ssp = Param(initialize=ssp_init,
                    doc='average propensity for private saving')
    
def ssg_init(model):
    return model.Sg0/(model.Td0+sum(model.Tz0[i] for i in model.i)+sum(model.Tm0[i] for i in model.i))
    
model.ssg = Param(initialize=ssg_init,
                    doc='average propensity for gov. saving')
    
def taud_init(model):
    return model.Td0/sum(model.FF[h] for h in model.h)
        
model.taud = Param(initialize=taud_init,
                    doc='direct tax rate')
   
# ------------------------------------------- #
# Define model system
# DEFINE VARIABLES

model.Y = Var(model.i,
              initialize=Y0_init,
              within=PositiveReals,
              doc='composite factor')

model.F = Var(model.h, model.i,
              initialize=F0_init,
              within=PositiveReals,
              doc='the h-th factor input by the j-th firm')

model.X = Var(model.i, model.i,
              initialize=X0_init,
              within=PositiveReals,
              doc='intermediate input')

model.Z = Var(model.i,
              initialize=Z0_init,
              within=PositiveReals,
              doc='output of the j-th good')

model.Xp = Var(model.i,
              initialize=Xp0_init,
              within=PositiveReals,
              doc=' household consumption of the i-th good')

model.Xg = Var(model.i,
              initialize=Xg0_init,
              within=PositiveReals,
              doc='government consumption')

model.Xv = Var(model.i,
              initialize=Xv0_init,
              within=PositiveReals,
              doc=' investment demand')

model.E = Var(model.i,
              initialize=E0_init,
              within=PositiveReals,
              doc=' exports')

model.M = Var(model.i,
              initialize=M0_init,
              within=PositiveReals,
              doc='imports')

model.Q = Var(model.i,
              initialize=Q0_init,
              within=PositiveReals,
              doc='Armingtons composite good')

model.D = Var(model.i,
              initialize=D0_init,
              within=PositiveReals,
              doc='domestic good')


def p_init(model, v):
    return 1



model.pf = Var(model.h,
              initialize=p_init,
              within=PositiveReals,
              doc='the h-th factor price')

model.py = Var(model.i,
              initialize=p_init,
              within=PositiveReals,
              doc='composite factor price')

model.pz = Var(model.i,
              initialize=p_init,
              within=PositiveReals,
              doc=' supply price of the i-th good')

model.pq = Var(model.i,
              initialize=p_init,
              within=PositiveReals,
              doc='Armingtons composite good price')

model.pe = Var(model.i,
              initialize=p_init,
              within=PositiveReals,
              doc='export price in local currency')

model.pm = Var(model.i,
              initialize=p_init,
              within=PositiveReals,
              doc='import price in local currency')

model.pd = Var(model.i,
              initialize=p_init,
              within=PositiveReals,
              doc='the i-th domestic good price')

model.epsilon = Var(
              initialize= 1,
              within=PositiveReals,
              doc='exchange rate')


model.Sp = Var(
              initialize=Sp0_init,
              within=PositiveReals,
              doc='private saving')

model.Sg = Var(
              initialize=Sg0_init,
              within=PositiveReals,
              doc='government saving')

model.Td = Var(
              initialize=Td0_init,
              within=PositiveReals,
              doc='direct tax')

model.Tz = Var(model.i,
              initialize=Tz0_init,
              within=PositiveReals,
              doc='production tax')

model.Tm = Var(model.i,
              initialize=Tm0_init,
              within=PositiveReals,
              doc='import tariff')

# ------------------------------------------- #
# DEFINE EQUATIONS

def eqpy_rule(model, i):
    return (model.Y[i] == model.b[i]*np.prod([model.F[h, i]**model.beta[h, i] for h in model.h]))

model.eqpy = Constraint(model.i, rule=eqpy_rule, doc='composite factor agg. func.')

def eqF_rule(model, h, i):
    return (model.F[h,i] == model.beta[h,i]*model.py[i]*model.Y[i]/model.pf[h])

model.eqF = Constraint(model.h, model.i, rule=eqF_rule, doc='factor demand function')

def eqX_rule(model, i, j):
    return (model.X[i,j] ==model.ax[i,j]*model.Z[i] )

model.eqX = Constraint(model.i, model.i, rule=eqX_rule, doc='intermediate demand function')

def eqY_rule(model, i):
    return (model.Y[i] == model.ay[i]*model.Z[i])

model.eqY = Constraint(model.i, rule=eqY_rule, doc='composite factor demand function')

def eqpzs_rule(model, i):
    return (model.pz[i] == model.ay[i]*model.py[i] +sum(model.ax[i,i]*model.pq[i] for i in model.i) )

model.eqpzs = Constraint(model.i, rule=eqpzs_rule, doc='unit cost function')

def eqTd_rule(model):
    return (model.Td == model.taud*sum(model.pf[h]*model.FF[h] for h in model.h) )

model.eqTd = Constraint(rule=eqTd_rule, doc='direct tax revenue function')

def eqTz_rule(model, i):
    return (model.Tz[i] == model.tauz[i]*model.pz[i]*model.Z[i])

model.eqTz = Constraint(model.i, rule=eqTz_rule, doc='production tax revenue function')

def eqTm_rule(model, i):
    return (model.Tm[i] == model.taum[i]*model.pm[i]*model.M[i])

model.eqTm = Constraint(model.i, rule=eqTm_rule, doc='import tariff revenue function')

def eqXg_rule(model, i):
    return (model.Xg[i] == model.mu[i]*(model.Td +sum(model.Tz[i] for i in model.i) +sum(model.Tm[i] for i in model.i)- model.Sg)  /model.pq[i])

model.eqXg = Constraint(model.i, rule=eqXg_rule, doc='government demand function')

def eqXv_rule(model, i):
    return (model.Xv[i] == model.lambd[i]*(model.Sp +model.Sg +model.epsilon*model.Sf)/model.pq[i])

model.eqXv = Constraint(model.i, rule=eqXv_rule, doc='investment demand function')

def eqSp_rule(model):
    return (model.Sp == model.ssp*sum(model.pf[h]*model.FF[h] for h in model.h) )

model.eqSp = Constraint(rule=eqSp_rule, doc='private saving function')

def eqSg_rule(model):
    return (model.Sg == model.ssg*(model.Td +sum(model.Tz[i] for i in model.i)+sum(model.Tm[i] for i in model.i)))

model.eqSg = Constraint(rule=eqSg_rule, doc='government saving function')

def eqXp_rule(model, i):
    return (model.Xp[i] == model.alpha[i]*(sum(model.pf[h]*model.FF[h] for h in model.h) - model.Sp - model.Td) / model.pq[i])

model.eqXp = Constraint(model.i, rule=eqXp_rule, doc='household demand function')

def eqpe_rule(model, i):
    return (model.pe[i] == (model.epsilon * model.pWe))

model.eqpe = Constraint(model.i, rule=eqpe_rule, doc='world export price equation')

def eqpm_rule(model, i):
    return (model.pm[i] == model.epsilon*model.pWm)

model.eqpm = Constraint(model.i, rule=eqpm_rule, doc='world import price equation')

def eqepsilon_rule(model):
    return (sum(model.pWe*model.E[i] for i in model.i)) + model.Sf == sum(model.pWm*model.M[i] for i in model.i)

model.eqepsilon = Constraint(rule=eqepsilon_rule, doc='balance of payments')

def eqpqs_rule(model, i):
    return (model.Q[i] == model.gamma[i]*(model.deltam[i]*model.M[i]**model.eta[i]+model.deltad[i]*model.D[i]**model.eta[i])**(1/model.eta[i]))

model.eqpqs = Constraint(model.i, rule=eqpqs_rule, doc='Armington function')

def eqM_rule(model, i):
    return ( model.M[i]== (model.gamma[i]**model.eta[i]*model.deltam[i]*model.pq[i]/((1+model.taum[i])*model.pm[i]))**(1/(1-model.eta[i]))*model.Q[i])

model.eqM = Constraint(model.i, rule=eqM_rule, doc='import demand function')

def eqD_rule(model, i):
    return ( model.D[i]== (model.gamma[i]**model.eta[i]*model.deltad[i]*model.pq[i]/model.pd[i])**(1/(1-model.eta[i]))*model.Q[i])

model.eqD = Constraint(model.i, rule=eqD_rule, doc='domestic good demand function')

def eqpzd_rule(model, i):
    return ( model.Z[i] == model.theta[i]*(model.xie[i]*model.E[i]**model.phi[i]+model.xid[i]*model.D[i]**model.phi[i])**(1/model.phi[i]))

model.eqpzd = Constraint(model.i, rule=eqpzd_rule, doc='transformation function') 

def eqDs_rule(model, i):
    return ( model.E[i]== (model.theta[i]**model.phi[i]*model.xie[i]*(1+model.tauz[i])*model.pz[i]/model.pe[i])**(1/(1-model.phi[i]))*model.Z[i])

model.eqDs = Constraint(model.i, rule=eqDs_rule, doc='domestic good supply function')

def eqE_rule(model, i):
    return ( model.D[i]== (model.theta[i]**model.phi[i]*model.xid[i]*(1+model.tauz[i])*model.pz[i]/model.pd[i])**(1/(1-model.phi[i]))*model.Z[i])

model.eqE = Constraint(model.i, rule=eqE_rule, doc='export supply function')

def eqpqd_rule(model, i):
    return ( model.Q[i]==  model.Xp[i] + model.Xg[i] + model.Xv[i] +sum(model.X[i,i] for i in model.i))

model.eqpqd = Constraint(model.i, rule=eqpqd_rule, doc='market clearing cond. for comp. good')

def eqpf_rule(model, h):
    return (sum(model.F[h,i] for i in model.i) == model.FF[h])

model.eqpf = Constraint(model.h, rule=eqpf_rule, doc='factor market clearing condition')


# ------------------------------------------- #
# DEFINE OBJECTIVE
def obj_rule(model):
    return np.prod([model.Xp[i]**model.alpha[i] for i in model.i])

model.obj = Objective(rule=obj_rule, sense=maximize,
                      doc='utility function [fictitious]')

# CREATE MODEL INSTANCE
data = DataPortal()
data.load(filename='./stdcge_data_directory/set-i-.csv', format='set', set='i')
data.load(filename='./stdcge_data_directory/set-h-.csv', format='set', set='h')
data.load(filename='./stdcge_data_directory/set-u-.csv', format='set', set='u')
data.load(filename='./stdcge_data_directory/param-sam-.csv', param='sam', format='array')

instance = model.create_instance(data)
instance.pf['LAB'].fixed = True
instance.display()


# ------------------------------------------- #
# SOLVE
# Using NEOS external solver

# Select solver
solver = 'minos'  # 'ipopt', 'knitro', 'minos'
solver_io = 'nl'

# To run as python script:
# This is an optional code path that allows the script to be run outside of
# pyomo command-line.  For example:  python splcge_demo.py

if __name__ == '__main__':
    #This replicates what the pyomo command-line tools does
    from pyomo.opt import SolverFactory
    from pyomo.opt import SolverResults
    import pyomo.environ
    import pickle
    #opt = SolverFactory(solver)
    #opt.options['max_iter'] = 20
    with SolverManagerFactory("neos") as solver_mgr:
        results = solver_mgr.solve(instance, opt=solver, tee=True)
        

    instance.solutions.store_to(results)
    
    results.write()






























