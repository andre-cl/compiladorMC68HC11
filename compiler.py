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

def compileBrsetAndBrclr(dict,s19List):
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
                            armarLineaS19(hex(dict["currentORG"]).removeprefix("0x"),dict["instructionSet"][dict["lineComponents"][0]]['dir']['opCode'],num+" "+num2+" "+numHex,s19List)
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
                            armarLineaS19(hex(dict["currentORG"]).removeprefix("0x"),dict["instructionSet"][dict["lineComponents"][0]][modoDir]['opCode'],num+" "+num2+" "+numHex,s19List)
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
def compileBsetAndBclr(dict,s19List):
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
                            armarLineaS19(hex(dict["currentORG"]).removeprefix("0x"),dict["instructionSet"][dict["lineComponents"][0]]['dir']['opCode'],num+" "+num2,s19List)
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
                            armarLineaS19(hex(dict["currentORG"]).removeprefix("0x"),dict['instructionSet'][dict['lineComponents'][0]][modoDir]['opCode'],num+" "+num2,s19List)
                            dict["currentORG"]=dict["currentORG"]+dict["instructionSet"][dict["lineComponents"][0]][modoDir]['byteSize']  
                    else:
                        print(f"Linea {dict['lineCounter']}: Error 7, magnitud de operando erronea")
                        dict["errorList"].append(f"Linea {dict['lineCounter']}: Error 7, magnitud de operando erronea")
                    return
    return
def compileInmediato(vars,s19List):
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
            armarLineaS19(hex(vars["currentORG"]).removeprefix("0x"),vars["instructionSet"][vars["lineComponents"][0]]['imm']['opCode'],num,s19List)
            vars["currentORG"]=vars["currentORG"]+vars['instructionSet'][vars['lineComponents'][0]]['imm']['byteSize']
            return True
        else:
            print(f"Linea {vars['lineCounter']}: Error 7, magnitud de operando erronea")
            vars['errorList'].append(f"Linea {vars['lineCounter']}: Error 7, magnitud de operando erronea")
        return
def compileIndexado(vars,s19List):
    if vars['lineComponents'][1].startswith("#"):
        print(f"Linea {vars['lineCounter']}: Error, modo de direccionamiento no soportado")
        vars['errorList'].append(f"Linea {vars['lineCounter']}: Error, modo de direccionamiento no soportado")
        return True
    opIndex=vars['lineComponents'][1].split(",")
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
                    num=vars['dicVariables'][opIndex[0]]
                except KeyError:
                    print(f"Linea {vars['lineCounter']}: Error, variable inexistente {num}")
                    vars['errorList'].append(f"Linea {vars['lineCounter']}: Error, variable inexistente")
                    return True
        if verificarRAM(num):
            
            if opIndex[1]=="x":
                modoDir="indx"
            elif opIndex[1]=="y":
                modoDir="indy"
            else:
                print(f"Linea {vars['lineCounter']}: Error, indexado incorrecto")
                vars['errorList'].append(f"Linea {vars['lineCounter']}: Error, indexado incorrecto")
                return True
            vars['lstLines'].append(f"{vars['lineCounter']}: {hex(vars['currentORG']).removeprefix('0x')} ({vars['instructionSet'][vars['lineComponents'][0]][modoDir]['opCode']} {num})\t\t\t\t: {vars['linePrint']}\n") #Cambiar print a escribir a archivo
            vars['htmlLstLines'].append(f"<p><font color='black'>{vars['lineCounter']}: {hex(vars['currentORG']).removeprefix('0x')}</font> <font color='red'>{vars['instructionSet'][vars['lineComponents'][0]][modoDir]['opCode']}</font><font color='blue'> {num}</font>\t\t\t\t: {vars['linePrint']}</p>\n")
            armarLineaS19(hex(vars["currentORG"]).removeprefix("0x"),vars["instructionSet"][vars["lineComponents"][0]][modoDir]['opCode'],num,s19List)
            vars['currentORG']=vars['currentORG']+vars['instructionSet'][vars['lineComponents'][0]][modoDir]['byteSize']
            return True
        else:
            if not verificarExtendido(vars['instructionSet'],vars['lineComponents'][0]):
                print(f"Linea {vars['lineCounter']}: Error 7, magnitud de operando erronea")
                vars['errorList'].append(f"Linea {vars['lineCounter']}: Error 7, magnitud de operando erronea")

