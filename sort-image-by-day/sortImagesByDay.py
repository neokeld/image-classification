#!/bin/python

# Arnaud Duforat 2016/08/13
# sorts image based on exif date

import sys, os, glob

from readers.exif import get_exif


# Get formated date from unformatted datetime
def format_datetime(unformatted: str):
    date, time = unformatted.split()
    return [date.replace(':', ''), time]


# Get hour
def format_time(time: str):
    return time.split(':')[0]


def sortPhotos(path: str):
    photos = []
    EXTENSIONS = ['.jpg', '.jpeg']
    print('managed extensions: ' + ', '.join(EXTENSIONS))
    for extension in EXTENSIONS:
        photo = glob.glob(path + '/*' + extension)
        photos.extend(photo)

    for photo in photos:
        exif = get_exif(photo)
        datetime_str = exif.get('DateTime') or exif.get('DateTimeOriginal') or exif.get('DateTimeDigitized') or exif.get('CreateDate')
        date, time = format_datetime(datetime_str)
        destinationPath = os.path.join(path, date + '-' + format_time(time))
        if not os.path.exists(destinationPath):
            os.mkdir(destinationPath)
        destinationFile = os.path.join(destinationPath, os.path.basename(photo))
        print(destinationFile)
        os.rename(photo, destinationFile)


if __name__ == "__main__":
    print('sortImages : sort images based on exif date')
    path = sys.argv[1]
    if path == '':
        path = os.getcwd()
    print(path)
    sortPhotos(path)
