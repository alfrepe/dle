# -*- coding: utf-8 -*-
# Nota: no tiene en cuenta los digrafos es decir, l será lo mismo que ll
# Le podemos pasar por parámetro las letras que queramos para generar los audios p.ej python generate_mp3.py abc
"""
TODO:
    - Mostrar la duracion total de los archivos de audio
"""

from gtts import gTTS
import concurrent.futures
import timeit
import logging
import sqlite3
import sys
from functools import wraps
import os
from mutagen.mp3 import MP3
#from tqdm import tqdm

directorio_audios = "audios/" # donde se guardarán los audios con las definiciones
db_name = "vocabulario.db"
tiempos = []

def print_time(func):
    @wraps(func)
    def tic_toc(*args, **kwargs):
        start = timeit.default_timer()
        func(*args, **kwargs)
        duration = timeit.default_timer() - start
        print(round(duration,2))
    return tic_toc

def logger_time_in_list(func):
    @wraps(func)
    def tic_toc(*args, **kwargs):
        start = timeit.default_timer()
        func(*args, **kwargs)
        duration = timeit.default_timer() - start
        tiempos.append(round(duration,2))
    return tic_toc

def generate_mp3(content,output_file):
    gTTS("\n".join(content), lang='es-es',lang_check=False).save(output_file)

@print_time
def generate_mp3_threading(content,files,workers):
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        executor.map(generate_mp3,content,files)
            

#################################################################################
# síncrono
def ensure_mp3_gen(content,file_name_path):
    tts = gTTS("\n".join(content), lang='es-es',lang_check=False)
    tts.save(file_name_path)

def generate_mp3_sincrono(content,files,path):
    for index,file in enumerate(files):
        ensure_mp3_gen(content[index],path+file) 

#################################################################################
logging.basicConfig(filename="tiempos",filemode='a',level=logging.INFO,format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


def pitfalls():
    import os, sys, requests
    url='http://www.google.com/'
    if not os.path.isdir(directorio_audios):
        os.mkdir(directorio_audios)
    try:
        requests.get(url, timeout=5)
    except requests.ConnectionError:
        print("Comprueba que tengas internet")
        sys.exit(1)

def convert(seconds):
    hours = seconds // 3600
    seconds %= 3600
    mins = seconds // 60
    seconds %= 60
    if hours < 10:
        hours = '0'+str(hours)
    if mins < 10:
        mins = '0'+str(mins)
    if seconds < 10:
        seconds = '0'+str(seconds)
    return hours, mins, seconds

def show_duration_time_mp3(files):
    for file in files:
        audio = MP3(file)
        h,m,s = convert(int(audio.info.length))
        print(f"{h}:{m}:{s}")
    #print("Duracion total: ")

def main():
    pitfalls()
    vocales = {"a":('a%','á%'), "e":('e%','é%'), "i":('i%','í%'), "o":('o%','ó%'), "u":('u%','ú%') }
    letras_no_encontradas = []
    letras = "abcdefghijklmnñopqrstuvwxyz"
    palabras = []
    lista_archivos = []
    index = -1
    if len(sys.argv) == 2: # TODO: hacer comprobaciones p.ej que no sea un entero
        if not sys.argv[1].isalpha():
            print("Error: solo se permiten letras")
            sys.exit(1)
        letras = set(sys.argv[1].lower()) # si omitimos lower no se generará el audio de la 'Ñ'
    try:
        conexion = sqlite3.connect(db_name)
        cursor = conexion.cursor()    
        for l in letras:
            if l in ("a","e","i","o","u"):
                cursor.execute("select palabras,definiciones from vocabulario where palabras like ? or palabras like ?",vocales[l]) # order by palabras collate unicode
            else:
                cursor.execute("select palabras,definiciones from vocabulario where palabras like ?",(l+'%',)) # order by palabras collate unicode
            registros = cursor.fetchall()
            if registros != []:
                lista_archivos.append(directorio_audios+l+".mp3")
                palabras.append([])
                index += 1
                for i in registros:
                    palabras[index].append(i[0]+"\n"+i[1])
            else:
                letras_no_encontradas.append(l)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conexion.close()
    
    size = len(palabras)
    if size == 0:
        print("No hay palabras que empiecen por ",letras_no_encontradas)
    
    #generate_mp3_sincrono(palabras,lista_archivos,directorio_audios)
    generate_mp3_threading(palabras,lista_archivos,size)
    show_duration_time_mp3(lista_archivos)
    """
    for i in range(5):
        generate_mp3_threading(palabras,lista_archivos)
        print("listo")
    print(tiempos)
    """
main()
