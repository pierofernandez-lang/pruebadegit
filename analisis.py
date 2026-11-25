from conexion_sheets import obtener_datos
## JENNYFER ##
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option(
    'display.max_colwidth', 20
)  # Evita que las celdas se amontonen en el centro


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
  print('\n' + '=' * 60)
  print(' 📊 FUNCIÓN 2: CLASIFICACIÓN DE ALTA VULNERABILIDAD DIGITAL')
  print('=' * 60)

  # Convertimos los datos a un DataFrame temporal para usar las posiciones fijas de tu Apps Script
  df_temp = pd.DataFrame(datos)
  vulnerables = []

  for idx, row in df_temp.iterrows():
    # Sincronizado restando 1 a las columnas correspondientes de tu Apps Script
    internet = str(row.iloc).lower()
    pc = str(row.iloc).lower()
    alumno = row.iloc if pd.notna(row.iloc) else 'Desconocido'

    # Evaluamos condiciones desfavorables combinadas
    es_net_debil = (
        'inalámbrico' in internet or 'móvil' in internet or 'datos' in internet
    )
    es_pc_compartida = 'comparte' in pc or 'no' in pc

    if es_net_debil and es_pc_compartida:
      vulnerables.append(
          {'estudiante': alumno, 'internet': row.iloc, 'pc': row.iloc}
      )

  pct_vulnerabilidad = (
      (len(vulnerables) / len(df_temp)) * 100 if not df_temp.empty else 0
  )
  print(
      'Porcentaje de alumnos en vulnerabilidad digital:'
      f' {pct_vulnerabilidad:.2f}%'
  )

  if vulnerables:
    print('\nLista de alumnos con conexión inestable y equipo compartido:')
    for v in vulnerables:
      print(f" 🔴 Alumno: {v['estudiante']} | Red: {v['internet']}")
  else:
    print(
        ' ✅ Todos los estudiantes cuentan con infraestructuras estables o'
        ' exclusivas.'
    )
  return vulnerables


def analizar_soporte_convivencia(dataframe):
    """Analiza la estructura de convivencia del estudiante y su apoyo familiar."""
    cols_salida = ['Estructura_Hogar', 'Porcentaje (%)']
    
    try:
        df = pd.DataFrame(dataframe) if isinstance(dataframe, list) else dataframe
        
        if not isinstance(df, pd.DataFrame) or df.empty or df.shape[1] <= 10:
            raise ValueError("Datos inválidos, vacíos o con menos de 11 columnas.")


        def categorizar(valor):
            texto = "" if pd.isna(valor) else str(valor).lower().strip()
            if any(p in texto for p in ['madre y hermanos', 'padre y hermanos', 'padres']):
                return 'Núcleo Familiar Directo'
            if any(p in texto for p in ['abuelos', 'tios', 'tíos']):
                return 'Familia Extendida'
            return 'Estudiante Independiente / Solo' if 'solo' in texto else 'Otros / No especificado'


        categorias = df.iloc[:, 10].apply(categorizar)
        resumen = (categorias.value_counts(normalize=True) * 100).round(2).reset_index()
        resumen.columns = cols_salida
        
        print(resumen)
        return resumen


    except Exception as e:
        print(f"Error en analizar_soporte_convivencia: {e}")
        return pd.DataFrame(columns=cols_salida)
  
def agrupar_por_tipo(registros):
  if registros is None:
    raise ValueError("No se recibieron datos de Google Sheets.")

  resumen = {}

  for numero, fila in enumerate(registros, start=1):
    try:
      # Usamos corchetes [] para que salte KeyError si la columna no existe
      eleccion = fila["Tipo de Documento de Identidad"]

      # Validamos que el dato sea texto (si viene un número o None salta TypeError)
      if not isinstance(eleccion, str):
        raise TypeError("El tipo de documento debe ser un texto.")

      eleccion = eleccion.strip()

      # Regla de negocio: el campo no puede estar vacío ni ser un documento no permitido
      if eleccion == "":
        raise ValueError("El campo 'Tipo de Documento de Identidad' está vacío.")

      if eleccion == "DNI":
        if "DNI" not in resumen:
          resumen["DNI"] = 0
        resumen["DNI"] += 1

      elif "Carnet" in eleccion:
        if "Carnet de Extranjería" not in resumen:
          resumen["Carnet de Extranjería"] = 0
        resumen["Carnet de Extranjería"] += 1

      else:
        raise ValueError(f"Tipo de documento no válido: '{eleccion}'")

    except KeyError as e:
      print(f"Registro {numero}: falta el campo {e}")

    except ValueError as e:
      print(f"Registro {numero}: valor incorrecto - {e}")

    except TypeError as e:
      print(f"Registro {numero}: tipo de dato incorrecto - {e}")

  return resumen


# FUNCIÓN 2: CONTAR ESTUDIANTES CON MANEJO DE ERRORES
def contar_estudiantes(registros):
  if registros is None:
    raise ValueError('No se recibieron datos de Google Sheets.')

  total = 0

  for numero, registro in enumerate(registros, start=1):
    try:
      # Limpiamos espacios invisibles de los nombres de las columnas por seguridad
      registro_limpio = {k.strip(): v for k, v in registro.items()}

      estudiante = registro_limpio[
          'Nombres y Apellidos Completos del Estudiante'
      ]

      # Validamos que sea una cadena de texto
      if not isinstance(estudiante, str):
        raise TypeError('El nombre del estudiante debe ser un texto.')

      estudiante = estudiante.strip()

      # Regla de negocio: no contar nombres vacíos ni compuestos solo por números
      if estudiante == '':
        raise ValueError('El nombre del estudiante está vacío.')

      if estudiante.isdigit():
        raise ValueError(
            f"El nombre '{estudiante}' no puede ser solo números."
        )

      total += 1

    except KeyError as e:
      print(f'Registro {numero}: falta el campo {e}')

    except ValueError as e:
      print(f'Registro {numero}: valor incorrecto - {e}')

    except TypeError as e:
      print(f'Registro {numero}: tipo de dato incorrecto - {e}')

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
if __name__ == '__main__':
  datos_hoja = obtener_datos()
  df_hoja = pd.DataFrame(datos_hoja)

  # Ejecución de las primeras 3 funciones analíticas
  resultado_comentarios = analizar_comentarios_criticos(df_hoja)
  print('\n--- COMENTARIOS CRÍTICOS ---')
  print(resultado_comentarios)

  analizar_vulnerabilidad_conectividad(datos_hoja)
  analizar_soporte_convivencia(df_hoja)

  # Ejecución de la función 4 (Agrupación de documentos)
  resultado_tipo = agrupar_por_tipo(datos_hoja)
  print('\n--- RESUMEN DE DOCUMENTOS ---')
  print(resultado_tipo)

  # Ejecución de la función 5 (Contar estudiantes)
  resultado_estudiantes = contar_estudiantes(datos_hoja)
  print('\n--- CANTIDAD DE ESTUDIANTES ---')
  print(resultado_estudiantes)

  # Ejecución de la función 6 (Contar apoderados)
  resultado_apoderados = contar_apoderados(datos_hoja)
  print('\n--- CANTIDAD DE APODERADOS ---')
  print(resultado_apoderados)

  print('\n--- ANALISIS DE DOMINIOS DE CORREO ---')
  agrupar_correos_institucionales(datos_hoja)
