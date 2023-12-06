import os
import zipfile
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.models import Sequential
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau

# Tentukan path untuk dataset
zip_path = 'Batik.zip'
csv_path = 'CSV/Dataset Motif Batik.csv'
extracted_path = 'Extract/extracted_images/Batik'

# Ekstrak file zip
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extracted_path)

# Baca file CSV untuk mendapatkan label dan deskripsi
df = pd.read_csv(csv_path)

# Memuat gambar dan label
images = []
labels = []

for index, row in df.iterrows():
    image_filename = os.path.join(extracted_path, row['Label'] + '.jpg')
    image = tf.keras.preprocessing.image.load_img(image_filename, target_size=(224, 224))
    image = tf.keras.preprocessing.image.img_to_array(image) / 255.0  # Normalisasi nilai piksel
    images.append(image)
    labels.append(row['Label'])

# Konversi ke numpy array
images = np.array(images)
labels = np.array(labels)

# Pra-pemrosesan label
label_binarizer = LabelBinarizer()
labels = label_binarizer.fit_transform(labels)

# Membagi data menjadi set pelatihan dan pengujian
X_train, X_test, y_train, y_test = train_test_split(images, labels, test_size=0.2, random_state=42)

# Model CNN
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
    MaxPooling2D(2, 2),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    Flatten(),
    Dense(512, activation='relu'),
    Dropout(0.5),
    Dense(len(label_binarizer.classes_), activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Callbacks
callbacks = [
    EarlyStopping(monitor='val_loss', patience=5, verbose=1),
    ModelCheckpoint('Model/model_batik.h5', save_best_only=True, monitor='val_loss', mode='min'),
    ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=2, verbose=1)
]

# Data augmentation generator
train_datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

val_datagen = ImageDataGenerator()

# Fit the data generator to the training data
train_generator = train_datagen.flow(X_train, y_train, batch_size=32)
val_generator = val_datagen.flow(X_test, y_test, batch_size=32)

# Tentukan jumlah sampel
train_samples = len(X_train)
val_samples = len(X_test)
batch_size = 32

# Hitung steps_per_epoch dan validation_steps
steps_per_epoch = train_samples // batch_size if train_samples > batch_size else 1
validation_steps = val_samples // batch_size if val_samples > batch_size else 1

# Pelatihan model dengan data augmentation
history = model.fit(
    train_generator,
    steps_per_epoch=steps_per_epoch,  # Pastikan nilai ini bukan 0
    validation_data=val_generator,
    validation_steps=validation_steps,  # Pastikan nilai ini bukan 0
    epochs=50,  # Anda mungkin ingin menyesuaikan jumlah epochs
    callbacks=callbacks
)

# Fungsi untuk memprediksi dan mendapatkan deskripsi
def predict_and_describe(image_path, model, label_binarizer, df):
    image = tf.keras.preprocessing.image.load_img(image_path, target_size=(224, 224))
    image = tf.keras.preprocessing.image.img_to_array(image) / 255.0  # Normalisasi nilai piksel
    image = np.expand_dims(image, axis=0)

    prediction = model.predict(image)
    label = label_binarizer.inverse_transform(prediction)[0]

    description = df[df['Label'] == label]['Deskripsi'].values[0]
    return label, description

# Contoh penggunaan fungsi predict_and_describe
# Anda harus menyesuaikan 'path_to_new_image.jpg' dengan path gambar yang ingin Anda prediksi
# label, description = predict_and_describe('path_to_new_image.jpg', best_model, label_binarizer, df)
# print(f"Label: {label}")
# print(f"Description: {description}")