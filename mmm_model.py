
import numpy as np
from math import sqrt
import statsmodels.formula.api as smf
from sklearn.metrics import r2_score
#===========================MODEL=============================
def Model(data_promo1,hier,channel_list):
    non_promo_col=np.array(['Price','PCV'])
    chann=np.array(channel_list)
    
    #Model 1 with nad curve
    Model.driver1 = [str("ad_stock_nad_")+i for i in chann.astype('object')+ "_log"]+[j for j in non_promo_col.astype('object') + "_log"]
    eqn1=' ~ '+' + '.join([i for i in Model.driver1])
    md1=smf.mixedlm('Sales_log' + eqn1,data = data_promo1,groups=data_promo1[hier],re_formula=eqn1)
    Model.mdf1=md1.fit()
    
    #Model 2 with S curve 
    Model.driver2 = [str("ad_stock_s_")+i for i in chann.astype('object')+ "_log"]+[j for j in non_promo_col.astype('object') + "_log"]
    eqn2=' ~ '+' + '.join([i for i in Model.driver2])
    md2=smf.mixedlm('Sales_log' + eqn2,data = data_promo1,groups=data_promo1[hier],re_formula=eqn2)
    Model.mdf2=md2.fit()
    
    Model.driver=Model.driver1
    Model.mdf=Model.mdf1
# =============================================================================
#     
#     acc1 = r2_score(data_promo1['Sales_log'],Model.mdf1.fittedvalues)
#     acc2 = r2_score(data_promo1['Sales_log'],Model.mdf2.fittedvalues)
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