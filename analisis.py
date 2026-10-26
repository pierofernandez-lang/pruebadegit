from conexion_sheets import obtener_datos

## JENNYFER ##
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_colwidth', 20)  # Evita que las celdas se amontonen en el centro

# funcion para analizar comentarios
def analizar_comentarios_criticos(archivo_csv='respuestas_entrevistas.csv'):
    # Detecta si recibe los datos directamente de Google Sheets o un archivo CSV
    if isinstance(archivo_csv, list):
        df = pd.DataFrame(archivo_csv)
    elif isinstance(archivo_csv, pd.DataFrame):
        df = archivo_csv
    else:
        df = pd.read_csv(archivo_csv)
    
    # Palabras clave asociadas a problemas profundos
    palabras_alerta = ['salud', 'enfermo', 'trabaja', 'dinero', 'economi', 'distancia', 'lejos', 'tiempo', 'falta', 'computadora', 'pc']
    
    casos_especiales = []
    
    for idx, row in df.iterrows():
        comentario = str(row.iloc[12]).lower()
        factores = str(row.iloc[11]).lower()
        texto_completo = comentario + " " + factores
        
        alertas_encontradas = [palabra for palabra in palabras_alerta if palabra in texto_completo]
        
        # Si el comentario contiene palabras de alerta o no es una respuesta simple como "No" o "Ninguno"
        if alertas_encontradas and comentario not in ['no', 'ninguno', 'no.', 'ninguna', 'nan']:
            casos_especiales.append({
                'Estudiante': row.iloc[1],
                'Apoderado': row.iloc[2],
                'Relación': row.iloc[4],
                'Factores de Riesgo declarados': row.iloc[11],
                'Comentario Abierto': row.iloc[12],
                'Foco de Alerta': ", ".join(alertas_encontradas)
            })
            
    df_alertas_texto = pd.DataFrame(casos_especiales)
    
    print(f"Se han detectado {len(df_alertas_texto)} estudiantes con comentarios que requieren revisión cualitativa inmediata.\n")
    print(df_alertas_texto)
    return df_alertas_texto

## JENNYFER ##
def analizar_vulnerabilidad_conectividad(datos):
    print("\n" + "="*60)
    print(" 📊 FUNCIÓN 2: CLASIFICACIÓN DE ALTA VULNERABILIDAD DIGITAL")
    print("="*60)
    
    # Convertimos los datos a un DataFrame temporal para usar las posiciones fijas de tu Apps Script
    df_temp = pd.DataFrame(datos)
    vulnerables = []
    
    for idx, row in df_temp.iterrows():
        # Sincronizado restando 1 a las columnas correspondientes de tu Apps Script
        internet = str(row.iloc[9]).lower()
        pc = str(row.iloc[8]).lower()
        alumno = row.iloc[1] if pd.notna(row.iloc[1]) else 'Desconocido'
        
        # Evaluamos condiciones desfavorables combinadas
        es_net_debil = 'inalámbrico' in internet or 'móvil' in internet or 'datos' in internet
        es_pc_compartida = 'comparte' in pc or 'no' in pc
        
        if es_net_debil and es_pc_compartida:
            vulnerables.append({
                'estudiante': alumno,
                'internet': row.iloc[9],
                'pc': row.iloc[8]
            })
            
    pct_vulnerabilidad = (len(vulnerables) / len(df_temp)) * 100 if not df_temp.empty else 0
    print(f"Porcentaje de alumnos en vulnerabilidad digital: {pct_vulnerabilidad:.2f}%")
    
    if vulnerables:
        print("\nLista de alumnos con conexión inestable y equipo compartido:")
        for v in vulnerables:
            print(f" 🔴 Alumno: {v['estudiante']} | Red: {v['internet']}")
    else:
        print(" ✅ Todos los estudiantes cuentan con infraestructuras estables o exclusivas.")
    return vulnerables

