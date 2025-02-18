import logging
import sys

from python_log_indenter import IndentedLoggerAdapter


class Narrator:
    """
    Allows Actors to narrate their actions through a logging.logger instance.

    Features:
        Can Indent logs for improved readability
    """

    def __init__(self, name: str = "Actor"):
        _logger = logging.getLogger(name)
        _logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter("[%(asctime)s] [%(name)s] %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        _logger.addHandler(handler)
        self.logger = IndentedLoggerAdapter(_logger)
        self.handler = None

    def add_indent(self) -> None:
        self.logger.add()

    def remove_indent(self) -> None:
        self.logger.sub()

    def __repr__(self):
        return self.__class__.__name__
