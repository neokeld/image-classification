# image-classification

Different categories of image classification based on their exif metadata in Python

| Algorithm                | Description                                                  |
| ------------------------ | ------------------------------------------------------------ |
| sort-image-by-day        | 2016-08-13 algorithm to sort image by day in Python 2        |
| sort-image-by-timedelta  | 2019-05-16 algorithm to sort image by timedelta in Python 3  |

## Install

```sh
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

## Run sort-image-by-day

```sh
python sort-image-by-day/sortImagesByDay.py tests/images/
```

## Run sort-image-by-timedelta

```sh
python sort-image-by-timedelta/sortImagesByTimedelta.py tests/images/
```
