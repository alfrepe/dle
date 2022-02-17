import matplotlib.pyplot as plt
import sys
import numpy as np
import time
sys.path.append('..')
import timeit
from dle import get_definitions
from functools import wraps

pool_procesos = [7.25, 12.86, 19.34, 20.52, 25.07, 27.5, 28.71, 36.47, 36.73, 36.8]
pool_threads =  [3.15, 5.72, 9.45, 11.65, 15.3, 17.54, 20.34, 22.58, 25.84, 28.17]

def generate_graph(elements, procesos,threads):
    plt.xlabel('Número de palabras') # eje horizontal
    plt.ylabel('Tiempo')  # eje vertical
    pro = np.array(procesos)
    th = np.array(threads)
    plt.plot(elements, th, label ='Threads')
    plt.plot(elements, pro, label ='Processes') 
    
    plt.grid() 
    plt.legend() 
    plt.show()

if __name__ == '__main__':
    l = [i+50 for i in range(0,500,50)]
    generate_graph(l,pool_procesos,pool_threads)