'''Code based on fullstackpython
https://www.fullstackpython.com/blog/build-first-slack-bot-python.html
and Pybites https://github.com/pybites/slackbot
to help set up the bot.

'''

import time
import logging
import string
from slackclient import SlackClient

# Commands
from commands.hello import COMMANDS_HELLO
from commands.roll import COMMANDS_ROLL


# ¯\_(ツ)_/¯

logging.basicConfig(level=logging.DEBUG)

# Constants
# SLACK_BOT_TOKEN is stored in a c file to keep it out of version control.
SLACK_BOT_TOKEN = open('Bot User OAuth Access Token.c').read()
BOT_ID = 'U8HGESKV0'    # Can be retrieved by clicking on the bot in Slack
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"

# Create an instance of the Slack client
slack_client = SlackClient(SLACK_BOT_TOKEN)


############

def command_help(sender, args=None):
    '''
    :param sender: The sender, which is force-fed to the function when it is
    called by handle_command(). Does nothing with it.
    :param args: Any text after the word 'help'. Likewise, args are force-fed to
    the function when it is called by handle_command(). Does nothing with them.
    :return: Outputs a list of valid commands.
    '''
    response = ("Use the syntax: '{} *command*' so that I know you're talking to "
                "me!\n Here is a list of commands I know how to respond to:"
                "\n").format(AT_BOT)
    # Append the list of commands. Crop out brackets
    response += str(sorted(COMMANDS))[1:-1]
    return response

#################

# Commands are kept in the commands subfolder. When a new command is added, the
# dictionary here is updated. The key is the text that the user types to call
# the command; the value is the function that will be executed.
COMMANDS = {'help': command_help}
COMMANDS.update(COMMANDS_HELLO)
COMMANDS.update(COMMANDS_ROLL)

#################

def handle_command(text, channel, sender):
    '''
    **Important note** - This function converts punctuation to spaces instead of
    concatenating. I'm not sure if this will break the code at some later time.

    :param text:  A text string containing a command directed at the bot
    :param channel: A string containing the channel that the command was given
    from.
    :return: If command is a valid command, execute that command. If not,
    display a message that the command is not valid.
    '''
    # Convert punctuation to spaces and separate words into additional arguments
    parsed = text.translate(
        text.maketrans(string.punctuation,
                       ' ' * len(string.punctuation))).split()
    command, args = parsed[0], parsed[1:]

    # Retrieve info on the sender, extract display name

    if command in COMMANDS:
        if args: response = COMMANDS[command](sender, args)
        else: response = COMMANDS[command](sender,)
    else:
        response = ("(´･_･`) Sorry <@{}>... No one ever taught me how to answer that."
                    "\n (use {} a list for available "
                    "commands)".format(sender, "*help*"))

    slack_client.api_call('chat.postMessage', channel=channel,
                          text=response, as_user=True)


def parse_slack_output(events):
    '''
    Parses slack events for direct mentions of the bot.

    :param events: An event is anything remotely interesting that happens in
    Slack. Messages, user status changes, and users typing are all events. Each
    event is stored as a dictionary and the events are stored in a list. Certain
    elements of the event can be extracted using dict functionality.

    :return: If an event directly mentions the bot (ignoring self-mentions by
    the bot), return the command, channel and user that sent the command.
    Otherwise return None for all.

    '''
    if events and len(events) > 0:
        logging.debug('event in parse_slack_output(): ' + str(events))
        for event in events:
            # Parse events that contain text mentioning the bot.
            if event and 'text' in event and AT_BOT in event['text']:
                # return text after the @ mention, whitespace removed
                text = event['text'].split(AT_BOT)[1].strip().lower()
                channel = event['channel']
                # Don't evaluate if bot calls its own name
                if event['user'] == BOT_ID: break

                # Retrieve sender's display name
                user = slack_client.api_call('users.info', user=event['user'])
                sender = user['user']['name']
                logging.debug('text, channel, user parse_slack_output(): '
                              '{}, {}, {}'.format(text, channel, sender))
                return text, channel, sender
    return None, None, None


def slack_bot(read_delay=2):
    '''
    Initializes the bot. Once initialized, the bot will run through an infinite
    loop where it will check all slack events for messages that are directed at
    it (via parse_slack_output). Any direct messages are passed to
    handle_command, which will attempt to execute the command.
    :param read_delay: Implements a 1 second delay between each loop of of the
    function to prevent CPU overload.
    :return: If the bot successfully connects, it will display a success
    message. If it fails, display a failure message. Outputs from handle_command
    are posted directly to Slack.
    '''
     # 1 second delay between reading

    if slack_client.rtm_connect():
        print("BBbot is connected and running!")
        # Command below can be used to retrieve ID
        logging.debug('Bot ID: ' + slack_client.api_call('auth.test')['user_id'])
        BOT_ID = slack_client.api_call('auth.test')['user_id']
        while True:
            command, channel, user = parse_slack_output(slack_client.rtm_read())
            if command and channel and user:
                handle_command(command, channel, user)
            time.sleep(read_delay)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")


if __name__ == "__main__":
    slack_bot()