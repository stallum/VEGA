from time import sleep

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

class VEGA:
    def __init__(self):
        self.llm = GoogleGenerativeAI(model="gemini-2.5-flash-lite")
        self.whats = WhatsWeb()

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
    msg = ' '
    last_msg = '/quit'
    while msg != '/quit':
        msg = bot.whats.ultima_msg()
        print(f"Mensagem recebida: {msg}")
        last_msg, msg = msg, last_msg
        print(msg), print(last_msg)
        try: 
            resultado = bot.processarMensagem(last_msg)
            print(f"Resultado: {resultado}")
        except Exception as e:
            print(e)
    
"""
    def criar_agente(self):
        llm = GoogleGenerativeAI(model="gemini-2.5-flash-lite")
        
        prompt = ChatPromptValue([
            (
                "system",
"""
                # Você é um agente especializado em ajudar o usuário criar notas detalhadas e completas;
                # Você deve extrair as informações principais dos dados que são te entregues;
                # Sempre deve-se resumir as informações de maneira claras e concisas;
                # Mantenha o controle dos resultados das ferramentas e incorpore-os às notas conforme necessário;
                # O resultado final deve estar em português brasileiro e formatado em Markdown.
""" 
             ),
             ("placeholder", "{chat_history}"),
             ("human", "{input}"),
        ])

        return prompt
"""