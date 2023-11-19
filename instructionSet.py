import openpyxl
import pandas
from tabulate import tabulate
import os

class IS:
    def getInstructionSet():
        
        data=openpyxl.load_workbook(filename="ins.xlsx") #Carga el archivo de excel
        wrksht=data.active #Carga la hoja activa
        insDict=dict()  #Define un diccionario vacio donde se almacenará todo
        
        for row in range(9,153): #Recorre todas las filas donde hay datos
            rowDict=dict() #Diccionario vacio para la fila
            i=0 #Contador para recorrer las columnas de acuerdo a su modo de direccionamiento
            for dirMode in ["imm", "dir", "indx", "indy", "ext","inh","rel"]: #Recorre de modos de direccionamiento 
                for col in range(2+(3*i),4+(3*i)): #Recorre las 3 columnas del modo de direccionamiento
                    if wrksht[row][col].value=="-- ": #Si no soporta el modo de direccionamiento, lo salta
                        break
                    op=dict() #Diccionario para cada modo de direccionamiento
                    op={
                        "opCode": wrksht[row][2+(3*i)].value, #El codigo de operacion es la primera columna
                        "clockTime": wrksht[row][2+(3*i)+1].value, #El tiempo de reloj es la segunda columna
                        "byteSize": wrksht[row][2+(3*i)+2].value #El tamaño en memoria es la tercer columna
                    }
                    rowDict[dirMode]=op  #En el diccionario de la instrucción, usando como clave el mnemonico, se asigna el diccionario del modo de direccionamiento
                i=i+1 #Contador de modo de direccionamiento
            insDict[wrksht[row][1].value]=rowDict #Se agrega al set de instrucciones la instruccion con todos sus modos de direccionamiento 
        return insDict

if __name__=="__main__":
    dic=IS.getInstructionSet()
    print(dic["nop"]["inh"]["byteSize"])