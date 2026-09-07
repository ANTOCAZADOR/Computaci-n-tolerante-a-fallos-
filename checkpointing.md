# Computación tolerante a fallas, checkpoint 

En el desarrollo de software tenemos algo importante para el manejo de los datos, que serían los backups. 

## ¿Para qué nos sirven los backups?

Los **backups** son respaldos de la base de datos que se hacen cada cierto tiempo, por ejemplo, en los bancos se suelen hacer backups de forma continua y en tiempo real, con el objetivo de que si existiera un error o por algún casual la base de datos se corrompe o se sufre algún ataque que encripte la información es necesario tener un backup. Estos mismos nos ayudarían a recuperar la información de la base de datos en su último momento antes de fallar o de estar comprometida, lo que nos permitiría tener acceso a los datos más actualizados. 

De esta manera podemos decir que funcionan los checkpoints, claro que dependiendo de la industria se les conoce de manera distinta, en los videojuegos solemos llamar a un punto de guardado como checkpoint, que es el lugar donde podemos cargar partida para continuar desde ahí en caso de perder o de salir del juego, pero en bases de datos se les conoce como backups. 

## Explicación del código checkpointing.py
En este código representé el flujo con un objeto JSON que originalmente recibe cuatro parámetros: id, producto, precio y stock. Guardamos esta información en la variable datos_actuales y seguidamente creamos un checkpoint en memoria (el backup).Para simular el fallo, eliminamos intencionalmente la columna precio. Al realizar una resta de conjuntos entre columnas_originales y columnas_actuales, la variable columnas_faltantes almacena los elementos eliminados (en este caso, { 'precio' }).En Python, cualquier colección o conjunto que no esté vacío se evalúa automáticamente como True. Por esta razón, el programa entra al bloque if, detecta el error, nos muestra qué columna hace falta y procede a cargar el backup restaurando el JSON a su estado inicial. Así es como simulamos un sistema de recuperación ante fallos.

## Conclusión: 
En conclusión, los checkpoints/backups son una pieza clave para la computación tolerante a fallas, ya que nos permite restaurar sistemas a un punto especifico en donde no estén fallando, para que la aplicación siga funcionando con completa normalidad, estos mismos son pieza clave y fundamental para crear sistemas escalables y sostenibles a largo plazo. 

