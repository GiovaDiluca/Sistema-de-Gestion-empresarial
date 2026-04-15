from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from database import obtener_empleados
from services.nomina_services import calcular_nomina, guardar_nomina
from services.pdf_services import generar_pdf_recibo
from kivymd.uix.pickers import MDDatePicker


class NominaScreen(Screen):

    def on_enter(self):
        self.cargar_empleados()

    def cargar_empleados(self):
        self.ids.spinner_empleados.values = []

        empleados = obtener_empleados()
        lista = [f"{emp[0]} - {emp[1]} {emp[2]}" for emp in empleados]

        self.ids.spinner_empleados.values = lista

    def mostrar_calendario(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save_date)
        date_dialog.open()

    def on_save_date(self, instance, value, date_range):
        self.ids.btn_fecha.text = str(value)


    def calcular(self):
        try:
            seleccion = self.ids.spinner_empleados.text

            if "-" not in seleccion:
                raise Exception("Seleccione un empleado")

            id_empleado = int(seleccion.split("-")[0])
            nombre = seleccion.split("-")[1].strip()
            # Obtener días según periodo
            periodo = self.ids.spinner_periodo.text
            if periodo == "Semanal":
                dias = 7
            elif periodo == "Quincenal":
                dias = 15
            elif periodo == "Mensual":
                dias = 30
            else:
                raise Exception("Seleccione un período válido")

            # Obtener fecha seleccionada
            fecha = self.ids.btn_fecha.text
            if fecha == "Seleccione fecha":
                raise Exception("Debe seleccionar una fecha")

            data = calcular_nomina(id_empleado, dias)

            # 🔹 Encabezado
            self.ids.encabezado_nomina.text = f"{nombre} | Fecha: {fecha}"

            # 🔹 Sueldo base
            self.ids.sueldo_base_lbl.text = f"${round(data['sueldo'],2)}"

            # 🔹 Limpiar tablas
            self.ids.tabla_ingresos.clear_widgets()
            self.ids.tabla_deducciones.clear_widgets()

            from kivy.uix.label import Label

            total_ingresos = 0
            total_deducciones = 0

            for d in data["detalles"]:
                if d["tipo"] == "ingreso":
                    self.ids.tabla_ingresos.add_widget(Label(text=d["nombre"]))
                    self.ids.tabla_ingresos.add_widget(Label(
                        text=f"+{round(d['monto'],2)}",
                        color=(0,1,0,1)
                    ))
                    total_ingresos += d["monto"]

                else:
                    self.ids.tabla_deducciones.add_widget(Label(text=d["nombre"]))
                    self.ids.tabla_deducciones.add_widget(Label(
                        text=f"-{round(d['monto'],2)}",
                        color=(1,0,0,1)
                    ))
                    total_deducciones += d["monto"]

            # 🔹 Totales
            self.ids.resumen_totales.text = (
                f"Total Ingresos: ${round(total_ingresos,2)}\n"
                f"Total Deducciones: ${round(total_deducciones,2)}\n"
                f"NETO: ${round(data['neto'],2)}"
            )

            self.data_nomina = data
            self.id_empleado = id_empleado

        except Exception as e:
            self.mostrar_popup(f"Error: {str(e)}")

    def guardar(self):
        try:
            fecha = self.ids.btn_fecha.text
            if fecha == "Seleccione fecha":
                raise Exception("Debe seleccionar una fecha")

            if not hasattr(self, "data_nomina"):
                raise Exception("Debe calcular primero")

            periodo = self.ids.spinner_periodo.text
            if periodo == "Semanal":
                dias = 7
            elif periodo == "Quincenal":
                dias = 15
            elif periodo == "Mensual":
                dias = 30
            else:
                raise Exception("Seleccione un período válido")

            guardar_nomina(
                self.id_empleado,
                fecha,
                dias
            )

            self.mostrar_popup("Nómina guardada correctamente")
            self.limpiar()

        except Exception as e:
            self.mostrar_popup(f"Error: {str(e)}")

    def generar_pdf(self):
        try:
            if not hasattr(self, "data_nomina"):
                raise Exception("Debe calcular primero para generar el recibo")
                
            nombre = self.ids.spinner_empleados.text
            fecha = self.ids.btn_fecha.text
            
            ruta_pdf = generar_pdf_recibo(nombre, fecha, self.data_nomina)
            
            self.mostrar_popup(f"Recibo generado exitosamente en:\n{ruta_pdf}")
        except Exception as e:
            self.mostrar_popup(f"Error generando PDF: {str(e)}")

    def limpiar(self):
        self.ids.btn_fecha.text = "Seleccione fecha"
        self.ids.spinner_periodo.text = "Seleccione período"
        self.ids.spinner_empleados.text = "Seleccione empleado"
        self.ids.sueldo_base_lbl.text = ""
        self.ids.encabezado_nomina.text = ""
        self.ids.resumen_totales.text = ""
        self.ids.tabla_ingresos.clear_widgets()
        self.ids.tabla_deducciones.clear_widgets()
        if hasattr(self, "data_nomina"):
            del self.data_nomina

    def volver(self):
        self.manager.current = "dashboard"

    def mostrar_popup(self, mensaje):
        popup = Popup(
            title="Información",
            content=Label(text=mensaje),
            size_hint=(0.6, 0.4)
        )
        popup.open()