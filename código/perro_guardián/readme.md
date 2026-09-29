# Propuesta del Escenario: Demonio "Watchdog" de Alta Disponibilidad

## Problema a resolver
En entornos de producción, los servicios críticos (como servidores web o APIs) pueden cerrarse abruptamente debido a excepciones no controladas, desbordamiento de memoria o picos de carga. Si el proceso muere, el servicio queda inaccesible para los usuarios.

## Por qué requiere ejecución en segundo plano
El monitor debe funcionar de manera desatendida y silenciosa, desvinculado de la interfaz principal del servicio, para garantizar que siga vigilando el sistema sin bloquear otros procesos del servidor.

## Qué tipo de falla podría ocurrir
Muerte inesperada del proceso principal (Crash). Esto simulado por una salida no planificada (`exit code != 0`).

## Qué estrategia de tolerancia se aplicará
Redundancia temporal y Recuperación automática. El demonio implementa un monitoreo continuo mediante un ciclo de tipo Watchdog. Si detecta que el hilo del proceso principal ha dejado de responder (falla *fail-stop*), inmediatamente lanza una nueva instancia del proceso, registrando el evento de caída y recuperación en una bitácora persistente. Además, maneja señales del sistema operativo (`SIGINT`, `SIGTERM`) para asegurar un apagado elegante (*graceful shutdown*), evitando dejar procesos zombies.