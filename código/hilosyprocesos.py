import threading
import multiprocessing
import time

# ==========================================
# HILOS (I/O-Bound)
# Simula la descarga de archivos de internet
# ==========================================

def descargar_archivo(id_archivo, tiempo_espera):
    print(f"[Hilo] Iniciando descarga del archivo {id_archivo}...")
    # time.sleep simula la espera de una respuesta del servidor (I/O)
    time.sleep(tiempo_espera)
    print(f"[Hilo] Archivo {id_archivo} descargado con éxito.")

def demostracion_hilos():
    print("--- INICIANDO DEMOSTRACIÓN DE HILOS (I/O-Bound) ---")
    inicio = time.time()
    
    # Creamos una lista para guardar nuestros hilos
    hilos = []
    
    # Lanzamos 3 hilos concurrentes
    for i in range(1, 4):
        # Cada hilo simulará tardar 2 segundos en descargar
        hilo = threading.Thread(target=descargar_archivo, args=(i, 2))
        hilos.append(hilo)
        hilo.start() # Inicia la ejecución del hilo
        
    # Esperamos a que todos los hilos terminen antes de continuar
    for hilo in hilos:
        hilo.join()
        
    fin = time.time()
    print(f"Tiempo total con hilos: {fin - inicio:.2f} segundos.\n")

# ==========================================
# EJEMPLO CON PROCESOS (CPU-Bound)
# Simula cálculos matemáticos pesados
# ==========================================

def calculo_intensivo(id_proceso):
    print(f"[Proceso] Proceso {id_proceso} iniciando cálculos pesados...")
    # Un cálculo que exige mucho a la CPU
    resultado = sum(i * i for i in range(10_000_000))
    print(f"[Proceso] Proceso {id_proceso} finalizado (Resultado: {resultado}).")

def demostracion_procesos():
    print("--- INICIANDO DEMOSTRACIÓN DE PROCESOS (CPU-Bound) ---")
    inicio = time.time()
    
    # Creamos una lista para guardar nuestros procesos
    procesos = []
    
    # Lanzamos 3 procesos paralelos
    for i in range(1, 4):
        proceso = multiprocessing.Process(target=calculo_intensivo, args=(i,))
        procesos.append(proceso)
        proceso.start() # Inicia un nuevo proceso con su propia memoria y su propio GIL
        
    # Esperamos a que todos los procesos terminen
    for proceso in procesos:
        proceso.join()
        
    fin = time.time()
    print(f"Tiempo total con procesos paralelos: {fin - inicio:.2f} segundos.")


if __name__ == "__main__":
    demostracion_hilos()
    
    demostracion_procesos()