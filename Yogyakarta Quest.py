from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.metrics import dp  # Import the dp function
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.logger import Logger
from kivy.uix.popup import Popup
from kivy.uix.image import Image as KivyImage
from kivy.core.image import Image as CoreImage
# from kivy.uix.filechooser import FileChooserIconView
import io
# TensorFlow and Json
import tensorflow as tf
from PIL import Image as PILImage
from tensorflow.keras.models import load_model
import numpy as np
import json
# Firebase
#from kivy.uix.spinner import Spinner
from firebase_auth import sign_up_user
from firebase_auth import sign_in_user
from firebase_auth import db


# Adjust the window size and remove the top bar
Window.size = (356, 665)  # Adjusted to match the provided screenshot dimensions
#Window.borderless = True  # This will remove the window decoration to simulate a full-screen mobile app

class IntroScreen(Screen):
    def __init__(self, **kwargs):
        super(IntroScreen, self).__init__(**kwargs)

        with self.canvas.before:
            Color(198/255, 40/255, 40/255, 1)  # Correct the alpha value to 1
            self.rect = Rectangle(size=Window.size)

        layout = FloatLayout(size=Window.size)

        # Image logo
        logo = Image(source='Foto/LogoCapstone.png', size_hint=(None, None), size=(dp(300), dp(300)),
                     pos_hint={'center_x': 0.5, 'center_y': 0.60})
        layout.add_widget(logo)

        # Title label - Make sure the font file is included in the project directory
        title = Label(text='Yogyakarta Quest', font_name='Font/irishgroverregular.ttf', font_size=dp(24),
                      color=(1, 1, 1, 1), size_hint=(None, None), size=(Window.width, dp(30)),
                      pos_hint={'center_x': 0.5, 'top': .95})
        layout.add_widget(title)

        # Subtitle label
        subtitle = Label(text='Temukan Keindahan Setiap Sudutnya!',
                         color=(1, 1, 1, 1),  # Ensure the text color contrasts with the background
                         font_size=dp(20),
                         size_hint=(None, None),
                         size=(Window.width, dp(30)),
                         pos_hint={'center_x': 0.5, 'center_y': 0.35})
        layout.add_widget(subtitle)

        # Start button
        start_button = Button(text='Mulai', size_hint=(None, None), size=(dp(200), dp(50)),
                              pos_hint={'center_x': 0.5, 'y': dp(0.2)})  # Adjust the position as necessary
        start_button.bind(on_release=self.go_to_register)
        layout.add_widget(start_button)

        self.add_widget(layout)

    def go_to_register(self, instance):
        # This line will change the current screen to the RegisterScreen
        self.manager.current = 'register'

