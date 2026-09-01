import tkinter as tk
from PIL import Image, ImageTk
from tools import image_printer
import requests
import os

TEMP_FOLDER = "image/temp"
TEMP_FILE_NAME = "last_rolled.png"
PRINT_ENABLED = True


def get_all_tokens():
    """Fetch all token types from Scryfall API"""
    url = "https://api.scryfall.com/cards/search?q=t:token"
    headers = {'User-Agent': 'MTPU/1.0 (Magic Thermal Printing Utility)'}
    
    tokens = set()
    has_more = True
    
    while has_more:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            for card in data.get("data", []):
                tokens.add(card["name"])
            
            has_more = data.get("has_more", False)
            if has_more:
                url = data.get("next_page")
        else:
            print(f"Error fetching tokens: {response.status_code}")
            break
    
    return sorted(list(tokens))


def get_random_token_image(token_name):
    """Fetch a random image for a specific token name"""
    url = f"https://api.scryfall.com/cards/random?q=t:token+{token_name}"
    headers = {'User-Agent': 'MTPU/1.0 (Magic Thermal Printing Utility)'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        # Handle both single-faced and double-faced cards
        if "image_uris" in data:
            return data.get("image_uris", {}).get("png")
        elif "card_faces" in data:
            return data["card_faces"][0].get("image_uris", {}).get("png")
    
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
    temp_image_path = os.path.abspath(os.path.join(TEMP_FOLDER, TEMP_FILE_NAME))
    if os.path.exists(temp_image_path):
        os.remove(temp_image_path)


def run_image_printer(image_array):
    try:
        if PRINT_ENABLED:
            image_printer.print_array_of_cards(image_array)
    except Exception as e:
        print(f"Error while running image_printer.py: {e}")


def create_and_configure_gui():
    app = tk.Toplevel()
    app.title("Tokens")
    app.geometry("400x600")
    app.configure(bg="black")

    # Create a Frame widget to hold the image display
    global image_label_
    image_label_ = tk.Label(app, bg="black")
    image_label_.pack(pady=10)

    # Show the default image at the start
    default_image_path = "image/icon/back.png"
    try:
        image = Image.open(default_image_path)
        image = image.resize((200, 280))
        photo = ImageTk.PhotoImage(image)
        image_label_.config(image=photo)
        image_label_.image = photo
        image_label_.pack()
    except FileNotFoundError:
        pass

    # Loading label
    loading_label = tk.Label(app, text="Loading tokens...", bg="black", fg="white")
    loading_label.pack(pady=5)

    # Token listbox
    listbox_frame = tk.Frame(app, bg="black")
    listbox_frame.pack(pady=10, fill=tk.BOTH, expand=False, padx=20)

    listbox = tk.Listbox(listbox_frame, bg="gray", fg="white", font=("Arial", 10), height=15)
    listbox.pack(fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(listbox_frame, orient="vertical", command=listbox.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    listbox.config(yscrollcommand=scrollbar.set)

    # Output label
    global output_label_
    output_label_ = tk.Label(app, text="", bg="black", fg="white")
    output_label_.pack(pady=5)

    # Print button (create before listbox to ensure it's at bottom)
    def print_selected_token():
        selection = listbox.curselection()
        if selection:
            selected_token = listbox.get(selection[0])
            image_url = get_random_token_image(selected_token)
            if image_url:
                image_path = download_image(image_url)
                if image_path:
                    run_image_printer([image_path])
                    delete_temp_image()

    print_button = tk.Button(app, text="Print Token", bg="white", fg="black", 
                           command=print_selected_token, font=("Arial", 12), width=15)
    print_button.pack(pady=15)

    # Fetch and populate tokens
    def load_tokens():
        tokens = get_all_tokens()
        loading_label.config(text="")
        
        for token in tokens:
            listbox.insert(tk.END, token)

    # Handle token selection
    def on_token_selected(event):
        selection = listbox.curselection()
        if selection:
            selected_token = listbox.get(selection[0])
            output_label_.config(text=f"Selected: {selected_token}")
            
            # Fetch and display random image for this token
            image_url = get_random_token_image(selected_token)
            if image_url:
                image_path = download_image(image_url)
                if image_path:
                    try:
                        image = Image.open(image_path)
                        image = image.resize((200, 280))
                        photo = ImageTk.PhotoImage(image)
                        image_label_.config(image=photo)
                        image_label_.image = photo
                    except Exception as e:
                        print(f"Error displaying image: {e}")
                    delete_temp_image()

    listbox.bind("<<ListboxSelect>>", on_token_selected)

    # Load tokens after GUI is created
    app.after(100, load_tokens)

    app.mainloop()


if __name__ == "__main__":
    create_and_configure_gui()
