# -*- coding: utf-8 -*-
"""
Created on Thu Feb  3 17:35:50 2022

@author: U346250
"""

import pandas as pd
import numpy as np

ctmt = pd.read_csv(r"./Dados/CTMT_EPB.txt", sep = ';')
ssdmt = pd.read_csv(r"./Dados/SSDMT_EPB.txt", sep = ';')
ssdmt_prod = ssdmt.copy()



##TAG 1 = PAC_1 > PAC_2
##TAG 2 = PAC_2 > PAC_1


############## FUNÇÃO ENCONTRAR OS PRIMEIROS TRECHOS DOS ALIMENTADORES  #######################################
#INPUTS: CTMT, SSDMT
#OUTPUT: LISTA COM PRIMEIROS TRECHOS
#DESCRIÇÃO: O campo PAC da CTMT é igual ao campo PAC_1 ou PAC_2 do primeiro trecho do alimentador

def ind_trecho_alimentador(ctmt, ssdmt):
    trecho_alimentador = pd.merge(ctmt[['PAC']], ssdmt[['COD_ID','CTMT','PAC_1', 'PAC_2']], left_on='PAC', right_on = 'PAC_1', how='right')
    trecho_alimentador.rename(columns={"PAC": "PAC_1_tag"}, inplace = True)
    trecho_alimentador = pd.merge(ctmt[['PAC']], trecho_alimentador, left_on='PAC', right_on = 'PAC_2', how='right')
    trecho_alimentador.rename(columns={"PAC": "PAC_2_tag"}, inplace = True)
    trecho_alimentador.fillna('0', inplace = True)
    trecho_alimentador = trecho_alimentador[(trecho_alimentador['PAC_1_tag'] !='0') | (trecho_alimentador['PAC_2_tag'] !='0')]
    trecho_alimentador['tag'] = np.where(trecho_alimentador['PAC_1_tag'] ==0, 2, 1)
    trecho_alimentador =  trecho_alimentador[['COD_ID','CTMT','tag']]
    trecho_alimentador.reset_index(inplace =True)
    return trecho_alimentador


############## PROXIMO PAC #######################################
def proximo_pac (ssdmt, index, tag):  
    if tag == 1:
        pac= ssdmt['PAC_2'][index_trecho_atual]
    if tag == 2:
        pac= ssdmt['PAC_1'][index_trecho_atual]    
    return pac
############## BUSCAR PROXIMO TRECHO #######################################


trecho_alimentador = ind_trecho_alimentador(ctmt, ssdmt)
trecho_atual = trecho_alimentador['COD_ID'][0]
tag = trecho_alimentador['tag'][0]
index_trecho_atual = ssdmt.loc[ssdmt['COD_ID']== trecho_atual].index.item() # index_atual 
pac_prox = proximo_pac(ssdmt, index_trecho_atual, tag)


tag = 1
trecho_atual = 15224270
index_trecho_atual = ssdmt.loc[ssdmt['COD_ID']== trecho_atual].index.item() # index_atual 


def pegar_proximo_trecho(df_prod,poste, no,chave, alim):
    lista_vazia =[]
    if chave != 2:
        df = df_prod[((df_prod['NU_NO_FINAL']== no) & (df_prod['NU_PG_FINAL_ID']== poste) & (df_prod['ALIMENTADOR']== alim)) | 
                     ((df_prod['NU_NO_INICIAL']== no) & (df_prod['NU_PG_INICIAL_ID']== poste) & (df_prod['ALIMENTADOR']== alim))]
        for ind in df.index:
            if (df['CD_INDD_ESTADO'][ind]== 2) & (df['POSTE_INSTALACAO'][ind] == poste):
                #print('entrou', poste, df.index)
                df.drop(index=ind, inplace=True)
                #print('entrou', poste,df.index)
        lista_vazia =  df.index.values.tolist()   
    return lista_vazia
