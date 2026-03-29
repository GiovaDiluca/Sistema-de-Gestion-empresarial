from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button

from database import *


class ConceptosScreen(Screen):

    def on_pre_enter(self):
        self.cargar_conceptos()

    def cargar_conceptos(self):
        self.ids.lista_conceptos.clear_widgets()
        conceptos = obtener_conceptos()

        for c in conceptos:
            id_c, nombre, tipo, valor, es_porcentaje = c

            simbolo = "%" if es_porcentaje else "$"
            texto = f"{nombre} | {tipo.upper()} | {simbolo}{valor}"

            btn = Button(
                text=texto,
                size_hint_y=None,
                height=45
            )
            btn.bind(on_release=lambda x, c=c: self.seleccionar(c))

            self.ids.lista_conceptos.add_widget(btn)

    def guardar(self):
        try:
            nombre = self.ids.nombre.text.strip()
            tipo = self.ids.tipo.text
            valor = float(self.ids.valor.text)
            es_porcentaje = 1 if self.ids.es_porcentaje.active else 0

            if not nombre:
                raise Exception("Nombre requerido")

            agregar_concepto(nombre, tipo, valor, es_porcentaje)

            self.mostrar("Concepto creado")
            self.limpiar()
            self.cargar_conceptos()

        except Exception as e:
            self.mostrar(str(e))

    def seleccionar(self, concepto):
        id_c, nombre, tipo, valor, es_porcentaje = concepto

        self.concepto_id = id_c
        self.ids.nombre.text = nombre
        self.ids.tipo.text = tipo
        self.ids.valor.text = str(valor)
        self.ids.es_porcentaje.active = bool(es_porcentaje)

    def actualizar(self):
        try:
            if not hasattr(self, "concepto_id"):
                raise Exception("Seleccione un concepto")

            actualizar_concepto(
                self.concepto_id,
                self.ids.nombre.text,
                self.ids.tipo.text,
                float(self.ids.valor.text),
                1 if self.ids.es_porcentaje.active else 0
            )

            self.mostrar("Concepto actualizado")
            self.limpiar()
            self.cargar_conceptos()

        except Exception as e:
            self.mostrar(str(e))

    def eliminar(self):
        try:
            if not hasattr(self, "concepto_id"):
                raise Exception("Seleccione un concepto")

            eliminar_concepto(self.concepto_id)

            self.mostrar("Concepto eliminado")
            self.limpiar()
            self.cargar_conceptos()

        except Exception as e:
            self.mostrar(str(e))

    def limpiar(self):
        self.ids.nombre.text = ""
        self.ids.tipo.text = "ingreso"
        self.ids.valor.text = ""
        self.ids.es_porcentaje.active = False
        self.concepto_id = None

    def volver(self):
        self.manager.current = "dashboard"

    def mostrar(self, msg):
        Popup(
            title="Sistema",
            content=Label(text=msg),
            size_hint=(0.5, 0.3)
        ).open()