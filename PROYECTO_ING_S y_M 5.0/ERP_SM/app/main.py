from kivymd.app import MDApp
from kivy.lang import Builder

# importar screens
from screens.dashboard import DashboardScreen
from screens.empleados import EmpleadosScreen
from screens.empleado_form import EmpleadoFormScreen
from screens.nomina import NominaScreen
from screens.conceptos import ConceptosScreen
from screens.contratos import ContratosScreen

from database import create_tables   # ← ESTE ES EL NOMBRE CORRECTO


class ERPApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "LightBlue"

        create_tables()   # ← aquí también

        Builder.load_file("ui/dashboard.kv")
        Builder.load_file("ui/empleados.kv")
        Builder.load_file("ui/empleado_form.kv")
        Builder.load_file("ui/nomina.kv")
        Builder.load_file("ui/conceptos.kv")
        Builder.load_file("ui/contratos.kv")

        return Builder.load_file("ui/main.kv")


if __name__ == "__main__":
    ERPApp().run()
