'''
**** NOT READY FOR INCORPORATION ****
This command is import into BBbot.py as a commannd that the Slack bot can
handle. When called by any of the keywords listed in `keys`, command_hi() will
be executed.
'''
import logging
import re
import os

TEST = 'apples, peanuts, oranges and pizza, and apricots to my poop list'


def command_add(sender, other_text=None):
	"""
	:param sender: Person who sent the message. This is force-fed to the
	function when called by handle_command(). Does nothing with it.
	:param other_text: String containing any other text in the message that
	was issued after the 'add' command. Function will look for certain keywords
	based on the syntax:

	"add [__], [__], [__] and [__] to ... (___) list ..."

	* 'add' is required to call command_add() through handle_command(), but is not
	actually required inside of command_add.
	* [__] represent list items (things to be added to the list; e.g., 'eggs')
	* ',', 'and', ';' are all delimiters that will separate list items
	* 'to' signals the end of the list items. Anything before 'to' will be added
	to the list, while everything after will be ignored.
	* ... are any words that can exist in between key words but are ignored.
	* '(__) list' (__) is the name of the list and signals to the bot to look up
	  that file in the directory.

	:returns: Writes the list items to the specified file as a new line. Returns
	a message that includes all of the items in the list.
	If no file exists under that name, create one and provide a message that a
	new file was created.
	"""
	logging.debug('command_add() evaluated.')
	delimiters = r'[,;]+|and|to'

	# Check syntax
	# Other conditions I need to add:
	#    - no delimiters appear after the first 'to'
	#    - code currently makes a bug if delimiters appear after the first 'to'
	text_as_list = other_text.split()
	cond1 = 'to' not in text_as_list
	cond2 = 'list' not in text_as_list
	cond3 = text_as_list.index('to') > text_as_list.index('list')

	if cond1 or cond2 or cond3:
		return ("(⊙_☉)7 Sorry... I'm not sure I understand what you mean."
		        " Try this: 'add ____, ____, and ____ to my ____ list'")

	else:
		parsed = [s.strip() for s in re.split(delimiters, other_text) if
		          s.strip()]
		list_items = parsed[:-1]
		# Find the word 'list' and join it to the word directly in front.
		i = parsed[-1].split().index('list')
		list_name = ' '.join(parsed[-1].split()[i-1:i+1])

	# Check if a file under the name '____ list.txt' exists
	path = os.path.join('./lists/', list_name) + '.txt'
	file_existed = os.path.isfile(path)

	with open(path, mode='a') as file:
		for item in list_items: file.write(item + '\n')

	if file_existed:
		response = "I've added these items to your {}: {}!".format(
			list_name, str(list_items)[1:-1])
	else:
		response = ("You don't have a list named {}. "
		            "Don't worry - I've made one and added these items: {} \n"
		            "If this was a mistake, use *delete*.".format(
			list_name, str(list_items)[1:-1]))
	return response



keys = ('add',)
elements = [command_add] * len(keys)
COMMANDS_LIST = dict(zip(keys, elements))

#### tests to run in Slack
# @bbbot2 add pizza and cheerios to my grocery list
# @bbbot2 add list pizza and cheerios to my grocery
# @bbbot2 add pizza, a big fat platter, cheerios; and ,,; juice to a new list
# @bbbot2 add pizza to that one thing... Oh yeah: grocery list. Thanks!
