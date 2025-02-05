Welcome to the PRIDE Submission Helper repository! 🎉 

This project was born out of real-world challenges faced during the submission of proteomics datasets to the ProteomeXchange Consortium via PRIDE.
If you’ve ever struggled with file naming conventions, metadata preparation, or validation errors, you’re in the right place! This repository is designed to make your life easier by providing scripts and tools to streamline the submission process.

# PrideMate
This tool assists researchers in preparing PriDE submissions by renaming files and their content, streamlining data processing, and ensuring project-specific compliance.

This README outlines the challenges faced during the PRIDE submission process for a BioID mass spectrometry dataset and provides a comprehensive checklist to help others streamline their submissions.

## Why This Project?
Submitting datasets to PRIDE can be challenging due to stringent requirements and complex workflows. Here are some of the common issues we encountered:

File Naming Restrictions: PRIDE enforces strict naming conventions (e.g., only 0–9, A–Z, _, and -), causing validation errors when special characters appear in filenames.
Instrument Metadata: Limited options in PRIDE’s controlled vocabulary for instrument names can make it tricky to represent your setup accurately.
File Dependencies: Simply renaming files isn’t enough if internal file references (e.g., in .mzIdentML) point to outdated names, leading to submission failures.
Metadata Completeness: Ensuring that all experimental details (e.g., sample prep, quantification methods, modifications) are accurately described takes time and precision.
Validation Hurdles: PRIDE’s validation process often requires multiple iterations to meet compliance, adding delays.


## Checklist for PRIDE Submission

Use the following checklist to ensure all steps are completed successfully. Check off items as you proceed.

### 1. Prepare Data
- [ ] Collect `.raw` or equivalent instrument output files.
- [x] Ensure filenames comply with PRIDE’s naming conventions (0–9, A–Z, `_`, `-`).

### 2. Process Data
- [x] Validate all `.mzIdentML`, `.mzTab`, and processed files.

### 3. Metadata Preparation
- [x] Provide detailed sample preparation protocols.
- [ ] Include search parameters (e.g., fixed/variable modifications, database, software version).
- [ ] Select the closest instrument match from PRIDE’s controlled vocabulary.

### 4. File Organization
- [ ] Organize raw, processed, and metadata files into separate directories.
- [x] Generate a `checksum.txt` file for all submitted files.

### 5. Submission Process
- [x] Use the PRIDE Submission



## Installation and Usage Guide
Here's the updated requirements.txt content for cross-platform compatibility and a command to set it up:

### requirements.txt

```
lxml
rename
elementpath
speedcopy
xmlschema
speedcopy
```
## Setup Command

Ensure you have Python 3.9+ installed.

Run the following command to install the dependencies:
`pip install -r requirements.txt`

This setup avoids Conda and ensures compatibility across operating systems.




### Reach out to us at KDhusia@uams.edu and DProvince@uams.edu for help !!!

Let’s make proteomics submissions a breeze! 😊 Fork this repo, give it a ⭐, and help us build a more efficient way to share data with the scientific community.
