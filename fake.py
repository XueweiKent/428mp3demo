import sys

store = {}

def begin(line):
	return "OK"

def set(line):
	words = line.split(' ')
	key = words[1]
	value = ' '.join(words[2:])
	store[key] = value
	return "OK"

def get(line):
	words = line.split(' ')
	key = words[1]
	if not store.has_key(key):
		return "NOT FOUND"
	value = store[key]
	return "{key} = {value}".format(key=key, value=value)

def commit(line):
	return "COMMIT OK"

def abort(line):
	store.clear()
	return "ABORT"

def main():
	while True:
		line = sys.stdin.readline()
		line = line[:-1]
		if line.startswith("BEGIN"):
			print begin(line)
		elif line.startswith("SET"):
			print set(line)
		elif line.startswith("GET"):
			print get(line)
		elif line.startswith("COMMIT"):
			print commit(line)
		elif line.startswith("ABORT"):
			print abort(line)
		sys.stdout.flush()



if __name__ == '__main__':
	main()