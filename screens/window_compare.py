import PySimpleGUI as sg
import os.path
import PIL.Image
import io
import base64

def start(image1, image2, count=None):
    layout_select = [
        [
            sg.Text("Select preffered image (use buttons bellow or use keyboard Left and Right)", justification="center", size=(100, 1))
        ],
        [
            sg.Image(key="-IMG1-", size=(50, 50)),
            sg.Image(key="-IMG2-", size=(50, 50)),
        ],
        [
            sg.Button("<", size=(50,1)),
            sg.Button(">", size=(50,1))
        ]
    ]

    if count != None:
        percent = count[0]/count[1]*100
        layout_select.insert(0, [sg.Text(f"Image {count[0]} of {count[1]} ({percent:.2f}%).", justification="center", size=(100, 1))])

    # Create the window
    window = sg.Window("Select folder", layout_select, return_keyboard_events=True, finalize=True)

    # Start variables
    startup = True

    # Create an event loop for PYSimpleGUI
    while True:
        # Init images
        if startup:
            window['-IMG1-'].update(data=convert_to_bytes(image1, resize=[400,400], new=True))
            window['-IMG2-'].update(data=convert_to_bytes(image2, resize=[400,400], new=True))
            startup = False

        # Event reading
        event, values = window.read()

        print(event)

        if event == "<" or event == "Left:37":
            window.close()
            return image1
        if event == ">" or event == "Right:39":
            window.close()
            return image2

        # Close if exit
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

    window.close()

def convert_to_bytes(file_or_bytes, resize=None, new=False):
    '''
    Will convert into bytes and optionally resize an image that is a file or a base64 bytes object.
    Turns into  PNG format in the process so that can be displayed by tkinter
    :param file_or_bytes: either a string filename or a bytes base64 image object
    :type file_or_bytes:  (Union[str, bytes])
    :param resize:  optional new size
    :type resize: (Tuple[int, int] or None)
    :return: (bytes) a byte-string object
    :rtype: (bytes)
    '''
    if isinstance(file_or_bytes, str):
        img = PIL.Image.open(file_or_bytes)
    else:
        try:
            img = PIL.Image.open(io.BytesIO(base64.b64decode(file_or_bytes)))
        except Exception as e:
            dataBytesIO = io.BytesIO(file_or_bytes)
            img = PIL.Image.open(dataBytesIO)

    cur_width, cur_height = img.size
    if resize:
        new_width, new_height = resize
        scale = min(new_height/cur_height, new_width/cur_width)
        img = img.resize((int(cur_width*scale), int(cur_height*scale)), PIL.Image.ANTIALIAS)
    if new:
        base = PIL.Image.new('RGBA', resize)
        position = (int((base.width - img.width)/2), int((base.height - img.height)/2))
        base.paste(img, position)
        img = base.copy()
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    del img
    return bio.getvalue()

if __name__ == '__main__':
    # Manual test script
    out = start('../test_assets/test1.png', '../test_assets/test2.png')
    print(out)