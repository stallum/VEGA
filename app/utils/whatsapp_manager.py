import os
from time import sleep
import re

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class WhatsWeb:

    def __init__(self):
        self.dir_path = os.getcwd()
        self.downloads = os.path.join(self.dir_path, "_downloads_whats")
        self.last_src = ''

        self.options = webdriver.ChromeOptions()
        profile = os.path.join(self.dir_path, "profile", "wpp")
        self.options.add_argument(r"user-data-dir={}".format(profile))
        # self.options.add_argument("--headless=new") # faz com que o chrome abra sem interface
        
        self.webdriver = webdriver.Chrome(options=self.options)
        self.webdriver.get("https://web.whatsapp.com")

        # sleep configurado apenas para ler o QRCode.
        # sleep(10)
    
    def buscarConversas(self):
        """ Essa função encontra o chat do assistente """
        try:
            print('Buscando conversa...')
            WebDriverWait(self.webdriver, timeout=10)\
                .until(EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Caixa de texto de pesquisa"]')))

            print('Achou a conversa')
            caixa_de_pesquisa = self.webdriver.find_element(By.XPATH, (
                    '//div[@aria-label="Caixa de texto de pesquisa"]'
                ))
            caixa_de_pesquisa.click()
            caixa_de_pesquisa.send_keys('V.E.G.A.')
            sleep(2)
            contato = self.webdriver.find_element(By.XPATH, '//*[@title="V.E.G.A."]')
            contato.click()
            print('Conversa aberta!')
        except Exception as e:
            print(f'Erro ao buscar conver: {e}')
            raise e
    
    def verificarLermais(self):
        """ Essa função verifica se há o botão "Ler Mais" na ultima conversa """
        print('Buscando "ler mais"...')
        readMore = self.webdriver.find_element(By.CLASS_NAME, 'read-more-button')
        if readMore:
            print('"Ler mais" encontrado...')
            readMore.click()
        else:
            print('Sem "Ler mais" por aqui.')
    
    def buscarTexto(self, post):
        """ Essa função copia o texto encontrado na ultima mensagem """
        try: 
            self.verificarLermais()
            texto = post[-1].find_element(By.CLASS_NAME, "copyable-text").get_attribute("textContent")
            
        except Exception as e: 
            texto = None
            print(e)
        return texto
    
    def ultima_msg(self):
        """Essa Função captura a ultima mensagem da conversa"""
        print('verificando mensagem!')
        post = self.webdriver.find_elements(By.CLASS_NAME, 'message-out')
        
        print(post)
        msg = self.buscarTexto(post)
        print(msg)
        if msg: 
            print('Mensagem encontrada.')
            return msg
        else:
            print('Mensagem não encontrada.')
            msg = None
            return msg



if __name__ == "__main__":
    whats = WhatsWeb()
    whats.buscarConversas()
    msg = ''
    last_msg = '/quit'
    
    while msg != '/quit':
        sleep(5)
        msg = whats.ultima_msg()
        if msg != last_msg and msg:
            print(f"Mensagem recebida: {msg}")
            msg, last_msg = last_msg, msg
        print(msg)
