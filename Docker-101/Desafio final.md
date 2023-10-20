# Desafío final

![alt desafio_final](desafio_final.png)

## Objetivo

El objetivo del desafío final es elaborar la topología que se muestra en la figura mas arriba utilizando `docker-compose` y ponerla a correr en el servidor utilizado para los laboratorios.

Una vez que esta topología esté corriendo, se debe acceder mediante un navegador web a la url del servidor: http://servernumx.labs.conatest.click. Esto desplegará una página como sigue:

![alt desafio_final](desafio_index.png)

Dentro del cuadro de texto, se debe pegar el contenido del archivo `docker-compose.yml` que se utilizó para levantar la aplicación y hacer click en "Aceptar". Esto enviará el contenido del cuadro de texto al grupo de `Webex Teams` que se está utilizando identificando el mensaje como proveniente del "grupox" tomando el dato de la variable de entorno `GRUPO` configurada en `appserver2`.

Si todo sale bien, además de recibirse el mensaje en el grupo de `Webex Teams` se debería desplegar la siguiente página:

![alt desafio_final](desafio_success.png)

## Requerimientos:

### Usuario Webex Team

Deben registarse como usuario en [Cisco Webex Teams](https://teams.webex.com/signin), con la misma dirección de correo que utilziaron para el curso.

Serán agregados a un grupo de teams (room), cuyo nombre indicará el instructor durante el curso. Prueben que pueden enviar mensaje a dicho grupo, desde la página de Cisco Webex Teams.

Ese mismo grupo es el que deben utilizar en el desafío final, en la variable de entorno `ROOM`.


### API Webex Teams

Para obtener la api se debe ingresar con un usuario registrado de Cisco a:

https://developer.webex.com/docs/getting-started

![Token de API](webexapi.png)
