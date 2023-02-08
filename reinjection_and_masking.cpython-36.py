import os, pydicom
from pydicom.uid import ExplicitVRLittleEndian
import matplotlib.pyplot as plt, matplotlib.patches as patches, numpy as np
from PIL import Image, ImageDraw
import time, pandas as pd, gc

def reinjection_job():
    dest_folder_path = 'E:/Archives/NUHSARCHIVE/NUHSLIB/Destination_anonymized_csv/'
    try:
        anonymized_csv = os.listdir(dest_folder_path)[0]
        files_to_process_df = pd.read_csv(dest_folder_path + anonymized_csv)
        for index, row in files_to_process_df.iterrows():
            try:
                reinject_meta_and_mask(row)
            except:
                continue

        os.rename(dest_folder_path + anonymized_csv, 'E:/Archives/NUHSARCHIVE/NUHSLIB/Destination_anonymized_csv_backup/' + anonymized_csv)
        print('Completed reinjecting from ' + anonymized_csv)
    except:
        pass


def reinject_meta_and_mask(row):
    input_file_path = row['File_Path']
    if row['Modality'] == 'SR':
        return
    else:
        if row['ImageType'] != None:
            if row['Modality'] != 'US':
                if 'derived' in row['ImageType'].lower():
                    if row['Modality'] == 'DX' or row['Modality'] == 'XA' or row['Modality'] == 'CT':
                        pass
                else:
                    return
            elif 'localizer' in row['ImageType'].lower() or 'screen save' in row['ImageType'].lower():
                return
    try:
        dicom_file = pydicom.dcmread(input_file_path, force=True)
        dicom_file.remove_private_tags()
        dicom_file.PatientName = row['PatientName']
        dicom_file.PatientID = row['PatientID']
        dicom_file.AccessionNumber = row['AccessionNumber']
    except Exception as e:
        return

    try:
        if 'report' in str(dicom_file[(8, 4158)].value).lower():
            return
    except:
        pass

    try:
        dicom_file.PatientBirthDate = None
    except:
        pass

    try:
        dicom_file.ReferringPhysicianName = None
    except:
        pass

    try:
        dicom_file.InstitutionName = None
    except:
        pass

    try:
        dicom_file.InstitutionAddress = None
    except:
        pass

    try:
        dicom_file.PatientAddress = None
    except:
        pass

    try:
        dicom_file.OperatorsName = None
    except:
        pass

    try:
        dicom_file.PerformingPhysicianName = None
    except:
        pass

    try:
        dicom_file.ProtocolName = None
    except:
        pass

    try:
        dicom_file[(8, 4168)].value = None
    except:
        pass

    try:
        dicom_file[(50, 4146)].value = None
    except:
        pass

    try:
        dicom_file[(32, 16)].value = None
    except:
        pass

    try:
        dicom_file[(8, 4437)].value = None
    except:
        pass

    try:
        dicom_file[(8, 4368)].value = None
    except:
        pass

    try:
        dicom_file[(64, 9)].value = None
    except:
        pass

    try:
        dicom_file[(64, 4097)].value = None
    except:
        pass

    try:
        dicom_file[(64, 629)].value = None
    except:
        pass

    try:
        dicom_file[(32, 13)].value = None
    except:
        pass

    try:
        dicom_file[(8, 4160)].value = None
    except:
        pass

    try:
        dicom_file[(16, 4096)].value = None
    except:
        pass

    try:
        dicom_file[(16, 4097)].value = None
    except:
        pass

    try:
        dicom_file[(16, 8532)].value = None
    except:
        pass

    try:
        dicom_file[(64, 8215)].value = None
    except:
        pass

    try:
        dicom_file[(8, 4144)].value = None
    except:
        pass

    try:
        dicom_file[(16, 4192)].value = None
    except:
        pass

    try:
        dicom_file[(16, 16384)].value = None
    except:
        pass

    try:
        dicom_file[(50, 4147)].value = None
    except:
        pass

    if dicom_file.Modality == 'US' or dicom_file.Modality == 'NM':
        try:
            height = dicom_file.pixel_array.shape[0]
            width = dicom_file.pixel_array.shape[1]
            fig = plt.figure()
            ax = fig.add_subplot(111)
            ax.axis('off')
            plt.imshow((dicom_file.pixel_array), cmap='gray')
            rect = patches.Rectangle((0, 0), width, (height * 0.1), facecolor='black')
            ax.add_patch(rect)
            plt.gca().set_axis_off()
            plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
            plt.margins(0, 0)
            plt.gca().xaxis.set_major_locator(plt.NullLocator())
            plt.gca().yaxis.set_major_locator(plt.NullLocator())
            temp_img_file_path = 'E:/Archives/NUHSARCHIVE/NUHSLIB/temp.png'
            plt.savefig(temp_img_file_path, bbox_inches='tight', pad_inches=0, dpi=200)
            plt.cla()
            plt.clf()
            plt.close('all')
            plt.close(fig)
            gc.collect()
            time.sleep(0.3)
            if dicom_file.PhotometricInterpretation == 'MONOCHROME2':
                im = Image.open(temp_img_file_path).convert('L').resize((width, height))
            else:
                if dicom_file.PhotometricInterpretation == 'RGB':
                    im = Image.open(temp_img_file_path).convert('RGB').resize((width, height))
                try:
                    dicom_file.PixelData = np.asarray(im).astype(dicom_file.pixel_array.dtype).tobytes()
                except:
                    pass

                try:
                    dicom_file.PixelData = np.asarray(im).astype(dicom_file.pixel_array.dtype).tobytes()
                    dicom_file.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian
                except:
                    pass

        except Exception as e:
            print('Image Masking Failed:', input_file_path, e)
            return

    output_file_path = 'E:/Archives/NUHSARCHIVE/NUHSLIB/Outgoing' + '/'.join(input_file_path.split('Incoming')[1].split('/')[:-1])
    try:
        os.makedirs(output_file_path)
    except:
        pass

    output_file_name = input_file_path.split('/')[-1]
    pydicom.filewriter.dcmwrite(output_file_path + '/' + output_file_name, dicom_file)


ic_counter = 1

def rename_nric_folder(ic_counter):
    outgoing_folder = 'E:/Archives/NUHSARCHIVE/NUHSLIB/Outgoing/'
    for year in os.listdir(outgoing_folder):
        for month in os.listdir(outgoing_folder + year + '/'):
            for day in os.listdir(outgoing_folder + year + '/' + month + '/'):
                for nric in os.listdir(outgoing_folder + year + '/' + month + '/' + day + '/'):
                    os.rename(outgoing_folder + year + '/' + month + '/' + day + '/' + nric, outgoing_folder + year + '/' + month + '/' + day + '/' + str(ic_counter))
                    ic_counter += 1


reinjection_job()
rename_nric_folder(ic_counter)
