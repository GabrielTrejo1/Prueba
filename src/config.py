import os
import sys

if hasattr(sys, '_MEIPASS'):
  base_path = sys._MEIPASS
else:
  base_path = os.path.abspath(".")
