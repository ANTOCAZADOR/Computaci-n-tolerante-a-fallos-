# Comprendiendo Hilos y Procesos en Python

Este documento explica la lógica detrás del código de simulación de concurrencia y paralelismo en Python. El objetivo principal del script es demostrar, de manera práctica, las diferencias entre el uso del módulo `threading` (hilos) y el módulo `multiprocessing` (procesos), así como el impacto del **GIL (Global Interpreter Lock)**.

## 1. Simulación de Hilos (I/O-Bound)

La primera parte del código utiliza el módulo `threading`. 

### ¿Por qué se hizo así?
* **Simulación de Espera (`time.sleep`)**: En lugar de hacer una descarga real que depende de tu conexión a internet, usamos `time.sleep(2)`. Para el procesador de una computadora, esperar a que un servidor remoto envíe datos (operación de Entrada/Salida o *I/O*) es idéntico a "dormir". 
* **Aprovechamiento del tiempo muerto**: Al lanzar 3 hilos, el programa no espera a que termine el primero para iniciar el segundo. Mientras el Hilo 1 "duerme" (espera la respuesta del servidor), Python cambia el contexto y arranca el Hilo 2, y luego el Hilo 3.
* **El resultado**: Tres descargas de 2 segundos cada una terminan en un tiempo total de aproximadamente **2 segundos**, en lugar de los 6 segundos que tomaría si se hicieran una tras otra (secuencialmente).

## 2. Simulación de Procesos (CPU-Bound)

La segunda parte del código utiliza el módulo `multiprocessing`.

### ¿Por qué se hizo así?
* **Cálculos pesados en lugar de esperas**: Aquí definimos la función `calculo_intensivo`, que realiza una suma de millones de números. Esto mantiene a la CPU trabajando al 100% (tarea *CPU-bound*), sin tiempos muertos.
* **El problema del GIL**: Si intentáramos ejecutar esta matemática pesada usando `threading`, Python no nos dejaría hacerlas al mismo tiempo. El **GIL** actúa como un candado que asegura que solo un hilo ejecute instrucciones de Python a la vez. En tareas de CPU, los hilos terminarían estorbándose y el tiempo total sería igual o peor que hacerlo secuencialmente.
* **La solución (`multiprocessing`)**: Al usar procesos en lugar de hilos, el sistema operativo crea copias completamente nuevas del programa. Cada proceso tiene su propio espacio de memoria y, lo más importante, **su propio GIL**. Esto permite que la computadora distribuya cada proceso a un núcleo físico diferente del procesador, logrando un verdadero *paralelismo*.

## 3. Elementos Clave del Código

Para que el ejemplo funcione correctamente y de forma didáctica, se implementaron dos mecánicas fundamentales:

### El uso de `.join()`
Tanto en la lista de `hilos` como en la de `procesos`, iteramos sobre ellos llamando al método `.join()`. 
* **¿Por qué?** Porque el programa principal (el hilo principal) se ejecuta muy rápido. Si no le decimos explícitamente "espera a que estos hilos/procesos terminen", el programa imprimiría el mensaje de "Tiempo total" en 0.001 segundos y luego se cerraría abruptamente, matando las descargas o cálculos a la mitad. `.join()` actúa como una barrera de sincronización.

### La guarda `if __name__ == "__main__":`
* **¿Por qué?** Es un requisito de seguridad del sistema operativo (especialmente en Windows) al usar `multiprocessing`. Cuando Python crea un nuevo proceso, vuelve a importar el archivo original. Si no ocultamos la ejecución principal detrás de esta condición, el nuevo proceso intentaría crear más subprocesos de forma infinita, provocando un error en el sistema.

## Conclusión
* Usa **Hilos (`threading`)** cuando tu programa pase mucho tiempo esperando cosas externas (red, leer/escribir archivos, bases de datos).
* Usa **Procesos (`multiprocessing`)** cuando tu programa necesite hacer muchos cálculos matemáticos o procesamiento de datos masivo.