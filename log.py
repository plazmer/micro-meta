import logging
import sys

logger = logging.getLogger('micro-meta')
logger.setLevel(logging.DEBUG)
fh = logging.StreamHandler(sys.stdout)
fh.setLevel(logging.DEBUG)

logger.addHandler(fh)

logger.debug('test')
logger.info('test')