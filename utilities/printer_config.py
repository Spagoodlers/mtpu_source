import tkinter as tk
from tkinter import ttk
import win32print


def create_and_configure_gui():
    app = tk.Toplevel()
    app.title("Printer Configuration")
    app.geometry("400x300")
    app.configure(bg="black")

    # Label
    label = tk.Label(app, text="Select Default Printer", bg="black", fg="white", font=("Arial", 14))
    label.pack(pady=20)

    # Get available printers
    try:
        printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)
        printer_names = [printer[2] for printer in printers]
        
        # Get current default printer
        default_printer = win32print.GetDefaultPrinter()
    except Exception as e:
        print(f"Error getting printers: {e}")
        printer_names = ["Error loading printers"]
        default_printer = ""

    # Printer listbox
    listbox_frame = tk.Frame(app, bg="black")
    listbox_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=20)

    listbox = tk.Listbox(listbox_frame, bg="gray", fg="white", font=("Arial", 10))
    listbox.pack(fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(listbox_frame, orient="vertical", command=listbox.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    listbox.config(yscrollcommand=scrollbar.set)

    # Populate listbox
    for printer in printer_names:
        listbox.insert(tk.END, printer)
        if printer == default_printer:
            listbox.selection_set(tk.END)
            listbox.see(tk.END)

    # Current printer label
    current_label = tk.Label(app, text=f"Current: {default_printer}", bg="black", fg="gray", font=("Arial", 9))
    current_label.pack(pady=5)

    def set_default_printer():
        selection = listbox.curselection()
        if selection:
            selected_printer = listbox.get(selection[0])
            try:
                win32print.SetDefaultPrinter(selected_printer)
                current_label.config(text=f"Current: {selected_printer}", fg="green")
                print(f"Default printer set to: {selected_printer}")
            except Exception as e:
                current_label.config(text=f"Error: {e}", fg="red")
                print(f"Error setting printer: {e}")

    # Set button
    set_button = tk.Button(app, text="Set as Default", bg="white", fg="black", 
                          command=set_default_printer, font=("Arial", 10))
    set_button.pack(pady=20)

    app.mainloop()


if __name__ == "__main__":
    create_and_configure_gui()
