import PySimpleGUI as sg
from pyparsing import col

class GUI:
    def elegir(self):
        opcion=0
        sg.theme("DarkGrey5")
        layout=[[sg.Text("Compilador :) ")],[sg.Text()],[sg.Button("Seleccionar archivo")],[sg.Exit()]]
        ventana=sg.Window("Bienvenido",layout,finalize="true")
        while True:
            event,values=ventana.read()
            if event in (None, "Exit"):
                opcion=0
                break
            elif event in (None,"Seleccionar archivo"):
                opcion=1
                break
           
        ventana.close()
        return opcion
    
    def mensaje(self,titulo,mensaje):
        sg.theme("DarkGrey5")
        layout=[[sg.Text(mensaje)],[sg.Exit()]]
        ventana=sg.Window(titulo,layout,finalize="true")
        while True:
            event,values=ventana.read()
            if event in (None, "Exit"):
                break
        ventana.close()
