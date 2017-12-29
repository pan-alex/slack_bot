'''
This command is import into BBbot.py as a command that the Slack bot can
handle. When called by any of the keywords listed in `keys`, command_read() will
be executed.
'''
import logging
import os
from commands.list_globals import list_remove_punctuation

DELIMITERS = r'[,;]+|and | to '


# TEST = 'apples, peanuts, oranges and pizza, and apricots to my todo list please'
TEST = 'pizza, pp, and pineapple to that one thing... Oh yeah! The grocery list. Thanks!'


def command_read_correct_syntax(text_no_punc=''):
	'''
	This is a function to be wrapped in command_read() and fed a string from
	list_remove_punctuation(). This function exists to check that the
	correct syntax was supplied to command_read().

	:param text_no_punc: A string with no punctuation except for those in
	DELIMITERS. Function will look for certain keywords
	based on the syntax:

	" ... (___) list ..."

	* [__] represent list items (things to be added to the list; e.g., 'eggs')
	* List items must be separated by designated delimiters: 'and' ',' ';'
	* ... are any words that can exist in between key words but are ignored.
	* '(__) list' (__) is the name of the list and signals to the bot to look up
	  that file in the directory.

	:return: A bool. False if any syntax errors exist and True if no syntax
	errors exist. Conditions checked:
	'''
	logging.debug('text_no_punc in command_add_correct_syntax: ' + text_no_punc)
	text_as_list = text_no_punc.split()

	cond1 = 'list' in text_as_list
	cond2 = len(text_as_list) > 1
	logging.debug('cond1: {}; cond2: {}'.format(cond1, cond2))
	return cond1 and cond2

################################################################ How to handle @bbbot2 add to list (nothing between 'to' and 'list')


def command_read(sender, other_text=''):
	"""
	**Note to self: Implement a way to not write in duplicates**


	:param sender: Person who sent the message. This is force-fed to the
	function when called by handle_command(). Does nothing with it.

	:param other_text: String containing any other text in the message that
	was issued after the 'add' command. Function will look for certain keywords
	based on the syntax:

	"read  ... (___) list ..."

	* [__] represent list items (things to be added to the list; e.g., 'eggs')
	* List items must be separated by designated delimiters: 'and' ',' ';'
	* ... are any words that can exist in between key words but are ignored.
	* '(__) list' (__) is the name of the list and signals to the bot to look up
	  that file in the directory.

	:returns: Writes the list items to the specified file as a new line. Returns
	a message that includes all of the items in the list.
	If no file exists under that name, create one and provide a message that a
	new file was created.
	"""
	logging.debug('command_read() evaluated.')
	text_no_punc = list_remove_punctuation(other_text)

	if not command_read_correct_syntax(text_no_punc):
		return ("(⊙_☉)7 Sorry... I didn't understand that syntax."
		        " Try this: 'read me my grocery list.'")
	else:
		i = text_no_punc.split().index('list')
		list_name = ' '.join(text_no_punc.split()[i - 1:i + 1])
		# Check if a file under the name '____ list.txt' exists.
		path = os.path.join('./lists/', list_name) + '.txt'
		file_existed = os.path.isfile(path)
	if file_existed:
		list_items = []
		with open(path, mode='r') as file:
			list_items = str(file.read())
			logging.debug('items in file.read() in command_read(): ' + list_items)
		response = "Here's what's on your *{}*: \n{}".format(
			list_name, list_items)
	else:
		response = ("You don't have a list named *{}*.".format(list_name))
	return response


####

keys = ('read',)
elements = [command_read] * len(keys)
COMMANDS_READ = dict(zip(keys, elements))

#### tests to run in Slack
# '''
# @bbbot2 read my grocery list
# @bbbot2 read eggs, milk, and cheese to my grocery list.
# @bbbot2 read pizza, a big fat platter, cheerios; and ,,; juice a new list
# @bbbot2 read .................... sjoFHSJF AS;ALKDJA; The grocery list. Thanks!
# @bbbot2 read
# @bbbot2 read list
# '''
