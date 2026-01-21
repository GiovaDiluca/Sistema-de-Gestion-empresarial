# app/database.py
import sqlite3
import os

# Ruta a la base de datos
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'database.db')

def get_connection():
    """Devuelve una conexión a la base de datos."""
    return sqlite3.connect(DB_PATH)

def create_tables():
    """Crea las tablas necesarias si no existen."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Tabla de empleados
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS empleados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            salario_base REAL NOT NULL,
            fecha_ingreso DATE NOT NULL,
            puesto TEXT,
            activo INTEGER DEFAULT 1  -- 1 = activo, 0 = inactivo
        )
    ''')
    
    # Tabla de nóminas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nominas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_empleado INTEGER NOT NULL,
            mes TEXT NOT NULL,  -- Formato: YYYY-MM
            salario_bruto REAL NOT NULL,
            deducciones REAL DEFAULT 0,
            impuestos REAL DEFAULT 0,
            salario_neto REAL NOT NULL,
            fecha_generacion DATE DEFAULT CURRENT_DATE,
            FOREIGN KEY (id_empleado) REFERENCES empleados (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Funciones CRUD para empleados
def agregar_empleado(nombre, apellido, salario_base, fecha_ingreso, puesto):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO empleados (nombre, apellido, salario_base, fecha_ingreso, puesto)
        VALUES (?, ?, ?, ?, ?)
    ''', (nombre, apellido, salario_base, fecha_ingreso, puesto))
    conn.commit()
    conn.close()

def obtener_empleados():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM empleados WHERE activo = 1')
    empleados = cursor.fetchall()
    conn.close()
    return empleados

def actualizar_empleado(id, nombre, apellido, salario_base, puesto):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE empleados SET nombre = ?, apellido = ?, salario_base = ?, puesto = ?
        WHERE id = ?
    ''', (nombre, apellido, salario_base, puesto, id))
    conn.commit()
    conn.close()

def eliminar_empleado(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE empleados SET activo = 0 WHERE id = ?', (id,))
    conn.commit()
    conn.close()

# Funciones para nóminas
def agregar_nomina(id_empleado, mes, salario_bruto, deducciones, impuestos):
    salario_neto = salario_bruto - deducciones - impuestos
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO nominas (id_empleado, mes, salario_bruto, deducciones, impuestos, salario_neto)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (id_empleado, mes, salario_bruto, deducciones, impuestos, salario_neto))
    conn.commit()
    conn.close()

def obtener_nominas_por_empleado(id_empleado):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM nominas WHERE id_empleado = ? ORDER BY mes DESC', (id_empleado,))
    nominas = cursor.fetchall()
    conn.close()
    return nominas

# Llama a create_tables() al importar el módulo
create_tables()