"""This module provides a cross platform implementation of getch."""

import sys
try:
	import msvcrt
except ImportError:
	try:
		import termios
		import tty
	except ImportError:
		pass

__all__ = ('getch',)

def getch(prompt=''):

	"""Reads a character from standard input.
	If the user enters a newline, an empty string is returned. For the most
	part, this behaves just like input().  An optional prompt can be
	provided.
	"""

	print(prompt, end='')
	sys.stdout.flush()

	# Windows
	try:
		char = msvcrt.getwch()
	except NameError:
		pass
	else:
		if char == '\r' or char == '\n':
			char = ''

		return char

	# Unix
	file_number = sys.stdin.fileno()
	try:
		old_settings = termios.tcgetattr(file_number)
	except NameError:
		pass
	except termios.error:
		pass
	else:
		tty.setcbreak(file_number)

	try:
		char = chr(27)
		if sys.stdin.isatty():
			# avoid escape sequences and other undesired characters
			while ord(char[0]) in (8, 27, 127):
				char = sys.stdin.read(len(sys.stdin.buffer.peek(1)))
		else:
			char = sys.stdin.read(1)

		if char == '\r' or char == '\n':
			char = ''

	finally:
		try:
			termios.tcsetattr(file_number, termios.TCSADRAIN, old_settings)
		except NameError:
			pass

	return char