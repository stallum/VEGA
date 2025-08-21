import os
import re

from langchain_google_genai import GoogleGenerativeAI

from dotenv import load_dotenv
load_dotenv()

llm = GoogleGenerativeAI(model="gemini-2.5-flash-lite")

class Notas():
    @staticmethod
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
        
    @staticmethod
    def criarResumos(texto):
        """ Essa função cria resumos detalhados sobre o conteúdo entregue para a nota"""
        print('Criando Resumo do texto')
        resumo = llm.invoke(
            f'Resuma detalhadamente o texto:  \n{texto}\n'
            f'mantendo todas as informações importantes de forma estruturada'
            f'o Resumo deve conter todas as informações para que uma pessoa que não leu o texto orignal possa entender por completo'
            f'Faça para que seja possível ler, entender e estudar de maneira mais aprofundada quando quiser'
            f'O resultado final deve estar em português brasileiro e formatado em Markdown.'
        )
        return resumo
    
    @staticmethod
    def formatarNotar(tags, resumo):
        """Essa função formata os textos em uma unica nota com título, #tags, os resumos."""
        print('Formatando texto...')
        texto_final = (
            f'{tags}\n\n'
            f'## Resumo Detalhado\n{resumo}\n\n'
        )
        return texto_final
    
    @staticmethod
    def salvarNotas(transcricao_path, msg):
        """Essa função salva o texto em um arquivo de texto no diretório _notas."""
        print('Criando nota em arquivo')

        print(f'Processando a partir do caminho: {transcricao_path}')

        tags = Notas.criarTags(msg)
        resumo = Notas.criarResumos(msg)
        nota = Notas.formatarNotar(tags, resumo)
        print('Nota criada.\n\n')
        
        output_path = os.path.dirname(transcricao_path)
        output_path = output_path.replace('transcricoes', 'notas')

        base_name = os.path.splitext(os.path.basename(transcricao_path))[0]
        resumo_path = os.path.join(output_path, f'{base_name}.md')

        if not os.path.exists(output_path):
            os.makedirs(output_path)
            print(f"Criada pasta '_notas' em: {output_path}")
        
        with open(resumo_path, 'w', encoding='utf-8') as f:
            f.write(nota)
        print(f"Nota salva em: {resumo_path}")

if __name__ == '__main__':
    # Exemplo de como usar a classe Notas
    # Cria um arquivo de transcrição de teste
    test_dir = '_transcricoes_teste'
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
    
    caminho_teste = os.path.join(test_dir, 'nota_de_teste.txt')
    conteudo_teste = "A V.E.G.A. é uma assistente de IA projetada para otimizar tarefas diárias. Ela pode resumir textos, vídeos e áudios, e organizar informações de forma eficiente."

    with open(caminho_teste, 'w', encoding='utf-8') as f:
        f.write(conteudo_teste)

    # Chama a função para salvar a nota. A saída será salva em '_notas_teste/nota_de_teste.md'
    Notas.salvarNotas(caminho_teste, conteudo_teste)