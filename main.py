from PyQt5.QtWidgets import QApplication
import parsing, GUI, util
import sys

def get_zip(file):
    """takes a filename, returns its postal code as a string if it is a JPG with EXIF GPS data.
    If unable to return the postal code, get_zip returns an error message"""
    
    try:
        JPG_Info = parsing.parse_JPG(file)
    
    except parsing.ParsingError as e:
        return e.message

    coords = util.get_coordinates(JPG_Info)
    zipcode = util.reverse_geocode(coords)
    return zipcode

def main(argv):
    # GUI mode
    if len(argv) <= 1:
        app = QApplication(argv)
        ui = GUI.MainWindow()
        ui.show()
        sys.exit(app.exec_())
        
    # command line mode for a single file
    print(get_zip(argv[1]))

if __name__ == "__main__":
    main(sys.argv)