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
            main()
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

def verificarRelativo(ins,str):
    try:
        var=ins[str]["rel"]
    except KeyError:
        return False
    return True

def placeRel(lista,rel,stri):
    i=-1
    for e in lista:
        
        i=i+1
        splitList=e.split(":")
        try:
            if rel[0]<int(splitList[0]):
                
                lista.insert(i,stri)
                break
        except ValueError:
            
            continue
    return lista

def placeRelHtml(lista,lista2,rel,stri):
    i=-1
    for e in lista:
        
        i=i+1
        splitList=e.split(":")
        try:
            if rel[0]<int(splitList[0]):
                
                lista2.insert(i,stri)
                break
        except ValueError:
            
            continue
    return lista2

def compileBrsetAndBrclr(dict):
    op1=dict["lineComponents"][1].split(",")
    if len(op1)==2:
        if op1[0].startswith("#"):
            print(f"Linea {dict['lineCounter']}: Error, modo de direccionamiento no soportado")
            dict["errorList"].append(f"Linea {dict['lineCounter']}: Error, modo de direccionamiento no soportado")
            return
        if op1[0].startswith("$"):
            num=op1[0].removeprefix("$")
            if len(num)==1 or len(num)==3:
                num=f'0{num}'
        else:
            try:
                num=hex(int(op1[0])).removeprefix("0x")
            except ValueError: 
                try:
                    num=dict["dicVariables"][op1[0]]
                except KeyError:
                    print(f"Linea {dict['lineCounter']}: Error, variable inexistente {num}")
                    dict["errorList"].append(f"Linea {dict['lineCounter']}: Error, variable inexistente")
                    return
        if verificarRAM(num):
                if op1[1].startswith("#"): #Verifica que ademas de soportarlo, lo esté utilizando
                    tempNum=op1[1].removeprefix("#")
                    if tempNum.startswith("$"):
                        num2=tempNum.removeprefix("$")
                        if len(num)==1 or len(num)==3:
                            num2=f'0{num2}'
                    else:
                        try:
                            num2=hex(int(tempNum)).removeprefix("0x")
                        except ValueError: 
                            try:
                                num2=dict["dicVariables"][op1[1].removeprefix("#")]
                            except KeyError:
                                print(f"Linea {dict['lineCounter']}: Error, variable inexistente{num2}")
                                dict["errorList"].append(f"Linea {dict['lineCounter']}: Error, variable inexistente")
                                return
                    if verificarRAMROM(num2):
                        try:
                            dir1=dict["dicEtiquetas"][dict["lineComponents"][2]]
                            delta=int(dir1,16)-dict["currentOrg"]
                            if delta>128 or delta<-127:
                                print(f"Linea {dict['lineCounter']}: Error 8, salto relativo muy lejano")
                                dict["errorList"].append(f"Linea {dict['lineCounter']}: Error 8, salto relativo muy lejano")
                                return
                            numHex=hex(int(bin(delta if delta>0 else delta+(1<<8)).removeprefix("0b"),2)).removeprefix("0x")
                            if len(numHex)==1:
                                numHex=f'0{numHex}'
                            dict["lstLines"].append(f"{dict['lineCounter']}: {hex(dict['currentORG']).removeprefix('0x')} ({dict['instructionSet'][dict['lineComponents'][0]]['dir']['opCode']} {num} {num2} {numHex})\t\t\t\t: {dict['linePrint']}\n")
                            dict["htmlLstLines"].append(f"<p><font color='black'>{dict['lineCounter']}: {hex(dict['currentORG']).removeprefix('0x')}</font> <font color='red'>{dict['instructionSet'][dict['lineComponents'][0]]['dir']['opCode']}</font><font color='blue'> {num} {num2} {numHex}</font>\t\t\t\t: {dict['linePrint']}</p>\n")
                            dict["currentORG"]=dict["currentORG"]+dict["instructionSet"][dict["lineComponents"][0]]['dir']['byteSize']
                            
                        except KeyError:
                            
                            et=(dict['lineCounter'],dict["currentORG"],dict["lineComponents"][2],dict["linePrint"],dict["lineComponents"][0],num,num2)
                            dict["queueEtiquetas2"].append(et)
                            dict["currentORG"]=dict["currentORG"]+dict["instructionSet"][dict["lineComponents"][0]]['dir']['byteSize']
                        finally:
                            return
                    else:
                        print(f"Linea {dict['lineCounter']}: Error 7, magnitud de operando erronea")
                        dict["errorList"].append(f"Linea {dict['lineCounter']}: Error 7, magnitud de operando erronea")
                    return
    elif len(op1)==3:
        modoDir="ind"+op1[1]
        if op1[0].startswith("#"):
            print(f"Linea {dict['lineCounter']}: Error, modo de direccionamiento no soportado")
            dict["errorList"].append(f"Linea {dict['lineCounter']}: Error, modo de direccionamiento no soportado")
            return
        if op1[0].startswith("$"):
            num=op1[0].removeprefix("$")
            if len(num)==1 or len(num)==3:
                num=f'0{num}'
        else:
            try:
                num=hex(int(op1[0])).removeprefix("0x")
            except ValueError: 
                try:
                    num=dict["dicVariables"][op1[0]]
                except KeyError:
                    print(f"Linea {dict['lineCounter']}: Error, variable inexistente {num}")
                    dict["errorList"].append(f"Linea {dict['lineCounter']}: Error, variable inexistente")
                    return
        if verificarRAM(num):
                if op1[2].startswith("#"): #Verifica que ademas de soportarlo, lo esté utilizando
                    tempNum=op1[2].removeprefix("#")
                    if tempNum.startswith("$"):
                        num2=tempNum.removeprefix("$")
                        if len(num)==1 or len(num)==3:
                            num2=f'0{num2}'
                    else:
                        try:
                            num2=hex(int(tempNum)).removeprefix("0x")
                        except ValueError: 
                            try:
                                num2=dict["dicVariables"][op1[2].removeprefix("#")]
                            except KeyError:
                                print(f"Linea {dict['lineCounter']}: Error, variable inexistente{num2}")
                                dict["errorList"].append(f"Linea {dict['lineCounter']}: Error, variable inexistente")
                                return
                    if verificarRAMROM(num2):
                        try:
                            dir1=dict["dicEtiquetas"][dict["lineComponents"][2]]
                            delta=int(dir1,16)-dict["currentOrg"]
                            if delta>128 or delta<-127:
                                print(f"Linea {dict['lineCounter']}: Error 8, salto relativo muy lejano")
                                dict["errorList"].append(f"Linea {dict['lineCounter']}: Error 8, salto relativo muy lejano")
                                return
                            numHex=hex(int(bin(delta if delta>0 else delta+(1<<8)).removeprefix("0b"),2)).removeprefix("0x")
                            if len(numHex)==1:
                                numHex=f'0{numHex}'
                            dict["lstLines"].append(f"{dict['lineCounter']}: {hex(dict['currentORG']).removeprefix('0x')} ({dict['instructionSet'][dict['lineComponents'][0]][modoDir]['opCode']} {num} {num2} {numHex})\t\t\t\t: {dict['linePrint']}\n") #Cambiar print a escribir a archivo
                            dict["htmlLstLines"].append(f"<p><font color='black'>{dict['lineCounter']}: {hex(dict['currentORG']).removeprefix('0x')}</font> <font color='red'>{dict['instructionSet'][dict['lineComponents'][0]][modoDir]['opCode']}</font><font color='blue'> {num} {num2} {numHex}</font>\t\t\t\t: {dict['linePrint']}</p>")
                            dict["currentORG"]=dict["currentORG"]+dict["instructionSet"][dict["lineComponents"][0]][modoDir]['byteSize']
                            
                        except KeyError:
                            
                            et=(dict['lineCounter'],dict["currentORG"],dict["lineComponents"][2],dict["linePrint"],dict["lineComponents"][0],num,num2,modoDir)
                            dict["queueEtiquetas3"].append(et)
                            dict["currentORG"]=dict["currentORG"]+dict["instructionSet"][dict["lineComponents"][0]][modoDir]['byteSize']
                        finally:
                            return
                    else:
                        print(f"Linea {dict['lineCounter']}: Error 7, magnitud de operando erronea")
                        dict["errorList"].append(f"Linea {dict['lineCounter']}: Error 7, magnitud de operando erronea")
                    return
    return
