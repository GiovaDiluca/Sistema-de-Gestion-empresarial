from database import get_connection, obtener_salario

# =========================
# CALCULAR NOMINA (AVANZADO)
# =========================
def calcular_nomina(id_empleado, dias_trabajados):

    salario_base = obtener_salario(id_empleado)
    salario_diario = salario_base / 30
    sueldo = salario_diario * dias_trabajados

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nombre, tipo, valor, es_porcentaje
        FROM conceptos
    """)
    conceptos = cursor.fetchall()
    conn.close()

    total_ingresos = 0
    total_deducciones = 0
    detalles = []

    for c in conceptos:
        id_c, nombre, tipo, valor, es_porcentaje = c

        if es_porcentaje:
            monto = sueldo * (valor / 100)
        else:
            monto = valor

        detalles.append({
            "concepto_id": id_c,
            "nombre": nombre,
            "tipo": tipo,
            "monto": monto
        })

        if tipo == "ingreso":
            total_ingresos += monto
        else:
            total_deducciones += monto

    salario_neto = sueldo + total_ingresos - total_deducciones

    return {
        "sueldo": sueldo,
        "ingresos": total_ingresos,
        "deducciones": total_deducciones,
        "neto": salario_neto,
        "detalles": detalles
    }


# =========================
# GUARDAR NOMINA
# =========================
def guardar_nomina(id_empleado, fecha, dias_trabajados):

    data = calcular_nomina(id_empleado, dias_trabajados)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO nominas
        (id_empleado, fecha, dias_trabajados, bonificaciones, deducciones, total_pago)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        id_empleado,
        fecha,
        dias_trabajados,
        data["ingresos"],
        data["deducciones"],
        data["neto"]
    ))

    nomina_id = cursor.lastrowid

    for d in data["detalles"]:
        cursor.execute("""
            INSERT INTO nomina_detalle (id_nomina, id_concepto, monto)
            VALUES (?, ?, ?)
        """, (nomina_id, d["concepto_id"], d["monto"]))

    conn.commit()
    conn.close()