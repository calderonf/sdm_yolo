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
import os.path
#python3
#from urllib.request import Request, urlopen

#python2
from urllib2 import Request, urlopen
from time import gmtime, strftime, localtime,mktime# time, strptime, sleep



class Festivos:#clase festivos tomada de github...
    def __init__(self, ano):
        self.__festivos=[]
        self.__hoy=strftime("%d/%m/%Y")
        
        if ano == "":
            ano=strftime("%Y")
        
        self.__ano=ano
        pascua = self.__pascua(ano)
        self.__pascua_dia=pascua[0]
        self.__pascua_mes=pascua[1]
        primero=(ano,1,1)
        self.__festivos.append(primero)         #primero de enero
        trabajo=(ano,5,1)
        self.__festivos.append(trabajo)         #dia del trabajo
        independencia=(ano,7,20)
        self.__festivos.append(independencia)   #independecia de colombia
        boyaca=(ano,8,7)
        self.__festivos.append(boyaca)          #batalla de boyaca
        virgen=(ano,12,8)
        self.__festivos.append(virgen)          #dia de la velitas inmaculada concepcion
        navidad=(ano,12,25)
        self.__festivos.append(navidad)         #navidad

        self.__calcula_emiliani(1,6)            #reyes magos
        self.__calcula_emiliani(3,19)           #san jose
        self.__calcula_emiliani(6,29)           #San pedro y san pablo
        self.__calcula_emiliani(8,15)           #Asuncion de la Virgen
        self.__calcula_emiliani(10,12)          #Dia de la Raza
        self.__calcula_emiliani(11,1)           #Todos los Santos
        self.__calcula_emiliani(11,11)          #Independencia de Cartagena

        self.__otrasFechasCalculadas(-3)        #Jueves Santo
        self.__otrasFechasCalculadas(-2)        #Viernes Santo

        self.__otrasFechasCalculadas(43,True)   #Ascension de Jesus
        self.__otrasFechasCalculadas(64,True)   #Corpus Christi
        self.__otrasFechasCalculadas(71,True)   #Sagrado Corazon de Jesus

    def __calcula_emiliani(self, mes_festivo, dia_festivo):
        t = (self.__ano, mes_festivo, dia_festivo, 0, 0, 0, 0, 0, 0)
        dd =int(strftime("%w", localtime(mktime(t))))
        if dd == 0:
            dia_festivo = dia_festivo + 1
        elif dd == 2:
            dia_festivo = dia_festivo + 6
        elif dd == 3:
            dia_festivo = dia_festivo + 5
        elif dd == 4:
            dia_festivo = dia_festivo + 4
        elif dd == 5:
            dia_festivo = dia_festivo + 3
        elif dd == 6:
            dia_festivo = dia_festivo + 2
        t = (self.__ano, mes_festivo, dia_festivo , 0, 0, 0, 0, 0, 0)
        mes=int(strftime("%m", localtime(mktime(t))))
        dia=int(strftime("%d", localtime(mktime(t))))
        festivo=(self.__ano,mes,dia)
        self.__festivos.append(festivo)

    def __otrasFechasCalculadas(self, cantidadDias=0,siguienteLunes=False):
        suma = int(self.__pascua_dia)+int(cantidadDias)
        t = (self.__ano, self.__pascua_mes, suma, 0, 0, 0, 0, 0, 0)
        mes_festivo=int(strftime("%m", localtime(mktime(t))))
        dia_festivo=int(strftime("%d", localtime(mktime(t))))
        if siguienteLunes:
            self.__calcula_emiliani(mes_festivo, dia_festivo)
        else:
            festivo=(self.__ano,mes_festivo,dia_festivo)
            self.__festivos.append(festivo)
    
    def __pascua(self, anno):
        M = 24  
        N = 5
        a = anno % 19
        b = anno % 4
        c = anno % 7
        d = (19*a + M) % 30
        e = (2*b+4*c+6*d + N) % 7

        if d+e < 10  :
            dia = d+e+22
            mes = 3
        else:
            dia = d+e-9
            mes = 4

        if dia == 26  and mes == 4:
            dia = 19

        if dia == 25 and mes == 4 and d==28 and e == 6 and a >10:
            dia = 18

        return [dia, mes, anno]
    
    def esFestivo(self, mes, dia):
        return (self.__ano,mes,dia) in self.__festivos

    def ListarFestivos(self):
        print("Este anio tiene: ",len(self.__festivos),"dias festivos")
        print(self.__festivos)

