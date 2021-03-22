import logging
from tele_config import token
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from redvid import Downloader
import argparse

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    bot.send_message(chat_id=update.message.chat_id, text='Hi!')


def help(bot, update):
    """Send a message when the command /help is issued."""
    bot.send_message(chat_id=update.message.chat_id, text='Help!')


def echo(bot, update):
    """Echo the user message."""
    try:
        link = update.message.text
        reddit = Downloader()
        reddit.url = link
        reddit.path = ''
        reddit.overwrite = False
        reddit.max_q = True
        reddit.min_q = True
        reddit.max_d = 1e1000
        reddit.max_s = 1e1000
        reddit.auto_max = False
        reddit.proxies = {}
        path = reddit.download()
        # bot.send_message(chat_id=update.message.chat_id, text=update.message.text)
        bot.send_video(chat_id=update.message.chat_id, video=open(path, 'rb'), supports_streaming=True)
    except:
        bot.send_message(chat_id=update.message.chat_id, text="Failed")


def error(bot, update):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', bot, update.error)


def main():
    """Start the bot."""
    updater = Updater(token)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_error_handler(error)


    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()