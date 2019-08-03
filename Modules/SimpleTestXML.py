import xml.etree.ElementTree as ET
import re
import os
import urllib.request
from shutil import copyfile

author_pattern = "username*"
author_list = []
text_list = []
links_list = []

if not os.path.isdir( "Out" ):
    os.mkdir( "Out" )

with open('Raw/CLEAN_PTF_ARCHIVE_KAAOS1.html', 'r') as file:
    data = file.read()
   
root = ET.fromstring(data)

for item in root.iter('span'):
    if 'class' in item.attrib:
        if re.match( author_pattern, item.attrib['class'] ):
            author_list.append( item.text )

        if item.attrib['class'] == 'postbody':
            text_list.append( item.text )
            local_links = []
            for link in item.iter('img'):
                local_links.append( link.attrib['src'] )
            links_list.append( local_links )
        
for i in range( 0, len( author_list ) ):
    print( "============" )
    print( author_list[i] )
    if not text_list[i] == None:
        print( text_list[i] )
    else:
        print( "" )
    for item in links_list[i]:
        print( item )
        
counter = 0
for i in range( 0, len( links_list ) ):
    for item in links_list[i]:
        try:
            url = item
            name = url.split( '/' )[-1]
            extension = url.split( '.' )[-1]
            normalized_name = str( counter ) + '.' +extension
            print( url, normalized_name )
            response = urllib.request.urlopen(url)
            data = response.read()
            file = open( 'Out/' + normalized_name, 'wb' )
            file.write( bytearray( data ) )
        except:
            print("An exception occurred")
            copyfile( "Raw/notfound.png", 'Out/' + str( counter ) + '.png' )
            
        counter = counter + 1

        