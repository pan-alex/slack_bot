'''
This command is import into BBbot.py as a command that the Slack bot can
handle. When called by any of the keywords listed in `keys`, command_hi() will
be executed.
'''
import logging
import time

def command_remind(sender, args=None):
    '''
    :param sender: Person who sent the message
    :param args: Any other text in the message that was issued with the command.
    This is force-fed to the function when called by handle_command(). This
    function does nothing with args.
    :return:
    '''
    logging.debug('command_hi() evaluated.')
    return 'Hi <@{}>!'.format(sender)


keys = ('hi', 'hello', 'hey', 'howdy', 'greetings', 'how',) #####################################
elements = [command_remind] * len(keys)
COMMANDS_HELLO = dict(zip(keys, elements))