import os
import pydicom
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from PIL import Image
import time

print('\n\n\n -------------------------------------------------------------------------------------------------------')
print(' ---------------------------     OCR Top 10% Image Masking     ------------------------')
print(' -------------------------------------------------------------------------------------------------------')

try: #create folder for storing xml outputs
    os.mkdir("./output")
except:
    pass

def mask_top10(input_file):
    try: dicom_file = pydicom.dcmread("./dicom_input/" + input_file)
    except:
        print('Error! Not a valid dicom file. ' + input_file)
        return

    height = dicom_file.pixel_array.shape[0]
    width = dicom_file.pixel_array.shape[1]
    original_file_pixeldata = str(dicom_file['PixelData'])

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.axis('off')
    plt.imshow(dicom_file.pixel_array, cmap="gray")
    rect = patches.Rectangle((0, 0), width, height*0.1, facecolor='black')
    ax.add_patch(rect)

    plt.gca().set_axis_off()
    plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
    plt.margins(0,0)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    plt.savefig('./temp.png', bbox_inches='tight', pad_inches=0, dpi = 200)
    time.sleep(2)

    im = Image.open("./temp.png").convert('L')
    im = im.resize((width, height))
    dicom_file.PixelData = (np.asarray(im).astype(dicom_file.pixel_array.dtype)).tobytes()

    if(original_file_pixeldata == str(dicom_file['PixelData'])):
        pydicom.filewriter.dcmwrite('./output/' + file, dicom_file)
        print('Processed ' + file)
    else:
        print('Output file pixeldata doesnt seem to match input ' + file)

for file in os.listdir("./dicom_input/"):
    mask_top10(file)

print('\n------------------------------------------------------------------------------------------------------------------------------------------------')
print('------------------------------------------    M A S K I N G     C O M P L E T E    ------------------------------------------')
print('------------------------------------------------------------------------------------------------------------------------------------------------')

    