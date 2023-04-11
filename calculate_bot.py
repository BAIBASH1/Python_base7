import os
import ptbot
from pytimeparse import parse
from dotenv import load_dotenv


def parse_time_and_create_countdown(chat_id, question, bot):
    time = parse(question)
    chart = render_progressbar(time, 0)
    message = "Таймер запущен"
    message_id = bot.send_message(chat_id, message)
    bot.create_countdown(
        time,
        notify_progress,
        chat_id=chat_id,
        time=time,
        bot=bot,
        message_id=message_id
    )
    bot.create_timer(time, bot.send_message, chat_id=chat_id, message='Время вышло')


def notify_progress(secs_left, chat_id, time, bot, message_id):
    message = f"Осталось секунд: {secs_left}"
    chart = render_progressbar(time, time - secs_left)
    bot.update_message(chat_id, message_id, f'{message}\n{chart}')


def render_progressbar(total, iteration, prefix='', suffix='',
                       length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def main():
    load_dotenv()
    tg_token = os.environ['TG_TOKEN']
    bot = ptbot.Bot(tg_token)
    bot.reply_on_message(parse_time_and_create_countdown, bot=bot)
    bot.run_bot()


if __name__ == '__main__':
    main()
