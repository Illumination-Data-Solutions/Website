import os
import time
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

IMG_DIRECTORY = "img"

def list_images(directory):
    return [f for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

def switch_image_names(directory, name1, name2):
    path1 = os.path.join(directory, name1)
    path2 = os.path.join(directory, name2)

    if not os.path.exists(path1) or not os.path.exists(path2):
        messagebox.showerror("Error", "One or both of the specified images do not exist.")
        return

    temp_name = "temp_image_name"
    os.rename(path1, os.path.join(directory, temp_name))
    os.rename(path2, path1)
    os.rename(os.path.join(directory, temp_name), path2)
    messagebox.showinfo("Success", f"Switched names: {name1} <-> {name2}")

def delete_image(directory, name):
    path = os.path.join(directory, name)
    if os.path.exists(path):
        os.remove(path)
        messagebox.showinfo("Success", f"Deleted image: {name}")
    else:
        messagebox.showerror("Error", f"Image {name} does not exist.")

def display_images():
    images = list_images(IMG_DIRECTORY)
    if not images:
        messagebox.showinfo("Info", "No images found in the directory.")
        return

    def on_switch():
        name1 = image1_var.get()
        name2 = image2_var.get()
        switch_image_names(IMG_DIRECTORY, name1, name2)
        refresh_images()

    def on_delete1():
        name1 = image1_var.get()
        delete_image(IMG_DIRECTORY, name1)
        refresh_images()

    def on_delete2():
        name2 = image2_var.get()
        delete_image(IMG_DIRECTORY, name2)
        refresh_images()

    def refresh_images():
        images = list_images(IMG_DIRECTORY)
        image1_var.set(images[0] if images else "")
        image2_var.set(images[1] if len(images) > 1 else "")
        update_image_display()

    def update_image_display():
        img1_path = os.path.join(IMG_DIRECTORY, image1_var.get())
        img2_path = os.path.join(IMG_DIRECTORY, image2_var.get())

        if os.path.exists(img1_path):
            img1 = Image.open(img1_path)
            img1 = img1.resize((200, 200), Image.LANCZOS)
            img1_tk = ImageTk.PhotoImage(img1)
            img1_label.config(image=img1_tk)
            img1_label.image = img1_tk
        else:
            img1_label.config(image='')

        if os.path.exists(img2_path):
            img2 = Image.open(img2_path)
            img2 = img2.resize((200, 200), Image.LANCZOS)
            img2_tk = ImageTk.PhotoImage(img2)
            img2_label.config(image=img2_tk)
            img2_label.image = img2_tk
        else:
            img2_label.config(image='')

    root = tk.Tk()
    root.title("Image Manager")

    image1_var = tk.StringVar(value=images[0] if images else "")
    image2_var = tk.StringVar(value=images[1] if len(images) > 1 else "")

    tk.Label(root, text="Image 1:").grid(row=0, column=0)
    tk.OptionMenu(root, image1_var, *images).grid(row=0, column=1)

    tk.Label(root, text="Image 2:").grid(row=1, column=0)
    tk.OptionMenu(root, image2_var, *images).grid(row=1, column=1)

    tk.Button(root, text="Switch", command=on_switch).grid(row=2, column=0)
    tk.Button(root, text="Delete Image 1", command=on_delete1).grid(row=2, column=1)
    tk.Button(root, text="Delete Image 2", command=on_delete2).grid(row=2, column=2)

    img1_label = tk.Label(root)
    img1_label.grid(row=3, column=0, columnspan=2)

    img2_label = tk.Label(root)
    img2_label.grid(row=3, column=2, columnspan=2)

    update_image_display()

    root.mainloop()

if __name__ == "__main__":
    display_images()