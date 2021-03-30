from os import walk
from shutil import copyfile
import PySimpleGUI as sg

import screens.window_selector as path_select
import screens.window_compare as image_compare

def list_images(files):
    _, _, filenames = next(walk(files))
    return [x for x in filenames if '.jpg' in x or '.png' in x]

if __name__ == "__main__":
    try:
        # Open folder selection screen
        in1, in2, out, remove_prev_result = path_select.start()

        # Filter image files and do inner-join
        in1_files = list_images(in1)
        in2_files = list_images(in2)
        inner_join = [x for x in in1_files if x in in2_files]

        # Variables
        count = 1
        total = len(inner_join)

        if remove_prev_result:
            out_files = list_images(out)
            inner_join = [x for x in inner_join if x not in out_files]
            count = len(out_files)

        for file in inner_join:
            count = count + 1
            selection = image_compare.start(in1 + '/' + file, in2 + '/' + file, [count, total])
            if selection:
                copyfile(selection, out + '/' + file)
            else:
                break

        sg.popup_ok("No more images!")
    except Exception as e:
        sg.popup_error("Error!", e)