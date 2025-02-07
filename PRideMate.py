
def display_instructions():
    """Display how to use the script."""
    print("""
PRIDE Submission File Cleaner
=============================
This script processes `.mzid` and `.MGF` files to comply with PRIDE submission rules.

## How to Use ##
1. Install Python 3.8+ if not already installed.
2. Create conda env using the given yml 
` conda env create -f pride_env.yml`

3. Place the `.mzid` and `.MGF` files all in the one folder.
4. Run the script:

   - Use: `python PRideMate.py`
   
5. Enter the full folder path containing the `.mzid` and `.MGF` files when prompted.

""")

# Other existing functions like clean_filename(), main(), etc.



import os
import re
import xml.etree.ElementTree as ET
from speedcopy import copyfile

def clean_filename(filename):
    """Replace invalid characters in the file name with valid ones."""
    filename = filename.replace("(F004051)", "_F004051")
    filename = re.sub(r'[^A-Za-z0-9_.]', '', filename)
    return filename

def find_mgf_file(mzid_file, folder_path):
    """Locate the corresponding MGF file for a given mzid file."""
    mzid_identifier = mzid_file.replace(".mzid", "")
    for file in os.listdir(folder_path):
        if file.endswith(".MGF") and mzid_identifier in file:
            return os.path.join(folder_path, file)
    return None

def update_mzid_content(mzid_path, new_name, mgf_file_name, results_dir):
    """Update the content of an mzid file to reflect the new file name and MGF reference."""
    try:
        tree = ET.parse(mzid_path)
        root = tree.getroot()
        ns = {'': 'http://psidev.info/psi/pi/mzIdentML/1.1'}
        ET.register_namespace('', ns[''])
        
        old_name = os.path.basename(mzid_path).replace('.mzid', '')
        for elem in root.iter():
            # Replace old identifier in text and attributes
            if elem.text and old_name in elem.text:
                elem.text = elem.text.replace(old_name, new_name)
            if elem.attrib:
                for key, value in elem.attrib.items():
                    if old_name in value:
                        elem.attrib[key] = value.replace(old_name, new_name)

            # Update the SpectraData location attribute to the new MGF file name
            if elem.tag.endswith('SpectraData') and 'location' in elem.attrib:
                elem.attrib['location'] = mgf_file_name

        # Save the updated file
        new_path = os.path.join(results_dir, f"{new_name}.mzid")
        tree.write(new_path, encoding='utf-8', xml_declaration=True)
        print(f"Updated mzid content saved to: {new_path}")
        return new_path
    except Exception as e:
        print(f"Error updating mzid file: {e}")
        return None

def update_mgf_content(mgf_path, new_identifier, results_dir):
    """Update the content of the MGF file to reflect the new identifier."""
    try:
        with open(mgf_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        updated_lines = []
        for line in lines:
            if line.startswith("COM="):
                updated_lines.append(f"COM={new_identifier}\n")
            else:
                updated_lines.append(line)
        
        new_file_name = f"{new_identifier}.MGF"
        new_file_path = os.path.join(results_dir, new_file_name)
        with open(new_file_path, 'w', encoding='utf-8') as f:
            f.writelines(updated_lines)
        
        print(f"Updated MGF content saved to: {new_file_path}")
        return new_file_name
    except Exception as e:
        print(f"Error updating MGF file: {e}")
        return None

def process_files_in_folder(folder_path):
    """Process all .mzid files in the given folder and their corresponding .MGF files."""
    if not os.path.exists(folder_path):
        print(f"Error: Folder {folder_path} does not exist.")
        return
    
    results_dir = os.path.join(folder_path, "results")
    os.makedirs(results_dir, exist_ok=True)
    
    mzid_files = [f for f in os.listdir(folder_path) if f.endswith('.mzid')]
    for mzid_file in mzid_files:
        mzid_path = os.path.join(folder_path, mzid_file)
        new_identifier = clean_filename(mzid_file.replace(".mzid", ""))
        print(f"\nProcessing mzid file: {mzid_path}")

        # Look for corresponding MGF file
        mgf_path = find_mgf_file(mzid_file, folder_path)
        if mgf_path:
            print(f"Found corresponding MGF file: {mgf_path}")
            mgf_file_name = update_mgf_content(mgf_path, new_identifier, results_dir)
        else:
            print(f"No corresponding MGF file found for: {mzid_file}")
            mgf_file_name = None

        # Clean mzid file and reference the correct MGF file
        if mgf_file_name:
            mgf_file_name_full_path = os.path.join(results_dir, mgf_file_name)
            update_mzid_content(mzid_path, new_identifier, mgf_file_name_full_path, results_dir)
        else:
            print(f"Skipping mzid update due to missing MGF file for: {mzid_file}")
    
    print("\nProcessing complete. Cleaned files saved in the 'results' folder.")

def main():
    print("PRIDE Submission File Cleaner")
    folder_path = input("Enter the full folder path containing the files: ").strip()
    process_files_in_folder(folder_path)

if __name__ == "__main__":
    display_instructions()
    main()
