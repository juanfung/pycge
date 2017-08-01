# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 10:42:04 2017

@author: cmb11
"""
# Pyomo port of stdcge.gms from GAMS Model Library


# ------------------------------------------- #
# Import packages
from pyomo.environ import *

import numpy as np



class StdModelDef:
    
    
    def model(self):
                
        # ------------------------------------------- #
        # MODEL OBJECT: "Container for problem"
        # Create abstract model
        self.m = AbstractModel()
        
         
        # ------------------------------------------- #
        # DEFINE SETS
        self.m.i = Set(doc='goods')
        self.m.h = Set(doc='factor')
        self.m.u = Set(doc='SAM entry')
        
        
        # ------------------------------------------- #
        # DEFINE PARAMETERS
        self.m.sam = Param(self.m.u, self.m.u, doc='social accounting matrix')
        
        
        def Td0_init(model):
            return model.sam['GOV','HOH']
        
        
        self.m.Td0 = Param(initialize=Td0_init,
                         doc='direct tax', mutable = True)
        
        def Tz0_init(model, i):
            return model.sam['IDT', i]
        
        
        self.m.Tz0 = Param(self.m.i, initialize=Tz0_init,
                         doc='production tax', mutable = True)
        
        def Tm0_init(model, i):
            return model.sam['TRF', i]
        
        self.m.Tm0 = Param(self.m.i, initialize=Tm0_init,
                         doc='import tariff', mutable = True)
        
        
        def F0_init(model, h, i):
            return model.sam[h,i]
        
        
        self.m.F0 = Param(self.m.h, self.m.i, initialize=F0_init,
                         doc='the h-th factor input by the j-th firm', mutable = True)
        
        def Y0_init(model, i):
            return sum(model.F0[h, i] for h in model.h)
         
        
        self.m.Y0 = Param(self.m.i, initialize=Y0_init,
                         doc='composite factor', mutable = True)
        
        def X0_init(model, i, j):
            return model.sam[i, j]
        
        
        self.m.X0 = Param(self.m.i, self.m.i, initialize=X0_init,
                         doc='intermediate input', mutable = True)
        
        def Z0_init(model, j):
            return model.Y0[j] + sum(model.X0[i,j] for i in model.i)
        
        
        self.m.Z0 = Param(self.m.i, initialize=Z0_init,
                         doc='output of the j-th good', mutable = True)
        
        def M0_init(model, i):
            return model.sam['EXT', i]
        
        
        self.m.M0 = Param(self.m.i, initialize=M0_init,
                         doc='imports', mutable = True)
        
        
        def tauz_init(model, i):
            return model.Tz0[i]/model.Z0[i]
        
        
        self.m.tauz = Param(self.m.i, initialize=tauz_init,
                         doc='production tax rate', mutable = True)
        
        def taum_init(model, i):
            return model.Tm0[i]/model.M0[i]
        
        
        self.m.taum = Param(self.m.i, initialize=taum_init,
                         doc='import tariff rate', mutable = True)
        
        
        def Xp0_init(model, i):
            return model.sam[i, 'HOH']
        
        
        self.m.Xp0 = Param(self.m.i, initialize=Xp0_init,
                         doc='household consumption of the i-th good', mutable = True)
        
        def FF_init(model, h):
            return model.sam['HOH', h]
        
        
        self.m.FF = Param(self.m.h, initialize=FF_init,
                         doc='factor endowment of the h-th factor', mutable = True)
        
        
        def Xg0_init(model, i):
            return model.sam[i, 'GOV']
        
        
        self.m.Xg0 = Param(self.m.i, initialize=Xg0_init,
                         doc='government consumption', mutable = True)
        
        def Xv0_init(model, i):
            return model.sam[i, 'INV']
        
        
        self.m.Xv0 = Param(self.m.i, initialize=Xv0_init,
                         doc='investment demand', mutable = True)
        
        def E0_init(model, i):
            return model.sam[i, 'EXT']
        
        
        self.m.E0 = Param(self.m.i, initialize=E0_init,
                         doc='exports', mutable = True)
        
        def Q0_init(model, i):
            return model.Xp0[i] + model.Xg0[i] + model.Xv0[i] + sum(model.X0[i,j] for j in model.i)
        
        
        self.m.Q0 = Param(self.m.i, initialize=Q0_init,
                         doc='Armingtons composite good', mutable = True)
        
        def D0_init(model, i):
            return (1 + model.tauz[i])*model.Z0[i]-model.E0[i]
        
        
        self.m.D0 = Param(self.m.i, initialize=D0_init,
                         doc='domestic good', mutable = True)
        
        def Sp0_init(model):
            return model.sam['INV', 'HOH']
        
        
        self.m.Sp0 = Param(initialize=Sp0_init,
                         doc='private saving', mutable = True)
        
        def Sg0_init(model):
            return model.sam['INV','GOV']
        
        
        self.m.Sg0 = Param(initialize=Sg0_init,
                         doc='government saving', mutable = True)
        
        def Sf_init(model):
            return model.sam['INV','EXT']
        
        
        self.m.Sf = Param(initialize=Sf_init,
                         doc='foreign saving in US dollars', mutable = True)
        
        def pWe_init(model, i):
            return 1
        
        
        self.m.pWe = Param(self.m.i, initialize=pWe_init,
                         doc='export price in US dollars', mutable = True)
        
        def pWm_init(model, i):
            return 1
        
        
        self.m.pWm = Param(self.m.i, initialize=pWm_init,
                         doc='import price in US dollars', mutable = True)
        
        # ------------------------------------------- #
        # CALIBRATION
        
        
        def sigma_init(model, i):
            return 2
        
        
        self.m.sigma = Param(self.m.i, initialize=sigma_init,
                            doc='elasticity of substitution')
        
        def psi_init(model, i):
            return 2
        
        self.m.psi = Param(self.m.i, initialize=psi_init,
                            doc='elasticity of transformation')
        
        def eta_init(model, i):
            return (model.sigma[i] - 1) / model.sigma[i]
        
        self.m.eta = Param(self.m.i, initialize=eta_init,
                            doc='substitution elasticity parameter')
        
        def phi_init(model, i):
            return (model.psi[i] + 1) / model.psi[i]
        
        self.m.phi = Param(self.m.i, initialize=phi_init,
                            doc='transformation elasticity parameter')
        
        def alpha_init(model, i):
            return (model.Xp0[i])/ sum(model.Xp0[j] for j in model.i)
        
        self.m.alpha = Param(self.m.i, initialize=alpha_init,
                            doc='share parameter in utility func.')
            
        def beta_init(model, h, i):
            return (model.F0[h, i]) / sum(model.F0[k,i] for k in model.h)
        
        self.m.beta = Param(self.m.h, self.m.i,  initialize=beta_init,
                            doc='share parameter in production func.')
            
        def b_init(model, i):
            return model.Y0[i] / np.prod([model.F0[h, i]**model.beta[h, i] for h in model.h])
        
        self.m.b = Param(self.m.i, initialize=b_init,
                            doc='scale parameter in production func.')
            
        def ax_init(model, i, j):
            return model.X0[i,j] / model.Z0[j]
        
        self.m.ax = Param(self.m.i, self.m.i, initialize=ax_init,
                            doc='intermediate input requirement coeff.')
            
        def ay_init(model,i):
            return model.Y0[i]/model.Z0[i]
            
        self.m.ay = Param(self.m.i, initialize=ay_init,
                            doc=' composite fact. input req. coeff.')
            
        def mu_init(model, i):
            return model.Xg0[i] / sum(model.Xg0[j] for j in model.i)
            
        self.m.mu = Param(self.m.i, initialize=mu_init,
                            doc=' government consumption share')
            
        def lambd_init (model, i):
            return model.Xv0[i] / (model.Sp0 + model.Sg0 + model.Sf)
            
        self.m.lambd = Param(self.m.i, initialize=lambd_init,
                            doc='investment demand share')
        
        def deltam_init(model, i):
            return (1+model.taum[i])*model.M0[i]**(1-model.eta[i]) / ((1+model.taum[i])*model.M0[i]**(1-model.eta[i]) + model.D0[i]**(1-model.eta[i]))
            
        self.m.deltam = Param(self.m.i, initialize=deltam_init,
                            doc='share par. in Armington func.')
            
        def deltad_init(model, i):
            return model.D0[i]**(1-model.eta[i]) / ((1+model.taum[i])*model.M0[i]**(1-model.eta[i]) + model.D0[i]**(1-model.eta[i]))
            
        self.m.deltad = Param(self.m.i, initialize=deltad_init,
                            doc='share par. in Armington func.')
            
        def gamma_init(model, i):
            return model.Q0[i] / (model.deltam[i]*model.M0[i]**model.eta[i]+model.deltad[i]*model.D0[i]**model.eta[i])**(1/model.eta[i])
               
        self.m.gamma = Param(self.m.i, initialize=gamma_init,
                            doc='scale par. in Armington func.')
            
        def xie_init(model, i):
            return model.E0[i]**(1-model.phi[i])/(model.E0[i]**(1-model.phi[i])+model.D0[i]**(1-model.phi[i]))
         
        self.m.xie = Param(self.m.i, initialize=xie_init,
                            doc='share par. in transformation func.')
        
        def  xid_init(model, i):
            return model.D0[i]**(1-model.phi[i])/(model.E0[i]**(1-model.phi[i])+model.D0[i]**(1-model.phi[i]))
            
        self.m.xid = Param(self.m.i, initialize=xid_init,
                            doc='share par. in transformation func.')
        
        def theta_init(model, i):
            return model.Z0[i] / (model.xie[i]*model.E0[i]**model.phi[i]+model.xid[i]*model.D0[i]**model.phi[i])**(1/model.phi[i])
           
        self.m.theta = Param(self.m.i, initialize=theta_init,
                            doc='scale par. in transformation func.')
             
        def ssp_init(model):
            return model.Sp0/sum(model.FF[h] for h in model.h)
            
        self.m.ssp = Param(initialize=ssp_init,
                            doc='average propensity for private saving')
            
        def ssg_init(model):
            return model.Sg0/(model.Td0+sum(model.Tz0[i] for i in model.i)+sum(model.Tm0[i] for i in model.i))
            
        self.m.ssg = Param(initialize=ssg_init,
                            doc='average propensity for gov. saving')
            
        def taud_init(model):
            return model.Td0/sum(model.FF[h] for h in model.h)
                
        self.m.taud = Param(initialize=taud_init,
                            doc='direct tax rate')
           
        # ------------------------------------------- #
        # Define model system
        # DEFINE VARIABLES
        
        self.m.Y = Var(self.m.i,
                      initialize=Y0_init,
                      within=PositiveReals,
                      doc='composite factor')
        
        self.m.F = Var(self.m.h, self.m.i,
                      initialize=F0_init,
                      within=PositiveReals,
                      doc='the h-th factor input by the j-th firm')
        
        self.m.X = Var(self.m.i, self.m.i,
                      initialize=X0_init,
                      within=PositiveReals,
                      doc='intermediate input')
        
        self.m.Z = Var(self.m.i,
                      initialize=Z0_init,
                      within=PositiveReals,
                      doc='output of the j-th good')
        
        self.m.Xp = Var(self.m.i,
                      initialize=Xp0_init,
                      within=PositiveReals,
                      doc=' household consumption of the i-th good')
        
        self.m.Xg = Var(self.m.i,
                      initialize=Xg0_init,
                      within=PositiveReals,
                      doc='government consumption')
        
        self.m.Xv = Var(self.m.i,
                      initialize=Xv0_init,
                      within=PositiveReals,
                      doc=' investment demand')
        
        self.m.E = Var(self.m.i,
                      initialize=E0_init,
                      within=PositiveReals,
                      doc=' exports')
        
        self.m.M = Var(self.m.i,
                      initialize=M0_init,
                      within=PositiveReals,
                      doc='imports')
        
        self.m.Q = Var(self.m.i,
                      initialize=Q0_init,
                      within=PositiveReals,
                      doc='Armingtons composite good')
        
        self.m.D = Var(self.m.i,
                      initialize=D0_init,
                      within=PositiveReals,
                      doc='domestic good')
        
        
        def p_init(model, v):
            return 1
        
        
        
        self.m.pf = Var(self.m.h,
                      initialize=p_init,
                      within=PositiveReals,
                      doc='the h-th factor price')
        
        self.m.py = Var(self.m.i,
                      initialize=p_init,
                      within=PositiveReals,
                      doc='composite factor price')
        
        self.m.pz = Var(self.m.i,
                      initialize=p_init,
                      within=PositiveReals,
                      doc=' supply price of the i-th good')
        
        self.m.pq = Var(self.m.i,
                      initialize=p_init,
                      within=PositiveReals,
                      doc='Armingtons composite good price')
        
        self.m.pe = Var(self.m.i,
                      initialize=p_init,
                      within=PositiveReals,
                      doc='export price in local currency')
        
        self.m.pm = Var(self.m.i,
                      initialize=p_init,
                      within=PositiveReals,
                      doc='import price in local currency')
        
        self.m.pd = Var(self.m.i,
                      initialize=p_init,
                      within=PositiveReals,
                      doc='the i-th domestic good price')
        
        self.m.epsilon = Var(
                      initialize= 1,
                      within=PositiveReals,
                      doc='exchange rate')
        
        self.m.Sp = Var(
                      initialize=Sp0_init,
                      within=PositiveReals,
                      doc='private saving')
        
        self.m.Sg = Var(
                      initialize=Sg0_init,
                      within=PositiveReals,
                      doc='government saving')
        
        self.m.Td = Var(
                      initialize=Td0_init,
                      within=PositiveReals,
                      doc='direct tax')
        
        self.m.Tz = Var(self.m.i,
                      initialize=Tz0_init,
                      within=PositiveReals,
                      doc='production tax')
        
        self.m.Tm = Var(self.m.i,
                      initialize=Tm0_init,
                      within=PositiveReals,
                      doc='import tariff')
        
        # ------------------------------------------- #
        # DEFINE EQUATIONS
        
        def eqpy_rule(model, i):
            return (model.Y[i] == model.b[i]*np.prod([model.F[h, i]**model.beta[h, i] for h in model.h]))
        
        self.m.eqpy = Constraint(self.m.i, rule=eqpy_rule, doc='composite factor agg. func.')
        
        def eqF_rule(model, h, i):
            return (model.F[h,i] == model.beta[h,i]*model.py[i]*model.Y[i]/model.pf[h])
        
        self.m.eqF = Constraint(self.m.h, self.m.i, rule=eqF_rule, doc='factor demand function')
        
        def eqX_rule(model, i, j):
            return (model.X[i,j] ==model.ax[i,j]*model.Z[j] )
        
        self.m.eqX = Constraint(self.m.i, self.m.i, rule=eqX_rule, doc='intermediate demand function')
        
        def eqY_rule(model, i):
            return (model.Y[i] == model.ay[i]*model.Z[i])
        
        self.m.eqY = Constraint(self.m.i, rule=eqY_rule, doc='composite factor demand function')
        
        def eqpzs_rule(model, j):
            return (model.pz[j] == model.ay[j]*model.py[j] +sum(model.ax[i,j]*model.pq[i] for i in model.i) )
        
        self.m.eqpzs = Constraint(self.m.i, rule=eqpzs_rule, doc='unit cost function')
        
        def eqTd_rule(model):
            return (model.Td == model.taud*sum(model.pf[h]*model.FF[h] for h in model.h) )
        
        self.m.eqTd = Constraint(rule=eqTd_rule, doc='direct tax revenue function')
        
        def eqTz_rule(model, i):
            return (model.Tz[i] == model.tauz[i]*model.pz[i]*model.Z[i])
        
        self.m.eqTz = Constraint(self.m.i, rule=eqTz_rule, doc='production tax revenue function')
        
        def eqTm_rule(model, i):
            return (model.Tm[i] == model.taum[i]*model.pm[i]*model.M[i])
        
        self.m.eqTm = Constraint(self.m.i, rule=eqTm_rule, doc='import tariff revenue function')
        
        def eqXg_rule(model, i):
            return (model.Xg[i] == model.mu[i]*(model.Td +sum(model.Tz[j] for j in model.i) +sum(model.Tm[j] for j in model.i)- model.Sg)  /model.pq[i])
        
        self.m.eqXg = Constraint(self.m.i, rule=eqXg_rule, doc='government demand function')
        
        def eqXv_rule(model, i):
            return (model.Xv[i] == model.lambd[i]*(model.Sp +model.Sg +model.epsilon*model.Sf)/model.pq[i])
        
        self.m.eqXv = Constraint(self.m.i, rule=eqXv_rule, doc='investment demand function')
        
        def eqSp_rule(model):
            return (model.Sp == model.ssp*sum(model.pf[h]*model.FF[h] for h in model.h) )
        
        self.m.eqSp = Constraint(rule=eqSp_rule, doc='private saving function')
        
        def eqSg_rule(model):
            return (model.Sg == model.ssg*(model.Td +sum(model.Tz[j] for j in model.i)+sum(model.Tm[j] for j in model.i)))
        
        self.m.eqSg = Constraint(rule=eqSg_rule, doc='government saving function')
        
        def eqXp_rule(model, i):
            return (model.Xp[i] == model.alpha[i]*(sum(model.pf[h]*model.FF[h] for h in model.h) - model.Sp - model.Td) / model.pq[i])
        
        self.m.eqXp = Constraint(self.m.i, rule=eqXp_rule, doc='household demand function')
        
        def eqpe_rule(model, i):
            return (model.pe[i] == (model.epsilon * model.pWe[i]))
        
        self.m.eqpe = Constraint(self.m.i, rule=eqpe_rule, doc='world export price equation')
        
        def eqpm_rule(model, i):
            return (model.pm[i] == model.epsilon*model.pWm[i])
        
        self.m.eqpm = Constraint(self.m.i, rule=eqpm_rule, doc='world import price equation')
        
        def eqepsilon_rule(model): 
            return sum(model.pWe[i]*model.E[i] for i in model.i) + model.Sf == sum(model.pWm[i]*model.M[i] for i in model.i)
        
        self.m.eqepsilon = Constraint(rule=eqepsilon_rule, doc='balance of payments')
        
        def eqpqs_rule(model, i):
            return (model.Q[i] == model.gamma[i]*(model.deltam[i]*model.M[i]**model.eta[i]+model.deltad[i]*model.D[i]**model.eta[i])**(1/model.eta[i]))
        
        self.m.eqpqs = Constraint(self.m.i, rule=eqpqs_rule, doc='Armington function')
        
        def eqM_rule(model, i):
            return ( model.M[i]== (model.gamma[i]**model.eta[i]*model.deltam[i]*model.pq[i]/((1+model.taum[i])*model.pm[i]))**(1/(1-model.eta[i]))*model.Q[i])
        
        self.m.eqM = Constraint(self.m.i, rule=eqM_rule, doc='import demand function')
        
        def eqD_rule(model, i):
            return ( model.D[i]== (model.gamma[i]**model.eta[i]*model.deltad[i]*model.pq[i]/model.pd[i])**(1/(1-model.eta[i]))*model.Q[i])
        
        self.m.eqD = Constraint(self.m.i, rule=eqD_rule, doc='domestic good demand function')
        
        def eqpzd_rule(model, i):
            return  model.Z[i] == model.theta[i]*(model.xie[i]*model.E[i]**model.phi[i]+model.xid[i]*model.D[i]**model.phi[i])**(1/model.phi[i])
        
        self.m.eqpzd = Constraint(self.m.i, rule=eqpzd_rule, doc='transformation function') 
        
        def eqE_rule(model, i): 
            return  model.E[i] == (model.theta[i]**model.phi[i]*model.xie[i]*(1+model.tauz[i])*model.pz[i]/model.pe[i])**(1/(1-model.phi[i]))*model.Z[i]
        
        self.m.eqE = Constraint(self.m.i, rule=eqE_rule, doc='export supply function')
        
        def eqDs_rule(model, i):
            return  model.D[i] == (model.theta[i]**model.phi[i]*model.xid[i]*(1+model.tauz[i])*model.pz[i]/model.pd[i])**(1/(1-model.phi[i]))*model.Z[i]
        
        self.m.eqDs = Constraint(self.m.i, rule=eqDs_rule, doc='domestic good supply function')
        
        def eqpqd_rule(model, i):
            return ( model.Q[i]==  model.Xp[i] + model.Xg[i] + model.Xv[i] +sum(model.X[i,j] for j in model.i))
        
        self.m.eqpqd = Constraint(self.m.i, rule=eqpqd_rule, doc='market clearing cond. for comp. good')
        
        def eqpf_rule(model, h):
            return (sum(model.F[h,i] for i in model.i) == model.FF[h])
        
        self.m.eqpf = Constraint(self.m.h, rule=eqpf_rule, doc='factor market clearing condition')
        
        
        # ------------------------------------------- #
        # DEFINE OBJECTIVE
        def obj_rule(model):
            return np.prod([model.Xp[i]**model.alpha[i] for i in model.i])
        
        self.m.obj = Objective(rule=obj_rule, sense=maximize,
                              doc='utility function [fictitious]')
        
        
        print("stdcge model loaded")
        return self.m
        
            
        
