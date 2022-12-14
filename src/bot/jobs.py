from parsers import parse_olx
from redis import Redis
import pickle
from typing import Set
import telebot
import logging


def update_offers(bot: telebot.TeleBot, redis_instance: Redis, user_id: str, chat_id: str):
    logging.info('Starting of updating...')
    parsed_urls = parse_olx()
    serialized_sended_urls = redis_instance.hget(user_id, 'sended_urls')
    if serialized_sended_urls is None:
        raise ValueError(f'Don\'t have any sended offer for user {user_id}')
    sended_urls: Set[str] = pickle.loads(serialized_sended_urls)
    url_for_sending = parsed_urls.difference(sended_urls)

    if len(url_for_sending) > 0:
        bot.send_message(chat_id, 'New offers:')
        for url in url_for_sending:
            try:
                bot.send_message(chat_id, url)
                sended_urls = sended_urls.union({url})
            except Exception as e:
                logging.warning(f'Not sended url: {url}\n With error: {e}')

    else:
        bot.send_message(chat_id, 'Didn\'t find any new offers')

    redis_instance.hset(user_id, 'sended_urls', pickle.dumps(sended_urls))