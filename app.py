import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk


def browse_directory():
    directory_path = filedialog.askdirectory()
    if directory_path:
        label.config(text="Selected Directory: " + directory_path)
        global selected_directory
        selected_directory = directory_path
        update_folder_list_and_count()


def update_folder_list_and_count():
    folder_tree.delete(*folder_tree.get_children())  # Clear the Treeview
    if selected_directory:
        folder_entries = [entry for entry in os.scandir(selected_directory) if entry.is_dir()]
        for folder_entry in folder_entries:
            folder_name = folder_entry.name
            folder_path = folder_entry.path
            folder_tree.insert("", "end", values=(folder_name, folder_path))
        folder_count_label.config(text=f"Number of Folders: {len(folder_entries)}")


def show_about():
    # Hide other items
    label.grid_remove()
    browse_button.grid_remove()
    folder_tree.grid_remove()
    folder_count_label.grid_remove()

    # Show the About section
    about_label.grid(row=0, column=0, padx=20, pady=20)
    about_text.grid(row=1, column=0, padx=20, pady=20)


def show_home():
    # Show other items
    label.grid()
    browse_button.grid()
    folder_tree.grid()
    folder_count_label.grid()

    # Hide the About section
    about_label.grid_remove()
    about_text.grid_remove()


# Create the main window
root = tk.Tk()
root.title("Directory Scanner")

# Set the window size to 800x600
root.geometry("450x400")

# Create a label to display the selected directory
label = tk.Label(root, text="Selected Directory: ")

# Create a button to open the file dialog
browse_button = tk.Button(root, text="Browse", command=browse_directory)

# Create a label to display the folder count result
folder_count_label = tk.Label(root, text="")

# Create a Treeview to display folder names and paths
folder_tree = ttk.Treeview(root, columns=("Folder Name", "Folder Path"), show="headings")
folder_tree.heading("Folder Name", text="Folder Name")
folder_tree.heading("Folder Path", text="Folder Path")

# Create a label to display the "About" section
about_label = tk.Label(root, text="About Section")

# Create a Text widget to display "About" information
about_text = tk.Text(root, wrap=tk.WORD, height=10, width=40)
about_text.insert(tk.END, "Your About Information Goes Here\n\n")

# Hide the "About" section initially
about_label.grid_remove()
about_text.grid_remove()

# Variable to store the selected directory
selected_directory = None

# Create a menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Create a "File" menu with "Home" and "Exit" options
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Home", command=show_home)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# Create a "Help" menu with an "About" option
help_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About", command=show_about)

# Initially, show the label and browse button
label.grid(row=0, column=0, padx=20, pady=20)
browse_button.grid(row=0, column=1, padx=20, pady=20)
folder_count_label.grid(row=1, column=0, columnspan=2, padx=20, pady=20)
folder_tree.grid(row=2, column=0, columnspan=2, padx=20, pady=20)

# Run the Tkinter main loop
root.mainloop()
