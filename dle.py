#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Esto es el juego del gato y el ratón. Cada vez que la rae actualice su página: https://dle.rae.es/ este script puede dejar de funcionar; al fin y al cabo estoy haciendo scraping.

TODO:
    - unittesting!!!!
    - un fallo que se repite bastante son las palabras con acento y sin acento p.ej espolon -> espolón
    - modo revisión como en git con el comando difftool
    - barra de progreso? MUY INTERESANTE
"""
import bs4
import requests
import sys
import argparse
import unittest
import concurrent.futures
import logging
from functools import wraps
import timeit
import sqlite3
from contextlib import closing
from ignorar_con_regex import ignore_by_regex

host = 'http://dle.rae.es/?w='
resumen = {"encontradas": 0, "no_encontradas": [], "similares": []}
db_name = "vocabulario.db"
# las palabras no encontradas o con formas similares serán escritas en este archivo:
archivo_revision = "REVISION.txt"
mensaje_palabras_no_encontradas = "[No encontradas]\n"
mensaje_palabras_similares = "[Contienen formas similares]\n"
aplicar_regex = False

def read_file(filename):
    content = []
    with open(filename, "r", encoding="utf-8") as file:
        content = file.readlines()
    return content

# para el archivo especial en la variable 'archivo_revision'
def read_file_and_ignore_special_lines(filename):
    content = []
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            if line not in [mensaje_palabras_no_encontradas, mensaje_palabras_similares]:
                content.append(line)
    return content


def get_response(word):
    # https://requests.readthedocs.io/en/v0.8.2/user/advanced/#keep-alive
    s = requests.Session()
    url = host + word
    return s.get(url, timeout=10,stream=True).text


def search(word):
    response = get_response(word)
    soup = bs4.BeautifulSoup(response, "lxml")
    div = soup.find('div').get_text()
    # Buscamos en la maraña del html el siguiente texto que coincide con el de la página web de la rae. Hay que tener en cuenta que puede cambiar, esto es scraping no lo olvides. Se cuidadoso!
    if div.find(f"{word} no está en el Diccionario.") != -1:
        return None
    elif div.find(f"Entradas que contienen la forma «{word}»") != -1:
        return f"Hay entradas que contienen la forma '{word}'"
    # buscamos por la etiqueta <article>, además la primera aparición contendrá lo que nos interesa que son las definiciones de la palabra
    article = soup.find('article')
    return article.get_text()


def show_definition(word, definition):
    if definition is None:
        print(f"No se encontró '{word}'")
        return
    print(definition[0])
    if definition[1]:  # simplemente para no mostrar una nueva línea cuando esta vacio
        print(definition[1])


def escribir_palabras_no_encontradas(no_encontradas, palabras_similares):
    with open(archivo_revision, "w", encoding="utf-8") as f:
        if no_encontradas:
            f.write(mensaje_palabras_no_encontradas)
            f.write('\n'.join(resumen["no_encontradas"])+'\n')

        if palabras_similares:
            f.write(mensaje_palabras_similares)
            f.write('\n'.join(resumen["similares"])+'\n')


def show_resume():
    n_encontradas = resumen["encontradas"]
    if n_encontradas:
        print(f"Encontradas: {n_encontradas}")
    hay_no_encontradas = len(resumen["no_encontradas"]) > 0
    hay_similares = len(resumen["similares"]) > 0
    if hay_no_encontradas or hay_similares:
        print(f"Hubo palabras que no fueron añadidas, se guardaron en '{archivo_revision}'")
        escribir_palabras_no_encontradas(hay_no_encontradas, hay_similares)

# https://stackoverflow.com/questions/51503672/decorator-for-timeit-timeit-method/51503837#51503837
def logger_time(func):
    @wraps(func)
    def tic_toc(*args, **kwargs):
        start = timeit.default_timer()
        func(*args, **kwargs)
        duration = timeit.default_timer() - start
        logging.info(round(duration,2))
    return tic_toc


def get_definition(word):
    assert word, "words None"
    # extraemos la palabra sin el salto de línea, llamamos a strip para convertir "   anales     " -> "anales"
    word = word.strip()
    if not word:
        return
    definition = search(word)
    if definition is not None:
        # eliminamos las strings vacias dentro de la lista debido a los \n. Algunas definiciones pueden tener varios \n consecutivos p.ej 'remolonear' o ser más peliguadas p.ej transgredir
        sanitize_output = [
            line for line in definition.split("\n") if line.split()]
        definition = (sanitize_output[0], '\n'.join(ignore_by_regex(
            sanitize_output[1:]) if aplicar_regex else sanitize_output[1:]))
    return word, definition


def saveInDB(word,definition,cursor):
    if not word.strip():  # ignorar lineas vacias
        return
    if definition is None:  # no se añaden a la db las palabras no encontradas
        resumen["no_encontradas"].append(word)
    # tampoco se añadirán las palabras con formas similares
    elif definition[0] == f"Hay entradas que contienen la forma '{word}'":
        resumen["similares"].append(word)
    else:
        try:
            cursor.execute(
                "INSERT INTO vocabulario VALUES (?,?,1)", definition)
        except sqlite3.IntegrityError:  # no se pueden repetir palabras ni definiciones
            pass
        except Exception as e:
            print(e)
        resumen["encontradas"] += 1

def execute_pool(words):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        return executor.map(get_definition, words) # devolvemos una lista de tuplas con todas las palabras y sus definiciones

def print_definition(words):
    # Por una parte manejamos parámetros vacios "", " " y la opcion -r si esta sola
    for w in words:
        if not w.strip():  # ignorar lineas vacias
            continue
        word, definition = get_definition(w)
        show_definition(word, definition)

# words es una lista con todas las palabras
@logger_time
def get_definitions(words, save_in_db):
    if save_in_db is None:
        print_definition(words)
        return
    with closing(sqlite3.connect(db_name)) as conexion:
        cursor = conexion.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS vocabulario"
                       "( palabras TEXT NOT NULL UNIQUE,"
                       "definiciones TEXT NOT NULL UNIQUE,"
                       "nuevas INTEGER)"
                       )
        for info in execute_pool(words):
            if info: # ignorar las lineas vacías
                word, definition = info
                saveInDB(word,definition,cursor)
        conexion.commit()
    show_resume()


def parse_commands():
    global aplicar_regex
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-f", "--file", dest="input_file",
                       help="archivo para leer palabras")
    group.add_argument('word', nargs="?", help="Busca una palabras cualquiera")
    parser.add_argument("-reg", "--regex", dest="aplicar_regex", action='store_true',
                        help="Intenta eliminar morfología, etimología... de las definiciones")

    opt = parser.parse_args()
    if len(sys.argv) < 2:  # mostrar la ayuda en caso de que no recibamos ningún argumento
        parser.print_help(sys.stderr)
        return
    content = []
    if opt.word is not None:
        content = [opt.word]
    if opt.input_file is not None:
        if opt.input_file == archivo_revision:
            content = read_file_and_ignore_special_lines(opt.input_file)
        else:
            content = read_file(opt.input_file)
    aplicar_regex = opt.aplicar_regex
    #timeit.timeit(lambda : get_definitions(content,opt.input_file),number=3)
    get_definitions(content,opt.input_file)


def main():
    logging.basicConfig(filename="tiempos", filemode='a', level=logging.INFO,
                        format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    parse_commands()

if __name__ == '__main__':
    main()
