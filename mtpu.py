import tkinter as tk
from PIL import Image, ImageTk
import os
import sys
import subprocess
from tkinter import messagebox
from tkinter import ttk
import importlib
import win32print

# Get the parent directory of the current script (app_gui.py)
current_script_dir = os.path.dirname(os.path.abspath(__file__))

# Append the parent directory to the Python path
parent_dir = os.path.join(current_script_dir, '..')
sys.path.append(parent_dir)

# Now you can import from 'tools'
from tools import image_printer

image_label = None  # Global variable to store the image label
root = None  # Global variable to store the main application window

# Global variable to store the reference to the frame where the sub GUI will be loaded
subgui_frame = None

TEMP_FOLDER = "image/temp"
TEMP_FILE_NAME = "last_rolled.png"
PRINT_ENABLED = True  # Initial state of the checkbox, printing is enabled by default


def show_image_in_app(image_path):
    try:
        image = Image.open(image_path)
        image = image.resize((200, 280))  # Resize the image to fit in the app
        photo = ImageTk.PhotoImage(image)
        image_label.config(image=photo)
        image_label.image = photo  # To prevent garbage collection of the image
        image_label.pack()
    except FileNotFoundError:
        # If the image file is not found, display the default image
        default_image_path = "image/icon/back.png"
        image = Image.open(default_image_path)
        image = image.resize((200, 280))  # Resize the image to fit in the app
        photo = ImageTk.PhotoImage(image)
        image_label.config(image=photo)
        image_label.image = photo  # To prevent garbage collection of the image
        image_label.pack()


def remove_current_subgui():
    # Destroy all widgets inside the frame
    for widget in subgui_frame.winfo_children():
        widget.destroy()


def load_and_execute_script(script_name):
    try:
        module_name = f"utilities.{script_name}"
        module_spec = importlib.util.spec_from_file_location(module_name, f"utilities/{script_name}.py")
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)

        # Now, the script has been loaded as a module. We assume it contains a function called `create_and_configure_gui`
        if hasattr(module, "create_and_configure_gui"):
            module.create_and_configure_gui()
        else:
            print(f"Error: Function 'create_and_configure_gui()' not found in the script '{script_name}'")
    except Exception as e:
        print(f"Error while running '{script_name}': {e}")


def create_and_configure_app():
    app = tk.Tk()
    app.title("Magic Thermal Printing Utility")
    app.geometry("275x375")  # Set window size with space for the checkbox

    # Create a Frame widget to hold the sub GUIs
    global subgui_frame
    subgui_frame = tk.Frame(app, bg="black")
    subgui_frame.pack()

    # Set the background color to black
    app.configure(bg="black")

    # Create a Label widget to display the image inside the app
    global image_label
    image_label = tk.Label(app, bg="black")
    image_label.pack()

    # Show the default image at the start of the application
    default_image_path = "image/icon/boot.png"
    show_image_in_app(default_image_path)

    # Load and add buttons for scripts in the "utilities" folder
    utilities_folder = "utilities"
    for file_name in os.listdir(utilities_folder):
        if file_name.endswith(".py") and file_name != "__init__.py" and file_name != "printer_config.py":
            script_name = os.path.splitext(file_name)[0]
            button = tk.Button(app, text=script_name.capitalize(), bg="black", fg="white",
                               command=lambda script=script_name: load_and_execute_script(script))
            button.pack()

    # Printer cycle button in corner
    def cycle_printer():
        try:
            printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)
            printer_names = [printer[2] for printer in printers]
            current = win32print.GetDefaultPrinter()
            
            if current in printer_names:
                current_index = printer_names.index(current)
                next_index = (current_index + 1) % len(printer_names)
                next_printer = printer_names[next_index]
                win32print.SetDefaultPrinter(next_printer)
                output_label.config(text=f"Printer: {next_printer}")
            else:
                win32print.SetDefaultPrinter(printer_names[0])
                output_label.config(text=f"Printer: {printer_names[0]}")
        except Exception as e:
            output_label.config(text=f"Error: {e}")

    printer_icon_path = "image/icon/printer.png"
    if os.path.exists(printer_icon_path):
        printer_icon = Image.open(printer_icon_path)
        printer_icon = printer_icon.resize((24, 24))
        printer_icon_photo = ImageTk.PhotoImage(printer_icon)
        printer_button = tk.Button(app, image=printer_icon_photo, bg="black", 
                                  command=cycle_printer, bd=0, highlightthickness=0)
        printer_button.image = printer_icon_photo
    else:
        printer_button = tk.Button(app, text="", bg="black", fg="white", font=("Arial", 16),
                                  command=cycle_printer, bd=0, highlightthickness=0)
    printer_button.place(x=240, y=10)

    # Output Label
    global output_label
    output_label = tk.Label(app, text="", bg="black", fg="white")  # Set text color to white
    output_label.pack()

    app.mainloop()


# Main
if __name__ == "__main__":
    create_and_configure_app()