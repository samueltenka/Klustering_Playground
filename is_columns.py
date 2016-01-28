from Box import Box
from Page import Page
from myFFT import periodicity
#from KMeans import KMeans

def columnation_of(filename, num_bins=1024): #must be pow of 2
    mypage = Page(filename)
    get_xs = lambda mybox: tuple(mybox.coors[i][1] for i in range(2))

    histogram = [0 for i in range(num_bins)]
    xstart, xend = get_xs(mypage.bb)
    to_bin = lambda x: int(num_bins*float(x-xstart)/(xend-xstart))
    for w in mypage.words:
        xmin, xmax = get_xs(w)
        for i in range(to_bin(xmin), to_bin(xmax)): #off-by-1?
            histogram[i] += 1

    s = sum(histogram)
    if s==0: return -1 #'article has no text'
    histogram  = [float(h)/s for h in histogram]
    #print(histogram[:3])

    return periodicity(histogram)

import os
path = "C:\\Users\\Samuel\\Desktop\\Batch 1\\Batch 1\\sn85042289\\15032502570\\1961110101\\"
myfiles = [(columnation_of(path+file), file)
           for file in os.listdir(path) if file.endswith(".xml")]
myfiles.sort()
for c,f in myfiles:
    print(f,c)
