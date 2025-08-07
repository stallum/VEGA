import re
import os
from pytube import YouTube

class YoutubeDownloader:
    def baixarVideo(self, link):
        try:
            print(f'Baixando vídeo do link: {link}')
            yt = YouTube(link)
            titulo = yt.title
            video = yt.streams.get_highest_resolution()

            output_path = '_videos'
            if not os.path.exists(output_path):
                os.makedirs(output_path)
                print(f'Pasta criada: {output_path}')
            
            title = re.sub(r'[<>:"/\\|?*]', '', titulo)
            title = title.replace("'", "")
            title = title.strip().replace(' ', '_')
            title = f'{title}.mp4'
            video_path = video.download(output_path, title)
            print(f"Baixado vídeo '{titulo}' para '{video_path}'")
            return video_path
        except Exception as e:
            print(f"Erro ao baixar vídeo: {e}")
            return None

if __name__ == '__main__':
    yt = YoutubeDownloader()
    link = 'https://youtu.be/VmRynpqImic?si=PPFEso3FWf_NMNT6'
    yt.baixarVideo(link)