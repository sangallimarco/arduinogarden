# -*- coding: utf-8 -*-
import urllib2,re,time
from gardenController import *
import math
import json

#yahoo ##########################################################################
def getWeather():
	url="http://www.myweather2.com/developer/forecast.ashx?uac=.frFFHX1sj&query=SE21&output=json"
	content = urllib2.urlopen(url).read()
	
	current = None
	if(content):
		res = json.loads(content)
		current = res['weather']['curren_weather'][0]
		
		#no rain data grep from text
		wt = current['weather_text'].upper()
		print wt
		rl = ['MIST','RAIN','CLOUD']
		
		#check if it's raining
		rain = 0
		for i in rl:
			if i in wt:
				rain = 1
				
		res={
			"temp":int(current['temp']),
			"hum":int(current['humidity']),
			"wind":int(current['wind'][0]['speed']),
			"rain":rain,
		}
		
	else:
		res={
			"temp":0,
			"hum":0,
			"wind":0,
			"rain":0,
		}
		
	#print res
	return res
	
#####################################################
if __name__=="__main__":
	#status 
	e=customEngine("192.168.1.177")
	#-----------------------------------------------
	#---------- CONFIG -----------------------------
	#-----------------------------------------------
	#triggers
	ht=[8,12,16,20]
	#wind Km/h
	wt=10
	#temperature C
	tt=0
	#humidity %
	hut=95
	#dalay seconds 60*minutes
	delay=60*15
	#-----------------------------------------------
	#-----------------------------------------------
	#-----------------------------------------------
	while 1:
		#current Hour
		h=time.localtime()[3]
		print "CURRENT TIME: %s" % h
		
		#get weather site data
		try:
			w=getWeather()
			print "WEATHER DATA: %s" % w
		except:
			pass
			#raise
		else:
			#check params
			if w["hum"]<hut and w["wind"]<wt and w["temp"]>=tt and h in ht:
				print "SYSTEM ON"
				#rain only 1 zones
				if w["rain"]<1:
					e.pumpsOn(delay)
				else:
					e.singlepumpOn(delay)
				#sleep one hour
				time.sleep(60*60)
			 
		#next loop in...
		#60*60*24/500 number of connections per day max 500
		time.sleep(500)	
		
		

