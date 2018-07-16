import sys
import re
from prettytable import PrettyTable

buildslist = []

def useless(buildslist):
    logdict = {}
    testdict = {}
    #buildslist = [126,127,128,129,130]
    listlen = len(buildslist)
    for i in buildslist:
        with open('/var/lib/jenkins/jobs/itrust_job2/builds/'+str(i)+'/log', 'r') as logfile:
            logdata_list=logfile.readlines()
        loglen = len(logdata_list)
        #print "Length of logs"+str(i)+" : "+str(loglen)
        j = 0
        while (j<loglen):
            test = re.search("Tests run: (\d+), Failures: 0,.*- in (.*)\n",logdata_list[j])
	    if test:
		if (logdict.has_key(test.group(2))):
		    temp = logdict.get(test.group(2))
                    if temp:
                        temp+=1
                        logdict.update({test.group(2):temp})
			testdict.update({test.group(2):int(test.group(1))})
	        else:
	     	    logdict.update({test.group(2):1})
		    testdict.update({test.group(2):int(test.group(1))})
	    j+=1
    values = logdict.values()
    logtestlist = logdict.keys()
    vallen = len(values)
    uselesstests = []
    uselesscount = []
    uselesscountsum = 0
    for i in range(vallen):
	if values[i]==listlen:
	    uselesstests.append(logtestlist[i])
	    uselesscount.append(testdict[logtestlist[i]])
	    uselesscountsum+=testdict[logtestlist[i]]

    logfile.close()
    t = PrettyTable(['Useless Test','No of tests'])
    k = 0
    while k < len(uselesstests):
	t.add_row([uselesstests[k],uselesscount[k]])
        k+=1

    print t
    #print uselesstests
    print "Number of useless tests: "+str(uselesscountsum)
    print "Exited Useless test detector!"



#useless(buildslist)
