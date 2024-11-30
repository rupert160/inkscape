from lxml import etree
from xml.dom import minidom
import os
import re

def create_icons(source_directory):
    badname = os.path.basename(source_directory)
    dir=re.sub(r'[\s]+','_',(re.sub(r'[^\w\s-]','',badname)))
    title=dir.title()
    target_file='files/in/sjjb-landuse.svg'
    updated_target_file='files/out/' + dir + '.svg'


    destination_tree = etree.parse(target_file)
    destination_root = destination_tree.getroot()
    destination_root.find('svg:title', destination_root.nsmap).text = 'Azure - ' + title
    destination_root.find('svg:desc', destination_root.nsmap).text = title + ' icons for mapping out diagrams for Microsoft Azure or Cloud'

    # Register namespaces

    (destination_root.find('svg:metadata/rdf:RDF/cc:Work/dc:title', destination_root.nsmap)).text = 'Cloud Architecture icons for ' + title
    (destination_root.find('svg:metadata/rdf:RDF/cc:Work/dc:creator/cc:Agent/dc:title', destination_root.nsmap)).text = 'Rupert Bailey'
    (destination_root.find('svg:metadata/rdf:RDF/cc:Work/dc:rights/cc:Agent/dc:title', destination_root.nsmap)).text = 'Microsoft for images MIT for development'
    (destination_root.find('svg:metadata/rdf:RDF/cc:Work/dc:source', destination_root.nsmap)).text = 'https://learn.microsoft.com/en-us/azure/architecture/icons/'
    (destination_root.find('svg:metadata/rdf:RDF/cc:Work/dc:description', destination_root.nsmap)).text = 'looking after the floss folk not using visio'
    container = destination_root.find('svg:defs', destination_root.nsmap)
    container.clear()

    # Loop through files in the directory
    for filename in os.listdir(source_directory):
        file_path = os.path.join(source_directory, filename)
        if os.path.isfile(file_path):
            print(file_path)
            # Parse the source and destination XML files
            source_tree = etree.parse(file_path)
            source_root = source_tree.getroot()

            # Find the target container in the destination tree
            container2 = etree.SubElement(container, "symbol")
            # Extract elements from the source tree and ...
            t2 = etree.SubElement(container2,'title')
            t2.text = filename
            container2.remove(container2.find('title'))
            container2.append(t2)
            # Insert extracted elements into the container in the destination tree
            svg_elements = source_root.getchildren()
            for item in svg_elements:
                container2.append(item)

    # One-liner to pretty print and write to file
    with open(updated_target_file, "w", encoding='utf-8') as f:
        f.write(minidom.parseString(etree.tostring(destination_tree.getroot(), encoding='utf-8', method='xml')).toprettyxml(indent="    "))

def loop_through_icons():
    path='/home/rupert/Downloads/Azure_Public_Service_Icons_V20/Azure_Public_Service_Icons/Icons'
    for root, dirs, files in os.walk(path):
        print(f"Current directory: {root}")
        create_icons(root)


loop_through_icons()
