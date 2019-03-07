"""
TESTING HARNESS (don't change, please!)
"""
import errors
import sys
import collections
import pip
# only import colorized if it's installed
colorized = 'termcolor' in pip.get_installed_distributions()
if colorized:
	from termcolor import colored

# Yes, I know, globals are terrible, but... we need this one
_all_tests = collections.defaultdict(list) # God I hope nobody uses this name...

class DummyFile(object):
    def write(self, x): pass

def opt_colored(x, color):
	if colorized:
		return colored(x, color)
	else:
		return x


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
				print(opt_colored(str(e), 'green'))

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

	passed = sum(map(int, passtable))
	print()
	print(opt_colored(f"Passed {passed} / {len(passtable)} tests.", 'blue'))