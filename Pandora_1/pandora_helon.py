# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

# Designação da Entidade: Circuito de Média Tensão
# Designação da Modelagem: CTMT
ctmt = pd.read_csv("./Dados/CTMT_EPB.txt", sep=';')
print(f'ctmt.columns = \n{ctmt.columns}')
print(f'\n')
print(f'ctmt = \n{ctmt}')
print(f'=====\n')

# Designação da Entidade: Segmento de Rede Média Tensão
# Designação da Modelagem: SSDMT
ssdmt = pd.read_csv("./Dados/SSDMT_EPB.txt", sep=';')
print(f'ssdmt.columns = \n{ssdmt.columns}')
print(f'\n')
print(f'ssdmt = \n{ssdmt}')
print(f'=====\n')

# TAG 1 = PAC_1 > PAC_2
# TAG 2 = PAC_2 > PAC_1

# ############# FUNÇÃO ENCONTRAR OS PRIMEIROS TRECHOS DOS ALIMENTADORES  #######################################
# INPUTS: CTMT, SSDMT
# OUTPUT: LISTA COM PRIMEIROS TRECHOS
# DESCRIÇÃO:
# São selecionados como trechos conectados
# O campo PAC da tabela CTMT é igual ao campo PAC_1 ou PAC_2 do primeiro trecho do alimentador


def ind_trecho_alimentador(ctmt, ssdmt):
    trecho_alimentador = pd.merge(ctmt[['PAC']], ssdmt[[
                                  'COD_ID', 'CTMT', 'PAC_1', 'PAC_2']], left_on='PAC', right_on='PAC_1', how='right')
    trecho_alimentador.rename(columns={"PAC": "PAC_1_tag"}, inplace=True)
    trecho_alimentador = pd.merge(
        ctmt[['PAC']], trecho_alimentador, left_on='PAC', right_on='PAC_2', how='right')
    trecho_alimentador.rename(columns={"PAC": "PAC_2_tag"}, inplace=True)
    trecho_alimentador.fillna('0', inplace=True)
    trecho_alimentador = trecho_alimentador[(trecho_alimentador['PAC_1_tag'] != '0') | (
        trecho_alimentador['PAC_2_tag'] != '0')]
    trecho_alimentador['tag'] = np.where(
        trecho_alimentador['PAC_1_tag'] == 0, 2, 1)
    trecho_alimentador = trecho_alimentador[['COD_ID', 'CTMT', 'tag']]
    trecho_alimentador.reset_index(inplace=True)
    return trecho_alimentador


def selecionar_troncos_dos_ctmt(ctmt, ssdmt):

    troncos_PAC1 = pd.merge(
        ctmt[['PAC']],
        ssdmt[['COD_ID', 'CTMT', 'PAC_1', 'PAC_2']],
        left_on='PAC',
        right_on='PAC_1',
        how='right')
    troncos_PAC1.rename(columns={"PAC": "PAC_1_tag"}, inplace=True)
    troncos_PAC1['tag'] = 1

    troncos_PAC2 = pd.merge(
        ctmt[['PAC']],
        ssdmt[['COD_ID', 'CTMT', 'PAC_1', 'PAC_2']],
        left_on='PAC',
        right_on='PAC_2',
        how='right')
    troncos_PAC2.rename(columns={"PAC": "PAC_2_tag"}, inplace=True)
    troncos_PAC2['tag'] = 2

    troncos = pd.concat([troncos_PAC1, troncos_PAC2])
    troncos.fillna('0', inplace=True)
    troncos.reset_index(inplace=True)
    return troncos

# ############# PROXIMO PAC #######################################


def proximo_pac(ssdmt, index, tag):
    if tag == 1:
        pac = ssdmt['PAC_2'][index_trecho_atual]
    if tag == 2:
        pac = ssdmt['PAC_1'][index_trecho_atual]
    return pac
############## BUSCAR PROXIMO TRECHO #######################################


trecho_alimentador = ind_trecho_alimentador(ctmt, ssdmt)
print(f'trecho_alimentador.columns = \n{trecho_alimentador.columns}')
print(f'\n')
print(f'trecho_alimentador = \n{trecho_alimentador}')
print(f'=====\n')

trecho_alimentador2 = selecionar_troncos_dos_ctmt(ctmt, ssdmt)
print(f'trecho_alimentador2.columns = \n{trecho_alimentador2.columns}')
print(f'\n')
print(f'trecho_alimentador2 = \n{trecho_alimentador2}')
print(f'=====\n')

breakpoint()

trecho_atual = trecho_alimentador['COD_ID'][0]
tag = trecho_alimentador['tag'][0]
index_trecho_atual = ssdmt.loc[ssdmt['COD_ID']
                               == trecho_atual].index.item()  # index_atual
pac_prox = proximo_pac(ssdmt, index_trecho_atual, tag)


tag = 1
trecho_atual = 15224270
index_trecho_atual = ssdmt.loc[ssdmt['COD_ID']
                               == trecho_atual].index.item()  # index_atual


def pegar_proximo_trecho(df_prod, poste, no, chave, alim):
    lista_vazia = []
    if chave != 2:
        df = df_prod[((df_prod['NU_NO_FINAL'] == no) & (df_prod['NU_PG_FINAL_ID'] == poste) & (df_prod['ALIMENTADOR'] == alim)) |
                     ((df_prod['NU_NO_INICIAL'] == no) & (df_prod['NU_PG_INICIAL_ID'] == poste) & (df_prod['ALIMENTADOR'] == alim))]
        for ind in df.index:
            if (df['CD_INDD_ESTADO'][ind] == 2) & (df['POSTE_INSTALACAO'][ind] == poste):
                #print('entrou', poste, df.index)
                df.drop(index=ind, inplace=True)
                #print('entrou', poste,df.index)
        lista_vazia = df.index.values.tolist()
    return lista_vazia
