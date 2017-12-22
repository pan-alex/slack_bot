'''
This command is import into BBbot.py as a command that the Slack bot can
handle. When called by any of the keywords listed in `keys`, command_roll() will
be executed.
'''
import logging
import random

def command_roll(sender, args=None):
	'''
	:param sender: Person who sent the command
	:param args: A list containing all of the words following the command
	itself. The function looks integers inside this list and uses the first
	integer it encounters as the number of sides on the die.
	:return: Randomly generates an integer between 1 and the number of sides on
	the die. If no number is supplied in args, it defaults to 20.
	'''
	logging.debug('command_roll() evaluated.')
	logging.debug('args in command_roll: ' + str(args))
	sides_on_die = 20
	if args:
		for item in args:
			logging.debug('item in command_roll: ' + str(item))
			if item.isdigit() and int(item) > 1:
				sides_on_die = int(item)
				break
	logging.debug('sides_on_die in command_roll: ' + str(sides_on_die))
	roll = random.randint(1, sides_on_die)
	return '<@{}> rolled {} on a {}-sided die!'.format(
		sender, roll, sides_on_die)


keys = ('roll', 'dice', 'die')
elements = [command_roll] * len(keys)
COMMANDS_ROLL = dict(zip(keys, elements))


#### tests to run in Slack

# # roll 0.5 and -5 return a 5-sided die. This is because punctuation chars
# # are replaced with spaces so the integers are read separately from punctuation
# # marks. I can't decide it this is a bug or a feature.
# @bbbot2 roll 0.5    # Number below 1
# @bbbot2 roll -5    # Number below 1
# @bbbot2 roll 0    # Number below 1; should roll 20
# hey @bbbot2 roll a 30 sided die for me!
# @bbbot2 roll a 400-sided die
# @bbbot2 roll 50.2
# @bbbot2 roll 0.5
#
# # These are evaluated the same way as roll. I only need to check that these
# # commands properly call the function.
# @bbbot2 die
# @bbbot2 die something 30
# @bbbot2 dice
# @bbbot2 dice 50.2
