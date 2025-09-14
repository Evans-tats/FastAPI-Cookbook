import logging
from uvicorn.logging import ColourizedFormatter
from logging.handlers import TimedRotatingFileHandler

client_logger = logging.getLogger("client_logger")
client_logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_formater = ColourizedFormatter(
    fmt="%(levelprefix)s %(asctime)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    use_colors=True,
)
console_handler.setFormatter(console_formater)
client_logger.addHandler(console_handler)

file_handler = TimedRotatingFileHandler("app.log")
file_formater = logging.Formatter("time: %(asctime)s | level: %(levelname)s | message: %(message)s"
                                   , datefmt="%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(file_formater)
client_logger.addHandler(file_handler)