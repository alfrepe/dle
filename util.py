# -*- coding: utf-8 -*-
import sys
import locale
import dle
import logging

# TODO: hacer unittesting
"""
Dado un archivo con palabras línea por línea, este script genera otro archivo con las palabras que no están repetidas y las ordena;
además omite las líneas en blanco y elimina los espacios o tabulaciones al empezar la palabra si los hubiera
Debemos tener en cuenta los siguentes casos:
    - Tabulaciones o espacios al inicio o al final
Cuando hablamos de palabras repetidas debemos tener en cuenta que el programa no es mágico y palabras como
vanidad o vanidoso las considerará, como cabe esperar, diferentes.
Sin embargo, esto podría causar una cierta redundacia de palabras muy similares.
P.ej:

aladas
alado
arrogancia
arrogante
vanidad
vanidoso
velado
velados
vigor
vigorosa
NOTA: al archivo de destino siempre le añadimos una nueva línea
"""
logging.basicConfig(filename="debug",filemode='w',level=logging.INFO,format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

def escribir_vocabulario(file,content):
    with open (file,"w",encoding='utf-8') as file:
        file.writelines(content)

def show_resume(palabras, palabras_nuevas):
    n_palabras_originales = len(palabras)
    n_palabras_nuevas = len(palabras_nuevas)
    print(f"numero de palabras: {n_palabras_originales}")
    print(f"n palabras que deberia haber sin repetir: {n_palabras_nuevas}")
    print(f"palabras repetidas: {n_palabras_originales-n_palabras_nuevas}")

def main():
    locale.setlocale(locale.LC_ALL, '')  # ordenar segun el locale; si no palabras como 'ávido' no estarán ordenadas adecuadamente
    if len(sys.argv) < 2:
        print(f"Uso: {sys.argv[0]} file")
        sys.exit(1)
    try:
        content = dle.read_file(sys.argv[1])
    except Exception as e:
        print(e)
        return
    words = [line.lstrip() for line in content if line.strip()] # no queremos lineas vacias por eso hacemos strip() ni tampoco espacios o tabulaciones al empezar la palabra lstrip()
    #logging.info(words)
    if words == []:
        print("El archivo esta vacio o solo contiene líneas vacias")
        return
    if words[-1][-1:] != "\n":
        words[-1] = words[-1]+"\n"
    palabras_sin_repetir = set(words) # tomamos las palabra que no se repiten
    ordenado = sorted(palabras_sin_repetir,key=locale.strxfrm)
    escribir_vocabulario("vocabulario-txt/vocabulario-release.txt",ordenado)
    show_resume(words,palabras_sin_repetir)

main()
    