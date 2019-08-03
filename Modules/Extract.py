##########################################################################
#
#   PTF_Revival
#__________________
#
# Suck.py
# Layl
# Please refer to LICENSE.md
#

# Imports
import xml.etree.ElementTree as ET
import re
import os
import urllib.request
from shutil import copyfile
import time

# utility var
author_pattern = "username.*"
signaler_pattern = ".*signal.*"

# Make Out dir
if not os.path.isdir( "Out" ):
    os.mkdir( "Out" )

# Open Registry.xml
with open('Raw/Registry.xml', 'r') as file:
    registry_data = file.read()

# Parse registry
registry_root = ET.fromstring( registry_data )

# For all items in registry
for item in registry_root.iter( 'entry' ):
    # Get file name
    filename = item.attrib['file']
    # build file path
    filepath = "Raw/" + filename
    
    # Print it
    print( filepath )
    
    # build basename without extension for filename
    basename = filename.split( '.' )[0]
    
    # build Outdir for this entry
    outdir = "Out/" + basename
    imgdir = outdir + "/img"
    if not os.path.isdir( outdir ):
        os.mkdir( outdir )
        
    if not os.path.isdir( imgdir ):
        os.mkdir( imgdir )
    
    # read source file
    with open( filepath ) as file:
        data = file.read()
    
    # build roots
    root = ET.fromstring(data)
    local_root = ET.Element( "root" )
    remote_root = ET.Element( "root" )
    
    # utility vars
    author_list = []
    text_list = []
    links_list = []
    
    # global iter on all spans
    for item in root.iter('span'):
        # for the ones with a class
        if 'class' in item.attrib:
            # collect authors
            if re.match( author_pattern, item.attrib['class'] ):
                author_list.append( item.text )

            # collect postbodies
            if item.attrib['class'] == 'postbody':
                text_list.append( item.text )
                local_links = []
                # list img in postbodies
                for link in item.iter('img'):
                    local_links.append( link.attrib['src'] )
                links_list.append( local_links )
            
    # iter on the results
    counter = 0
    for i in range( 0, len( links_list ) ):
        for item in links_list[i]:
            if not re.match( signaler_pattern, str(item) ):
                print( item )
                url = item
                name = url.split( '/' )[-1]
                extension = url.split( '.' )[-1]
                normalized_name = basename + '_' + str( counter ) + '.' +extension
                time.sleep(0.5)
                try:
                    response = urllib.request.urlopen(url)
                    data = response.read()
                    file = open( imgdir + "/" + normalized_name, 'wb' )
                    file.write( bytearray( data ) )
                except:
                    print("An exception occurred for item at count:", item, counter )
                    copyfile( "Raw/notfound.png", imgdir + '/' + basename + '_' + str( counter ) + '.png' )

                local_item = ET.SubElement( local_root, "entry", author = author_list[i], file = "img/" + normalized_name )
                remote_item = ET.SubElement( remote_root, "entry", author = author_list[i], file = url )
                counter = counter + 1

    tree = ET.ElementTree( local_root )
    tree.write( outdir + "/local.xml" )
    tree = ET.ElementTree( remote_root )
    tree.write( outdir + "/remote.xml" )


'''
with open('Raw/CLEAN_PTF_ARCHIVE_KAAOS2.html', 'r') as file:
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

'''
