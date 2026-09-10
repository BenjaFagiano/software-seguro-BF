* Informe Lab
  - Aldeas inseguras
    Primero realizo un envío a cada una de las Aldeas de oro, para poder obtener el ID de cada aldea. Una vez que obtengo el ID, cierro sesión y vuelvo a iniciar el juego. Primero realizo un envío a una aldea para poder obtener la petición POST donde se modifica el id_origen y id_destino; Como cada aldea puede recibir una sola vez al día oro, envío primero todo el oro de la aldea A a la B, luego todo el oro de la Aldea B a la aldea C y por último la cantidad completa de oro de la aldea C a la Aldea de Pedro.

  - Gran Rifa 2019
    Primero antes de realizar el login, abrir el DevTools para obtener el ID de "John Backus" en la petición GET numeros/. Una vez identificado el ID procedo a "Editar" una de las rifas desde el Front-end y luego "Guardar" para obtener la petición POST editar/, desde ahí se envía {"esta_pago": true} los que realiza el cambio a Esta Pago = SI

  - Presupuesto
    Primero antes de realizar el login, abrir el DevTools 
    Consulto la petición GET /api/gastos/ para obtener ID, Montos y Tipo de Gastos
    Desde el Front-end hacer click en el botón revisar para obtener la petición POST /api/gastos/1/editar/
    Identificar los ID a modificar y empezar primero por el Promedio de gastos varios, modificando el ID y Montos en la petición POST
    Seguir por el Promedio de gastos esenciales
    Finalmente realizar las modificaciones con la petición POST para el Gasto promedio total
  
  - Turnero
    Primero antes de realizar el login, abrir el DevTools 
    Consulto la petición GET /api/1/appointments/ para obtener el ID del usuario "xdalvik"
    Se realiza prueba y modificación del ID en GET /api/1/appointments/ hasta encontrar al usuario en /api/101/appointments/
    Una vez identificados los turnos, ejecutar la petición DELETE:
      - /api/appointments/10
      - /api/appointments/11
      - /api/appointments/12
      - /api/appointments/13
  
  - Ventas
