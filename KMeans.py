'''implements kmeans clustering
   see Page.py : Page class
'''
from sys import stdout

lvls = '00 CC 44 FF 88'.split() #not in order, for better color-contrast
colors = ['#'+R+G+B for R in lvls for G in lvls for B in lvls] #5**3==125 colors total
class KMeans:
    def __init__(self, K, page):
        print('initializing kmeans clusterer...'); stdout.flush()
        self.K=K
        self.page=page
        self.N=len(self.page.words)
        self.centers = [self.page.bb.random_pt_within() for k in range(K)]
        self.Estep() #initializes self.assignments
    def Estep(self):
        self.assignments = [coor.closest_cent(self.centers) for coor in self.page.words]
    def Mstep(self):
        for i in range(self.K):
            c = self.centers[i]
            c.from_point(c.center())
        for i in range(self.N):
            self.centers[self.assignments[i]].join_with(self.page.words[i])
    def draw_on(self, canvas, cbbcs):
        pbbcs = self.page.bb.coors
        for center,color in zip(self.centers, colors):
            center.draw_on(canvas, cbbcs, pbbcs, color, fill=color)
        for word,i in zip(self.page.words, range(len(self.page.words))):
            word.draw_on(canvas, cbbcs, pbbcs, colors[self.assignments[i]])
