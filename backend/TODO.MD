1. Ver como manejar los proyectos en logfire para que solo los devs de ese proyecto los puedan ver y como hacerles llegar, ya sea por mail la invitacion, lo mismo para infisical
2. Agregar poder subir audio o video a un proyecto para que te genere los tickets de jira identificando nuevas funcionalidades o correcciones

COSAS A TENER EN CUENTA: Jira se puede crear siempre y cuando exista un dominio y usuario
debemos generar un api-key de ese usuario, deberiamos tmb mandar la invitacion al jira a los devs

INFRA -> Crean los recursos en amazon, agregan las variables de entorno en infisical -> el back las consume solo cuando estamos en dev, despues las lee del entorno normal
y yo desde aca si necesito una nueva variable o cambiar una variable lo puedo hacer sin tener que mandar mail a infra (necesitaria un user AWS ID para poder hacerlo)
