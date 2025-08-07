import os
import re

from langchain_google_genai import GoogleGenerativeAI

from dotenv import load_dotenv
load_dotenv()

llm = GoogleGenerativeAI(model="gemini-2.5-flash-lite")

class Notas():
    def criarTags(texto):
        """ Essa função tem o objetivo de criar as tags da nota """
        print('Criando as Tags')
        tags = llm.invoke(
            f'Crie até 10 tags referentes a este texto: \n{texto}\n'
            f'Voce deve responder apenas as tags, sem nenhum comentario, nem numeração'
            f'as tags devem estar alinhadas em uma unica linha, separadas por um espaço'
            f'Elas devem ser relacionadas apenas ao conteudo do texto'
            f'por exemplo, um texto que fale sobre filosofia pode ter a tag #filosofia'
            f'outro exemplo, um texto que fale sobre treino de academia pode ter as tags #fitness #health'
            f'todas a tags devem ter # na frente, por exemplo: #exemplo'
        )
        return tags
        
    def criarResumos(texto):
        """ Essa função cria resumos detalhados sobre o conteúdo entregue para a nota"""
        print('Criando Resumo do texto')
        resumo = llm.invoke(
            f'Resuma detalhadamente o texto:  \n{texto}\n'
            f'mantendo todas as informações importantes de forma estruturada'
            f'o Resumo deve conter todas as informações para que uma pessoa que não leu o texto orignal possa entender por completo'
            f'O resultado final deve estar em português brasileiro e formatado em Markdown.'
        )
        return resumo
    
    def formatarNotar(tags, resumo):
        """Essa função formata os textos em uma unica nota com título, #tags, os resumos."""
        print('Formatando texto...')
        texto_final = (
            f'{tags}\n\n'
            f'## Resumo Detalhado\n{resumo}\n\n'
        )
        return texto_final
    
    def salvarNotas(transcricao_path):
        """Essa função salva o texto em um arquivo de texto no diretório _notas."""
        print('Criando nota em arquivo')

        transcricao_path = transcricao_path.replace("'", "")
        print(f'1transcricao_path {transcricao_path}')

        with open(transcricao_path, 'rb') as file:
            transcricao = file.read()
            tags = Notas.criarTags(transcricao)
            resumo = Notas.criarResumos(transcricao)
            nota = Notas.formatarNotar(tags, resumo)
            print('Nota criada.\n\n')
        
        output_path = os.path.dirname(transcricao_path)
        output_path = output_path.replace('transcricoes', 'notas')

        base_name = os.path.splitext(os.path.basename(transcricao_path))[0]
        resumo_path = f'{output_path}/{base_name}.md'

        if not os.path.exists(output_path):
            os.makedirs(output_path)
            print(f"Criada pasta '_notas' em: {output_path}")
        
        with open(resumo_path, 'w') as f:
            f.write(nota)
        print(f"Nota salva em: {resumo_path}")

if __name__ == '__main__':
    transcricao_path =  'C:/Users/stall/Documents/programacao/projetos/VEGA/txt.txt'
    Notas.salvarNotas(transcricao_path)