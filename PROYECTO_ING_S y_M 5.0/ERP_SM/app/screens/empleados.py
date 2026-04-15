from kivy.uix.screenmanager import Screen
from database import obtener_empleados
from database import importar_empleados_excel
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from database import eliminar_empleado


def importar_excel(self):

    layout = BoxLayout(orientation="vertical")

    filechooser = FileChooserListView(filters=["*.xlsx"])
    layout.add_widget(filechooser)

    btn_importar = Button(text="Importar", size_hint_y=None, height=40)
    layout.add_widget(btn_importar)

    popup = Popup(
        title="Seleccionar archivo Excel",
        content=layout,
        size_hint=(0.9, 0.9)
    )

    def cargar(_):
        if filechooser.selection:
            ruta = filechooser.selection[0]
            resultado = importar_empleados_excel(ruta)

            popup.dismiss()

            mensaje = f"""
Insertados: {resultado['insertados']}
Duplicados: {resultado['duplicados']}
"""

            if resultado['errores']:
                mensaje += f"\nError: {resultado['errores']}"

            resultado_popup = Popup(
                title="Resultado de Importación",
                content=Label(text=mensaje),
                size_hint=(0.6, 0.4)
            )

            resultado_popup.open()
            self.cargar_empleados()

    btn_importar.bind(on_release=cargar)
    popup.open()



# ===============================
# PANTALLA LISTA DE EMPLEADOS
# ===============================
class EmpleadosScreen(Screen):  

    def eliminar_empleado(self, empleado_id):

        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)

        layout.add_widget(Label(text="¿Seguro que deseas eliminar este empleado?"))

        botones = BoxLayout(size_hint_y=None, height=40, spacing=10)

        btn_si = Button(text="Sí")
        btn_no = Button(text="No")

        botones.add_widget(btn_si)
        botones.add_widget(btn_no)

        layout.add_widget(botones)

        popup = Popup(
            title="Confirmar eliminación",
            content=layout,
            size_hint=(0.6, 0.4)
        )

        def confirmar(_):
            eliminar_empleado(empleado_id)
            popup.dismiss()
            self.cargar_empleados()

        btn_si.bind(on_release=confirmar)
        btn_no.bind(on_release=lambda x: popup.dismiss())

        popup.open()

    def importar_excel(self):

        layout = BoxLayout(orientation="vertical")

        filechooser = FileChooserListView(filters=["*.xlsx"])
        layout.add_widget(filechooser)

        btn_importar = Button(text="Importar", size_hint_y=None, height=40)
        layout.add_widget(btn_importar)

        popup = Popup(
            title="Seleccionar archivo Excel",
            content=layout,
            size_hint=(0.9, 0.9)
        )

        def cargar(_):
            if filechooser.selection:
                ruta = filechooser.selection[0]
                resultado = importar_empleados_excel(ruta)

                popup.dismiss()

                mensaje = f"""
Insertados: {resultado['insertados']}
Duplicados: {resultado['duplicados']}
"""

                if resultado['errores']:
                    mensaje += f"\nError: {resultado['errores']}"

                resultado_popup = Popup(
                    title="Resultado de Importación",
                    content=Label(text=mensaje),
                    size_hint=(0.6, 0.4)
                )

                resultado_popup.open()
                self.cargar_empleados()

        btn_importar.bind(on_release=cargar)
        popup.open()


    def volver_dashboard(self):
        self.manager.current = "dashboard"

    def on_enter(self):
        self.cargar_empleados()


    def cargar_empleados(self):
        contenedor = self.ids.lista_empleados
        contenedor.clear_widgets()

        empleados = obtener_empleados()

        for emp in empleados:
            contenedor.add_widget(self.crear_item(emp))

    def crear_item(self, emp):
        # Usamos importaciones de kivymd locales para el item
        from kivymd.uix.label import MDLabel
        from kivymd.uix.button import MDRectangleFlatButton
        from kivymd.uix.boxlayout import MDBoxLayout
        
        fila = MDBoxLayout(size_hint_y=None, height="60dp", spacing="10dp", padding="5dp")

        fila.add_widget(MDLabel(text=emp[1], theme_text_color="Primary"))  # nombre
        fila.add_widget(MDLabel(text=emp[2], theme_text_color="Primary"))  # apellido
        fila.add_widget(MDLabel(text=emp[3], theme_text_color="Secondary"))  # cedula
        fila.add_widget(MDLabel(text=f"${emp[8]}", theme_text_color="Hint"))  # salario_base

        btn_editar = MDRectangleFlatButton(text="Editar", size_hint_x=None, width="90dp")
        btn_eliminar = MDRectangleFlatButton(text="Eliminar", size_hint_x=None, width="90dp", text_color=[0.8, 0, 0, 1], line_color=[0.8, 0, 0, 1])

        btn_editar.bind(on_release=lambda x: self.editar_empleado(emp))
        btn_eliminar.bind(on_release=lambda x: self.eliminar_empleado(emp[0]))

        fila.add_widget(btn_editar)
        fila.add_widget(btn_eliminar)

        return fila

    def abrir_formulario(self):
        self.manager.current = "empleado_form"
        

    def editar_empleado(self, emp):
        formulario = self.manager.get_screen("empleado_form")

        formulario.ids.input_nombre.text = emp[1]
        formulario.ids.input_apellido.text = emp[2]
        formulario.ids.input_cedula.text = emp[3]
        formulario.ids.input_telefono.text = emp[4]
        formulario.ids.input_email.text = emp[5]
        formulario.ids.input_nivel.text = emp[6]
        formulario.ids.input_puesto.text = emp[7]
        formulario.ids.input_salario.text = str(emp[8])
        formulario.ids.input_fecha.text = emp[9]

        formulario.empleado_id = emp[0]  # guardar id para actualizar

        self.manager.current = "empleado_form"

    

