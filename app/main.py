from time import sleep
import datetime

from langchain.agents import (
    AgentExecutor,
    create_tool_calling_agent
)

import os

from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompt_values import ChatPromptValue

from utils.whatsapp_manager import WhatsWeb
from utils.criar_notas import Notas

class VEGA:
    def __init__(self):
        self.llm = GoogleGenerativeAI(model="gemini-2.5-flash-lite")
        self.whats = WhatsWeb()
        self.notas = Notas()

    def processarMensagem(self, msg):
        """Essa função verifica a mensagem recebida e escolhe qual é a ferramenta correta para utilizar."""
        resultado = None
        executorPrompt = {
            "input": 
            f'identifique o tipo de arquivo da mensagem e siga as instruções.'
            f' - se for um link do youtube: sua resposta deve ser apenas a palavra "link"'
            f' - se for um arquivo mp4: sua resposta deve ser apenas a palavra "video"'
            f' - se for um arquivo mp3 ou ogg: sua resposta deve ser apenas a palavra "audio"'
            f' - se for um arquivo de imagem: descreva a imagem e seu conteudo e salve a nota a partir de sua transcrição'
            f'a mensagem é: {msg}'}
        
        resultado = resultado.invoke(executorPrompt)
        return resultado
    

if __name__ == '__main__':
    bot = VEGA()
    bot.whats.buscarConversas()
    output_path = '_notas'

    msg = ' '
    last_msg = '/quit'

    while msg != '/quit':
        output_path = '_msgs'
        path = datetime.date.today().strftime("%d-%m-%y_%H-%M-%S")
        msg_path = f"{output_path}/{path}.txt"

        msg = bot.whats.ultima_msg()
        print(f"Mensagem recebida: {msg}")
        last_msg, msg = msg, last_msg
        
        if not os.path.exists(output_path):
            os.makedirs(output_path)
            print(f'Criando pasta "_msgs" em: {output_path}')

        with open(msg_path, "w") as arquivo:
            arquivo.write(last_msg)

        try: 
            bot.notas.salvarNotas(msg_path, last_msg)
        except Exception as e:
            print(e)