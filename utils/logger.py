import logging

class Logger(object):
    logger = None
    
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(funcName)s:%(lineno)d:%(message)s')

        file_handler = logging.FileHandler('logs/error.log')
        file_handler.setLevel(logging.ERROR)
        file_handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)
    
    def exception(self, message):
        self.logger.exception(message)
        