#!/bin/python

# Arnaud Duforat 2016/08/13
# sorts image based on exif date
# update 2019/05/16: python 3 + gather images based on a timedelta

import sys, os, glob
from datetime import datetime, timedelta
from typing import List

from readers.exif import get_exif

METADATA_DATE_PATTERN = "%Y:%m:%d %H:%M:%S"
TEST_MODE = False


# Get formated date from unformatted datetime
def format_dateTime(UNFORMATTED: str):
    date, time = UNFORMATTED.split()
    return [date.replace(':', '-'), time]


# Get hour
def format_time(time: str):
    return time.split(':')[0] + 'H'


# Get Date + Hour
def format_date(date_time: datetime):
    date, time = format_dateTime(date_time.strftime(METADATA_DATE_PATTERN))
    return date + '_' + format_time(time)


# Get destination path
def destination_path(base_path: str, formated_date: str, formated_time: str):
    return os.path.join(base_path, formated_date + '-' + formated_time)


# Move image
def move_image(destination_path: str, photo: str):
    destinationFile = os.path.join(destination_path, os.path.basename(photo))
    if TEST_MODE:
        print("Destination file: " + destinationFile)
    else:
        os.rename(photo, destinationFile)


def datetime_metadata(exif) -> str:
    return exif.get('DateTime') \
        or exif.get('DateTimeOriginal') \
        or exif.get('DateTimeDigitized') \
        or exif.get('CreateDate')


def sort_photos_by_date(path: str) -> List[str]:
    photos = []
    EXTENSIONS = ['.jpg', '.jpeg']
    print('managed extensions: ' + ', '.join(EXTENSIONS))
    for extension in EXTENSIONS:
        photo = glob.glob(path + '/*' + extension)
        photos.extend(photo)
    return sorted(photos, key=lambda photo: datetime_metadata(get_exif(photo)))


def in_time_segment(current: datetime, last_segment_beginning: datetime) -> bool:
    TIME_SEGMENT_IN_HOUR = timedelta(hours=1)
    return (current - last_segment_beginning) < TIME_SEGMENT_IN_HOUR


def classify_photos(basepath: str, sorted_photos: List[str]):
    last_segment_beginning = None
    for photo in sorted_photos:
        exif = get_exif(photo)
        datetime_str = datetime_metadata(exif)
        if TEST_MODE:
            print("Photo date: " + datetime_str)
        current = datetime.strptime(datetime_str, METADATA_DATE_PATTERN)
        if last_segment_beginning is not None \
                and in_time_segment(current, last_segment_beginning):
            to_path = basepath + format_date(last_segment_beginning)
            move_image(to_path, photo)
        else:
            last_segment_beginning = current
            destinationPath = basepath + format_date(last_segment_beginning)
            if not os.path.exists(destinationPath):
                print("New dir: " + destinationPath)
                if not TEST_MODE:
                    os.mkdir(destinationPath)
            move_image(destinationPath, photo)


if __name__ == "__main__":
    print('sortImages : sort images based on exif date')
    print('gather images in a directory based on period')
    path = sys.argv[1]
    if path == '':
        path = os.getcwd()
    print('source path: ' + path)
    sorted_photos = sort_photos_by_date(path)
    classify_photos(path, sorted_photos)
