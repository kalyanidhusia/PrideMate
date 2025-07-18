import os
import re
import xml.etree.ElementTree as ET

def display_instructions():
    print("""
PRIDE Submission File Cleaner
=============================
Processes .mzid and .MGF files to ensure PRIDE compatibility.

Steps:
1. Ensure Python 3.8+ installed.
2. Install dependencies: pip install -r requirements.txt
3. Place .mzid and .MGF files in one folder.
4. Run: python PRideMate.py
5. Enter the folder path when prompted.
""")

def clean_filename(filename):
    """Sanitize filename to comply with PRIDE: only A-Z a-z 0-9 _ . - allowed."""
    return re.sub(r'[^\w.-]', '_', filename)

def find_mgf_file(mzid_file, folder):
    """Find the matching MGF file based on identifier."""
    base = mzid_file.replace('.mzid', '')
    for file in os.listdir(folder):
        if file.lower().endswith('.mgf') and base in file:
            return file
    return None
def update_mzid_content(mzid_path, new_identifier, mgf_filename, output_dir):
    """Update mzid XML internal references after cleaning malformed characters."""
    import xml.etree.ElementTree as ET

    try:
        # Read and clean raw XML content first
        with open(mzid_path, 'r', encoding='utf-8', errors='replace') as file:
            raw_xml = file.read()

        # Replace known problematic characters
        cleaned_xml = raw_xml.replace('&', '&amp;')  # XML-safe replacement
        cleaned_xml = re.sub(r'[^\x09\x0A\x0D\x20-\x7F\u00A0-\uD7FF\uE000-\uFFFD]', '', cleaned_xml)

        # Write cleaned temporary XML for parsing
        tmp_path = os.path.join(output_dir, f"{new_identifier}_temp.xml")
        with open(tmp_path, 'w', encoding='utf-8') as temp_file:
            temp_file.write(cleaned_xml)

        # Now parse the cleaned XML
        tree = ET.parse(tmp_path)
        root = tree.getroot()
        ns = {'': 'http://psidev.info/psi/pi/mzIdentML/1.1'}
        ET.register_namespace('', ns[''])

        old_identifier = os.path.basename(mzid_path).replace('.mzid', '')

        for elem in root.iter():
            if elem.text and old_identifier in elem.text:
                elem.text = elem.text.replace(old_identifier, new_identifier)
            for attr in elem.attrib:
                if old_identifier in elem.attrib[attr]:
                    elem.attrib[attr] = elem.attrib[attr].replace(old_identifier, new_identifier)

            if elem.tag.endswith("SpectraData") and 'location' in elem.attrib:
                elem.attrib['location'] = mgf_filename

        new_mzid_path = os.path.join(output_dir, f"{new_identifier}.mzid")
        tree.write(new_mzid_path, encoding='utf-8', xml_declaration=True)
        print(f"✔ mzid updated: {new_mzid_path}")

        # Clean up temp file
        os.remove(tmp_path)
        return new_mzid_path

    except Exception as e:
        print(f"❌ Failed to update mzid: {e}")
        return None


def update_mgf_content(mgf_path, new_identifier, output_dir):
    """Update MGF COM= line to new identifier and save cleaned MGF."""
    try:
        new_mgf_path = os.path.join(output_dir, f"{new_identifier}.mgf")
        with open(mgf_path, 'r', encoding='utf-8') as infile:
            lines = infile.readlines()

        with open(new_mgf_path, 'w', encoding='utf-8') as outfile:
            for line in lines:
                if line.startswith("COM="):
                    outfile.write(f"COM={new_identifier}\n")
                else:
                    outfile.write(line)

        print(f"✔ MGF updated: {new_mgf_path}")
        return os.path.basename(new_mgf_path)
    except Exception as e:
        print(f"❌ Failed to update MGF: {e}")
        return None

def process_files(folder_path):
    """Process all mzid + mgf pairs in the folder."""
    if not os.path.exists(folder_path):
        print(f"❌ Folder does not exist: {folder_path}")
        return

    results_dir = os.path.join(folder_path, "results")
    os.makedirs(results_dir, exist_ok=True)

    mzid_files = [f for f in os.listdir(folder_path) if f.endswith('.mzid')]
    for mzid_file in mzid_files:
        mzid_path = os.path.join(folder_path, mzid_file)
        cleaned_identifier = clean_filename(mzid_file.replace(".mzid", ""))

        mgf_file = find_mgf_file(mzid_file, folder_path)
        if not mgf_file:
            print(f"⚠️ No matching MGF found for: {mzid_file}")
            continue

        mgf_path = os.path.join(folder_path, mgf_file)
        updated_mgf_filename = update_mgf_content(mgf_path, cleaned_identifier, results_dir)

        if updated_mgf_filename:
            update_mzid_content(mzid_path, cleaned_identifier, updated_mgf_filename, results_dir)

    print("\n🎉 Processing complete. See 'results/' folder for PRIDE-ready files.")

def main():
    display_instructions()
    folder = input("📁 Enter the full path to your data folder: ").strip()
    process_files(folder)

if __name__ == "__main__":
    main()