class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super(RegisterScreen, self).__init__(**kwargs)
        with self.canvas.before:
            Color(198 / 255, 40 / 255, 40 / 255, 1)  # Set background color to red
            self.rect = Rectangle(size=Window.size)

        layout = FloatLayout(size=Window.size)

        # Add the "Daftar" label
        daftar_label = Label(text='Daftar', font_name='Font/irishgroverregular.ttf', font_size=dp(24),
                             color=(1, 1, 1, 1), size_hint=(None, None), size=(Window.width, dp(30)), pos_hint={'center_x': 0.5, 'top': .95})
        layout.add_widget(daftar_label)

        # Create input fields for name, phone number, email, password, and password confirmation
        self.name_input = TextInput(hint_text='Nama', multiline=False, size_hint=(0.8, None), height=dp(40),
                                pos_hint={'center_x': 0.5, 'center_y': 0.8})
        self.phone_input = TextInput(hint_text='No Telepon', multiline=False, size_hint=(0.8, None), height=dp(40),
                                pos_hint={'center_x': 0.5, 'center_y': 0.7})
        self.email_input = TextInput(hint_text='Email', multiline=False, size_hint=(0.8, None), height=dp(40),
                                pos_hint={'center_x': 0.5, 'center_y': 0.6})
        self.address_input = TextInput(hint_text='Alamat', multiline=False, size_hint=(0.8, None), height=dp(40),
                                       pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.password_input = TextInput(hint_text='Kata Sandi', password=True, multiline=False, size_hint=(0.8, None),
                                   height=dp(40),
                                   pos_hint={'center_x': 0.5, 'center_y': 0.4})
        self.confirm_password_input = TextInput(hint_text='Ulangi Kata Sandi', password=True, multiline=False,
                                           size_hint=(0.8, None), height=dp(40),
                                           pos_hint={'center_x': 0.5, 'center_y': 0.3})

        # Add a status label to show the registration status
        self.status_label = Label(text='', size_hint=(None, None), size=(Window.width, dp(30)),
                                  pos_hint={'center_x': 0.5, 'y': dp(0.1)})
        layout.add_widget(self.status_label)

        # Create a register button and bind it to the register method
        register_button = Button(text='DAFTAR', size_hint=(0.8, None), height=dp(50),
                                 pos_hint={'center_x': 0.5, 'center_y': 0.2})
        register_button.bind(on_release=self.register)

        # Create a login button and bind it to the go_to_login method
        login_button = Button(text='Masuk', size_hint=(0.8, None), height=dp(50),
                              pos_hint={'center_x': 0.5, 'center_y': 0.1})
        login_button.bind(on_release=self.go_to_login)

        # Add widgets to the layout
        layout.add_widget(self.name_input)
        layout.add_widget(self.phone_input)
        layout.add_widget(self.email_input)
        layout.add_widget(self.address_input)
        layout.add_widget(self.password_input)
        layout.add_widget(self.confirm_password_input)
        layout.add_widget(register_button)
        layout.add_widget(login_button)

        self.add_widget(layout)

    def register(self, instance):
        name = self.name_input.text
        phone = self.phone_input.text
        email = self.email_input.text
        address = self.address_input.text
        password = self.password_input.text
        confirm_password = self.confirm_password_input.text

        if password == confirm_password:
            # Attempt to create the user in Firebase
            user = sign_up_user(name, phone, email, address, password)
            if user:
                print("User created successfully.")
                self.status_label.text = 'Status Daftar: Berhasil Daftar'
                # Optionally, you can switch to the login screen or some other screen
                self.manager.current = 'login'  # for example
            else:
                print("Failed to create user.")
                self.status_label.text = 'Status Daftar: Gagal Daftar'
        else:
            print("Passwords do not match.")

    def go_to_login(self, instance):
        self.manager.current = 'login'  # Make sure you have a 'login' screen defined and added to the ScreenManager

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        with self.canvas.before:
            Color(198 / 255, 40 / 255, 40 / 255, 1)  # Set background color to red
            self.rect = Rectangle(size=Window.size)

        layout = FloatLayout(size=Window.size)

        # Add the "Masuk" label
        masuk_label = Label(text='Masuk', font_name='Font/irishgroverregular.ttf', font_size=dp(24),
                            color=(1, 1, 1, 1), size_hint=(None, None), size=(Window.width, dp(30)),
                            pos_hint={'center_x': 0.5, 'top': .95})
        layout.add_widget(masuk_label)

        # Create input fields for phone number/email and password
        self.phone_email_input = TextInput(hint_text='No Telepon / Email', multiline=False, size_hint=(0.8, None),
                                           height=dp(40),
                                           pos_hint={'center_x': 0.5, 'center_y': 0.6})
        self.password_input = TextInput(hint_text='Kata Sandi', password=True, multiline=False, size_hint=(0.8, None),
                                        height=dp(40), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # Create a login button and bind it to the login method
        login_button = Button(text='Masuk', size_hint=(0.8, None), height=dp(50),
                              pos_hint={'center_x': 0.5, 'center_y': 0.4})
        login_button.bind(on_release=self.login)

        # Add a status label to show the registration status
        self.status_label = Label(text='', size_hint=(None, None), size=(Window.width, dp(30)),
                                  pos_hint={'center_x': 0.5, 'y': dp(0.1)})
        layout.add_widget(self.status_label)

        # Add widgets to the layout
        layout.add_widget(self.phone_email_input)
        layout.add_widget(self.password_input)
        layout.add_widget(login_button)

        self.add_widget(layout)

    def login(self, instance):
        phone_email = self.phone_email_input.text
        password = self.password_input.text

        # Authenticate with Firebase using the provided credentials
        #user_token = sign_in_user(phone_email, password)
        # Authenticate with Firebase using the provided credentials
        user_token, local_id = sign_in_user(phone_email, password)
        if user_token:
            print("User signed in successfully.")
            App.get_running_app().local_id = local_id
            # Switch to the main menu or dashboard screen
            self.manager.current = 'main_menu'  # replace with your main menu screen name
            self.status_label.text = 'Status Login: Berhasil Login'
        else:
            print("Failed to sign in user.")
            # Optionally, update the UI to notify the user of the failed sign-in attempt
            self.status_label.text = 'Status Login: Gagal Login'

class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MainMenuScreen, self).__init__(**kwargs)
        with self.canvas.before:
            Color(1, 0, 0, 1)  # Red background
            self.rect = Rectangle(size=Window.size)

        layout = FloatLayout(size=Window.size)

        # Add the "Masuk" label
        menu_label = Label(text='Main Menu', font_name='Font/irishgroverregular.ttf', font_size=dp(24),
                            color=(1, 1, 1, 1), size_hint=(None, None), size=(Window.width, dp(30)),
                            pos_hint={'center_x': 0.5, 'top': .95})
        layout.add_widget(menu_label)

        # Add a "Memprediksi Batik" button
        self.memprediksi_batik_button = Button(text='Memprediksi Batik', size_hint=(0.8, 0.15),
                                               pos_hint={'center_x': 0.5, 'center_y': 0.7})
        self.memprediksi_batik_button.bind(on_release=self.go_to_memprediksi_batik)
        layout.add_widget(self.memprediksi_batik_button)

        # Add a "Rekomendasi Wisata" button
        wisata_button = Button(text='Rekomendasi Wisata', size_hint=(0.8, 0.15),
                               pos_hint={'center_x': 0.5, 'center_y': 0.5})
        layout.add_widget(wisata_button)

        # Add a "Data User" button
        self.data_user_button = Button(text='Data User', size_hint=(0.8, 0.15),
                                  pos_hint={'center_x': 0.5, 'center_y': 0.3})
        self.data_user_button.bind(on_release=self.go_to_data_user)
        self.add_widget(self.data_user_button)

        self.add_widget(layout)

    def go_to_memprediksi_batik(self, instance):
        self.manager.current = 'memprediksi_batik'

    def go_to_data_user(self, instance):
        self.manager.current = 'data_user'

class MemprediksiBatikScreen(Screen):
    def __init__(self, **kwargs):
        super(MemprediksiBatikScreen, self).__init__(**kwargs)
        self.load_class_indices()  # Make sure this is called

        # Set the background to red
        with self.canvas.before:
            Color(198 / 255, 40 / 255, 40 / 255, 1)  # Set background color to red
            self.rect = Rectangle(size=Window.size)

        # Set up layout
        layout = BoxLayout(orientation='vertical')

        # Load model and class indices
        self.interpreter = tf.lite.Interpreter(model_path='model-batik/model_batik.tflite')
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

        # Image widget to display the uploaded image
        self.image_widget = Image(size_hint=(1, 0.8))
        layout.add_widget(self.image_widget)

        # Label to display the classification result
        self.result_label = Label(size_hint=(1, 0.1), text="Klasifikasi akan muncul di sini")
        layout.add_widget(self.result_label)

        # Button to upload an image
        self.upload_button = Button(text="Unggah Gambar", size_hint=(1, 0.1))
        self.upload_button.bind(on_release=self.upload_image)
        layout.add_widget(self.upload_button)

        # Button to classify the image
        self.classify_button = Button(text="Klasifikasi Batik", size_hint=(1, 0.1))
        self.classify_button.bind(on_release=self.classify_image)
        layout.add_widget(self.classify_button)

        self.add_widget(layout)

    def load_class_indices(self):
        class_indices_path = 'JSON/class_indices_batik.json'
        try:
            with open(class_indices_path, 'r') as file:
                self.class_indices = json.load(file)
            Logger.info(f"MemprediksiBatikScreen: Class indices loaded: {self.class_indices}")
        except Exception as e:
            self.class_indices = {}
            Logger.error(f"MemprediksiBatikScreen: Error loading class indices: {e}")

    def upload_image(self, instance):
        Logger.info("MemprediksiBatikScreen: Upload button pressed")
        content = BoxLayout(orientation='vertical')

        # Create a file chooser and add it to the layout
        self.filechooser = FileChooserListView(filters=["*.png", "*.jpg", "*.jpeg"])
        content.add_widget(self.filechooser)

        # Create a select button
        select_button = Button(text="Pilih", size_hint_y=None, height=30)
        select_button.bind(on_release=self.on_file_select)

        # Add the select button to the layout
        content.add_widget(select_button)

        # Create the popup
        self.popup = Popup(title="Pilih Foto Batik", content=content, size_hint=(0.9, 0.9))
        self.popup.open()

    def on_file_select(self, *args):
        Logger.info("MemprediksiBatikScreen: File selection event triggered")
        if self.filechooser.selection:
            selected = self.filechooser.selection[0]
            self.display_image(selected)
            self.popup.dismiss()  # Dismiss the popup after selection
            self.selected_image_path = selected
            self.classify_button.disabled = False
        else:
            Logger.warning("No image has been selected.")

    def display_image(self, file_path):
        core_image = CoreImage(file_path)
        self.image_widget.texture = core_image.texture

    def classify_image(self, instance=None):
        if hasattr(self, 'selected_image_path') and hasattr(self, 'class_indices'):
            try:
                pil_image = PILImage.open(self.selected_image_path).resize((150, 150))
                img = np.array(pil_image) / 255.0
                img = np.expand_dims(img, axis=0).astype(np.float32)

                # Set the tensor to the input image
                self.interpreter.set_tensor(self.input_details[0]['index'], img)

                # Run the inference
                self.interpreter.invoke()

                # Retrieve the output of the model
                output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
                class_idx = np.argmax(output_data, axis=1)[0]
                class_label = list(self.class_indices.keys())[class_idx]
                self.result_label.text = f"Prediksi: {class_label}"
                Logger.info(f"MemprediksiBatikScreen: Classification: {class_label}")
            except Exception as e:
                Logger.error(f"MemprediksiBatikScreen: Classification error: {e}")
        else:
            Logger.warn("MemprediksiBatikScreen: No image has been selected for classification")

class UserDataScreen(Screen):
    def __init__(self, **kwargs):
        super(UserDataScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=[10, 10, 10, 10], spacing=10)

        with self.canvas.before:
            Color(1, 0, 0, 1)  # Set the background to red
            self.rect = Rectangle(size=Window.size)

        # Data User Label
        self.data_label = Label(text='Data User', font_name='Font/irishgroverregular.ttf', font_size=dp(24),
                                color=(1, 1, 1, 1), size_hint=(1, None), height=dp(40),
                                pos_hint={'center_x': 0.5})
        self.layout.add_widget(self.data_label)

        # Placeholder labels for user data
        self.email_label = Label(text='Email: Loading...')
        self.name_label = Label(text='Nama: Loading...')
        self.phone_label = Label(text='No Telepon: Loading...')
        self.address_label = Label(text='Alamat: Loading...')

        # Add widgets to the layout
        self.layout.add_widget(self.email_label)
        self.layout.add_widget(self.name_label)
        self.layout.add_widget(self.phone_label)
        self.layout.add_widget(self.address_label)

        # Update Button
        self.update_data_button = Button(text='Update Data', size_hint_y=None, height=dp(50),
                                       pos_hint={'center_x': 0.5})
        self.update_data_button.bind(on_release=self.go_to_update_data_user)
        self.layout.add_widget(self.update_data_button)

        # Delete Data Button
        self.delete_data_button = Button(text='Delete Data', size_hint_y=None, height=dp(50),
                                         pos_hint={'center_x': 0.5})
        self.delete_data_button.bind(on_release=self.delete_data)
        self.layout.add_widget(self.delete_data_button)

        # Main Menu Button
        self.main_menu_button = Button(text='Main Menu', size_hint_y=None, height=dp(50),
                                       pos_hint={'center_x': 0.5})
        self.main_menu_button.bind(on_release=self.go_to_main_menu)
        self.layout.add_widget(self.main_menu_button)

        self.add_widget(self.layout)

    def go_to_main_menu(self, instance):
        self.manager.current = 'main_menu'

    def go_to_update_data_user(self, instance):
        self.manager.current = 'update_data_user'

    def on_enter(self):
        # This method is called when the screen is displayed
        local_id = App.get_running_app().local_id
        user_data_response = db.child("users").child(local_id).get()
        # user_data = self.get_user_data()
        user_data_response = db.child("users").child(local_id).get()
        if user_data_response.val():  # Use .val() to get the actual data from the response
            user_data = user_data_response.val()  # Now user_data is a dictionary
            self.email_label.text = f"Email: {user_data.get('email', 'Unavailable')}"
            self.name_label.text = f"Nama: {user_data.get('name', 'Unavailable')}"
            self.phone_label.text = f"No Telepon: {user_data.get('phone', 'Unavailable')}"
            self.address_label.text = f"Alamat: {user_data.get('address', 'Unavailable')}"

    def get_user_data(self):
        # TODO: Implement the function to fetch user data from Firebase
        # You will need to use the Firebase SDK or REST API to fetch the user data
        # The following is just a placeholder for illustration purposes
        return {
            "email": "user@example.com",
            "name": "User Name",
            "phone": "1234567890"
        }

    def delete_data(self, instance):
        local_id = App.get_running_app().local_id
        try:
            # Delete the user's data from Firebase
            db.child("users").child(local_id).remove()
            Logger.info("UserDataScreen: User data deleted successfully")
            # Go back to the IntroScreen
            self.manager.current = 'intro'
        except Exception as e:
            Logger.error(f"UserDataScreen: Failed to delete user data: {e}")
            self.status_label.text = 'Failed to delete data'

class UpdateDataUserScreen(Screen):
    def __init__(self, **kwargs):
        super(UpdateDataUserScreen, self).__init__(**kwargs)
        layout = FloatLayout(size=Window.size)

        with self.canvas.before:
            Color(198 / 255, 40 / 255, 40 / 255, 1)  # Set background color to red
            self.rect = Rectangle(size=Window.size)

        update_data_label = Label(text='Update Data', font_name='Font/irishgroverregular.ttf', font_size=dp(24),
                           color=(1, 1, 1, 1), size_hint=(None, None), size=(Window.width, dp(30)),
                           pos_hint={'center_x': 0.5, 'top': .95})
        layout.add_widget(update_data_label)

        # Status Label
        self.status_label = Label(text='', size_hint=(None, None), size=(Window.width, dp(30)),
                                  pos_hint={'center_x': 0.5, 'center_y': 0.85})
        layout.add_widget(self.status_label)

        # Create input fields for Name, Phone, and Address
        self.name_input = TextInput(hint_text='Nama', multiline=False, size_hint=(0.8, None), height=dp(40),
                                    pos_hint={'center_x': 0.5, 'center_y': 0.6})
        self.phone_input = TextInput(hint_text='No Telepon', multiline=False, size_hint=(0.8, None), height=dp(40),
                                     pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.address_input = TextInput(hint_text='Alamat', multiline=False, size_hint=(0.8, None), height=dp(40),
                                       pos_hint={'center_x': 0.5, 'center_y': 0.4})

        # Create a button to submit changes
        update_data_button = Button(text='Update Data', size_hint=(0.8, None), height=dp(50),
                               pos_hint={'center_x': 0.5, 'center_y': 0.3})
        update_data_button.bind(on_release=self.submit_update)

        # Main Menu button
        main_menu_button = Button(text='Main Menu', size_hint=(0.8, None), height=dp(50),
                                  pos_hint={'center_x': 0.5, 'y': dp(0.1)})
        main_menu_button.bind(on_release=self.go_to_main_menu)

        # Add widgets to the layout
        layout.add_widget(self.name_input)
        layout.add_widget(self.phone_input)
        layout.add_widget(self.address_input)
        layout.add_widget(update_data_button)
        layout.add_widget(main_menu_button)

        self.add_widget(layout)

    def go_to_main_menu(self, instance):
        self.manager.current = 'main_menu'

    def submit_update(self, *args):
        # Code to submit updates to Firebase
        local_id = App.get_running_app().local_id
        name = self.name_input.text
        phone = self.phone_input.text
        address = self.address_input.text

        # Update data in Firebase
        try:
            # Update data in Firebase
            db.child("users").child(local_id).update({"name": name, "phone": phone, "address": address})
            self.status_label.text = 'Status Update: Berhasil Update'
            print("User data updated successfully.")
        except Exception as e:
            self.status_label.text = 'Status Update: Gagal Update'
            print(f"Failed to update user data: {e}")
class YogyakartaQuestApp(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(IntroScreen(name='intro'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MainMenuScreen(name='main_menu'))
        sm.add_widget(MemprediksiBatikScreen(name='memprediksi_batik'))
        sm.add_widget(UserDataScreen(name='data_user'))
        sm.add_widget(UpdateDataUserScreen(name='update_data_user'))
        return sm

if __name__ == '__main__':
    YogyakartaQuestApp().run()