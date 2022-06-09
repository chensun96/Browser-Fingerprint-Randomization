import io
import os
from PIL import Image
import PIL
import glob
location = "/Users/chen/Desktop/testFile/T5"
location2 = "/Users/chen/Desktop/testFile/resizeAds"
document_foler = "/Users/chen/Desktop/testFile/analyzeAds"
'''
  First: replace the location, location2, doucument_folder with the correct address
  Second: before you run, set the enviroment variable GOOGLE_APPLICATION_CREDENTIALS to the path conatins JSON file
  e.g. export GOOGLE_APPLICATION_CREDENTIALS="/Users/chen/Desktop/testFile/privacyandlaw-e6d088e7af21.json"
'''
# Imports the Google Cloud client library
from google.cloud import vision

# shrink the image size to google vision API support
def shrinkSize():
    counter = 1
    for filename in os.listdir(location):
        if not (filename.startswith('.')):
            file_name = os.path.abspath(os.path.join(location, filename))
            image = Image.open(file_name)
            # print(image.size)
            base_width = 360
            image = Image.open(file_name)
            width_percent = (base_width / float(image.size[0]))
            hsize = int((float(image.size[1]) * float(width_percent)))
            image = image.resize((base_width, hsize), PIL.Image.ANTIALIAS)
            #image.save('resizeAds/{}.png'.format(counter))
            image.save('resizeAds/{}.jpg'.format(counter))
            counter += 1
        
    

def main():
    
    shrinkSize()
    
    # The name of the image file to annotate
    for filename in os.listdir(location2):
        if not (filename.startswith('.')):
            file_name = os.path.abspath(os.path.join(location2, filename))
            print("file_name: ", filename)
        
            client = vision.ImageAnnotatorClient()
            # Loads the image into memory
            with io.open(file_name, 'rb') as image_file:
                content = image_file.read()
            image = vision.Image(content=content)

            # Performs texts detection on the image file
            response = client.text_detection(image=image)
            texts = response.text_annotations
            print('Text for :', filename)
            textList = []
            for text in texts:
                #print('\n"{}"'.format(text.description))
                plainText = text.description
                plainText = plainText.replace('\n', ' ')
                textList.append(plainText)
                #vertices = (['({},{})'.format(vertex.x, vertex.y)
                #            for vertex in text.bounding_poly.vertices])
                #print('bounds: {}'.format(','.join(vertices)))
            if response.error.message:
                raise Exception(
                    '{}\nFor more info on error messages, check: '
                    'https://cloud.google.com/apis/design/errors'.format(
                        response.error.message))
            print(textList)

            # Performs logo detection on the image file
            response = client.logo_detection(image=image)
            logos = response.logo_annotations
            print('Logo for: ',filename)
            logoList = []
            for logo in logos:
                # print("\n", logo.description)
                plainLogo = logo.description.replace('\n', ' ')
                logoList.append(plainLogo)
            if response.error.message:
                raise Exception(
                    '{}\nFor more info on error messages, check: '
                    'https://cloud.google.com/apis/design/errors'.format(
                    response.error.message))
            print(logoList)

            # Performs label detection on the image file
            response = client.label_detection(image=image)
            labels = response.label_annotations
            print('Label for:', filename)
            labelList = []
            for label in labels:
                plainLable = label.description.replace('\n', ' ')
                #print("\n",label.description)
                labelList.append(plainLable)
            print(labelList)
            # write into corresponding folder
            with open(document_foler + "/" + filename + '.txt', 'w') as f:
                f.write("================Text===============\n")
                for element in textList:
                    f.write(element + "\n")
                f.write("================logo===============\n")
                for element in logoList:
                    f.write(element + "\n")
                f.write("================label===============\n")
                for element in labelList:
                    f.write(element + "\n")
            print("============Next Image============================")
        
           

if __name__ == '__main__':
    main()