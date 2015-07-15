import sublime, sublime_plugin
import socket 
import threading

class CollabClientCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.view.insert(edit, 0, "Client!")
		s = socket.socket()
		host = socket.gethostname()
		port = 12346
		try:
			s.settimeout(2)
			s.connect((host, port))
			self.view.insert(edit, 0, s.recv(1024).decode('utf-8'))
			s.close
		except Exception as e:
			self.view.insert(edit, 0, '\n'+e)
			s.close

class CollabHostCommand(sublime_plugin.TextCommand):
	# put this in a thread?
	def run(self, edit):
	#	self.view.insert(edit, 0, "Host!")
		thread = serverThread(self.view)
		thread.start()

class serverThread(threading.Thread):
	def __init__(self, data):
		#self.timeout = timeout
		self.data = data
		threading.Thread.__init__(self)

	def run(self):
		s = socket.socket()
		host = socket.gethostname()
		port = 12346
		s.bind((host,port))

		s.listen(5)
		i = 0
		while i < 8:
			c, addr = s.accept()
			#self.view.insert(edit, 0, 'Got connection from', addr)
			i = i + 1
			#self.view.insert(dit, 0, 'looping')
			data = "thank you for connecting!"
			#try:
			c.send(data.encode())
			#c.send(self.data.substr(sublime.Region(0,100)).encode())
			c.close()
			#except:
			#	c.send(data.encode())
			#	c.close()
class ScratchCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.view.insert(edit,0,self.view.substr(sublime.Region(0,1000)))
