import logging


logging.basicConfig(
    filename="utils\\misc\\bot.log",
    format=u'[%(asctime)s] #%(levelname)s %(filename)s [LINE:%(lineno)d] %(message)s',
    level=logging.INFO
)