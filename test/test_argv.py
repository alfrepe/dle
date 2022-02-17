import argparse
import sys
import unittest

class testCLI(unittest.TestCase):
    parser = argparse.ArgumentParser()
    @staticmethod # evitamos pasarle self; además como no tenemos intencion de acceder a los miembros de la clase con static queda más clara nuestra intención
    def match(dict1,list1): # comparar los valores de un diccionario del estilo {clave:valor} con una lista
        for key in dict1.values():
            if key not in list1:
                return False
        return True
    @staticmethod
    def init_arg():
        group = testCLI.parser.add_mutually_exclusive_group()
        group.add_argument('word', nargs="?",help="Busca una palabras cualquiera")
        group.add_argument("-f","--file",dest="input_file",help="archivo para leer palabras")
        testCLI.parser.add_argument("-reg","--regex",dest="aplicar_regex",action='store_true',help="Intenta eliminar morfología, etimología... de las definiciones")
    
    def test_grupo_mutuamente_exclusivo(self):
        self.assertRaises(SystemExit ,self.parser.parse_args,["lúgubre","-f","file"])
    
    def test_parametro_posicional(self):
        
        result = vars(self.parser.parse_args(["macabro"]))
        self.assertTrue(self.match(result,['macabro',None,False]))
        self.assertRaises(SystemExit ,self.parser.parse_args,["lúgubre","sinuoso"])  

    def test_regex_funciona_en_ambos_grupos(self):
        result = vars(self.parser.parse_args(["macabro","-r"]))
        self.assertTrue(self.match(result,['macabro',None,True]))

        result = vars(self.parser.parse_args(["-f","noexisto","-r"]))
        self.assertTrue(self.match(result,[None,"noexisto",True])) 

    def test_parametro_file(self):
        self.assertRaises(SystemExit ,self.parser.parse_args,["-f"])
<<<<<<< HEAD
    def test_only_regex(self):
        result = vars(self.parser.parse_args(["-r"]))
        self.assertTrue(self.match(result,[[],None,True]))
=======
>>>>>>> 21d075ab9e972ee63ed10ac52932745e9049fbdd


testCLI.init_arg()
#unittest.main(exit=False)