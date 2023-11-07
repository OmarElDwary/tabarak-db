import tkinter as tk
from tkinter import filedialog
from pymongo import MongoClient
from bson import Binary
import io
from PIL import Image, ImageTk

# MongoDB connection details
mongo_url = "mongodb+srv://admin:tabarak1234@tabarak.94qrjvu.mongodb.net/?retryWrites=true&w=majority"
db_name = "test"
collection_name = "properties"

# Create a MongoDB client and select the database and collection
client = MongoClient(mongo_url)
db = client[db_name]
collection = db[collection_name]

# Tkinter GUI
def add_property():
    title = entry_title.get()
    description = entry_description.get()
    image_path = entry_image.get()

    # Read the image file and convert it to binary data
    with open(image_path, "rb") as image_file:
        image_binary = Binary(image_file.read())

    property = {"title": title, "description": description, "image": image_binary}
    collection.insert_one(property)

    # Clear input fields
    entry_title.delete(0, tk.END)
    entry_description.delete(0, tk.END)
    entry_image.delete(0, tk.END)

def show_properties():
    properties = collection.find()

    property_list.delete(0, tk.END)

    for prop in properties:
        property_list.insert(tk.END, f"Title: {prop['title']}, Description: {prop['description']}")

def browse_image():
    file_path = filedialog.askopenfilename()
    entry_image.delete(0, tk.END)
    entry_image.insert(0, file_path)

# Create the main window
root = tk.Tk()
root.title("Property Management")

# Create widgets
label_title = tk.Label(root, text="Title:")
label_description = tk.Label(root, text="Description:")
label_image = tk.Label(root, text="Image:")
entry_title = tk.Entry(root)
entry_description = tk.Entry(root)
entry_image = tk.Entry(root)
add_button = tk.Button(root, text="Add Property", command=add_property)
show_button = tk.Button(root, text="Show Properties", command=show_properties)
browse_button = tk.Button(root, text="Browse Image", command=browse_image)
property_list = tk.Listbox(root, width=50)

# Place widgets on the window
label_title.grid(row=0, column=0)
label_description.grid(row=1, column=0)
label_image.grid(row=2, column=0)
entry_title.grid(row=0, column=1)
entry_description.grid(row=1, column=1)
entry_image.grid(row=2, column=1)
add_button.grid(row=3, column=0, columnspan=2)
show_button.grid(row=4, column=0, columnspan=2)
browse_button.grid(row=5, column=0, columnspan=2)
property_list.grid(row=6, column=0, columnspan=2)

root.mainloop()