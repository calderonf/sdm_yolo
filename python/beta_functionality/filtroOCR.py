# -*- coding: utf-8 -*-
"""
Created on Sat Jul  6 20:14:16 2019

@author: francisco
"""

#s1=[('E', 0.833227276802063, (7.773296356201172, 11.036909103393555, 8.591050148010254, 16.373933792114258)), ('D', 0.8816303014755249, (8.20012378692627, 11.049068450927734, 9.364285469055176, 16.476924896240234)), ('M', 0.622424304485321, (14.926791191101074, 11.932206153869629, 7.48298454284668, 17.82145881652832)), ('R', 0.8999488949775696, (21.121110916137695, 12.924960136413574, 9.40836238861084, 18.275907516479492)), ('9', 0.9184494614601135, (32.066375732421875, 13.831130981445312, 8.259383201599121, 16.552345275878906)), ('3', 0.9161961674690247, (40.11615753173828, 14.460262298583984, 7.8487677574157715, 15.728691101074219)), ('1', 0.8604661822319031, (46.80643081665039, 14.646771430969238, 6.965776443481445, 16.99363899230957))]
#s2=[('Y', 0.7354421615600586, (21.822696685791016, 10.582317352294922, 10.570930480957031, 14.14423656463623)), ('0', 0.6817562580108643, (35.974124908447266, 10.743364334106445, 9.117761611938477, 16.873655319213867)), ('M', 0.6290832161903381, (15.611699104309082, 10.408123970031738, 9.562665939331055, 13.761083602905273)), ('C', 0.4327918291091919, (51.39061737060547, 10.773151397705078, 9.01660442352295, 17.06894302368164)), ('B', 0.38255247473716736, (6.807430267333984, 10.29312515258789, 8.45710563659668, 13.097220420837402)), ('W', 0.37903112173080444, (6.426553249359131, 10.008864402770996, 9.220621109008789, 14.07129192352295)), ('Y', 0.37711092829704285, (43.55257797241211, 11.514595031738281, 8.161310195922852, 15.499324798583984)), ('Z', 0.3583143651485443, (51.2105712890625, 11.570274353027344, 8.652822494506836, 16.271259307861328)), ('7', 0.2667195200920105, (51.2105712890625, 11.570274353027344, 8.652822494506836, 16.271259307861328)), ('D', 0.24833934009075165, (6.807430267333984, 10.29312515258789, 8.45710563659668, 13.097220420837402))]

def compareCharacters(cra,crb,delta=2.0):
    cxa=cra[2][0]
    cxb=crb[2][0]
    distancia=abs(cxa-cxb)
    if distancia<delta:
        return True
    return False
def promedioAnchos(OCR):
    promedio=0
    for char in OCR:
        promedio+=char[2][2]
    return promedio/len(OCR)
def minorConfidence(cra,crb,i,j):
    if cra[1]>crb[1]:
        return j
    return i
def eliminarRepetidos(OCR,pceliminacion=0.2):
    """
    funcion que elimina los caracteres repetidos en las detecciones de OCR, si estas detecciones son muy cercanas 
    se eliminan la cercania esta dada por que tan juntas estan en su coordenada x
    se puede aumentar esta diferencia aumentando el PCeliminacion por ahora esta en 20%
    """
    if len(OCR)<=6:# Si tiene menos de 6 o 6 letras retorne la misma cadena de detecciones
        return OCR
    paraeliminar=[]
    promedio=promedioAnchos(OCR)
    for i in range(len(OCR)):
        for j in range(i + 1, len(OCR)):
            if compareCharacters(OCR[i], OCR[j],delta=promedio*pceliminacion):
                paraeliminar.append(minorConfidence(OCR[i], OCR[j],i,j))
    paraeliminar=list(set(paraeliminar))# quitar elementos repetidos
    for i in sorted(paraeliminar, reverse=True):
        if len(OCR)<=6:
            break
        del OCR[i]
    return OCR





#p1=eliminarRepetidos(s1)

#p2=eliminarRepetidos(s2)
