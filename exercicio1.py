#!/usr/bin/env python

import urllib
import pandas as pd
from exercicio1_lookup import lookup_regiao

########################################################################
#As a first step, retrieve data for all years saving it in a .csv file #
########################################################################

anos = [2003,2004,2005,2006,2007]
#Lendo o arquivo csv dos anos especificados e os concatenando em um pandas.dataframe
df_acidentes = pd.DataFrame()
for ano in anos :
  url = "http://api.dataprev.gov.br/previdencia/anuario/{0}/acidentes-do-trabalho.csv".format(ano)
  df1 = pd.read_csv(url)
  df_acidentes = pd.concat([df_acidentes, df1])

#Armazenando o arquivo, em formato cvs, com todos os 5 anos recuperados
df_acidentes.to_csv('acidentes-do-trabalho-2003-2007.csv')

###################################################################################
#transform and analyze the data to get the top 3 brazilian cities on the dataset, #
#which grew the metric the most between 2003 and 2007, by geopolitical region.    #
##################################################################################

#Reduzindo o Dataframe somente para os anos 2003 e 2007 para calcular a diferenca de acidentes
df_2003 = df_acidentes[(df_acidentes['Ano'] == 2003)] 
df_2007 = df_acidentes[(df_acidentes['Ano'] == 2007)]

#Criando dois dataframes proprios, para que as proximas operacoes nao sejam feitas nas copias em memoria do df_acidentes 
df_2003 = df_2003.copy()
df_2007 = df_2007.copy()

#Criando array com os campos de tipos de acidentes/obitos que devem ser somados  
campos_quantidade = ['Quantidade_Acidentes_com_CAT_Tipicos',\
                    'Quantidade_Acidentes_com_CAT_Trajeto',\
                    'Quantidade_Acidentes_com_CAT_Doenca_Profissional',\
                    'Quantidade_Obitos',\
                    'Quantidade_Acidentes_Sem_CAT']

#Somando e adicionando o campo Soma no dataframe
df_2003['Soma'] = df_2003[campos_quantidade].sum(axis=1)
df_2007['Soma'] = df_2007[campos_quantidade].sum(axis=1)

#Reduzindo os dataframes somente para os campos que serao utilizados
df_2003 = df_2003[['Municipio_COD-IBGE','Municipio_Nome','UF', 'Soma']]
df_2007 = df_2007[['Municipio_COD-IBGE','Soma']]

#Calculando a diferenca entre os totais de acidentes de 2007 e 2003
df_acidentes = pd.merge(df_2003, df_2007, on='Municipio_COD-IBGE', how='inner')
df_acidentes['Diferenca'] = df_acidentes['Soma_y'] - df_acidentes['Soma_x']

#Criando um campo de Regiao
df_acidentes['Regiao'] = df_acidentes['UF'].apply(lookup_regiao)

#Recuperando as 3 cidades com as maiores diferencas por regiao
regioes = ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul']
data_final = pd.DataFrame()
for regiao in regioes :
  #Ordenando pela diferenca
  df1 = df_acidentes[df_acidentes['Regiao'] == regiao].sort_values(by='Diferenca', ascending=False)
  #Restringindo os 3 primeiros da regiao
  data_final = pd.concat([data_final, df1.iloc[0:3]])

#Reduzindo o dataframe para somente a informacao requerida
data_final = data_final[['Diferenca','UF','Municipio_COD-IBGE','Municipio_Nome']]
#Armazenando o resultado final
data_final.to_csv('acidentes-do-trabalho-resultado.csv', index=False)