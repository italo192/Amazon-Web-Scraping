from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
from time import sleep

#codigo 
def iniciar_driver():
    chrome_options = Options()
    arguments = ['--lang=pt-BR','--window-size= 800,600','--incognito']
    for argument in arguments:
        chrome_options.add_argument(argument)
        
    chrome_options.add_experimental_option('prefs', {
        # Desabilitar a confirmação de download
        'download.prompt_for_download': False,
        # Desabilitar notificações
        'profile.default_content_setting_values.notifications': 2,
        # Permitir multiplos downloads
        'profile.default_content_setting_values.automatic_downloads': 1,

    })

    #inicializando o webdriver
    driver= webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=chrome_options)
    return driver
# base
driver = iniciar_driver()
# navegar ate o site
driver.get('https://www.amazon.com.br/s?k=xeon&__mk_pt_BR=ÅMÅŽÕÑ&crid=2TAN03PAUMI2O&sprefix=xeon%2Caps%2C505&ref=nb_sb_noss_1')
sleep(40)
while True:
    #rola a paina para baixo
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
    sleep(2)
    #rola a pagina para cima
    driver.execute_script('window.scrollTo(0,document.body.scrollTop);')
    sleep(2)
    # Encontra títulos
    titulos = driver.find_elements(By.XPATH, '//span[@class="a-size-base-plus a-color-base a-text-normal"]')
    #preços
    precos = driver.find_elements(By.XPATH, '//span[@class="a-color-base"]')
    # Encontra links
    links = driver.find_elements(By.XPATH, '//a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]')
    if titulos:
        print(f"{len(titulos)} elementos XPath encontrados com sucesso!")
    else:
        print('Nada encontrado')
    if precos:
        print(f"{len(precos)} elementos XPath encontrados com sucesso!")
    else:
        print('Nada encontrado')
    if links:
        print(f"{len(links)} elementos XPath encontrados com sucesso!")
    else:
        print('Nada encontrado')

    # criar o arquivo CSV para guarda os itens
    for titulo, preco, link in zip(titulos,precos,links):
        with open('precos.csv', 'a',encoding='utf-8',newline='') as arquivo:
            link_processado = link.get_attribute('href')
            arquivo.write(f'{titulo.text};{preco.text};{link_processado}{os.linesep}')
    
    # passa para a proxima pagina
    try:
        proxima_pagina = driver.find_element(By.XPATH,"//a[text()='Próximo']")
        sleep(2)
        proxima_pagina.click()
    except:
        print('última página')
        break    
         
input('')  