def compileDirecto(vars,s19List):
    if vars['lineComponents'][1].startswith("#"):
        print(f"Linea {vars['lineCounter']}: Error, modo de direccionamiento no soportado")
        vars['errorList'].append(f"Linea {vars['lineCounter']}: Error, modo de direccionamiento no soportado")

        return True
    if vars['lineComponents'][1].startswith("$"):
        num=vars['lineComponents'][1].removeprefix("$")
        if len(num)==1 or len(num)==3:
            num=f'0{num}'
    else:
        try:
            num=hex(int(vars['lineComponents'][1])).removeprefix("0x")
        except ValueError: 
            try:
                num=vars['dicVariables'][vars['lineComponents'][1]]
            except KeyError:
                print(f"Linea {vars['lineCounter']}: Error, variable inexistente {num}")
                vars['errorList'].append(f"Linea {vars['lineCounter']}: Error, variable inexistente")
                return True
    if verificarRAM(num):
        num=num.removeprefix("00")
        vars['lstLines'].append(f"{vars['lineCounter']}: {hex(vars['currentORG']).removeprefix('0x')} ({vars['instructionSet'][vars['lineComponents'][0]]['dir']['opCode']} {num})\t\t\t\t: {vars['linePrint']}\n") #Cambiar print a escribir a archivo
        vars['htmlLstLines'].append(f"<p><font color='black'>{vars['lineCounter']}: {hex(vars['currentORG']).removeprefix('0x')}</font> <font color='red'>{vars['instructionSet'][vars['lineComponents'][0]]['dir']['opCode']}</font><font color='blue'> {num}</font>\t\t\t\t: {vars['linePrint']}</p>\n")
        armarLineaS19(hex(vars["currentORG"]).removeprefix("0x"),vars["instructionSet"][vars["lineComponents"][0]]['dir']['opCode'],num,s19List)
        vars['currentORG']=vars['currentORG']+vars['instructionSet'][vars['lineComponents'][0]]['dir']['byteSize']
        return True
    else:
        if not verificarExtendido(vars['instructionSet'],vars['lineComponents'][0]):
            print(f"Linea {vars['lineCounter']}: Error 7, magnitud de operando erronea")
            vars['errorList'].append(f"Linea {vars['lineCounter']}: Error 7, magnitud de operando erronea")

def compileExtendido(vars,s19List):
    if vars['lineComponents'][1].startswith("#"):
        print(f"Linea {vars['lineCounter']}: Error, modo de direccionamiento no soportado")
        vars['errorList'].append(f"Linea {vars['lineCounter']}: Error, modo de direccionamiento no soportado")

        return True
    if vars['lineComponents'][1].startswith("$"):
        num=vars['lineComponents'][1].removeprefix("$")
        if len(num)==1 or len(num)==3:
                num=f'0{num}'
    else:
        try:
            num=hex(int(vars['lineComponents'][1])).removeprefix("0x")
        except ValueError:
            if vars['lineComponents'][0]=="jmp" or vars['lineComponents'][0]=="jsr":
                try:
                    num=vars['dicEtiquetas'][vars['lineComponents'][1]]
                except KeyError:
                    print(f"Linea {vars['lineCounter']}: Error 3, etiqueta inexistente")
                    vars['errorList'].append(f"Linea {vars['lineCounter']}: Error 3, etiqueta inexistente")
                    return True
            else:
                try:
                    num=vars['dicVariables'][vars['lineComponents'][1]]
                except KeyError:
                    print(f"Linea {vars['lineCounter']}: Error, variable inexistente")
                    vars['errorList'].append(f"Linea {vars['lineCounter']}: Error, variable inexistente")
                    return True
    
    if verificarRAMROM(num):
        vars['lstLines'].append(f"{vars['lineCounter']}: {hex(vars['currentORG']).removeprefix('0x')} ({vars['instructionSet'][vars['lineComponents'][0]]['ext']['opCode']} {num})\t\t\t\t: {vars['linePrint']}\n") #Cambiar print a escribir a archivo
        vars['htmlLstLines'].append(f"<p><font color='black'>{vars['lineCounter']}: {hex(vars['currentORG']).removeprefix('0x')}</font> <font color='red'>{vars['instructionSet'][vars['lineComponents'][0]]['ext']['opCode']}</font><font color='blue'> {num}</font>\t\t\t\t: {vars['linePrint']}</p>\n")
        armarLineaS19(hex(vars["currentORG"]).removeprefix("0x"),vars["instructionSet"][vars["lineComponents"][0]]['ext']['opCode'],num,s19List)
        vars['currentORG']=vars['currentORG']+vars['instructionSet'][vars['lineComponents'][0]]['ext']['byteSize']
    else:
        print(f"Linea {vars['lineCounter']}: Error 7, magnitud de operando erronea")
        vars['errorList'].append(f"Linea {vars['lineCounter']}: Error 7, magnitud de operando erronea")

