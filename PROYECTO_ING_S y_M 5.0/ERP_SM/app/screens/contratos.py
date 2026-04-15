from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty, ListProperty
from kivymd.toast import toast
from database import obtener_empleados
from services.pdf_services import generar_pdf_contrato
import os

PLANTILLA_GENERICA_BASE = """CONTRATO DE TRABAJO

Conste por el presente documento, que entre la empresa SOLUCIONES & MAS, y por otra parte el/la Sr/a. {nombre} {apellido}, portador(a) de la cédula de identidad {cedula}, se celebra el presente contrato individual de trabajo bajo los siguientes términos:

1. CARGO Y FUNCIONES: El trabajador desempeñará el cargo de {puesto}.
2. REMUNERACIÓN: El trabajador percibirá un salario base mensual de ${sueldo}.
3. INICIO: La fecha de ingreso registrada es {fecha_ingreso}.

Leído que fue el presente contrato, las partes lo aceptan y firman conforme.

___________________________         ___________________________
Firma del Empleado                  Firma del Empleador
"""

class ContratosScreen(Screen):
    empleado_spinner = ObjectProperty(None, allownone=True)
    plantilla_input = ObjectProperty(None, allownone=True)
    vista_previa_input = ObjectProperty(None, allownone=True)
    
    empleados_data = ListProperty([])
    empleado_seleccionado = ObjectProperty(None, allownone=True)
    
    def on_enter(self, *args):
        self.cargar_empleados()
        if not self.plantilla_input.text:
            self.plantilla_input.text = PLANTILLA_GENERICA_BASE
            
    def cargar_empleados(self):
        empleados_db = obtener_empleados()
        self.empleados_data = empleados_db
        # empleados_db schema: id, nombre, apellido, cedula, telefono, email, nivel, puesto, salario_base, fecha_ingreso, activo
        
        nombres = []
        for emp in empleados_db:
            nombre_completo = f"{emp[1]} {emp[2]} - {emp[3]}"
            nombres.append(nombre_completo)
            
        if nombres:
            self.empleado_spinner.values = nombres
            # self.empleado_spinner.text = "Seleccione un empleado"
        else:
            self.empleado_spinner.values = ["No hay empleados"]
            
    def seleccionar_empleado(self, texto_seleccion):
        self.empleado_seleccionado = None
        for emp in self.empleados_data:
            nombre_test = f"{emp[1]} {emp[2]} - {emp[3]}"
            if nombre_test == texto_seleccion:
                self.empleado_seleccionado = emp
                break
                
    def generar_vista_previa(self):
        if not self.empleado_seleccionado:
            toast("Por favor, seleccione un empleado.")
            return
            
        emp = self.empleado_seleccionado
        plantilla = self.plantilla_input.text
        
        # Mapeo de variables
        valores = {
            "{nombre}": emp[1],
            "{apellido}": emp[2],
            "{cedula}": emp[3],
            "{puesto}": emp[7],
            "{sueldo}": str(emp[8]),
            "{fecha_ingreso}": emp[9]
        }
        
        texto_final = plantilla
        for comodin, valor in valores.items():
            texto_final = texto_final.replace(comodin, str(valor))
            
        self.vista_previa_input.text = texto_final
        toast("Vista previa generada.")

    def exportar_pdf(self):
        if not self.vista_previa_input.text:
            toast("Primero genere la vista previa.")
            return
            
        if not self.empleado_seleccionado:
            toast("Por favor, seleccione un empleado.")
            return
            
        emp = self.empleado_seleccionado
        nombre_completo = f"{emp[1]} {emp[2]}"
        
        try:
            ruta = generar_pdf_contrato(nombre_completo, self.vista_previa_input.text)
            toast(f"PDF generado: {ruta}")
            # Limpiar
            self.vista_previa_input.text = ""
            self.empleado_spinner.text = "Seleccione un empleado"
            self.empleado_seleccionado = None
        except Exception as e:
            toast(f"Error al generar PDF: {e}")
