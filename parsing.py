from config import *

class ParsingError(Exception):    
    def __init__(self, message, data=None):
        self.message = message
        if data is None:
            data = {}
        self.data = data


def parse_JPG_start(file):
    """takes a file pointer at the start of file and checks for JPEG signature"""
    
    buff = file.read(2)
    if not buff:
        raise ParsingError(EMPTY)
    
    if buff != JPG_START:
        raise ParsingError(NOT_JPG)


def parse_exif_start(file):
    """reads from current file pointer until it finds the 10 byte exif signature: 
    2 bytes 0xFFE1, followed by 4 bytes, then ascii 'EXIF' """

    buff = file.read(10)
    if buff[0:2] == EXIF_START and buff[4:10] == EXIF_ASCII:
        return
    
    next = file.read(1)
    while next:
        buff = buff[1:] + next
        if buff[0:2] == EXIF_START and buff[4:10] == EXIF_ASCII:
            return

        next = file.read(1)

    raise ParsingError(NO_EXIF)


def parse_TIFF(file):
    """reads TIFF header from current file pointer, sets the byte ordering, and returns the offset to IDF0"""
    
    global byte_order
    byte_order = BYTE_ALIGNMENT[file.read(2)]
    file.seek(2, SEEK_CUR)
    offset = int.from_bytes(file.read(4), byte_order, signed=False)

    return offset


def extract_tag_payload(file, fp_TIFF, data_type, num_components, value):
    """given an entry in an IDF, returns the payload of the entry."""

    signed = True if data_type > 5 else False
    num_bytes = IDF_type_to_bytes[data_type]

    # exif tries to fit the payload in the last 4 bytes
    if num_bytes * num_components <= 4:
        # if payload is ascii, we must decode the string
        if data_type == 2:
            return value.decode("ascii").rstrip('\x00')
        else:
            return int.from_bytes(value, byte_order, signed=signed)

    # if more than 4 bytes are required, then the last 4 bytes of the entry represent an offset to the payload
    else:
        file.seek(fp_TIFF + int.from_bytes(value, byte_order, signed=False))
    
    # if the payload type is a rational, then the value is <first long>/<second long>
    if data_type == 5 or data_type == 8:
        return [int.from_bytes(file.read(4), byte_order, signed=signed) \
                /int.from_bytes(file.read(4), byte_order, signed=signed) \
                for x in range(num_components)]
    
    return [int.from_bytes(file.read(num_bytes), byte_order, signed=signed) for x in range(num_components)]


def parse_tag(file, fp_TIFF, IFD_offset, tag):
    """given an offset to an IFD and a tag, searches for the tag in the IDF and returns the payload if found"""

    #every IFD starts with 2 bytes representing the number of entries it contains
    file.seek(fp_TIFF + IFD_offset)
    entries = int.from_bytes(file.read(2), byte_order, signed=False)

    #every entry follows the format: 2 bytes: tag, 2 bytes: data type, 4 bytes: number of components, 4 bytes: payload or offset
    while entries:
        curr_tag = int.from_bytes(file.read(2), byte_order, signed=False)
        
        if tag == curr_tag:
            data_type =  int.from_bytes(file.read(2), byte_order, signed=False)
            num_components =  int.from_bytes(file.read(4), byte_order, signed=False)
            value = file.read(4)
            return extract_tag_payload(file, fp_TIFF, data_type, num_components, value)
        
        else:
            file.seek(10, SEEK_CUR)

        entries -= 1
        
    raise ParsingError(f"Tag: {tag} not found in IDF", {})


def parse_GPS_IFD(file, fp_TIFF, offset_GPS_IFD):
    """extracts GPS information from the GPS IFD"""

    #Search for, and extract GPS information here
    lat_ref = parse_tag(file, fp_TIFF, offset_GPS_IFD, IDF_tags["GPSLatitudeRef"])
    lat     = parse_tag(file, fp_TIFF, offset_GPS_IFD, IDF_tags["GPSLatitude"])
    lon_ref = parse_tag(file, fp_TIFF, offset_GPS_IFD, IDF_tags["GPSLongitudeRef"])
    lon     = parse_tag(file,fp_TIFF, offset_GPS_IFD, IDF_tags["GPSLongitude"])

    #Put results into a dictionary, record if something is missing
    errors = []
    GPS_Info = {}
    GPS_Info["GPSLatitudeRef"]  = lat_ref if lat_ref else errors.append("latitude Reference")
    GPS_Info["GPSLatitude"]     = lat     if lat     else errors.append("latitude")
    GPS_Info["GPSLongitudeRef"] = lon_ref if lon_ref else errors.append("latitude Reference")
    GPS_Info["GPSLongitude"]    = lon     if lon     else errors.append("longitude")

    if errors:
        raise ParsingError("Missing: " + (", ".join(errors), GPS_Info))

    return GPS_Info


def parse_JPG(file):
    """validates the given file is a JPG, and extracts available metadata information"""

    JPG_Info = {}
    with open(file, 'rb') as f:
        parse_JPG_start(f)
        parse_exif_start(f)

        fp_TIFF = f.tell()
        offset_IFD0 = parse_TIFF(f)

        try:
            JPG_Info["GPSInfo"] = parse_tag(f, fp_TIFF, offset_IFD0, IDF_tags["GPSInfo"])
        except ParsingError as e:
            raise ParsingError(NO_GPS, JPG_Info.update(e.data))

        try:
            JPG_Info.update(parse_GPS_IFD(f, fp_TIFF, JPG_Info["GPSInfo"]))
        except ParsingError as e:
            raise ParsingError(e.message, JPG_Info.update(e.data))

    return JPG_Info