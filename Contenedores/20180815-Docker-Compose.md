Docker Compose
===

Referencias:
- [Documentación oficial Docker Compose](https://docs.docker.com/compose/)



Introducción
---
*Docker Compose* es una herramienta que permite definir y correr aplicaciones Docker multi-contentedor.

A medida que las aplicaciones son mas complejas, es razonable distribuirlas en múltiples contenedores. Por ej. aplicaciones basadas en microservicios son apropiadas para usar múltiples contenedores, un contenedor con una base de datos, otro con un servidor web, un sistema de mensajería en otro, etc., etc.
Crear estos contenedores en forma manual (*docker run*) resultará poco práctico y no es la mejor opción.

Con Docker Compose podemos definir nuestra aplicación multicontenedor utilizando un archivo de configuración, que contiene las definiciones de todos los contenedores que necesitamos, y con **un único comando podemos iniciar todos los contenedores**, con las relaciones entre ellos y en el orden indicado.

Este archivo de configuración, en formato *yaml*, no solo nos sirve para poder iniciar los contenedores, sino que también es útil como documentación de la aplicación, dado que incluye toda la información sobre sus contenedores, imágenes, volúmenes, networking, y el resto de las características.

Ejemplo de archivo de configuración *docker-compose.yml*:
```
version: '3'
services:
  web:
    build: .
    ports:
    - "5000:5000"
    volumes:
    - .:/code
    - logvolume01:/var/log
    links:
    - redis
  redis:
    image: redis
volumes:
  logvolume01: {}
```
Luego avanzaremos sobre los detalles de este archivo.



## Instalando Docker Compose

Docker Compose se puede instalar de varias formas, recomendamos realizar la instalación mediante una de estas dos alternativas.

Nota: Al momento de escribir este tutorial, instalar Docker Compose mediante *apt-get* nos ha dado problemas, dado que la versión instalada no soporta el archivo de configuración *version 3* que es el que utilizamos en este tutorial. Por tanto no recomendamos por el momento instalar de esta forma.



#### Alternativa 1: Instalación mediante *curl* 

```bash
sudo curl -L https://github.com/docker/compose/releases/download/1.22.0/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
```

Para instalar la última versión, en el comando anterior debemos indicar el último release disponible, el cual lo podemos ver aquí: [Compose repository release page on GitHub](https://github.com/docker/compose/releases).

Luego de finalizada la instalación debemos aplicar permiso de ejecución al binario:

```bash
sudo chmod +x /usr/local/bin/docker-compose
```



#### Alternativa 2: Instlación mediante *pip*

```bash
$ sudo pip install docker-compose
```



#### Verificación de la instalación:

```bash
$ docker-compose --version
docker-compose version 1.21.2, build 1719ceb
```



Ref.: [Instalación Docker Compose](https://docs.docker.com/compose/install/#install-compose)



