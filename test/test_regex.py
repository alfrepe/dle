import re
import sys
sys.path.append("..")
from ignorar_con_regex import ignore_by_regex
import unittest
"""
Hay demasiadas posibilidades que debemos tener en cuenta y abarcarlas todas puede ser un proceso tedioso y propenso al error.
En un mundo ideal, utilizaríamos IA para que nuestro algoritmo vaya aprendiendo y elimine esa información que no quiero
"""

class test(unittest.TestCase):
    def test_eliminar_lineas(self):
        
        file_input = [
                "Quizá del ár. hisp. aḍḍíman o aḍḍamán.",
                "Conjug. c. peinar.",
                "campiña\n",
                "Del mozár. y ár. hisp. *kanpínya, y este del lat. tardío campania.\n",
                "1. f. Espacio grande de tierra llana labrantía.\n",
                "cerrarse de campiña\n",
                "1. loc. verb. coloq. cerrarse de banda.\n",
                "\n", # líneas vacia
                "cínico, ca\n",
                "Del lat. cynĭcus, y este del gr. κυνικός kynikós; propiamente 'perruno'.\n",
                "1. adj. Dicho de una persona: Que actúa con falsedad o desvergüenza descaradas. U. t. c. s.",
        ]
        #self.assertEqual(dle.read_file("prueba"),file_input)
        file_output = ignore_by_regex(file_input)
        result = [
                "campiña\n",
                "Espacio grande de tierra llana labrantía.\n",
                "cerrarse de campiña\n",
                "coloq. cerrarse de banda.\n",
                "\n",
                "cínico, ca\n",
                "Dicho de una persona: Que actúa con falsedad o desvergüenza descaradas. U. t. c. s.",
        ]
        self.assertEqual(file_output,result)
"""
def prueba_definitiva(file,output):
    import dle
    content = dle.read_file(file)
    print("lineas antes: ",len(content))
    with open (output,"w",encoding="utf-8") as f:
        for line in content:
            if re.search(expr1,line,re.IGNORECASE):
                continue
            f.write(re.sub(expr2,"",line,re.UNICODE))
"""

if __name__ == '__main__':
    #prueba_definitiva("prueba_regex","prueba_regex_SALIDA.txt")
    unittest.main()