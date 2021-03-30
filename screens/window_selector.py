import PySimpleGUI as sg

def start():
    layout_select = [
        [
            sg.Text("Image Folder #1:", justification="right", size=(13, 1)),
            sg.In(size=(25, 1), enable_events=True, key="-FOLDER1-", justification="left"),
            sg.FolderBrowse()
        ],
        [
            sg.Text("Image Folder #2:", justification="right", size=(13, 1)),
            sg.In(size=(25, 1), enable_events=True, key="-FOLDER2-", justification="left"),
            sg.FolderBrowse()
        ],
        [
            sg.Text("Output Folder:", justification="right", size=(13, 1)),
            sg.In(size=(25, 1), enable_events=True, key="-FOLDEROUT-", justification="left"),
            sg.FolderBrowse()
        ],
        [
             sg.Checkbox('Do not show if file already in output (continue)', key="-CONTINUE-", default=True)
        ],
        [
            sg.Button("OK", size=(44, 1))
        ]
    ]

    # Create the window
    window = sg.Window("Select folder", layout_select)

    # Start variables
    folder1 = ""
    folder2 = ""
    folder_out = ""
    continue_out = True

    # Create an event loop for PYSimpleGUI
    while True:
        event, values = window.read()

        if event == "-FOLDER1-": folder1 = values["-FOLDER1-"]
        if event == "-FOLDER2-": folder2 = values["-FOLDER2-"]
        if event == "-FOLDEROUT-": folder_out = values["-FOLDEROUT-"]
        continue_out = values["-CONTINUE-"]

        if event == "OK":
            if folder1 != "" and folder2 != "" and folder_out != "":
                window.close()
                return [folder1, folder2, folder_out, continue_out]
            else:
                sg.popup_error("Select image!")

        # Close if exit
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

    window.close()