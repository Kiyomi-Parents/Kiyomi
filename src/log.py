from datetime import datetime
import os


class Logger:

    @staticmethod
    def log_init():
        if os.path.isfile('log.txt'):
            try:
                os.rename('log.txt', 'prev_log.txt')
            except FileExistsError:
                os.remove('prev_log.txt')
                os.rename('log.txt', 'prev_log.txt')

    @staticmethod
    def log_add(message):
        send_message = f'{datetime.utcnow()} {message}'
        print(send_message)
        with open('log.txt', 'a') as f:
            f.write("\n" + send_message)
