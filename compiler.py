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
        file_path = "filedialog.askopenfilename()"
        if file_path.endswith(".asc"):
            compile("file_path")
        elif file_path=="":
            gui.mensaje("Error","Archivo no seleccionado")
        else:
            gui.mensaje("Error","Archivo no soportado")
            main()
def verificarRAM(num):
    if int(num,16)<=int("00FF",16):
        return True
    return False
def verificarRAMROM(num):
    if int(num,16)<=int("FFFF",16):
        return True
    return False

def verificarMneumonico(ins,str):
    try:
        var=ins[str]
    except KeyError:
        return False
    return True

def verificarInherente(ins,str):
    try:
        var=ins[str]["inh"]
        
    except KeyError:
        return False
    return True

def verificarInmediato(ins,str):
    try:
        var=ins[str]["imm"]
    except KeyError:
        return False
    return True

def verificarDirecto(ins,str):
    try:
        var=ins[str]["dir"]
    except KeyError:
        return False
    return True

def verificarExtendido(ins,str):
    try:
        var=ins[str]["ext"]
    except KeyError:
        return False
    return True

def verificarIndexado(ins,str):
    try:
        var=ins[str]["indx"]
    except KeyError:
        return False
    return True


def compile(path):
    errorList=[]
    gui=GUI()
    hasEnd=False
    num=str()
    file=open(path, "r")
    instructionSet=loadInstructionSet()
    l=file.readlines()
    lineCounter=0
    currentORG=0
    dicVariables=dict()
    dicEtiquetas=dict()
    for line in l:
        lineCounter=lineCounter+1
        if line=="\n":

            continue
        newLine=line.replace("\n"," ").lower()
        linePrint=line.replace("\n"," ")
        lineComponents=newLine.strip().split(" ")
        #print(lineComponents)
        isMneumonico=verificarMneumonico(instructionSet,lineComponents[0])
        if newLine.startswith(" ") or newLine.startswith("\t"): #Verifica si tiene un espacio relativo al margen
            if isMneumonico: #Si la tiene y es una instruccion valida, revisa de qué modo de direccionamiento se trata

                #Verificar si es inherente
                if verificarInherente(instructionSet,lineComponents[0]): 
                    if len(lineComponents)>1:
                        print(f"Linea {lineCounter}: Error 6, instruccion no lleva operando")
                        errorList.append(f"Linea {lineCounter}: Error 6, instruccion no lleva operando")

                        continue
                    print(f"{lineCounter}: {hex(currentORG).removeprefix('0x')} ({instructionSet[lineComponents[0]]['inh']['opCode']})\t\t: {linePrint}") #Cambiar print a escribir a archivo
                    currentORG=currentORG+instructionSet[lineComponents[0]]['inh']['byteSize']

                    continue
                if len(lineComponents)==1: #Como no es inherente debe tener operando, si no lo tiene, arroja error
                    print(f"Linea {lineCounter}: Error 5, instruccion carece de operando(s)")
                    errorList.append(f"Linea {lineCounter}: Error 5, instruccion carece de operando(s)")

                    continue

                #Verificar si es inmediato
                if verificarInmediato(instructionSet,lineComponents[0]): #Verificar que a la instruccion soporte direccionamiento inmediato
                    if lineComponents[1].startswith("#"): #Verifica que ademas de soportarlo, lo esté utilizando
                        tempNum=lineComponents[1].removeprefix("#")
                        if tempNum.startswith("$"):
                            num=tempNum.removeprefix("$")
                            if len(num)==1 or len(num)==3:
                                num=f'0{num}'
                        else:
                            try:
                                num=hex(int(tempNum)).removeprefix("0x")
                            except ValueError: 
                                try:
                                    num=dicVariables[lineComponents[1].removeprefix("#")]
                                except KeyError:
                                    print(f"Linea {lineCounter}: Error, variable inexistente{num}")
                                    errorList.append(f"Linea {lineCounter}: Error, variable inexistente")
                                    continue
                        if verificarRAMROM(num):
                            print(f"{lineCounter}: {hex(currentORG).removeprefix('0x')} ({instructionSet[lineComponents[0]]['imm']['opCode']}{num})\t\t: {linePrint}") #Cambiar print a escribir a archivo
                            currentORG=currentORG+instructionSet[lineComponents[0]]['imm']['byteSize']
                        else:
                            print(f"Linea {lineCounter}: Error 7, magnitud de operando erronea")
                            errorList.append(f"Linea {lineCounter}: Error 7, magnitud de operando erronea")
                        continue

                #Verificar si es indexado
                if verificarIndexado(instructionSet,lineComponents[0]):
                    if lineComponents[1].startswith("#"):
                        print(f"Linea {lineCounter}: Error, modo de direccionamiento no soportado")
                        errorList.append(f"Linea {lineCounter}: Error, modo de direccionamiento no soportado")
                        continue
                    opIndex=lineComponents[1].split(",")
                    if len(opIndex)>1:
                        if opIndex[0].startswith("$"):
                            num=opIndex[0].removeprefix("$")
                            if len(num)==1 or len(num)==3:
                                num=f'0{num}'
                        else:
                            try:
                                num=hex(int(opIndex[0])).removeprefix("0x")
                            except ValueError: #Cambiar por uso de etiquetas
                                try:
                                    num=dicVariables[opIndex[0]]
                                except KeyError:
                                    print(f"Linea {lineCounter}: Error, variable inexistente {num}")
                                    errorList.append(f"Linea {lineCounter}: Error, variable inexistente")
                                    continue
                        if verificarRAM(num):
                            if opIndex[1]=="x":
                                print(f"{lineCounter}: {hex(currentORG).removeprefix('0x')} ({instructionSet[lineComponents[0]]['indx']['opCode']}{num})\t\t: {linePrint}") #Cambiar print a escribir a archivo
                                currentORG=currentORG+instructionSet[lineComponents[0]]['indx']['byteSize']
                            elif opIndex[1]=="y":
                                print(f"{lineCounter}: {hex(currentORG).removeprefix('0x')} ({instructionSet[lineComponents[0]]['indy']['opCode']}{num})\t\t: {linePrint}") #Cambiar print a escribir a archivo
                                currentORG=currentORG+instructionSet[lineComponents[0]]['indy']['byteSize']
                            else:
                                print(f"Linea {lineCounter}: Error, indexado incorrecto")
                                errorList.append(f"Linea {lineCounter}: Error, indexado incorrecto")
                            continue
                        else:
                            if not verificarExtendido:
                                print(f"Linea {lineCounter}: Error 7, magnitud de operando erronea")
                                errorList.append(f"Linea {lineCounter}: Error 7, magnitud de operando erronea")
                #Verificar si es directo
                if verificarDirecto(instructionSet,lineComponents[0]):
                    if lineComponents[1].startswith("#"):
                        print(f"Linea {lineCounter}: Error, modo de direccionamiento no soportado")
                        errorList.append(f"Linea {lineCounter}: Error, modo de direccionamiento no soportado")

                        continue
                    if lineComponents[1].startswith("$"):
                        num=lineComponents[1].removeprefix("$")
                        if len(num)==1 or len(num)==3:
                            num=f'0{num}'
                    else:
                        try:
                            num=hex(int(lineComponents[1])).removeprefix("0x")
                        except ValueError: #Cambiar por uso de etiquetas
                            try:
                                num=dicVariables[lineComponents[1]]
                            except KeyError:
                                print(f"Linea {lineCounter}: Error, variable inexistente {num}")
                                errorList.append(f"Linea {lineCounter}: Error, variable inexistente")
                                continue
                    if verificarRAM(num):
                        print(f"{lineCounter}: {hex(currentORG).removeprefix('0x')} ({instructionSet[lineComponents[0]]['dir']['opCode']}{num})\t\t: {linePrint}") #Cambiar print a escribir a archivo
                        currentORG=currentORG+instructionSet[lineComponents[0]]['dir']['byteSize']
                        continue
                    else:
                        if not verificarExtendido:
                            print(f"Linea {lineCounter}: Error 7, magnitud de operando erronea")
                            errorList.append(f"Linea {lineCounter}: Error 7, magnitud de operando erronea")

                            
                #Verificar si es extendido
                if verificarExtendido(instructionSet,lineComponents[0]):
                    if lineComponents[1].startswith("#"):
                        print(f"Linea {lineCounter}: Error, modo de direccionamiento no soportado")
                        errorList.append(f"Linea {lineCounter}: Error, modo de direccionamiento no soportado")

                        continue
                    if lineComponents[1].startswith("$"):
                        num=lineComponents[1].removeprefix("$")
                        if len(num)==1 or len(num)==3:
                                num=f'0{num}'
                    else:
                        try:
                            num=hex(int(lineComponents[1])).removeprefix("0x")
                        except ValueError:
                            try:
                                num=dicVariables[lineComponents[1]]
                            except KeyError:
                                print(f"Linea {lineCounter}: Error, variable inexistente")
                                errorList.append(f"Linea {lineCounter}: Error, variable inexistente")
                                continue
                    
                    if verificarRAMROM(num):
                        print(f"{lineCounter}: {hex(currentORG).removeprefix('0x')} ({instructionSet[lineComponents[0]]['ext']['opCode']}{num})\t\t: {linePrint}") #Cambiar print a escribir a archivo
                        currentORG=currentORG+instructionSet[lineComponents[0]]['ext']['byteSize']
                    else:
                        print(f"Linea {lineCounter}: Error 7, magnitud de operando erronea")
                        errorList.append(f"Linea {lineCounter}: Error 7, magnitud de operando erronea")
                    continue

            #Si se trata de org
            elif lineComponents[0]=="org": 
                if lineComponents[1].startswith("$"):
                        num=int(lineComponents[1].removeprefix("$"),16)
                else:
                    num=int(lineComponents[1])
                currentORG=num
            else:
                print(f"Linea {lineCounter}: Error 4, mneumonico inexistente")
                errorList.append(f"Linea {lineCounter}: Error 4, mneumonico inexistente")


        else: #Si no tiene espacio relativo al margen
            if isMneumonico: #Si además es una instruccion del MC68HC11, marca error
                print(f"Linea {lineCounter}: Error 9, instruccion carece de espacio relativo al margen")
                errorList.append(f"Linea {lineCounter}: Error 9, instruccion carece de espacio relativo al margen")
                continue
            if len(lineComponents)>1:
                if(lineComponents[1])=="equ":
                    try:
                        if lineComponents[2].startswith("$"):
                            num=lineComponents[2].removeprefix("$")
                        else:
                            num=hex(int(lineComponents[2])).removeprefix("0x")
                        dicVariables[lineComponents[0]]=num
                    except KeyError:
                       dicVariables[lineComponents[0]]="0"
                continue
            if lineComponents[0]=="end":
                hasEnd=True
                break
    if hasEnd==False:
        print(f"Linea {lineCounter+1}: Error 10, no se encuentra END")
        errorList.append(f"Linea {lineCounter+1}: Error 10, no se encuentra END")

def  loadInstructionSet():
    return IS.getInstructionSet()

compile("compilador/code.asc")