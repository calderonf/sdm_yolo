# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 10:19:27 2018

@author: calderonf
"""

class rect:
    """
    Clase de rectangulo, que contiene dos puntos, [x,y] y [u,v] con \n
    las esquinas del rectangulo contenedor\n
    """
    def __init__(self, x, y, u, v):
        """
        Inicializacion\n
        """
        self.x = x
        self.y = y
        self.u = u
        self.v = v
        self.w = u-x
        self.h = v-y
        
        
    def retPoints(self):
        """
        Funcion que retorna dos parejas ordenadas, util para usar en conjunto con cv2\n
        """
        return ((self.x,self.y),(self.u,self.v))
        
    def retInitPoint(self):
        """
        Funcion que retorna una pareja ordenada de inicio de punto\n
        """
        return (self.x,self.y)
        
    def retEndPoint(self):
        """
        Funcion que retorna una pareja ordenada de fin de punto\n
        """
        return (self.u,self.v)
        
    def retSize(self):
        """
        Funcion que retorna el tama;o del rectangulo\n
        """
        return (self.w,self.h)
        
    def retArea(self):
        """
        Funcion que retorna el area del rectangulo\n
        """
        return float((((self.u-self.x)+1)*(1+(self.v-self.y))))
        
    def isRectInside(self,rt):
        """
        Funcion que retorna si el tectangulo esta contenido en otro rectangulo\n
        """
        if (self.x>rt.u or rt.x>self.u):
            return False
        elif (self.v<rt.y or rt.v<self.y):
            return False
        else:
            return True

    def retCommPC(self,rt):
        """
        Funcion que retorna el area comun , el porcentaje (por uno en realidad de 0 a 1) comun que tiene un rectangulo en otro sin importar la referencia. si este da 100 es que son iguales
        y el porcentaje en comun que tiene con respecto al mas pequenio de los dos, si este ultimo da 1 pero el anterior no es que uno esta contenido en otro
                                
        """
        if self.isRectInside(rt):
            x=max(self.x,rt.x)
            y=max(self.y,rt.y)
            u=min(self.u,rt.u)
            v=min(self.v,rt.v)
            Acomm=float((u-x+1)*(v-y+1))
            Amin=min(self.retArea(),rt.retArea())
            return (Acomm,Acomm/(self.retArea()+rt.retArea()-Acomm),Acomm/Amin)
        else:
            return (0.0,0.0,0.0)
            


if __name__ == "__main__":
    
    r1=rect(1,1,10,10)
    r2=rect(10,10,20,20)
    r3=rect(11,11,20,20)
    r4=rect(1,1,20,20)
    r4=rect(-11,11,0,0)
    
    r10=rect(1,1,8,8)
    r11=rect(2,2,6,6)
    
    print "Este test debe retornar 100.0"
    print r1.retArea()
    
    print "Este test debe retornar 121.0"
    print r2.retArea()
    
    print "estos dos test deben retornar True"
    print r1.isRectInside(r2)
    print r2.isRectInside(r1)
    
    print "estos dos test deben retornar False"
    print r1.isRectInside(r3)
    print r3.isRectInside(r1)
    
    print "este test debe retornar: (1.0, 0.004545454545454545)"
    print r1.retCommPC(r2)
    
    
    print "este test debe retornar: (100.0, 1.0)"
    print r1.retCommPC(r1)
    
    
    print "este test debe retornar: (0.0, 0.0)"
    print r1.retCommPC(r3)
    
    print "este test debe retornar: (0.0, 0.0)"
    print r1.retCommPC(r4)
    
    
    print "este test debe retornar: "
    print r10.retCommPC(r11)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    