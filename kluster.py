'''
parses xml file of ocr'd string-location data:
   <String ID="TB.0005.2_0_0" STYLEREFS="TS_10.0" HEIGHT="156.0" WIDTH="448.0" HPOS="540.0" VPOS="1908.0" CONTENT="121st" WC="1.0"/>
and clusters
'''
import re
from math import sqrt
from random import random
from sys import stdout

from tkinter import *
master = Tk()

print('defining lambdas...')
p = re.compile('<String ID="(?P<stringid>[^"]*)" ' +
               'STYLEREFS="(?P<stylerefs>[^"]*)" ' +
               'HEIGHT="(?P<height>[^"]*)" ' +
               'WIDTH="(?P<width>[^"]*)" ' +
               'HPOS="(?P<hpos>[^"]*)" ' +
               'VPOS="(?P<vpos>[^"]*)" ' +
               'CONTENT="(?P<content>[^"]*)" ' +
               'WC="(?P<wc>[^"]*)"/>')

print('defining lambdas...')
with open('0005.xml') as f:
    text = f.read()
    coordinates = [(float(m.group('vpos')), float(m.group('hpos'))) for m in p.finditer(text)]
    print('xml has %d characters, %d ocr points.' % (len(text), len(coordinates)))
xs = [[c[i] for c in coordinates] for i in range(2)]
miny, maxy, minx, maxx = min(xs[0]), max(xs[0]), min(xs[1]), max(xs[1])
print('vpos ranges in [%d,%d]; hpos ranges in [%d,%d]' % (miny, maxy, minx, maxx))

cnvs_h, cnvs_w = 480, 320
w = Canvas(master, height=cnvs_h, width=cnvs_w)
to_canvas = lambda coor: (cnvs_h * (coor[0]-miny)/(maxy-miny), cnvs_w * (coor[1]-minx)/(maxx-minx))
w.pack()
#for c in coordinates:
#    y,x = to_canvas(c)
#    w.create_rectangle(x, y, x+1, y+1, outline="blue",fill="blue")

#kmeans klustering:
K = 8; N = len(coordinates); numsteps=40;
print('defining lambdas...')
randcoor = lambda : (random()*(maxy-miny)+miny, random()*(maxx-minx)+minx)
def dist(c0,c1):
    #print(c0, c1)
    return max(abs(c1[0]-c0[0]),abs(c1[1]-c0[1]))
#dist = lambda c0, c1: max(abs(c1[0]-c0[0]),abs(c1[1]-c0[1])) #sqrt((c1[0]-c0[0])**2+(c1[1]-c0[1])**2)
closest_cent = lambda centers, coor: min((dist(centers[i],coor), i) for i in range(K))[1]
def accumulate(c0, c1):
    c0[0] += c1[0]
    c0[1] += c1[1]
def acc_max(c0, c1):
    c0[0] = max(c0[0], c1[0])
    c0[1] = max(c0[1], c1[1])
def acc_min(c0, c1):
    c0[0] = min(c0[0], c1[0])
    c0[1] = min(c0[1], c1[1])
def scale(c, scale):
    return (c[0]*scale, c[1]*scale)

centers = [randcoor() for k in range(K)]
assignments = [closest_cent(centers, coor) for coor in coordinates] #not DRY!
for i in range(numsteps):
   print('step %d...' % i); stdout.flush()
   kluster_sums_min = [[miny,minx] for i in range(K)]
   kluster_sums_max = [[maxy,maxx] for i in range(K)]
   counts = [0 for i in range(K)]
   for i in range(N):
       acc_min(kluster_sums_min[assignments[i]], coordinates[i])
       acc_max(kluster_sums_max[assignments[i]], coordinates[i])
       counts[assignments[i]] += 1
   for i in range(K):
       #centers[i] = randcoor() if counts[i]==0 else scale(kluster_sums[i], 1.0/counts[i])
       accumulate(kluster_sums_max[i],kluster_sums_min[i])
       centers[i] = randcoor() if counts[i]==0 else scale(kluster_sums_max[i], 1.0/2.0)
   assignments = [closest_cent(centers, coor) for coor in coordinates]

lvls = '00 FF'.split()
colors = ['#'+R+G+B for R in lvls for G in lvls for B in lvls]

for i in range(K):
    y,x = to_canvas(centers[i])
    w.create_rectangle(x, y, x+10, y+10, outline=colors[i])
for i in range(N):
    y,x = to_canvas(coordinates[i])
    w.create_rectangle(x, y, x+1, y+1, outline=colors[assignments[i]])
mainloop()
