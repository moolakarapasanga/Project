import socket
import threading
from queue import Queue 
import argparse

queue = Queue()

def sock_connect(target,port):
	try:

		socket.setdefaulttimeout(10) 
		sock= socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
		output = sock.connect_ex((target,port))
		sock.close()
		return output
	except:
    	  pass

def main():
	parser=argparse.ArgumentParser('Smart PortScanner')
	parser.add_argument("-a","--address",type=str,help="The target IP address")
	parser.add_argument("-p","--port",type=str,help="<port-range>")
	parser.add_argument("-t","--thread",type=int,help="threads to run")
	args=parser.parse_args()
	target=args.address
	portNumbers=args.port.split('-')
	threads=int(args.thread)

	for i in range(int(portNumbers[0]),int(portNumbers[1])):
		queue.put(i)

	thread_runner(threads,target)

def scanner(target):
    while not queue.empty():
        port = queue.get()
        if sock_connect(target,port)==0:
           service=socket.getservbyport(port)
           print("[+] Port {}/tcp is open".format(port))
           print("[+] Banner : {}\n".format(service))
        else:
        	pass


def thread_runner(threads,target):

    thread_list = []
    try:
	    for t in range(threads):
	        thread = threading.Thread(target=scanner,args=(target,))
	        thread_list.append(thread)

	    for thread in thread_list:
	        thread.start()
    except:
    	pass

if __name__=="__main__":
	main()
