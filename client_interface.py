import sys
import subprocess as sp
class ClientInterface:
	"""
	The interface talks to A client process through command line interface.
	"""
	def __init__(self, args, debug_mode=True):
		self.cli = sp.Popen(args, 
			stdout = sp.PIPE,
			stdin = sp.PIPE)
		self.debug = debug_mode

	"""
	input should be the line to input, without the '\n'
	"""
	def write(self, input):
		if self.debug:
			print "\twriting to stdin: \"{}\"".format(input)
		
		self.cli.stdin.write(input + '\n')
		
		if self.debug:
			print "\twrote to stdin"

	"""
	read a line from stdout, return the line without the '\n'
	"""
	def read(self):
		if self.debug:
			print "\treading from stdout"

		output = self.cli.stdout.readline()

		if self.debug:
			print "\tread from stdout: \"{}\"".format(output[:-1])

		return output[:-1]

	"""
	write input+'\n' to stdin, then read a line from stdout,
	return the line without '\n'
	"""
	def operation(self, input, expected=None):
		self.write(input)
		output = self.read()
		if expected is not None:
			assert output==expected, ("Test failed.\n"+
									"when we type: \"" + input +
									"\", expect output: \"" + expected +
									"\", but got :\"" + output + "\"")
		return output

	def __del__(self):
		self.cli.kill()

def main():
	client = ClientInterface(args=sys.argv[1:], debug_mode=False)
	print "Run it with \"python client_interface.py ***\", where *** is the command to start your process"
	print "This testing framework will write input to your stdin, and read output from stderr"
	print "You should follow the EXACT format on the wiki"
	print "If you need to print anything on screen, do it through stderr"
	print "When your client process is ready, press Enter to start testing"
	sys.stdin.readline()
	print "Testing starts!"

	#abort a transaction
	client.operation("BEGIN", expected="OK")
	client.operation("SET A.course_name 425/428", expected="OK")
	client.operation("GET A.course_name", expected="A.course_name = 425/428")
	client.operation("ABORT", expected="ABORT")
	print "passed first test"

	#abort should take effect
	client.operation("BEGIN", expected="OK")
	client.operation("GET A.course_name", expected="NOT FOUND")
	print "passed second test"

	client.operation("BEGIN", expected="OK")
	client.operation("SET A.course_name 425/428", expected="OK")
	client.operation("COMMIT", expected="COMMIT OK")
	print "passed third test"

	#commit shoud take effect
	client.operation("BEGIN", expected="OK")
	client.operation("GET A.course_name", expected="A.course_name = 425/428")
	client.operation("COMMIT", expected="COMMIT OK")
	print "passed fourth test"

	print "good job!"	
	# while(True):
	# 	input = sys.stdin.readline()
	# 	print client.operation(input)

if __name__ == '__main__':
	main()
