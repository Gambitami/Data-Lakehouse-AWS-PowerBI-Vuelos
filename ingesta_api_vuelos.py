import json
import requests
import boto3
from datetime import datetime

def ingestar_vuelos_sedes():
    # 1. Definir las tres cajas precisas para el Mundial 2026
    # La caja de Guadalajara ha sido ajustada y centrada en el aeropuerto
    cajas_sedes = {
        "Monterrey": {"lamin": 25.0, "lamax": 26.0, "lomin": -101.0, "lomax": -99.5},
        "Guadalajara": {"lamin": 19.5, "lamax": 21.5, "lomin": -104.5, "lomax": -102.0},
        "CDMX": {"lamin": 19.0, "lamax": 20.0, "lomin": -100.0, "lomax": -98.5}
    }

    vuelos_totales = []
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    timestamp_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("Iniciando escaneo focalizado de sedes mundialistas...")
    print("-" * 50)

    # 2. Consultar cada caja por separado
    for sede, coords in cajas_sedes.items():
        print(f"Consultando espacio aéreo de {sede}...")
        url = f"https://opensky-network.org/api/states/all?lamin={coords['lamin']}&lamax={coords['lamax']}&lomin={coords['lomin']}&lomax={coords['lomax']}"

        try:
            respuesta = requests.get(url, timeout=10)
            respuesta.raise_for_status()
            datos_api = respuesta.json()

            vuelos_sede_actual = 0 # Contador individual para el diagnóstico

            if datos_api and datos_api.get('states'):
                for vuelo in datos_api['states']:
                    # Filtrar vuelos que no tengan coordenadas válidas desde la extracción
                    if vuelo[5] is not None and vuelo[6] is not None:
                        registro = {
                            "icao24": vuelo[0],
                            "callsign": str(vuelo[1]).strip() if vuelo[1] else "Desconocido",
                            "origin_country": vuelo[2],
                            "longitude": vuelo[5],
                            "latitude": vuelo[6],
                            "altitude": vuelo[7],
                            "velocity": vuelo[9],
                            "date_updated": timestamp_actual,
                            "fecha": fecha_actual
                        }
                        vuelos_totales.append(registro)
                        vuelos_sede_actual += 1
            
            # Print de diagnóstico para evaluar el tráfico por ciudad
            print(f" > Vuelos encontrados en {sede}: {vuelos_sede_actual}")

        except Exception as e:
            print(f" > Error al consultar la API para {sede}: {e}")

    print("-" * 50)

    # 3. Guardar en formato JSONL y subir a Amazon S3
    if vuelos_totales:
        hora_actual = datetime.now().strftime("%H%M%S")
        nombre_archivo = f"vuelos_mundial_{hora_actual}.json"

        # Escribir el archivo localmente en formato JSON Lines (JSONL) para Athena
        with open(nombre_archivo, 'w') as f:
            for vuelo in vuelos_totales:
                f.write(json.dumps(vuelo) + '\n')

        try:
            print(f"Subiendo archivo a Data Lake en S3...")
            s3 = boto3.client('s3')
            bucket_name = 'vuelos-mundial-data-lake-amicp'
            ruta_s3 = f"raw/fecha={fecha_actual}/{nombre_archivo}"

            s3.upload_file(nombre_archivo, bucket_name, ruta_s3)
            print(f"¡Éxito! {len(vuelos_totales)} vuelos focalizados subidos a s3://{bucket_name}/{ruta_s3}")
        except Exception as e:
            print(f"Error al subir a S3: {e}")
    else:
        print("No se encontraron vuelos comerciales activos en las 3 sedes en este momento.")

if __name__ == "__main__":
    ingestar_vuelos_sedes()