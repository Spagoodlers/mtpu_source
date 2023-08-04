import tkinter as tk
from PIL import Image, ImageTk
import os
import requests

TEMP_FOLDER = "image/temp"
TEMP_FILE_NAME = "last_rolled.png"

PRINT_ENABLED = True  # Initial state of the checkbox, printing is enabled by default


def get_random_card_image_by_cmc(cmc, card_type):
    exclude_sets = ["unh", "ugl", "ust"]
    exclude_query = " ".join([f"-set:{set_code}" for set_code in exclude_sets])

    url = f"https://api.scryfall.com/cards/random?q=type:{card_type}+cmc:{cmc}+{exclude_query}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data.get("image_uris", {}).get("png")

    return None


def download_image(image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        os.makedirs(TEMP_FOLDER, exist_ok=True)
        with open(os.path.join(TEMP_FOLDER, TEMP_FILE_NAME), "wb") as f:
            f.write(response.content)
        return os.path.abspath(os.path.join(TEMP_FOLDER, TEMP_FILE_NAME))
    return None


def delete_temp_image():
    temp_image_path = os.path.abspath(os.path.join(TEMP_FOLDER, TEMP_FILE_NAME))
    if os.path.exists(temp_image_path):
        os.remove(temp_image_path)


def show_image_in_app(image_path, image_label):
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


def print_array_of_cards(image_array):
    try:
        if PRINT_ENABLED:
            # Add the actual printing logic here
            print("Printing images...")
            print(image_array)
    except Exception as e:
        print(f"Error while printing images: {e}")


def create_transparent_button(parent, text, command):
    button = tk.Button(parent, text=text, bg="black", fg="white", activebackground="black",
                       activeforeground="white", bd=0, highlightthickness=0, relief="flat", command=command)
    return button


def on_checkbox_click(checkbox_var):
    global PRINT_ENABLED
    PRINT_ENABLED = checkbox_var.get()
