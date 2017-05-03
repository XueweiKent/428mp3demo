import sys
import os
import struct
from client_interface import ClientInterface

def test1(client, k=1000):
	serv_keys = ['A.key1', 'B.key2', 'C.key3', 'D.key4', 'E.key5']
	random_val = str(struct.unpack("<L", os.urandom(4))[0])
	
	print "test3 will try to set all the 5 keys to the same value: {}".format(random_val)
	print "When your client process is ready, press Enter to start testing"
	sys.stdin.readline()
	print "Testing starts!"
	for i in range(k):
		client.operation("BEGIN", expected="OK")
		for s_k in serv_keys:
			client.operation("SET {} {}".format(s_k, random_val))
		client.operation("COMMIT")

	client.operation("BEGIN", expected="OK")
	for s_k in serv_keys:
		print 'value of {} is: {}'.format(s_k, client.operation("GET {}".format(s_k)))
	client.operation("COMMIT")

	print "now we check the value. The result from all 5 keys on the same client should be the same"
	print "when all client finished, type ENTER, see if all clients GET the same result"
	sys.stdin.readline()

	client.operation("BEGIN", expected="OK")
	for s_k in serv_keys:
		print 'value of {} is: {}'.format(s_k, client.operation("GET {}".format(s_k)))
	client.operation("COMMIT")

def main():
	client = ClientInterface(args=sys.argv[1:], debug_mode=True)
	print "Run this test on all three clients, should not deadlock, result should converge"
	print "Run it with \"python load_test3.py ***\", where *** is the command to start your process"

	test1(client, 1000)

	print "When everything is finished, type Enter"
	sys.stdin.readline()

if __name__ == '__main__':
	main()
