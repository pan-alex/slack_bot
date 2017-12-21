'''
This command is import into BBbot.py as a commannd that the Slack bot can
handle. When called by any of the keywords listed in `keys`, command_hi() will
be executed.
'''
import logging


def command_hi(sender, *args):
    logging.debug('command_hi() evaluated.')
    return 'Hi <@{}>!'.format(sender)


keys = ('hi', 'hello', 'hey', 'howdy', 'greetings', 'how',) #####################################
elements = [command_hi] * len(keys)
COMMANDS_HELLO = dict(zip(keys, elements))