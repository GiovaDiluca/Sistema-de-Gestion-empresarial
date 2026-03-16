from kivy.app import App
from kivy.lang import Builder

# importar screens
from screens.dashboard import DashboardScreen
from screens.empleados import EmpleadosScreen
from screens.empleado_form import EmpleadoFormScreen

from database import create_tables   # ← ESTE ES EL NOMBRE CORRECTO


class ERPApp(App):
    def build(self):
        create_tables()   # ← aquí también

        Builder.load_file("ui/dashboard.kv")
        Builder.load_file("ui/empleados.kv")
        Builder.load_file("ui/empleado_form.kv")
        Builder.load_file("ui/nomina.kv")

        return Builder.load_file("ui/main.kv")


if __name__ == "__main__":
    ERPApp().run()
