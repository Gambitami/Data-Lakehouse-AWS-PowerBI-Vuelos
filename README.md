# ✈️ Data Lakehouse & BI: Monitor de Tráfico Aéreo (Sedes Mundialistas 2026)

**[📊 Haz clic aquí para interactuar con el Dashboard en vivo] ((https://app.powerbi.com/view?r=eyJrIjoiZjQ4OTI4MmUtOGEyMS00MDA1LWJlYjUtYzViZDhmNTgxOTBhIiwidCI6Ijc0YTRhM2JiLWQxNmYtNDQ5OC05MmExLTk4OTk1ZTIzODdhYSJ9))**
![Dashboard Preview](dashboard_preview.jpg)

## 📌 Descripción del Proyecto
Este proyecto es una arquitectura de datos **End-to-End** diseñada para extraer, procesar y visualizar telemetría en tiempo real de vuelos comerciales que sobrevuelan las tres ciudades sedes del Mundial 2026 en México (CDMX, Monterrey y Guadalajara). 

Demuestra habilidades en **Ingeniería de Datos** y **Business Intelligence**, implementando un flujo automatizado desde una API pública hasta un dashboard interactivo en la nube, utilizando servicios serverless de AWS.

## 🛠️ Arquitectura y Tecnologías (Tech Stack)
* **Fuente de Datos:** [OpenSky Network API](https://opensky-network.org/) (Telemetría de vuelos comerciales).
* **Ingesta (Capa Bronze):** Script en `Python` automatizado localmente (programador de tareas) extrayendo JSON y cargándolo en la nube mediante la librería `boto3`.
* **Almacenamiento (Data Lake):** `Amazon S3`. Particionado cronológico por día (estrategia Data Lake).
* **Transformación (Capa Silver):** `AWS Glue` (ETL). Limpieza de datos y conversión de formato crudo (JSON) a formato columnar optimizado (`Parquet`).
* **Motor de Consultas:** `Amazon Athena` (Serverless SQL) conectado al catálogo de Glue.
* **Visualización y Analytics:** `Power BI`. Conexión vía conector ODBC y actualización programada a través de Power BI Personal Gateway para sincronización híbrida (Nube-Local).

## 🚀 Flujo de Trabajo (Pipeline)
1. **Extracción:** Un script en Python escanea las coordenadas de las sedes mundialistas.
2. **Carga Inicial:** Los datos se depositan en S3 (`raw/fecha=YYYY-MM-DD/`).
3. **ETL:** Un Job de AWS Glue transforma y optimiza los datos, depositándolos en la capa `silver/`.
4. **Catálogo:** Amazon Athena actualiza las particiones (`MSCK REPAIR TABLE`).
5. **Reporte:** Power BI Service (Nube) consume la tabla procesada y se actualiza de forma programada.

## 🧠 Siguientes Pasos (Roadmap)
- [ ] Migrar el script local de ingesta (Python) a **AWS Lambda** y orquestarlo con **Amazon EventBridge** para una arquitectura 100% Serverless.
- [ ] Implementar validación de calidad de datos usando AWS Glue DataBrew o Great Expectations.

---
*Desarrollado por Amílcar Carrillo*
