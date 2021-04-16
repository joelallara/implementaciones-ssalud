# implementaciones-ssalud

Aplicación web desarrollada por iniciativa propia para la empresa en la que actualmente trabajo, utilizando el framework Django. La misma se conecta a una base de datos SQL y se encuentra implementada sobre IIS.
El objetivo de la aplicación es el de mantener un registro de cambios realizados sobre proyectos SSIS, donde el autor de los mismos debe cargar una solicitud indicando el Proyecto, Paquete, Tarea y una pequeña descripción.
La solicitud dispara un mail a los usuarios “implementadores”, quienes se encargan de implementar los cambios de test a producción. Estos usuarios cuentan con un “Panel de implementaciones” en el cual visualizan los pendientes, y una vez implementados los cambios, deben ingresar un LSN(log sequence number) que, al confirmar, dispara un mail para el usuario que cargó la solicitud, informando que ya se encuentra en producción.
La aplicación cuenta con un script (BuscadorSSIS.py) que recorre una unidad compartida donde se encuentran los proyectos, para obtener sus archivos dtsx, copiarlos localmente, convertirlos en XML y recorrerlos en búsqueda de los nombres de los Paquetes y Tareas para actualizar esta info en la base de datos.
Además, la aplicación cuenta con un “Buscador SQL” que permite a los desarrolladores identificar en qué tareas se encuentra una fracción de código, permitiendo minimizar tiempos de detección del impacto del cambio a realizar.

