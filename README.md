# image-classification

Different categories of image classification based on their exif metadata in Python

| Algorithm                | Description                                                  |
| ------------------------ | ------------------------------------------------------------ |
| sort_image_by/day        | 2016-08-13 algorithm to sort image by day in Python 2        |
| sort_image_by/timedelta  | 2019-05-16 algorithm to sort image by timedelta in Python 3  |

## Install

```sh
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

## Run image_classification_by

### Day

```sh
python image_classification_by.py day tests/images/
```

### Timedelta

```sh
python image_classification_by.py timedelta tests/images/
```
