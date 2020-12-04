
from supportFunc import ocr_space_file as ocrFile
import json, regex
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np

# Image name 
image_name = 'img2.png'

# Running OCR on given file
print('Running OCR on given image')
test_file = ocrFile(filename=image_name, language='eng',overlay=True,OCREngine=1)

# Converting string from OCR to json object
test_file = json.loads(test_file)

# To See if there is any error
print('Error While Running OCR: ',test_file['IsErroredOnProcessing'])
if str(test_file['IsErroredOnProcessing']) == 'False':
    # Seperating overlay text only
    test_file = test_file['ParsedResults'][0]
    test_file = test_file['TextOverlay']['Lines']

    print('Colatting Coordinates of text identified by OCR')
    coor = []

    for i in range(len(test_file)):
        interm = test_file[i]
        
        line = interm['LineText']
        words = interm['Words']
        
        # # For Specific word
        # print('Looking for coordinated of target word')
        # result = regex.search('.*\s?^?(toshi[A-Za-z0-9]*)\s?.*',line, regex.IGNORECASE)
        # if result:
        #     match_text = result.group(1)
        
        #     for words_num in range(len(words)):
        #         interm_pair = words[words_num]
        #         if interm_pair['WordText'] == result.group(1):
        #             coor.append([interm_pair['Left'],interm_pair['Top'],interm_pair['Height'],interm_pair['Width']])

        # For Specific word
        for words_num in range(len(words)):
            interm_pair = words[words_num]
            coor.append([interm_pair['Left'],interm_pair['Top'],interm_pair['Height'],interm_pair['Width']])
            
    # Applying patches on the image
    print('Applying Patches on The Image')
    if len(coor) > 0:
        # Opening image file as numpy array
        im = np.array(Image.open(image_name), dtype=np.uint8)

        # Create figure and axes
        fig,ax = plt.subplots(1)

        # Display the image
        ax.imshow(im)

        # Create a Rectangle patch
        # rect = patches.Rectangle((coor[0]-1,coor[1]-1),coor[3],coor[2],linewidth=1,edgecolor='r',facecolor='black')
        for i in range(len(coor)):
            interm = coor[i]
            rect = patches.Rectangle((interm[0]-1,interm[1]-1),interm[3]+2,interm[2]+2,facecolor='black')

            # Add the patch to the Axes
            ax.add_patch(rect)

        plt.show()

    else:
        print('Cannot find anything')
