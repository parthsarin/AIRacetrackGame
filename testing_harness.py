"""
TESTING HARNESS (don't change, please!)
"""
import errors
import sys
import collections
import pip
import traceback

"""
Silence output
"""
class DummyFile(object):
    def write(self, x): pass

"""
A lot of stuff having to do with colors
"""
def supports_color():
    """
    Returns True if the running system's terminal supports color, and False
    otherwise.
    """
    plat = sys.platform
    supported_platform = plat != 'Pocket PC' and (plat != 'win32' or 'ANSICON' in os.environ)
    # isatty is not always implemented, #6223.
    is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    if not supported_platform or not is_a_tty:
        return False
    return True

colors = {
    'header': '\033[95m',
    'blue': '\033[94m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'red': '\033[91m',
    'end': '\033[0m',
    'bold': '\033[1m',
    'underline': '\033[4m'
}

# Colorize things at all?
colorized = supports_color()

# Use termcolor?
try:
	from termcolor import colored
	use_termcolor = True
except ModuleNotFoundError:
	use_termcolor = False

def opt_colored(x, color):
	if colorized:
		if use_termcolor:
			return colored(x, color)
		else:
			return colors[color] + x + colors['end']
	else:
		return x

"""
The actual testing harness
"""
# Yes, I know, globals are terrible, but... we need this one
_all_tests = collections.defaultdict(list) # God I hope nobody uses this name...

def run_test(name, category='default', silence=False):
	"""
	Note for the curious: there's a cool / annoying feature of decorators
	that if you want the decorator to have an input, you need to write
	ANOTHER decorator function within your real decorator...
	"""
	if type(name) != str or not name:
		raise errors.NameError("Please provide a valid test name.")

	# Here's the real function...
	def wrapper(func):
		def modified_test(*args, **kwargs):
			# Try running the function and catch exceptions
			try:
				if silence:
					save_stdout = sys.stdout
					sys.stdout = DummyFile()

				output = func(*args, **kwargs)

				if silence:
					sys.stdout = save_stdout
			
			except KeyboardInterrupt:
				# Wouldn't want this to go wrong...
				raise KeyboardInterrupt

			except Exception as e:
				print(opt_colored('FAIL: {}'.format(name), 'red'))
				print(opt_colored("The test raised the following exception:", 'red'))
				traceback.print_exc()

			# Make sure that the output is boolean
			if type(output) != bool:
				raise errors.OutputTypeError("Test '{}' was not set up correctly. The output should be a bool.".format(name))

			# Did it pass the test?
			if output:
				print(opt_colored('PASS: {}'.format(name), 'green'))
			else:
				print(opt_colored('FAIL: {}'.format(name), 'red'))

			return output

		_all_tests[category].append(modified_test)
		return modified_test

	return wrapper

def run_all_tests():
	passtable = []

	all_tests = collections.OrderedDict(_all_tests)
	for category in all_tests:
		print(opt_colored(f"Category {category}:", 'blue'))
		print(opt_colored('-----------------------', 'blue'))

		for test in all_tests[category]:
			passtable.append(test())
		
		print()

	passed = sum(map(int, passtable))
	print(opt_colored(f"Passed {passed} / {len(passtable)} tests.", 'blue'))