def compileRelativo(vars,s19List):
    try:
        dir1=vars['dicEtiquetas'][vars['lineComponents'][1]]
        delta=int(dir1,16)-vars['currentORG']
        if delta>128 or delta<-127:
            print(f"Linea {vars['lineCounter']}: Error 8, salto relativo muy lejano")
            vars['errorList'].append(f"Linea {vars['lineCounter']}: Error 8, salto relativo muy lejano")
            return True
        numHex=hex(int(bin(delta if delta>0 else delta+(1<<8)).removeprefix("0b"),2)).removeprefix("0x")
        if len(numHex)==1:
            numHex=f'0{numHex}'
        vars['lstLines'].append(f"{vars['lineCounter']}: {hex(vars['currentORG']).removeprefix('0x')} ({vars['instructionSet'][vars['lineComponents'][0]]['rel']['opCode']} {numHex})\t\t\t\t: {vars['linePrint']}\n") #Cambiar print a escribir a archivo
        vars['htmlLstLines'].append(f"<p><font color='black'>{vars['lineCounter']}: {hex(vars['currentORG']).removeprefix('0x')}</font> <font color='red'>{vars['instructionSet'][vars['lineComponents'][0]]['rel']['opCode']}</font><font color='blue'> {numHex}</font>\t\t\t\t: {vars['linePrint']}</p>\n")

        armarLineaS19(hex(vars["currentORG"]).removeprefix("0x"),vars["instructionSet"][vars["lineComponents"][0]]['rel']['opCode'],numHex,s19List)
        vars['currentORG']=vars['currentORG']+vars['instructionSet'][vars['lineComponents'][0]]['rel']['byteSize']
    except KeyError:
        et=(vars['lineCounter'],vars['currentORG'],vars['lineComponents'][1],vars['linePrint'],vars['lineComponents'][0])
        vars['queueEtiquetas'].append(et)
        vars['currentORG']=vars['currentORG']+vars['instructionSet'][vars['lineComponents'][0]]['rel']['byteSize']
    finally:
        return True

def cmpS19(arr):
    stri=arr[2].removesuffix("</font>")
    return int(stri,16)


def decHex(num):
    return str(int(num)-1 if num.isnumeric() else 9 if num=="A" else chr(ord(dir[3])-1))

def incDirLinea(numHex):
    new=hex(int(numHex,16)+int("1F",16)).removeprefix("0x")
    while len(new)<4:
        new="0"+new
    return new

def parHex(num):
    if num.isnumeric():
        val=True
        return val if int(num)%2==0 else not val
    else:
        if num=="A" or num=="C" or num=="E":
            return True
        else:
            return False
        
def obtenerDirLinea(dir):
    if not parHex(dir[2]):
        return dir[0]+dir[1]+decHex(dir[2])+"0"
    return dir[0]+dir[1]+dir[2]+"0"

