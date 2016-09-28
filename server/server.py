#!/usr/bin/python


import socket, sys, os 
 
host = "localhost"
verbose = "-v" in sys.argv
port = int(sys.argv[1])


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host,port))

if verbose:
	print "server waiting on port:" + str(port)
sock.listen(0)

def get(file):
	if os.access(file, os.R_OK):
		size = os.path.getsize(file) 
		if verbose:
			print "server receiving " + str(size) + " bytes"
		conn.send(str(size))
		
		status = conn.recv(2)
		
		
		if status == "OK":
			
			f = open(file,"rb")
			bytesSent = 0
			
			while bytesSent < size:
				data = f.read(1024)
				conn.send(data)
				bytesSent+=len(data)
			f.close()
			return "DONE"
	elif os.access(file, os.F_OK):
		return "Cannot access file"

def put(file):
	conn.send("OK")
	size = int(conn.recv(1024))
	f = open(file,'wb')
	
	bytesReceived = 0
	while bytesReceived < size:
		data = conn.recv(1024)
		f.write(data)
		bytesReceived+=len(data)
	f.close()
	return "DONE"
	
def delete(file):
	if os.access(file, os.R_OK):
	
		if verbose:
			print "server deleting " + file 
			
		os.remove(file)
		return "DONE"
		
	elif os.access(file, os.F_OK):
		return "Cannot access file"



	
while True:
	conn, addr = sock.accept()
	
	if verbose:
		print "server connected to client at: "+addr[0]+":"+str(port)
	conn.send("READY")
	protocol = conn.recv(3)
	if verbose:
		print "server receiving request:" + protocol
	if protocol == "GET":
		file = conn.recv(1024)
		conn.send(get(file))
		conn.close()
	elif protocol == "PUT":
		file = conn.recv(1024)
		conn.send(put(file))
		conn.close()
		
	elif protocol == "DEL":
		file = conn.recv(1024)
		conn.send(str(delete(file)))
		conn.close()

	


