import sys

import sort_image_by.day
import sort_image_by.timedelta


def show_help():
    print('image_classification_by:')
    print('    sort image by an algorithm chosen by the user')
    print('args:')
    print('    1. Sort Algorithm: the algorithm used to classify images')
    print('        Options: day, timedelta')
    print('    2. Path: Directory where images are')


if __name__ == "__main__":
    if len(sys.argv) < 3:
        show_help()
        sys.exit()
    sort_algorithm = sys.argv[1]
    if sort_algorithm == '':
        show_help()
        sys.exit()
    path = sys.argv[2]
    if path == '':
        show_help()
        sys.exit()
    print(f"sort algorithm: {sort_algorithm}")
    print(f"source path: {path}")
    if sort_algorithm == 'day':
        print('day : sort images based on exif date')
        sort_image_by.day.classify_photos(path)
    if sort_algorithm == 'timedelta':
        print('timedelta : sort images based on exif date')
        print('and gather images in a directory based on 1 hour period')
        sorted_photos = sort_image_by.timedelta.sort_photos_by_date(path)
        sort_image_by.timedelta.classify_photos(path, sorted_photos)
