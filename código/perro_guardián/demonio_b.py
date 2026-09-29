import subprocess
import time
import logging
import signal
import sys

# 1. Registro persistente de eventos (Logging)
# Crea un archivo system_monitor.log donde se guardará todo el historial
logging.basicConfig(
    filename='system_monitor.log', 
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

proceso_a = None
demonio_activo = True

# 2. Manejo adecuado de señales del sistema
def apagado_seguro(sig, frame):
    """Atrapa señales como Ctrl+C o kill, y apaga todo limpiamente."""
    global demonio_activo, proceso_a
    nombre_senal = signal.Signals(sig).name
    
    print(f"\n[Demonio] Recibida señal {nombre_senal}. Iniciando apagado seguro...")
    logging.info(f"Señal de sistema {nombre_senal} interceptada. Apagando demonio.")
    
    demonio_activo = False # Rompe el ciclo principal
    
    # Si el proceso A sigue vivo, lo matamos de forma controlada
    if proceso_a is not None and proceso_a.poll() is None:
        print("[Demonio] Terminando Proceso A para evitar procesos zombies...")
        proceso_a.terminate()
        proceso_a.wait()
        
    logging.info("Apagado del sistema completado con éxito.")
    print("[Demonio] Apagado completo.")
    sys.exit(0)

def iniciar_proceso():
    """Ejecuta el proceso A en un subproceso usando el ejecutable actual de Python."""
    global proceso_a
    # Abrimos el proceso con sys.executable para evitar problemas de alias en Windows
    proceso_a = subprocess.Popen([sys.executable, "proceso_a.py"])
    logging.info(f"Proceso principal (A) iniciado con PID: {proceso_a.pid}")

def main():
    # Registrar la captura de señales
    signal.signal(signal.SIGINT, apagado_seguro)   # Ctrl+C
    signal.signal(signal.SIGTERM, apagado_seguro)  # Comando kill por defecto
    
    print("=== Demonio Monitor Iniciado (Presiona Ctrl+C para salir) ===")
    logging.info("--- NUEVA SESIÓN DEL DEMONIO INICIADA ---")
    
    iniciar_proceso()
    
    # 3. Implementación de monitoreo continuo
    while demonio_activo:
        time.sleep(2) # Intervalo de chequeo (Heartbeat)
        
        # .poll() devuelve None si el proceso sigue corriendo. 
        # Si devuelve un número, es el código de salida (murió).
        estado = proceso_a.poll()
        
        if estado is not None:
            # 4. Estrategia de Tolerancia a Fallas (Reinicio automático)
            mensaje_error = f"¡Falla detectada! Proceso A murió inesperadamente (Código: {estado})."
            print(f"\n[Demonio] {mensaje_error}")
            logging.error(mensaje_error)
            
            print("[Demonio] Aplicando tolerancia a fallas: Reiniciando proceso...")
            logging.info("Reiniciando Proceso A...")
            iniciar_proceso()

if __name__ == "__main__":
    main()