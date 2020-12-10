'''
this is a really stupidly written script to check if my papers have been cited

you feed it a list of papers (ADS links) and citations, and it will only check on those.
this is better for me than the ADS tool because it only checks a specific list of papers

it returns info if new citation found, and updated h-index

you could script it with cron, if you want
'''

import os
# import subprocess
import ads
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


def run_papers(papers = 'papers.tbl', dir = '/python/vis-a-vis/', makefig=True):
    home = os.path.expanduser("~")
    run_dir = home + dir

    # read in the papers.tbl file
    df = read_csv(run_dir + papers, names=('bibcodes', 'num'))
    bibcodes = df['bibcodes'].values
    num = np.array(df['num'].values, dtype='float')
    h0 = h_indx(num)

    for k in range(len(bibcodes)):
        article = list(ads.SearchQuery(bibcode=bibcodes[k], fl=['citation_count']))[0]
        num_k = article.citation_count
        if num_k != num[k]:
            print(str(int(num_k-float(num[k]))) +
                  ' new citations for paper: https://ui.adsabs.harvard.edu/abs/'+bibcodes[k])
            print('\a') # make the computer "beep"
            num[k] = num_k

    ss = np.argsort(num)

    # write updated output file
    # np.savetxt(papers, np.column_stack((url, num)), delimiter=',', fmt="%s")
    dfout = DataFrame(data = {'a':bibcodes[ss], 'b':num[ss]})
    dfout.to_csv(run_dir + papers, header=False, index=False, index_label=False, columns=['a', 'b'], encoding='ascii')

    # if h-index goes up, alert
    h1 = h_indx(num)

    if h1>h0:
        print( 'h-index increased from '+str(h0)+' to '+str(h1))
        print('\a') # make the computer "beep"
    else:
        print( 'h-index still is '+str(h1))

    # make a figure
    if makefig:
        plt.figure()
        plt.plot(np.arange(1,len(num)+1), num[ss][::-1], '-o')
        plt.title('H-index='+str(h1)+', '+str(datetime.datetime.today()))
        plt.xlabel('Paper')
        plt.ylabel('Citations')
        plt.savefig(run_dir + 'cite_count.png', dpi=150, bbox_inches='tight', pad_inches=0.25)
        plt.close()



if __name__ == "__main__":
    '''
      let this file be called from the terminal directly. e.g.:
      $ python vis-a-vis.py
    '''
    run_papers()
