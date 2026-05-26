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
    
        # CONCEPTOS (INGRESOS / DEDUCCIONES)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conceptos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            tipo TEXT CHECK(tipo IN ('ingreso', 'deduccion')) NOT NULL,
            valor REAL NOT NULL,
            es_porcentaje INTEGER DEFAULT 0
        )
    ''')

    # DETALLE DE NOMINA (TRAZABILIDAD)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nomina_detalle (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_nomina INTEGER,
            id_concepto INTEGER,
            monto REAL,
            FOREIGN KEY (id_nomina) REFERENCES nominas(id),
            FOREIGN KEY (id_concepto) REFERENCES conceptos(id)
        )
    ''')    
            

        # EMPLEADOS
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS empleados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                cedula TEXT UNIQUE,
                telefono TEXT,
                email TEXT,
                nivel TEXT,
                puesto TEXT,
                salario_base REAL,
                fecha_ingreso TEXT,
                activo INTEGER DEFAULT 1
            )
        ''')

        # NOMINA (MEJORADA)
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS nominas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_empleado INTEGER,
                fecha TEXT,
                dias_trabajados INTEGER,
                bonificaciones REAL,
                deducciones REAL,
                total_pago REAL,
                FOREIGN KEY (id_empleado) REFERENCES empleados(id)
            )
        ''')

        # CONFIGURACION EMPRESA
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS configuracion_empresa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            rif TEXT NOT NULL,
            direccion TEXT,
            telefono TEXT
        )
    ''')
    
    # Initialize with default if empty
    cursor.execute("SELECT COUNT(*) FROM configuracion_empresa")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO configuracion_empresa (nombre, rif, direccion, telefono) VALUES ('EMPRESA DEMO, C.A', 'J-12345678-9', '', '')")

    conn.commit()
    conn.close()
    
# =========================
# CONCEPTOS (CRUD PRO)
# =========================

def agregar_concepto(nombre, tipo, valor, es_porcentaje):
    if tipo not in ("ingreso", "deduccion"):
        raise ValueError("Tipo inválido")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO conceptos (nombre, tipo, valor, es_porcentaje)
        VALUES (?, ?, ?, ?)
    """, (nombre, tipo, valor, es_porcentaje))

    conn.commit()
    conn.close()


def obtener_conceptos():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM conceptos ORDER BY tipo, nombre")
    data = cursor.fetchall()

    conn.close()
    return data


def actualizar_concepto(id_concepto, nombre, tipo, valor, es_porcentaje):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE conceptos
        SET nombre=?, tipo=?, valor=?, es_porcentaje=?
        WHERE id=?
    """, (nombre, tipo, valor, es_porcentaje, id_concepto))

    conn.commit()
    conn.close()


def eliminar_concepto(id_concepto):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM conceptos WHERE id=?", (id_concepto,))
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


# ✅ ELIMINACIÓN LÓGICA (PROFESIONAL)
def eliminar_empleado(empleado_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE empleados SET activo = 0 WHERE id = ?", (empleado_id,))

    conn.commit()
    conn.close()


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

            if pd.isna(row['cedula']):
                continue

            cedula = str(row['cedula']).strip()

            cursor.execute("SELECT id FROM empleados WHERE cedula = ?", (cedula,))
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
# NOMINA (NUEVO MÓDULO)
# =========================

def obtener_salario(id_empleado):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT salario_base FROM empleados WHERE id = ?", (id_empleado,))
    result = cursor.fetchone()

    conn.close()

    return result[0] if result else 0

# =========================
# CONFIGURACION EMPRESA
# =========================
def obtener_empresa():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM configuracion_empresa LIMIT 1")
    data = cursor.fetchone()
    conn.close()
    if data:
        return {
            "id": data[0],
            "nombre": data[1],
            "rif": data[2],
            "direccion": data[3],
            "telefono": data[4]
        }
    return {"nombre": "EMPRESA DEMO, C.A", "rif": "J-12345678-9", "direccion": "", "telefono": ""}

def actualizar_empresa(nombre, rif, direccion, telefono):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if exists
    cursor.execute("SELECT COUNT(*) FROM configuracion_empresa")
    count = cursor.fetchone()[0]
    
    if count > 0:
        cursor.execute("""
            UPDATE configuracion_empresa
            SET nombre=?, rif=?, direccion=?, telefono=?
            WHERE id=(SELECT min(id) FROM configuracion_empresa)
        """, (nombre, rif, direccion, telefono))
    else:
        cursor.execute("""
            INSERT INTO configuracion_empresa (nombre, rif, direccion, telefono)
            VALUES (?, ?, ?, ?)
        """, (nombre, rif, direccion, telefono))
        
    conn.commit()
    conn.close()

