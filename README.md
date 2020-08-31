# Jpeg Locator
validates if a file is a jpeg, and if gps information exists, returns the zip-code the picture was taken in

# Installation
install python 3.8.5

Then run the following commands:
```bash
pip install PyQt5
pip install requests
```

you're good to go!

# Usage Modes
running:
```bash
python main.py
```

Will start a very simple GUI. Drag and drop multiple files at a time into the UI to learn their zip codes!

running:
```bash
python main.py <filename>
```
Will run in commandline mode and output the zipcode of the given file

running:
```bash
python tests.py
```

Will run unit tests