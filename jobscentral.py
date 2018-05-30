
# Simple scraper in order to find some IT related jobs in Singapore from JobsCentral
# Capitals are being placeholders for sensitive information. You can change them to your credentials

import requests
import json
import time
from datetime import datetime
import os
from random import randint
import psycopg2
import sys

def write_to_db(id, timestamp, jobTitle, onlineSince, company, description, jobNature, totalJobCount):
	#Define our connection string
	conn_string = "host='ENTER_YOUR_HOST_E.G.AMAZONAWS' dbname='ENTER_YOUR_DB_NAME' user='USERNAME' password='PASS'"

	# print the connection string we will use to connect
	print "Connecting to database\n	->%s" % (conn_string)

	# get a connection, if a connect cannot be made an exception will be raised here
	conn = psycopg2.connect(conn_string)

	# conn.cursor will return a cursor object, you can use this cursor to perform queries
	cursor = conn.cursor()
	print "Connected!\n"

	cursor.execute("INSERT INTO jobcentraljobs VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
	[id, timestamp, jobTitle, onlineSince, company, description, jobNature, totalJobCount])
	# the write statement has to be commited!
	conn.commit()
	conn.close()
	print 'commit to db and close connection'

# method needed in order to avoid running it at startup when importing in flask framework
def run_jobscentral():
	timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	print('start jobscentral data gathering: ' + str(timestamp))

	#Define our connection string
	conn_string = "host='ENTER_YOUR_HOST_E.G.AMAZONAWS' dbname='ENTER_YOUR_DB_NAME' user='USERNAME' password='PASS'"

	# print the connection string we will use to connect
	print "Connecting to database\n	->%s" % (conn_string)

	# get a connection, if a connect cannot be made an exception will be raised here
	conn = psycopg2.connect(conn_string)

	# conn.cursor will return a cursor object, you can use this cursor to perform queries
	cursor = conn.cursor()
	print "Connected!\n"
	# clear all entries from table before running
	cursor.execute("TRUNCATE TABLE jobcentraljobs")
	conn.commit() 	# the write statement has to be commited!
	conn.close()

	#Job descriptions in the IT field
	businessAnalyst = ['Business Analyst','Business%20Analyst']
	softwareBusinessAnalyst = ['Software Business Analyst','Software%20Business%20Analyst']
	softdev = ['Software Developer','Software%20Developer']
	integrator = ['Software Integrator','Software%20Integrator']
	planner = ['Software Planner','Software%20Planner']
	implementationManager = ['Software Implementation Manager','Software%20Implementation%20Manager']
	softwareConsultant = ['Software Consultant','Software%20Consultant']
	softwareIntTestEngineer = ['Software Integration Test Engineer','Software%20Integration%20Test%20Engineer']

	#Jobs array
	jobList = [businessAnalyst, softwareBusinessAnalyst, softdev, integrator, planner, implementationManager, softwareConsultant, softwareIntTestEngineer]


	#write top line of CSV file
	#with open('statsSingapore.txt', 'a') as the_file:
	    #write now the info for all jobs in region with distribution
	 #   the_file.write('id') #time of query
	 #   the_file.write(',,')
	 #   the_file.write('timestamp') #time of query
	 #   the_file.write(',,')
	 #   the_file.write('jobTitle')
	 #   the_file.write(',,')
	  #  the_file.write('onlineSince') #number of jobs found in region
	  #  the_file.write(',,')
	  #  the_file.write('company') #name of region, first number is clear text, second number for query
	  #  the_file.write(',,')
	  #  the_file.write('description') #how many jobs in large company
	  #  the_file.write(',,')
	  #  the_file.write('jobNature') #how many jobs in recruiting agent
	  #  the_file.write(',,')
	  #  the_file.write('totalJobCount') #how many jobs in sme
	  #  the_file.write('\n')

	# Get a copy of the default headers that requests would use
	headers = requests.utils.default_headers()
	# Update the headers with your custom ones
	# You don't have to worry about case-sensitivity with
	# the dictionary keys, because default_headers uses a custom
	# CaseInsensitiveDict implementation within requests' source code.
	#userAgents
	headers.update(
	    {#mobile header: huawei android phone with app
	        'User-Agent': 'jobscentral; Dalvik/1.6.0 (Linux; U; Android 4.4.2; CHM-U01 Build/HonorCHM-U01)',
	    }
	)

	#start for loop here for looping thru the jobs
	counter = 1 # first id to fill out db

	for jobEntry in jobList:
		print('loop started for job: ' + jobEntry[0])
		#url of JobsCentral Singapore
		url = 'https://m.jobscentral.com.sg/api/jobs?q='+ jobEntry[1] +'&_page=1&_limit=100&sf=jf'

		#get the query result from the url with UA set for a ALL jobs in current location
		response = requests.get(url, headers=headers)
		json_data = response.json()
		print(json_data)

		#print out the jobtitles being returned in json object
		for entry in json_data:
			print entry['jobTitle'].encode('utf-8')

			write_to_db(counter, timestamp, entry['jobTitle'].encode('utf-8'), entry['postedDate'], entry['company'].encode('utf-8'), entry['descriptionTeaser'].encode('utf-8'), entry['jobNature'].encode('utf-8'), counter)
			print 'written to db'

			#with open('statsSingapore.txt', 'a') as the_file:
				#write now the info for all jobs in region with distribution
			#	the_file.write(str(counter)) #time of query
			#	the_file.write(',,')
			#	the_file.write(timestamp) #time of query
			#	the_file.write(',,')
			#	the_file.write(entry['jobTitle'].encode('utf-8'))
			#	the_file.write(',,')
			#	the_file.write(str(entry['postedDate'])) #number of jobs found in region
			#	the_file.write(',,')
			#	the_file.write(entry['company'].encode('utf-8')) #name of region, first number is clear text, second number for query
			#	the_file.write(',,')
			#	the_file.write(entry['descriptionTeaser'].encode('utf-8')) #how many jobs in large company
			#	the_file.write(',,')
			#	the_file.write(entry['jobNature'].encode('utf-8')) #how many jobs in recruiting agent
			#	the_file.write(',,')
			#	the_file.write(str(counter)) #how many jobs in sme
			#	the_file.write('\n')
			counter = counter + 1

		print(str(counter) + ' jobs found')
		write_to_db(counter, timestamp, jobEntry[0], '2017-05-18 14:55:21', str(0), str(0), str(0), counter)
		print 'written to db'
		counter = counter + 1
		#with open('statsSingapore.txt', 'a') as the_file:
			#write now the info for all jobs in region with distribution
		#	the_file.write(str(counter)) #time of query
		#	the_file.write(',,')
		#	the_file.write(timestamp) #time of query
		#	the_file.write(',,')
		#	the_file.write(jobEntry[0])
		#	the_file.write(',,')
		#	the_file.write(str(0)) #number of jobs found in region
		#	the_file.write(',,')
		#	the_file.write(str(0)) #name of region, first number is clear text, second number for query
		#	the_file.write(',,')
		#	the_file.write('Total jobs found') #how many jobs in large company
		#	the_file.write(',,')
		#	the_file.write(str(0)) #how many jobs in recruiting agent
		#	the_file.write(',,')
		#	the_file.write(str(counter)) #how many jobs in sme
		#	the_file.write('\n')

	print('All done: Exit jobscentral scraper')
