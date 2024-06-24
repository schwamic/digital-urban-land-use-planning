# -*- coding: utf-8 -*-
from dotenv import find_dotenv, load_dotenv
import xml.etree.ElementTree as ET

# import BauGB.xml from local file
xml_file_path = "./../../data/external/BauGB.xml"
tree = ET.parse(xml_file_path)
root = tree.getroot()

print(root.tag)