class pypHoyGetTaxi:
    
    def __init__(self,verbose=True):
        self.verbose=verbose
        self.Ahora=datetime.date.today()
        self.link ="https://www.pyphoy.com/bogota/taxis?f=1"
        self.archivodata="pyptaxi.data"
        self.festivos=Festivos(self.Ahora.year)
        self.HoyesFestivo=self.festivos.esFestivo(self.Ahora.month,self.Ahora.day)
        
        if not os.path.isfile(self.archivodata):
            if self.verbose:
                print("No existe el archivo de pico y placa taxis, se crea...")
            self.refresqueRestriccionPyP()
        if self.archivoDesactualizado():
            self.refresqueRestriccionPyP()
            
    def refresqueRestriccionPyP(self):
        self.Ahora==datetime.date.today()
        self.festivos=Festivos(self.Ahora.year)
        self.HoyesFestivo=self.festivos.esFestivo(self.Ahora.month,self.Ahora.day)
        if not (self.Ahora.isoweekday()==7 or self.HoyesFestivo): # si no es domingo o festivo
            req = Request(self.link, headers={'User-Agent': 'Mozilla/5.0'})
            webpage = urlopen(req).read()
            webpagedec = webpage.decode('utf-8')
            #print(webpagedec)
            try:
                self.p1=int(webpagedec[webpagedec.find("plate is-public")+len("plate is-public")+2])
                self.p2=int(webpagedec[webpagedec.find("plate is-public")+len("plate is-public")+4])
            except:
                self.p1=int(webpagedec[webpagedec.find("plate public")+len("plate public")+2])
                self.p2=int(webpagedec[webpagedec.find("plate public")+len("plate public")+4])
            
            if self.verbose:
                print("Hoy tienen pico y placa: ",self.p1," y ",self.p2)
                
        else:
            self.p1=-1
            self.p2=-1
            if self.verbose:
                print("Hoy es domingo o festivo, no hay pico y placa, Dia=",self.Ahora.isoweekday()," festivo=",self.HoyesFestivo)
        
        myfile=open(self.archivodata,"w")
        myfile.write(str(self.Ahora))
        myfile.write("\n")
        myfile.write(str(self.p1))
        myfile.write("\n")
        myfile.write(str(self.p2))
        myfile.write("\n")
        myfile.write
        myfile.close()
        
    def archivoDesactualizado(self):
        try:
            file2=open(self.archivodata,"r")
            fecha=file2.readline()
            self.p1=int(file2.readline())
            self.p2=int(file2.readline())
            ahoracargado=datetime.date(int(fecha[0:4]),int(fecha[5:7]),int(fecha[8:10]))
            file2.close()
            if (self.Ahora==ahoracargado):
                if self.verbose:
                    print ("fecha del archivo actual corresponde, datos cargados correctamente")
                self.p1=p1
                self.p2=p2
                return False
            else:
                if self.verbose:
                    print ("fecha del archivo actual NO corresponde, se debe actuaizar")
                return True
        except:# si ocurre un error cualquiera, cree el archivode nuevo
            print ("error leyendo archivo revisar")
            return True
        return True
        
    def tienePyP(self):
        
        if self.Ahora==datetime.date.today():
            if(self.verbose):
                print("No cambia el dia, retornando pico y placa")
            if self.Ahora.isoweekday()==7:# si es domingo retorne False
                return (False,-1,-1)
            if self.HoyesFestivo:# si es festivo retorne False
                return (False,-1,-1)
            # de lo contrario retorne pico y placa
            return (True,self.p1,self.p2)
        else:
            print ("Cambia el dia, refrescando pico y placa")
            self.refresqueRestriccionPyP()
            if self.Ahora.isoweekday()==7 or self.HoyesFestivo :# si es domingo retorne False
                return (False,-1,-1)
            return (True,self.p1,self.p2)
            




