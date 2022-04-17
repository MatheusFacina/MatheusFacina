#!/usr/bin/env python
# coding: utf-8

# **PARA FAZER**
#     
#     - criar uma sublista com os que não foram baixados, em DF que possa ser lido novamente e baixar
#     - fazer os downloads em um ambiente separado da pasta final para não ficar listando todos os arquivos todas as vezes
#     - separar os do xx automaticamente

# **Instalando e importantdo bibliotecas**

# !pip install selenium
# !pip install pandas
# !pip install openpyxl


import time
from datetime import datetime
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.action_chains import ActionChains


# **Definindo Funções**

# Função que apenas pergunta se pode continuar, sim ou nao

def ask_ok(prompt, follow="Continando "):
    while True:
            ok = input(prompt)
            if ok in ["SIM", "SI", "S" "sim", "si", "s", "ok"]:
                print(follow)
                return True
            elif ok in ["n", "na", "nao", "não", "nã" "N", "NA", "NÃ", "NÃO", "NAO"]:
                print("\nEntão digite novamente ")
                return False
            else:
                print("\nPOR FAVOR DIGITE SIM OU NAO")

# variável para esperar

x=0.5

# testando a função de espera acima pra ver velocidade

start_time = datetime.now()

for i in range(10):

    start_time = datetime.now()
    
    time.sleep(x)
    
    end_time = datetime.now()

    print('Duração: {}'.format(end_time - start_time))


#função da biblioteca os para pegar a current working dir
default_dir = os.getcwd() 


print(default_dir)


# **Lendo as contas no excel**

DIR=os.getcwd()
print(DIR)

os.chdir(default_dir)
print(os.getcwd())

contas_df = pd.read_excel("contas.xlsx")
display(contas_df)

os.chdir(DIR)
print(os.getcwd())

del DIR

# contas.xlsx é o nome da planilha excel na mesma pasta que o código que aqui é alocada em contas_df com o Pandas

display(contas_df)


# **Pedindo datas**


while True:
    dataInicio = input("Data inicial dos extratos com barras: ")
    dataFinal = input("Data final dos extratos com barras: ")
    if ask_ok("As datas " + '\033[1m' + dataInicio + " a " + dataFinal + "\033[0;0m" +" estão corretas? ", "Continuando com o período de " + '\033[1m' + dataInicio + " a " + dataFinal + "\033[0;0m")==True:



# Variável com as datas concatenadas e trocando / por - para não dar problema com os caminhos de arquivos do windows

datas = (dataInicio + "_" + dataFinal).replace(r"/","-")


print(datas)


# **Mudando o local onde o chrome salva arquivos e Abrindo uma janela do Chrome automatizada chamada driver**   

# variável de onde vai baixar aqrquivos pelo chrome seguido de uma pergunta se está correto e deseja continuar

while True:
    
    ondebaixar = input("Digite o caminho para fazer downloads ou deixe em branco para configuração padrão ")
    if ask_ok("Você digitou " + '\033[1m' + ondebaixar + "\033[0;0m" +"? ", "Continuando com o caminho:\n" + '\033[1m' + ondebaixar)==True:
        break


if ondebaixar =="":
    ondebaixar=os.path.join(os.getcwd(), datas)
else:
    ondebaixar=os.path.join(ondebaixar, datas)


print(ondebaixar)


# colocando o caminho escolhido como caminho de downloads nas opções do chrome e abilitando downloads multiplos

chromeOptions = webdriver.ChromeOptions()

if ondebaixar == "":
    
    
    print("Será baixado em uma pasta nova dentro da pasta do codigo mesmo") 
    prefs = {"download.default_directory" : ondebaixar,  "default_content_settings": {"multiple-automatic-downloads": 1.0}}
    chromeOptions.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome("chromedriver",options=chromeOptions)
    driver = webdriver.Chrome("chromedriver")
    driver.set_window_size(1296, 1000)
    driver.get("https://example.com")
    
    
else:
    
    
    print("Será baixado na pasta dentro de " + ondebaixar)
    prefs = {"download.default_directory" : ondebaixar, "default_content_settings": {"multiple-automatic-downloads": 1.0}}
    chromeOptions.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome("chromedriver",options=chromeOptions)
    driver.set_window_size(1296, 1000)
    driver.get("https://example.com")

del chromeOptions
    
while True:
    if ask_ok("Por favor, entre com as credenciais na example e digite SIM ")==True:
        break


#Mudando dir pra pasta mãe de ondebaixar

os.chdir(os.path.dirname(ondebaixar))


print(os.getcwd())


# Criando pasta dentro da pasta atual com nome de datas e mudando a dir para ela

try:
    os.mkdir(datas)
    os.chdir(os.path.join(os.getcwd(),datas))
except Exception as e: 
    print(e)

print(os.getcwd())


# **Solicitando os extratos**\
# \
#    Entrando no link dos extratos personalizados com o numero da conta e cpf do cliente
#    Preenchendo campos com datas Inicio e Final(perguntadas acima
#    Apertando Enter para Solicitar

