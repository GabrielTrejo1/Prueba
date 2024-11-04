import os
import sys

if hasattr(sys, '_MEIPASS'):
    base_path = sys._MEIPASS  # Para el ejecutable empaquetado
else:
    base_path = os.path.abspath(".")  # Para el entorno de desarrollo
