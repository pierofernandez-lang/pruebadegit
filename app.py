from flask import Flask, render_template
from conexion_sheets import obtener_datos
import pandas as pd

from analisis import (
    analizar_comentarios_criticos,
    analizar_soporte_convivencia,
    analizar_vulnerabilidad_conectividad,
    agrupar_por_tipo,
    contar_apoderados,
    contar_estudiantes,
    agrupar_correos_institucionales
)

from graficos import (
    grafico_barras,
    grafico_dona,
    grafico_comentarios,
    grafico_categorias,
    grafico_total_estudiantes,
    grafico_total_apoderados,
    grafico_correos
)

app = Flask(__name__)

@app.route("/")
def dashboard():
    datos = obtener_datos()

    total_registros = len(datos)
    total_estudiantes = contar_estudiantes(datos)
    total_apoderados = contar_apoderados(datos)

    # Procesamiento analítico adaptado a tus retornos reales
    comentarios_df = analizar_comentarios_criticos(datos)
    comentarios_criticos = len(comentarios_df) if isinstance(comentarios_df, pd.DataFrame) else 0
    
    convivencia_df = analizar_soporte_convivencia(datos)
    soporte_convivencia = len(convivencia_df)
    
    vulnerables_lista = analizar_vulnerabilidad_conectividad(datos)
    vulnerabilidad_conectividad = len(vulnerables_lista)

    resumen_tipo = agrupar_por_tipo(datos)
    total_por_tipo = sum(resumen_tipo.values()) if isinstance(resumen_tipo, dict) else 0

    correos_dicc = agrupar_correos_institucionales(datos)
    total_institucionales = correos_dicc.get('Institucional', 0)

    # Renderizado HTML de Gráficos de Plotly
    grafico1 = grafico_barras(datos).to_html(full_html=False, include_plotlyjs='cdn')
    grafico2 = grafico_dona(datos).to_html(full_html=False, include_plotlyjs=False)
    grafico3 = grafico_comentarios(datos).to_html(full_html=False, include_plotlyjs=False)
    grafico4 = grafico_categorias(datos).to_html(full_html=False, include_plotlyjs=False)
    grafico5 = grafico_total_estudiantes(datos).to_html(full_html=False, include_plotlyjs=False)
    grafico6 = grafico_total_apoderados(datos).to_html(full_html=False, include_plotlyjs=False)
    grafico7 = grafico_correos(datos).to_html(full_html=False, include_plotlyjs=False)

    return render_template(
        "dashboard.html",
        total_registros=total_registros,
        total_estudiantes=total_estudiantes,
        total_apoderados=total_apoderados,
        comentarios_criticos=comentarios_criticos,
        soporte_convivencia=soporte_convivencia,
        vulnerabilidad_conectividad=vulnerabilidad_conectividad,
        total_por_tipo=total_por_tipo,
        total_institucionales=total_institucionales,
        grafico1=grafico1, grafico2=grafico2, grafico3=grafico3,
        grafico4=grafico4, grafico5=grafico5, grafico6=grafico6,
        grafico7=grafico7
    )

if __name__ == "__main__":
    app.run(debug=True)