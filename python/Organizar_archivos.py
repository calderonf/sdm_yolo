#!/usr/bin/python2
# -*- coding: utf-8 -*-

import easygui
import os
import glob

def weekDay(year, month, day):
    year=int(year)
    month=int(month)
    day=int(day)
    offset = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    week   = ['Domingo', 
              'Lunes', 
              'Martes', 
              'Miercoles', 
              'Jueves',  
              'Viernes', 
              'Sabado']
    afterFeb = 1
    if month > 2: afterFeb = 0
    aux = year - 1700 - afterFeb
    # dayOfWeek for 1700/1/1 = 5, Friday
    dayOfWeek  = 5
    # partial sum of days betweem current date and 1700/1/1
    dayOfWeek += (aux + afterFeb) * 365                  
    # leap year correction    
    dayOfWeek += aux / 4 - aux / 100 + (aux + 100) / 400     
    # sum monthly and day offsets
    dayOfWeek += offset[month - 1] + (day - 1)               
    dayOfWeek %= 7
    return week[dayOfWeek]





folder=easygui.diropenbox(title="Seleccione la carpeta con los de videos a organizar",default="/Videos")
filelistavi=glob.glob(folder+"/*.avi")
filelistavi.sort()


for fll in filelistavi:
    fl=os.path.basename(fll.rstrip())
    pp=fl.split("_")
    flyear=(pp[1][0:4])
    flmonth=(pp[1][4:6])
    flday=(pp[1][6:8])
    flhour=(pp[1][8:10])
    flmin=(pp[1][10:12])
    flseg=(pp[1][12:14])
  
    directory=folder+"/"+(flyear)+(flmonth)+(flday)+"_"+str(weekDay(flyear,flmonth,flday))
    if not os.path.exists(directory):
        print "Se crea carpeta:"
        print directory
        os.makedirs(directory)
    print "Se mueve archivo"
    print fl 
    print "de"
    print fll
    print "a"
    print directory+"/"+fl
    os.rename(fll, directory+"/"+fl)






#print weekDay(1985,5,8)
#print weekDay(2018,8,25)
