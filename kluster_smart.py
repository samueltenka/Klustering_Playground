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
from Box.py import Box
master = Tk()

p = re.compile('<String ID="(?P<stringid>[^"]*)" ' +
               'STYLEREFS="(?P<stylerefs>[^"]*)" ' +
               'HEIGHT="(?P<height>[^"]*)" ' +
               'WIDTH="(?P<width>[^"]*)" ' +
               'HPOS="(?P<hpos>[^"]*)" ' +
               'VPOS="(?P<vpos>[^"]*)" ' +
               'CONTENT="(?P<content>[^"]*)" ' +
               'WC="(?P<wc>[^"]*)"/>')

with open('0005.xml') as f:
    text = f.read()
    getnum = lambda match, label: float(match.group(label))
    coordinates = [(getnum(m,'vpos')+0.5*getnum(m,'height'),
                    getnum(m,'hpos')+0.5*getnum(m,'width')) for m in p.finditer(text)]
    print('xml has %d characters, %d ocr points.' % (len(text), len(coordinates)))
xs = [[c[i] for c in coordinates] for i in range(2)]
miny, maxy, minx, maxx = min(xs[0]), max(xs[0]), min(xs[1]), max(xs[1])
print('vpos ranges in [%d,%d]; hpos ranges in [%d,%d]' % (miny, maxy, minx, maxx))

cnvs_h, cnvs_w = 480, 320
w = Canvas(master, height=cnvs_h, width=cnvs_w)
to_canvas = lambda coor: (cnvs_h * (coor[0]-miny)/(maxy-miny), cnvs_w * (coor[1]-minx)/(maxx-minx))
w.pack()

#kmeans klustering:
K = 100; N = len(coordinates); numsteps=100
def random_pt_within(self, other, bb):
    return Box([random()*(bb.coors[1][i]-bb.coors[0][i])+bb.coors[1][i] for i in range(2)])
centers = [random_pt_within() for k in range(K)]
assignments = [closest_cent(centers, coor) for coor in coordinates] #not DRY!

STEP=0
def render():
   global centers,assignments, STEP
   w.delete('all')

   for j in range(5):
       print('step %d...' % STEP); stdout.flush(); STEP+=1
       kluster_sums = [[0.0,0.0] for i in range(K)]
       kluster_mins = [list(centers[i]) for i in range(K)]
       kluster_maxs = [list(centers[i]) for i in range(K)]
       counts = [0 for i in range(K)]
       for i in range(N):
           accumulate(kluster_sums[assignments[i]], coordinates[i])
           acc_min(kluster_mins[assignments[i]], coordinates[i])
           acc_max(kluster_maxs[assignments[i]], coordinates[i])
           counts[assignments[i]] += 1
       kluster_avgs = [((c0[0]+c1[0])/2,(c0[1]+c1[1])/2) for c0,c1 in zip(kluster_mins, kluster_maxs)]
       for i in range(K):
           centers[i] = randcoor() if counts[i]==0 else scale(kluster_sums[i], 1.0/counts[i])
           #centers[i] = randcoor() if counts[i]==0 else kluster_avgs[i]
       assignments = [closest_cent(centers, coor) for coor in coordinates]

   lvls = '00 CC 44 FF 88'.split()
   colors = ['#'+R+G+B for R in lvls for G in lvls for B in lvls]
   for i in range(K):
       y,x = to_canvas(centers[i])
       y0,x0 = to_canvas(kluster_mins[i])
       y1,x1 = to_canvas(kluster_maxs[i])
       w.create_Box(x0,y0,x1,y1, outline=colors[i])
   for i in range(N):
       y,x = to_canvas(coordinates[i])
       w.create_Box(x, y, x+1, y+1, outline=colors[assignments[i]])

   if STEP<numsteps:
      w.after(100, render) #render 10 times a second

render()
mainloop()
