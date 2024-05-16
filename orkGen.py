import zipfile
from lxml import etree
import io

# Path to the .ork ZIP file
og_path = 'D:\Repos\Rocketry\OR-Optimizer\.ork\sample.ork'
path = 'D:\Repos\Rocketry\OR-Optimizer\.cache\\'
# The name of the XML file inside the ZIP
xml_file_name = 'rocket.ork'

def orkGet(filename):
    with zipfile.ZipFile(path+filename, 'r') as z:
        with z.open(xml_file_name) as xml_file:
            tree = etree.parse(xml_file)
            root = tree.getroot()
            coords = list()
            for element in root.iter("point"):
                # Find and print all parent tags up to the root
                parents = []
                parent = element.getparent()
                while parent is not None:
                    parents.append(parent.tag)  # Collect all parent tags
                    parent = parent.getparent()
                
                parents.reverse()

                coords.append([float(element.get('x')),float(element.get('y'))])
            return coords


def orkGen(filename, coords=list()):
    i = 0
    flag = True
    with zipfile.ZipFile(og_path, 'r') as z:
        # Read the XML file from the ZIP
        with z.open(xml_file_name) as xml_file:
            # Parse the XML file
            tree = etree.parse(xml_file)
            root = tree.getroot()

            xml_data = etree.tostring(root, pretty_print=True)
            for element in root.iter("point"):
                element.set('x', str(coords[i][0]))
                element.set('y', str(coords[i][1]))
                xml_data = etree.tostring(root, pretty_print=True)
                i+=1

        with zipfile.ZipFile('D:\Repos\Rocketry\OR-Optimizer\.cache\\'+filename, 'w') as new_z:
            # Write the modified XML back into a new ZIP file
            new_z.writestr(xml_file_name, xml_data)
            
            # Copy other files from the original ZIP if there are any
            for item in z.infolist():
                if item.filename != xml_file_name:  # Avoid the file we already modified
                    new_z.writestr(item, z.read(item.filename))
    return True