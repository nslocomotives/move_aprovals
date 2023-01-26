"""Main module."""
import logging
import logging.handlers
import base64
import ast

import trello_tools as tt

## quick function to move cards along the board when approved.

logger = logging.getLogger('moveAprovals')
logger.setLevel(logging.DEBUG)

LOGFILE = 'C:\\repos\\slogan_maker\\automation.log'
fh = logging.handlers.RotatingFileHandler(LOGFILE, maxBytes=10240, backupCount=5)
fh.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)

logger.info('Started')

#defining variables
BOARD_NAME = 'Redbubble Process Board'
LIST_NAME = 'in progress'
IDEAS_LIST_NAME = 'Phrase ideas'
REVIEW_LIST_NAME = 'Review'
UPLOAD_LIST_NAME = 'Ready to upload'
PARKED_LIST_NAME = 'Parked'
PUBLISHED_LIST_NAME = 'Published'
CHECKLIST_NAME = 'automation'
ITEM = 'generate tags'

#def get_secret(secret_name):
#    """ A wrapper for the secret variable assignement to perform a get"""
#    response = ''
#    response = assign_secret_variable(secret_name)
#    return response

def unpack_data(data):
    """Function to unpack data from its encoded form"""
    result = ""
    result = base64.b64decode(data).decode('utf-8')
    # TODO: what is this eval doing?  there should be a better way to do this in python. # pylint: disable=W0511
    result = ast.literal_eval(result) #pylint disable:W0123
    return result

board = tt.get_board(BOARD_NAME)
our_list = tt.get_list(board, LIST_NAME)
review_list = tt.get_list(board, REVIEW_LIST_NAME)
upload_list = tt.get_list(board, UPLOAD_LIST_NAME)
parked_list = tt.get_list(board, PARKED_LIST_NAME)
published_list = tt.get_list(board, PUBLISHED_LIST_NAME)
ideas_list = tt.get_list(board, IDEAS_LIST_NAME)
labels = tt.get_labels(board)

def get_card(card_id):
    """Function to get all the data on the card."""
    card = ''
    card = tt.get_cards(card_id)
    return card

def get_card_approval(card):
    """A function to get the just the aproval status of a card."""
    aproval = tt.get_card_approval(card)
    # aproval = False
    return aproval

def update_list(card, lista):
    """A function to update the list of cards."""
    response = card.change_list(lista)
    return response

def move_approval(event, context):
    """Fucntion called by google cloud message """
    message = ''
    if 'data' in event:
        data = unpack_data(event['data'])
    else:
        data = False
        message = r"No data passed in event consumed, "
        message = message + r"please check the producer is sending event[\'data\'\]"
        logger.info(message)
        return message
    card_id = ''
    card = get_card(card_id)
    aproval = get_card_approval(card)
    if aproval is True:
        update_list(card, list)

    logger.info(" [x] Received %s | %s", data, context)

    # TODO: need to understand what this bt was for and why...

    #recipiants = data['recipiants']
    #payload = build_payload(data['alert'])
    #for recipiant in recipiants:
    #    logger.info('texting %s : %s', recipiant, payload['alert'])
    #    result = send_text(recipiant, payload)
    #    logger.debug(result)
    logger.info(" [x] Done")

    if tt.get_card_approval(card) is True:
        card.change_list(str(upload_list.id))
        logger.info('%s approved', card.name)
    return message
logger.info('Finished')
