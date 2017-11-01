'''
this is a really stupidly written script to check if my papers have been cited

you feed it a list of papers (ADS links) and citations, and it will only check on those.
this is better for me than the ADS tool because it only checks a specific list of papers

it returns info if new citation found, and updated h-index

it requires wget. I had to install it using homebrew for my Mac.

you could script it with cron, if you want
'''

import os
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import datetime
from pandas import read_csv, DataFrame


def h_indx(num):
    '''
    compute the h-index for a string of numbers (citation counts)
    '''
    fnum = np.array(num, dtype='float')
    s = np.argsort(fnum)[::-1]
    ind = np.arange(len(s))+1
    return sum(fnum[s] >= ind)


home = os.path.expanduser("~")
dir = home + '/python/vis-a-vis/'
papers = 'papers.tbl'

# read in the papers.tbl file
# url, num = np.loadtxt(dir + papers, dtype='str',
#                       delimiter=',', unpack=True)

df = read_csv(dir + papers, names=('url', 'num'))
num = np.array(df['num'].values, dtype='float')
url = df['url'].values

h0 = h_indx(num)

## TO DO
## redo this with urllib2 or beautiful soup, not downloading with wget like a chump
## instead of grep and sed use pythonic regular expressions, etc
## send email (maybe with linux mail command) when done if new papers found
## use ADS API (but, needs dev key)

for i in range(0,len(url)):
    # run wget on each URL
    os.system('wget '+url[i]+' -O ' + dir + 'test'+str(i)+'.html -q')

    # use grep to scrape out the number of citations
    o = subprocess.check_output('grep ">Citations to the Article" '+dir+'test'+
                                str(i)+'.html | wc',shell=True)
    yn = float( o.split()[0] )

    # if that = 0, then no hits
    if (yn != 0):
        o2 = float(
            subprocess.check_output('grep ">Citations to the Article (" '+dir+'test'+
                                    str(i)+'.html | sed "s|[^(]*(\([^)]*\)).*|\\1|"',
                                    shell=True) )
        #print o2==float(num[i])
        if (o2 != float(num[i])):
            print(str(int(o2-float(num[i]))) +
                  ' new citations for paper '+url[i])
            print('\a') # make the computer "beep"

            num[i] = str(int(o2))

    os.system('rm test'+str(i)+'.html')


ss = np.argsort(num)

# write updated output file
# np.savetxt(papers, np.column_stack((url, num)), delimiter=',', fmt="%s")
dfout = DataFrame(data = {'a':url[ss], 'b':num[ss]})
dfout.to_csv(dir + papers, header=False, index=False, index_label=False, columns=['a', 'b'], encoding='ascii')


# if h-index goes up, alert
h1 = h_indx(num)

if h1>h0:
    print( 'h-index increased from '+str(h0)+' to '+str(h1))
else:
    print( 'h-index still is '+str(h1))


# make a figure
plt.figure()
plt.plot(num[ss], '-o')
plt.title('H-index='+str(h1)+', '+str(datetime.datetime.today()))
plt.xlabel('Paper')
plt.ylabel('Citations')
plt.savefig(dir + 'cite_count.png', dpi=150, bbox_inches='tight', pad_inches=0.25)
plt.close()
