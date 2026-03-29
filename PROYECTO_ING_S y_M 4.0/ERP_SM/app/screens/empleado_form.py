from kivy.uix.screenmanager import Screen
from database import actualizar_empleado, agregar_empleado

class EmpleadoFormScreen(Screen):
    empleado_id = None

    def guardar(self):    

        nombre = self.ids.input_nombre.text
        apellido = self.ids.input_apellido.text
        cedula = self.ids.input_cedula.text
        telefono = self.ids.input_telefono.text
        email = self.ids.input_email.text
        nivel = self.ids.input_nivel.text
        puesto = self.ids.input_puesto.text
        salario = self.ids.input_salario.text
        fecha = self.ids.input_fecha.text

        if not nombre or not apellido:
            self.ids.lbl_estado.text = "Nombre y apellido obligatorios"
            return

        if self.empleado_id:  # EDITAR
            actualizar_empleado(
                self.empleado_id,
                nombre, apellido, cedula, telefono,
                email, nivel, puesto, float(salario), fecha
            )
        else:  # CREAR
            agregar_empleado(
                nombre, apellido, cedula, telefono,
                email, nivel, puesto, float(salario), fecha
            )

        self.manager.get_screen("empleados").cargar_empleados()
        self.manager.current = "empleados"

        self.empleado_id = None
        self.limpiar()

    def limpiar(self):
        for campo in self.ids:
            if "input_" in campo:
                self.ids[campo].text = ""

    def volver(self):
        self.manager.current = "empleados"
