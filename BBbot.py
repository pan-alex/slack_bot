'''code from fullstackpython
https://www.fullstackpython.com/blog/build-first-slack-bot-python.html'''

import time
import logging
from slackclient import SlackClient

# ¯\_(ツ)_/¯

logging.basicConfig(
	level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
SLACK_BOT_TOKEN = open('Bot User OAuth Access Token.c').read()
BOT_ID = 'U8HGESKV0'    # Can be retrieved by clicking the bot in Slack
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"

# instantiate Slack & Twilio clients
slack_client = SlackClient(SLACK_BOT_TOKEN)


def handle_command(command, channel):
    '''
    :param command:  A text string containing a command directed at the bot
    :param channel: A string containing the channel that the command was given
    from.
    :return: If command is a valid command, execute that command. If not,
    display a message that the command is not valid.
    '''
    response = ("(´･_･`) No one ever taught me how to do that. \n"
               " (use {} a list for available commands)".format("*help*"))
    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure...write some more code then I can do that!"
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def parse_slack_output(events):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    if events and len(events) > 0:
        logging.debug('event in parse_slack_output(): ' + str(events))
        for event in events:
            if event and 'text' in event and AT_BOT in event['text']:
                # return text after the @ mention, whitespace removed
                command = event['text'].split(AT_BOT)[1].strip().lower()
                channel = event['channel']
                logging.debug('command, channel parse_slack_output(): '
                              '{}, {}'.format(command, channel))
                return command, channel
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("BBbot is connected and running!")
        # Command below can be used to retrieve ID
        logging.debug('ID: ' + slack_client.api_call('auth.test')['user_id'])
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else: print("Connection failed. Invalid Slack token or bot ID?")