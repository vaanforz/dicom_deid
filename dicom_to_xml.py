# For data extraction and conversion to xml
import os
import shutil
import pydicom

print('\n\n\n -------------------------------------------------------------------------------------------------------')
print(' ---------------------------     DICOM to XML Converter     ------------------------')
print(' -------------------------------------------------------------------------------------------------------')
print(' ------- This program extracts the header information from DICOM Images.')
print(' ------- It de-identify patient\'s NRIC and remove patient\'s name from meta data.')
# print(' ------- To run this program correctly, you need to follow following steps')
# print(' ------- Step 1 : Create folder name "DICOM Files" where this program is stored.')
# print(' ------- Step 2 : Copy all DICOM files that needs to be process.')
# print(' ------- Step 3 : All extracted ".xml" files will be created in "DICOM Files" folder.')

print(' Note : Remember, this program won\'t effect the original DICOM Images which still contains identifiers.')
print('        Therefore, User of this software will need to ensure the security of the original DICOM Images.')
print(' -------------------------------------------------------------------------------------------------------')

def generate_xml(filename, output_fields):
    out_file = open('./xml_output/' + filename[:-4] + '.xml', 'w')
    out_file.writelines('<?xml version="1.0" encoding="UTF-8" ?>\n')
    out_file.writelines('<File>\n')
    out_file.writelines('<FileName>' + filename + '</FileName>\n')
    for field in output_fields:
        out_file.writelines('<' + field[0] + '>' + field[1] + '</' + field[0]  + '>\n')
    out_file.writelines('</File>\n')

try: #create folder for storing xml outputs
    os.mkdir("./xml_output")
    os.mkdir("./derived_secondary_dicom")
except:
    pass

fields_to_anonymize = ['PatientsName', 'PatientID', 'AccessionNumber', 'PixelData']
# fields_to_retain = ['Manufacturer','ManufacturerModelName',
#                     'StudyInstanceUID','SeriesInstanceUID',
#                     'ImagePositionPatient','ImageOrientationPatient'
#                     ]
for file in os.listdir("./dicom_input/"):
    if('.dcm' not in file): #check for dicom file extension
        continue
    dicom_file = pydicom.dcmread("./dicom_input/" + file)
    if(dicom_file.data_element('ImageType') == None):
        shutil.move("./dicom_input/" + file, "./derived_secondary_dicom/" + file)
        continue
    if('derived' in (str(dicom_file['ImageType'].value)).lower()): #transfer derived/secondary files for isolation first
        shutil.move("./dicom_input/" + file, "./derived_secondary_dicom/" + file)
        continue
    output_fields = []
    dicom_file.remove_private_tags()
    for elem in dicom_file.iterall():
        elem_name = ''.join(e for e in elem.name if e.isalnum())
        if(elem_name in fields_to_anonymize):
            output_fields.append((elem_name,'Anonymized'))
        else:
            output_fields.append((elem_name,str(elem.value)))
    # for field in fields_to_anonymize:
    #     if(dicom_file.data_element(field) != None):
    #         output_fields.append((field,'Anonymized'))
    # for field in fields_to_retain:
    #     if(dicom_file.data_element(field) != None):
    #         output_fields.append((field,str(dicom_file[field].value)))
    generate_xml(file, output_fields)
    print('Processed ' + file)

print('\n------------------------------------------------------------------------------------------------------------------------------------------------')
print('------------------------------------------     D A T A     E X T R A C T I O N     C O M P L E T E    ------------------------------------------')
print('------------------------------------------------------------------------------------------------------------------------------------------------')

    