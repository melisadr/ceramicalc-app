import streamlit as st
import math
import matplotlib.pyplot as plt
import numpy as np
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO
from PIL import Image

CM_TO_PT = 28.3465  # Conversión cm → puntos

def calcular_patron_cono_truncado(diam_sup, diam_inf, altura):
    r_sup = diam_sup / 2
    r_inf = diam_inf / 2

    # Generatrices
    g_mayor = math.sqrt(altura**2 + r_sup**2)
    g_menor = math.sqrt(altura**2 + r_inf**2)

    # Ángulo usando la boca
    angulo_grados = (2 * math.pi * r_sup) / (2 * math.pi * g_mayor) * 360

    return g_mayor, g_menor, angulo_grados

def generar_patron_png(diam_sup, diam_inf, altura):
    g_mayor, g_menor, angulo_grados = calcular_patron_cono_truncado(diam_sup, diam_inf, altura)
    angulo_rad = math.radians(angulo_grados)

    fig, ax = plt.subplots(subplot_kw={'aspect': 'equal'})
    theta = np.linspace(0, angulo_rad, 300)

    # Arco exterior
    ax.plot(g_mayor*np.cos(theta), g_mayor*np.sin(theta), 'k')
    # Arco interior
    ax.plot(g_menor*np.cos(theta), g_menor*np.sin(theta), 'k')

    # Líneas radiales
    ax.plot([0, g_mayor], [0, 0], 'k')
    ax.plot([0, g_mayor*np.cos(angulo_rad)], [0, g_mayor*np.sin(angulo_rad)], 'k')

    ax.axis('off')

    buf = BytesIO()
    plt.savefig(buf, format="png", bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return buf, angulo_grados

def generar_patron_pdf(diam_sup, diam_inf, altura):
    g_mayor_cm, g_menor_cm, angulo_grados = calcular_patron_cono_truncado(diam_sup, diam_inf, altura)

    g_mayor = g_mayor_cm * CM_TO_PT
    g_menor = g_menor_cm * CM_TO_PT

    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=A4)
    width, height = A4
    c.translate(width / 2, height / 2)

    # Arcos del sector anular
    c.arc(-g_mayor, -g_mayor, g_mayor, g_mayor, startAng=0, extent=angulo_grados)
    c.arc(-g_menor, -g_menor, g_menor, g_menor, startAng=0, extent=angulo_grados)

    # Líneas radiales
    c.line(0, 0, g_mayor, 0)
    x2 = g_mayor * math.cos(math.radians(angulo_grados))
    y2 = g_mayor * math.sin(math.radians(angulo_grados))
    c.line(0, 0, x2, y2)

    # Etiquetas
    c.setFont("Helvetica", 10)
    c.drawString(-g_mayor, -g_mayor - 20, f"Altura: {altura} cm")
    c.drawString(-g_mayor, -g_mayor - 35, f"Ø boca: {diam_sup} cm | Ø base: {diam_inf} cm")
    c.drawString(-g_mayor, -g_mayor - 50, f"Ángulo: {angulo_grados:.2f}°")

    c.showPage()
    c.save()
    pdf_buffer.seek(0)
    return pdf_buffer