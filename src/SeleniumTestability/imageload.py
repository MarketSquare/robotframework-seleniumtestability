import urllib.request
from PIL import Image


#It'll download the image and save as file01.jpg in directory
def download_image(url):
    resource = urllib.urlopen(str(url))
    output = open("file01.jpg","wb")      #save the image file in directory
    output.write(resource.read())
    output.close()


def load_image(path):  #there path will be file01.jpg
    #img  = Image.open(path)      
# On successful execution of this statement, 
# an object of Image type is returned and stored in img variable) 
   
    try:  
        img  = Image.open(path)  
    except IOError: 
        pass
# Use the above statement within try block, as it can  
# raise an IOError if file cannot be found,  
# or image cannot be opened.