def analizar_soporte_convivencia(dataframe):
    """
    Analiza la estructura de convivencia del estudiante para medir el
    núcleo de apoyo familiar directo reportado en la entrevista.
    """
    # Detecta si recibe una lista de Google Sheets y la convierte a DataFrame
    if isinstance(dataframe, list):
        dataframe = pd.DataFrame(dataframe)
        
    col_vive = '¿Con quiénes vive el estudiante actualmente?'
    
    def categorizar_entorno(valor):
        valor = str(valor).lower()
        if 'madre y hermanos' in valor or 'padre y hermanos' in valor or 'padres' in valor:
            return 'Núcleo Familiar Directo'
        elif 'abuelos' in valor or 'tios' in valor or 'con sus tios' in valor:
            return 'Familia Extendida'
        elif 'solo' in valor:
            return 'Estudiante Independiente / Solo'
        else:
            return 'Otros / No especificado'


    df_analisis = dataframe.copy()
    # Sincronizado a la columna 11 de tu Apps Script (Índice 10 en Python)
    df_analisis['Estructura_Hogar'] = df_analisis.iloc[:, 10].apply(categorizar_entorno)
    
    # Agrupamos por estructura y calculamos el porcentaje del total
    resumen = df_analisis['Estructura_Hogar'].value_counts(normalize=True) * 100
    resumen_final = resumen.round(2).reset_index(name='Porcentaje (%)')
    print(resumen_final)
    return resumen_final

def agrupar_por_tipo(registros):
    resumen = {}
    for fila in registros:
        eleccion = fila.get("Tipo de Documento de Identidad", "")
        
        if eleccion == "DNI":
            if "DNI" not in resumen:
                resumen["DNI"] = 0
            resumen["DNI"] += 1
            
        elif "Carnet" in eleccion:
            if "Carnet de Extranjería" not in resumen:
                resumen["Carnet de Extranjería"] = 0
            resumen["Carnet de Extranjería"] += 1
            
    return resumen

def contar_estudiantes(registros):
    total = 0
    for registro in registros:
        estudiante = registro.get("Nombres y Apellidos Completos del Estudiante")
        
        if estudiante != "":
            total += 1
            
    return total

def contar_apoderados(registros):
    total = 0
    for registro in registros:
        apoderado = registro.get("Nombres y Apellidos Completos del Apoderado")
        
        if apoderado != "":
            total += 1
            
    return total

def agrupar_correos_institucionales(dataframe):
    # Solución de compatibilidad universal: convierte a DataFrame si viene como lista
    if isinstance(dataframe, list):
        dataframe = pd.DataFrame(dataframe)
        
    resumen = {}
    
    # Extraemos directamente los valores de la columna de correos (Índice 10)
    columna_correos = dataframe.iloc[:, 10].dropna()
    
    for celda in columna_correos:
        correo = str(celda).lower().strip()
        
        # Filtramos estrictamente por dominio de Valle Grande
        if "@vallegrande.edu.pe" in correo:
            if "Institucional" not in resumen:
                resumen["Institucional"] = 0
            resumen["Institucional"] += 1
            
    # Mostramos el resultado ordenado en consola
    print(resumen)
    return resumen


# =======================================================
#  BLOQUE DE EJECUCIÓN UNIFICADO AL FINAL DEL ARCHIVO
# =======================================================
if __name__ == "__main__":
    datos_hoja = obtener_datos()
    df_hoja = pd.DataFrame(datos_hoja)
    
    # Ejecución de las primeras 3 funciones analíticas
    analizar_comentarios_criticos(df_hoja)
    analizar_vulnerabilidad_conectividad(datos_hoja)
    analizar_soporte_convivencia(df_hoja)
    
    # Ejecución de la función 4 (Agrupación de documentos)
    resultado_tipo = agrupar_por_tipo(datos_hoja)
    print("\n--- RESUMEN DE DOCUMENTOS ---")
    print(resultado_tipo)
    
    # Ejecución de la función 5 (Contar estudiantes)
    resultado_estudiantes = contar_estudiantes(datos_hoja)
    print("\n--- CANTIDAD DE ESTUDIANTES ---")
    print(resultado_estudiantes)
    
    # Ejecución de la función 6 (Contar apoderados)
    resultado_apoderados = contar_apoderados(datos_hoja)
    print("\n--- CANTIDAD DE APODERADOS ---")
    print(resultado_apoderados)

    print("\n--- ANALISIS DE DOMINIOS DE CORREO ---")
    agrupar_correos_institucionales(datos_hoja)