for idx, conta, nome in contas_df.itertuples():
    
    try:
    
        print (idx+1,f"{conta:09d}",nome + " Fazendo")

        start_time = datetime.now()

        driver.get('https://example.com')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="mainNavbar"]/form/div[1]/input'))).send_keys(format(conta,'09d'))
        
        time.sleep(x)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="mainNavbar"]/form/div[2]/div/a'))).click()
        
        time.sleep(x)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="submenu-documents"]/a')))
        
        time.sleep(x)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="menu-list-history"]/a'))).click()
        
        time.sleep(x)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="submenu-documents"]/a'))).click()
        
        time.sleep(x)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="submenu-documents-extract"]/a'))).click()
        
        time.sleep(x)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'/html/body/examplemenu/div/div/div/div/ui-view/documents-extract/div/
                                                                        div/nav/li[2]'))).click()
                                                                        
        time.sleep(x)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'/html/body/examplemenu/div/div/div/div/ui-view/documents-extract/
                                                                        div/div/ng-include[2]/div/div[1]/form/div[1]/div[1]/
                                                                        div/datepicker/input'))).send_keys(dataInicio)
                                                                        
        time.sleep(x)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'/html/body/examplemenu/div/div/div/div/ui-view/documents-extract/div/div/
                                                                        ng-include[2]/div/div[1]/form/div[1]/div[2]/div/datepicker/input'))).send_keys(dataFinal)
                                                                        
        time.sleep(1)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'/html/body/examplemenu/div/div/div/div/ui-view/documents-extract/div/div/
                                                                        ng-include[2]/div/div[1]/form/div[1]/div[2]/div/datepicker/input'))).send_keys(Keys.ENTER)
                                                                        
        time.sleep(2)
        
        end_time = datetime.now()
        
        print(idx+1,f"{conta:09d}", nome + ' Feito em {}'.format(end_time-start_time))
        
    except Exception as e: print(e)
        
    


# **Fazer dowload dos extratos anteriormente solicitados**
# Versão 2


os.chdir(ondebaixar)
ultimo_nome_baixado="aoisjda1doiasjd31276alskidn1" #coloquei qualquer string que nunca apareceria apenas para iniciar a variável
listaes=[] #uma lista com as excessões que podem aparecer para saber depois quais deram errrado e baixar manualmente
total_start_time = datetime.now()

for idx, conta, nome in contas_df.itertuples():
    
    try:
    
        print (idx+1,f"{conta:09d}",nome + " Fazendo")
        
        start_time = datetime.now()
        
        driver.get('https://access.examplex.com/op/')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="mainNavbar"]/form/div[1]/input'))).send_keys(format(conta,'09d'))
        time.sleep(x)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="mainNavbar"]/form/div[2]/div/a'))).click()
        time.sleep(x)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="submenu-documents"]/a')))
        time.sleep(x)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="menu-list-history"]/a'))).click()
        time.sleep(x)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="submenu-documents"]/a'))).click()
        time.sleep(x)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="submenu-documents-extract"]/a'))).click()
        time.sleep(x)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'/html/body/examplemenu/div/div/div/div/ui-view/documents-extract/div/div/
                                                                        nav/li[2]' ))).click()
        time.sleep(x)
        body = driver.find_element(By.XPATH, '/html/body')
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(x)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/examplemenu/div/div/div/div/ui-view/documents-extract/div/div/
                                                                        ng-include[2]/div/div[2]/div/table/thead/tr/th[1]'))).click()
        time.sleep(1)
        
        nfiles0=len(os.listdir(os.getcwd()))
        
        try:
    
            # Verifica se o primeiro da lista é o da data referente
            if WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH,'/html/body/examplemenu/div/div/div/div/ui-view/documents-extract/
                                                                              div/div/ng-include[2]/div/div[2]/div/table/tbody/
                                                                              tr[1]/td[3]' ))).text == dataInicio + " até " + dataFinal:
                                                                              
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH,'/html/body/examplemenu/div/div/div/div/ui-view/documents-extract/
                                                                               div/div/ng-include[2]/div/div[2]/div/table/tbody/tr[1]/td[5]/
                                                                               button'))).send_keys(Keys.RETURN)
                                                                               
                pass
            
        except Exception as e:
            print(e)
            listaes.append(nome)   
            end_time = datetime.now()
            print(idx+1,f"{conta:09d}", nome + '\033[1m' + ' NÂO ' + '\033[0;0m' + ' foi feito em {}'.format(end_time-start_time))
            continue            

        time.sleep(x)

        cont=0
        while cont<20: # quando vir que a quantidade de arquivos aumentou(baixou um novo) ele passa pra próxima 
            time.sleep(0.5)
            
            nfiles1=len(os.listdir(os.getcwd()))

            if nfiles1>nfiles0:
                break
            else:
                cont=cont+1
        
        time.sleep(1)      
        
        # checar se fez download certo
        files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime) # cria uma lista ordenada pela data de modificação        
        while True:
            time.sleep(1)
            if files == [] or 'crdownload' in files[-1] or '.tmp' in files[-1] : # caso o último item da lista baixado tenha a string crdownload
                files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
                continue
            
            elif nfiles0==nfiles1:
                listaes.append(conta + '_' + nome)
                end_time = datetime.now()
                print(idx+1,f"{conta:09d}", nome + ' NÂO foi feito em {}'.format(end_time-start_time))
                break
            
            else:
                
                try:
                    
                    os.rename(files[-1], nome + "_" + files[-1])
                    end_time = datetime.now()
                    print(idx+1,f"{conta:09d}", nome + ' Feito em {}'.format(end_time-start_time))
                    break
               
                except Exception as e:
                    print(e)
                    continue
                
    except Exception as e:
        print(e)
        listaes.append(nome)   
        end_time = datetime.now()
        print(idx+1,f"{conta:09d}", nome + ' NÂO foi feito em {}'.format(end_time-start_time))
        continue
                
