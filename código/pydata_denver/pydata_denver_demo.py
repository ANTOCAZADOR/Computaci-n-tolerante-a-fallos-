import requests
import json
from collections import namedtuple
from contextlib import closing
import sqlite3

from prefect import task, Flow

## 1. EXTRACT (Extracción)
@task
def get_complaint_data(estado, cantidad):
    print(f"-> Extrayendo {cantidad} quejas del estado de {estado}...")
    # Agregamos los parámetros 'state' y 'size' a la API
    params = {'state': estado, 'size': cantidad}
    r = requests.get("https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/", params=params)
    response_json = json.loads(r.text)
    return response_json['hits']['hits']

## 2. TRANSFORM (Transformación)
@task
def parse_complaint_data(raw):
    print("-> Transformando y limpiando los datos...")
    complaints = []
    Complaint = namedtuple('Complaint', ['date_received', 'state', 'product', 'company', 'complaint_what_happened'])
    
    for row in raw:
        source = row.get('_source')
        descripcion = source.get('complaint_what_happened')
        
        # LIMPIEZA: Si la queja no tiene descripción, le ponemos un texto por defecto
        if not descripcion:
            descripcion = "Sin descripción proporcionada por el usuario"
            
        this_complaint = Complaint(
            date_received=source.get('date_received'),
            state=source.get('state'),
            product=source.get('product'),
            company=source.get('company'),
            complaint_what_happened=descripcion
        )
        complaints.append(this_complaint)
        
    print(f"-> Se procesaron {len(complaints)} quejas.")
    return complaints

## 3. LOAD (Carga)
@task
def store_complaints(parsed):
    print("-> Guardando los datos en la base de datos SQLite...")
    create_script = 'CREATE TABLE IF NOT EXISTS complaint (timestamp TEXT, state TEXT, product TEXT, company TEXT, complaint_what_happened TEXT)'
    insert_cmd = "INSERT INTO complaint VALUES (?, ?, ?, ?, ?)"

    with closing(sqlite3.connect("cfpbcomplaints.db")) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.executescript(create_script)
            cursor.executemany(insert_cmd, parsed)
            conn.commit()
            
    print("-> ¡Proceso ETL completado con éxito!")

# ORQUESTACIÓN DEL FLUJO
# Aquí le pasamos los parámetros que queremos buscar
estado_a_buscar = "TX" # TX = Texas
cantidad_a_buscar = 20

with Flow("ETL_Quejas_Financieras") as f:
    raw = get_complaint_data(estado_a_buscar, cantidad_a_buscar)
    parsed = parse_complaint_data(raw)
    store_complaints(parsed)

# Ejecutar el flujo
f.run()