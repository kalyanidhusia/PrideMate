Welcome to the PRIDE Submission Helper repository! 🎉 This project was born out of real-world challenges faced during the submission of proteomics datasets to the ProteomeXchange Consortium via PRIDE.
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

### 1. Prepare Raw Data
- [ ] Collect `.raw` or equivalent instrument output files.
- [ ] Ensure filenames comply with PRIDE’s naming conventions (0–9, A–Z, `_`, `-`).

### 2. Process Data
- [ ] Validate all `.mzIdentML`, `.mzTab`, and processed files.
- [ ] Ensure quantification methods (e.g., NSAF) are properly described.

### 3. Metadata Preparation
- [ ] Provide detailed sample preparation protocols.
- [ ] Include search parameters (e.g., fixed/variable modifications, database, software version).
- [ ] Select the closest instrument match from PRIDE’s controlled vocabulary.

### 4. File Organization
- [ ] Organize raw, processed, and metadata files into separate directories.
- [ ] Generate a `checksum.txt` file for all submitted files.

### 5. Submission Process
- [ ] Use the PRIDE Submission


Tips for Success
File Naming: Address special characters in filenames early in the process to avoid cascading issues.
Validation Tool: Regularly use PRIDE’s validation tool to identify and resolve issues iteratively.
Documentation: Maintain detailed records of experimental protocols and file dependencies to streamline metadata preparation.
Collaboration: Coordinate with collaborators early to resolve gaps in raw data or metadata.
This guide is designed to make your PRIDE submission smoother and minimize delays. 

### Reach out to us at KDhusia@uams.edu for help !!!

Let’s make proteomics submissions a breeze! 😊 Fork this repo, give it a ⭐, and help us build a more efficient way to share data with the scientific community.
