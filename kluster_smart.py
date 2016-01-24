'''
parses xml file of ocr'd string-location data:
   <String ID="TB.0005.2_0_0" STYLEREFS="TS_10.0" HEIGHT="156.0" WIDTH="448.0" HPOS="540.0" VPOS="1908.0" CONTENT="121st" WC="1.0"/>
and clusters
'''
from sys import stdout

from Box import Box
from Page import Page
from KMeans import KMeans
from tkinter import *

master = Tk()
canvasbb = Box((0,0),(480,320))
mycanvas = Canvas(master, height=canvasbb.coors[1][0], width=canvasbb.coors[1][1])
mycanvas.pack()

mypage = Page('0005.xml')
myclusterer = KMeans(K=100, page=mypage)

STEP=0; numsteps=100
def render():
    global STEP, numsteps, mycanvas, mypage, myclusterer
    print('step %d...' % STEP); STEP+=1; stdout.flush()
    mycanvas.delete('all')
    myclusterer.Mstep()
    myclusterer.Estep()
    myclusterer.draw_on(mycanvas, canvasbb.coors)
    if STEP<numsteps:
        mycanvas.after(10, render) #render 100 times a second (or slower)

render()
mainloop()
