Docker Compose
===

Ref.: [Documentación oficial Docker Compose](https://docs.docker.com/compose/)



Introducción
---
*Docker Compose* es una herramienta que permite definir y correr aplicaciones Docker multi-contentedor.

A medida que las aplicaciones son mas complejas, es razonable distribuirlas en múltiples contenedores. Por ej. aplicaciones basadas en microservicios son apropiadas para usar múltiples contenedores, un contenedor con una base de datos, otro con un servidor web, un sistema de mensajería en otro, etc., etc.
Crear estos contenedores en forma manual (*docker run*) resultará poco práctico y no es la mejor opción.

Con Docker Compose podemos definir nuestra aplicación multicontenedor utilizando un archivo de configuración, que contiene las definiciones de todos los contenedores que necesitamos, y con **un único comando podemos iniciar todos los contenedores**, con las relaciones entre ellos y en el orden indicado.

Este archivo de configuración, en formato *yaml*, no solo nos sirve para poder iniciar los contenedores, sino que también es útil como documentación de la aplicación, dado que incluye toda la información sobre sus contenedores, imágenes, volúmenes, networking, y el resto de las características.



## Instalando Docker Compose

Docker Compose se puede instalar de varias formas, recomendamos realizar la instalación mediante una de estas dos alternativas.

Nota: Al momento de escribir este tutorial, instalar Docker Compose mediante *apt-get* nos ha dado problemas, dado que la versión instalada no soporta el archivo de configuración *version 3* que es el que utilizamos en este tutorial. Por tanto no recomendamos por el momento instalar de esta forma.



#### Alternativa 1: Instalación mediante *curl*

```bash
$ sudo curl -L https://github.com/docker/compose/releases/download/1.22.0/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
```

Para instalar la última versión, en el comando anterior debemos indicar el último release disponible, el cual lo podemos ver aquí: [Compose repository release page on GitHub](https://github.com/docker/compose/releases).

Luego de finalizada la instalación debemos aplicar permiso de ejecución al binario:

```bash
$ sudo chmod +x /usr/local/bin/docker-compose
```



#### Alternativa 2: Instlación mediante *pip*

```bash
$ sudo pip install docker-compose
```



#### Verificación de la instalación:

```bash
$ sudo docker-compose --version
docker-compose version 1.21.2, build 1719ceb
```



Ref.: [Instalación Docker Compose](https://docs.docker.com/compose/install/#install-compose)





## Configuración: archivo *docker-compose.yml*

Docker Compose se basa en la utilización de un archivo de configuración en formato *yml*, donde vamos a indicar todo el ambiente que queremos crear, incluyendo las imagenes de contenedores que vamos a desplegar con su configuración (variables de entorno, volumenes de disco, etc.), cómo se van a configurar las redes, y las dependencias entre contenedores.

Las dependencias permiten no solo crear los contenedores en determinado orden, sino que además, si un contenedor depende de otro, el *contendor hijo* no será creado hasta que el *contenendor padre* exista y esté corriendo.

Este archivo no solo permite especificar toda la creación de nuestro ambiente, también podemos usarlo para eliminar nuestro ambiente una vez que ya no lo necesitamos, y es una fuenta de documentación muy precisa sobre el mismo.

Si bien el nombre del archivo puede ser cualquiera, el nombre por defecto a utilizar es *docker-compose.yml*, si utilizmos otro nombre debemos pasar como referencia el mismo en los comandos que utilizaremos para crear y bajar nuestro ambiente.

Ref.: [Compose file version 3 reference](https://docs.docker.com/compose/compose-file/)



## Desplegando nuestro ambiente

Para entender como se realiza el despliegue de los contonedores, realizaremos el siguiente ejercicio.

En el mismo vamos a crear un ambiente con dos contenedores, uno con *wordpress* y el otro con la base de datos requerida por el primero.



#### Ejercicio 20:

1. Crear un directorio para nuestro proyecto.

   Este directorio debería contar únicamente con los elementos necesarios para el ambiente que vamos a crear. Si bien en este caso tendría unicamente el archivo *docker-compse.yml* podríamos incluir aquí dentro cualquier otro recurso necesario (ej. dockerfiles). Esto nos permite tener toda la documentación específica de nuestro proyecto, y actualizada.

   ```bash
   $ mkdir my_wordpress
   $ cd my_wordpress
   ```



2. Crear el archivo *docker-compose.yml* con el siguiente contenido:

   ```bash
   version: '3.3'
   
   services:
      db:
        image: mysql:5.7
        volumes:
          - db_data:/var/lib/mysql
        restart: always
        environment:
          MYSQL_ROOT_PASSWORD: somewordpress
          MYSQL_DATABASE: wordpress
          MYSQL_USER: wordpress
          MYSQL_PASSWORD: wordpress
   
      wordpress:
        depends_on:
          - db
        image: wordpress:latest
        ports:
          - "8000:80"
        restart: always
        environment:
          WORDPRESS_DB_HOST: db:3306
          WORDPRESS_DB_USER: wordpress
          WORDPRESS_DB_PASSWORD: wordpress
   volumes:
       db_data:
   
   ```



***DUDA: Ya incluimos los volumenes en este ejemplo? o lo dejamos para que lo descubran solos en el desafío final???**



3. Realizar el despliegue, mediante el comando  `docker-compose up -d` desde el directorio que creamos, que contiene el archivo *docker-compose.yml*.

   Como ya hemos visto, si no tenemos las imagenes almacenadas localmente, las descargará del repositorio desde [dockerhub](https://hub.docker.com/).

   

   ```bash
   $ sudo docker-compose up -d
   Creating volume "my_wordpress_db_data" with default driver
   Pulling db (mysql:5.7)...
   5.7: Pulling from library/mysql
   be8881be8156: Already exists
   c3995dabd1d7: Pull complete
   9931fdda3586: Downloading [================>                                  ]  1.522MB/4.499MB
   bb1b6b6eff6a: Download complete
   a65f125fa718: Download complete
   2d9f8dd09be2: Downloading [=====>                                             ]  1.293MB/12.09MB
   37b912cb2afe: Waiting
   faf9da46e0cf: Waiting
   ...
   ...
   ...
   02243b284270: Pull complete
   Digest: sha256:e25e2768e910223db3095c1560aa2255371986b24fbebf4b015bae3cc60b9b34
   Status: Downloaded newer image for mysql:5.7
   Pulling wordpress (wordpress:latest)...
   latest: Pulling from library/wordpress
   be8881be8156: Already exists
   69a25f7e4930: Pull complete
   ...
   ...
   ...
   61b17faecc30: Pull complete
   c85ae8a39ff7: Pull complete
   Digest: sha256:d92a0d4e9aae885789af8538bb8afe8624c23cb5d763dcc1d3a2e4ac57531d21
   Status: Downloaded newer image for wordpress:latest
   Creating my_wordpress_db_1 ... done
   Creating my_wordpress_wordpress_1 ... done
   ```

   

   La opción `-d` hace que el deploy corra en segundo plano, ejcutando como servicio. Si no ponemos esta opción el comando quedará en primer plano, y si lo cortamos (ctrl-c) detendrá la ejecución de todos los contenedores generados. El no utilizar la opción  `-d` puede ser útil en algunos casos, dado que nos muestra al momento de ejecutar el comando la salida de stderr, que podría indicarnos mensajes de error o warnings derivados del proceso de levante de los propios containers.

   

4. Una vez finalizado el despliegue, podemos verificar si los dos contenedores están corriendo:

   ```bash
   $ sudo docker ps
   CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                  NAMES
   8e8771bccefe        wordpress:latest    "docker-entrypoint..."   5 minutes ago       Up 5 minutes        0.0.0.0:8000->80/tcp   my_wordpress_wordpress_1
   8724f78e61a0        mysql:5.7           "docker-entrypoint..."   5 minutes ago       Up 5 minutes        3306/tcp, 33060/tcp    my_wordpress_db_1
   ```



​	Y además podemos acceder al servicio wordpress desde un navegador:

**DUDA: ESTO FUNCIONA DESDE AWS ???**



![alt text](Imagenes/wordpress.png)



Y también podemos ver que tenemos las nuevas imagenes que fueron descargadas en forma local:

```bash
$ sudo docker images
REPOSITORY            TAG                 IMAGE ID            CREATED             SIZE
wordpress             latest              e2c4085bbc2b        2 days ago          408MB
mysql                 5.7                 43b029b6b640        2 days ago          372MB
...
...
```



5. Para detener los contenedores en forma ordenada, lo hacemos mediante el comando  `docker-compose down` desde el directorio que creamos, que contiene el archivo *docker-compose.yml*.

   ```bash
   $ sudo docker-compose down
   Stopping my_wordpress_wordpress_1 ... done
   Stopping my_wordpress_db_1        ... done
   Removing my_wordpress_wordpress_1 ... done
   Removing my_wordpress_db_1        ... done
   Removing network my_wordpress_default
   ```

   

   Podemos ver que los contenedores ya no se encuentra corriendo:

   ```bash
   $ sudo docker ps
   CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
   
   ```

   

   Y las imagenes que fueron descargadas durante el proces de despliegue, siguen estando almacenadas localmente:

   ```bash
   $ sudo docker images 
   REPOSITORY            TAG                 IMAGE ID            CREATED             SIZE
   wordpress             latest              e2c4085bbc2b        2 days ago          408MB
   mysql                 5.7                 43b029b6b640        2 days ago          372MB
   ...
   ```

   

   Por lo tanto si realizaramos el despliegue nuevamente con  `docker-compose up -d` , el proceso será muy rápido:

   ```bash
   $ sudo docker-compose up -d
   Creating network "my_wordpress_default" with the default driver
   Creating my_wordpress_db_1 ... done
   Creating my_wordpress_wordpress_1 ... done
   
   
   $ sudo docker ps -a
   CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                  NAMES
   a4e556375891        wordpress:latest    "docker-entrypoint..."   3 seconds ago       Up 2 seconds        0.0.0.0:8000->80/tcp   my_wordpress_wordpress_1
   83fb7904980c        mysql:5.7           "docker-entrypoint..."   4 seconds ago       Up 3 seconds        3306/tcp, 33060/tcp    my_wordpress_db_1
   
   
   $ sudo docker-compose down
   Stopping my_wordpress_wordpress_1 ... done
   Stopping my_wordpress_db_1        ... done
   Removing my_wordpress_wordpress_1 ... done
   Removing my_wordpress_db_1        ... done
   Removing network my_wordpress_default
   ```

   

   

**falta networking y explicar un poco mas el archivo**







xxxxxx


```bash
$ docker-compose --version
docker-compose version 1.21.2, build 1719ceb
```





fff

