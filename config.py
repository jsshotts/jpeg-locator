"""global variables"""
byte_order = ""

"""constants"""
SEEK_CUR = 1

JPG_START = b'\xff\xd8'
EXIF_START = b'\xff\xe1'
EXIF_ASCII = b'\x45\x78\x69\x66\x00\x00'

BYTE_ALIGNMENT = {
    b'\x49\x49' : "little", # intel
    b'\x4d\x4d' : "big" # motorola
}

IDF_type_to_bytes = {
    1 : 1, # unsigned byte
    2 : 1, # ascii string
    3 : 2, # unsigned short
    4 : 4, # unsigned long
    5 : 8, # unsigned rational
    6 : 1, # signed byte
    7 : 1, # undefined
    8 : 2, # signed short
    9 : 4, # signed long
    10 : 8, # signed rational
    11 : 4, # single float
    12 : 8 # double float
}

IDF_tags = {
    "GPSInfo" : 34853,
    "GPSLatitudeRef" : 1,
    "GPSLatitude" : 2,
    "GPSLongitudeRef" : 3,
    "GPSLongitude" : 4
}

# errors
EMPTY = "empty file"
NOT_JPG = "not a JPG"
NO_EXIF = "no EXIF data"
NO_GPS = "No GPS data found"

# reverse geocoding api
BASE_URL = "https://us1.locationiq.com/v1/reverse.php"
API_KEY = "a0a829ac1f49b9"
RESPONSE_FORMAT = "json"

# UI
UI_LABEL = "Drag and drop your images above!"
FONT = "Courier" # must be monospaced and crossplatform
FONT_SIZE = 10
WINDOW_TITLE = "Images to Postal Codes"