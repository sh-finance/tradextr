import logging

logger = logging.getLogger()

logger.setLevel(logging.DEBUG)

handler = logging.FileHandler('app.log')

# formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')

# handler.setFormatter(formatter)

logger.addHandler(handler)
