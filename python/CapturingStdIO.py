#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 20:17:16 2019

@author: francisco
"""

# import StringIO for Python 2 or 3
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import sys

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout

if __name__ == "__main__":
    import cv2
    fn='rtsp://movil:egccol@186.29.90.163:8891/EGC'
    fn2='rtsp://multiview:egccol@186.29.90.163:8891/Multiview'
    fn3='rtsp://movil:egccol@186.29.90.163:8891/CamFull2'
    cam = cv2.VideoCapture(fn)
    
    
    
    while True:# se itera 5 segundo para estabilizar la conexion
        with Capturing() as output:
            ret_val, imgFile2 = cam.read()
        #if len(output)>0:
        print ("Salida del io: ")
        print (output)
        print (len(output))
        
        if not ret_val:
            print ('ERROR:  no se pudo abrir la camara, saliendo')
            break
        cv2.imshow('streaming',imgFile2)
        k = cv2.waitKey(1)& 0xFF
        if k==ord('q') or k==ord('Q'):
            break
    cv2.destroyWindow('streaming')
    cv2.destroyAllWindows()
    cv2.waitKey(3)
    cv2.waitKey(30)
    cv2.waitKey(300)