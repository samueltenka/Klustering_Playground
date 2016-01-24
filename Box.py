class Box:
    point_metric = lambda c0,c1: max(abs(c1[0]-c0[0]),abs(c1[1]-c0[1]))
    def __init__(self, coor0=None, coor1=None):
        '''0th coor is (miny,minx); 1th coor is (maxy,maxx)'''
        if coor2 is None:
            self.from_point([None]*2 if coor0 is None else coor0)
        else:
            self.coors = [coor0,coor1]
    def draw_on(self, canvas):
        y,x = to_canvas(self.coors[0])
        Y,X = to_canvas(self.coors[1])
        w.create_Box(x,y,X,Y, outline=colors[assignments[i]])
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
        rtrn = Box(); stats = (min,max)
        rtrn.coors = [[stats[i](self.coors[i][j]) for j in range(2)] for i in range(2)]
        return rtrn
    def from_point(self, coor):
        self.coors = [coor[:]]*2
    def closest_cent(self, centers):
        return min((dist(centers[i],coor), i) for i in range(len(centers)))[1]
