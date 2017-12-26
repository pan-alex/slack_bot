''' Some functions and globals are shared between all of the list commands so
that they share the same syntax. These are in this file and then imported to
each list command to avoid any circular dependencies.
'''

# same as string.punctuation but exclude: , ; - (keep hyphenated words)
PUNCTUATION = '!"#$%&\'()*+./:<=>?@[\\]^_`{|}~'

def list_remove_punctuation(other_text=''):
	'''
	This is a function to be wrapped in the list commands:
	 * command_add(), command_delete(),

	:param other_text: String containing any other text in the message that
	was issued after the 'add' command. Will remove any punctuation, other than
	those in DELIMITERS.

	:return: Returns a string, which is other_text with the punctuation removed.
	'''
	text_no_punc = other_text.translate(
		other_text.maketrans(PUNCTUATION, ' ' * len(PUNCTUATION)))
	return text_no_punc