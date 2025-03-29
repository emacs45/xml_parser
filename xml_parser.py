#------------------------------------------------------------------
# This script searches XML files, extracts specific tags and values,
# and saves the results in a human-readable text file.
#------------------------------------------------------------------

import xml.etree.ElementTree as ET
from pathlib import Path
import re

def get_xml_info(root: ET.Element) -> dict:
    """Extracts specific values from an XML tree and returns them in a dictionary."""
    
    result = {}
    tags_to_search = ['Customer', 'Period', 'ReportType', 'Licenses/License']

    for tag in tags_to_search:
        try:
            for element in root.findall(tag):
                if element.tag == 'License':
                    for sub_element in element:
                        if sub_element.tag == 'LicenseCount':
                            result[sub_element.tag] = sub_element.text.strip() if sub_element.text else ''
                else:
                    result[element.tag] = element.text.strip() if element.text else ''
        except Exception as e:
            print(f'[WARN] Could not process tag "{tag}": {e}')

    return result

def write_report(data: dict, output_dir: Path, original_filename: str) -> None:
    """Writes extracted data to a text report in the specified output directory."""
    
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        txt_filename = f'report_{original_filename.replace(".xml", ".txt")}'
        report_path = output_dir / txt_filename

        with report_path.open('w') as file:
            file.write('------ Report ------\n')
            for key, value in data.items():
                file.write(f'{key}: {value}\n')

    except Exception as e:
        print(f'[ERROR] Failed to write report for "{original_filename}": {e}')

def search_xml_files(source_dir: Path, output_dir: Path, pattern: str) -> None:
    """Searches for XML files matching a pattern and generates reports."""

    for file_path in source_dir.rglob('*.xml'):
        if re.search(pattern, file_path.name, re.IGNORECASE):
            try:
                root = ET.parse(file_path).getroot()
                data = get_xml_info(root)
                write_report(data, output_dir, file_path.name)
            except ET.ParseError as e:
                print(f'[ERROR] XML parsing failed for "{file_path.name}": {e}')
            except Exception as e:
                print(f'[ERROR] Failed to process "{file_path.name}": {e}')

#------------------------------------------------------------------
def main():
    source_dir = Path('/opt/xxx')       # Change this path as needed
    output_dir = Path('/tmp/reports')   # Ensure this directory exists or will be created
    file_pattern = r'\.xml$'

    search_xml_files(source_dir, output_dir, file_pattern)

#------------------------------------------------------------------
if __name__ == '__main__':
    main()
