from flask import Flask, render_template
from datetime import datetime
import requests

app = Flask(__name__)


@app.route('/')
def home():
    actual = datetime.now()
    fecha_formateada = actual.strftime("%d, %B, %Y, %H, %M, %S")

    url = "https://gist.githubusercontent.com/reroes/502d11c95f1f8a17d300ece914464c57/raw/872172ebb60e22e95baf8f50e2472551f49311ff/gistfile1.txt"

    try:
        response = requests.get(url)
        # response.status_code
        response.raise_for_status()

        contenido = response.text

        lineas = contenido.strip().split('\n')

        personas = []

        for linea in lineas:
            if linea.strip():
                partes = linea.split(';')
                if len(partes) >= 3:
                    id_persona = partes[0].strip()
                    # Verificar si el ID comienza con 3, 4, 5 o 7
                    if id_persona.startswith(('3', '4', '5', '7')):
                        nombre = partes[1].strip()
                        correo = partes[2].strip()
                        personas.append({
                            'id': id_persona,
                            'nombre': nombre,
                            'correo': correo
                        })

        return render_template('index.html',
                               fecha=fecha_formateada,
                               personas=personas)



    except Exception as e:
        return f"Error al procesar el archivo: {str(e)}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)