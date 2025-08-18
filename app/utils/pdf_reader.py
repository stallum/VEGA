import os
from PyPDF2 import PdfReader

class PDF:
    def __init__(self):
        pass
        

    def pdfReader(self, pdf='./_pdf/TeoriaDosGrafos.pdf'):
        self.pdf = PdfReader(f'{pdf}')
        self.page = self.pdf.pages[0]
        print(self.page.extract_text())
    



        
if __name__ == '__main__':
    pdf = PDF()
    pdf.pdfReader()