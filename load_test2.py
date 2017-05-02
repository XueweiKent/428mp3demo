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
	print "test2 will increase a certain key for {} times on each client".format(k)
	print "When your clients are ready, press Enter to start testing"
	sys.stdin.readline()
	print "Testing starts!"
	#client.operation("BEGIN", expected="OK")
	#client.operation("SET {} 0".format(serv_key), expected="OK")
	#client.operation("COMMIT", expected="COMMIT OK")
	
	count = 0
	while count < k:
		if add(client, serv_key, 1):
			count  += 1

	print "now we check the value. The result from the last client should be 3000"
	print "IMPORTANT: BEGIN: " + client.operation("BEGIN")
	print "IMPORTANT: GET: " + client.operation("GET {}".format(serv_key))
	print "IMPORTANT: COMMIT: " + client.operation("COMMIT")

def main():
	client = ClientInterface(args=sys.argv[1:], debug_mode=False)
	print "Run this test on all three clients, the result from the last client should be 3000"
	print "Run it with \"python load_test2.py ***\", where *** is the command to start your process"

	test1(client, 1000)

	print "when finished, type Enter"
	sys.stdin.readline()

if __name__ == '__main__':
	main()
