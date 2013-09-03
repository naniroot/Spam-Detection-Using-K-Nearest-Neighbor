from os import listdir
from os.path import isfile, join
from os import system

import sys
import math


stopwords = []
spamwords = []
genuinewords =[]
testwords =[]

spamdict = {}
genuinedict = {}
testdict={}

pgbr = True

def processspam(files):
	spampath = "./spam"
	for i in range (0, len(files)):
		k=files[i]
		with open(join(spampath,k), "r") as fs:
			while True:
				t = fs.readline()
				if len(t) == 0:
					break
				print t
				words = t.split()
				for l in range(0, len(words)):
					words[l] = words[l].lower()
					words[l] = ''.join(e for e in words[l] if e.isalpha())
					if len(words[l]) <= 2: continue;
					if words[l] not in stopwords: 
						spamwords.append(words[l])

def processgenuine(files):
        genuinepath = "./genuine"
        for i in range (0, len(files)):
                k=files[i]
                with open(join(genuinepath,k), "r") as fs:
                        while True:
                                t = fs.readline()
                                if len(t) == 0:
                                        break
				print t
                                words = t.split()
                                for l in range(0, len(words)):
                                        words[l] = words[l].lower()
                                        words[l] = ''.join(e for e in words[l] if e.isalpha())
					if len(words[l]) <= 2: continue;
                                        if words[l] not in stopwords:
                                                genuinewords.append(words[l])

def processtest(singlefile):
	testpath = "./test"
        with open(join(testpath,singlefile), "r") as fs:
       		while True:
        		t = fs.readline()
	                if len(t) == 0: break
			if pgbr: print "\n\nTEST FILE " + singlefile
			if pgbr: print "\n"+t
			if pgbr: raw_input()
        	        word = t.split()
                	for l in range(0, len(word)):
                		word[l] = word[l].lower()
	                        word[l] = ''.join(e for e in word[l] if e.isalpha())
        	                if len(word[l]) <= 2: continue;
                	        if word[l] not in stopwords:
                        		testwords.append(word[l])



def readstopwords():
	with open("stopwords.txt","r") as fs:
		while True:
			t= fs.readline()
			t=t.strip()
			if len(t) == 0: break
			stopwords.append(t)

def generatespamdict():
	for x in spamwords:
		if x in spamdict: spamdict[x]+=1
		else: spamdict[x] = 1 

def generategenuinedict():
	for x in genuinewords:
		if x in genuinedict: genuinedict[x]+=1
		else: genuinedict[x]=1

def generatetestdict():
	for x in testwords:
		if x in testdict: testdict[x]+=1
		else: testdict[x]=1

def eucledean(test, data):
	sum = 0 
	for x in test:
		if x in data:
			sum += test[x] * test[x]	# (test[x]-data[x])*(test[x]-data[x])
	return math.sqrt(sum)	

if len(sys.argv)>1: pgbr = False	
if not pgbr: system("cp ./test/spam* ./spam/")
if not pgbr: system("cp ./test/genuine* ./genuine/")
if pgbr: system("clear")
if pgbr: print "SPAM FILES"
if pgbr: raw_input()
spampath ="./spam"
spamfiles = [f for f in listdir(spampath) if isfile(join(spampath,f)) ]
processspam(spamfiles)

if pgbr: raw_input()
if pgbr: system("clear")
print "GENUINE FILES"
if pgbr: raw_input()
genuinepath ="./genuine"
genuinefiles = [k for k in listdir(genuinepath) if isfile(join(genuinepath, k))]
processgenuine(genuinefiles)
if pgbr: raw_input()

testpath = "./test"
testfiles = [l for l in listdir(testpath) if isfile(join(testpath,l))]

readstopwords()
generatespamdict()
generategenuinedict()

system("clear")
print "SPAMWORDS"
if pgbr: raw_input()
for t in spamwords: print t+"\t", 
if pgbr: raw_input()
system("clear")
print "GENUINEWORDS"
if pgbr: raw_input()
for t in genuinewords: print t+"\t",
if pgbr: raw_input()
system("clear")
print "STOP WORDS"
if pgbr: raw_input()
for t in stopwords: print t+"\t",
if pgbr: raw_input()

if pgbr: system("clear")
print "SPAM DICTIONARY GENERATED"
if pgbr: raw_input()
for t in spamdict: print t+":"+str(spamdict[t])+"\t",
if pgbr: raw_input()

if pgbr: system("clear")
print "GENUINE DICTIONARY GENERATED"
if pgbr: raw_input()
for t in genuinedict: print t+":"+str(genuinedict[t])+"\t",
if pgbr: raw_input()

if pgbr: system("clear")
print "Starting to classify TEST DATA"
if pgbr: raw_input()
if pgbr: 
	for k in testfiles:
		system("clear")
		testdict = {}
		testwords = []	
		processtest(k)
		generatetestdict()

		spamdistance = eucledean(testdict, spamdict)
		genuinedistance = eucledean ( testdict, genuinedict)

		print "For " + str(k) + " SPAMDISTANCE is " + str(spamdistance) + " and GENUINEDISTANCE is " + str(genuinedistance) + "\n"
	
		if spamdistance > genuinedistance: result = "SPAM"
		elif genuinedistance > spamdistance: result = "GENUINE"
		else: result = "UNKOWN"	
		print "The file " + k + " is classified as " + result + " is that correct? (Y/N)"
		opinion = raw_input()
		if opinion.lower() == "y" : 
			print "Thank You"
		else: 
			print "Please enter the classification required for the file. (S) Spam or (G) Genuine"
			changeresult =raw_input()
			if changeresult.lower() == "s" : print "The file is now classified as SPAM"
			else: print "The file is now classified as GENUINE"
		raw_input()
else:
	system("clear")
	for k in testfiles:
		testdict = {}
		testwords = []	
		processtest(k)
		generatetestdict()
		spamdistance = eucledean(testdict, spamdict)
		genuinedistance = eucledean ( testdict, genuinedict)
		if spamdistance > genuinedistance: result = "SPAM"
		elif genuinedistance > spamdistance: result = "GENUINE"
		else: result = "UNKOWN"	
		print "The file " + k + " is classified as " + result,
		print "spamdistance" + str(spamdistance) + "genuinedistance" + str(genuinedistance)
		