def insEnDatos(dir,opCode,info,lineInfo,s19List):
    subDir=int(dir,16)-int(obtenerDirLinea(dir),16)
    intOpLis=[]
    intInfoLis=[]
    litaVacia=[]
    
    
    if info!=None and type(info)!=list:
        if len(info)==1:
            info="0"+info
        if len(info)==4:
            info=info[0]+info[1]+" "+info[2]+info[3]
        infoLis=info.split(" ")
        intInfoLis=infoLis.copy()
    else:
        
        infoLis=info
    if opCode!=None and type(opCode)!=list:
        opLis=opCode.split(" ")
        intOpLis=opLis.copy()
    else:
        
        opLis=opCode
    print(f"{dir} {opCode}, {info}")
    try:
        if opCode!=None and len(opCode)!=0:
            for code in opLis:
                
                lineInfo[subDir]=f"<font color='red'>{code}</font>"
                subDir=subDir+1
                
                if len(intOpLis)!=0:
                    intOpLis.pop(0)
                elif len(intOpLis)==0:
                    intOpLis=None
        
        if info!=None:
            for ins in infoLis:
                lineInfo[subDir]=f"<font color='blue'>{ins}</font>"
                subDir=subDir+1
                
                if len(intInfoLis)!=0:
                    intInfoLis.pop(0)
        
    except IndexError:
        obtenerDirLinea(dir[0]+dir)
        newDir=obtenerDirLinea(incDirLinea(dir))
        armarLineaS19(newDir,intOpLis,intInfoLis,s19List)
 
    
def elimNone(lineInfo):
    for byte in range(len(lineInfo)-1,0,-1):
        if lineInfo[byte]=="N":
            lineInfo.pop(byte)
        else:
            break
    if len(lineInfo)==1:
        if lineInfo[0]=="N":
            lineInfo[0]="<font color='yellow'>FF</font>"
    for byte in range(0,len(lineInfo)-1):
        if lineInfo[byte]=="N":
            lineInfo[byte]="<font color='green'>FF</font>"

def dirExisteEnLista(dir,s19List):
    
    for e in range(0,len(s19List)):
        
        if dir==s19List[e][2].removesuffix("</font>"):
            return e
    
    return -1

def armarLineaS19(dir,opCode,info,s19List):
    dirLinea=obtenerDirLinea(dir)
    i=dirExisteEnLista(dirLinea,s19List)
    if i>-1:
        lineInfo=s19List[i][3]
        insEnDatos(dir,opCode,info,lineInfo,s19List)
    else:
        lineInfo=["N","N","N","N","N","N","N","N","N","N","N","N","N","N","N","N","N","N","N","N","N","N","N","N","N","N","N","N","N","N","N","N"]
        insEnDatos(dir,opCode,info,lineInfo,s19List)
        s19List.append(["<p><font color='black'> S1","len",dirLinea+"</font>",lineInfo,"checkSum"])

def sumBin(numHex1,numHex2):
    numBin1=bin(int(numHex1,16)).removeprefix("0b")
    numBin2=bin(int(numHex2,16)).removeprefix("0b")
    while len(numBin1)<8:
        numBin1="0"+numBin1
    while len(numBin2)<8:
        numBin2="0"+numBin2
    res=""
    carry=False
    for i in range(7,-1,-1):
        if numBin1[i]=="0" and numBin2[i]=="0" and carry==False:
            res="0"+res
            carry=False
        elif numBin1[i]=="0" and numBin2[i]=="0" and carry==True:
            res="1"+res
            carry=False
        elif (numBin1[i]=="1" and numBin2[i]=="0") or (numBin1[i]=="0" and numBin2[i]=="1") and carry==False:
            res="1"+res
            carry=False
        elif (numBin1[i]=="1" and numBin2[i]=="0") or (numBin1[i]=="0" and numBin2[i]=="1") and carry==True:
            res="0"+res
            carry=True
        elif numBin1[i]=="1" and numBin2[i]=="1" and carry==False:
            res="0"+res
            carry=True
        elif numBin1[i]=="1" and numBin2[i]=="1" and carry==True:
            res="1"+res
            carry=True
    resHex=hex(int(res,2)).removeprefix("0x")
    #print(f"{numBin1}+{numBin2}={resHex}")
    return resHex

def complementoAUno(numHex):
    numBin=bin(int(numHex,16)).removeprefix("0b")
    
    while len(numBin)<8:
        numBin="0"+numBin
    res=numBin
    for i in range(0,7):
        if numBin[i]=="0":
            res[i]=="1"
        elif numBin[i]=="1":
            res[i]=="0"
    return hex(int(res,2)).removeprefix("0x").upper()

