from django.http import FileResponse
from django.shortcuts import render
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person
from matplotlib.pyplot import imshow
from PIL import Image, ImageFont, ImageDraw
import urllib

def index(request):
    return render(request, 'index.html')

def get_face_client():
    #variables
    SUBSCRIPTION_KEY = '20f7e5d4f2c94df3b0a52f4b6627d03f'
    ENDPOINT = 'https://projectoface.cognitiveservices.azure.com/'

    #creación
    credential = CognitiveServicesCredentials(SUBSCRIPTION_KEY)
    return FaceClient(ENDPOINT, credential)

def analizar(request):

    # variables
    age_result=""
    gender_result=""
    face_client = get_face_client()
    url = request.GET['imagen']
    urllib.request.urlretrieve(url, "python.jpg")
    img = Image.open("python.jpg")
    attributes = ["age", "gender", "emotion"]
    include_id = True
    include_landmarks = True
    detection_model=["detection_03"]
    detected_faces = face_client.face.detect_with_url(url, include_id, include_landmarks, attributes, raw=True)
    detected_faces.response.json()
    color="blue"
    font = ImageFont.truetype("/usr/share/fonts/truetype/ubuntu/Ubuntu-L.ttf", 20)

    # logica
    if detected_faces is not None:
        draw = ImageDraw.Draw(img)
    for currFace in detected_faces.response.json():
        faceRectangle = currFace['faceRectangle']
        left = faceRectangle['left']
        top = faceRectangle['top']
        width = faceRectangle['width']
        height = faceRectangle['height']
        draw.line([(left,top),(left+width,top)], fill=color, width=5)
        draw.line([(left+width,top),(left+width,top+height)], fill=color, width=5)
        draw.line([(left+width,top+height),(left,height+top)], fill=color, width=5)
        draw.line([(left,top+height),(left,top)], fill=color, width=5)
        edad = currFace ['faceAttributes']['age']
        genero = currFace ['faceAttributes']['gender']
        emocion = currFace ['faceAttributes']['emotion']
        #emociones
        anger = currFace ['faceAttributes']['emotion']['anger']
        contempt = currFace ['faceAttributes']['emotion']['contempt']
        disgust = currFace ['faceAttributes']['emotion']['disgust']
        fear = currFace ['faceAttributes']['emotion']['fear']
        happiness = currFace ['faceAttributes']['emotion']['happiness']
        neutral = currFace ['faceAttributes']['emotion']['neutral']
        sadness = currFace ['faceAttributes']['emotion']['sadness']
        surprise = currFace ['faceAttributes']['emotion']['surprise']

        if str(genero)=='female':
            genero = 'Femenino'
        else:
            genero = 'Masculino'
        draw.text((left, top+height), text = str('Edad: ' + str(edad)+'\n'+'Género: ' + str(genero)))
        texto = str('Edad: ' + str(edad)+'\n'+'Género: ' + str(genero) + '\n' + 'Emoción: ' + str(emocion))
        print(texto)

        #diccionario de emociones
        emociones_dict = {'enojo': anger, 'contento': contempt, 'disgusto': disgust, 'miedo': fear, 'felicidad': happiness, 'neutral': neutral, 'tristeza': sadness, 'sorpresa': surprise}
        emocion_final = max(emociones_dict, key=emociones_dict.get)
        print(emocion_final)

        #musica
        #switch
        if emocion_final == 'enojo':
            url_playlist = 'https://open.spotify.com/embed/playlist/2Pwo61TzNBeTMAtvuloSoL?utm_source=generator&theme=0'
        elif emocion_final == 'contento':
            url_playlist = 'https://open.spotify.com/embed/playlist/37i9dQZF1DX9XIFQuFvzM4?utm_source=generator&theme=0'
        elif emocion_final == 'disgusto':
            url_playlist = 'https://open.spotify.com/embed/playlist/37i9dQZF1DWYWddJiPzbvb?utm_source=generator&theme=0'
        elif emocion_final == 'miedo':
            url_playlist = 'https://open.spotify.com/embed/playlist/37i9dQZF1DX3Ogo9pFvBkY?utm_source=generator&theme=0'
        elif emocion_final == 'felicidad':
            url_playlist = 'https://open.spotify.com/embed/playlist/37i9dQZF1DWVovHcLREwOK?utm_source=generator&theme=0'
        elif emocion_final == 'neutral':
            url_playlist = 'https://open.spotify.com/embed/playlist/37i9dQZF1DX35X4JNyBWtb?utm_source=generator&theme=0'
        elif emocion_final == 'tristeza':
            url_playlist = 'https://open.spotify.com/embed/playlist/37i9dQZF1DWZqdNJSufucb?utm_source=generator&theme=0'
        elif emocion_final == 'sorpresa':
            url_playlist = 'https://open.spotify.com/embed/playlist/37i9dQZEVXbnHQUb1lTw1I?utm_source=generator&theme=0'
    img.show()
    

    return render(request, 'analizar.html', {'edad': edad, 'genero': genero, 'emocion': emocion_final, 'playlist': url_playlist, 'imagen': url})