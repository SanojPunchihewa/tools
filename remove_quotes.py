from lxml import etree
import re
import os

def update_xml_file(file_path):
    # Read the XML content from the file
    with open(file_path, 'rb') as file:
        xml_content = file.read()

    # Parse XML
    tree = etree.fromstring(xml_content)

    # Define namespace
    ns = {'ns': 'http://ws.apache.org/ns/synapse'}

    # Find parameter with 'Type: object'
    parameters = tree.xpath("//ns:parameter[contains(@description, 'Type: object')]/@name", namespaces=ns)
    payload_factory = tree.find('.//ns:payloadFactory', namespaces=ns)

    with open(file_path, 'r', encoding='utf-8') as file:
        updated_content = file.read()

    # Print results
    for param_name in parameters:
        print("Updating Parameter:", param_name)
        # Define the search and replacement patterns
        # Create the search pattern and replacement pattern using regex
        # This pattern matches "param_name": "${args.arg<number>}"
        search_pattern = re.compile(rf'"{param_name}": "\${{args\.arg(\d+)}}"')
        
        def replace_func(match):
            # Extract the matched number and create the replacement string
            number = match.group(1)
            return f'"{param_name}": ${{args.arg{number}}}'

        # Perform the replacement using the defined function
        updated_content = search_pattern.sub(replace_func, updated_content)
        
    # Write the updated XML content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(updated_content)

def process_files_in_folder(folder_path):
    # Iterate over all files in the specified folder
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        
        # Check if the file is an XML file
        if os.path.isfile(file_path) and file_name.lower().endswith('.xml'):
            update_xml_file(file_path)
        else:
            print(f'Skipping file: {file_path}')

file_path = '<CONNECTOR_HOME>/src/main/resources/functions/'  

process_files_in_folder(file_path)
