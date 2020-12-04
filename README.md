# Dicom Deidentification

dicom_deid is a repository for deidentifying meta-data and image pixels in dicom files.

## dicom_to_xml.py Usage

Requires the pydicom library and a folder named 'dicom_files' containing dicom files.

```bash
pip install pydicom
python dicom_to_xml.py
```

The script will automatically create 2 additional folders (if not already present):
#### xml_output folder
Contains the xml output from the script, all officials dicom tags are kept and all private tags are deleted. Special fields 
**```['PatientsName', 'PatientID', 'AccessionNumber']```** are anonymized, while **```['PixelData']```** field is not copied due to large array size.
#### derived_secondary_dicom folder
Contains segregated dicom files that remain unprocessed, due to the 'DERIVED' keyword in **```['ImageType']```** field.

## online_OCR.py Usage

To be updated.
