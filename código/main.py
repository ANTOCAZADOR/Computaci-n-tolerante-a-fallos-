import asyncio
import random

async def execute_with_fault_tolerance(operation, retries: int, delay_s: float, fallback_data):
    """
    Función tolerante a fallos que implementa reintentos automáticos y fallback.
    """
    attempt = 0

    while attempt < retries:
        try:
            # Intentamos ejecutar la operación principal
            result = await operation()
            return {"data": result, "source": "primary"}
        except Exception as e:
            attempt += 1
            print(f"⚠️ [Intento {attempt}/{retries}] Falló la operación. Error: {e}")
            
            if attempt >= retries:
                print("❌ Todos los intentos fallaron. Aplicando mecanismo de Fallback.")
                break
            
            # Espera asíncrona antes del siguiente intento
            await asyncio.sleep(delay_s)

    # Si todos los reintentos fallan, devuelve el estado de respaldo
    return {"data": fallback_data, "source": "fallback"}

# ==========================================
# Caso de Uso (Simulación)
# ==========================================

async def unstable_network_call():
    # Simulamos un 80% de probabilidad de fallo
    success = random.random() > 0.8 
    if not success:
        raise ConnectionError("Connection timeout")
    return ["Dato 1", "Dato 2", "Dato 3"]

async def main():
    print("Iniciando solicitud de datos...\n")
    
    cached_or_local_data = ["Dato Respaldo 1", "Dato Respaldo 2"]
    
    # Intentará 3 veces, esperando 1 segundo entre cada intento
    result = await execute_with_fault_tolerance(
        operation=unstable_network_call,
        retries=3,
        delay_s=1.0,
        fallback_data=cached_or_local_data
    )
    
    print("\n--- Resultado Final ---")
    print(f"Origen de los datos: {result['source']}")
    print(f"Datos obtenidos: {result['data']}")

# Punto de entrada de la aplicación
if __name__ == "__main__":
    asyncio.run(main())