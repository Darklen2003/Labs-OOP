import logging
import sys


class LoggingMixin:

    __slots__ = ()

    def _get_logger(self) -> logging.Logger:
        logger = logging.getLogger(self.__class__.__name__)
        if not logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            fmt = "[%(name)s] %(levelname)s: %(message)s"
            formatter = logging.Formatter(fmt)
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
            logger.propagate = True
        return logger

    def log(self, message: str) -> None:
        self._get_logger().info(message)

    def log_warning(self, message: str) -> None:
        self._get_logger().warning(message)

    def log_error(self, message: str) -> None:
        self._get_logger().error(message)
