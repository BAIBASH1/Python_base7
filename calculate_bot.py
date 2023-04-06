from dotenv import load_dotenv
import os
import ptbot
from pytimeparse import parse

load_dotenv()
TG_TOKEN = os.environ['TG_TOKEN']


def parse_time_and_create_countdown(chat_id, question, bot):
    time = parse(question)
    message = f"Осталось секунд: {time}"
    chart = render_progressbar(time, 0)
    message_id = bot.send_message(chat_id, f'{message}\n{chart}')
    bot.create_countdown(
        time,
        notify_progress,
        chat_id=chat_id,
        time=time,
        bot=bot,
        message_id=message_id
    )


def notify_progress(secs_left, chat_id, time, bot, message_id):
    message = f"Осталось секунд: {secs_left}"
    chart = render_progressbar(time, time - secs_left)
    bot.update_message(chat_id, message_id, f'{message}\n{chart}')
    if not secs_left:
        bot.send_message(chat_id, "Время вышло")


def render_progressbar(total, iteration, prefix='', suffix='',
                       length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def main():
    bot = ptbot.Bot(TG_TOKEN)
    bot.reply_on_message(parse_time_and_create_countdown, bot=bot)
    bot.run_bot()


if __name__ == '__main__':
    main()
