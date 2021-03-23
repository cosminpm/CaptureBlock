
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

def check_mentions(api):
    stat = "Esto es una prueba :)"
    api.update_status(status=stat)

def main():
    api = create_api()
    check_mentions(api)

if __name__ == '__main__':
    main()


