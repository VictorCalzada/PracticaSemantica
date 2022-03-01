
import re
import json


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
    text = re.sub(r'<br\s*\/>', ' ', text)
    aux = text.split(',')
    filename = 'valoraciones/'+str(number)+aux[-1][0:-1]+'.txt'
    with open(filename, 'w') as f:
        f.write(text)

def normalSpliting(fichero):
    with open(fichero,'r') as f:
        for i, line in enumerate(f):

            line = re.sub(r'<\s*br\s*\/\s*>', ' ', line)
            dictionary(i, line)
            with open('ficheros/file'+str(i)+'.txt','w') as p:
                
                p.write(line)

    _dictToJson()



def dictionary(numero, text):
    
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



def printDict(quieres, noquieres):
    listaquieres = []
    for palabra in quieres:
        listaquieres.extend(diccionario[palabra])
    
    liq = repList(listaquieres,len(quieres))
    
    listanoquieres = []
    for palabra in noquieres:
        listanoquieres.extend(diccionario[palabra])
    
    linq = repList(listanoquieres,len(noquieres))
    
    result = [item for item in liq if item not in linq]
    
    print('-'*75)       
    print(f'Aparece en {len(result)}\nLos textos en los que aparece son {result}')
    print('-'*75+'\n')


    

    


if __name__ ==  "__main__":
    #Ejercicio 02
    #escribir_archivos("IMDB Dataset.csv")

    #Ejercicio 03
    #normalSpliting("IMDB_raiz.csv")
    diccionario =_jsonToDict()
    palabras = ['prison','brutal']
    palabrano = ['king']
    printDict(palabras, palabrano)
    

    



    
