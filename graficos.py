import matplotlib.pyplot as plt
from analisis import agrupar_por_carrera
from conexion_sheets import obtener_datos

datos = obtener_datos()
resumen = agrupar_por_carrera(datos)


carreras = list(resumen.keys())
cantidad = list(resumen.values())
colores = ["#3B82F6", "#10B981", "#F59E0B", "#8B5CF6"]


plt.figure(figsize=(7, 4))
plt.bar(
    carreras, cantidad, color=colores[: len(carreras)], edgecolor="black"
)

plt.title("carrera eligidas", fontsize=14, fontweight="bold")
plt.xlabel("carreras")
plt.ylabel("cantidad")
plt.grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()


plt.figure(figsize=(6, 6))
plt.pie(
    cantidad,               # Reemplazamos cantidades por tus datos
    labels=carreras,        # Reemplazamos productos por tus carreras
    autopct="%1.1f%%",
    startangle=140,
    colors=colores[:len(carreras)],
)

# Esto crea el agujero blanco en el centro para que parezca una dona
circulo_centro = plt.Circle((0, 0), 0.60, fc="white")
fig = plt.gcf()
fig.gca().add_artist(circulo_centro)

# Título del gráfico
plt.title("2. Distribución Porcentual (%)", fontsize=14, fontweight="bold")

plt.tight_layout()
plt.show()