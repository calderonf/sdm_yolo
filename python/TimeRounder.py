# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 18:08:21 2019

@author: francisco
"""

import datetime


def round_time_ceil(dt=None, round_to=60*15):
   if dt == None: 
       dt = datetime.datetime.now()
   print ("From: ")
   print (dt)
   seconds = (dt - dt.min).seconds
   rounding = (seconds+round_to) // round_to * round_to
   return dt + datetime.timedelta(0,rounding-seconds,-dt.microsecond)


if __name__ == "__main__":
    from time import sleep
    

    print ("*"*30)
    print (round_time_ceil())
    print (datetime.datetime.now()<round_time_ceil())
    print ("*"*30)
        
    
    #Ejemplo bucles cada cuarto de hora
    while(True):
        print( "Inicia nuevo ciclo")
        futrq=round_time_ceil()
        while (datetime.datetime.now()<futrq):
            print( "En espera")
            print(datetime.datetime.now())
            sleep(60)
    