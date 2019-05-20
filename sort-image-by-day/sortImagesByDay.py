#!/bin/python

# Arnaud Duforat 2016/08/13
# sorts image based on exif date

from PIL import Image
from PIL.ExifTags import TAGS
import sys, os, glob

# Get formated date from unformatted datetime
def format_dateTime(UNFORMATTED):
    DATE, TIME = UNFORMATTED.split()
    return [DATE.replace(':',''), TIME]

# Get hour
def format_time(TIME):
    return TIME.split(':')[0]

#
def get_exif(fn):
#see <a href="http://www.blog.pythonlibrary.org/2010/03/28/getting-photo-metadata-exif-using-python/">http://www.blog.pythonlibrary.org/2010/03/28/getting-photo-metadata-exif-using-python/</a>
    ret = {}
    i = Image.open(fn)
    info = i._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
    print ret['DateTime']
    return ret
 
def sortPhotos(path):
    PHOTOS = []
    EXTENSIONS = ['.jpg','.jpeg', '.png']
    print 'managed extensions: ' + ', '.join(EXTENSIONS)
    for EXTENSION in EXTENSIONS:
        PHOTO = glob.glob(path + '/*' + EXTENSION)
        PHOTOS.extend(PHOTO)
 
    for PHOTO in PHOTOS:
        DATE, TIME = format_dateTime(get_exif(PHOTO)['DateTime'])
	destinationPath = path + '/' + DATE + '-' + format_time(TIME)
        if not os.path.exists(destinationPath):
            os.mkdir(destinationPath)
	destinationFile = destinationPath + '/' + os.path.basename(PHOTO)
	print destinationFile
        os.rename(PHOTO, destinationFile)
 
if __name__=="__main__":
    print 'sortImages : sort images based on exif date'
    PATH = sys.argv[1]
    if PATH == '': PATH = os.getcwd()
    print PATH
    sortPhotos(PATH)
