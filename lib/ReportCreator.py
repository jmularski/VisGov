import sys, os
from CsvParser import FileReader
from Analyser import Analyser

for fileName in os.listdir("../files"):
  xmlFile = FileReader('../files/', fileName)
  Analyser(xmlFile, fileName)
