# coding: utf-8

import os
DIR = os.path.expanduser("/tmp")
FICHEROS = os.listdir(DIR)
TESTS = [fich for fich in FICHEROS
         if os.path.isfile(os.path.join(DIR, fich)) and fich.endswith(".txt")]
# El siguiente código permite abrirlos para lectura.
for fich in TESTS:
    f = open(os.path.join(DIR, fich), 'r')
    print(f.read())
    f.close()
