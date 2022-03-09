
import re
import json
import numpy as np


__title__ =  "Script para separar películas"
__author__ = "Nombre de los integrantes de grupo"

diccionario = dict()

def escribir_archivos(fichero):
    '''
    Método que permite, a partir de un fichero con valoraciones, escribir varios archivos.
    '''
    with open(fichero,'r') as f:
        next(f)
        for i, line in enumerate(f):
            writeFile(i, line)


def writeFile(number, text):
    """
    Elimina <br/> y escribe cada una de las criticas en la 
    carpeta valoraciones con el número de la valoracion
    y su valoracion (positiva, negativa)
    """
    text = re.sub(r'<br\s*\/>', ' ', text)
    aux = text.split(',')
    filename = 'valoraciones/'+str(number)+aux[-1][0:-1]+'.txt'
    with open(filename, 'w') as f:
        f.write(text)

        
def normalSpliting(fichero):
    """
    Escribe cada una de las criticas del fichero raiz y crea
    un diccionario de índice invertido

    La función dictionary(...) guarda los pares clave (palabra) - valor (lista de ficheros, identificados por número) en la variable diccionario declarada al principio del script
    La función _dictToJson() crea un archivo json que almacena el diccionario
    """
    with open(fichero,'r') as f:
        for i, line in enumerate(f):

            line = re.sub(r'<\s*br\s*\/\s*>', ' ', line)
            dictionary(i, line)
            with open('ficheros/file'+str(i)+'.txt','w') as p:
                
                p.write(line)

    _dictToJson()


def dictionary(numero, text):
    """
    Guarda los pares clave (palabra) - valor (lista de ficheros, identificados por número) en la variable diccionario declarada al principio del script
    """
    palabras = text.split(' ')
    palabras = set(palabras)
    for palabra in palabras:
        if palabra not in diccionario:
            diccionario[palabra] = [numero]
        else:
            diccionario[palabra].append(numero)


def _dictToJson(jsonname = "data.json"):
    """
    Almacena el contenido de diccionario en un archivo .json
    """
    with open(jsonname, "w") as f:
        json.dump(diccionario, f)

        
def _jsonToDict(jsonname = "data.json"):
    """
    Pasa el contenido de un archivo .json al diccionario
    """
    with open(jsonname, "r") as f:
        diccionario = json.load(f) 
    return diccionario
    

def repList(lista, numero):
    """
    Método que retorna una lista con los elementos comunes en todas las listas que recibe como parámetros.
    """
    elementos = dict()
    for elem in lista:
        if elem not in elementos:
            elementos[elem] = 1
        else:
            elementos[elem] += 1
    listaTextos = []
    for val,key in zip(elementos.values(),elementos.keys()):
        if val >= numero:
            listaTextos.append(key)
    return listaTextos


def printDict(quieres, noquieres, verbose = True):
    """
    Método que hace el recuento de documentos en los que se encuentran simultáneamente todas las palabras incluidas en la lista del parámetro "quieres" y a su vez en los que no se encuentran las palabras en la lista "noquieres". Imprime la información por pantalla y devuelve la lista de documentos.
    
    La función repList(...) retorna una lista con los elementos comunes en todas las listas que recibe como parámetros.
    """
    listaquieres = []
    for palabra in quieres:
        listaquieres.extend(diccionario[palabra])
    
    liq = repList(listaquieres,len(quieres))
    
    listanoquieres = []
    for palabra in noquieres:
        listanoquieres.extend(diccionario[palabra])
    
    linq = repList(listanoquieres,len(noquieres))
    
    result = [item for item in liq if item not in linq]
    
    if verbose:
        print('-'*75)       
        print(f'Aparece en {len(result)}\nLos textos en los que aparece son:\n {result}')
        print('-'*75+'\n')

    return result


def lecturaFilesId(lista, palabras):
    """
    Método que crea un diccionario que tiene como claves las palabras de la consulta y como valores listas que representan los vectores de pesos, basados en la función del enunciado: 1+ log(frecuencia)
    """
    cuenta = dict()
    for palabra in palabras:
        cuenta[palabra] = []
    for elem in lista:
        with open("ficheros/file"+str(elem)+".txt", "r") as f:
            contenido = f.read()
            for palabra in palabras:
                val = contenido.count(palabra) 
                if val != 0:
                    peso = 1 + np.log10(val)
                else:
                    peso = 0
                cuenta[palabra].append(peso)
           

    return cuenta



if __name__ ==  "__main__":
    #Ejercicio 02
    escribir_archivos("IMDB Dataset.csv")

    #Ejercicio 03
    normalSpliting("IMDB_raiz.csv")
    #diccionario =_jsonToDict() # Si ya tienes creado el data.json puedes no ejecutar los metodos escribir_archivos y normalSpliting
    palabras = ['prison','brutal']
    palabrano = ['king']
    printDict(palabras, palabrano)

    #Ejercicio 04
    palabras = ['humor']
    palabrano = []
    textos = []
    textos.extend(printDict(palabras, palabrano, verbose=False))
    palabras = ['oscar']
    textos.extend(printDict(palabras, palabrano, verbose=False))
    textos = set(textos)
    cuenta = lecturaFilesId(textos,['humor','oscar'])
    
    # Cálculo de la puntuación como el coseno (producto escalar / módulo de los vectores)
    puntuacion = np.zeros(len(textos))
    vectores = np.array(list(cuenta.values()))
    consulta = np.array([1,1])
    for i in range(len(textos)):
        prMod = np.linalg.norm(vectores[:,i])*np.sqrt(2)
        puntuacion[i] = np.dot(vectores[:,i],consulta)/prMod

    print(puntuacion)
    


    

    



    
