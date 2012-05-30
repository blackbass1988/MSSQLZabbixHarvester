# -*- coding: utf-8
import time, os, pymssql

def loadConfig():
	import ConfigParser
	config = ConfigParser.ConfigParser()
	config.read("config.ini")
	return config

def printResponse(row,format):
	if format == "json":
		print "{connections:"+row[0]+",cpu:"+row[1]+",pio:"+row[2]+",musage:"+row[3]+"}"
	if format == "cvs":
		print row[0] + ";" +  row[1] + ";" + row[2] + ";" + row[3]

config = loadConfig()
try:
	msConnection = pymssql.connect(host=config.get("mssql","host"),user=config.get("mssql","user"),password=config.get("mssql","password"))
	msCursor = msConnection.cursor()
except:
	print "getCursor exception! Check the config.ini for correct properties!"

query = "select (select count(dbid) from sys.sysprocesses where dbid>0) as totalCon, sum (cpu) as cpu, sum(physical_io)  as pio, sum(memusage)  as musage from sys.sysprocesses;"	

try:
	result = msCursor.execute(query)
except:
	print "SQL syntax error"

for row in result:
	printResponse(row, config.get("commin","format"))

msConnection.close()

