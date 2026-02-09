"""
    Primeiro código com selenium
    @author: AC Pedrosa - 22/01/2026
"""
from selenium.webdriver import Chrome
from time import sleep

#Para iniciar uma sessão é necessaŕio criar uma instancia do webdriver indicando o brownser a ser utilizado para o teste
driver = Chrome()

url = "https://scratch.mit.edu/"

#Para acessar a página do navegador utilizado a função .get() seguido da url entre os parênteses
driver.get(url)

sleep(3)

driver.find_element_by_class_name('intro-button create-button button')

#Para solicitar uma informação do navegador utilize o nome do atributo que precisa
title = driver.title

#Uns dos desafios no selenium é a espera para acessar um elemento que não está na página, dessa forma, é melhor esperar um tempo para acessar o elemento
driver.implicitly_wait(0.5)

driver.quit()