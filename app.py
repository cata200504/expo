from flask import Flask, jsonify, render_template
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Cargar el CSV
df = pd.read_csv("precios.csv")

# Función para limpiar valores de precio
def limpiar_precio(valor):
    try:
        valor = valor.replace("$", "").replace(",", "").strip()
        return int(valor)
    except:
        return None

# API que retorna los precios por producto
@app.route("/api/precios", methods=["GET"])
def obtener_precios():
    productos = df["PRODUCTO"].unique()
    resultados = {}

    for producto in productos:
        subset = df[df["PRODUCTO"] == producto].copy()
        semanas = []
        precios = []

        for _, fila in subset.iterrows():
            semana = fila["SEMANA"]
            valores = [limpiar_precio(fila[dia]) for dia in ["LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES"]]
            valores_validos = [v for v in valores if v is not None]
            if valores_validos:
                promedio = sum(valores_validos) / len(valores_validos)
                semanas.append(semana)
                precios.append(round(promedio, 2))

        resultados[producto] = {
            "semanas": semanas,
            "precios": precios
        }

    return jsonify(resultados)

# Ruta para servir la página HTML
@app.route("/")
def inicio():
    return render_template("index.html")

# Ejecutar el servidor
if __name__ == "__main__":
    print("✅ Servidor Flask arrancando en: http://127.0.0.1:8080")
    app.run(debug=True, host="127.0.0.1", port=8080)
