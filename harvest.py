# -*- coding: utf-8
import time, os, pymssql

def loadConfig():
	import ConfigParser
	config = ConfigParser.ConfigParser()
	config.read("config.ini")
	return config

def printResponse(row,format):
	if format == "json":
		print "{connections:" + str(row[0]) + ",cpu:" + str(row[1]) + ",pio:" + str(row[2]) + ",musage:" + str(row[3]) + "}"
	if format == "cvs":
		print row[0] + ";" +  str(row[1]) + ";" + str(row[2]) + ";" + str(row[3])

config = loadConfig()
msConnection = pymssql.connect(host=config.get("mssql","host"),user=config.get("mssql","login"),password=config.get("mssql","password"))
msCursor = msConnection.cursor()

query = "select (select count(dbid) from sys.sysprocesses where dbid>0) as totalCon, sum (cpu) as cpu, sum(physical_io)  as pio, sum(memusage)  as musage from sys.sysprocesses;"	
msCursor.execute(query)
result = msCursor.fetchall()
if result <> None:
	for row in result:
		printResponse(row, config.get("common","format"))
else:
	print "query returs none"
msConnection.close()

