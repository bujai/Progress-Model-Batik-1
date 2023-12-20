import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.applications import VGG16
import json

# Mengatur path untuk dataset
train_dir = 'Foto-Batik/train'
validation_dir = 'Foto-Batik/validation'

# Menyiapkan data generator untuk augmentasi data dan normalisasi
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    vertical_flip=True,  # Opsional, tergantung pada dataset Anda
    fill_mode='nearest'
)

validation_datagen = ImageDataGenerator(rescale=1./255)

# Mengatur data generator
train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(150, 150),
    batch_size=32,
    class_mode='categorical'
)

validation_generator = validation_datagen.flow_from_directory(
    validation_dir,
    target_size=(150, 150),
    batch_size=32,
    class_mode='categorical'
)

# Mengatur model dasar VGG16
base_model = VGG16(input_shape=(150, 150, 3), include_top=False, weights='imagenet')
base_model.trainable = False  # Membekukan lapisan dasar

# Membangun arsitektur model
model = Sequential([
    base_model,
    Flatten(),
    Dense(256, activation='relu'),
    Dropout(0.5),
    Dense(len(train_generator.class_indices), activation='softmax')
])

# Compile model dengan learning rate awal
optimizer = Adam(lr=1e-4)
model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

# Callback untuk menyimpan model terbaik
checkpoint = ModelCheckpoint('model-batik/model_batik.h5', save_best_only=True, monitor='val_loss', mode='min')

# Pelatihan model
history = model.fit(
    train_generator,
    epochs=25,
    validation_data=validation_generator,
    callbacks=[checkpoint]
)

# Simpan class_indices ke dalam file JSON setelah pelatihan
class_indices = train_generator.class_indices
with open('model-batik/class_indices_batik.json', 'w') as json_file:
    json.dump(class_indices, json_file)

# Convert Tensorflow Lite
# Lokasi file model .h5 Anda
model_path = 'model-batik/model_batik.h5'

# Memuat model .h5
model = tf.keras.models.load_model(model_path)

# Mengonversi model
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Menyimpan model yang telah dikonversi ke file .tflite
with open('model-batik/model_batik.tflite', 'wb') as f:
    f.write(tflite_model)

# Mulai fine-tuning
base_model.trainable = True

# Bekukan lapisan-lapisan awal
for layer in base_model.layers[:-4]:
    layer.trainable = False

# Compile model lagi untuk fine-tuning dengan learning rate yang lebih kecil
model.compile(optimizer=Adam(lr=1e-5), loss='categorical_crossentropy', metrics=['accuracy'])

# Lanjutkan pelatihan dengan fine-tuning
history_fine = model.fit(
    train_generator,
    epochs=25,  # Atur jumlah epoch sesuai kebutuhan
    validation_data=validation_generator,
    callbacks=[checkpoint]
)