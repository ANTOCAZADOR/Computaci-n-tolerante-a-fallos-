import copy
import json

# 1. Cargamos el JSON original (Simulación)
json_datos = """
{
    "id": 101,
    "producto": "Laptop Gamer",
    "precio": 1500,
    "stock": 25
}
"""

datos_actuales = json.loads(json_datos)

print("JSON original cargado con éxito:")
print(json.dumps(datos_actuales, indent=4, ensure_ascii=False))

# 2. Creamos el Checkpoint (Backup idéntico en memoria)
checkpoint_backup = copy.deepcopy(datos_actuales)
print("\n Checkpoint guardado con éxito")


# 3. Simulamos el error: Alguien borra una columna requerida
print("\n Ocurre un error: Se elimina la columna 'precio'")
if "precio" in datos_actuales:
    del datos_actuales["precio"]


# 4. Validamos/Comparamos para detectar el error
print("\n Validando los datos actuales contra el Checkpoint ")

columnas_originales = set(checkpoint_backup.keys())
columnas_actuales = set(datos_actuales.keys()) 

# Buscamos si falta alguna columna
columnas_faltantes = columnas_originales - columnas_actuales

if columnas_faltantes:
    print(
        f"\n¡ERROR DETECTADO! Faltan las siguientes columnas: {list(columnas_faltantes)} \n"
    )
    print(json.dumps(datos_actuales, indent=4, ensure_ascii=False))

    # 5. Cargamos el Backup / Restauramos el Checkpoint
    print("\n Cargando el Backup (Checkpoint) para solucionar el error")
    datos_actuales = copy.deepcopy(checkpoint_backup)

    print("\n Estado restaurado correctamente:")
    print(json.dumps(datos_actuales, indent=4, ensure_ascii=False))
else:
    print("Todo está correcto. No se requiere restaurar el backup.")
