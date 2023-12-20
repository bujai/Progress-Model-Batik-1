import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from tensorflow.keras.models import load_model
import numpy as np
import json

# Fungsi untuk memuat class_indices dari file JSON
def load_class_indices():
    class_indices_path = 'model-batik/class_indices_batik.json'  # Pastikan path ini benar
    with open(class_indices_path, 'r') as file:
        class_indices = json.load(file)
    return class_indices

class_indices = load_class_indices()  # Memuat class_indices ketika GUI dimulai

# Memuat model yang telah dilatih
model_path = 'model-batik/model_batik.h5'  # Pastikan untuk menggunakan path yang benar
model = load_model(model_path)

# Fungsi untuk memuat dan mempersiapkan gambar
def load_image(filename):
    img = Image.open(filename).resize((150, 150))
    img = np.array(img) / 255.0
    img = np.expand_dims(img, axis=0)
    return img

# Fungsi untuk melakukan prediksi
def classify_image():
    global image_path
    image = load_image(image_path)
    prediction = model.predict(image)
    class_idx = np.argmax(prediction, axis=1)[0]
    class_label = list(class_indices.keys())[class_idx]  # Gunakan class_indices yang dimuat
    result_label.config(text=f"Prediksi: {class_label}")

# Fungsi untuk memilih gambar
def upload_image():
    global image_path
    file_path = filedialog.askopenfilename()
    if not file_path:  # Jika tidak ada file yang dipilih, kembali.
        return
    image_path = file_path
    img = Image.open(file_path)
    img.thumbnail((150, 150), Image.Resampling.LANCZOS)
    img = ImageTk.PhotoImage(img)
    panel.config(image=img)
    panel.image = img
    classify_button.config(state=tk.NORMAL)

# Membuat jendela utama
window = tk.Tk()
window.title('Klasifikasi Batik')

# Panel untuk menampilkan gambar
panel = tk.Label(window)
panel.grid(column=0, row=0, columnspan=2)

# Label untuk menampilkan hasil prediksi
result_label = tk.Label(window, text="Klik 'Unggah' untuk memilih gambar batik.", font=('bold', 14))
result_label.grid(column=0, row=1, columnspan=2)

# Tombol untuk mengunggah gambar
upload_button = tk.Button(window, text='Unggah', command=upload_image)
upload_button.grid(column=0, row=2)

# Tombol untuk klasifikasi
classify_button = tk.Button(window, text='Klasifikasi', state=tk.DISABLED, command=classify_image)
classify_button.grid(column=1, row=2)

window.mainloop()