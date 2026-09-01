import tkinter as tk
from PIL import Image, ImageTk
import os
import subprocess
from tkinter import messagebox
from tkinter import ttk
from tools import image_printer
import requests

TEMP_FOLDER = "image/temp"
TEMP_FILE_NAME = "last_rolled.png"

PRINT_ENABLED = True  # Initial state of the checkbox, printing is enabled by default


def get_random_sorcerery_image_by_cmc(cmc):
    exclude_sets = ["unh", "ugl", "ust"]
    exclude_query = " ".join([f"-set:{set_code}" for set_code in exclude_sets])

    url = f"https://api.scryfall.com/cards/random?q=type:sorcery+cmc:{cmc}+{exclude_query}"
    headers = {'User-Agent': 'MTPU/1.0 (Magic Thermal Printing Utility)'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data.get("image_uris", {}).get("png")

    return None


def download_image(image_url):
    headers = {'User-Agent': 'MTPU/1.0 (Magic Thermal Printing Utility)'}
    response = requests.get(image_url, headers=headers)
    if response.status_code == 200:
        os.makedirs(TEMP_FOLDER, exist_ok=True)
        with open(os.path.join(TEMP_FOLDER, TEMP_FILE_NAME), "wb") as f:
            f.write(response.content)
        return os.path.abspath(os.path.join(TEMP_FOLDER, TEMP_FILE_NAME))
    return None


def delete_temp_image():
    temp_image_path = os.path.abspath(
        os.path.join(TEMP_FOLDER, TEMP_FILE_NAME))
    if os.path.exists(temp_image_path):
        os.remove(temp_image_path)


def show_image_in_app(image_path):
    try:
        image = Image.open(image_path)
        image = image.resize((200, 280))  # Resize the image to fit in the app
        photo = ImageTk.PhotoImage(image)
        image_label_.config(image=photo)
        image_label_.image = photo  # To prevent garbage collection of the image
        image_label_.pack()
    except FileNotFoundError:
        # If the image file is not found, display the default image
        default_image_path = "image/icon/back.png"
        image = Image.open(default_image_path)
        image = image.resize((200, 280))  # Resize the image to fit in the app
        photo = ImageTk.PhotoImage(image)
        image_label_.config(image=photo)
        image_label_.image = photo  # To prevent garbage collection of the image
        image_label_.pack()


def run_image_printer(image_array):
    try:
        if PRINT_ENABLED:
            image_printer.print_array_of_cards(image_array)
    except Exception as e:
        print(f"Error while running image_printer.py: {e}")


def on_cmc_button_click_(cmc):
    roll_random_cmc(cmc)


def roll_random_cmc(cmc):
    try:
        cmc = int(cmc)
        if cmc < 0 or cmc > 20:
            messagebox.showerror(
                "Invalid CMC", "Please enter a number between 0 and 20.")
            return

        image_url = get_random_sorcerery_image_by_cmc(cmc)

        if image_url:
            output_label_.config(text=f"Random CMC: {cmc}")

            # Download the image and save it to the temporary folder
            image_path = download_image(image_url)
            if image_path:
                show_image_in_app(image_path)

                # Print the image if printing is enabled
                # Call the image_printer.py script
                run_image_printer([image_path])
                delete_temp_image()

            else:
                print("Failed to download the image.")

        else:
            output_label_.config(text="No creature found for the given CMC.")
            show_image_in_app('image/icon/back.png')
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number.")


def create_transparent_button_(parent, text, command):
    button = tk.Button(parent, text=text, bg="black", fg="white", activebackground="black",
                       activeforeground="white", bd=0, highlightthickness=0, relief="flat", command=command)
    return button


def on_checkbox_click_():
    global PRINT_ENABLED
    PRINT_ENABLED = checkbox_var_.get()


def create_and_configure_gui():
    app = tk.Toplevel()  # Create a new top-level window
    app.title("Sorcerer")
    app.geometry("275x570")  # Set window size with space for the checkbox

    # Set the background color to black
    app.configure(bg="black")

    # Create a Label widget to display the image inside the app
    global image_label_
    image_label_ = tk.Label(app, bg="black")
    image_label_.pack()

    # Show the default image at the start of the application
    default_image_path = "image/icon/back.png"
    show_image_in_app(default_image_path)

    # CMC Buttons (0-20)
    cmc_buttons_frame = tk.Frame(app, bg="black")
    cmc_buttons_frame.pack()

    # Load and display the icons for the buttons in a 5x5 grid layout
    grid_row = 0
    grid_column = 0
    for cmc_value in range(13):  # 0 to 16 (to fit the 5x5 grid)
        icon_path = f"image/icon/{cmc_value}.png"
        if os.path.exists(icon_path):
            icon_image = Image.open(icon_path)
            icon_image = ImageTk.PhotoImage(icon_image)

            # Use a lambda function to pass the current cmc_value as an argument to on_cmc_button_click_
            cmc_button = create_transparent_button_(cmc_buttons_frame, text=str(
                ''), command=lambda cmc=cmc_value: on_cmc_button_click_(cmc))
            cmc_button.config(image=icon_image, compound=tk.CENTER)
            cmc_button.image = icon_image  # To prevent garbage collection of the image
            cmc_button.grid(row=grid_row, column=grid_column)

            grid_column += 1
            if grid_column > 4:  # 5 buttons per row
                grid_column = 0
                grid_row += 1
        else:
            print(f"Icon not found for CMC {cmc_value}")

    # Output Label
    global output_label_
    output_label_ = tk.Label(app, text="", bg="black",
                             fg="white")  # Set text color to white
    output_label_.pack()

    # Checkbox to control the printer
    global checkbox_var_
    checkbox_var_ = tk.BooleanVar()
    checkbox_var_.set(PRINT_ENABLED)  # Set initial state
    checkbox = ttk.Checkbutton(
        app, text="Enable Printing", variable=checkbox_var_, command=on_checkbox_click_)
    checkbox.pack()

    app.mainloop()


# Main
if __name__ == "__main__":
    create_and_configure_gui()
