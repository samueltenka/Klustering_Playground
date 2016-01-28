from Box import Box
from Page import Page
from myFFT import FFT, periodicity
#from KMeans import KMeans

def histogram_of(filename, num_bins=1024):
    '''num_bins must be power of 2'''
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
    if s==0: return None #return -1 #article has no text
    return [float(h)/s for h in histogram]

def FFT_columnation_of(histogram):
    return periodicity(histogram)
def var_columnation_of(histogram):
    return 1.0/sum((h-1.0/len(histogram))**2 for h in histogram)

import os, sys
from matplotlib import pyplot as plt
path = "C:\\Users\\Samuel\\Desktop\\Batch 1\\Batch 1\\sn85042289\\15032502570\\1961110101\\"
files = [] #(columnation score, filename, histogram) tuples
for f in (f for f in os.listdir(path) if len(f)==len('0000.xml') and f.endswith(".xml")):
   print('processing %s...' %f); sys.stdout.flush()
   h = histogram_of(path+f)
   if h is None: continue
   vc = var_columnation_of(h)
   files.append((vc,f,h))

files.sort()
for (c,f,h),i in zip(files,range(len(files))):
   plt.plot(h) #plt.plot(FFT(h))
   plt.title('var_columnation(%s) = %f'%(f,var_columnation_of(h)))
   plt.savefig('%d_plot_%s.png' % (i,f))
   plt.clf()