def compileBsetAndBclr(dict):
    op1=dict["lineComponents"][1].split(",")
    if len(op1)==2:
        if op1[0].startswith("#"):
            print(f"Linea {dict['lineCounter']}: Error, modo de direccionamiento no soportado")
            dict["errorList"].append(f"Linea {dict['lineCounter']}: Error, modo de direccionamiento no soportado")
            return
        if op1[0].startswith("$"):
            num=op1[0].removeprefix("$")
            if len(num)==1 or len(num)==3:
                num=f'0{num}'
        else:
            try:
                num=hex(int(op1[0])).removeprefix("0x")
            except ValueError: 
                try:
                    num=dict["dicVariables"][op1[0]]
                except KeyError:
                    print(f"Linea {dict['lineCounter']}: Error, variable inexistente {num}")
                    dict["errorList"].append(f"Linea {dict['lineCounter']}: Error, variable inexistente")
                    return
        if verificarRAM(num):
                if op1[1].startswith("#"): #Verifica que ademas de soportarlo, lo esté utilizando
                    tempNum=op1[1].removeprefix("#")
                    if tempNum.startswith("$"):
                        num2=tempNum.removeprefix("$")
                        if len(num)==1 or len(num)==3:
                            num2=f'0{num2}'
                    else:
                        try:
                            num2=hex(int(tempNum)).removeprefix("0x")
                        except ValueError: 
                            try:
                                num2=dict["dicVariables"][op1[1].removeprefix("#")]
                            except KeyError:
                                print(f"Linea {dict['lineCounter']}: Error, variable inexistente{num2}")
                                dict["errorList"].append(f"Linea {dict['lineCounter']}: Error, variable inexistente")
                                return
                    if verificarRAMROM(num2):
                        try:
                            dict["lstLines"].append(f"{dict['lineCounter']}: {hex(dict['currentORG']).removeprefix('0x')} ({dict['instructionSet'][dict['lineComponents'][0]]['dir']['opCode']} {num} {num2})\t\t\t\t: {dict['linePrint']}\n")
                            dict["htmlLstLines"].append(f"<p><font color='black'>{dict['lineCounter']}: {hex(dict['currentORG']).removeprefix('0x')}</font> <font color='red'>{dict['instructionSet'][dict['lineComponents'][0]]['dir']['opCode']}</font><font color='blue'> {num} {num2}</font>\t\t\t\t: {dict['linePrint']}</p>\n")
                            dict["currentORG"]=dict["currentORG"]+dict["instructionSet"][dict["lineComponents"][0]]['dir']['byteSize']
                            
                        except KeyError:
                            print("RRRR")    
                        
                        finally:
                            return
                    else:
                        print(f"Linea {dict['lineCounter']}: Error 7, magnitud de operando erronea")
                        dict["errorList"].append(f"Linea {dict['lineCounter']}: Error 7, magnitud de operando erronea")
                    return
    elif len(op1)==3:
        modoDir="ind"+op1[1]
        if op1[0].startswith("#"):
            print(f"Linea {dict['lineCounter']}: Error, modo de direccionamiento no soportado")
            dict["errorList"].append(f"Linea {dict['lineCounter']}: Error, modo de direccionamiento no soportado")
            return
        if op1[0].startswith("$"):
            num=op1[0].removeprefix("$")
            if len(num)==1 or len(num)==3:
                num=f'0{num}'
        else:
            try:
                num=hex(int(op1[0])).removeprefix("0x")
            except ValueError: 
                try:
                    num=dict["dicVariables"][op1[0]]
                except KeyError:
                    print(f"Linea {dict['lineCounter']}: Error, variable inexistente {num}")
                    dict["errorList"].append(f"Linea {dict['lineCounter']}: Error, variable inexistente")
                    return
        if verificarRAM(num):
                if op1[2].startswith("#"): #Verifica que ademas de soportarlo, lo esté utilizando
                    tempNum=op1[2].removeprefix("#")
                    if tempNum.startswith("$"):
                        num2=tempNum.removeprefix("$")
                        if len(num)==1 or len(num)==3:
                            num2=f'0{num2}'
                    else:
                        try:
                            num2=hex(int(tempNum)).removeprefix("0x")
                        except ValueError: 
                            try:
                                num2=dict["dicVariables"][op1[2].removeprefix("#")]
                            except KeyError:
                                print(f"Linea {dict['lineCounter']}: Error, variable inexistente{num2}")
                                dict["errorList"].append(f"Linea {dict['lineCounter']}: Error, variable inexistente")
                                return
                    if verificarRAMROM(num2):
                        
                            dict["lstLines"].append(f"{dict['lineCounter']}: {hex(dict['currentORG']).removeprefix('0x')} ({dict['instructionSet'][dict['lineComponents'][0]][modoDir]['opCode']} {num} {num2} )\t\t\t\t: {dict['linePrint']}\n") #Cambiar print a escribir a archivo
                            dict["htmlLstLines"].append(f"<p><font color='black'>{dict['lineCounter']}: {hex(dict['currentORG']).removeprefix('0x')}</font> <font color='red'>{dict['instructionSet'][dict['lineComponents'][0]][modoDir]['opCode']}</font><font color='blue'> {num} {num2}</font>\t\t\t\t: {dict['linePrint']}</p>")
                            dict["currentORG"]=dict["currentORG"]+dict["instructionSet"][dict["lineComponents"][0]][modoDir]['byteSize']
                            
                        
                        
                    else:
                        print(f"Linea {dict['lineCounter']}: Error 7, magnitud de operando erronea")
                        dict["errorList"].append(f"Linea {dict['lineCounter']}: Error 7, magnitud de operando erronea")
                    return
    return