class PicoYPlaca:
    """
    Clase pico y placa
    """
    def __init__(self,*args, **kwargs):
        """
        Funcion de inicialización       !PROBADA!
        Si no le entran argumentos los toma la hora del sistema y la fecha como la hora a ser procesada
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
        self.pyptaxi=pypHoyGetTaxi()
        
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
        
        self.fest=Festivos(self.fecha_actual.year)
        
        
        
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
            
            
        if ((not self.realtime) and tipo==self.taxi):
            print("WARNING:::::::::::::::::tipo taxi solo soporta REALTIME WARNING :::::::::::::::::::::::::::::::")
        
        
        
        if self.enRestriccion(tipo): # Si no esta el tipo en restriccion retornar Falso
            if tipo == self.particular:
                if self.placaPar(placa) and self.diaPar():
                    return True
                if self.placaImpar(placa) and self.diaImpar():
                    return True
                return False
                    
            elif tipo == self.taxi:
                digitostaxi=self.pyptaxi.tienePyP()
                if digitostaxi[0]:
                    p1=digitostaxi[1]
                    p2=digitostaxi[2]
                    if (self.ultimoDigito(placa,p1) or self.ultimoDigito(placa,p2)):
                        return True
                else:
                    print ("%"*30)
                    print ("%"*30)
                    print ("%"*30)
                    print ("WARNING NO DEBERIA ENTRAR ACA --"+tipo+"-- WARNING NO DEBE ENTRAR ACA YA SE REVISO RESTRICCION")
                    print ("%"*30) 
                    print ("%"*30)
                    print ("%"*30)
                    return False
                
                
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
        self.ahora=datetime.datetime.now()
        if not self.fecha_actual==datetime.date.today():
            self.fecha_actual=datetime.date.today()
            self.fest=Festivos(self.fecha_actual.year)
        
        
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
        
        if tipo==self.particular:
            
            maini=datetime.datetime(self.fecha_actual.year,self.fecha_actual.month,self.fecha_actual.day,6,0,0)#6:00am a 8:30am
            mafin=datetime.datetime(self.fecha_actual.year,self.fecha_actual.month,self.fecha_actual.day,8,30,0)
            
            evini=datetime.datetime(self.fecha_actual.year,self.fecha_actual.month,self.fecha_actual.day,15,0,0)#3:00pm a 7:30pm
            evfin=datetime.datetime(self.fecha_actual.year,self.fecha_actual.month,self.fecha_actual.day,19,30,0)
            
            if self.diaHabil():
                if self.ahora>=maini and self.ahora<=mafin:
                    return True
                if self.ahora>=evini and self.ahora<=evfin:
                    return True
        if tipo==self.taxi:
            
            maini=datetime.datetime(self.fecha_actual.year,self.fecha_actual.month,self.fecha_actual.day,5,30,0)#5:30am a 21:00
            mafin=datetime.datetime(self.fecha_actual.year,self.fecha_actual.month,self.fecha_actual.day,21,0,0)
            
            if not self.esFeriado():
                if self.ahora>=maini and self.ahora<=mafin:
                    return True
            
            
            
            #return pyptaxi.tienePyP()[0]
                
        return False
            
    def diaHabil(self):
        """
        Funcion que retorna si es un dia habil o no !PROBADA!
        """
        dia=self.fecha_actual.weekday()
        if dia==5 or dia==6:# Si es sabado o Domingo
            return False
        return True
        
    def esFeriado(self):
        """
        Funcion que retorna si es un dia feriado en Colombia o domingo
        """
        esfestivo=self.fest.esFestivo(self.fecha_actual.month,self.fecha_actual.day)
        dia=self.fecha_actual.weekday()
        
        if esfestivo or dia==6:# Si hoy es festivo o Domingo
            return True
        return False    
    
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

    def ultimoDigito(self,placa,digito):
        """
        Funcion que retorna si el ultimo digito de la placa corresponde al pedido  !PROBADA!
        por ahora solo es valido si la placa termina en numero.
        
        """
        esplaca=self.esPlaca(placa)
        tipo=self.tipoPlaca(placa)

        if esplaca and tipo== self.particular:
            if int(placa[-1])==digito:
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
    

    guiasini("ultimoDigito")
    for placa in placas:
        print ("probando placa " ,placa," Retorna ",pp.ultimoDigito(placa,9))
    
    guiasfin("ultimoDigito")    
    
    
    
    
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
    
    guiasini("pypHoyGetTaxi")
    
    pyptaxi=pypHoyGetTaxi()
    print(pyptaxi.tienePyP())
    
    guiasfin("pypHoyGetTaxi")
    
    guiasini("Festivos")
    
    fest=Festivos(2019)
    
    print(u"Listado Festivos del año: ")
    fest.ListarFestivos()
    guiasfin("Festivos")    
    
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
    print ("Probando Particulares:")
    print ("probando enRestriccion HOY=" ,pp.ahora," Retorna ",pp.enRestriccion(pp.particular))
    
    for itera in range(len(fechasytiempo)):
        fecha=fechas[itera]
        ftemp=fechasytiempo[itera]
        pp=PicoYPlaca(fecha,ftemp)
        print ("probando enRestriccion " ,pp.ahora," Retorna ",pp.enRestriccion(pp.particular))
        
    print ("Probando taxis:")
    print ("probando enRestriccion HOY=" ,pp.ahora," Retorna ",pp.enRestriccion(pp.taxi))
    
    for itera in range(len(fechasytiempo)):
        fecha=fechas[itera]
        ftemp=fechasytiempo[itera]
        pp=PicoYPlaca(fecha,ftemp)
        print ("probando enRestriccion " ,pp.ahora," Retorna ",pp.enRestriccion(pp.taxi))
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
    
    
    guiasini("tienePicoYPlaca TAXI")
    pp=PicoYPlaca()
    print ("probando tienePicoYPlaca, Placa ","BFA850" ," Fecha: ", pp.fecha_actual," ",pp.ahora," Retorna ",pp.tienePicoYPlaca("BFA853",pp.taxi))
    
    pp=PicoYPlaca()
    for itera in range(len(fechasytiempo)):
        fecha=fechas[itera]
        ftemp=fechasytiempo[itera]
        placa=placas[itera]
        pp=PicoYPlaca(fecha,ftemp)
        pp.tienePicoYPlaca(placa,tipo="taxi")
        print ("probando tienePicoYPlaca, Placa ",placa ," Fecha: ", pp.fecha_actual," ",pp.ahora," Retorna ",pp.tienePicoYPlaca(placa,pp.taxi))
    
    
    guiasfin("tienePicoYPlaca TAXI")
    
    
    
    
    
    
    
    
    
    
        
        
        