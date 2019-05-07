from pyomo.environ import *


class CrModelDef:
    def model():
        # Create AbstractModel
        m = AbstractModel()

        # Create Sets
        m.Z = Set(doc='All Accounts in Social Accounting Matrix')
        m.F = Set(within=m.Z, doc='Factors')
        m.L = Set(within=m.F, doc='Labor')
        m.LA = Set(within=m.F, doc='Land')
        m.K = Set(within=m.F, doc='Capital')
        m.G = Set(within=m.Z, doc='Governments')
        m.GN = Set(doc='Endogenous Governments')
        m.GNL = Set(doc='Local Endogenous Governments')
        m.GX = Set(doc='Exogenous Governments')
        m.GC = Set(doc='Local Governments')
        m.GS = Set(doc='Sales or Excise Taxes')
        m.GL = Set(doc='Land Taxes')
        m.GF = Set(doc='Factor Taxes')
        m.GI = Set(doc='Income Tax Units')
        m.GH = Set(doc='Household Tax Units')
        m.GY = Set(doc='Exognous Transfer PMT')
        m.GTA = Set(doc='Exognous Transfer PMT')
        m.GT = Set(doc='Endogenous Transfer PMT')
        m.H = Set(doc='Households')
        m.IG = Set(doc='I+G Sectors')
        m.I = Set(doc='Industry Sectors')
        m.DT = Set(doc='Downton sectors')
        m.NDT = Set(doc='Not Downtown sectors')
        m.IG2 = Set(doc='Endogenous Governments')
        m.IP = Set(doc='Production Sectors')
        m.FG = Set(doc='Production GOV.')
        m.HD = Set(doc='Housing serv. demand')
        m.SM = Set(doc='SimmLoop')
        ## TODO: Remove?
        m.R1H = Set(doc='Report 1 for Scalars')
        m.R2H = Set(doc='Report 2 for Status')
        m.MS = Set(doc='Labels for Model Status')
        m.SS = Set(doc='Labels for Sovler Status')

        # Aliases
        # Unnecessary, but easier when porting from something that uses them
        # TODO: remove
        m.J = SetOf(m.I)
        m.I1 = SetOf(m.I)
        m.Z1 = SetOf(m.Z)
        m.F1 = SetOf(m.F)
        m.G1 = SetOf(m.G)
        m.G2 = SetOf(m.G)
        m.GI1 = SetOf(m.GI)
        m.GC1 = SetOf(m.GC)
        m.GS1 = SetOf(m.GS)
        m.GX1 = SetOf(m.GX)
        m.GN1 = SetOf(m.GN)
        m.GF1 = SetOf(m.GF)
        m.H1 = SetOf(m.H)
        m.JP = SetOf(m.IP)
        m.JG = SetOf(m.IG)
        m.GY1 = SetOf(m.GY)
        m.GT1 = SetOf(m.GT)
        m.GY2 = SetOf(m.GY)
        m.GNL1 = SetOf(m.GNL)

        ## Index sets for elasticities etc
        m.ETALANDCAP = Set(initialize=['ETAL1', 'ETAI1', 'ETALB1'])
        m.ETAMISC = Set(initialize=['ETAM', 'ETAE', 'ETAY', 'ETAOP', 'SIGMA'])
        m.ETAMISCH = Set(initialize=['ETAPIT', 'ETAPT', 'HH0', 'HW0', 'ETARA', 'NRPG', 'ETAYD', 'ETAU']) 

        # Parameters
        # SAM and Other Parameters
        m.SAM = Param(m.Z, m.Z1, doc='Social Accounting Matrix')
        m.EMPLOY = Param(m.Z, m.F, doc='Factor demand')
        m.LANDCAP = Param(m.IG, doc='Misc elasticities')
        # TODO: indices for MISC?
        m.MISC = Param(m.Z, doc='misc file')
        m.MISCH = Parame(m.H, doc='misc HH data')
        m.TPC = Param(m.H, m.G, doc='')
        m.JOBCR = Param(m.H, m.L, doc='')
        m.TAUFF = Param(m.G, m.F, doc='assng of factor tax')
        m.IOUT = Param(m.G1, m.G1, doc='trans exclude')
        m.IGTD = Param(m.G1, m.G1, doc='gov trans')
        # Capital Coefficient Matrix
        m.BB = Param(m.I, m.IG, doc='capital comp')

        # More Parameters
        # Scalars

        # REMARK:
        # If double summation doesn't work, try:
        #  DEPR_initK(model, K) then sum over k in K
        def DEPR_init(model):
            return (sum(model.SAM[i, 'INVES'] for i in model.IG) /
                    sum(model.KS0[k, i] for k in model.K for i in model.IG))

        m.DEPR = Param(initialize=DEPR_init,
                       doc='CALC Depreciation Rate for K',
                       mutable=True)

        def ETAL2_init(model):
            return 3.0

        m.ETAL2 = Param(initialize=ETAL2_init,
                        doc='CRCE Land Supply Elasticity',
                        mutable=True)

        # More Parameters
        # Parameters calculated from the SAM and Table Data

        def Q10_init(model, z):
            return sum(model.SAM[z, zz] for zz in model.Z)

        def Q0_init(model, z):
            return sum(model.SAM[zz, z] for zz in model.Z)

        def DQ0_init(model, z):
            return model.Q10[z] - model.Q0[z]

        def B1_init(model, i, j):
            return model.SAM[i,j]

        m.B1 = Param(m.I, m.J, initialize=B1_init, doc='', mutable=True)

        # TODO: fill in; depends on IOUT
        def out_init(model, g, g1):
            return 0
        
        m.out = Param(m.G1, m.G1, initialize=out_init, doc='', mutable=True)

        def A_init(model, z1, z2):
            return model.SAM[z1, z2] / model.Q0[z1]

        m.A = Param(m.Z, m.Z,
                    initialize=A_init,
                    doc='IMPLAN Input Output Coefficients',
                    mutable=True)

        def A3_init(model, h, l):
            return 0

        m.A3 = Param(m.H, m.L, initialize=A3_init, doc='', mutable=True)

        def AD_init(model, z1, z2):
            return 0

        m.AD = Param(m.Z, m.Z1,
                     initialize=AD_init,
                     doc='IMPLAN Domestic Input Output Coefficients',
                     mutable=True)

        def AD1_init(model, z1, z2):
            return 0

        m.AD1 = Param(m.Z, m.Z1, initialize=AD1_init, doc='', mutable=True)

        def AG_init(model, z, g):
            return 0

        m.AG = Param(m.Z, m.G,
                     initialize=AG_init,
                     doc='IMPLAN Government Spending Shares of Net Income',
                     mutable=True)

        def AGFS_init(model, z, g):
            return 0

        m.AGFS = Param(m.Z, m.G, initialize=AGFS_init, doc='', mutable=True)

        def ALPHA_init(model, f, i):
            return 0

        m.ALPHA = Param(m.F, m.I,
                        initialize=ALPHA_init,
                        doc='IMPLAN Factor Share Exponents in Production Function',
                        mutable=True)

        def ALPHA1_init(model, f, i):
            return 0

        m.ALPHA1 = Param(m.F, m.I,
                         initialize=ALPHA1_init, doc='', mutable=True)

        def B_init(model, i, j):
            return model.BB[i, j]

        m.B = Param(m.I, m.IG, initialize=B_init, doc='', mutable=True)

        # TODO: depends on DS0, ALPHA, FD0, RHO
        def GAMMA_init(model, i):
            return (model.DS0[i] /
                    (sum(model.ALPHA[f, i] for f in model.F)**(-model.RHO[i])
                     )**(-1 / model.RHO[i]))
        
        m.GAMMA = Param(m.I,
                        initialize=GAMMA_init,
                        doc='CALC Production Function Scale',
                        mutable=True)

        # TODO: depends on DS0, ALPHA, FD0
        def DELTA_init(model, i):
            return (model.DS0[i] /
                    prod(model.FD0[f, i]**model.ALPHA[f, i] for f in model.F))
        
        m.DELTA = Param(m.I, initialize=DELTA_init, doc='', mutable=True)

        # TODO: depends on Y0
        def PIT_init(model, g, h):
            return model.SAM[g, h] / model.Y0[h]
        
        m.PIT = Param(m.G, m.H,
                      initialize=PIT_init,
                      doc='',
                      mutable=True)

        m.PIT0 = Param(m.G, m.H,
                       initialize=PIT_init,
                       doc='CALC Personal Income Tax SAM Value',
                       mutable=True)

        # TODO: depends on HH0
        def PRIVRET_init(model, h):
            return ((sum(model.SAM[z, h] for z in model.Z) -
                    sum(model.SAM[h, f] for f in model.F) +
                    sum(model.SAM[h, g] for g in model.GX)) /
                    model.HH0[h])
        
        m.PRIVRET = Param(m.H, initialize=PRIVRET_init, doc='', mutable=True)

        # TODO: depends on KPFOR0
        def KFOR_init(model, k):
            return (model.KPFOR0[k] /
                    sum(model.SAM['KAP', ig] for ig in model.IG))
        
        m.KFOR = Param(m.K,
                       initialize=KFOR_init,
                       doc='Proportion of Capital Income Outflow',
                       mutable=True)

        # TODO: depends on Y0, GVFOR0
        def GFOR_init(model, g):
            if model.Y0[g] != 0:
                return (model.GVFOR0[g] / model.Y0[g])

        m.GFOR = Param(m.G,
                       initialize=GFOR_init,
                       doc='Proportion of GOVT income Outflow',
                       mutable=True)

        # TODO: fill in
        def TAUF_init(model, g, f, z):
            return 0
        
        m.TAUF = Param(m.G, m.F, m.Z,
                       initialize=TAUF_init,
                       doc='CITY Factor Taxes',
                       mutable=True)

        # TODO: fill in
        def TAUF_init(model, g, f):
            return 0
        
        m.TAUFH = Param(m.G, m.F,
                        initialize=TAUFH_init,
                        doc='CITY AGG Factor Taxes',
                        mutable=True)

        # TODO: fill in
        def TAUFL_init(model, g, l):
            return 0
        
        m.TAUFL = Param(m.G, m.L,
                        initialize=TAUFL_init,
                        doc='CITY Employee Portion of Factor Tax',
                        mutable=True)

        # TODO: fill in
        def TAUFK_init(model, g, k):
            return 0
        
        m.TAUFK = Param(m.G, m.K,
                        initialize=TAUFK_init,
                        doc='CITY Capital Factor Taxes',
                        mutable=True)

        def TAUFX_init(model, g, f, z):
            return model.TAUF[g, f, z]

        m.TAUFX = Param(m.G, m.F, m.Z,
                        initialize=TAUFX_init, doc='', mutable=True)

        # TODO: fill in
        def TAUH_init(model, g, h):
            return 0

        m.TAUH = Param(m.G, m.H,
                       initialize=TAUH_init,
                       doc='CITY Household Taxes Other than PIT',
                       mutable=True)

        # TODO: fill in
        def TAUH0_init(model, g, h):
            return 0
        
        m.TAUH0 = Param(m.G, m.H,
                        initialize=TAUH0_init,
                        doc='CITY Household Taxes Other than PIT SAM Value',
                        mutable=True)

        def TAUQ_init(model, g, i):
            return (model.SAM[g, i] / (
                sum(model.SAM[i, j] for j in model.I) +
                sum(model.SAM[h, i] for h in model.H) +
                sum(model.SAM[i, gg] for gg in model.G) +
                model.SAM[i, 'ROW'] -
                sum(model.SAM[gs, i] for gs in model.GS)))

        m.TAUQ = Param(m.G, m.IG,
                       initialize=TAUQ_init,
                       doc='CITY Average Sales Tax Rates', mutable=True)

        def TAUC_init(model, g, i):
            return model.TAUQ[g, i]

        m.TAUC = Param(m.G, m.I,
                       initialize=TAUC_init,
                       doc='CITY Experimental Consumption Sales Tax Rates',
                       mutable=True)

        def TAUV_init(model, g, i):
            return model.TAUQ[g, i]

        m.TAUV = Param(m.G, m.I,
                       initialize=TAUV_init,
                       doc='CITY Experimental Consumption Sales Tax Rates',
                       mutable=True)

        def TAUN_init(model, g, i):
            return model.TAUQ[g, i]

        m.TAUN = Param(m.G, m.IG,
                       initialize=TAUN_init,
                       doc='CITY Experimental Consumption Sales Tax Rates',
                       mutable=True)

        def TAUX_init(model, g, i):
            return model.TAUQ[g, i]

        m.TAUX = Param(m.G, m.IG,
                       initialize=TAUX_init,
                       doc='CITY Experimental Consumption Sales Tax Rates',
                       mutable=True)

        def TAUG_init(model, g, i):
            return model.TAUQ[g, i]

        m.TAUG = Param(m.G, m.I,
                       initialize=TAUG_init,
                       doc='CITY Experimental Consumption Sales Tax Rates',
                       mutable=True)

        # TODO: fill in
        def TAXS_init(model, g, gx):
            return 0
        
        m.TAXS = Param(m.G, m.GX,
                       initialize=TAXS_init,
                       doc='CITY Tax Destination Shares',
                       mutable=True)

        def TAXS1_init(model, g):
            return (model.SAM[g, 'CYGF'] /
                    sum(model.SAM[g1, 'CYGF'] for g1 in model.GNL))
        
        m.TAXS1 = Param(m.GNL,
                        initialize=TAXS1_init, doc='',
                        mutable=True)

        ## TODO: depends on TAUFF
        def TEST20_init(model, f, i):
            return sum(model.SAM[gf, i] for gf in model.GF
                       if model.TAUFF[gf, f] != 0)
            
        m.TEST20 = Param(m.Z, m.Z,
                         initialize=TEST20_init,
                         doc='', mutable=True)

        ## For storing changes -> UNNECESSARY?
        ## TODO: replace with *post-process* functions
        # m.fstore = Param(m.Z, m.F, mutable=TRUE)
        # m.dystore = Param(m.Z, mutable=TRUE)
        # m.cpistore = Param(m.H, mutable=TRUE)
        # m.hhstore = Param(m.H, mutable=TRUE)
        # m.dsstore = Param(m.I, mutable=TRUE)
        
        #ELASTICITIES AND TAX DATA IMPOSED

        def BETA_init(model, i, h):
            return model.MISC[i, 'ETAY']

        m.BETA = Param(m.I, m.H, initialize=BETA_init,
                       doc='INCOME ELASTICITY OF DEMAND',
                       mutable=True)

        ## TODO: depends on ETAM, M0, DD0, D0
        def ETAD_init(model, i):
            return (-model.ETAM[i] * model.M0[i] /
                    (model.DD0[i] * model.D0[i]))

        m.ETAD = Param(m.I, initialize=ETAD_init,
                       doc='DOMESTIC SHARE PRICE ELASTICITIES',
                       mutable=True)

        def TEST0_init(model, z):
            return model.Q10[z] - model.Q0[z]

        def out_init(model, g):
            return model.IOUT[g, g]

        def LAMBDA_init(model, i):
            return model.MISC[i, 'ETAOP']

        # NOT IMPLEMENTED: a general function to grad the ETAs
        # ALT: Def ETA as matrix, rows indexed by i, columns by name
        def ETA_init(model, i, eta):
            return model.MISC[i, eta]

        def ETAE_init(model, i):
            return model.MISC[i, 'ETAE']

        def ETAM_init(model, i):
            return model.MISC[i, 'ETAM']

        def RHO_init(model, i):
            return (1 - model.MISC[i, 'SIGMA'])/model.MISC[i, 'SIGMA']

        def ETARA_init(model, h):
            return model.MISCH[h, 'ETARA']

        def ETAPI_init(model, h):
            return model.MISCH[h, 'ETAPI']

        def ETAPT_init(model, h):
            return model.MISCH[h, 'ETAPT']

        def ETAYD_init(model, h):
            return model.MISCH[h, 'ETAYD']

        def NRPG_init(model, h):
            return model.MISCH[h, 'NRPG']

        def ETAU_init(model, h):
            return model.MISCH[h, 'ETAU']

        def ETAI_init(model, i):
            return model.LANDCAP[i, 'ETAI1']

        def ETAL1_init(model, i):
            return model.LANDCAP[i, 'ETAL1']

        def ETALB1_init(model, i):
            return model.LANDCAP[i, 'ETALB1']

        # NB: should be indexed ['KAP', i]
        def ETAIX_init(model, i):
            return model.ETAI[i]

        # NB: indexed ['LAND', i]
        def ETAL_init(model, i):
            return model.ETAL1[i]

        def ETALB_init(model, l, i):
            return model.ETALB1[i]

        def TAUF0_init(model, g, f, z):
            return 0

