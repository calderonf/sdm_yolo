#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@author: Francisco Carlos Calderon
Created on Sun Jun 16 19:29:19 2019


Este modulo implementa llamados de validacion de pico y placa\n 
puede ser llamado desde esta misma carpeta o invocado como un modulo aparte\n


Para generar la documentacion del modulo ejecute desde una terminal en el directorio raiz del modulo:\n

  python -m pydoc -w picoyplaca\n
  
  A continuacion se listan prerequisitos o 'modulos',  clases y funciones implementadas.\n
  
"""
import re
import datetime

class PicoYPlaca:
    """
    Clase pico y placa
    """
    def __init__(self,*args, **kwargs):
        """
        Funcion de inicialización       !PROBADA!
        Si no le entrarn argumentos los toma la hora del sistema y la fecha como la hora a ser procesada
        Si le entra un argumento toma este como la fecha
        Si le entran dos argumentos toma estos como la fecha y la hora        
        
        """
        if len(args)==0:
            self.realtime=True
        else:
            self.realtime=False
        self.particular="particular"
        self.moto="moto"
        
        self.taxi="taxi"
        
        if self.realtime:
            self.fecha_actual=datetime.date.today()
            self.ahora=datetime.datetime.now()
        else:
            if len(args)==1:
                print ("WARNING: USANDO MODO NO REALTIME DE DEBUG DATE ONLY")
                print ("fecha en: ")
                self.fecha_actual=args[0]
                print (self.fecha_actual)
            elif len(args)==2:
                print ("WARNING: USANDO MODO NO REALTIME DE DEBUG DATETIME")
                print ("fecha en: ")
                self.fecha_actual=args[0]
                self.ahora=args[1]
                print (self.fecha_actual)
                print (self.ahora)
                
            else:
                print ("ERROR: si realtime no es True debe proveer una fecha")
    def tienePicoYPlaca(self, placa,tipo="particular"):
        """
        Funcion que determina si una placa tiene pico y placa en el momento actual
        dependiendo del tipo del vehículos                                                    !PROBADA!
        """
        placa=placa.upper()
        tipo=tipo.lower()
        if not self.esPlaca(placa):
            return False
        
        if self.realtime:
            self.refrescarFecha()
            
        if self.enRestriccion(tipo): # Si no esta el tipo en restriccion retornar Falso
            if tipo == self.particular:
                if self.placaPar(placa) and self.diaPar():
                    return True
                if self.placaImpar(placa) and self.diaImpar():
                    return True
                return False
                    
            elif tipo == self.taxi:
                print ("por implementar")
                return False
            else:
                print ("*"*30)
                print ("*"*30)
                print ("*"*30)
                print ("ERROR TIPO --"+tipo+"-- NO DEFINIDO")
                print ("*"*30)
                print ("*"*30)
                print ("*"*30)
                return False
        return False
        
    def refrescarFecha(self):
        """
        Funcion que refresca la fecha a una fecha actual,  !PROBADA!
        """
        self.fecha_actual=datetime.date.today()
        self.ahora=datetime.datetime.now()
        
        
    def diaPar(self):
        """
        Funcion que retorna si el dia es par o impar !PROBADA!
        """
        if self.realtime:
            self.refrescarFecha()
        dia=self.fecha_actual.day
        if dia%2==0:
            return True
        return False
        
        
    def diaImpar(self):
        """
        Funcion que retorna si el dia es impar o par !PROBADA!
        """
        if self.realtime:
            self.refrescarFecha()
        dia=self.fecha_actual.day
        if dia%2==1:
            return True
        return False
        
    def enRestriccion(self,tipo):
        """
        Funcion que retorna si el tipo de vehiculo se encuentra en restriccion   !PROBADA!
        
        Los tipos soportados son:
            self.particular:
                https://www.pyphoy.com/bogota/particulares
                Días de apliación:
                    Lunes
                    Martes
                    Miércoles
                    Jueves
                    Viernes
                No Aplica los días festivos
                
                Horario
                    6:00am a 8:30am
                    3:00pm a 7:30pm
                Clase de vehículos
                    Vehículos automotores de servicio particular
                Esquema
                    Último dígito del número de la placa
                
            self.taxi NO IMPLEMENTADO
            self.moto NO IMPLEMENTADO
        """
        
        if self.realtime:
            self.refrescarFecha()
        
        maini=datetime.datetime(self.fecha_actual.year,self.fecha_actual.month,self.fecha_actual.day,6,0,0)#6:00am a 8:30am
        mafin=datetime.datetime(self.fecha_actual.year,self.fecha_actual.month,self.fecha_actual.day,8,30,0)
        
        evini=datetime.datetime(self.fecha_actual.year,self.fecha_actual.month,self.fecha_actual.day,15,0,0)#3:00pm a 7:30pm
        evfin=datetime.datetime(self.fecha_actual.year,self.fecha_actual.month,self.fecha_actual.day,19,30,0)
        
        if tipo==self.particular:
            if self.diaHabil():
                if self.ahora>=maini and self.ahora<=mafin:
                    return True
                if self.ahora>=evini and self.ahora<=evfin:
                    return True
                
        return False
            
    def diaHabil(self):
        """
        Funcion que retorna si es un dia habil o no !PROBADA!
        """
        dia=self.fecha_actual.weekday()
        if dia==5 or dia==6:# Si es sabado o Domingo
            return False
        return True
        
    def esPlaca(self,placa):
        """
        Funcion que retorna si es una placa valida !PROBADA!
        """
        placa=placa.upper()
        if (len(placa)==6):
            match=re.search(r'[A-Z][A-Z][A-Z][0-9][0-9][0-9]', placa)
            if match:
                return True,self.particular
            match=re.search(r'[A-Z][A-Z][A-Z][0-9][0-9][A-Z]', placa)
            if match:
                return True,self.moto
            return False,"invalida_formato" 
        else:
            return False,"invalida_longitud"   
            
    def tipoPlaca(self,placa):
        """
        Funcion que retorna si es una placa valida !PROBADA!
        """
        placa=placa.upper()
        if (len(placa)==6):
            match=re.search(r'[A-Z][A-Z][A-Z][0-9][0-9][0-9]', placa)
            if match:
                return self.particular
            match=re.search(r'[A-Z][A-Z][A-Z][0-9][0-9][A-Z]', placa)
            if match:
                return self.moto
            return "invalida_formato" 
        else:
            return "invalida_longitud"   
        
        
    def placaPar(self,placa):
        """
        Funcion que retorna si es una placa par !PROBADA!
        """
        esplaca=self.esPlaca(placa)
        tipo=self.tipoPlaca(placa)
        if esplaca and tipo== self.particular:
            if int(placa[-1])%2==0:
                    return True
        return False
            
        
    def placaImpar(self,placa):
        """
        Funcion que retorna si es una placa impar !PROBADA!
        """
        esplaca=self.esPlaca(placa)
        tipo=self.tipoPlaca(placa)
        if esplaca and tipo== self.particular:
            if int(placa[-1])%2==1:
                    return True
        return False

if __name__ == "__main__":
    def guiasini(inn):
        print (" ")
        print (" ")
        print("="*30,inn,"="*30)
    def guiasfin(inn):
        print("#"*30,inn,"#"*30)
    
    pp=PicoYPlaca()
    placas=["ABC123","ABC12A","ABC1234","AB132","ABC124", "abc444", "jns239"]
    
    guiasini("esPlaca")
    print ("probando funcion esPlaca:")
    for placa in placas:
        print ("probando placa " ,placa," Retorna ",pp.esPlaca(placa))
    guiasfin("esPlaca")
    
    guiasini("tipoPlaca")
    print ("probando funcion tipoPlaca:")
    for placa in placas:
        print ("probando placa " ,placa," Retorna ",pp.tipoPlaca(placa))
    guiasfin("tipoPlaca")
    
    guiasini("placaPar")
    for placa in placas:
        print ("probando placa " ,placa," Retorna ",pp.placaPar(placa))
    guiasfin("esPlaca")
    
    guiasini("placaImpar")
    for placa in placas:
        print ("probando placa " ,placa," Retorna ",pp.placaImpar(placa))
    guiasfin("placaImpar")
    
    fechas=[datetime.date(2019,6,17),datetime.date(2019,6,18),datetime.date(2019,6,19),datetime.date(2019,6,20),datetime.date(2019,6,21),datetime.date(2019,6,22),datetime.date(2019,6,23)]

    guiasini("diaPar")
    pp=PicoYPlaca()
    print ("probando diaPar HOY=" ,pp.fecha_actual," Retorna ",pp.diaPar())
    
    for fecha in fechas:
        pp=PicoYPlaca(fecha)
        print ("probando diaPar " ,pp.fecha_actual," Retorna ",pp.diaPar())
    guiasfin("diaPar")
    
    guiasini("diaImpar")
    pp=PicoYPlaca()
    print ("probando diaImpar HOY=" ,pp.fecha_actual," Retorna ",pp.diaImpar())
    
    for fecha in fechas:
        pp=PicoYPlaca(fecha)
        print ("probando diaImpar " ,pp.fecha_actual," Retorna ",pp.diaImpar())
    guiasfin("diaImpar")
    
    guiasini("diaHabil")
    pp=PicoYPlaca()
    print ("probando diaHabil HOY=" ,pp.fecha_actual," Retorna ",pp.diaHabil())
    
    for fecha in fechas:
        pp=PicoYPlaca(fecha)
        print ("probando diaHabil " ,pp.fecha_actual," Retorna ",pp.diaHabil())
    guiasfin("diaHabil")
    
    
    
    fechas=[datetime.date(2019,6,17),datetime.date(2019,6,18),datetime.date(2019,6,19),datetime.date(2019,6,20),datetime.date(2019,6,21),datetime.date(2019,6,22),datetime.date(2019,6,23)]
    fechasytiempo=[datetime.datetime(2019,6,17,7,15,00),datetime.datetime(2019,6,18,8,15,00),datetime.datetime(2019,6,19,6,30,30),datetime.datetime(2019,6,20,14,15,45),datetime.datetime(2019,6,21,16,15,00),datetime.datetime(2019,6,22,16,15,00),datetime.datetime(2019,6,23,16,15,00)]
    placas=["ABC123","ABC123","ABC124","ABC124","ABC125", "abc444", "jns239"]
    
    guiasini("enRestriccion")
    pp=PicoYPlaca()
    print ("probando enRestriccion HOY=" ,pp.ahora," Retorna ",pp.enRestriccion(pp.particular))
    
    for itera in range(len(fechasytiempo)):
        fecha=fechas[itera]
        ftemp=fechasytiempo[itera]
        pp=PicoYPlaca(fecha,ftemp)
        print ("probando enRestriccion " ,pp.ahora," Retorna ",pp.enRestriccion(pp.particular))
    guiasfin("enRestriccion")
    
    
    fechas=[datetime.date(2019,6,17),datetime.date(2019,6,18),datetime.date(2019,6,19),datetime.date(2019,6,20),datetime.date(2019,6,21),datetime.date(2019,6,22),datetime.date(2019,6,23)]
    fechasytiempo=[datetime.datetime(2019,6,17,7,15,00),datetime.datetime(2019,6,18,8,15,00),datetime.datetime(2019,6,19,6,30,30),datetime.datetime(2019,6,20,14,15,45),datetime.datetime(2019,6,21,16,15,00),datetime.datetime(2019,6,22,16,15,00),datetime.datetime(2019,6,23,16,15,00)]

    guiasini("tienePicoYPlaca")
    pp=PicoYPlaca()
    print ("probando tienePicoYPlaca, Placa ","BFA850" ," Fecha: ", pp.fecha_actual," ",pp.ahora," Retorna ",pp.tienePicoYPlaca("BFA850",pp.particular))
    
    pp=PicoYPlaca()
    for itera in range(len(fechasytiempo)):
        fecha=fechas[itera]
        ftemp=fechasytiempo[itera]
        placa=placas[itera]
        pp=PicoYPlaca(fecha,ftemp)
        pp.tienePicoYPlaca(placa,tipo="particular")
        print ("probando tienePicoYPlaca, Placa ",placa ," Fecha: ", pp.fecha_actual," ",pp.ahora," Retorna ",pp.tienePicoYPlaca(placa,pp.particular))
    
    
    guiasfin("tienePicoYPlaca")
    
    
    
    
    
    
    
    
    
    
    
        
        
        