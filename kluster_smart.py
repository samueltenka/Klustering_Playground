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
from Box import Box
from GetCoors import Page
from KMeans import KMeans

master = Tk()
canvasbb = Box((0,0),(480,320))
mycanvas = Canvas(master, height=canvasbb.coors[1][0], width=canvasbb.coors[1][1])
mycanvas.pack()

mypage = Page('0005.xml')
myclusterer = KMeans(K=100, page=mypage)

STEP=0; numsteps=100
def render():
    global mypage, mycanvas
    mycanvas.delete('all')

    lvls = '00 CC 44 FF 88'.split()
    colors = ['#'+R+G+B for R in lvls for G in lvls for B in lvls]
    for i in range(K):
        centers[i].draw_on(mycanvas, canvasbb.coors, mypage.bb.coors)
    for i in range(N):
        mypage.words[i].draw_on(mycanvas, canvasbb.coors, mypage.bb.coors)

    if STEP<numsteps:
        mycanvas.after(10, render) #render 100 times a second (or slower)

render()
mainloop()
