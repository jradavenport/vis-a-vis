'''
this is a really stupidly written script to check if my papers have been cited

you feed it a list of papers (ADS links) and citations, and it will only check on those. 
this is better for me than the ADS tool because it only checks a specific list of papers

it returns info if new citation found, and updated h-index

you could script it with cron, if you want
'''

import os
import subprocess
import numpy as np


def h_indx(num):
    fnum = np.array(num,dtype='float')
    s = np.argsort(fnum)[::-1]
    ind = np.arange(len(s))+1
    return sum(fnum[s] >= ind)

papers = 'papers.tbl'
# read in the papers.tbl file
url, num = np.loadtxt(papers, dtype='string',
                      delimiter=',', unpack=True)

h0 = h_indx(num)

## TO DO
## redo this with urllib2 or beautiful soup, not downloading with wget like a chump
## instead of grep and sed use pythonic regular expressions, etc
## send email (maybe with linux mail command) when done if new papers found
## use ADS API (but, needs dev key)

for i in range(0,len(url)):
    # run wget on each URL
    os.system('wget '+url[i]+' -O test'+str(i)+'.html -q')
    
    # use grep to scrape out the number of citations
    o = subprocess.check_output('grep ">Citations to the Article" test'+
                                str(i)+'.html | wc',shell=True)
    yn = float( o.split()[0] )

    # if that = 0, then no hits
    if (yn != 0):
        o2 = float(
            subprocess.check_output('grep ">Citations to the Article (" test'+
                                    str(i)+'.html | sed "s|[^(]*(\([^)]*\)).*|\\1|"',
                                    shell=True) )
        #print o2==float(num[i])
        if (o2 != float(num[i])):
            print str(int(o2-float(num[i]))) + ' new citations for paper '+url[i]
            num[i] = str(int(o2))
    os.system('rm test'+str(i)+'.html')

# write updated output file
np.savetxt(papers, np.column_stack((url, num)), delimiter=',', fmt="%s")

# if number increased, send email

# if h-index goes up, alert
h1 = h_indx(num)

if h1>h0:
    print 'h-index increased from '+str(h0)+' to '+str(h1)
else:
    print 'h-index still is '+str(h1)

