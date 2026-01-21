from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from database import agregar_empleado, obtener_empleados


class EmpleadosScreen(Screen):

    def volver_dashboard(self, *args):
        self.manager.current = "dashboard"

    def guardar_empleado(self, *args):
        nombre = self.input_nombre.text
        cargo = self.input_cargo.text
        salario = self.input_salario.text

        if not nombre or not cargo or not salario:
            self.lbl_estado.text = "❌ Todos los campos son obligatorios"
            return

        try:
            agregar_empleado(nombre, cargo, float(salario))
            self.lbl_estado.text = "✅ Empleado guardado correctamente"

            self.input_nombre.text = ""
            self.input_cargo.text = ""
            self.input_salario.text = ""

        except Exception as e:
            self.lbl_estado.text = f"❌ Error: {e}"

    def on_enter(self):
        self.clear_widgets()

        layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=10
        )

        layout.add_widget(Label(
            text="REGISTRO DE EMPLEADOS",
            font_size=24,
            size_hint_y=None,
            height=50
        ))

        self.input_nombre = TextInput(
            hint_text="Nombre del empleado",
            multiline=False
        )

        self.input_cargo = TextInput(
            hint_text="Cargo",
            multiline=False
        )

        self.input_salario = TextInput(
            hint_text="Salario",
            multiline=False,
            input_filter="float"
        )

        layout.add_widget(self.input_nombre)
        layout.add_widget(self.input_cargo)
        layout.add_widget(self.input_salario)

        btn_guardar = Button(
            text="Guardar empleado",
            size_hint_y=None,
            height=50
        )
        btn_guardar.bind(on_press=self.guardar_empleado)

        layout.add_widget(btn_guardar)

        self.lbl_estado = Label(
            text="",
            size_hint_y=None,
            height=40
        )

        layout.add_widget(self.lbl_estado)

        btn_volver = Button(
            text="Volver al Dashboard",
            size_hint_y=None,
            height=50
        )
        btn_volver.bind(on_press=self.volver_dashboard)

        layout.add_widget(btn_volver)

        self.add_widget(layout)
