import plotly.graph_objects as go
import pandas as pd

from analisis import (
    analizar_comentarios_criticos,
    analizar_soporte_convivencia,
    analizar_vulnerabilidad_conectividad,
    agrupar_por_tipo,
    contar_estudiantes,
    contar_apoderados,
    analizar_correos_institucionales
)

from conexion_sheets import obtener_datos

colores = ["#3B82F6", "#10B981", "#F59E0B", "#8B5CF6"]

# 1. GRÁFICO DE BARRAS: ALERTAS POR TIPO
def grafico_barras(datos):
    resumen = agrupar_por_tipo(datos)
    tipos = list(resumen.keys())
    cantidades = list(resumen.values())

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=tipos, y=cantidades,
        marker_color=[colores[i % len(colores)] for i in range(len(tipos))],
        text=cantidades, textposition="auto"
    ))
    # SE AGREGA MARGEN (margin) Y AUTOSIZE PARA EVITAR RECORTES
    fig.update_layout(
        title="1. Distribución de casos por tipo", 
        template="plotly_white", 
        height=400,
        autosize=True,
        margin=dict(l=40, r=40, t=60, b=80)  # Margen inferior aumentado para las etiquetas
    )
    return fig

# 2. GRÁFICO DE DONA: DISTRIBUCIÓN POR TIPO PORCENTUAL
def grafico_dona(datos):
    resumen = agrupar_por_tipo(datos)
    fig = go.Figure()
    fig.add_trace(go.Pie(labels=list(resumen.keys()), values=list(resumen.values()), hole=0.60, marker=dict(colors=colores)))
    fig.update_layout(title="2. Distribución porcentual por tipo", template="plotly_white", height=400)
    return fig

# 3. GRÁFICO DE BARRAS: COMENTARIOS CRÍTICOS VS SOPORTE FAMILIAR NúCLEO
def grafico_comentarios(datos):
    criticos_df = analizar_comentarios_criticos(datos)
    conteo_criticos = len(criticos_df) if isinstance(criticos_df, pd.DataFrame) else 0

    convivencia_df = analizar_soporte_convivencia(datos)
    conteo_convivencia = 0
    if not convivencia_df.empty and 'Estructura_Hogar' in convivencia_df.columns:
        fila_nucleo = convivencia_df[convivencia_df['Estructura_Hogar'] == 'Núcleo Familiar Directo']
        if not fila_nucleo.empty:
            conteo_convivencia = fila_nucleo['Porcentaje (%)'].values[0]

    categorias_analisis = ["Estudiantes Críticos (Cant.)", "Núcleo Familiar Directo (%)"]
    valores = [conteo_criticos, conteo_convivencia]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=categorias_analisis, y=valores, marker_color="#10B981", text=valores, textposition="auto"))
    # SE AGREGA MARGEN PREVENTIVO TAMBIÉN AQUÍ
    fig.update_layout(
        title="3. Análisis de Comentarios Críticos y Convivencia", 
        template="plotly_white", 
        height=400,
        autosize=True,
        margin=dict(l=40, r=40, t=60, b=80)
    )
    return fig

# 4. GRÁFICO DE DONA: VULNERABILIDAD Y CONECTIVIDAD
def grafico_categorias(datos):
    vulnerables = analizar_vulnerabilidad_conectividad(datos)
    conteo_vuln = len(vulnerables) if isinstance(vulnerables, list) else 0
    total_otros = max(0, len(datos) - conteo_vuln)

    fig = go.Figure()
    fig.add_trace(go.Pie(labels=["Alta Vulnerabilidad Digital", "Acceso Estable/Regular"], values=[conteo_vuln, total_otros], hole=0.60, marker=dict(colors=["#EF4444", "#10B981"])))
    fig.update_layout(title="4. Índice de Vulnerabilidad y Conectividad", template="plotly_white", height=400)
    return fig

# 5. KPI: TOTAL ESTUDIANTES
def grafico_total_estudiantes(datos):
    total = contar_estudiantes(datos)
    fig = go.Figure(go.Indicator(mode="number", value=total, title={"text": "Cantidad de Estudiantes", "font": {"size": 18}}, number={"font": {"color": "#3B82F6"}}))
    fig.update_layout(height=200, template="plotly_white")
    return fig

# 6. KPI: TOTAL APODERADOS
def grafico_total_apoderados(datos):
    total = contar_apoderados(datos)
    fig = go.Figure(go.Indicator(mode="number", value=total, title={"text": "Cantidad de Apoderados", "font": {"size": 18}}, number={"font": {"color": "#10B981"}}))
    fig.update_layout(height=200, template="plotly_white")
    return fig

def grafico_correos(datos):
    resumen_df = analizar_correos_institucionales(datos)
    
    etiquetas = resumen_df['Tipo_Correo'].tolist()
    valores = resumen_df['Cantidad'].tolist()

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=etiquetas,
        y=valores,
        marker_color="#8B5CF6",
        text=valores,
        textposition="auto"
    ))
    
    fig.update_layout(
        title="7. Distribución de Correos Institucionales vs Personales", 
        template="plotly_white", 
        height=400
    )
    return fig