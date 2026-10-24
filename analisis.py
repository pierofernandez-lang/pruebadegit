from conexion_sheets import obtener_datos

def agrupar_por_carrera(carreras):
    resumen = {}
    for carrera in carreras:
        eleccion = carrera["Carrera"]
        
        if eleccion == "Analisis de Sistemas Empresariales":
            if "Analisis de Sistemas Empresariales" not in resumen:
                resumen["Analisis de Sistemas Empresariales"] = 0
            resumen["Analisis de Sistemas Empresariales"] += 1
            
        elif eleccion == "Gestión Agricola":
            if "Gestión Agricola" not in resumen:
                resumen["Gestión Agricola"] = 0
            resumen["Gestión Agricola"] += 1
            
    return resumen

datos = obtener_datos()
resultado = agrupar_por_carrera(datos)
print("--- RESUMEN DE CARRERAS ---")
print(resultado)


def contar_apoderados(registros):
      total = 0
      for registro in registros:
           if registro ["Rol del Solicitante"]  == "Apoderado":
              total +=1
      return total

datos = obtener_datos()
resultado = contar_apoderados(datos)
print("--- CANTIDAD DE APODERADO ---")
print(resultado)
