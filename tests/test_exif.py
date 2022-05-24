import os

from readers.exif import get_exif


def test_should_get_exif_have_date_time_original():
    path = os.path.join('tests', 'images', '1.jpg')
    exif = get_exif(path)
    assert exif['DateTimeOriginal'] == '2022:05:21 16:41:41'
