#!/usr/bin/env python
# coding: utf-8

# pip install pandas
# pip install docx
# pip install docxtpl
# pip install docx2pdf


import pandas as pd
import os
# from docx import Document
from docxtpl import DocxTemplate
from docx2pdf import convert
import time
from datetime import datetime


# **Funções basicas**

def get_MonthName_Day_Year(dateEnglish):
    __months = ["nada",
          "Janeiro",
          "Fevereiro",
          "Março",
          "Abril",
          "Maio",
          "Junho",
          "Julho",
          "Agosto",
          "Setembro",
          "Outubro",
          "Novembro",
          "Dezembro"]
    month = dateEnglish.partition("/")[0]
    monthName = __months[int(month)]
    day = dateEnglish.partition("/")[2].partition("/")[0]
    year = dateEnglish.partition("/")[2].partition("/")[2]
    return monthName, day, year


# **Buscando URL do google sheets para importar DataFrame**

sheet_url = "https://docs.google.com/spreadsheets/d/1AAAAio2nLeJk64k4WW55opBOx3ESsCQcXg6lyPGhbZU/edit?resourcekey#gid=1249177938"
url_1 = sheet_url.replace("/edit?resourcekey#gid=", "/export?format=csv&gid=")

df = pd.read_csv(url_1)

df_last = df.iloc[-1:]

display(df_last)


# **Preenchendo Template**

default_dir = os.getcwd()

print(os.getcwd())
os.chdir(r"C:\Users\mathe\OneDrive\DeskMatheus\Nova pasta")
print(os.getcwd())


document = Document(r'0. Formulário de Entrega_BATS_Modelo_AUto.docx')
template = DocxTemplate(r'0. Formulário de Entrega_BATS_Modelo_AUto.docx')
template.render(context)
template.save(r'autoTeste1.docx')


# **Código final só rodar quando tiver pronto**

import pandas as pd
import os
from docxtpl import DocxTemplate
from docx2pdf import convert

def get_MonthName_Day_Year(dateEnglish):
    
    months = ["nada",
          "Janeiro",
          "Fevereiro",
          "Março",
          "Abril",
          "Maio",
          "Junho",
          "Julho",
          "Agosto",
          "Setembro",
          "Outubro",
          "Novembro",
          "Dezembro"]
    
    month = dateEnglish.partition("/")[0]
    
    monthName = months[int(month)]
    
    day = dateEnglish.partition("/")[2].partition("/")[0]
    
    year = dateEnglish.partition("/")[2].partition("/")[2]
    
    return monthName, day, year

def makeForm():

    sheet_url = "https://docs.google.com/spreadsheets/d/"    "1AAAAio2nLeJk64k4WW55opBOx3ESsCQcXg6lyPGhbZU/edit?resourcekey#gid=1249177938"
    
    url_1 = sheet_url.replace("/edit?resourcekey#gid=", "/export?format=csv&gid=")

    df = pd.read_csv(url_1)

    df_last = df.iloc[-1:]

    default_dir = os.getcwd()

    print(os.getcwd())

    os.chdir(r"C:\Users\mathe\OneDrive\DeskMatheus\Nova pasta")

    print(os.getcwd())
    
    for idx, timeStamp, equipamento, nome, email, dataIni, dataFin, dano, problema,    acessorio, fotos in df_last.itertuples():
        
        monthName, day, year = get_MonthName_Day_Year(dataIni)
        
        context = {
            'equipamento' : equipamento,
            'dia': day,
            'mes': monthName,
            'ano': year,
            'nome': nome,
            'email' : email,
            'dano' : dano,
            'problema' : problema,
            'acessorio' : acessorio,
            }
        
        sheet_url = "https://docs.google.com/spreadsheets/d/"        "1AAAAio2nLeJk64k4WW55opBOx3ESsCQcXg6lyPGhbZU/edit?resourcekey#gid=1249177938"
        
        url_1 = sheet_url.replace("/edit?resourcekey#gid=", "/export?format=csv&gid=")
        
        template = DocxTemplate(r'0. Formulário de Entrega_BATS_Modelo_AUto.docx')
        
        template.render(context)
        
        os.mkdir(nome)
        
        template.save(r'{}/Form de Entrega do pedido {} de {}.docx'.format(nome,idx, nome) )
       
        convert(r'{}/Form de Entrega do pedido {} de {}.docx'.format(nome,idx, nome) )

start_time = datetime.now()

makeForm()

end_time = datetime.now()

print('Duração: {}'.format(end_time - start_time))

del start_time, end_time
