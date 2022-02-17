import sys
sys.path.append('../')
import dle
import requests
import logging
"""
    Segun el sistema operativo timeit elige una implementation u otra para una mayor precisión.
    Por eso es mas conveniente usarlo. Fuente: https://docs.python.org/2/library/timeit.html#timeit.default_timer
"""
import timeit

host = 'http://dle.rae.es/?w='


def read_file(filename):
    content = []
    with open (filename,"r",encoding="utf-8") as file:
        content = file.readlines()
    return content

def work(words):
    for w in words:
        dle.search(w)
if __name__ == "__main__":
    logging.basicConfig(filename="tiempos-sincrono",filemode='a',level=logging.INFO,format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    words = read_file("../palabras/palabras.txt")
    start_time = timeit.default_timer()
    for w in words:
        dle.search(w)
    
    duration = timeit.default_timer() - start_time
    
    #duration = timeit.timeit("download_all_sites(sites)", "from __main__ import download_all_sites, sites", number=5)
    logging.info(f"{duration:0.2f}")
    