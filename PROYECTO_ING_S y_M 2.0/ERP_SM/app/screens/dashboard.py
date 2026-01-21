from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


class DashboardScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation="vertical")

        layout.add_widget(Label(
            text="ERP S&M\nBienvenido",
            font_size=28
        ))

        layout.add_widget(Button(
            text="Empleados",
            on_press=lambda x: self.ir_empleados()
        ))

        layout.add_widget(Button(
            text="Nómina",
            on_press=lambda x: self.ir_nomina()
        ))

        self.add_widget(layout)

    def ir_empleados(self):
        self.manager.current = "empleados"

    def ir_nomina(self):
        self.manager.current = "nomina"
