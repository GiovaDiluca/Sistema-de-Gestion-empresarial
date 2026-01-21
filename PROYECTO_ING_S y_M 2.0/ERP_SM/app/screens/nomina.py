from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


class NominaScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation="vertical")

        layout.add_widget(Label(
            text="Módulo de Nómina",
            font_size=24
        ))

        layout.add_widget(Button(
            text="Volver",
            on_press=lambda x: self.volver()
        ))

        self.add_widget(layout)

    def volver(self):
        self.manager.current = "dashboard"
