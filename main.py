from kivy.app import App
from kivy.uix.label import Label

class TGameApp(App):
    def build(self):
        return Label(text="Halo! Ini APK pertama TGame")

TGameApp().run()
