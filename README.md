# PrideMate
This tool assists researchers in preparing PriDE submissions by renaming files and their content, streamlining data processing, and ensuring project-specific compliance.

This README outlines the challenges faced during the PRIDE submission process for a BioID mass spectrometry dataset and provides a comprehensive checklist to help others streamline their submissions.

Problems Faced During PRIDE Submission
File Naming Restrictions
PRIDE requires file names to include only alphanumeric characters, underscores (_), and hyphens (-). Parentheses and other special characters automatically generated by MASCOT caused validation errors, as these characters were also referenced internally within files.

Instrument Metadata
The specific model used (Thermo Scientific Orbitrap Eclipse) was not listed in PRIDE’s controlled vocabulary. The closest matches, Orbitrap Fusion or Orbitrap Lumos, had to be selected, with the actual instrument details clarified in comments.

Quantification Method
The normalization method used (NSAF) needed to be clearly explained. While PRIDE supports spectral counting, additional steps were required to align the study’s methods with PRIDE’s requirements.

File Dependency Issues
Renaming files externally was not sufficient, as many files referenced parenthetical identifiers internally, leading to validation errors. Reanalysis of raw data was initially considered but was avoided with alternative adjustments.

Metadata Completeness
Metadata for experimental setup, modifications, and database search parameters had to be meticulously detailed to meet PRIDE standards, requiring careful cross-referencing of protocols and intermediate data.

Validation Delays
Multiple iterations were required to meet PRIDE’s validation criteria, including adjustments to file formats, naming conventions, and controlled vocabulary terms.

Checklist for PRIDE Submission
Use the following checklist to ensure all steps are completed successfully. Tick (✔) or cross (✖) each step as you proceed.

Step	Status
1. Prepare Raw Data	⬜
- Collect .raw or equivalent instrument output files.	⬜
- Ensure filenames comply with PRIDE’s naming conventions (0–9, A–Z, _, -).	⬜
2. Process Data	⬜
- Validate all .mzIdentML, .mzTab, and processed files.	⬜
- Ensure quantification methods (e.g., NSAF) are properly described.	⬜
3. Metadata Preparation	⬜
- Provide detailed sample preparation protocols.	⬜
- Include search parameters (e.g., fixed/variable modifications, database, software version).	⬜
- Select the closest instrument match from PRIDE’s controlled vocabulary.	⬜
4. File Organization	⬜
- Organize raw, processed, and metadata files into separate directories.	⬜
- Generate a checksum.txt file for all submitted files.	⬜
5. Submission Process	⬜
- Use the PRIDE Submission Tool to upload files.	⬜
- Ensure compliance with PRIDE’s validation tool.	⬜
- Add a descriptive abstract and methods section.	⬜
6. Final Review and Submission	⬜
- Cross-check all metadata for accuracy and completeness.	⬜
- Ensure all files pass PRIDE’s validation criteria.	⬜
- Submit the dataset and record the assigned PXD accession number.	⬜
Tips for Success
File Naming: Address special characters in filenames early in the process to avoid cascading issues.
Validation Tool: Regularly use PRIDE’s validation tool to identify and resolve issues iteratively.
Documentation: Maintain detailed records of experimental protocols and file dependencies to streamline metadata preparation.
Collaboration: Coordinate with collaborators early to resolve gaps in raw data or metadata.
This guide is designed to make your PRIDE submission smoother and minimize delays.