del nfiles0, nfiles1, files, cont

total_end_time=datetime.now()

print("Terminamos em {}".format(total_end_time-total_start_time))

if listaes == []:
    print("Todos os extratos foram baixados com sucesso")
else:
    print("Faltaram os seguintes:", listaes)


os.chdir(default_dir)



print(files[-1])


# **Apertando Page Down no body da página**



# body = driver.find_element(By.XPATH, '/html/body')
# body.send_keys(Keys.PAGE_DOWN)


# **Solicitar notas de corretagem**



os.chdir(ondebaixar)

listaes=[]
ultimo_nome_baixado=None
for idx, conta, nome in contas_df.itertuples():
    try:
        print (idx+1,f"{conta:09d}",nome + " Fazendo")

        start_time = datetime.now()

        driver.get('https://example.com/op/')
        time.sleep(x)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="mainNavbar"]/form/div[1]/input'))).send_keys(format(conta,'09d'))
        time.sleep(x)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="mainNavbar"]/form/div[2]/div/a'))).click()
        time.sleep(x)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="submenu-documents"]/a')))
        time.sleep(x)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="menu-list-history"]/a'))).click()
        time.sleep(x)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="submenu-documents"]/a'))).click()
        time.sleep(x)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'/html/body/menu/div/div/div/div/navbar/div/nav[2]/ul/li[3]/ul/li[4]/ul/li[4]/a'))).click()
        time.sleep(x)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="period"]'))).send_keys("Personalizado")
        time.sleep(x)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'/html/body/examplemenu/div/div/div/div/ui-view/history-documents-trade-tickets/div/div/ng-include[1]/div/div[1]/fieldset/div[1]/div[4]/datepicker/input'))).send_keys(dataInicio)
        time.sleep(x)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'/html/body/examplemenu/div/div/div/div/ui-view/history-documents-trade-tickets/div/div/ng-include[1]/div/div[1]/fieldset/div[1]/div[5]/datepicker/input'))).send_keys(dataFinal)
        time.sleep(x)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'/html/body/examplemenu/div/div/div/div/ui-view/history-documents-trade-tickets/div/div/ng-include[1]/div/div[1]/fieldset/div[2]/button'))).send_keys(Keys.RETURN)
        time.sleep(x)
        
        nfiles0=len(os.listdir(ondebaixar))
        
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH,'/html/body/examplemenu/div/div/div/div/ui-view/history-documents-trade-tickets/div/div/ng-include[1]/div/div[2]/div/div/button'))).send_keys(Keys.RETURN)
        time.sleep(x)
        
        cont=0
        while cont<20: # quando vir que a quantidade de arquivos aumentou(baixou um novo) ele passa pra próxima 
            time.sleep(0.5)
            
            nfiles1=len(os.listdir(os.getcwd()))

            if nfiles1>nfiles0:
                break
            else:
                cont=cont+1
        
        del nfiles0, nfiles1
        
        time.sleep(1.5)       
        
        files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
        
        while True:
            
            time.sleep(1)
            
            if files == [] or "crdownload" in files[-1]:
                files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
                continue
            
            else:
                os.rename(files[-1], nome + "_" + files[-1])
                ultimo_nome_baixado=nome
                break
                
        end_time = datetime.now()
        
        print(idx+1,f"{conta:09d}", nome + ' Feito em {}'.format(end_time-start_time))
        
    except Exception as e: 
        print(e)
        listaes.append(nome)
        
print("Terminamos")

if listaes == []:
    print("Todos os extratos foram baixados com sucesso")
else:
    print("Faltaram os seguintes:", listaes)


os.chdir(r'C:\Users\xxx\pasta')


# **RISCOS SISTEMICOS:**\
#      Se mudar a posição/xpath de algum elemento das páginas web precisa pega-los novamente
#      Se muda a quantidade de caracteres na conta ou no cpf precisa formatar as variáveis de acordo
