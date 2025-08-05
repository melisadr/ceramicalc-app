from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import math

def generar_patron_cono_truncado(diametro_superior, diametro_inferior, altura, filename="patron_cono.pdf"):
    r1 = diametro_inferior / 2
    r2 = diametro_superior / 2
    h = altura

    # Calcular generatrices
    g1 = math.sqrt(h**2 + r1**2)
    g2 = math.sqrt(h**2 + r2**2)

    # Ángulo para el desarrollo (en radianes)
    angulo = 2 * math.pi * r1 / (g1 - g2)
    angulo_grados = math.degrees(angulo)

    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    cx, cy = width / 2, height / 2

    # Dibujar desarrollo del cono truncado
    c.translate(cx, cy)
    c.setLineWidth(1)

    # Arco exterior
    c.arc(-g1, -g1, g1, g1, startAng=0, extent=angulo_grados)
    # Arco interior
    c.arc(-g2, -g2, g2, g2, startAng=0, extent=angulo_grados)

    # Líneas radiales
    c.line(0, 0, g1, 0)
    x = g1 * math.cos(math.radians(angulo_grados))
    y = g1 * math.sin(math.radians(angulo_grados))
    c.line(0, 0, x, y)

    # Agregar etiquetas
    c.drawString(-g1, -g1 - 20, f"Altura: {h} cm")
    c.drawString(-g1, -g1 - 35, f"Ø superior: {diametro_superior} cm | Ø base: {diametro_inferior} cm")

    c.showPage()
    c.save()
