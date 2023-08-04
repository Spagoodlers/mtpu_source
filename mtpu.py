import tkinter as tk
from PIL import Image, ImageTk
import os
import sys
import subprocess
from tkinter import messagebox
from tkinter import ttk
import importlib

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
        if file_name.endswith(".py") and file_name != "__init__.py":
            script_name = os.path.splitext(file_name)[0]
            button = tk.Button(app, text=script_name.capitalize(), bg="black", fg="white",
                               command=lambda script=script_name: load_and_execute_script(script))
            button.pack()

    # Output Label
    global output_label
    output_label = tk.Label(app, text="", bg="black", fg="white")  # Set text color to white
    output_label.pack()

    app.mainloop()


# Main
if __name__ == "__main__":
    create_and_configure_app()