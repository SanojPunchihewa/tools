import json
import re
import os

# Function to strip HTML tags from a string
def strip_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

# Function to generate HTML with operation details and table
def generate_html_table(json_data):
    # Extract operation name and description
    operation_name = data['operationName']
    operation_description = strip_html_tags(data['help'])

    html = f'??? note "{operation_name}"\n'
    html += f'    {operation_description}\n'
    html += '    <table>\n'
    html += '        <tr>\n'
    html += '            <th>Parameter Name</th>\n'
    html += '            <th>Description</th>\n'
    html += '            <th>Required</th>\n'
    html += '        </tr>\n'

    # Find the Parameters group
    for element in data['elements']:
        for parameter in element['value']['elements']:
            if 'groupName' in parameter['value']:
                group_name = parameter['value']['groupName']
                if group_name == 'Parameters':
                    for param_element in parameter['value']['elements']:
                        param_name = param_element['value']['name']
                        description = strip_html_tags(param_element['value']['helpTip'])
                        required = 'Yes' if param_element['value']['required'] == 'true' else 'No'
                        html += '        <tr>\n'
                        html += f'            <td>{param_name}</td>\n'
                        html += f'            <td>{description}</td>\n'
                        html += f'            <td>{required}</td>\n'
                        html += '        </tr>\n'
    html += '    </table>\n'
    html += '\n'
    html += '    **Sample configuration**\n'
    html += '\n'
    html += '    ```xml\n'
    html += '    <>\n'
    html += '    ```\n'
    html += ' \n'
    html += '    **Sample request**\n'
    html += '\n'
    html += '    ```json\n'
    html += '    {}\n'
    html += '    ```\n'
    return html

# Define the path to the directory containing the JSON files
directory_path = '<CONNECTOR_HOME>/src/main/resources/uischema'

output_html_file = 'connecter_reference_docs.md'

# List all files in the directory
files = os.listdir(directory_path)

# Filter the list to include only JSON files, excluding 'connection.json'
json_files = [file for file in files if file.endswith('.json') and file != 'connection.json']

# Read each JSON file
with open(output_html_file, 'w') as html_file:
    for json_file in json_files:
        file_path = os.path.join(directory_path, json_file)
        
        with open(file_path, 'r') as file:
            try:
                # Load the JSON data
                data = json.load(file)
                html_table = generate_html_table(data)
                # print(html_table)
                html_file.write(html_table + '\n')
                # print(f"Data from {json_file}:")
                # print(data)
            except json.JSONDecodeError as e:
                print(f"Error reading {json_file}: {e}")
