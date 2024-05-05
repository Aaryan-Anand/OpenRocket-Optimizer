import zipfile
from lxml import etree
import io

# Path to the .ork ZIP file
zip_file_path = 'D:\Repos\Rocketry\OR-Optimizer\.ork\sample.ork'

# The name of the XML file inside the ZIP
xml_file_name = 'rocket.ork'

# Open the ZIP file
with zipfile.ZipFile(zip_file_path, 'r') as z:
    # Read the XML file from the ZIP
    with z.open(xml_file_name) as xml_file:
        # Parse the XML file
        tree = etree.parse(xml_file)
        root = tree.getroot()

        # Modify the XML tree
        # Example: Modify an attribute or element
        #for element in root.iter('someElementTag'):
        #    element.set('someAttribute', 'newValue')

        # Prepare the modified XML to write back to the ZIP
        xml_data = etree.tostring(root, pretty_print=True)
        for element in root.iter("point"):
            print(f"Element: {element.tag}, Attributes: {element.attrib}")
            
            # Find and print all parent tags up to the root
            parents = []
            parent = element.getparent()
            while parent is not None:
                parents.append(parent.tag)  # Collect all parent tags
                parent = parent.getparent()
            
            # Reverse the list to show the path from root to the point
            parents.reverse()
            print("Path from root to 'point':", " -> ".join(parents))

            # Retrieve current 'x' and 'y' values (assuming you want to modify them)
            current_x = float(element.get('x'))
            current_y = float(element.get('y'))

            # Example modification: increment each coordinate by some value
            new_x = current_x + 0.1
            new_y = current_y + 0.1

            # Set the new 'x' and 'y' values
            element.set('x', str(new_x))
            element.set('y', str(new_y))

            # Print updated coordinates
            print(f"Updated Point with coordinates x: {new_x}, y: {new_y}")

            xml_data = etree.tostring(root, pretty_print=True)

        
    # Define the new ZIP to write changes into (could overwrite the original after checking)
    with zipfile.ZipFile('D:\Repos\Rocketry\OR-Optimizer\.ork\modified_sample.ork', 'w') as new_z:
        # Write the modified XML back into a new ZIP file
        new_z.writestr(xml_file_name, xml_data)
        
        # Copy other files from the original ZIP if there are any
        for item in z.infolist():
            if item.filename != xml_file_name:  # Avoid the file we already modified
                new_z.writestr(item, z.read(item.filename))