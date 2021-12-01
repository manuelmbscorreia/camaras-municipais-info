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

tempo = 5

empresa_extraida = 0

start = time.time()

for empresa in lcm:

    print(empresa)

    # Pesquisar empresa no Código Postal

    browser.get("https://codigopostal.ciberforma.pt/")

    search = browser.find_element(By.XPATH, "//*[@id='autocomplete-ajax']")
    search.send_keys(empresa)
    search.send_keys(Keys.RETURN)

    time.sleep(tempo)

    # Página de Pesquisa

    content = browser.page_source

    # Procurar Pesquisa com Sucesso
    pesquisa = browser.find_element(By.CSS_SELECTOR, "div.gsc-result:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > a:nth-child(1)")
    browser.execute_script("return arguments[0].scrollIntoView();", pesquisa)

    # Se existir empresa em BD
    if pesquisa is not None:

        try:

            print(f"Encontramos pesquisa de {empresa} dentro do 'Código Postal'")

            link = pesquisa.get_attribute("href")

            browser.get(link)

            time.sleep(tempo)

            print(f"Entramos na página de {empresa}.")

            elem_nome_municipio = browser.find_element(By.CSS_SELECTOR,"div.Ads-Details:nth-child(6) > div:nth-child(2) > div:nth-child(1) > h2:nth-child(1)")
            browser.execute_script("return arguments[0].scrollIntoView();", elem_nome_municipio)
            elem_nome_municipio = elem_nome_municipio.get_attribute("h2")


            elem_morada = browser.find_element(By.CSS_SELECTOR,"div.Ads-Details:nth-child(6) > div:nth-child(2) > div:nth-child(1) > h4:nth-child(2)")
            browser.execute_script("return arguments[0].scrollIntoView();", elem_morada)
            elem_morada = elem_morada.get_attribute("h4")


            elem_telefone = browser.find_element(By.CSS_SELECTOR,"div.Ads-Details:nth-child(6) > div:nth-child(2) > div:nth-child(1) > h4:nth-child(3) > span:nth-child(1)")
            browser.execute_script("return arguments[0].scrollIntoView();", elem_telefone)
            elem_telefone = elem_telefone.get_attribute("span")

            elem_email = browser.find_element(By.CSS_SELECTOR,"div.Ads-Details:nth-child(6) > div:nth-child(2) > div:nth-child(1) > h4:nth-child(5) > span:nth-child(1)")
            browser.execute_script("return arguments[0].scrollIntoView();", elem_email)
            elem_email = elem_email.get_attribute("span")

            elem_site = browser.find_element(By.CSS_SELECTOR,"div.Ads-Details:nth-child(6) > div:nth-child(2) > div:nth-child(1) > h4:nth-child(6) > span:nth-child(1) > a:nth-child(1)")
            browser.execute_script("return arguments[0].scrollIntoView();", elem_site)
            elem_site = elem_site.get_attribute("href")

            print(f"Extraimos dados da página de {empresa}.")

            time.sleep(tempo)


        except:

            #print("Pronto já houve um erro")

