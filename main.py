import trello_tools as tt
import logging
import logging.handlers

## quick function to move cards along the board when approved.

logger = logging.getLogger('moveAprovals')
logger.setLevel(logging.DEBUG)

fh = logging.handlers.RotatingFileHandler('C:\\repos\\slogan_maker\\automation.log', maxBytes=10240, backupCount=5)
fh.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)

logger.info('Started')
cards = tt.get_cards(tt.review_list)
for card in cards:
    if tt.get_card_approval(card) is True:
        card.change_list(str(tt.upload_list.id))
        logger.info('%s approved', card.name)
logger.info('Finished')
