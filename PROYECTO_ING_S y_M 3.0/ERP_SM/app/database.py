import sqlite3
import os
import pandas as pd

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'database.db')


# =========================
# CONEXIÓN
# =========================
def get_connection():
    return sqlite3.connect(DB_PATH)


# =========================
# CREAR TABLAS
# =========================
def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # EMPLEADOS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS empleados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            cedula TEXT,
            telefono TEXT,
            email TEXT,
            nivel TEXT,
            puesto TEXT,
            salario_base REAL,
            fecha_ingreso TEXT,
            activo INTEGER DEFAULT 1
        )
    ''')

    # NOMINA
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nominas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_empleado INTEGER,
            mes TEXT,
            salario_bruto REAL,
            deducciones REAL,
            impuestos REAL,
            salario_neto REAL,
            FOREIGN KEY (id_empleado) REFERENCES empleados(id)
        )
    ''')

    conn.commit()
    conn.close()


# =========================
# CRUD EMPLEADOS
# =========================
def agregar_empleado(nombre, apellido, cedula, telefono, email,
                     nivel, puesto, salario_base, fecha_ingreso):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO empleados
        (nombre, apellido, cedula, telefono, email, nivel, puesto, salario_base, fecha_ingreso)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (nombre, apellido, cedula, telefono, email, nivel, puesto, salario_base, fecha_ingreso))

    conn.commit()
    conn.close()


def obtener_empleados():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM empleados WHERE activo = 1")
    data = cursor.fetchall()

    conn.close()
    return data


def eliminar_empleado(id_emp):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE empleados SET activo = 0 WHERE id = ?", (id_emp,))

    conn.commit()
    conn.close()


# =========================
# IMPORTAR EXCEL
# =========================
def importar_empleados_excel(ruta_excel):

    try:
        df = pd.read_excel(ruta_excel)
    except Exception as e:
        return {
            "insertados": 0,
            "duplicados": 0,
            "errores": f"No se pudo leer el archivo: {e}"
        }

    # ============================
    # Normalizar nombres columnas
    # ============================
    df.columns = df.columns.str.strip().str.lower()
    df.columns = df.columns.str.replace(" ", "_")

    columnas_requeridas = [
        'nombre', 'apellido', 'cedula',
        'telefono', 'email', 'nivel',
        'puesto', 'salario_base', 'fecha_ingreso'
    ]

    for col in columnas_requeridas:
        if col not in df.columns:
            return {
                "insertados": 0,
                "duplicados": 0,
                "errores": f"Falta la columna obligatoria: {col}"
            }

    conn = get_connection()
    cursor = conn.cursor()

    insertados = 0
    duplicados = 0

    try:
        conn.execute("BEGIN")

        for _, row in df.iterrows():

            # Saltar filas completamente vacías
            if pd.isna(row['cedula']):
                continue

            cedula = str(row['cedula']).strip()

            # Verificar duplicado por cédula
            cursor.execute(
                "SELECT id FROM empleados WHERE cedula = ?",
                (cedula,)
            )

            if cursor.fetchone():
                duplicados += 1
                continue

            try:
                cursor.execute('''
                    INSERT INTO empleados
                    (nombre, apellido, cedula, telefono, email,
                     nivel, puesto, salario_base, fecha_ingreso)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    str(row['nombre']).strip(),
                    str(row['apellido']).strip(),
                    cedula,
                    str(row['telefono']).strip(),
                    str(row['email']).strip(),
                    str(row['nivel']).strip(),
                    str(row['puesto']).strip(),
                    float(row['salario_base']),
                    str(row['fecha_ingreso'])
                ))

                insertados += 1

            except Exception as e:
                print("Error insertando fila:", e)
                continue

        conn.commit()

    except Exception as e:
        conn.rollback()
        conn.close()
        return {
            "insertados": 0,
            "duplicados": 0,
            "errores": f"Error durante la importación: {e}"
        }

    conn.close()

    return {
        "insertados": insertados,
        "duplicados": duplicados,
        "errores": None
    }
    
# =========================
# ELIMINAR EMPLEADOS
# =========================

def eliminar_empleado(empleado_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM empleados WHERE id = ?", (empleado_id,))
    
    conn.commit()
    conn.close()
    
# =========================
# ACTUALIZAR EMPLEADOS
# =========================   


def actualizar_empleado(id_empleado, nombre, apellido, cedula,
                         telefono, email, nivel, puesto,
                         salario_base, fecha_ingreso):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE empleados
        SET nombre=?, apellido=?, cedula=?, telefono=?,
            email=?, nivel=?, puesto=?, salario_base=?, fecha_ingreso=?
        WHERE id=?
    """, (
        nombre, apellido, cedula, telefono,
        email, nivel, puesto, salario_base,
        fecha_ingreso, id_empleado
    ))

    conn.commit()
    conn.close()