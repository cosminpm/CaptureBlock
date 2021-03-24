
# tweepy-bots/bots/config.py
import tweepy
import logging
import os
import time

TIME_WAITING = 60

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

def check_mentions(api, since_id):
    logger.info("Escribiendo tweets de respuestas a los usuarios")
    new_since_id = since_id
    # Recorre todos los tweets en los que se menciona cuya id sea la pasada como parametro
    for tweet in tweepy.Cursor(api.mentions_timeline, since_id = since_id).items():
        #logger.info(tweet)
        logger.info(tweet.text)


def main():
    api = create_api()
    since_id = 1
    while True:
        # La id sirve para que aquellos tweets que se hayan mencionado no se vuelvan a mencionar
        since_od = check_mentions(api, since_id)
        logger.info("Esperando a que lleguen solicitudes")
        # Se tiene que hacer un sleep para que no se sobreesature las solicitudes de la API
        time.sleep(60)

if __name__ == '__main__':
    main()


