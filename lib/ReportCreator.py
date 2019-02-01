import sys
from CsvParser import FileReader
from Analyser import Analyser

fileName = sys.argv[1]

xmlFile = FileReader('../files/', fileName + '.xml')
print(Analyser(xmlFile, fileName))
