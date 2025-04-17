from flask import Flask, render_template
from datetime import datetime
import requests

app = Flask(__name__)

@app.route('/')
def home():
    actual = datetime.now()
    fecha_formateada = actual.strftime("%d de %B de %Y, %H:%M:%S")

    url = "https://gist.githubusercontent.com/reroes/502d11c95f1f8a17d300ece914464c57/raw/872172ebb60e22e95baf8f50e2472551f49311ff/gistfile1.txt"

    try:
        response = requests.get(url) # obtener una respuesta http en base a la url
        response.raise_for_status()
        contenido = response.text
        lineas = contenido.strip().split('\n')

        personas_filtradas = []
        primera_linea = True # ignorar encabezado

        for linea in lineas:
            if linea.strip():
                if primera_linea and "id" in linea.lower():
                    primera_linea = False
                    continue

                partes = linea.split('|')

                if len(partes) >= 5:
                    id_persona = partes[0].strip()
                    if id_persona.startswith(('3', '4', '5', '7')):
                        persona = { # se crea el diccionario
                            'id': id_persona,
                            'nombre': partes[1].strip(),
                            'apellido': partes[2].strip(),
                            'pais': partes[3].strip(),
                            'direccion': partes[4].strip()
                        }
                        personas_filtradas.append(persona) # se agrega a la lista

        return render_template('index.html', fecha=fecha_formateada, personas=personas_filtradas)

    except Exception as e:
        return f"Error al procesar el archivo: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
