import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

def generar_pdf_recibo(nombre_empleado, fecha, data_nomina):
    # Crear directorio si no existe
    if not os.path.exists("comprobantes"):
        os.makedirs("comprobantes")
    
    # Limpiar strings para que sirvan de nombre de archivo
    nombre_limpio = nombre_empleado.split("-")[-1].strip().replace(" ", "_")
    fecha_limpia = fecha.replace("/", "-").replace(":", "-").replace(" ", "_")
    
    filename = f"comprobantes/Recibo_{nombre_limpio}_{fecha_limpia}.pdf"
    
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    c.setFont("Helvetica-Bold", 18)
    c.drawString(inch, height - inch, "Recibo de Pago de Nómina")
    
    c.setFont("Helvetica", 12)
    c.drawString(inch, height - 1.5*inch, f"Empleado: {nombre_empleado}")
    c.drawString(inch, height - 1.8*inch, f"Fecha de Pago: {fecha}")
    c.drawString(inch, height - 2.1*inch, f"Sueldo Base Calculado: ${round(data_nomina['sueldo'], 2)}")
    
    # INGRESOS
    y = height - 2.6*inch
    c.setFont("Helvetica-Bold", 14)
    c.drawString(inch, y, "Ingresos")
    y -= 0.3*inch
    
    c.setFont("Helvetica", 12)
    total_ingresos = 0
    for d in data_nomina["detalles"]:
        if d["tipo"] == "ingreso":
            c.drawString(inch + 0.3*inch, y, f"{d['nombre']}")
            # Alinear a la derecha
            c.drawRightString(width - 2*inch, y, f"+ ${round(d['monto'], 2)}")
            total_ingresos += d["monto"]
            y -= 0.25*inch
            
    # DEDUCCIONES
    y -= 0.2*inch
    c.setFont("Helvetica-Bold", 14)
    c.drawString(inch, y, "Deducciones")
    y -= 0.3*inch
    
    c.setFont("Helvetica", 12)
    total_deducciones = 0
    for d in data_nomina["detalles"]:
        if d["tipo"] == "deduccion":
            c.drawString(inch + 0.3*inch, y, f"{d['nombre']}")
            # Alinear a la derecha
            c.drawRightString(width - 2*inch, y, f"- ${round(d['monto'], 2)}")
            total_deducciones += d["monto"]
            y -= 0.25*inch
            
    # TOTALES
    y -= 0.5*inch
    c.setFont("Helvetica-Bold", 14)
    c.drawString(inch, y, f"Total Ingresos:")
    c.drawRightString(width - 2*inch, y, f"${round(total_ingresos, 2)}")
    y -= 0.3*inch
    c.drawString(inch, y, f"Total Deducciones:")
    c.drawRightString(width - 2*inch, y, f"${round(total_deducciones, 2)}")
    
    y -= 0.5*inch
    c.setFont("Helvetica-Bold", 16)
    c.drawString(inch, y, f"NETO A PAGAR:")
    c.drawRightString(width - 2*inch, y, f"${round(data_nomina['neto'], 2)}")
    
    # Línea decorativa
    c.line(inch, y - 0.2*inch, width - 1.5*inch, y - 0.2*inch)
    
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

