import os
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk

def list_images(directory):
    return [f for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

def switch_image_names(path1, path2):
    directory = os.path.dirname(path1)
    name1 = os.path.basename(path1)
    name2 = os.path.basename(path2)

    temp_name = "temp_image_name"
    os.rename(path1, os.path.join(directory, temp_name))
    os.rename(path2, path1)
    os.rename(os.path.join(directory, temp_name), path2)
    messagebox.showinfo("Success", f"Switched names: {name1} <-> {name2}")

def delete_image(path):
    if os.path.exists(path):
        os.remove(path)
        messagebox.showinfo("Success", f"Deleted image: {os.path.basename(path)}")
    else:
        messagebox.showerror("Error", f"Image {os.path.basename(path)} does not exist.")

def display_images():
    def select_image1():
        path = filedialog.askopenfilename()
        if path:
            image1_var.set(path)
            update_image_display()

    def select_image2():
        path = filedialog.askopenfilename()
        if path:
            image2_var.set(path)
            update_image_display()

    def on_switch():
        path1 = image1_var.get()
        path2 = image2_var.get()
        switch_image_names(path1, path2)
        update_image_display()

    def on_delete1():
        path1 = image1_var.get()
        delete_image(path1)
        image1_var.set("")
        update_image_display()

    def on_delete2():
        path2 = image2_var.get()
        delete_image(path2)
        image2_var.set("")
        update_image_display()

    def update_image_display():
        img1_path = image1_var.get()
        img2_path = image2_var.get()

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

    image1_var = tk.StringVar()
    image2_var = tk.StringVar()

    tk.Button(root, text="Select Image 1", command=select_image1).grid(row=0, column=0)
    tk.Entry(root, textvariable=image1_var, width=50).grid(row=0, column=1)

    tk.Button(root, text="Select Image 2", command=select_image2).grid(row=1, column=0)
    tk.Entry(root, textvariable=image2_var, width=50).grid(row=1, column=1)

    tk.Button(root, text="Switch", command=on_switch).grid(row=2, column=0)
    tk.Button(root, text="Delete Image 1", command=on_delete1).grid(row=2, column=1)
    tk.Button(root, text="Delete Image 2", command=on_delete2).grid(row=2, column=2)

    img1_label = tk.Label(root)
    img1_label.grid(row=3, column=0, columnspan=2)

    img2_label = tk.Label(root)
    img2_label.grid(row=3, column=2, columnspan=2)

    root.mainloop()

if __name__ == "__main__":
    display_images()