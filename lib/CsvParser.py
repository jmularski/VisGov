# -*- coding: utf-8 -*-

from xml.etree import ElementTree


def FileReader(directory, fileName):
    fileName = directory + fileName
    xmlp = ElementTree.XMLParser(encoding='utf-8')
    e = ElementTree.parse(fileName, parser=xmlp).getroot()
    return e
