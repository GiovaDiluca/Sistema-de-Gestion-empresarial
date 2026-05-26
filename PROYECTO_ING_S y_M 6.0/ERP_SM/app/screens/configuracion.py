from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import obtener_empresa, actualizar_empresa

class ConfiguracionScreen(Screen):
    def on_enter(self):
        self.cargar_datos()

    def cargar_datos(self):
        datos = obtener_empresa()
        self.ids.nombre_input.text = datos["nombre"]
        self.ids.rif_input.text = datos["rif"]
        self.ids.direccion_input.text = datos["direccion"]
        self.ids.telefono_input.text = datos["telefono"]

    def guardar_datos(self):
        nombre = self.ids.nombre_input.text.strip()
        rif = self.ids.rif_input.text.strip()
        direccion = self.ids.direccion_input.text.strip()
        telefono = self.ids.telefono_input.text.strip()

        if not nombre or not rif:
            self.mostrar_popup("Error", "Nombre y RIF son obligatorios")
            return
            
        try:
            actualizar_empresa(nombre, rif, direccion, telefono)
            self.mostrar_popup("Éxito", "Datos de la empresa actualizados")
        except Exception as e:
            self.mostrar_popup("Error", f"No se pudieron guardar los datos:\n{str(e)}")

    def volver(self):
        self.manager.current = "dashboard"

    def mostrar_popup(self, titulo, mensaje):
        popup = Popup(
            title=titulo,
            content=Label(text=mensaje),
            size_hint=(0.6, 0.4)
        )
        popup.open()
