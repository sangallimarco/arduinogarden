# -*- coding: utf-8 -*-
from universal import engineManager
from threading import Thread
import time

########################################
class actionTimer(Thread):
	def __init__(self,actions,callback):
		Thread.__init__(self)
		self.actions=actions
		self.callback=callback
		self.start()
		
	def run(self):
		while len(self.actions)>0:
			cmd,t=self.actions.pop(0)
			print "SENDING CMD: %s" % cmd[:-1]
			self.callback(cmd)
			#
			time.sleep(t)
			
########################################
class pinger(Thread):
	def __init__(self,callback):
		Thread.__init__(self)
		self.callback=callback
		self.start()
		
	def run(self):
		while 1:
			print "SENDING PING"
			self.callback("#~A0\n")
			#
			time.sleep(1)
		
########################################
class customEngine(engineManager):
	def __init__(self,host):
		#@@@p=pinger(self.sendCmd)
		self.bridge = "C"
		self.pins = ["D","E","F","G"]

		engineManager.__init__(self,host)
		
	def onConnect(self):
			print "RESET SYSTEM"
			#append 
			cmd = [
				"*\n",
				"*\n",
				"#>%s1\n" % self.bridge #reset bridge
			]
			#add pins
			for i in self.pins:
				cmd.append("#%s>1\n" % i)
			self.cmd=cmd+self.cmd

			#set thread tick
			#self.setTick(0.5)
	
	def onData(self,engine,data):
		print "DATA FROM ARDUINO: %s" % data[:-1]
		
	def createCmd(self,pin,on,off):
		cmd = [
			["#>%s0\n#>%s0\n" % (self.bridge,pin), off], #open valve
			["#>%s0\n#>%s1\n" % (self.bridge,pin), off], #change bridge
			["#>%s1\n#>%s1\n" % (self.bridge,pin), on], #sleep
			["#>%s1\n#>%s0\n" % (self.bridge,pin), off], #close valve
			["#>%s1\n#>%s1\n" % (self.bridge,pin), off] #sleep
		]
		return cmd
		
	def pumpsOn(self,on=10,off=1):
		#pass all to a timer
		cmd = []
		for i in self.pins:
			cmd += self.createCmd(i,on,off)
		#
		t=actionTimer(cmd,self.sendCmd)
		
	def singlepumpOn(self,on=10,off=2):
		#pass all to a timer
		cmd = self.createCmd(self.pins[0],on,off)
		#
		t=actionTimer(cmd,self.sendCmd)

########################################
if __name__=="__main__":
	e=customEngine("192.168.1.177")
	#send command
	time.sleep(2)
	while 1:
		#pumps on!
		e.pumpsOn(10)
		#
		time.sleep(120)
		print "----------------"

