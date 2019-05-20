#!/bin/python

# Arnaud Duforat 2016/08/13
# sorts image based on exif date
# update 2019/05/16: python 3 + gather images based on a timedelta

from PIL import Image
from PIL.ExifTags import TAGS
import sys, os, glob
from datetime import datetime, timedelta

TEST_MODE=False

# Get formated date from unformatted datetime
def format_dateTime(UNFORMATTED):
    DATE, TIME = UNFORMATTED.split()
    return [DATE.replace(':','-'), TIME]

# Get hour
def format_time(TIME):
    return TIME.split(':')[0] + 'H'

# Get Date + Hour
def format_date(DATE_TIME):
    DATE, TIME = format_dateTime(DATE_TIME)
    return DATE + '_' + format_time(TIME)

# Get destination path
def destination_path(BASE_PATH, FORMATED_DATE, FORMATED_TIME):
    return BASE_PATH + '/' + FORMATED_DATE + '-' + FORMATED_TIME

# Move image
def move_image(DESTINATION_PATH, PHOTO):
    destinationFile = DESTINATION_PATH + '/' + os.path.basename(PHOTO)
    if TEST_MODE:
        print("Destination file: " + destinationFile)
    else:
        os.rename(PHOTO, destinationFile)

# Get image informations
def get_exif(fn):
#see <a href="http://www.blog.pythonlibrary.org/2010/03/28/getting-photo-metadata-exif-using-python/">http://www.blog.pythonlibrary.org/2010/03/28/getting-photo-metadata-exif-using-python/</a>
    ret = {}
    i = Image.open(fn)
    info = i._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
    return ret

def sort_photos_by_date(path):
    PHOTOS = []
    EXTENSIONS = ['.jpg','.jpeg', '.png']
    print('managed extensions: ' + ', '.join(EXTENSIONS))
    for EXTENSION in EXTENSIONS:
        PHOTO = glob.glob(path + '/*' + EXTENSION)
        PHOTOS.extend(PHOTO)
    return sorted(PHOTOS, key= lambda photo: get_exif(photo)['DateTime'])
 
def classify_photos(BASEPATH, SORTED_PHOTOS):
    TIME_SEGMENT_IN_HOUR = timedelta(hours=1)
    LAST_SEGMENT_BEGIN = None
    for PHOTO in SORTED_PHOTOS:
        DATETIME_STR = get_exif(PHOTO)['DateTime']
        if TEST_MODE:
            print("Photo date: " + DATETIME_STR)
        datetime_object = datetime.strptime(DATETIME_STR, "%Y:%m:%d %H:%M:%S")
        DATE, TIME = format_dateTime(DATETIME_STR)
        if LAST_SEGMENT_BEGIN != None and (datetime_object - LAST_SEGMENT_BEGIN) < TIME_SEGMENT_IN_HOUR:
            move_image(BASEPATH + format_date(LAST_SEGMENT_BEGIN.strftime("%Y:%m:%d %H:%M:%S")), PHOTO)
        else:
            LAST_SEGMENT_BEGIN = datetime_object
            destinationPath = BASEPATH + format_date(LAST_SEGMENT_BEGIN.strftime("%Y:%m:%d %H:%M:%S"))
            if not os.path.exists(destinationPath):
                print("New dir: " + destinationPath)
                if not TEST_MODE:
                    os.mkdir(destinationPath)
            move_image(destinationPath, PHOTO)


if __name__=="__main__":
    print('sortImages : sort images based on exif date')
    print('gather images in a directory based on period')
    PATH = sys.argv[1]
    if PATH == '': PATH = os.getcwd()
    print('source path: ' + PATH)
    SORTED_PHOTOS = sort_photos_by_date(PATH)
    classify_photos(PATH, SORTED_PHOTOS)
