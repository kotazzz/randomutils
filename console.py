import os
import random
import re
import shlex
import sys
import time


class Console:
    def __init__(self):
        os.system('')
        self.queue = []
        self.csi = {
            "0": "\033[0m",
            "red": "\033[31m",
            "green": "\033[32m",
            "yellow": "\033[33m",
            "blue": "\033[34m",
            "magenta": "\033[35m",
            "cyan": "\033[36m",
            "white": "\033[37m",
            "gray": "\033[90m",
            "b-red": "\033[41m",
            "b-green": "\033[42m",
            "b-yellow": "\033[43m",
            "b-blue": "\033[44m",
            "b-magenta": "\033[45m",
            "b-cyan": "\033[46m",
            "b-white": "\033[47m",
            "b-gray": "\033[100m",
            "bold": "\033[1m",
            "underline": "\033[4m",
            "blink": "\033[5m",
            "reverse": "\033[7m",
            "conceal": "\033[8m",
            "strike": "\033[9m",
            "overline": "\033[53m",
        }

    def prompt(self, prompt=1, checker=None):
        levels = {
            1: "[bold red]> [/]",
            2: "[bold yellow]>> [/]",
            3: "[bold green]>>> [/]",
            4: "[bold blue]>>>> [/]",
            5: "[bold magenta]>>>>> [/]",
        }
        checker = checker or (lambda x: True)
        while True:
            if not self.queue:
                data = input(self.format(levels.get(prompt, prompt)))
                data, *self.queue = shlex.split(data)
            else:
                data = self.queue.pop(0)
                self.print(
                    f"[blue][AUTO] {levels.get(prompt, prompt)} [bold blue underline]{data}[0]"
                )
            if data and checker(data):
                return data

    def format(self, text):
        # replace [red reverse] with \033[31m\033[7m
        text = re.sub(
            r"\[([a-z0-9 -]+)\]",
            lambda m: "".join(self.csi.get(i, "") for i in m.group(1).split()),
            text,
        )
        # replace [/] with \033[0m
        text = re.sub(r"\[\/\]", self.csi["0"], text)
        # replace [#123456] with \033[38;2;18;52;86m
        text = re.sub(
            r"\[#([0-9a-fA-F]{6})\]",
            lambda m: f"\033[38;2;{int(m.group(1)[:2], 16)};{int(m.group(1)[2:4], 16)};{int(m.group(1)[4:], 16)}m",
            text,
        )
        return text

    def print(
        self, *text, sep=" ", end="\n", min=0, max=None, format=True, convert_float=True
    ):
        text = [
            f"{i:.2f}" if convert_float and isinstance(i, float) else str(i)
            for i in text
        ]
        if format:
            text = [self.format(str(i)) for i in text]
        if min != 0:
            text = sep.join(text) + end
            for i in text:
                delay = random.uniform(min, max or min)
                sys.stdout.write(i)
                sys.stdout.flush()
                time.sleep(delay)
        else:
            print(*text, sep=sep, end=end, flush=True)