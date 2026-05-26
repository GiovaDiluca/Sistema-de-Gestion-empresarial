import os
import random
from datetime import datetime
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
from database import obtener_empresa  # Import config

def generar_pdf_recibo(empleado, periodo, fecha, data_nomina):
    # Crear directorio si no existe
    if not os.path.exists("comprobantes"):
        os.makedirs("comprobantes")
    
    nombre_limpio = empleado["nombre"].split("-")[-1].strip().replace(" ", "_")
    fecha_limpia = fecha.replace("/", "-").replace(":", "-").replace(" ", "_")
    
    filename = f"comprobantes/Recibo_{nombre_limpio}_{fecha_limpia}.pdf"
    
    # Formato horizontal para replicar ticket amplio
    c = canvas.Canvas(filename, pagesize=landscape(letter))
    width, height = landscape(letter)
    
    # Cargar datos de la empresa
    empresa_data = obtener_empresa()
    nombre_empresa = empresa_data.get("nombre", "EMPRESA DEMO, C.A") if empresa_data else "EMPRESA DEMO, C.A"
    rif_empresa = empresa_data.get("rif", "J-12345678-9") if empresa_data else "J-12345678-9"

    # ----------------------------------------------------
    # HEADER (EMPRESA)
    # ----------------------------------------------------
    logo_path = "assets/logo.png"
    if os.path.exists(logo_path):
        # Dibujar imagen en la esquina superior izquierda
        c.drawImage(logo_path, 1*cm, height - 2.5*cm, width=1.5*cm, height=1.5*cm, preserveAspectRatio=True, mask='auto')
        text_x = 3*cm
    else:
        text_x = 1*cm

    c.setFont("Helvetica-Bold", 11)
    c.drawString(text_x, height - 1.5*cm, nombre_empresa) 
    c.setFont("Helvetica", 9)
    c.drawString(text_x, height - 2*cm, f"R.I.F.: {rif_empresa}")
    
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(width/2, height - 1.8*cm, str(periodo).upper())
    
    c.setFont("Helvetica", 9)
    now = datetime.now()
    c.drawString(width - 6*cm, height - 1.5*cm, f"Usuario:          Admin")
    c.drawString(width - 6*cm, height - 2*cm, f"Fecha: {now.strftime('%d/%m/%Y')}   {now.strftime('%I:%M%p').lower()}")
    
    # ----------------------------------------------------
    # CAJA PERIODO
    # ----------------------------------------------------
    c.rect(1*cm, height - 3*cm, width - 2*cm, 0.6*cm)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(1.2*cm, height - 2.8*cm, f"Fecha:   {fecha}")
    c.drawString(7*cm, height - 2.8*cm, f"PERIODO DESDE:  {fecha}") 
    c.drawString(14*cm, height - 2.8*cm, f"HASTA:  {fecha}")
    c.drawString(21*cm, height - 2.8*cm, f"Nº Recibo:        {random.randint(1000,99999)}")
    
    # ----------------------------------------------------
    # CAJA TRABAJADOR
    # ----------------------------------------------------
    c.rect(1*cm, height - 4.2*cm, width - 2*cm, 1.2*cm)
    
    c.drawString(1.2*cm, height - 3.5*cm, "TRABAJADOR:")
    c.setFont("Helvetica", 9)
    c.drawString(3.8*cm, height - 3.5*cm, str(empleado.get("codigo", "")))
    c.drawString(5.5*cm, height - 3.5*cm, str(empleado.get("nombre", "")))
    
    c.setFont("Helvetica-Bold", 9)
    c.drawString(12*cm, height - 3.5*cm, "CEDULA:")
    c.setFont("Helvetica", 9)
    c.drawString(13.8*cm, height - 3.5*cm, str(empleado.get("cedula", "")))
    
    c.setFont("Helvetica-Bold", 9)
    c.drawString(17*cm, height - 3.5*cm, "CARGO:")
    c.setFont("Helvetica", 9)
    c.drawString(18.5*cm, height - 3.5*cm, str(empleado.get("cargo", ""))[:25])
    
    c.setFont("Helvetica-Bold", 9)
    c.drawString(1.2*cm, height - 4*cm, "SUELDO MENSUAL:")
    c.setFont("Helvetica", 9)
    c.drawString(4.5*cm, height - 4*cm, f"{empleado.get('sueldo', 0):.2f}")
    
    c.setFont("Helvetica-Bold", 9)
    c.drawString(7*cm, height - 4*cm, "DEPARTAMENTO:")
    c.setFont("Helvetica", 9)
    c.drawString(10*cm, height - 4*cm, str(empleado.get("departamento", "")))
    
    c.setFont("Helvetica-Bold", 9)
    c.drawString(14*cm, height - 4*cm, "C.C:")
    c.setFont("Helvetica", 9)
    c.drawString(15*cm, height - 4*cm, "033") 
    
    c.setFont("Helvetica-Bold", 9)
    c.drawString(17*cm, height - 4*cm, "FECHA DE INGRESO:")
    c.setFont("Helvetica", 9)
    c.drawString(20.5*cm, height - 4*cm, str(empleado.get("fecha_ingreso", "")))
    
    # ----------------------------------------------------
    # TABLA CABECERAS
    # ----------------------------------------------------
    y_table = height - 4.2*cm
    c.rect(1*cm, height - 4.8*cm, width - 2*cm, 0.6*cm) 
    
    col_x = [1*cm, 3*cm, 12*cm, 15.5*cm, 19*cm, 22.5*cm, width-1*cm]
    for x in col_x:
        c.line(x, height - 4.2*cm, x, height - 4.8*cm)
        
    c.setFont("Helvetica-Bold", 8)
    c.drawString(col_x[0] + 0.2*cm, height - 4.6*cm, "CODIGO")
    c.drawString(col_x[1] + 0.2*cm, height - 4.6*cm, "DESCRIPCION")
    c.drawString(col_x[2] + 0.2*cm, height - 4.6*cm, "VALOR AUXILIAR")
    c.drawString(col_x[3] + 0.2*cm, height - 4.6*cm, "ASIGNACIONES")
    c.drawString(col_x[4] + 0.2*cm, height - 4.6*cm, "DEDUCCIONES")
    c.drawString(col_x[5] + 0.2*cm, height - 4.6*cm, "NETO A COBRAR")
    
    # ----------------------------------------------------
    # TABLA CUERPO
    # ----------------------------------------------------
    y_body_top = height - 4.8*cm
    y_body_bot = 5*cm
    c.rect(1*cm, y_body_bot, width - 2*cm, y_body_top - y_body_bot)
    
    for x in col_x:
        c.line(x, y_body_top, x, y_body_bot)
    
    y = y_body_top - 0.5*cm
    c.setFont("Helvetica", 8)
    
    c.drawString(col_x[0] + 0.2*cm, y, "A001")
    c.drawString(col_x[1] + 0.2*cm, y, "Salario") # Or "Sueldo Base Calculado"
    c.drawRightString(col_x[4] - 0.2*cm, y, f"{data_nomina['sueldo']:,.2f}".replace(",","."))
    y -= 0.4*cm
    
    for idx, det in enumerate(data_nomina["detalles"]):
        c.drawString(col_x[0] + 0.2*cm, y, f"B{idx+1:03d}")
        c.drawString(col_x[1] + 0.2*cm, y, det["nombre"])
        
        if det["tipo"] == "ingreso":
            c.drawRightString(col_x[4] - 0.2*cm, y, f"{det['monto']:,.2f}".replace(",","."))
        else:
            c.drawRightString(col_x[5] - 0.2*cm, y, f"{det['monto']:,.2f}".replace(",","."))
            
        y -= 0.4*cm

    # ----------------------------------------------------
    # TOTALES
    # ----------------------------------------------------
    c.rect(1*cm, y_body_bot - 0.6*cm, width - 2*cm, 0.6*cm)
    c.line(col_x[3], y_body_bot, col_x[3], y_body_bot - 0.6*cm)
    c.line(col_x[4], y_body_bot, col_x[4], y_body_bot - 0.6*cm)
    c.line(col_x[5], y_body_bot, col_x[5], y_body_bot - 0.6*cm)
    
    c.setFont("Helvetica-Bold", 8)
    c.drawString(col_x[2] + 0.2*cm, y_body_bot - 0.4*cm, "Total Trabajador:")
    
    total_asign = data_nomina['sueldo'] + data_nomina['ingresos']
    total_deduc = data_nomina['deducciones']
    
    c.drawRightString(col_x[4] - 0.2*cm, y_body_bot - 0.4*cm, f"{total_asign:,.2f}".replace(",","."))
    c.drawRightString(col_x[5] - 0.2*cm, y_body_bot - 0.4*cm, f"{total_deduc:,.2f}".replace(",","."))
    c.drawRightString(col_x[6] - 0.2*cm, y_body_bot - 0.4*cm, f"{data_nomina['neto']:,.2f}".replace(",","."))
    
    # ----------------------------------------------------
    # FOOTER FIRMA Y BANCO
    # ----------------------------------------------------
    c.rect(1*cm, y_body_bot - 2.5*cm, width - 2*cm, 1.8*cm)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(1.2*cm, y_body_bot - 2*cm, "Recibí Conforme:")
    c.line(3.5*cm, y_body_bot - 2*cm, 10*cm, y_body_bot - 2*cm)
    
    c.line(10.5*cm, y_body_bot - 0.7*cm, 10.5*cm, y_body_bot - 2.5*cm)
    
    c.drawString(11*cm, y_body_bot - 1.2*cm, "BANCO:")
    c.setFont("Helvetica", 8)
    c.drawString(13*cm, y_body_bot - 1.2*cm, "OTROS BANCOS")
    
    c.setFont("Helvetica-Bold", 8)
    c.drawString(11*cm, y_body_bot - 2*cm, "CUENTA:")
    c.setFont("Helvetica", 8)
    c.drawString(13*cm, y_body_bot - 2*cm, "01000020002000000000") 
    
    c.save()
    return filename

def generar_pdf_contrato(nombre_empleado, texto_contrato):
    if not os.path.exists("comprobantes"):
        os.makedirs("comprobantes")
        
    nombre_limpio = nombre_empleado.split("-")[-1].strip().replace(" ", "_")
    filename = f"comprobantes/Contrato_{nombre_limpio}.pdf"
    
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(inch, height - inch, "CONTRATO DE TRABAJO")
    
    c.setFont("Helvetica", 12)
    y = height - 1.5 * inch
    
    # Simple line wrapping
    lineas = texto_contrato.split('\n')
    for linea in lineas:
        if not linea.strip():
            y -= 15
            continue
            
        palabras = linea.split(' ')
        linea_actual = ""
        for palabra in palabras:
            test_linea = f"{linea_actual} {palabra}".strip()
            # Approximation of text width limit for letter size: ~90 chars
            if len(test_linea) > 90:
                c.drawString(inch, y, linea_actual)
                y -= 15
                linea_actual = palabra
            else:
                linea_actual = test_linea
                
        if linea_actual:
            c.drawString(inch, y, linea_actual)
            y -= 15
            
        if y < inch:
            c.showPage()
            y = height - inch
            c.setFont("Helvetica", 12)
            
    c.save()
    return filename

