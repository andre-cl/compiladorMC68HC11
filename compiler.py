from gui import GUI
import tkinter as tk
from tkinter import filedialog
from instructionSet import IS

def main():
    gui=GUI()
    opcion=gui.elegir()
    if opcion==1:
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        if file_path.endswith(".asc"):
            compile(file_path)
        elif file_path=="":
            gui.mensaje("Error","Archivo no seleccionado")
        else:
            gui.mensaje("Error","Archivo no soportado")
            main()

def compile(path):
    errorList=[]
    gui=GUI()
    file=open(path, "r")
    instructionSet=loadInstructionSet()
    l=file.readlines()
    lineCounter=1
    for line in l:
        newLine=line.replace("\n"," ").lower()
        print(newLine)
        if newLine.startswith(" ") or newLine.startswith("\t"):
            lineComponents=newLine.strip().split(" ")
            print(lineComponents)
            try:
            
                print(instructionSet[lineComponents[0]])
            except KeyError:
                print(f"Linea {lineCounter}: Error 4, mneumonico inexistente")
                errorList.append(f"Linea {lineCounter}: Error 4, mneumonico inexistente")
        else:
            print("Esto es una etiqueta")
        lineCounter=lineCounter+1

def  loadInstructionSet():
    return IS.getInstructionSet()
      
main()