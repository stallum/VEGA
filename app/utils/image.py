
from PIL import Image
from io import BytesIO
import base64

from langchain_google_genai import GoogleGenerativeAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

llm = GoogleGenerativeAI(model="gemini-2.5-flash-lite")

class ProcessImage():
    def analysis(self, image_path): 
        """
        Analisa imagem, e descreve detalhadamente seu conteudo.
        Caso ela possua textos, transcreve em formato markdown.
        """
        
        image = Image.open(image_path)
        buffer = BytesIO()
        image.save(buffer, format="jpeg")
        img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")

        input = [
            [HumanMessage(
                content=[
                    {
                        'type': 'text',
                        'text': """
                        Analise a imagem, e descreva detalhadamente seu conteudo.
                        Caso ela possua textos, transcreva-os em formato markdown.
                        """
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpg;base64,{img_str}"
                        }
                    }
                ]
            )],
        ]


        analise_imagem = llm.invoke(input[0])
        return analise_imagem
 
if __name__ == '__main__':
    img = ProcessImage()
    img_path = "../VEGA/test/img/download.jpg"
    analise_imagem = img.analysis(img_path)
    print(analise_imagem)