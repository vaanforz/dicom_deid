import os, shutil, time, pydicom, pandas as pd
from datetime import date

def output_idt_csv_job():
    AIO_PICKUP_folder_path = 'E:/AIO_PICKUP/'
    recon_file = ''
    for file in os.listdir(AIO_PICKUP_folder_path):
        if 'AIO_Recon' in file:
            if '.csv' in file:
                recon_file = file
                break

    if recon_file == '':
        return
    recon_df = pd.read_csv(AIO_PICKUP_folder_path + recon_file)
    os.rename(AIO_PICKUP_folder_path + recon_file, AIO_PICKUP_folder_path + 'archive/' + recon_file)
    print('Moved ', recon_file)
    if recon_df.empty:
        return
    dicom_data = []
    for index, row in recon_df.iterrows():
        dicom_filepath = row['FilePath'].replace('\\', '/')
        py_file = ''
        try:
            py_file = pydicom.dcmread(dicom_filepath, force=True)
        except:
            dicom_data.append(['dicom_filepath', "'Error loading file'", 'None', 'None', 'None', 
             'None', 'None'])
            continue

        ImageType = 'nil'
        try:
            ImageType = str(py_file.ImageType)
        except:
            pass

        Modality = 'nil'
        try:
            Modality = str(py_file.Modality)
        except:
            pass

        try:
            dicom_data.append([dicom_filepath, 'Success', str(py_file.PatientName), str(py_file.PatientID), str(py_file.AccessionNumber), ImageType, Modality])
        except:
            dicom_data.append(['dicom_filepath', "'Error loading attributes'", 'None', 'None', 'None', 
             'ImageType', 'Modality'])

    dicom_df = pd.DataFrame(dicom_data, columns=["'File_Path'", "'Description'", "'PatientName'", "'PatientID'", "'AccessionNumber'", 
     "'ImageType'", "'Modality'"])
    dicom_df.to_csv(('E:/Archives/NUHSARCHIVE/NUHSLIB/Source_data_csv/identifiable_csv_' + recon_file.replace('AIO_Recon_', '')), index=False)
    print('Processed: ', recon_file)


output_idt_csv_job()
# okay decompiling output_idt_csv.cpython-36.pyc
