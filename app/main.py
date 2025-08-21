from time import sleep
import datetime

import os

from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompt_values import ChatPromptValue

from utils.whatsapp_manager import WhatsWeb
from utils.criar_notas import Notas
from utils.image import ProcessImage

class VEGA:
    def __init__(self):
        self.llm = GoogleGenerativeAI(model="gemini-2.5-flash-lite")
        self.whats = WhatsWeb()
        self.notas = Notas()
        self.image = ProcessImage()
    
    def criarTitulo(self, msg):
        """Essa função cria os titulos ee caminhos para os arquivos de texto finais do programa"""
        title = self.llm.invoke(
            f'Crie um titulo de até três (3) palavras para o texto descrito na mensagem: {msg}'
            f'Esse título deve fazer sentido com todo o conteúdo do texto recebido e deve ser coeso.'
            f'Deve ser relacionado APENAS ao conteúdo do texto'
            f'Utilize apenas termos aceitos para nomear arquivos no computador, nada de Caracteres especiais'
        )
        return title
    

if __name__ == '__main__':
    bot = VEGA()
    bot.whats.buscarConversas()
    output_path = '_notas'

    msg = ' '
    last_msg = '/quit'

    while msg != '/quit':
        output_path = '_msgs'
        result = bot.whats.ultima_msg()

        msg = result
        print(f"Mensagem recebida: {msg}")
        last_msg, msg = msg, last_msg

        try:
            path = bot.criarTitulo(last_msg)
        except Exception as e:
            print(e)
        
        msg_path = f"{output_path}/{path}.txt"

        if not os.path.exists(output_path):
            os.makedirs(output_path)
            print(f'Criando pasta "_msgs" em: {output_path}')

        with open(msg_path, "w", encoding="utf-8") as arquivo:
            arquivo.write(last_msg)

        try: 
            bot.notas.salvarNotas(msg_path, last_msg)
        except Exception as e:
            print(e)