| [<-- Volver](20170807-Networking.md) |



Docker Compose
===

Referencias:

* [Documentación oficial Docker Compose](https://docs.docker.com/compose/)

* [Compose file version 3 reference](https://docs.docker.com/compose/compose-file/)



Introducción
---
*Docker Compose* es una herramienta que permite definir y correr aplicaciones Docker multi-contentedor.

A medida que las aplicaciones son mas complejas, resulta necesario distribuirlas en múltiples contenedores. Por ej. aplicaciones basadas en microservicios son apropiadas para usar múltiples contenedores, un contenedor con una base de datos, otro con un servidor web, un sistema de mensajería en otro, etc., etc. Crear estos contenedores en forma manual (*docker run*) resultará poco práctico, y si tuvieramos que crear un ambiente con decenas de contenedores, ciertamente no es la mejor opción.

Con Docker Compose podemos definir nuestra aplicación multicontenedor utilizando un único archivo de configuración, que contiene las definiciones de todos los servicios (contenedores) que necesitamos, y con un único comando podemos iniciar todos los servicios, o bajarlos.

Este archivo de configuración, en formato *yaml*, no solo nos sirve para poder desplegar y eliminar todo nuestro ambiente, sino que también es útil como documentación, dado que incluye toda la información sobre sus contenedores, imágenes, volúmenes, networking, y el resto de las características.



## Instalando Docker Compose

Docker Compose se puede instalar de varias formas, recomendamos realizar la instalación mediante una de estas dos alternativas.

**Nota**: Al momento de escribir este tutorial, instalar Docker Compose mediante *apt-get* nos ha dado problemas, dado que la versión instalada no soporta el archivo de configuración *version 3* que es el que utilizamos en este tutorial. Por tanto no recomendamos por el momento instalar de esta forma.



#### Alternativa 1: Instalación mediante *curl*

```bash
$ sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

Para instalar la última versión, en el comando anterior debemos indicar cuál es el último release disponible (1.29.2). Esto lo podemos ver aquí: [Compose repository release page on GitHub](https://github.com/docker/compose/releases).

Luego de finalizada la instalación debemos aplicar permiso de ejecución al binario:

```bash
$ sudo chmod +x /usr/local/bin/docker-compose
```


#### Alternativa 2: Instlación mediante *pip*

Si tenemos instalado `pip` (o lo instalamos), podemos usar esta alternativa:

```bash
$ sudo pip install docker-compose
```



#### Verificación de la instalación:

```bash
$ docker-compose --version
docker-compose version 1.29.2, build 5becea4c
```



## Como funciona Docker Compose

Docker Compose se basa en la utilización de un archivo de configuración en formato *YAML*, donde vamos a indicar los servicios que queremos desplegar. Esto incluye, entre otras cosas, que imagen de contenedor vamos a utilizar, su configuración, las dependencias entre contenedores, los volúmenes de disco, la configuración de las redes, etc.

Las dependencias permiten no solo crear los contenedores en determinado orden, sino que además, si un contenedor depende de otro, el *contenedor hijo* no será creado hasta que el *contenedor padre* exista y esté corriendo.

Este archivo también podemos usarlo para eliminar (bajar) nuestro ambiente una vez que ya no lo necesitamos, y es una fuenta de documentación muy precisa sobre el mismo.



## Desplegando los servicios

Para entender el contenido del archivo *docker-compose.yml* y como realizar el despliegue del mismo, realizaremos algunos ejercicios.



#### Ejercicio 20:

En este ejercicio vamos a crear dos servicios simples, llamados *db-server* y *web-server*.

1. Crear un directorio para nuestro proyecto.

   Este directorio debe contener únicamente los elementos necesarios para el ambiente que vamos a desplegar. Aquí incluiremos el archivo *docker-compse.yml*, así como los Dockerfiles, etc. Esto nos permite contar con toda la documentación específica de nuestro proyecto.

   ```bash
   $ mkdir compose01
   $ cd compose01
   ```



2. Crear un archivo *Dockerfile* que utilizaremos para construir las imagenes a utilizar para los servicios:

   ```bash
   FROM ubuntu
   LABEL maintainer="fagis@conatel.com.uy"
   RUN apt-get update
   RUN apt-get install -y net-tools
   RUN apt-get install -y dnsutils
   RUN apt-get install -y iputils-ping
   CMD bash
   ```

   Como ya vimos, este *Dockerfile* simplemente crea una imagen a partir de *ubuntu* a la cuál le instala algunos paquetes, y ejecuta el shell `bash`.

3. Crear el archivo *docker-compose.yml* con el siguiente contenido:

   ```bash
   version: '3'
   
   services:
     db-server:
       build: .
       container_name: "dbserver01"
       stdin_open: true
       tty: true
   
     web-server:
       build: .
       container_name: "webserver01"
       depends_on:
         - db-server
       stdin_open: true
       tty: true
   
   ```

   Las opciones `stdin_open: true` y `tty: true` permiten dejar abierta `STDIN` y asigarle una terminal al mismo, de forma que tendremos acceso al shell para poder interactuar con el contenedor. Esto es análogo a correr el comando `docker run -it` que vimos anteriormente.

4. Realizar el despliegue de los servicios, mediante el comando  `docker-compose up -d` desde el directorio del proyecto:

   ```bash
   $ docker-compose up -d
   Creating network "compose01_default" with the default driver
   Building db-server
   Step 1/7 : FROM ubuntu
   latest: Pulling from library/ubuntu
   Digest: sha256:586519e288b47ac3585061b424956418a0435e6469d9c02d6e9dc4ab03eed286
   Status: Downloaded newer image for ubuntu:latest
    ---> 16508e5c265d
   Step 2/7 : LABEL maintainer="fagis@conatel.com.uy"
    ---> Using cache
    ---> 7b6a16db23b6
   Step 3/7 : RUN apt-get update
    ---> Using cache
    ---> 565e7ab19a74
   Step 4/7 : RUN apt-get install -y net-tools
    ---> Running in 951f508c0fc7
   Reading package lists...
   ...
   ...
   ...
   Step 7/7 : CMD bash
    ---> Using cache
    ---> 3cb72a988a69
   Successfully built 3cb72a988a69
   Successfully tagged compose01_web-server:latest
   WARNING: Image for service web-server was built because it did not already exist. To rebuild this image you must use `docker-compose build` or `docker-compose up --build`.
   Creating dbserver01 ... done
   Creating webserver01 ... done
   
   ```



   La opción `-d` hace que el deploy corra en segundo plano (*detached*), ejecutando como servicio. 

   Si no ponemos esta opción el comando quedará en primer plano, y veremos los logs de todos los contenedores. Esto puede ser útil para diagnosticar algún problema, como contra, si lo cortamos (ctrl-c) detendrá la ejecución de todos los contenedores generados.

   Como es la primera vez que generamos nuestra imagen, el deploy va a mostrar todo el proceso de creación de la misma, bajando la imagen de `ubuntu` e instalando los paquetes que indicamos en el *Dockerfile*. La próxima vez el deploy será mucho mas rápido, dado que la imagen ya estará creada.



4. Una vez finalizado el despliegue, podemos verificar que los dos servicios están corriendo:

   ```bash
   $ docker container ls
   CONTAINER ID   IMAGE                  COMMAND             CREATED          STATUS           PORTS      NAMES
   5b1ccbd47029   compose01_web-server   "/bin/sh -c bash"   5 seconds ago    Up 4 seconds                webserver01
   e2c909735c87   compose01_db-server    "/bin/sh -c bash"   6 seconds ago    Up 5 seconds                dbserver01
   ```



5. Para detener todos los servicios, lo hacemos mediante el comando  `docker-compose down`:

   ```bash
   $ docker-compose down
   Stopping webserver01 ... done
   Stopping dbserver01  ... done
   Removing webserver01 ... done
   Removing dbserver01  ... done
   Removing network compose01_default
   
   $ docker container ls
   CONTAINER ID   IMAGE                  COMMAND             CREATED          STATUS           PORTS      NAMES
   
   ```



## Contenido del archivo *docker-compose.yml*

El nombre por defecto para el archivo de configuración es *docker-compose.yml*.

Si bien podemos utilizar otro nombre, tendremos que pasarselo como opción (-f) a cada uno de los comandos que ejecutemos, por lo cual recomendamos utilizar siempre el nombre por defecto, y crear directorios particulares para cada proyecto (como hicimos en el ejemplo anterior).

Este archivo contiene **3 secciones principales**, las cuales son:

- **services:** contiene la configuración de cada uno de los servicios que vamos a levantar, esto es, cada contenedor y sus opciones.
- **volumes:** contiene la configuración de los volumenes de disco que vamos a utilizar. Si bien es posible declarar los volumenes de cada contenedor dentro de la sección *services:*, hacerlo aquí en *volumes:* nos permite crear volumenes con nombres, que puedan ser reutilizados y fácilmente referenciados desde múltiples servicios.  
- **networks:** contiene la configuración de las redes que vamos a utilizar para los servivios. Si no definimos esta sección, se utilizará una única red por defecto para todos los servicios.

Veamos las opciones principales dentro de cada una de estas secciones.



### Definición de *services:*

En la sección **services:** es donde definimos todos los servicios que vamos a levantar en nuestro ambiente.

***service-name***: es un nombre que permite identificar el el servicio que estamos creando. Es un nombre arbitrario que seleccionamos nosotros, que nos permite diferenciar cada uno de los contenedores que vamos a levantar en nuestro ambiente, por ejemplo: *web-server*, *db-server*.

**container_name:** es el nombre que le va a dar al contenedor cuando levante el servicio. Es opcional, si no lo indicamos va a utilizar un nombre generado por defecto.

**build:** si vamos a construir nuestra imagen, aquí indicamos el directorio donde se encuentra el archivo *Dockerfile* que se utilizará para crear la misma (camino relativo).

**image:** si vamos a utilizar una imagen existente, aquí le indicamos cual es esa imagen. En caso de no encontrarla localmente la itentará bajar del repositorio de github.

**command:** comando que le pasamos a la imagen para que corra al momento de ejecutar el contenedor.

**ports:** permite mapear puertos al contenedor, en formato `host_port:container_port `

**environment:** perminte pasarle variables de entorno al contenedor, en formato `VARIABLE=valor `

**depends_on:** indica dependencia con otro(s) contenedor(es). El contenedor no va a levantar si los contenedores de los cuales depende no se encuentran corriendo. Los contenedores son iniciados/bajados siguiendo el orden necesario de acuerdo a las dependencias establecidas.

**network**: indica las redes que va a utilizar el servicio (lo veremos mas adelante).

**volumes:** indica los volumenes de disco que vamos a acceder desde el servicio. Como vimos antes, podemos definir los volumenes aquí dentro de *services:* o hacerlo preferentemente mas adelante, dentro de *volumes:*.

Veamos con un ejemplo como acceder a un directorio local del host (*bind mount*) desde un contenedor:

1. Iniciamos los servicios:

   ```bash
   $ docker-compose up -d
   Creating network "compose01_default" with the default driver
   Creating dbserver01 ... done
   Creating webserver01 ... done
   
   $ docker container ls
   CONTAINER ID     IMAGE                  COMMAND             CREATED             STATUS           PORTS     NAMES
   e6ddd3f51806     compose01_web-server   "/bin/sh -c bash"   52 seconds ago      Up 51 seconds              webserver01
   88adc0875532     compose01_db-server    "/bin/sh -c bash"   52 seconds ago      Up 51 seconds              dbserver01
   ```

2. En el mismo directorio de nuestro proyecto, creamos un directorio `./data` y un archivo dentro, que montaremos dentro de uno de los servicios:

   ```bash
   $ mkdir data
   $ touch data/test.txt
   ```


3. Editamos el archivo *docker-compose.yml*, agregando la referencia a este directorio dentro del servicio *web-server*:

   ```bash
   version: '3'
   
   services:
     db-server:
       build: .
       container_name: "dbserver01"
       stdin_open: true
       tty: true
   
     web-server:
       build: .
       container_name: "webserver01"
       depends_on:
         - db-server
       stdin_open: true
       tty: true
       volumes:
         - ./data:/mnt/data
   ```

   De esta forma, vamos a montamos el directorio local `./data` del host, en el direcotrio `/mnt/data` del contenedor `webserver01` que es creado para el servicio `web-server`.



4. Reflejamos los cambios en los servicios:

   ```bash
   $ docker-compose up -d
   dbserver01 is up-to-date
   Recreating webserver01 ... done
   ```



   Si nos conectamos al contenedor, podemos ver que el directorio local fue montado:

   ```bash
   $ docker attach webserver01
   root@e4be32bbc206:/#
   root@e4be32bbc206:/# ls -l /mnt/data
   total 0
   -rw-rw-r-- 1 1000 1000 0 Aug 21 23:17 test.txt
   ```

   **nota:** recuerde que para salir del contenedor debe hacer \<ctrl-p-q>, de lo contrario terminará el proceso bash que está ejecutando y el contenedor finalizará su ejecución.


Podemos hacer las definiciones de esta forma, dentro de la sección **services:** para cada uno de los servicios que requieran acceso a disco. Pero si quisieramos utilizar volumenes de docker, y además poder accederlos desde múltiples servicios, es preferible definirlos utilizando la sección **volumes:** como veremos a continuación.


### Definición de *volumes:*

Editemos nuevamente el archivo *docker-compose.yml*, realizando los siguientes cambios:

```bash
version: '3'

services:
  db-server:
    build: .
    container_name: "dbserver01"
    stdin_open: true
    tty: true
    volumes:
      - db-volume:/base

  web-server:
    build: .
    container_name: "webserver01"
    depends_on:
      - db-server
    stdin_open: true
    tty: true
    volumes:
      - ./data:/mnt/data

  backup-server:
    build: .
    container_name: "backupserver"
    stdin_open: true
    tty: true
    restart: always
    volumes:
      - db-volume:/backup/base

volumes:
  db-volume:
```



En este ejemplo, agregamos un volumen `db-volume`, definiendolo dentro de la sección **volumes:**.
El mismo es utilizado por el servicio *db-server* existente, así como también por un nuevo servicio *backup-server* que estamos agregando. Ambos servicios utilizan el mismo volumen, pero lo montan internamente en diferentes ubicaciones de cada contenedor.

Refrescamos nuestros servicios (puede demorar algunos segundos):

```bash
$ docker-compose up -d
Creating volume "compose01_db-volume" with default driver
Building backup-server
Step 1/7 : FROM ubuntu
...
...
Successfully built 3cb72a988a69
Successfully tagged compose01_backup-server:latest
WARNING: Image for service backup-server was built because it did not already exist. To rebuild this image you must use `docker-compose build` or `docker-compose up --build`.
Recreating dbserver01 ... done
Creating backupserver ... done
Recreating webserver01 ... done


$ docker container ls
CONTAINER ID     IMAGE                     COMMAND             CREATED              STATUS              PORTS     NAMES
0fe09e3f54f3     compose01_web-server      "/bin/sh -c bash"   About a minute ago   Up About a minute             webserver01
407b6d0533a5     compose01_db-server       "/bin/sh -c bash"   About a minute ago   Up About a minute             dbserver01
612cfaf139a7     compose01_backup-server   "/bin/sh -c bash"   2 minutes ago        Up About a minute             backupserver
```



Podemos ver que además de crear el nuevo servicio *backupserver*, se crea también un volumen:

```bash
$ docker volume ls
DRIVER              VOLUME NAME
local               compose01_db-volume
```



Nuevamente, podemos conectarnos a ambos contenedores y acceder al volumen en el punto de montaje correspondiente: 

```bash
$ docker attach dbserver01
root@6dae219d5ac6:/# 
root@6dae219d5ac6:/# cd /base
root@6dae219d5ac6:/base# touch archivo1.txt
root@6dae219d5ac6:/base# ls -l
total 0
-rw-r--r-- 1 root root 0 Aug 22 01:06 archivo1.txt

<ctrl-pq>


$ docker attach backupserver
root@94f5d5cb6abb:/# 
root@94f5d5cb6abb:/# ls -l /backup/base/
total 0
-rw-r--r-- 1 root root 0 Aug 22 01:06 archivo1.txt

<ctrl-pq>

```



##### Accediendo a volumenes mediante driver específico

Si vemos nuevamente el *docker-compose.yml* dentro de la sección `volumes:`, la entrada `db-volume:` que creamos se encuentra vacía. Por lo cual para acceder a dicho volumen se va a utilizar el driver por defecto del Docker Engine, que como ya vimos, generalmente es el driver `local`.  

```bash
volumes:
  db-volume:
```


Podemos en cambio, especificar que driver queremos utilizar, así como pasarle las opciones necesarias al mismo.
Por ejemplo, podemos utilizar el driver *sshfs* que ya vimos anteriormente [aquí](https://github.com/conapps/Devops-101/blob/master/Contenedores/20170815-Storage.md#volumenes-con-drivers-creados-por-los-usuarios), para montar un volumen desde un servidor ssh. 

```
volumes:
  db-volume:
    driver: vieux/sshfs:latest
    driver_opts:
      sshcmd: "ubuntu@sshserver.labs.conatest.click:/home/ubuntu/docker101"
      password: "conatel_docker101"
```


##### Accediendo a volumenes externos

En los casos anteriores, el comando `docker-compose up` se encarga de crear el volumen que definimos dentro de la sección `volumes:` del archivo *docker-compose.yml*. Esto lo verificamos al hacer un `docker volume ls`. Pero si ya tuvieramos un volumen definido previamente e intentáramos accederlo de esta forma, vamos a obtener un error.

Para esto, podemos acceder a volumenes externos que hayan sido definidos previamente. En este caso, el comando `docker-compose up` no intentará crear el volumen, sino que buscará el volumen ya creado y lo montará en el servicio. Claro que, en caso de que el volumen no exista, el deploy terminará con error.

Para definir un volumen como externo, le agregamos la opción `external: true`:

```bash
volumes:
  mi-volumen-externo: 
    external: true
```

En este caso, buscará un [volumen](https://github.com/conapps/Devops-101/blob/master/Contenedores/20170815-Storage.md#volumenes) ya definido en docker, con nombre *mi-volumen-externo*.



##### Eliminación de volumenes

Si bajamos el ambiente con `docker-compose down`, por defecto los volumenes creados en la sección *volumes:* no son eliminados. Si queremos forzar su eliminación, debemos agregarle la opción  `-v` o `--volumes`.

**Atención:** Tenga en cuenta que esto eliminará la información contenida en dichos volumenes.

```bash
$ docker-compose down -v
Stopping webserver01  ... done
Stopping backupserver ... done
Stopping dbserver01   ... done
Removing webserver01  ... done
Removing backupserver ... done
Removing dbserver01   ... done
Removing network compose01_default
Removing volume compose01_db-volume
Volume mi-volumen-externo is external, skipping

$ docker volume ls
DRIVER              VOLUME NAME
local               mi-volumen-externo
```

Los volumenes definidos como externos nunca son eliminados desde docker compose (y tampoco las redes externas).



### Definición de Networks:

Por defecto, cuando desplegamos nuestro ambiente el comando `docker-compose up` crea una única network y agrega cada contenedor a esta *XXXXX_default* network. 

```bash
$ docker network ls
NETWORK ID          NAME                DRIVER              SCOPE
ecdf172b3adf        bridge              bridge              local
db68a213cd9c        compose01_default   bridge              local
4b6f37984b56        host                host                local
b9b7a573b4d0        none                null                local
```


Como consecuencia, todos los contenedores pueden conectarse entre si, y además pueden descubrirse mediante su *hostname*:

```bash
$ docker container ls
CONTAINER ID   IMAGE                     COMMAND             CREATED         STATUS         PORTS     NAMES
851ae243af3a   compose01_web-server      "/bin/sh -c bash"   8 seconds ago   Up 7 seconds             webserver01
828c77fe3061   compose01_db-server       "/bin/sh -c bash"   9 seconds ago   Up 7 seconds             dbserver01
de70336c7814   compose01_backup-server   "/bin/sh -c bash"   9 seconds ago   Up 7 seconds             backupserver

$ docker attach backupserver 
root@03c3f705f7d1:/# ping dbserver01
PING dbserver01 (172.26.0.2) 56(84) bytes of data.
64 bytes from dbserver01.compose01_default (172.26.0.2): icmp_seq=1 ttl=64 time=0.047 ms
64 bytes from dbserver01.compose01_default (172.26.0.2): icmp_seq=2 ttl=64 time=0.055 ms
64 bytes from dbserver01.compose01_default (172.26.0.2): icmp_seq=3 ttl=64 time=0.056 ms
^C

root@03c3f705f7d1:/# ping webserver01
PING web-server (172.26.0.4) 56(84) bytes of data.
64 bytes from webserver01.compose01_default (172.26.0.4): icmp_seq=1 ttl=64 time=0.071 ms
64 bytes from webserver01.compose01_default (172.26.0.4): icmp_seq=2 ttl=64 time=0.068 ms
64 bytes from webserver01.compose01_default (172.26.0.4): icmp_seq=3 ttl=64 time=0.058 ms
^C

```



Si bien esto puede ser muy útil en un ambiente de prueba, en una ambiente en producción podría ser necesario restringir o segmentar esta conectividad, de modo que cada servicio pueda comunicarse únicamente con aquellos otros servicios que sea extrictamente necesario. 

Para esto, dentro de la sección **networks:** del archivo *docker-compose.yml* podemos crear nuestras propias redes, y así definir la conectividad entre los servicios.



**Ejercicio 21:**

Como vimos antes, nuestro *docker-compose.yml* crea los servicios *db-server*, *web-server*, y *backup-server*.  
En este ejercicio queremos modificar la conectividad, de forma que *db-server* se pueda comunicar con *web-server* y *backup-server*, pero, no queremos que *web-server* y *backup-server* se comuniquen entre si.
Para esto vamos a crear dos redes en forma manual (*custom networks*):



1. Primero bajemos nuestros servicios con `docker-compose down`. 
Si bien podemos dejarlos arriba y luego actualizarlos, será mas claro si lo hacemos de este modo, y aprovechamos a eliminar la default network:

   ```bash
   $ docker-compose down
   Stopping webserver01  ... done
   Stopping dbserver01   ... done
   Stopping backupserver ... done
   Removing webserver01  ... done
   Removing dbserver01   ... done
   Removing backupserver ... done
   Removing network compose01_default
   ```


2. Editamos el *docker-compose.yml* y en la sección *networks:* agregamos dos redes llamadas `prod-network` y `backup-network`.
Y dentro de la configuración de cada servicio, colocamos la *networks:* a las cuales queremos que acceda.


   ```bash
   version: '3'
   
   services:
     db-server:
       build: .
       container_name: "dbserver01"
       stdin_open: true
       tty: true
       volumes:
         - db-volume:/base
       networks:
         - prod-network
         - backup-network
   
     web-server:
       build: .
       container_name: "webserver01"
       depends_on:
         - db-server
       stdin_open: true
       tty: true
       volumes:
         - ./data:/mnt/data
       networks:
         - prod-network
       
     backup-server:
       build: .
       container_name: "backupserver"
       stdin_open: true
       tty: true
       volumes:
         - db-volume:/backup/base
         - mi-volumen-externo:/mi-volumen
       networks:
         - backup-network
       
   volumes:
     db-volume:
     mi-volumen-externo: 
       external: true
   
   networks:
     prod-network:
       driver: bridge
     backup-network:
       driver: bridge
   ```



   Ambas redes las definimos con el driver `bridge` (el cuál vimos [aqui](https://github.com/conapps/Devops-101/blob/master/Contenedores/20170807-Networking.md#bridge)), y dado que no estamos indicando ninguna configuración adicional, es el engine de docker quien asignará los rangos de direcciones IP a las redes, y las direcciones IP específicas a los servicios.

   De esta forma, la red `prod-network` conecta únicamente los servicios *db-server* y *web-server*, mientras que la red `backup-network` conecta a *backup-server* y *db-server*; pero no hay ninguna red que conecte a *web-server* con *backup-server* por lo cual estos dos servicios no podrán comunicarse entre si.


3. Ahora despleguemos nuestro ambiente, y verifiquemos la comunicación entre los servicios:

   ```bash
   $ docker-compose up -d
   Creating network "compose01_prod-network" with driver "bridge"
   Creating network "compose01_backup-network" with driver "bridge"
   Creating backupserver ... done
   Creating dbserver01   ... done
   Creating webserver01  ... done
   
   ubuntu@serverNum1:~/compose01$ docker network ls
   NETWORK ID          NAME                       DRIVER              SCOPE
   ecdf172b3adf        bridge                     bridge              local
   e62e9a0d6427        compose01_backup-network   bridge              local
   ef19fff25231        compose01_prod-network     bridge              local
   4b6f37984b56        host                       host                local
   b9b7a573b4d0        none                       null                local
   ```



   Podemos ver el detalle de cada una de las redes mediante el comando `docker network inspect`, y así saber por ejemplo que contenedor se encuentra conectado a cada red.

   En este caso también podemos conectarnos a los contenedores y probar la comunicación entre ellos como hicimos antes:

   ```bash
   $ docker attach backupserver
   root@f7397251a392:/# ping dbserver01
   PING dbserver01 (192.168.0.3) 56(84) bytes of data.
   64 bytes from dbserver01.compose01_backup-network (192.168.0.3): icmp_seq=1 ttl=64 time=0.056 ms
   64 bytes from dbserver01.compose01_backup-network (192.168.0.3): icmp_seq=2 ttl=64 time=0.054 ms
   ^C
         
   root@f7397251a392:/# ping webserver01
   ping: webserver01: Name or service not known
         
   ```


##### Estableciendo configuración de red a las custom networks

Podemos establecer la configuración de cada una de nuestras *custom networks*, indicando por ej. que rangos de IP queremos utilizar para cada una de ellas. 

Esto lo hacemos en la sección **networks:** del *docker-compose.yml*:

   ```bash
networks:
  prod-network:
    driver: bridge
    ipam:
      driver: default
      config:
        - subnet: 172.16.0.0/24   
   ```



Y podemos también configurar las opciones de red de los servicios, por ej. asignandoles una dirección IP específica, lo cuál hacemos en la sección **services:** del *docker-compose.yml*:

```bash
services:
  db-server:
    build: .
    container_name: "dbserver01"
    stdin_open: true
    tty: true
    volumes:
      - db-volume:/base
    networks:
      prod-network:
        ipv4_address: 172.16.0.3
```



##### Accediendo a redes externas

Si ya tenemos una red previamente definida en docker, y queremos utilizarla para nuestros servicios, podemos referenciarla de la siguiente manera:

```bash
networks:
  mi-red-externa: 
    external: true
```

Como indicamos antes, ni las redes externas, ni los volúmenes externos son eliminados cuando bajamos nuestros servicios con `docker-compose down`.



##### Eliminación de *custom networks:*

Si bajamos el ambiente con `docker-compose down`, por defecto las redes serán eliminadas:

```bash
$ docker-compose down -v
Stopping webserver01  ... done
Stopping backupserver ... done
Stopping dbserver01   ... done
Removing webserver01  ... done
Removing backupserver ... done
Removing dbserver01   ... done
Removing network compose01_prod-network
Removing network compose01_backup-network
Network mi-red-externa is external, skipping
Removing volume compose01_db-volume
Volume mi-volumen-externo is external, skipping

$ docker network ls
NETWORK ID          NAME                DRIVER              SCOPE
241e4c4be1e6        bridge              bridge              local
f9a3c9feaf96        host                host                local
9166adfed0fa        mi-red-externa      bridge              local
a8fd98b4fcd6        none                null                local
```

Las redes definidas como externas nunca son eliminados desde docker compose.



---



| [<-- Volver](20170807-Networking.md) |



