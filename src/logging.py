import logging

from pydantic import BaseModel, field_validator


class LogEndpointScheme(BaseModel):
    request_path: str
    request_method: str
    remote_ip: str
    response_status_code: int
    duration: int | str

    @field_validator('duration', mode='before')
    @classmethod
    def validate(cls, v: int):
        return f'{v} ms'


class LogDecoratorScheme(BaseModel):
    func_method_name: str
    duration: int | str

    @field_validator('duration', mode='before')
    @classmethod
    def validate(cls, v: int):
        return f'{v} ms'


class CustomFormatter(logging.Formatter):
    grey = '\x1b[38;20m'
    yellow = '\x1b[33;20m'
    red = '\x1b[31;20m'
    bold_red = '\x1b[31;1m'
    reset = '\x1b[0m'
    format = '%(asctime)s - %(message)s'

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomFormatter())
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)
logger.addHandler(ch)
