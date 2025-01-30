import pandas as pd
import os
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import checkboxlist_dialog

def collect_metadata():
    # Collect basic metadata for the experiment
    organism = input("Enter the organism (e.g., Homo sapiens): ")
    instrument = input("Enter the instrument used (e.g., Orbitrap Fusion): ")
    enzyme = input("Enter the digest enzyme used (e.g., trypsin): ")
    mass_tolerance = input("Enter the precursor mass tolerance (e.g., 7 ppm): ")
    frag_tolerance = input("Enter the fragment mass tolerance (e.g., 0.02 Da): ")
    
    return {
        "organism": organism,
        "instrument": instrument,
        "enzyme": enzyme,
        "mass_tolerance": mass_tolerance,
        "frag_tolerance": frag_tolerance
    }

def load_sample_list():
    # Ask for the path to the sample list
    while True:
        sample_path = input("Enter the path to the Sample_List_andNotes.xlsx: ").strip()
        if os.path.exists(sample_path):
            try:
                sample_data = pd.ExcelFile(sample_path)
                return sample_data
            except Exception as e:
                print(f"Error loading file: {e}")
        else:
            print("File not found. Please enter a valid path.")

def select_samples(sample_df):
    # Ensure valid sample IDs
    sample_df = sample_df.dropna(subset=['sample ID'])
    sample_ids = sample_df['sample ID'].unique().tolist()
    
    if not sample_ids:
        print("No valid sample IDs found in the file. Exiting.")
        exit()
    
    # Present available Sample IDs for selection
    selected_samples = checkboxlist_dialog(
        title="Select Samples",
        text="Tick the samples you want to include:",
        values=[(sample, sample) for sample in sample_ids]
    ).run()
    
    if not selected_samples:
        print("No samples selected. Exiting.")
        exit()
    
    return sample_df[sample_df['sample ID'].isin(selected_samples)]

def create_sdrf_file(sample_df, metadata, output_file):
    # Add metadata columns to the sample data
    sdrf_data = sample_df.copy()
    sdrf_data['characteristics[organism]'] = metadata['organism']
    sdrf_data['comment[instrument]'] = f"NT={metadata['instrument']};AC=MS:1002877"
    sdrf_data['comment[modification parameters]'] = "NT=Carbamidomethyl;TA=C;MT=fixed;AC=UNIMOD:4"
    sdrf_data['comment[modification parameters].1'] = "NT=Oxidation;MT=variable;TA=M;AC=UNIMOD:35"
    sdrf_data['comment[digest enzyme]'] = metadata['enzyme']
    sdrf_data['comment[precursor mass tolerance]'] = metadata['mass_tolerance']
    sdrf_data['comment[fragment mass tolerance]'] = metadata['frag_tolerance']
    
    # Save the SDRF file
    sdrf_data.to_csv(output_file, sep='\t', index=False)
    print(f"SDRF file generated: {output_file}")

def main():
    # Load sample list
    sample_data = load_sample_list()
    sheet_name = sample_data.sheet_names[0]  # Assume first sheet if no specific sheet is given
    sample_df = sample_data.parse(sheet_name)

    # Select samples
    selected_samples_df = select_samples(sample_df)
    
    # Collect metadata
    metadata = collect_metadata()
    
    # Ask for output file name
    output_file = input("Enter the name of the output SDRF file (e.g., generated_sdrf.tsv): ").strip()
    
    # Create SDRF file
    create_sdrf_file(selected_samples_df, metadata, output_file)

if __name__ == "__main__":
    main()