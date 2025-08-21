import os
from PyPDF2 import PdfReader

class PDF:
    def __init__(self):
        pass
        

    def pdfReader(self, pdf):
        """ Função de extração dee texto do PDF"""

        output_path = '_msgs'
        msg_path = f"{output_path}/livro.txt"
        
        with open(pdf, 'rb') as arquivo:
            self.leitor = PdfReader(arquivo)
            texto = ''
            for pagina in self.leitor.pages:
                texto += pagina.extract_text()
                print(f'Pagina {texto}')
            
            
        with open(msg_path, 'w', encoding='utf-8') as f:
            f.write(texto)

        return texto
    
    



        
if __name__ == '__main__':
    pdf = PDF()
    texto = pdf.pdfReader(os.path.join(os.path.dirname(__file__), '..', '_pdf', 'Fundamentos matemáticos para a ciência da computação Matemática Discreta e Suas Aplicações (Judith L. Gersting).pdf'))

    print(texto)