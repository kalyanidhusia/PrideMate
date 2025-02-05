import os
import re
import xml.etree.ElementTree as ET

# Print Instructions
print("##############################")
print("####  python clean_MZID.py PATHTOFOLDER  ####")
print("##############################\n")

def clean_filename(filename):
    """Replace invalid characters in the file name with valid ones."""
    filename = filename.replace("(F004051)", "_F004051")
    filename = re.sub(r'[^A-Za-z0-9_.]', '', filename)
    return filename

def update_mzid_content(mzid_path, new_name, result_dir):
    """Update the content of an mzid file and clean its MGF reference."""
    try:
        tree = ET.parse(mzid_path)
        root = tree.getroot()

        # Namespace handling
        ns = {'': 'http://psidev.info/psi/pi/mzIdentML/1.1'}
        ET.register_namespace('', ns[''])

        old_name = os.path.basename(mzid_path).replace('.mzid', '')
        mgf_file_name = None

        for elem in root.iter():
            # Clean content
            if elem.text and old_name in elem.text:
                elem.text = elem.text.replace(old_name, new_name)
            if elem.attrib:
                for key, value in elem.attrib.items():
                    if old_name in value:
                        elem.attrib[key] = value.replace(old_name, new_name)

            # Update MGF reference in SpectraData
            if elem.tag.endswith('SpectraData') and 'location' in elem.attrib:
                mgf_file_name = os.path.basename(elem.attrib['location'])
                mgf_file_name = clean_filename(mgf_file_name)
                elem.attrib['location'] = mgf_file_name

        # Save updated mzid
        new_mzid_path = os.path.join(result_dir, f"{new_name}.mzid")
        tree.write(new_mzid_path, encoding='utf-8', xml_declaration=True)
        print(f"Updated mzid content saved to: {new_mzid_path}")

        return new_mzid_path, mgf_file_name
    except Exception as e:
        print(f"Error updating mzid file: {e}")
        return None, None

def update_mgf_file(folder_path, mgf_file_name, result_dir):
    """Rename and clean the referenced MGF file in compliance with PRIDE rules."""
    if not mgf_file_name:
        print("No MGF file found in mzid content. Skipping MGF update.")
        return None

    # Look for MGF file recursively
    mgf_path = None
    for root, _, files in os.walk(folder_path):
        if mgf_file_name in files:
            mgf_path = os.path.join(root, mgf_file_name)
            break

    if not mgf_path:
        print(f"MGF file not found: {mgf_file_name}")
        return None

    try:
        # Read and clean MGF content
        with open(mgf_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        updated_lines = []
        for line in lines:
            if line.startswith("COM="):
                updated_lines.append(f"COM={mgf_file_name}\n")
            else:
                updated_lines.append(line)

        # Save cleaned MGF
        new_mgf_path = os.path.join(result_dir, mgf_file_name)
        with open(new_mgf_path, 'w', encoding='utf-8') as f:
            f.writelines(updated_lines)

        print(f"Updated MGF content saved to: {new_mgf_path}")
        return new_mgf_path
    except Exception as e:
        print(f"Error updating MGF file: {e}")
        return None

def process_folder(folder_path):
    """Recursively process all .mzid files and their corresponding .MGF files."""
    if not os.path.exists(folder_path):
        print(f"Error: Folder {folder_path} does not exist.")
        return

    # Create result_MZID folder
    result_dir = os.path.join(folder_path, "result_MZID")
    os.makedirs(result_dir, exist_ok=True)

    # Recursively process files
    for root, _, files in os.walk(folder_path):
        mzid_files = [f for f in files if f.endswith('.mzid')]

        for mzid_file in mzid_files:
            mzid_path = os.path.join(root, mzid_file)
            new_name = clean_filename(mzid_file.replace(".mzid", ""))
            print(f"\nProcessing mzid file: {mzid_path}")

            # Clean mzid file and get referenced MGF
            updated_mzid_path, mgf_file_name = update_mzid_content(mzid_path, new_name, result_dir)

            # Process corresponding MGF file
            if mgf_file_name:
                update_mgf_file(folder_path, mgf_file_name, result_dir)

    print("\nProcessing complete. Cleaned files are saved in 'result_MZID'.")

if __name__ == "__main__":
    folder_path = input("Enter the folder path containing .mzid files: ").strip()
    process_folder(folder_path)
