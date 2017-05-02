import sys
from client_interface import ClientInterface

def add(client, serv_key, inc):
	client.operation("BEGIN", expected="OK")
	ret = client.operation("GET {}".format(serv_key))
	split = ret.split(' = ')
	result = int(split[1])
	client.operation("SET {} {}".format(serv_key, str(result+inc)), expected="OK")
	ret = client.operation("COMMIT")
	if ret=="COMMIT OK":
		return True
	else:
		return False

def test1(client, k=1000):
	serv_key = 'A.money'
	print "test1 will increase a certain key for {} times".format(k)
	print "When your client process is ready, press Enter to start testing"
	sys.stdin.readline()
	print "Testing starts!"
	client.operation("BEGIN", expected="OK")
	client.operation("SET {} 0".format(serv_key), expected="OK")
	client.operation("COMMIT", expected="COMMIT OK")
	
	count = 0
	while count < k:
		if add(client, serv_key, 1):
			count  += 1

	client.operation("BEGIN", expected="OK")
	client.operation("GET {}".format(serv_key), expected="{} = {}".format(serv_key, str(k)))
	client.operation("COMMIT", expected="COMMIT OK")
	print "passed test1"

def main():
	client = ClientInterface(args=sys.argv[1:], debug_mode=True)
	print "Run this test on only one client"
	print "Run it with \"python client_interface.py ***\", where *** is the command to start your process"

	test1(client, 1000)

	print "good job!"

if __name__ == '__main__':
	main()
