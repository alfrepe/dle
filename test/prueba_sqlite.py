import sqlite3
import unidecode

# SELECT EXISTS(SELECT palabras FROM vocabulario WHERE palabras="árido, da"); # comprobar si existe un campo; devuelve 1 si existe, de lo contrario 0
palabras = {
            "a": ("'a%' or palabras like 'á%'",),
            'b': ("b%",),
            'c': ("c%",),
            'd': ("d%",),
            'e': (" 'e%' or 'é%' ",),
            'f': ("f%",),
            'g': ("g%",),
            'h': ("h%",),
            'i': (" 'i%' or 'í%' ",),
            'j': ("j%",),
            'k': ("k%",),
            'l': ("l%",),
            'm': ("m%",),
            'n': ("n%",),
            'ñ': ("ñ%",),
            'o': ("o%' or 'ó%' ",),
            'p': ("p%",),
            'q': ("q%",),
            'r': ("r%",),
            's': ("s%",),
            't': ("t%",),
            'u': (" 'u%' or 'ú%' ",),
            'v': ("v%",),
            'w': ("w%",),
            'x': ("x%",),
            'y': ("y%",),
            'z': ("z%",),
        }
"""
a -> 0
e -> 4
i -> 8
o -> 14
u -> 20

"""
def agrupar_por_letra():
    vocales = {"a":('a%','á%'), "e":('e%','é%'), "i":('i%','í%'), "o":('o%','ó%'), "u":('u%','ú%') }
    letras = "abcdefghijklmnñopqrstuvwxyz"
    try:
        conexion = sqlite3.connect("../vocabulario.db")
        cursor = conexion.cursor()
        # debug
        #cursor.execute("select palabras from vocabulario where palabras like ? or palabras like ?",('a%','á%',))
    
        for i in letras:
            if i in ["a","e","i","o","u"]:
                cursor.execute("select palabras,definiciones from vocabulario where palabras like ? or palabras like ?",vocales[i]) # order by palabras collate unicode
            else:
                cursor.execute("select palabras,definiciones from vocabulario where palabras like ?",(i+'%',)) # order by palabras collate unicode
            registros = cursor.fetchall()
            print(f"\nPalabras que empiezan por {i}")
            for i in registros:
                print(i[0])
        

    except sqlite3.IntegrityError as e:
        print(e)
    finally:
        cursor.close()
        conexion.close()

agrupar_por_letra()