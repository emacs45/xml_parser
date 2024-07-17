#------------------------------------------------------------------
# This script searches xml files and parses particular xml tags
# which contain several values and saves those to a txt file.
#------------------------------------------------------------------
import xml.etree.ElementTree as ET 
import os
import re

def get_xml_info(root: ET) -> dict:
    '''searches and returns xml values'''

    result = {}

    #please define xml tags here
    tags = ['Customer', 'Period', 'ReportType', 'Licenses/License']

    for tg in tags:
        try:

            for child in root.findall(tg):
                if child.tag == 'License':
                    for ch in child:
                        if ch.tag == 'LicenseCount':
                            result[ch.tag] = ch.text
                else:    
                    result[child.tag] = child.text  
        
        except AttributeError as e:
            print(f'Error finding tag {tg}: {e}')

    return result

def write_report(processed_data: dict, target_path: str, target_file_name: str) -> None:
    '''writes report to txt file'''

    try:
        target_file_name = target_file_name.replace('.xml', '.txt')
        target_file = os.path.join(target_path, f'report_{target_file_name}')
        with open (target_file,'w') as file:
            file.write('------Report------\n')
            for key, value in processed_data.items():
                file.write(f'{key}: {value}\n')
    
    except FileNotFoundError as e:
        print(f'Error: {e}')

def search_xml_files(path: str, target_path: str, file_pattern: str) -> None:
    '''searches for xml files in target directory'''

    for dirpath, _, files in os.walk(path):
        for file in files:
            if re.search(file_pattern, file, re.IGNORECASE):
                
                target_file = os.path.join(dirpath, file)
                try:
                    root = ET.parse(target_file).getroot()
                    write_report(get_xml_info(root), target_path, file)
                except ET.ParseError as e:
                        print(f'Error parsing {file}: {e}')
                except FileNotFoundError as e:
                    print(f'Error processing {file}: {e}')
#------------------------------------------------------------------  
def main():
    # please change source path e.g. /opt/xxx/
    path = '/opt/xxx/'
    # please change target path e.g. /tmp/reports also make sure directory exists
    target_path = '/tmp/reports'
    # Regex Pattern
    file_pattern = r'.xml$'
    search_xml_files(path, target_path, file_pattern)
#------------------------------------------------------------------
if __name__ == '__main__':
    main()
    