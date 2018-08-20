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



Este archivo contiene 3 secciones principales, las cuales son: 

- [Service Configuration:](https://docs.docker.com/compose/compose-file/#service-configuration-reference) contiene la configuración de cada uno de los contenedores que vamos a crear para nuestro servicio. 
- [Volume Configuration:](https://docs.docker.com/compose/compose-file/#volume-configuration-reference) contiene la configuración de los volumenes de disco que vamos a utilizar. Si bien es posible declarar los volumenes de cada contenedor dentro de la sección de *Service*, hacerlo en esta sección nos permite crear volumenes que nombres, que pueden ser reutilizados y facilmente referenciados desde múltiples contenedores.  
- [Network Configuration:](https://docs.docker.com/compose/compose-file/#netowrk-configuration-reference) contiene la configuración de las redes que vamos a utilizar para los contenedores dentro de este servicio. Si no definimos esta sección, se utilizará una red por defecto para todos los contenedores creados en el servicio.

	

#### Service Configuration:

***service-name***: es un nombre que permite identificar el el servicio que vamos a correr en este contenedor, Es un nombre arbitrario que seleccionamos nosotros, que nos permite diferenciar cada uno de los contenedores que vamos a levantar en nuestro ambiente, por ejemplo: *web-server*, *db-server*. 

**container_name:** nombre del contenedor, si no lo indicamos va a utilizar el nombre generado por defecto.

**image:** es la imagen que vamos a utilizar para crear el contenedor. En caso de no encontrarla localmente al hacer el deploy bajará la imagen del repositorio de github, como lo hace habitualmente.

**build:** si en lugar de utilizar una imagen existente, queremos crear nuestra propia imagen a partir de un *Dockerfile*, es aquí donde colocamos el camino relativo (*./directorio*) a donde se encuentra nuestro archivo  *Dockerfile*.

**command:** comando que le pasamos al contenedor para que corra al momento de ejecución.

**ports:** permite mapear puertos al contenedor en formato ```host_port:container_port ``` 

**environment:** variables de entorno que le pasamos al contendor ```VARIABLE=valor ``` o ```VARIABLE:valor ```. Por ejemplo, en un contendor con MySQL le pasaríamos la base de datos a crear y las credenciales.

**depends_on:** indica dependencia con otro(s) contenedor(es). Este contenedor no va a levanta si los contenedores de los cuales depende ya se encuentran corriendo. Los contenedores son iniciados siguiendo el orden necesario de acuerdo a las dependencias establecidas.

**volumes:** indica los volumenes de disco que vamos a montar en el contenedor. Podemos montar un directorio del host directamente utilizando esta sentencia, la cual aplica únicamente para este servicio. 

```bash
version: '3.3'

services:
  web-server:
    build: .
    volumes:
      - ./online_app:/app
```

En este ejemplo, definimos un volumen para el servicio `web-server`, el cual monta el directorio local `./online_app` del host, en el direcotrio `/app` dentro del contenedor. 

Podemos hacer todas las definiciones de esta forma, dentro de cada servicio. Pero si quisieramos hacerlo de forma un poco mas ordenada, y además poder reutilizar volumenes para accederlos desde múltiples servicios, es preferible definirlos utilizando la sección de *Volume Configuration*, tal como lo veremos un poco mas adelante.

**network**: indica que redes va a utilizar el servicio, haciendo referencia a las redes definidas en la sección de *Network Configuration*, como veremos mas adelante.

En esta definición, podemos indicar parametros de red, tales como la dirección ip, default gateway, etc. 

```bash
version: '3.3'

services:
  web-server:
    build: .
    volumes:
      - ./online_app:/app
```





#### Volume Configuration:

En el siguiente ejemplo, tenemos dos servicios que utilizan el mismo volumen, el cual se define en la sección de *volumes:*

Here’s an example of a two-service setup where a database’s data directory is shared with another service as a volume so that it can be periodically backed up:

```
version: "3"

services:
  db:
    image: db
    volumes:
      - data-volume:/var/lib/db
  backup:
    image: backup-service
    volumes:
      - data-volume:/var/lib/backup/data

volumes:
  data-volume:
```

An entry under the top-level `volumes` key can be empty, in which case it uses the default driver configured by the Engine (in most cases, this is the `local` driver). Optionally, you can configure it with the following keys:





Podemos montar un directorio del host (*bind mount*), un volumen (*volumes*) con . También podemos montar volumenes con drivers creados por los usuarios (ej. *sshFS*, *REX-Ray*).



#### Network Configuration:











## Desplegando nuestro ambiente

Para entender como se realiza el despliegue de los contonedores, realizaremos el siguiente ejercicio.

En el mismo vamos a crear un ambiente con dos contenedores, uno con *wordpress* y el otro con la base de datos requerida por el primero.



#### Ejercicio 20:

1. Crear un directorio para nuestro proyecto.

   Este directorio debería contar únicamente con los elementos necesarios para el ambiente que vamos a crear. Si bien en este caso tendría unicamente el archivo *docker-compse.yml* podríamos incluir aquí dentro cualquier otro recurso necesario (ej. Dockerfiles). Esto nos permite mantener ordenada y actualizada toda la documentación específica de nuestro proyecto.

   ```bash
   $ mkdir my_wordpress
   $ cd my_wordpress
   ```



2. Crear el archivo *docker-compose.yml* con el siguiente contenido:

   ```bash
   version: '3.3'

   services:
      db:
        image: mysql
        container_name: "db"
        volumes:
          - db_data:/var/lib/mysql
        environment:
          MYSQL_ROOT_PASSWORD: somewordpress
          MYSQL_DATABASE: wordpress
          MYSQL_USER: wordpress
          MYSQL_PASSWORD: wordpress

      wordpress:
        image: wordpress
        container_name: "wordpress"
        depends_on: [db]
        ports:
          - "8000:80"
        environment:
          WORDPRESS_DB_HOST: db:3306
          WORDPRESS_DB_USER: wordpress
          WORDPRESS_DB_PASSWORD: wordpress
   volumes:
       db_data:

   ```



3. Realizar el despliegue, mediante el comando  `docker-compose up -d` desde el directorio que creamos, que contiene el archivo *docker-compose.yml*.

   Como ya hemos visto, si no tenemos las imagenes almacenadas localmente, las descargará del repositorio desde [dockerhub](https://hub.docker.com/).



   ```bash
   $ sudo docker-compose up -d
   Creating volume "my_wordpress_db_data" with default driver
   Pulling db (mysql:latest)...
   latest: Pulling from library/mysql
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
   Status: Downloaded newer image for mysql:latest
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
   8724f78e61a0        mysql:latest        "docker-entrypoint..."   5 minutes ago       Up 5 minutes        3306/tcp, 33060/tcp    my_wordpress_db_1
   ```



	Y además podemos acceder al servicio wordpress desde un navegador:

**ABRIR EL PUERTO 8080 EN AWS PARA QUE ESTO FUNCIONE**



![alt text](Imagenes/wordpress.png)



Y también podemos ver que tenemos las nuevas imagenes que fueron descargadas en forma local:

```bash
$ sudo docker images
REPOSITORY            TAG                 IMAGE ID            CREATED             SIZE
wordpress             latest              e2c4085bbc2b        2 days ago          408MB
mysql                 latest              29e0ae3b69b9        2 days ago          372MB
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



   Y las imágenes que fueron descargadas durante el proceso de despliegue, siguen estando almacenadas localmente:

   ```bash
   $ sudo docker images
   REPOSITORY            TAG                 IMAGE ID            CREATED             SIZE
   wordpress             latest              e2c4085bbc2b        2 days ago          408MB
   mysql                 latest              29e0ae3b69b9        2 days ago          372MB
   ...
   ```



   Por lo tanto si realizáramos el despliegue nuevamente con  `docker-compose up -d` , el proceso será muy rápido:

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







xxxxxx


```bash
$ docker-compose --version
docker-compose version 1.21.2, build 1719ceb
```







```
version: "3"
services:
  appserver1:
    image: "conatel/appserver1"
    container_name: "appserver1"
    depends_on: [dbserver1]
    environment:
      - MYSQL_DATABASE=grupo1
      - DMZ_IP=172.18.0.3
      - BACKEND_IP=172.18.1.3
    networks:
      dmz:
        ipv4_address: ${DMZ_IP}
      backend:
        ipv4_address: ${BACKEND_IP}
  appserver2:
    image: "conatel/appserver2"
    container_name: "appserver2"
    networks:
      dmz:
        ipv4_address: 172.18.0.4
  webserver1:
    image: "conatel/webserver1"
    container_name: "webserver1"
    environment:
      - DMZ_IP=172.18.0.2
    ports:
      - "80:80"
    networks:
      dmz:
        ipv4_address: ${DMZ_IP}
  webserver2:
    image: "conatel/webserver2"
    container_name: "webserver2"
    ports:
      - "8080:8080"
    networks:
      dmz:
        ipv4_address: 172.18.0.5
      backend:
        ipv4_address: 172.18.1.5
  dbserver1:
    image: "mysql"
    container_name: "dbserver1"
    environment:
      - MYSQL_DATABASE=grupo1
      - MYSQL_ROOT_PASSWORD=password
      - BACKEND_IP=172.18.1.2
    networks:
      backend:
        ipv4_address: ${BACKEND_IP}

networks:
  dmz:
    driver: bridge
    ipam:
      driver: default
      config:
        - subnet: 172.18.0.0/24
  backend:
    driver: bridge
    ipam:
      driver: default
      config:
        - subnet: 172.18.1.0/24

```

