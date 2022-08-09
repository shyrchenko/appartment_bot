import telebot
from redis import Redis
import pickle
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from parsers import parse_url
from jobs import update_offers

scheduler = BackgroundScheduler()

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s\n')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)\

logging.getLogger('apscheduler').setLevel(logging.DEBUG)

redis_instance = Redis('cache')

API_TOKEN = '1101957006:AAHfjfmZWxYT-Fk5l1pOLR1PadBInI_oDOI'
bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id: str = message.from_user.id
    chat_id: str = message.chat.id
    parsed_urls = parse_url()

    bot.reply_to(message, 'I will help you with finding new apartments')
    sended_urls = set()
    url_for_sending = parsed_urls
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

    scheduler.add_job(
        func=update_offers,
        trigger=IntervalTrigger(minutes=30),
        kwargs={
            'bot': bot,
            'redis_instance': redis_instance,
            'user_id': user_id,
            'chat_id': chat_id
        }
    )


if __name__ == '__main__':
    scheduler.start()
    bot.infinity_polling()
