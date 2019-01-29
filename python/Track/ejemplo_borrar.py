# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 17:40:01 2018

@author: francisco
"""
ej=[1,2,3,4,5,6,7,8,9,10,9,8,7,6,5,4,3,2,1,-1]
def getMinItem(a):
    idx=min(range(len(a)), key=a.__getitem__)    
    return (idx,a[idx])
    
    
ret=getMinItem(ej)


pesos = [[1000000 for x in range(6)] for y in range(4)]

print 'minimo encontrado en :'
print ret(0)
print "y vale"
print ret(1)





print 'antes'
print ej
print '     '
for el in ej[:]:
    if el>2:
        ej.remove(el)

print 'despues:'
print ej
print '     '