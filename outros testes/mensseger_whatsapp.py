from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
import time
import urllib.parse
import sys

# Variáveis de escopo global
WHATSAPP_WEB_URL = "https://web.whatsapp.com/"
TEMPO_ESPERA_LOGIN = 90
TEMPO_ESPERA_ENVIO = 20
TEMPO_ENTRE_MENSAGENS = 20

XPATH_CAMPO_MENSAGEM = '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div/div[3]/div[1]/p' #xpath - indica o campo de escrita da mensagem


def obter_mensagem_padrao():
    """
        Função para obter a mensagem que será enviada, retorna uma string
    """
    return (
        "*Você foi selecionado(a) para participar do (Nome do projeto)*\n\n"
        "Prezados Responsáveis,\n\n"
        "Dados do projeto "
        "*Sobre o Projto:* \n\n"
        "*Próximos Passos:*\n\n"
        "Para receber mais informações, pedimos que você entre no nosso grupo oficial de WhatsApp:\n\n"
        "👉 https://chat.whatsapp.com/SEU_LINK\n\n"
        "Atenciosamente,\n\n"
        "Equipe do Projeto"
    )


def carregar_contatos_planilha(caminho_arquivo: str) -> pd.DataFrame:
    try:
        df_contatos = pd.read_excel(caminho_arquivo)
        return df_contatos
    except Exception as e:
        print(f"Erro ao carregar o arquivo: {e}")
        sys.exit(1)

def iniciar_navegador() -> webdriver.Chrome: #retorna um objeto chrome do webdriver
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    service = Service(ChromeDriverManager().install())
    navegador = webdriver.Chrome(service=service, options=chrome_options)

    navegador.get(WHATSAPP_WEB_URL)
    return navegador


def aguardar_login(navegador: webdriver.Chrome):
    try:
        WebDriverWait(navegador, TEMPO_ESPERA_LOGIN).until(
            EC.presence_of_element_located((By.ID, "side"))
        )
        print("WhatsApp foi carregado")
    except TimeoutException:
        print("Tempo esgotado, reinicie")
        navegador.quit()
        sys.exit(1)


def enviar_mensagem(navegador: webdriver.Chrome, numero: str, mensagem: str):
    texto_codificado = urllib.parse.quote(mensagem)
    link = f"https://web.whatsapp.com/send?phone={numero}&text={texto_codificado}"
    navegador.get(link)

    try:
        campo_mensagem = WebDriverWait(navegador, TEMPO_ESPERA_ENVIO).until(
            EC.presence_of_element_located((By.XPATH, XPATH_CAMPO_MENSAGEM))
        )
        time.sleep(5)
        campo_mensagem.click()
        campo_mensagem.send_keys(Keys.ENTER)
        print(f"Mensagem enviada para {numero}")
    except Exception as e:
        print(f"Erro ao enviar mensagem para {numero}: {e}")


def main():
    contatos = carregar_contatos_planilha("nome_arquivo.xlsx")
    mensagem = obter_mensagem_padrao()
    navegador = iniciar_navegador()

    aguardar_login(navegador)

    for _, linha in contatos.iterrows():
        numero = linha["Telefone do Responsável:"]
        enviar_mensagem(navegador, numero, mensagem)
        time.sleep(TEMPO_ENTRE_MENSAGENS)


if __name__ == "__main__":
    main()

# Contatos no dicionário para teste
#contatos_df = pd.DataFrame({
#    'Pessoa': ['01', '02', '03', '04', '05', '06'],
#    'Contato': ['559999999999', '559999999999', '559999999999', '559999999999', '559999999999', '559999999999']
#})
  

