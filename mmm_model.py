import numpy as np
from math import sqrt
import statsmodels.formula.api as smf
from sklearn.metrics import r2_score,mean_squared_error
#===========================MODEL=============================
def Model(data_promo1,hier,channel_list):
    non_promo_col=np.array(['Price','PCV'])
    chann=np.array(channel_list)
    #chann=np.array(chann_list)
# =============================================================================
#     #Model 1 with nad curve and log log model 
#     Model.driver1 = [str("ad_stock_nad_")+i for i in chann.astype('object')+ "_log"]+[j for j in non_promo_col.astype('object') + "_log"]
#     eqn1=' ~ '+' + '.join([i for i in Model.driver1])
#     md1=smf.mixedlm('Sales_log' + eqn1,data = data_promo1,groups=data_promo1[hier],re_formula=eqn1)
#     Model.mdf1=md1.fit(method='lbfgs') 
# =============================================================================
    
    Model.driver1 = [str("ad_stock_nad_")+i for i in chann.astype('object')]+[j for j in non_promo_col.astype('object') ]
    eqn1=' ~ '+' + '.join([i for i in Model.driver1])
    md1=smf.mixedlm('Sales' + eqn1,data = data_promo1,groups=data_promo1[hier],re_formula=eqn1)
    Model.mdf1=md1.fit(method='lbfgs')
    #mdf= Model.mdf1
    
    #MODEL WITH SEASONALITY 
    Model.driver1_sea = [str("ad_stock_nad_")+i for i in chann.astype('object')]+[j for j in non_promo_col.astype('object')]+[str('season_')+str(i) for i in range(4)]
    eqn1_sea=' ~ '+' + '.join([i for i in Model.driver1_sea])
    md1_sea=smf.mixedlm('Sales' + eqn1_sea,data = data_promo1,groups=data_promo1[hier],re_formula=eqn1_sea)
    Model.mdf1_sea=md1_sea.fit(method='lbfgs')
    #mdf1_sea = Model.mdf1_sea
    
# =============================================================================
#     #Model 2 with S curve 
#     Model.driver2 = [str("ad_stock_s_")+i for i in chann.astype('object')+ "_log"]+[j for j in non_promo_col.astype('object') + "_log"]
#     eqn2=' ~ '+' + '.join([i for i in Model.driver2])
#     md2=smf.mixedlm('Sales_log' + eqn2,data = data_promo1,groups=data_promo1[hier],re_formula=eqn2)
#     Model.mdf2=md2.fit(method='cg')
# =============================================================================
     
    Model.driver=Model.driver1
    Model.mdf=Model.mdf1
    
    rms1 = r2_score(data_promo1['Sales'],Model.mdf1.fittedvalues)
    rms2 = r2_score(data_promo1['Sales'],Model.mdf1_sea.fittedvalues)

# =============================================================================
#     
#     acc1 = r2_score(data_promo1['Sales'],Model.mdf1.fittedvalues)
#     acc1 = r2_score(data_promo1['Sales_log'],Model.mdf1_sea.fittedvalues)
#     #if time (choose the best model)
#     
#     if acc1>acc2:
#         Model.mdf=Model.mdf1
#         Model.driver=Model.driver1
#     else:
#         Model.mdf=Model.mdf2
#         Model.driver=Model.driver2
# =============================================================================

#==================================================================
    
#Model(data_promo1,hier,chann_list)
