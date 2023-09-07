import os
import threading
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

# Constants
SIZE_NAMES = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
MAX_DISPLAY_FOLDERS = 20


# Method to browse for a directory
def browse_directory():
    directory_path = filedialog.askdirectory()
    if directory_path:
        label.config(text="Selected Directory: " + directory_path)
        selected_directory.set(directory_path)
        clear_results()
        start_scan_thread()


# Method to get the size of a directory
def get_directory_size(path):
    total_size = 0
    for dirpath, _, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)
    return total_size


# Method to convert file size in bytes to a readable format
def convert_bytes_to_readable(size_in_bytes):
    size_index = 0
    while size_in_bytes > 1024 and size_index < len(SIZE_NAMES) - 1:
        size_in_bytes /= 1024.0
        size_index += 1
    return f"{size_in_bytes:.2f} {SIZE_NAMES[size_index]}"


# Method to get single directory size as a readable format
def get_single_directory_size(path):
    size_bytes = get_directory_size(path)
    return convert_bytes_to_readable(size_bytes)


# Method to scan the selected directory in a separate thread
def browse_directory_scan_thread():
    directory_path = selected_directory.get()

    if directory_path:
        folder_entries = [entry for entry in os.scandir(directory_path) if entry.is_dir()]
        folder_count_label.config(text=f"Number of Folders: {len(folder_entries)}")

        total_items = len(folder_entries)
        progress = 0

        # Show the progress bar and stop button
        progress_bar.grid()
        stop_scan_button.grid()

        # Calculate the number of rows to display
        num_rows_to_display = min(MAX_DISPLAY_FOLDERS, total_items)

        # Update the Treeview height based on the number of rows
        folder_tree.configure(height=num_rows_to_display)

        # Update the progress bar
        progress_bar["maximum"] = total_items

        # Resize the window based on the number of rows
        new_window_height = min(num_rows_to_display * 25 + 200, 600)
        root.geometry(f"650x{new_window_height}")

        for folder_entry in folder_entries:
            if stop_scan_flag.is_set():  # Check if the stop flag is set
                break

            # Get the folder name, and path
            folder_name = folder_entry.name
            folder_path = folder_entry.path

            # Get the folder size
            try:
                folder_size = get_single_directory_size(folder_path)
            except Exception as e:
                messagebox.showerror("Error", f"Error in {folder_name}: {e}")
                folder_size = "ERROR"

            folder_tree.insert("", "end", values=(folder_name, folder_path, folder_size))

            # Update the progress bar
            progress += 1
            progress_bar["value"] = progress
            root.update_idletasks()

        # Update the total size label
        folder_size_label.config(text=f"Total Size of Directory: {get_single_directory_size(directory_path)}")

        # Hide the progress bar and stop button
        progress_bar.grid_remove()
        stop_scan_button.grid_remove()


# Method to clear the Treeview, progress bar, and labels
def clear_results():
    folder_tree.delete(*folder_tree.get_children())
    folder_count_label.config(text="")
    folder_size_label.config(text="")
    progress_bar["value"] = 0
    folder_tree.configure(height=MAX_DISPLAY_FOLDERS)


# Flag to stop the scanning thread
stop_scan_flag = threading.Event()


# Method to start the directory scan in a separate thread
def start_scan_thread():
    stop_scan_flag.clear()  # Clear the flag to allow scanning
    scan_thread = threading.Thread(target=browse_directory_scan_thread)
    scan_thread.daemon = True  # The thread will exit when the main program exits
    scan_thread.start()


# Method to stop the scanning thread
def stop_scan_thread():
    stop_scan_flag.set()
    clear_results()


# Method to show the Home screen
def show_home():
    # Show other items
    label.grid()
    browse_button.grid()
    folder_tree.grid()
    folder_count_label.grid()
    folder_size_label.grid()
    progress_bar.grid()
    stop_scan_button.grid()

    # Hide the About section
    about_label.grid_remove()
    about_text.grid_remove()


# Method to show the About screen
def show_about():
    # Hide other items
    label.grid_remove()
    browse_button.grid_remove()
    folder_tree.grid_remove()
    folder_count_label.grid_remove()
    folder_size_label.grid_remove()
    progress_bar.grid_remove()
    stop_scan_button.grid_remove()

    # Show the About section
    about_label.grid(row=0, column=0, padx=20, pady=20)
    about_text.grid(row=1, column=0, padx=20, pady=20)


# Create the main window
root = tk.Tk()
root.title("Directory Scanner")
root.geometry("650x400")  # Initial window size

icon_path = os.path.join(os.path.dirname(__file__), 'app.ico')
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)
else:
    print(f"Icon file not found: {icon_path}")

# Create a StringVar to store the selected directory
selected_directory = tk.StringVar()

# Create a label to display the selected directory
label = tk.Label(root, text="Selected Directory: ")

# Set the StringVar for the label
label["textvariable"] = selected_directory

# Create a button to open the file dialog
browse_button = tk.Button(root, text="Browse", command=browse_directory)

# Create a label to display the folder count result
folder_count_label = tk.Label(root, text="")

# Create a label to display the folder size result
folder_size_label = tk.Label(root, text="")

# Create a Treeview to display folder names, paths, and sizes
folder_tree = ttk.Treeview(root, columns=("Folder Name", "Folder Path", "Folder Size"), show="headings")
folder_tree.heading("Folder Name", text="Folder Name")
folder_tree.heading("Folder Path", text="Folder Path")
folder_tree.heading("Folder Size", text="Folder Size")
folder_tree.column("Folder Name", width=150)
folder_tree.column("Folder Path", width=300)
folder_tree.column("Folder Size", width=100)
folder_tree.configure(height=MAX_DISPLAY_FOLDERS)

# Create a vertical scrollbar for the Treeview
tree_scrollbar = ttk.Scrollbar(root, orient="vertical", command=folder_tree.yview)
folder_tree.configure(yscrollcommand=tree_scrollbar.set)

# Create a progress bar
progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")

# Buttons to star and stop the scan
# start_scan_button = tk.Button(root, text="Start Scan", command=start_scan_thread)
stop_scan_button = tk.Button(root, text="Stop Scan", command=stop_scan_thread)

# Hide the progress bar and stop button
progress_bar.grid_remove()
stop_scan_button.grid_remove()

# Create a label to display the "About" section
about_label = tk.Label(root, text="About")

# Create a label to display the description
about_text = tk.Label(root, text="I'm Paradocx96 and Python is my favorite programming language.\n\n")

# Hide the "About" section initially
about_label.grid_remove()
about_text.grid_remove()

# Initially, show the label and browse button
label.grid(row=0, column=0, padx=20, pady=20)
browse_button.grid(row=0, column=1, padx=20, pady=20)
folder_count_label.grid(row=1, column=0, padx=20, pady=20)
folder_size_label.grid(row=1, column=1, padx=20, pady=20)
folder_tree.grid(row=2, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")
tree_scrollbar.grid(row=2, column=2, sticky="ns")
progress_bar.grid(row=3, column=0, columnspan=2, padx=20, pady=20)
stop_scan_button.grid(row=4, column=0, padx=20, pady=20)

# Configure grid row and column weights to make the Treeview expand with the window size
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)

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

# Start the main loop
if __name__ == '__main__':
    root.mainloop()
