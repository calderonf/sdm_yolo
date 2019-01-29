# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 15:05:46 2018

@author: francisco
"""

import cv2
import numpy as np
import collections

Params = collections.namedtuple('Params', ['a','b','c']) #to store equation of a line

def calcParams(point1, point2): #line's equation Params computation
    if point2[1] - point1[1] == 0:
         a = 0
         b = -1.0
    elif point2[0] - point1[0] == 0:
        a = -1.0
        b = 0
    else:
        a = float(point2[1] - point1[1]) / float(point2[0] - point1[0])
        b = -1.0

    c = (-a * point1[0]) - b * point1[1]
    print ('parametros',a,b,c)
    return Params(a,b,c)

def areLinesIntersecting(params1, params2, point1, point2):
    det = float(params1.a) * float(params2.b) - float(params2.a) * float(params1.b)
    print ("det ",det)
    if det == 0:
        return False #lines are parallel
    else:
        x = (params2.b * -params1.c - params1.b * -params2.c)/det
        y = (params1.a * -params2.c - params2.a * -params1.c)/det
        print("intersecting in: [", x,",",y,"]")
        if x <= max(point1[0],point2[0]) and x >= min(point1[0],point2[0]) and y <= max(point1[1],point2[1]) and y >= min(point1[1],point2[1]):
            
            cv2.circle(frame,(int(x),int(y)),4,(0,0,255), -1) #intersecting point
            return True #lines are intersecting inside the line segment
        else:
            return False #lines are intersecting but outside of the line segment

cv2.namedWindow('frame')
frame = np.zeros((240,320,3), np.uint8)

last_centroid = (200,200) #centroid of a car at t-1
centroid = (50,160) #centroid of a car at t

line_params = calcParams(last_centroid, centroid)
intercept_line_params = calcParams((0,170), (300,170))
print("Params:", line_params.a,line_params.b,line_params.c) 

while(1):
    cv2.circle(frame,last_centroid,4,(0,255,0), -1) #last_centroid
    cv2.circle(frame,centroid,4,(0,255,0), -1) #current centroid
    cv2.line(frame,last_centroid,centroid,(0,0,255),1) #segment line between car centroid at t-1 and t
    cv2.line(frame,(0,170),(300,170),(200,200,0),2) #intercepting line
    print("AreLinesIntersecting: ",areLinesIntersecting(intercept_line_params,line_params,last_centroid,centroid)) 
    cv2.imshow('frame',frame)
    if cv2.waitKey(5000) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()