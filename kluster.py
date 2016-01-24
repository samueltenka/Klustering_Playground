'''
parses xml file of ocr'd string-location data:
   <String ID="TB.0005.2_0_0" STYLEREFS="TS_10.0" HEIGHT="156.0" WIDTH="448.0" HPOS="540.0" VPOS="1908.0" CONTENT="121st" WC="1.0"/>
and clusters
'''
import re
from math import sqrt
from random import random

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
    coordinates = [(int(float(m.group('height'))), int(float(m.group('width')))) for m in p.finditer(text)]
    print('xml has %d characters, %d ocr points.' % (len(text), len(coordinates)))
xs = [[c[i] for c in coordinates] for i in range(2)]
minx, maxx, miny, maxy = min(xs[0]), max(xs[0]), min(xs[1]), max(xs[1])
print('height ranges in [%d,%d]; width ranges in [%d,%d]' % (minx, maxx, miny, maxy))

#kmeans klustering:
K = 100; N = len(coordinates)
print('defining lambdas...')
randcoor = lambda: (random()*(maxx-minx)+minx, random()*(maxy-miny)+miny)
centers = [[randcoor()] for k in range(K)] #extra[]layer for identity-permanence
print('defining lambdas...')
dist = lambda c0, c1: sqrt((c1[0]-c0[0])**2+(c1[1]-c0[1])**2)
closest = lambda coor: min((dist(c[0],coor), c) for c in centers)[1]
print('defining lambdas...')
assignments = [closest(coor) for coor in coordinates] #not DRY!
#avg = lambda clist: randcoor() if len(clist)==0 else (sum(c[0] for c in clist)/len(clist), sum(c[1] for c in clist)/len(clist))
#kluster_avg = lambda cent: avg([c for c in coordinates if assignments[i]==cent])

for i in range(100):
   print('step %d...' % i)
   kluster_sums = [[0.0,0.0] for i in range(K)]
   for i in range(N):
       assignments[i]
   centers = [[kluster_avg(c)] for c in centers]
   assignments = [closest(coor) for coor in coordinates]'''
