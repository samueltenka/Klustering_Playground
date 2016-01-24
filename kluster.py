'''
parses xml file of ocr'd string-location data:
   <String ID="TB.0005.2_0_0" STYLEREFS="TS_10.0" HEIGHT="156.0" WIDTH="448.0" HPOS="540.0" VPOS="1908.0" CONTENT="121st" WC="1.0"/>
and clusters
'''
import re
from math import sqrt
from random import random
from sys import stdout

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
K = 10; N = len(coordinates)
print('defining lambdas...')
randcoor = lambda : (random()*(maxx-minx)+minx, random()*(maxy-miny)+miny)
dist = lambda c0, c1: sqrt((c1[0]-c0[0])**2+(c1[1]-c0[1])**2)
closest_cent = lambda centers, coor: min((dist(centers[i],coor), i) for i in range(K))[1]
def accumulate(c0, c1):
    c0[0] += c1[0]
    c0[1] += c1[1]
def scale(c, scale):
    c0[0] *= scale
    c0[1] *= scale

centers = [randcoor() for k in range(K)]
assignments = [closest_cent(centers, coor) for coor in coordinates] #not DRY!
for i in range(100):
   print('step %d...' % i); stdout.flush()
   kluster_sums = [[0.0,0.0] for i in range(K)]
   counts = [0 for i in range(K)]
   for i in range(N): accumulate(kluster_sums[assignments[i]], coordinates[i])
   for i in range(K): centers[i] = randcoor() if counts[i]==0 else kluster_sums[i]/counts[i]
   assignments = [closest_cent(centers, coor) for coor in coordinates]
