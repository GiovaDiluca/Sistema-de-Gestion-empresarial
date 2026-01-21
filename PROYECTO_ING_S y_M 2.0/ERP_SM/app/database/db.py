# app/database/db.py
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "erp.db")

def conectar():
    return sqlite3.connect(DB_NAME)

def crear_tablas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS empleados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        cargo TEXT NOT NULL,
        salario REAL NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS nomina (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        empleado_id INTEGER,
        mes TEXT,
        salario_bruto REAL,
        deducciones REAL,
        impuestos REAL,
        FOREIGN KEY (empleado_id) REFERENCES empleados(id)
    )
    """)

    conn.commit()
    conn.close()

def agregar_empleado(nombre, cargo, salario):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO empleados (nombre, cargo, salario)
        VALUES (?, ?, ?)
    """, (nombre, cargo, salario))

    conn.commit()
    conn.close()

def obtener_empleados():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nombre, cargo, salario
        FROM empleados
        ORDER BY nombre
    """)

    empleados = cursor.fetchall()
    conn.close()

    return empleados

def obtener_nominas_por_empleado(empleado_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, mes, salario_bruto, deducciones, impuestos
    FROM nomina
    WHERE empleado_id = ?
    """, (empleado_id,))

    datos = cursor.fetchall()
    conn.close()
    return datos
