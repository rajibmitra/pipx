from contextlib import contextmanager
import sys
from typing import Dict
from threading import Thread
from time import sleep
import asyncio


class AsyncAnimate:
    def __init__(self, *args, **kwargs):
        pass

    async def __aenter__(self):
        self.task = asyncio.ensure_future(aanimate())
        print("entering")
        await asyncio.wait([self.task])

    async def __aexit__(self, exc_type, exc, tb):
        print("exiting")
        self.task.cancel()


async def aanimate():
    while True:
        print("waiting")
        await asyncio.sleep(0.2)
        print("waiting...")
        await asyncio.sleep(0.2)


@contextmanager
def animate(message: str, do_animation: bool):
    max_width = len(message) + 3
    spaces = " " * max_width
    clear_line_str = f"\r{spaces}\r"
    animate = {
        "do_animation": do_animation,
        "message": message,
        "clear_line_str": clear_line_str,
    }
    t = Thread(target=print_animation, args=(animate,))
    t.start()
    try:
        yield
    finally:
        sys.stderr.write(clear_line_str + message + "\r")
        t.join(0)
        animate["do_animation"] = False


def print_animation(meta: Dict[str, bool]):
    if not sys.stderr.isatty():
        return

    cur = "."
    sleep(0)
    while meta["do_animation"]:
        if cur == "":
            cur = "."
        elif cur == ".":
            cur = ".."
        elif cur == "..":
            cur = "..."
        else:
            cur = ""
        if not meta["do_animation"]:
            break
        message = f"{meta['message']}{cur}"
        sys.stderr.write(meta["clear_line_str"] + message + "\r")
        sleep(2)
    sys.stderr.write(meta["clear_line_str"])
