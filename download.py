from flask import Flask, render_template, request
from pytube import YouTube
from moviepy.editor import *
import os, re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

#Limpar nome do arquivo de caracteres especiais
def limpar_nome_arquivo(nome_original):
    padrao = re.compile(r'[\\/:\*\?"<>\|]')
    novo_nome = re.sub(padrao, '', nome_original)
    return novo_nome

#Função de download
@app.route('/download', methods=['POST'])
def download():
    tipo = request.form['rbTipoDownload'] #Pegar o tipo de Download
    caminhoDownload = "" #Variável com caminho pra salvar
    url = request.form['url'] #Pegando a URL do vídeo
    if tipo == 'mp3': #Se o download for para MP3
        try:
            yt = YouTube(url)
            nome = yt.title #Nome do vídeo no YouTube
            novo_nome = limpar_nome_arquivo(nome) #Novo nome após retirar caracteres especiais
            audio = yt.streams.filter(only_audio=True).first() #Pegando somente o áudio do vídeo
            caminhoDownload = "downloads/audio" #Baixa o áudio para o diretório especificado
            caminhoAudio = f"{caminhoDownload}/audio_temp.webm" #Cria o arquivo temporário tipo WEBM
            audio.download(output_path=caminhoDownload, filename='audio_temp.webm') #Salva o arquivo na pasta "audio"
            audioVideo = AudioFileClip(caminhoAudio) 
            audioVideo.write_audiofile(f"{caminhoDownload}/{novo_nome}.mp3") #Converte o áudio de WEBM para MP3
            os.remove(caminhoAudio) #Apaga o audio em formato WEBM
            menssagem = "Download do áudio concluído!" #Mensagem de sucesso
        except Exception as e: #Em caso de erro
            caminhoAudio = f"{caminhoDownload}/audio_temp.webm" 
            os.remove(caminhoAudio) #Remove o áudio WEBM baixado
            menssagem = f"Ocorreu um erro: {e}" #Retorna a mensagem de erro
    else: #Caso não seja MP3
        try:
            yt = YouTube(url) 
            video = yt.streams.get_highest_resolution() #Pega a maior resolução disponível do vídeo
            caminhoDownload = "downloads/video" #Caminho de download
            video.download(caminhoDownload) #Baixa o vídeo no caminho indicado
            menssagem = "Download do vídeo concluído!" #Mensagem de sucesso
        except Exception as e: #Em caso de erro
            menssagem = f"Ocorreu um erro: {e}" #Mensagem de erro
    return render_template('index.html', message=menssagem) #Retorna o valor da variável 'mensagem', sendo sucesso ou o erro

#Funcao para abrir a pasta de downloads de audio
@app.route('/abrirAudio', methods=['POST'])
def abrirAudio():
    path = "downloads/audio" #Caminho da pasta [passível de alteração]
    path = os.path.realpath(path) #Pega o caminho de acordo com o SO
    os.startfile(path) #Abre a pasta
    return render_template('index.html') #Retorna para o início

#Funcao para abrir a pasta de downloads de video
@app.route('/abrirVideo', methods=['POST'])
def abrirVideo():
    path = "downloads/video" #Caminho da pasta [passível de alteração]
    path = os.path.realpath(path) #Pega o caminho de acordo com o SO
    os.startfile(path) #Abre a pasta
    return render_template('index.html') #Retorna para o início


if __name__ == '__main__':
    app.run(debug=True)
