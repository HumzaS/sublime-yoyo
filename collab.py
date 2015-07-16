import sublime, sublime_plugin
import socket 
import threading

class CollabClientCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		s = socket.socket()
		host = socket.gethostname()
		port = 12345
		try:
			s.settimeout(2)
			s.connect((host, port))
			self.view.insert(edit, 0, s.recv(1024).decode('utf-8') + "\n")
			s.close()
			print("connection closed")
		except Exception as e:
			print("exception", e)
			s.close()

class CollabHostCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		thread = serverThread(self.view)
		thread.start()

class serverThread(threading.Thread):
	def __init__(self, data):
		#self.timeout = timeout
		self.data = data
		threading.Thread.__init__(self)

	def run(self):
		s = socket.socket()
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		port = 12345
		s.bind((socket.gethostname(),port))

		s.listen(5)
		i = 0
		while i < 3:
			i += 1
			c, addr = s.accept()
			print('Got connection from', addr)
			try:
				#print("region contents: ", self.data.substr(sublime.Region(0,100)))
				#c.send("hello world {0}".format(i).encode())
				c.send(self.data.substr(sublime.Region(0,100)).encode())
				c.close()
			except:
				c.close()
		print("shutting down !!!!!!!")

class ScratchCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.view.insert(edit,0,self.view.substr(sublime.Region(0,1000)))
