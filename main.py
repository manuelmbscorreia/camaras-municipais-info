#Importar tudo o que é necessário
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import pandas as pd
import time
import unidecode
import requests
from bs4 import BeautifulSoup
import urllib3
import re
import numpy as np

dfcm = pd.read_csv("listamunicipios.csv")

lcm = dfcm["Name of municipality[a]"]

for i in range(0, len(lcm)):
    lcm[i] = f"Município de {lcm[i]}"

#Setup Firefox on Linux
browser = webdriver.Firefox()
#browser.set_context("chrome")

tempo = 1.5

empresa_extraida = 0

start = time.time()

for empresa in lcm:

    print(empresa)

    # Pesquisar empresa no Código Postal

    browser.get("https://codigopostal.ciberforma.pt/")

    search = browser.find_element_by_xpath("//*[@id='autocomplete-ajax']")
    search.send_keys(empresa)
    search.send_keys(Keys.RETURN)

    time.sleep(tempo)

    # Página de Pesquisa

    content = browser.page_source

    soup = BeautifulSoup(content)

    # Procurar Erro
    #empresa_search = soup.find("div", attrs={"class": "gs-snippet"})

    # Procurar Pesquisa com Sucesso
    pesquisa = soup.find("a", attrs={"class": "gs-title"}, href=True)

    # Se existir empresa em BD
    if pesquisa is not None:

        try:

            time.sleep(tempo)

            element = browser.find_element_by_xpath("/html/body/div[3]/div[2]/div/div/div[1]/div/div/div[2]/div/div/div/div/div[5]/div[2]/div/div/div[1]/div[1]/div[1]/div[1]/div/a")

            #Click on Element
            actions = webdriver.ActionChains(browser)
            actions.move_to_element(element)
            actions.click(element)
            actions.perform()

            # Entrar na página da empresa dentro do Código Postal

            pesquisa_link = webdriver.current_url

            site = requests.get(pesquisa_link)

            site = site.content.decode('ISO-8859-1')

            soup = BeautifulSoup(site)

            print(f"Entramos na página de {empresa} dentro do 'Código Postal'")

            time.sleep(tempo)


        except:
            print("Pronto já houve um erro")

