import tkinter as tk
from PIL import Image, ImageTk
from tools import image_printer
import requests
import os

TOKENS_FILE = "utilities/tokens.txt"


def run_image_printer(image_array):
    try:
        image_printer.print_array_of_cards(image_array)
    except Exception as e:
        print(f"Error while running image_printer.py: {e}")


def display_tokens_and_image(image_array):
    # Create a Tkinter window
    root = tk.Tk()
    root.title("Token List")

    # Function to handle the listbox selection event
    def on_token_selected(event):
        selected_index = listbox.curselection()
        if selected_index:
            selected_token = image_array[selected_index[0]]
            show_image_in_app(selected_token["image_path"])

    # Create a listbox to display the tokens
    listbox = tk.Listbox(root)
    listbox.pack()

    # Add each token from image_array to the listbox
    for token in image_array:
        listbox.insert(tk.END, token["name"])

    # Bind the listbox selection event to the function
    listbox.bind("<<ListboxSelect>>", on_token_selected)

    # Create a Label widget to display the image inside the app
    global image_label_
    image_label_ = tk.Label(root)
    image_label_.pack()

    # Show the default image at the start of the application
    default_image_path = "image/icon/back.png"
    show_image_in_app(default_image_path)

    # Start the Tkinter main loop
    root.mainloop()


def show_image_in_app(image_path):
    image = Image.open(image_path)
    image = image.resize((200, 280))  # Resize the image to fit in the app
    photo = ImageTk.PhotoImage(image)
    image_label_.config(image=photo)
    image_label_.image = photo  # To prevent garbage collection of the image


def create_and_configure_gui():
    # Fetch tokens from Scryfall API and save them to file if needed
    tokens = ["howdy"]

    if tokens:
        display_tokens_and_image(tokens)
    else:
        print("Failed to load tokens. Please check your internet connection.")
