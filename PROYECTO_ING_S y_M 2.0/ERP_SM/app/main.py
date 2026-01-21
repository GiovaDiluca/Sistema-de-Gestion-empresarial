from kivy.app import App
from kivy.lang import Builder

from database import crear_tablas

from screens.dashboard import DashboardScreen
from screens.empleados import EmpleadosScreen
from screens.nomina import NominaScreen


class ERPApp(App):
    def build(self):
        crear_tablas()   # 👈 ESTA LÍNEA ES CLAVE
        return Builder.load_file("ui/main.kv")


if __name__ == "__main__":
    ERPApp().run()
