import os
import win32print
import win32ui
from PIL import Image, ImageWin

PHYSICALWIDTH = 110
PHYSICALHEIGHT = 111


def print_array_of_cards(image_paths):
    # Get the current working directory
    current_directory = os.getcwd()

    try:
        # Note: The printing options available in the image viewer application may vary depending on the OS and associated default application for images.
        printer_name = win32print.GetDefaultPrinter()
        print("The printer is called:", printer_name)

        # Create a printer device context
        hDC = win32ui.CreateDC()
        hDC.CreatePrinterDC(printer_name)
        printer_size = hDC.GetDeviceCaps(
            PHYSICALWIDTH), hDC.GetDeviceCaps(PHYSICALHEIGHT)

        # Loop through each image path in the array
        for file_name in image_paths:
            # Use os.path.join to construct the complete path to the image
            full_image_path = os.path.join(current_directory, file_name)

            bmp = Image.open(full_image_path)
            if bmp.size[0] < bmp.size[1]:
                bmp = bmp.rotate(0)

            hDC.StartDoc(file_name)
            hDC.StartPage()

            dib = ImageWin.Dib(bmp)
            dib.draw(hDC.GetHandleOutput(),
                     (0, 0, printer_size[0], printer_size[1]))

            hDC.EndPage()
            hDC.EndDoc()

    except Exception as e:
        print("Error printing the cards:", e)

    finally:
        hDC.DeleteDC()