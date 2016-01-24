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

class Rectangle:
    point_metric = lambda c0,c1: max(abs(c1[0]-c0[0]),abs(c1[1]-c0[1]))
    def __init__(self, coor=None):
        '''0th coor is (miny,minx); 1th coor is (maxy,maxx)'''
        self.from_point([None]*2 if coor is None else coor)
    def draw_on(self, canvas):
        y,x = to_canvas(self.coors[0])
        Y,X = to_canvas(self.coors[1])
        w.create_rectangle(x,y,X,Y, outline=colors[assignments[i]])
    def center(self):
        return [sum(self.coors[i][j] for i in range(2))/2 for j in range(2)]
    def disconnect_distance(self, other):
        return min(-other.coors[1][0] + self.coors[0][0],
                   other.coors[1][0] - self.coors[1][0],
                   -other.coors[1][1] + self.coors[0][1],
                   other.coors[1][1] - self.coors[1][1])
    def overlaps(self, other): #TODO: check correctness!
        return disconnect_distance(self, other) < 0.0
    def dist_to(self, other):
        return point_metric(self.center(),other.center()) +\
               max(0, disconnect_distance(self, other))
    def join(self, other):
        rtrn = Rectangle(); stats = (min,max)
        rtrn.coors = [[stats[i](self.coors[i][j]) for j in range(2)] for i in range(2)]
        return rtrn
    def from_point(self, coor):
        self.coors = [coor[:]]*2
    def closest_cent(self, centers):
        return min((dist(centers[i],coor), i) for i in range(len(centers)))[1]

#kmeans klustering:
K = 100; N = len(coordinates); numsteps=100
def randomize_to_point(self, other):
    Rectangle rtrn()
    from_point([random()*(maxy-miny)+miny, random()*(maxx-minx)+minx])
centers = [Rectangle() for k in range(K)]
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
       w.create_rectangle(x0,y0,x1,y1, outline=colors[i])
   for i in range(N):
       y,x = to_canvas(coordinates[i])
       w.create_rectangle(x, y, x+1, y+1, outline=colors[assignments[i]])

   if STEP<numsteps:
      w.after(100, render) #render 10 times a second

render()
mainloop()
