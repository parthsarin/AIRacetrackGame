"""
TESTING HARNESS (don't change, please!)
"""
import errors
import sys
from termcolor import colored
import collections

_all_tests = collections.defaultdict(list) # God I hope nobody uses this name...

class DummyFile(object):
    def write(self, x): pass

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
				print(colored('FAIL: {}'.format(name), 'red'))
				print(colored("The test raised the following exception:", 'red'))
				print(colored(str(e), 'green'))

			# Make sure that the output is boolean
			if type(output) != bool:
				raise errors.OutputTypeError("Test '{}' was not set up correctly. The output should be a bool.".format(name))

			# Did it pass the test?
			if output:
				print(colored('PASS: {}'.format(name), 'green'))
			else:
				print(colored('FAIL: {}'.format(name), 'red'))

			return output

		_all_tests[category].append(modified_test)
		return modified_test

	return wrapper

def run_all_tests():
	passtable = []

	all_tests = collections.OrderedDict(_all_tests)
	for category in all_tests:
		print(colored(f"Category {category}:", 'blue'))
		print(colored('-----------------------', 'blue'))
		for test in all_tests[category]:
			passtable.append(test())

	passed = sum(map(int, passtable))
	print()
	print(colored(f"Passed {passed} / {len(passtable)} tests.", 'blue'))