def finS19(s19List):
    s19ListFinal=sorted(s19List,key=cmpS19)
    s19ListFinal[len(s19ListFinal)-1][0]="<p><font color='black'>S9"
    s19ListString=[]
    for element in s19ListFinal:
        elimNone(element[3])
        element[1]=hex(3+len(element[3])).removeprefix("0x")
        if len(element[1])==1:
            element[1]="0"+element[1]
        checkSum=sumBin(element[1],element[2][0]+element[2][1])
        checkSum=sumBin(checkSum,element[2][2]+element[2][3])
        stringInfo=""
        for byte in element[3]:
            stringInfo=stringInfo+byte
            copyByte=byte.removeprefix("<font color='red'>").removeprefix("<font color='black'>").removeprefix("<font color='blue'>").removesuffix("</font>").removeprefix("<font color='yellow'>").removeprefix("<font color='green'>")
            checkSum=sumBin(checkSum,copyByte)
        element[4]="<font color='black'>"+complementoAUno(checkSum)+"</font></p>"
        s19String=element[0]+element[1]+element[2]+stringInfo+element[4]+"\n"
        s19ListString.append(s19String)
    return s19ListString

def compile(path):
    errorList=[]
    lstLines=[]
    htmlLstLines=[f'<title>{path.split("/")[len(path.split("/"))-1].removesuffix(".asc")+".lst"}</title>\n']
    s19List=[]
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
    s19File=open(path.removesuffix(".asc")+"(s19).html","w+")
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
                "dicEtiquetas":dicEtiquetas,
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
                    armarLineaS19(hex(currentORG).removeprefix("0x"),instructionSet[lineComponents[0]]['inh']['opCode'],None,s19List)
                    currentORG=currentORG+instructionSet[lineComponents[0]]['inh']['byteSize']

                    continue

                if len(lineComponents)==1: #Como no es inherente debe tener operando, si no lo tiene, arroja error
                    print(f"Linea {lineCounter}: Error 5, instruccion carece de operando(s)")
                    errorList.append(f"Linea {lineCounter}: Error 5, instruccion carece de operando(s)")
                    continue
                if currentORG+1>int("FFFF",16):
                    print(f"Linea {lineCounter}: Error, instruccion fuera de memoria")
                    errorList.append(f"Linea {lineCounter}: Error, instruccion fuera de memoria")
                if lineComponents[0]=="brset" or lineComponents[0]=="brclr":
                    compileBrsetAndBrclr(vars,s19List)
                    currentORG=vars["currentORG"]
                    queueEtiquetas2=vars["queueEtiquetas2"]
                    queueEtiquetas3=vars["queueEtiquetas3"]
                    continue
                    
                if lineComponents[0]=="bset" or lineComponents[0]=="bclr":
                    compileBsetAndBclr(vars,s19List)
                    currentORG=vars["currentORG"]
                    queueEtiquetas2=vars["queueEtiquetas2"]
                    queueEtiquetas3=vars["queueEtiquetas3"]
                    continue

                #Verificar si es inmediato
                if verificarInmediato(instructionSet,lineComponents[0]): #Verificar que a la instruccion soporte direccionamiento inmediato
                    next=compileInmediato(vars,s19List)
                    currentORG=vars["currentORG"]
                    if next==True:
                        continue
                    

                #Verificar si es indexado
                if verificarIndexado(instructionSet,lineComponents[0]):
                    next=compileIndexado(vars,s19List)
                    currentORG=vars["currentORG"]
                    if next==True:
                        continue

                #Verificar si es directo
                if verificarDirecto(instructionSet,lineComponents[0]):
                    next=compileDirecto(vars,s19List)
                    currentORG=vars["currentORG"]
                    if next==True:
                        continue

                            
                #Verificar si es extendido
                if verificarExtendido(instructionSet,lineComponents[0]):
                    next=compileExtendido(vars,s19List)
                    currentORG=vars["currentORG"]
                    if next==True:
                        continue

                #Relativos
                if verificarRelativo(instructionSet,lineComponents[0]):
                    next=compileRelativo(vars,s19List)
                    currentORG=vars["currentORG"]
                    queueEtiquetas=vars["queueEtiquetas"]
                    if next==True:
                        continue

            #Si se trata de org
            elif lineComponents[0]=="org": 
                if lineComponents[1].startswith("$"):
                        num=int(lineComponents[1].removeprefix("$"),16)
                else:
                    num=int(lineComponents[1])
                
                if verificarRAMROM(hex(num).removeprefix("0x")):
                    currentORG=num
                    orgHex=hex(currentORG).removeprefix("0x")
                    if len(orgHex)==1:
                        orgHex=f'000{orgHex}'
                    elif len(orgHex)==2:
                        orgHex=f'000{orgHex}'
                    elif len(orgHex)==3:
                        orgHex=f'0{orgHex}'
                    lstLines.append(f'\t\tORG ${hex(currentORG).removeprefix("0x")}\n')
                    htmlLstLines.append(f'<p><font color="black">{lineCounter}: Vacio : ORG ${hex(currentORG).removeprefix("0x")}</font></p>\n')
                else:
                    print(f"Linea {lineCounter}: Error 7, magnitud de operando erronea")
                    errorList.append(f"Linea {lineCounter}: Error 7, magnitud de operando erronea")
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
            armarLineaS19(hex(element[1]).removeprefix("0x"),instructionSet[element[4]]['rel']['opCode'],numHex,s19List)
            #print(hex(element[1]).removeprefix("0x"),instructionSet[element[4]]['rel']['opCode'],numHex,s19List)
            htmlLstLines=placeRelHtml(lstLines,htmlLstLines,element,f"<p><font color='black'>{element[0]}: {hex(element[1]).removeprefix('0x')}</font> <font color='red'> {instructionSet[element[4]]['rel']['opCode']}</font><font color='blue'>{numHex}</font><font color='black'>\t\t\t\t: {element[3]}</font></p>\n")
        except KeyError:
            print(f"Linea {element[0]}: Error 3, etiqueta inexistente 1")
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
            armarLineaS19(hex(element[1]).removeprefix("0x"),instructionSet[element[4]]['dir']['opCode'],element[5]+" "+element[6]+" "+numHex,s19List)
            htmlLstLines=placeRelHtml(lstLines,htmlLstLines,element,f"<p><font color='black'>{element[0]}: {hex(element[1]).removeprefix('0x')}</font> <font color='red'> {instructionSet[element[4]]['dir']['opCode']}</font><font color='blue'>{element[5]} {element[6]} {numHex}</font><font color='black'>\t\t\t\t: {element[3]}</font></p>\n")
        except KeyError:
            print(f"Linea {element[0]}: Error 3, etiqueta inexistente 2")
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
            armarLineaS19(hex(element[1]).removeprefix("0x"),instructionSet[element[4]][element[7]]['opCode'],element[5]+" "+element[6]+" "+numHex,s19List)
            htmlLstLines=placeRelHtml(lstLines,htmlLstLines,element,f"<p><font color='black'>{element[0]}: {hex(element[1]).removeprefix('0x')}</font> <font color='red'> {instructionSet[element[4]][element[7]]['opCode']}</font><font color='blue'>{element[5]} {element[6]} {numHex}</font><font color='black'>\t\t\t\t: {element[3]}</font></p>\n")
        except KeyError:
            print(f"Linea {element[0]}: Error 3, etiqueta inexistente 3")
            errorList.append(f"Linea {element[0]}: Error 3, etiqueta inexistente")
    #armarLineaS19("8007","26","f9",s19List)
    s19Lines=finS19(s19List)
    s19Lines.insert(0,f'<title>{path.split("/")[len(path.split("/"))-1].removesuffix(".asc")+".s19"}</title>\n')
    s19File.writelines(s19Lines)
    lstFile.writelines(lstLines)
    htmlLstFile.writelines(htmlLstLines)
    if len(errorList)>0:
        errorString=""
        for error in errorList:
            errorString=errorString+error+"\n"
        gui.mensaje(titulo=f"Exito",mensaje=f"Se ha terminado el proceso de compilacion\n\nErrores ({len(errorList)}):\n"+errorString)
    

def  loadInstructionSet():
    return IS.getInstructionSet()

compile("compilador/reloj.asc")