
# tweepy-bots/bots/config.py
import tweepy
import logging
import os
import time
import webbrowser
import pyautogui
from PIL import Image

NOMBRE_FICHERO = 'patata.png'
RESULTADO_FICHERO = 'patata2.png'


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def create_api():
    consumer_key = "----"
    consumer_secret = "----"
    access_token = "----"
    access_token_secret = "----"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True,
        wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api

def capturarImagen(tweet_citado_id):
    COORD_X = 600
    COORD_Y = 170
    ANCHURA = 1190 - COORD_X
    ALTURA = 1010 - COORD_Y

    COLOR_CUT = (235, 238, 240, 255)
    # Abre browser
    webbrowser.open("https://twitter.com/cosminpm/status/" + str(tweet_citado_id))
    
    time.sleep(5)
    img = pyautogui.screenshot(region=(COORD_X, COORD_Y, ANCHURA, ALTURA))
    img.save(NOMBRE_FICHERO)
    #Recortar imagen
    captura = Image.open(NOMBRE_FICHERO).convert('RGBA')
    cols, rows = captura.size
    recorte_y = rows
    print(cols, rows)
    for row in range(0, rows):
        #print(row)
        print(captura.getpixel((0, row)))
        if (captura.getpixel((0,row)) == COLOR_CUT):
            recorte_y = row
            break
    print(str(captura.size), ANCHURA, ALTURA - recorte_y)
    captura.crop((0, 0, ANCHURA, recorte_y)).save(RESULTADO_FICHERO)
    # Cerrar browser
    os.system("taskkill /im chrome.exe /f")

def check_mentions(api, since_id):
    logger.info("Escribiendo tweets de respuestas a los usuarios")
    new_since_id = since_id
    # Recorre todos los tweets en los que se menciona cuya id sea la pasada como parametro
    for tweet in tweepy.Cursor(api.mentions_timeline, since_id = since_id).items():
        if tweet.in_reply_to_status_id is not None:
            # Obtiene id en string del tuit citado
            tweet_citado_id = api.get_status(tweet.in_reply_to_status_id).quoted_status_id
            capturarImagen(tweet_citado_id)
            respuesta = "@"+str(tweet.author.screen_name)
            api.update_with_media(RESULTADO_FICHERO, status=(respuesta), in_reply_to_status_id=tweet.id)
def main():
    TIME_WAITING = 60
    api = create_api()
    since_id = 1
    while True:
        # La id sirve para que aquellos tweets que se hayan mencionado no se vuelvan a mencionar
        since_od = check_mentions(api, since_id)
        logger.info("Esperando a que lleguen solicitudes")
        # Se tiene que hacer un sleep para que no se sobreesature las solicitudes de la API
        time.sleep(TIME_WAITING)

if __name__ == '__main__':
    main()


