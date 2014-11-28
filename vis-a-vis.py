import os
import subprocess
import numpy as np

papers = 'papers.tbl'
# read in the papers.tbl file
url, num = np.loadtxt(papers, dtype='string',
                      delimiter=',', unpack=True)


## TO DO
## redo this with urllib2 or beautiful soup, not downloading with wget
## instead of grep and sed use pythonic regular expressions, etc
## send email (maybe with linux mail command) when done if new papers

for i in range(0,len(url)):
    # run wget on each URL
    os.system('wget '+url[i]+' -O test'+str(i)+'.html')
    
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


