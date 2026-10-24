import gspread

def obtener_datos():
    cliente = gspread.service_account(
        filename="credenciales.json"
    )
    archivo = cliente.open("Formulario para Entrevistas (respuestas)")
    hoja = archivo.sheet1
    datos = hoja.get_all_records()

    return datos

if __name__ == "__main__":

    cliente = gspread.service_account(filename="credenciales.json")

    archivo = cliente.open("Formulario para Entrevistas (respuestas)")
    print("¡Conexión exitosa!")

    print(f"Título de la hoja: {archivo.title}")

    datos = obtener_datos()

    print(f"Datos recuperados correctamente. Total de filas: {len(datos)}")
