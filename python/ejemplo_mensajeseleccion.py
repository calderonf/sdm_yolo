import easygui
title  ="Cuantas lineas de conteo?"
msg = "Seleccione el numero de lineas de conteo que quiere poner, se recomiendan maximo 6 lineas de conteo"
choices = ["1", "2", "3", "4", "5", "6"]
choice = easygui.choicebox(msg, title, choices)
type(choice)
lineasDeConteo=int(choice)
print "usted ha seleccionado ",lineasDeConteo," lineas de conteo"
