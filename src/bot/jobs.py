from parsers import parse_url
import pickle
from typing import Set
import telebot
import logging


def update_offers(bot: telebot.TeleBot, user_id: str, chat_id: str):
    logging.info('Starting of updating...')
    parsed_urls = parse_url()
    try:
        with open(f'data/{user_id}', 'rb') as f:
            sended_urls = pickle.load(f)
    except Exception as e:
        raise ValueError(f'Don\'t have any sended offer for user {user_id}. Have error: {e}')
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

    with open(f'data/{user_id}', 'rb') as f:
        pickle.dump(sended_urls, f)
