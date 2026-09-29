import time
import random
import sys
import os

def main():
    print(f"[Proceso A - PID {os.getpid()}] Iniciando servicio principal...")
    
    ciclos = 0
    while True:
        time.sleep(2) # Simula tiempo de procesamiento
        ciclos += 1
        print(f"[Proceso A] Trabajando normalmente... (Ciclo {ciclos})")
        
        # Simular una falla aleatoria (20% de probabilidad en cada ciclo)
        if random.random() < 0.20:
            print(f"[{time.strftime('%X')}] ERROR FATAL: Desbordamiento de memoria simulado. El Proceso A va a colapsar.")
            sys.exit(1) # El código 1 indica que terminó con error

if __name__ == "__main__":
    main()