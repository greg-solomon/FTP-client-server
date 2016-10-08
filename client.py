#!/usr/bin/python

import socket, sys, os

# USAGE : client.py {host} {port} {protocol [GET, PUT, DEL]} {filename}
host = sys.argv[1]
port = int(sys.argv[2])

protocol = sys.argv[3]
protocol = protocol.upper()
file = sys.argv[4]

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

sock.connect((host,port))


 



status = sock.recv(5)
if status == "READY":
	if protocol == "GET":
		
		sock.send("GET")
		# send file name, receive number of bytes 
		sock.send(file)
		size = sock.recv(1024)
		status = "OK"
		sock.send(status)
			
		f = open(file,'wb')
		print "client receiving file " + file + " " + str(size) + " bytes"
		bytesReceived = 0
		while bytesReceived < int(size):
			data = sock.recv(int(size) % 1024)
			f.write(data)
			bytesReceived+=len(data)
		status = sock.recv(4)
		
		if status == "DONE":
			print "Complete"
			 
			
		
	elif protocol == "PUT":
		if os.access(file, os.R_OK):
			size = os.path.getsize(file)
			f = open(file,'rb')
			sock.send("PUT")
			sock.send(file)
			# wait for ok from server, send file
			status = sock.recv(2) 
			if status == "OK":
				print "client sending file " + file + " " + str(size) + " bytes"
				sock.send(str(size))
				bytesSent = 0
				while bytesSent < size:
					data = f.read(1024)
					sock.send(data)
					bytesSent+=len(data)
				
				status = sock.recv(4)
				if status == "DONE":
					print "Complete"
		elif os.access(file, os.F_OK):
			print "Cannot access file " + file + " or it does not exist" 
	elif protocol == "DEL":
		sock.send("DEL")
		sock.send(file)
		print "deleting file " + file 
		
		status = sock.recv(1024)
		if status == "DONE":
			print "Complete"
		else:
			print "Server cannot access " + file
	else:
		print "Please enter a valid protocol"





