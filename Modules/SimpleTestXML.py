import xml.etree.ElementTree as ET
import re
author_pattern = "username*"
author_list = []

with open('Raw/CLEAN_PTF_ARCHIVE_KAAOS1.html', 'r') as file:
    data = file.read()
   
root = ET.fromstring(data)

for item in root.iter('span'):
    if 'class' in item.attrib:
        if re.match( author_pattern, item.attrib['class'] ):
            elem = item.text
            if not elem in author_list:
                author_list.append( elem )

print( author_list )