def compileInmediato(vars):
    if vars['lineComponents'][1].startswith("#"): #Verifica que ademas de soportarlo, lo esté utilizando
        tempNum=vars['lineComponents'][1].removeprefix("#")
        if tempNum.startswith("$"):
            num=tempNum.removeprefix("$")
            if len(num)==1 or len(num)==3:
                num=f'0{num}'
        else:
            try:
                num=hex(int(tempNum)).removeprefix("0x")
            except ValueError: 
                try:
                    num=vars['dicVariables'][vars['lineComponents'][1].removeprefix("#")]
                except KeyError:
                    print(f"Linea {vars['lineCounter']}: Error, variable inexistente{num}")
                    vars['errorList'].append(f"Linea {vars['lineCounter']}: Error, variable inexistente")
                    return True
        if verificarRAMROM(num):
            vars['lstLines'].append(f"{vars['lineCounter']}: {hex(vars['currentORG']).removeprefix('0x')} ({vars['instructionSet'][vars['lineComponents'][0]]['imm']['opCode']} {num})\t\t\t\t: {vars['linePrint']}\n") #Cambiar print a escribir a archivo
            vars['htmlLstLines'].append(f"<p><font color='black'>{vars['lineCounter']}: {hex(vars['currentORG']).removeprefix('0x')}</font> <font color='red'>{vars['instructionSet'][vars['lineComponents'][0]]['imm']['opCode']}</font><font color='blue'> {num}</font>\t\t\t\t: {vars['linePrint']}</p>\n")
            vars["currentORG"]=vars["currentORG"]+vars['instructionSet'][vars['lineComponents'][0]]['imm']['byteSize']
            return True
        else:
            print(f"Linea {vars['lineCounter']}: Error 7, magnitud de operando erronea")
            vars['errorList'].append(f"Linea {vars['lineCounter']}: Error 7, magnitud de operando erronea")
        return
