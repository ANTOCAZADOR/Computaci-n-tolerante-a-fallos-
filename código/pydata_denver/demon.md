# README - Actualización del Proceso ETL

Este documento describe las modificaciones y mejoras realizadas al script original del proceso ETL (Extraer, Transformar, Cargar) que consume datos de la API de quejas financieras.

## Modificaciones Implementadas

### 1. Extracción (Extract) - Parametrización
* **Antes:** El script estaba limitado ("hardcodeado") a obtener siempre 10 resultados aleatorios.
* **Mejora:** Se agregaron parámetros a la función `get_complaint_data(estado, cantidad)`. 
* **Beneficio:** Ahora el código es flexible y permite consultar fácilmente las quejas de un estado específico (ej. "TX" para Texas) y ajustar el tamaño de la muestra sin modificar la lógica interna de la petición HTTP.

### 2. Transformación (Transform) - Limpieza de Datos
* **Antes:** Si la API devolvía un registro sin el campo de descripción de la queja, se guardaba como un valor vacío o nulo.
* **Mejora:** Se implementó una regla de negocio para validar la existencia del texto. Si el campo `complaint_what_happened` viene vacío, se asigna automáticamente el valor: *"Sin descripción proporcionada por el usuario"*.
* **Beneficio:** Aumenta la calidad de los datos al evitar valores nulos (Data Cleaning) y estandariza la información que llegará a la base de datos. (También se corrigió un error tipográfico en la variable `date_received`).

### 3. Carga (Load) - Observabilidad
* **Antes:** El script se ejecutaba de manera silenciosa, dificultando saber en qué paso se encontraba o si había fallado a la mitad.
* **Mejora:** Se agregaron mensajes de consola (`print`) estratégicos al inicio de cada tarea y al finalizar el guardado en la base de datos SQLite.
* **Beneficio:** Mejora el monitoreo del proceso. En el contexto de sistemas y computación tolerante a fallas, tener visibilidad (observabilidad) de la ejecución paso a paso permite identificar rápidamente dónde ocurre un error en caso de que el sistema falle.