import logging


class Logging:

    def __init__(self):
        self.logger = logging.getLogger()
        self.handler = logging.StreamHandler()
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def get_logger(self):
        self.logger.setLevel(logging.ERROR)
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)
        return self.logger