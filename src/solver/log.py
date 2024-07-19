from rich.console import Console
from rich.highlighter import NullHighlighter
from rich.logging import RichHandler
import logging

def get_logger(name:str, from_pytest: bool = False):
    log = logging.getLogger(name)
    if from_pytest:
        while log.handlers:
            log.removeHandler(log.handlers[0])
        log.propagate = False

    log.addHandler(
        RichHandler(
            show_time=False,
            highlighter=NullHighlighter(),
            console=Console(stderr=True),
            show_path=True,
            show_level=True,
        )
    )
    log.setLevel(logging.DEBUG)
    return log