def compile(path):
    errorList=[]
    lstLines=[]
    htmlLstLines=[f'<title>{path.removesuffix(".asc")+".lst"}</title>\n']
    
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
    queueEtiquetas=[]
    queueEtiquetas2=[]
    queueEtiquetas3=[]
    lstFile=open(path.removesuffix(".asc")+".lst","w+")
    htmlLstFile=open(path.removesuffix(".asc")+".html","w+")
    for line in l:
        lineCounter=lineCounter+1
        if line=="\n" or line==" " or line.replace("\t"," ").strip().startswith("*") or line.replace("\t"," ").strip()=="\n" :
            continue
        newLine=line.replace("\n"," ").lower()
        oldLine=newLine
        loop=True
        while loop:
            newLine=oldLine.replace("  "," ").replace("\t\t","\t")
            if newLine==oldLine:
                loop=False
                break
            oldLine=newLine
        loop=True
        if newLine.isspace():
            continue
        linePrint=line.replace("\n"," ")
        lineComponents=newLine.strip().split(" ")
        isMneumonico=verificarMneumonico(instructionSet,lineComponents[0])
        if newLine.startswith(" ") or newLine.startswith("\t"): #Verifica si tiene un espacio relativo al margen
            vars={
                "instructionSet": instructionSet,
                "lineCounter": lineCounter,
                "lineComponents":lineComponents,
                "linePrint": linePrint,
                "errorList": errorList,
                "lstLines": lstLines,
                "htmlLstLines": htmlLstLines,
                "queueEtiquetas":queueEtiquetas,
                "queueEtiquetas2":queueEtiquetas2,
                "queueEtiquetas3":queueEtiquetas3,
                "dicVariables":dicVariables,
                "currentORG": currentORG
            }
            if isMneumonico: #Si la tiene y es una instruccion valida, revisa de qué modo de direccionamiento se trata

                #Verificar si es inherente
                if verificarInherente(instructionSet,lineComponents[0]): 
                    if len(lineComponents)>1:
                        print(f"Linea {lineCounter}: Error 6, instruccion no lleva operando")
                        errorList.append(f"Linea {lineCounter}: Error 6, instruccion no lleva operando")

                        continue
                    lstLines.append(f"{lineCounter}: {hex(currentORG).removeprefix('0x')} ({instructionSet[lineComponents[0]]['inh']['opCode']})\t\t\t\t: {linePrint}\n") 
                    htmlLstLines.append(f"<p><font color='black'>{lineCounter}: {hex(currentORG).removeprefix('0x')} </font> <font color='red'>{instructionSet[lineComponents[0]]['inh']['opCode']}</font><font color='black'>\t\t\t\t: {linePrint}</font></p>") 
                    currentORG=currentORG+instructionSet[lineComponents[0]]['inh']['byteSize']

                    continue

                if len(lineComponents)==1: #Como no es inherente debe tener operando, si no lo tiene, arroja error
                    print(f"Linea {lineCounter}: Error 5, instruccion carece de operando(s)")
                    errorList.append(f"Linea {lineCounter}: Error 5, instruccion carece de operando(s)")
                    continue

                if lineComponents[0]=="brset" or lineComponents[0]=="brclr":
                    compileBrsetAndBrclr(vars)
                    continue
                    
                if lineComponents[0]=="bset" or lineComponents[0]=="bclr":
                    compileBsetAndBclr(vars)
                    continue

                #Verificar si es inmediato
                if verificarInmediato(instructionSet,lineComponents[0]): #Verificar que a la instruccion soporte direccionamiento inmediato
                    next=compileInmediato(vars)
                    if next==True:
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
                                lstLines.append(f"{lineCounter}: {hex(currentORG).removeprefix('0x')} ({instructionSet[lineComponents[0]]['indx']['opCode']} {num})\t\t\t\t: {linePrint}\n") #Cambiar print a escribir a archivo
                                htmlLstLines.append(f"<p><font color='black'>{lineCounter}: {hex(currentORG).removeprefix('0x')}</font> <font color='red'>{instructionSet[lineComponents[0]]['indx']['opCode']}</font><font color='blue'> {num}</font>\t\t\t\t: {linePrint}</p>\n")
                                currentORG=currentORG+instructionSet[lineComponents[0]]['indx']['byteSize']
                            elif opIndex[1]=="y":
                                lstLines.append(f"{lineCounter}: {hex(currentORG).removeprefix('0x')} ({instructionSet[lineComponents[0]]['indy']['opCode']} {num})\t\t\t\t: {linePrint}\n") #Cambiar print a escribir a archivo
                                htmlLstLines.append(f"<p><font color='black'>{lineCounter}: {hex(currentORG).removeprefix('0x')}</font> <font color='red'>{instructionSet[lineComponents[0]]['indy']['opCode']}</font><font color='blue'> {num}</font>\t\t\t\t: {linePrint}</p>\n")
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
                        except ValueError: 
                            try:
                                num=dicVariables[lineComponents[1]]
                            except KeyError:
                                print(f"Linea {lineCounter}: Error, variable inexistente {num}")
                                errorList.append(f"Linea {lineCounter}: Error, variable inexistente")
                                continue
                    if verificarRAM(num):
                        lstLines.append(f"{lineCounter}: {hex(currentORG).removeprefix('0x')} ({instructionSet[lineComponents[0]]['dir']['opCode']} {num})\t\t\t\t: {linePrint}\n") #Cambiar print a escribir a archivo
                        htmlLstLines.append(f"<p><font color='black'>{lineCounter}: {hex(currentORG).removeprefix('0x')}</font> <font color='red'>{instructionSet[lineComponents[0]]['dir']['opCode']}</font><font color='blue'> {num}</font>\t\t\t\t: {linePrint}</p>\n")
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
                            if lineComponents[0]=="jmp" or lineComponents[0]=="jsr":
                                try:
                                    num=dicEtiquetas[lineComponents[1]]
                                except KeyError:
                                    print(f"Linea {lineCounter}: Error 3, etiqueta inexistente")
                                    errorList.append(f"Linea {lineCounter}: Error 3, etiqueta inexistente")
                                    continue
                            else:
                                try:
                                    num=dicVariables[lineComponents[1]]
                                except KeyError:
                                    print(f"Linea {lineCounter}: Error, variable inexistente")
                                    errorList.append(f"Linea {lineCounter}: Error, variable inexistente")
                                    continue
                    
                    if verificarRAMROM(num):
                        lstLines.append(f"{lineCounter}: {hex(currentORG).removeprefix('0x')} ({instructionSet[lineComponents[0]]['ext']['opCode']} {num})\t\t\t\t: {linePrint}\n") #Cambiar print a escribir a archivo
                        htmlLstLines.append(f"<p><font color='black'>{lineCounter}: {hex(currentORG).removeprefix('0x')}</font> <font color='red'>{instructionSet[lineComponents[0]]['ext']['opCode']}</font><font color='blue'> {num}</font>\t\t\t\t: {linePrint}</p>\n")
                        currentORG=currentORG+instructionSet[lineComponents[0]]['ext']['byteSize']
                    else:
                        print(f"Linea {lineCounter}: Error 7, magnitud de operando erronea")
                        errorList.append(f"Linea {lineCounter}: Error 7, magnitud de operando erronea")
                    continue
                #Relativos
                if verificarRelativo(instructionSet,lineComponents[0]):
                    try:
                        dir1=dicEtiquetas[lineComponents[1]]
                        delta=int(dir1,16)-currentORG
                        if delta>128 or delta<-127:
                            print(f"Linea {lineCounter}: Error 8, salto relativo muy lejano")
                            errorList.append(f"Linea {lineCounter}: Error 8, salto relativo muy lejano")
                            continue
                        numHex=hex(int(bin(delta if delta>0 else delta+(1<<8)).removeprefix("0b"),2)).removeprefix("0x")
                        if len(numHex)==1:
                            numHex=f'0{numHex}'
                        lstLines.append(f"{lineCounter}: {hex(currentORG).removeprefix('0x')} ({instructionSet[lineComponents[0]]['rel']['opCode']} {numHex})\t\t\t\t: {linePrint}\n") #Cambiar print a escribir a archivo
                        htmlLstLines.append(f"<p><font color='black'>{lineCounter}: {hex(currentORG).removeprefix('0x')}</font> <font color='red'>{instructionSet[lineComponents[0]]['rel']['opCode']}</font><font color='blue'> {numHex}</font>\t\t\t\t: {linePrint}</p>\n")
                        currentORG=currentORG+instructionSet[lineComponents[0]]['rel']['byteSize']
                        
                    except KeyError:
                        
                        et=(lineCounter,currentORG,lineComponents[1],linePrint,lineComponents[0])
                        queueEtiquetas.append(et)
                        currentORG=currentORG+instructionSet[lineComponents[0]]['rel']['byteSize']
                    finally:
                        continue

            #Si se trata de org
            elif lineComponents[0]=="org": 
                if lineComponents[1].startswith("$"):
                        num=int(lineComponents[1].removeprefix("$"),16)
                else:
                    num=int(lineComponents[1])
                
                currentORG=num
                lstLines.append(f'\t\tORG ${hex(currentORG).removeprefix("0x")}\n')
                htmlLstLines.append(f'<p><font color="black">{lineCounter}: Vacio : ORG ${hex(currentORG).removeprefix("0x")}</font></p>\n')
            else:
                print(f"Linea {lineCounter}: Error 4, mneumonico inexistente")
                errorList.append(f"Linea {lineCounter}: Error 4, mneumonico inexistente")


        else: #Si no tiene espacio relativo al margen
            if isMneumonico: #Si además es una instruccion del MC68HC11, marca error
                print(f"Linea {lineCounter}: Error 9, instruccion carece de espacio relativo al margen")
                errorList.append(f"Linea {lineCounter}: Error 9, instruccion carece de espacio relativo al margen")
                continue

            #Verifica si es una constanteS
            if len(lineComponents)>1:
                if(lineComponents[1])=="equ":
                    try:
                        if lineComponents[2].startswith("$"):
                            num=lineComponents[2].removeprefix("$")
                        else:
                            num=hex(int(lineComponents[2])).removeprefix("0x")
                        if len(num)==1 or len(num)==3:
                            num=f'0{num}'
                        dicVariables[lineComponents[0]]=num
                    except ValueError:
                       dicVariables[lineComponents[0]]="00"
                lstLines.append(f'\t\t\t\t{lineComponents[0]} EQU ${num}\n')
                htmlLstLines.append(f'<p><font color="black">{lineCounter}: Vacio : {lineComponents[0]} EQU ${num}</font></p>\n')
                continue
            #Verifica si se trata de un end
            if lineComponents[0]=="end":
                hasEnd=True
                break
            dicEtiquetas[lineComponents[0]]=hex(currentORG).removeprefix("0x")
            lstLines.append(f'\t\t\t\t{lineComponents[0]}\n')
            htmlLstLines.append(f'<p><font color="black">{lineCounter}: Vacio : {lineComponents[0]}</font></p>\n')

    if hasEnd==False:
        print(f"Linea {lineCounter+1}: Error 10, no se encuentra END")
        errorList.append(f"Linea {lineCounter+1}: Error 10, no se encuentra END")


    for element in queueEtiquetas:
        try:
            dir1=dicEtiquetas[element[2]]
            delta=int(dir1,16)-element[1]
            if delta>128 or delta<-127:
                print(f"Linea {element[0]}: Error 8, salto relativo muy lejano")
                errorList.append(f"Linea {element[0]}: Error 8, salto relativo muy lejano")
                continue
            numHex=hex(int(bin(delta if delta>0 else delta+(1<<8)).removeprefix("0b"),2)).removeprefix("0x")
            if len(numHex)==1:
                numHex=f'0{numHex}'
            lstLines=placeRel(lstLines,element,f"{element[0]}: {hex(element[1]).removeprefix('0x')} ({instructionSet[element[4]]['rel']['opCode']} {numHex})\t\t\t\t: {element[3]}\n")
            htmlLstLines=placeRelHtml(lstLines,htmlLstLines,element,f"<p><font color='black'>{element[0]}: {hex(element[1]).removeprefix('0x')}</font> <font color='red'> {instructionSet[element[4]]['rel']['opCode']}</font><font color='blue'>{numHex}</font><font color='black'>\t\t\t\t: {element[3]}</font></p>\n")
        except KeyError:
            print(f"Linea {element[0]}: Error 3, etiqueta inexistente")
            errorList.append(f"Linea {element[0]}: Error 3, etiqueta inexistente")

    for element in queueEtiquetas2:
        try:
            dir1=dicEtiquetas[element[2]]
            delta=int(dir1,16)-element[1]
            if delta>128 or delta<-127:
                print(f"Linea {element[0]}: Error 8, salto relativo muy lejano")
                errorList.append(f"Linea {element[0]}: Error 8, salto relativo muy lejano")
                continue
            numHex=hex(int(bin(delta if delta>0 else delta+(1<<8)).removeprefix("0b"),2)).removeprefix("0x")
            if len(numHex)==1:
                numHex=f'0{numHex}'
            lstLines=placeRel(lstLines,element,f"{element[0]}: {hex(element[1]).removeprefix('0x')} ({instructionSet[element[4]]['dir']['opCode']} {element[5]} {element[6]} {numHex})\t\t\t\t: {element[3]}\n") #Cambiar print a escribir a archivo  
            htmlLstLines=placeRelHtml(lstLines,htmlLstLines,element,f"<p><font color='black'>{element[0]}: {hex(element[1]).removeprefix('0x')}</font> <font color='red'> {instructionSet[element[4]]['dir']['opCode']}</font><font color='blue'>{element[5]} {element[6]} {numHex}</font><font color='black'>\t\t\t\t: {element[3]}</font></p>\n")
        except KeyError:
            print(f"Linea {element[0]}: Error 3, etiqueta inexistente")
            errorList.append(f"Linea {element[0]}: Error 3, etiqueta inexistente")
    
    for element in queueEtiquetas3:
        try:
            dir1=dicEtiquetas[element[2]]
            delta=int(dir1,16)-element[1]
            if delta>128 or delta<-127:
                print(f"Linea {element[0]}: Error 8, salto relativo muy lejano")
                errorList.append(f"Linea {element[0]}: Error 8, salto relativo muy lejano")
                continue
            numHex=hex(int(bin(delta if delta>0 else delta+(1<<8)).removeprefix("0b"),2)).removeprefix("0x")
            if len(numHex)==1:
                numHex=f'0{numHex}'
            lstLines=placeRel(lstLines,element,f"{element[0]}: {hex(element[1]).removeprefix('0x')} ({instructionSet[element[4]][element[7]]['opCode']} {element[5]} {element[6]} {numHex})\t\t\t\t: {element[3]}\n") #Cambiar print a escribir a archivo  
            htmlLstLines=placeRelHtml(lstLines,htmlLstLines,element,f"<p><font color='black'>{element[0]}: {hex(element[1]).removeprefix('0x')}</font> <font color='red'> {instructionSet[element[4]][element[7]]['opCode']}</font><font color='blue'>{element[5]} {element[6]} {numHex}</font><font color='black'>\t\t\t\t: {element[3]}</font></p>\n")
        except KeyError:
            print(f"Linea {element[0]}: Error 3, etiqueta inexistente")
            errorList.append(f"Linea {element[0]}: Error 3, etiqueta inexistente")

    lstFile.writelines(lstLines)
    htmlLstFile.writelines(htmlLstLines)
    if len(errorList)>0:
        errorString=""
        for error in errorList:
            errorString=errorString+error+"\n"
        gui.mensaje(titulo=f"{len(errorList)} errores",mensaje=errorString)
    gui.mensaje(titulo="Exito",mensaje="Se ha terminado el proceso de compilacion")

def  loadInstructionSet():
    return IS.getInstructionSet()

compile("compilador/reloj.asc")