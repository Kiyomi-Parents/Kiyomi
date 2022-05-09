import os
from datetime import datetime

from termcolor import colored


class Logger:
    @staticmethod
    def log_init():
        if os.path.isfile("log.txt"):
            try:
                os.rename("log.txt", "prev_log.txt")
            except FileExistsError:
                os.remove("prev_log.txt")
                os.rename("log.txt", "prev_log.txt")

    @staticmethod
    def get_timestamp():
        return f"{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}"

    @staticmethod
    def log_file(msg):
        with open("log.txt", "a", encoding="utf-8") as file:
            file.write("\n" + msg)

    @staticmethod
    def log_add(msg):
        timestamp = Logger.get_timestamp()
        final_msg = f"{timestamp} | {msg}"

        print(final_msg)
        Logger.log_file(final_msg)

    @staticmethod
    def log(tag, msg):
        timestamp = Logger.get_timestamp()
        tag_with_color = colored(f"[{tag}]", "green")
        final_msg = f"{timestamp} | {tag_with_color} {msg}"

        print(final_msg)
        Logger.log_file(final_msg)

    @staticmethod
    def error(tag: str, msg: str):
        timestamp = Logger.get_timestamp()
        tag_with_color = colored(f"[{tag}]", "red")
        final_msg = f"{timestamp} | {tag_with_color} {msg}"

        print(final_msg)
        Logger.log_file(final_msg)

    @staticmethod
    def warn(tag: str, msg: str):
        timestamp = Logger.get_timestamp()
        tag_with_color = colored(f"[{tag}]", "yellow")
        final_msg = f"{timestamp} | {tag_with_color} {msg}"

        print(final_msg)
        Logger.log_file(final_msg)
