| [<-- Volver](20170807-Networking.md) |



Docker Compose
===

Referencias:

* [Documentación oficial Docker Compose](https://docs.docker.com/compose/)

* [Compose file version 3 reference](https://docs.docker.com/compose/compose-file/)



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

Si tenemos instalado `pip` (o lo instalamos), podemos usar esta alternativa:

```bash
$ sudo pip install docker-compose
```



#### Verificación de la instalación:

```bash
$ sudo docker-compose --version
docker-compose version 1.21.2, build 1719ceb
```



## Como funciona Docker Compose

Docker Compose se basa en la utilización de un archivo de configuración en formato *yml*, donde vamos a indicar los servicios que queremos desplegar. Esto incluye, entre otras cosas, que imagen de contenedor vamos a utilizar, su configuración, las dependencias entre contenedores, los volúmenes de disco, la configuración de las redes, etc.

Las dependencias permiten no solo crear los contenedores en determinado orden, sino que además, si un contenedor depende de otro, el *contendor hijo* no será creado hasta que el *contenendor padre* exista y esté corriendo.

Este archivo también podemos usarlo para eliminar (bajar) nuestro ambiente una vez que ya no lo necesitamos, y es una fuenta de documentación muy precisa sobre el mismo.



## Desplegando los servicios

Para entender el contenido del archivo *docker-compose.yml* y como realizar el despliegue del mismo, realizaremos algunos ejercicios.



#### Ejercicio 20:

En este ejercicio vamos a crear dos servicios simples, llamados *db-server* y *web-server*.

1. Crear un directorio para nuestro proyecto.

   Este directorio debería contar únicamente con los elementos necesarios para el ambiente que vamos a crear. Si bien en este caso tendrá unicamente el archivo *docker-compse.yml* podríamos incluir aquí dentro cualquier otro recurso necesario (ej. Dockerfiles). Esto nos permite mantener ordenada y actualizada toda la documentación específica de nuestro proyecto.

   ```bash
   $ mkdir compose01
   $ cd compose01
   ```



2. Crear el archivo *docker-compose.yml* con el siguiente contenido:

   ```bash
   version: '3'

   services:
     db-server:
       image: ubuntu
       container_name: "dbserver01"
       command: /bin/bash
       stdin_open: true
       tty: true

     web-server:
       image: ubuntu
       container_name: "webserver01"
       command: /bin/bash
       depends_on:
         - db-server
       stdin_open: true
       tty: true
   ```

   En este caso para hacer un ejemplo sencillo, simplemente estamos utilizando una imagen de *ubuntu* para nuestros dos servicios.

   Las opciones `stdin_open: true` y `tty: true` permiten dejar abierta la stdin y la terminal conectada, de forma que el comando `/bin/bash` quede ejecutando. Si no hacemos esto, el `bash` se ejecuta, termina inmediatamente, y el contenedor se apaga. Esto es análogo a correr a mano el comando `docker run -it` que vimos anteriormente.

3. Realizar el despliegue de los servicios, mediante el comando  `docker-compose up -d` desde el directorio que contiene el archivo *docker-compose.yml*.

   ```bash
   $ docker-compose up -d
   Creating network "compose01_default" with the default driver
   Creating dbserver01 ... done
   Creating webserver01 ... done
   $
   ```

   La opción `-d` hace que el deploy corra en segundo plano (*detached*), ejcutando como servicio. 

   Si no ponemos esta opción el comando quedará en primer plano, y de veremos los logs de todos los contenedores. Esto puede ser útil para diagnosticar algún problema, como contra, si lo cortamos (ctrl-c) detendrá la ejecución de todos los contenedores generados.

   En este caso el despliegue es muy rapido, dado que utilizamos la imagen de *ubuntu* que se encuentra almacenada localmente. Si la imagen no estuviera local la descargará del repositorio de [dockerhub](https://hub.docker.com/).


4. Una vez finalizado el despliegue, podemos verificar si los dos contenedores están corriendo:

   ```bash
   $ docker ps
   CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
   ffce08dd859c        ubuntu              "/bin/bash"         7 seconds ago       Up 6 seconds                            webserver01
   c7743be062e6        ubuntu              "/bin/bash"         8 seconds ago       Up 7 seconds                            dbserver01
   ```


5. Para detener todos los servicios, lo hacemos mediante el comando  `docker-compose down`:

   ```bash
   $ docker-compose down
   Stopping webserver01 ... done
   Stopping dbserver01  ... done
   Removing webserver01 ... done
   Removing dbserver01  ... done
   Removing network compose01_default
   
   $ docker ps
   CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
   
   ```



## Contenido del archivo *docker-compose.yml*

Como vimos , el nombre por defecto para el archivo de configuración es *docker-compose.yml*.

Si bien podemos utilizar otro nombre, tendremos que pasarselo a cada uno de los comandos que ejecutemos, por lo cual recomendamos utilizar siempre el nombre por defecto, y crear directorios particulares para cada proyecto (como hicimos en el ejemplo anterior).

Este archivo contiene 3 secciones principales, las cuales son:

- **services:** contiene la configuración de cada uno de los servicios que vamos a levantar, esto es, cada contenedor y sus opciones.
- **volumes:** contiene la configuración de los volumenes de disco que vamos a utilizar. Si bien es posible declarar los volumenes de cada contenedor dentro de la sección de *services:*, hacerlo en esta sección nos permite crear volumenes con nombres, que puedan ser reutilizados y facilmente referenciados desde múltiples servicios.  
- **networks:** contiene la configuración de las redes que vamos a utilizar para los servivios. Si no definimos esta sección, se utilizará una red por defecto para todos los servicios.

Veamos las opciones principales dentro de cada una de estas secciones.



### Definición de *services:*

En la sección **services:** es donde definimos todos los servicios que vamos a levantar en nuestro ambiente.

***service-name***: es un nombre que permite identificar el el servicio que estamos creando. Es un nombre arbitrario que seleccionamos nosotros, que nos permite diferenciar cada uno de los contenedores que vamos a levantar en nuestro ambiente, por ejemplo: *web-server*, *db-server*.

**container_name:** es el nombre que le va a dar al contenedor cuando levante el servicio. Es opcional, si no lo indicamos va a utilizar un nombre generado por defecto.

**image:** es la imagen que vamos a utilizar para crear el contenedor. En caso de no encontrarla localmente la itentará bajar del repositorio de github.

**build:** si en lugar de utilizar una imagen existente queremos crear nuestra propia imagen a partir de un *Dockerfile*, es aquí donde le indicamos el directorio donde se encuentra el mismo.

**command:** comando que le pasamos al contenedor para que corra al momento de ejecución.

**ports:** permite mapear puertos al contenedor en formato `host_port:container_port `

**environment:** perminte pasarle variables de entorno al contenedor en formato `VARIABLE=valor `

**depends_on:** indica dependencia con otro(s) contenedor(es). El contenedor no va a levanta si los contenedores de los cuales depende no se encuentran corriendo. Los contenedores son iniciados/bajados siguiendo el orden necesario de acuerdo a las dependencias establecidas.

**network**: indica las redes va a utilizar el servicio.

**volumes:** indica los volumenes de disco que vamos a acceder desde el servicio.

Veamos con un ejemplo, como acceder con docker compose a un directorio local del host (*bind mount*):

1. Iniciemos nuevamente nuestros servicios:

   ```bash
   $ docker-compose up -d
   Creating network "compose01_default" with the default driver
   Creating dbserver01 ... done
   Creating webserver01 ... done
   
   $ docker ps
      CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
      51b6c6d19029        ubuntu              "/bin/bash"         5 seconds ago       Up 4 seconds                            webserver01
      5c8c67e6ebc4        ubuntu              "/bin/bash"         5 seconds ago       Up 4 seconds                            dbserver01
   ```

2. En el mismo directorio de nuestro proyecto, crear un directorio `./data`, el cual montaremos dentro de uno de los servicios:

   ```bash
   $ mkdir data
   $ touch data/test.txt
   ```


3. Editemos el archivo *docker-compose.yml*, agregando el directorio que queremos montar desde el host (bind mount) al servicio *web-server*:

   ```bash
   version: '3'

   services:
     db-server:
       image: ubuntu
       container_name: "dbserver01"
       command: /bin/bash
       stdin_open: true
       tty: true

     web-server:
       image: ubuntu
       container_name: "webserver01"
       command: /bin/bash
       depends_on:
         - db-server
       stdin_open: true
       tty: true
       volumes:
         - ./data:/mnt/data

   ```

   Esto monta el directorio local `./data` del host, en el direcotrio `/mnt/data` dentro del contenedor creado para el servicio `web-server`.



4. Para reflejar los cambios realizados hacemos:

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

**nota:** recuerde que para salir del contenedor luego de hacer el `attach` debe hacer <ctrl-p-q>, de lo contrario terminará el proceso bash que estaba ejecutando, y por tanto el contenedor finalizará su ejecución.

Podemos hacer las definiciones de esta forma, dentro de la sección **services:** para cada uno de los servicios que requieran acceso a disco. Pero si quisieramos utilizar volumenes de docker, y además poder accederlos desde múltiples servicios de forma mas clara y ordenada, es preferible definirlos utilizando la sección **volumes:** como veremos a continuación.



### Definición de *volumes:*

Editemos nuevamente el archivo *docker-compose.yml*, realizando los siguientes cambios:

```bash
version: '3'

services:
  db-server:
    image: ubuntu
    container_name: "dbserver01"
    command: /bin/bash
    stdin_open: true
    tty: true
    volumes:
      - db-volume:/base

  web-server:
    image: ubuntu
    container_name: "webserver01"
    command: /bin/bash
    depends_on:
      - db-server
    stdin_open: true
    tty: true
    volumes:
      - ./data:/mnt/data

  backup-server:
    image: ubuntu
    container_name: "backupserver"
    command: /bin/bash
    stdin_open: true
    tty: true
    volumes:
      - db-volume:/backup/base

volumes:
  db-volume:
```



En este ejemplo, creamos un volumen `db-volume` que es utilizado por el servicio *db-server*  y es compartido con un nuevo servicio *backup-server* que agregamos. Ambos servicios utilizan el mismo volumen, que esta vez lo definimos en la sección **volumes:** , y lo montan en diferentes ubicaciones:

Volvemos a refrescar nuestros servicios:

```bash
$ docker-compose up -d
Creating volume "compose01_db-volume" with default driver
Recreating dbserver01 ... done
Creating backupserver  ... done
Recreating webserver01 ... done


$ docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
cfa28d9f11bd        ubuntu              "/bin/bash"         11 seconds ago      Up 10 seconds                           webserver01
6dae219d5ac6        ubuntu              "/bin/bash"         12 seconds ago      Up 10 seconds                           dbserver01
94f5d5cb6abb        ubuntu              "/bin/bash"         12 seconds ago      Up 9 seconds                            backupserver
```



Podemos ver que además de crear el nuevo servicio *backupserver*, se crea también un volumen:

```bash
$ docker volume ls
DRIVER              VOLUME NAME
...
local               compose01_db-volume
...
```



Nuevamente, podemos conectarnos a ambos contenedores y acceder al volumen en el punto de montaje correspondiente: 

```bash
$ sudo docker attach dbserver01
root@6dae219d5ac6:/# 
root@6dae219d5ac6:/# cd /base
root@6dae219d5ac6:/base# touch archivo1.txt
root@6dae219d5ac6:/base# ls -l
total 0
-rw-r--r-- 1 root root 0 Aug 22 01:06 archivo1.txt
root@6dae219d5ac6:/base#
<ctrl-pq>


$ sudo docker attach backupserver
root@94f5d5cb6abb:/# 
root@94f5d5cb6abb:/# ls -l /backup/base/
total 0
-rw-r--r-- 1 root root 0 Aug 22 01:06 archivo1.txt
root@94f5d5cb6abb:/# 
<ctrl-pq>

```



##### Accediendo a volumenes mediante driver específico

Si vemos nuevamente nuestro *docker-compose.yml*, dentro de la sección `volumes:` lo que agregamos es el volumen que será creado al correr el comando `docker-compose up`.

En nuesto caso esta entrada  `db-volume:` se encuentra vacía, por lo cual para acceder a dicho volumen se va a utilizar el driver por defecto del Docker Engine (generalmente es el driver `local`).  

```bash
volumes:
  db-volume:
```



Si quisieramos, podemos indicar que driver utilizar, así como pasarle opciones al mismo. Por ejemplo:

```
volumes:
  db-volume:
    driver: vieux/sshfs:latest
    driver_opts:
      sshcmd: "conatel@sshserver.labs.conatest.click:/home/conatel"
      password: "docker101"
```

En este caso utilizamos el driver *sshfs* que ya vimos anteriormente, que permite montar un volumen desde un servidor ssh. 



##### Accediendo a volumenes externos

En todos los casos anteriores, el comando `docker-compose up`se encarga de crear el volumen que estamos definiendo dentro de la sección `volumes:` del archivo *docker-compose.yml*. Esto lo verificamos al hacer un `docker volume ls`. Pero si ya tuvieramos creardo un volumen, definido previamente, e intentamos accederlo de esta misma forma, vamos a obtener un error.

Para esto, podemos acceder a **volumenes externos** que hayan sido definidos previamente. En este caso, el comando `docker-compose up` no intentará crear el volumen, sino que buscará el volumen ya creado. Claro que, en caso de que el volumen no exista, el comando terminará con error.

Veamos esto con el siguiente ejercicio. Primero creamos un volumen:

```bash
$ docker volume create mi-volumen-externo
mi-volumen-externo

$ docker volume ls
DRIVER              VOLUME NAME
local               mi-volumen-externo
```



Y en el archivo *docker-compose.yml* agregamos este volumen como externo, al servicio *db-server*:

```bash
version: '3'

services:
  db-server:
    image: ubuntu
    container_name: "dbserver01"
    command: /bin/bash
    stdin_open: true
    tty: true
    volumes:
      - db-volume:/base
      
  web-server:
    image: ubuntu
    container_name: "webserver01"
    command: /bin/bash
    depends_on:
      - db-server
    stdin_open: true
    tty: true
    volumes:
      - ./data:/mnt/data

  backup-server:
    image: ubuntu
    container_name: "backupserver"
    command: /bin/bash
    stdin_open: true
    tty: true
    restart: always
    volumes:
      - db-volume:/backup/base
      - mi-volumen-externo:/mi-volumen
  
volumes:
  db-volume:
  mi-volumen-externo: 
    external: true
```

Nuevamente, podemos conectarnos al *backupserver* y ver que el puedo acceder al volumen montado en `/mi_volumen`. 



##### Eliminación de volumenes

Si bajamos nuestro ambiente, los volumenes creados en la sección *volumes:* por defecto no son eliminados:

```bash
$ docker-compose down
Stopping webserver01  ... done
Stopping backupserver ... done
Stopping dbserver01   ... done
Removing webserver01  ... done
Removing backupserver ... done
Removing dbserver01   ... done
Removing network compose01_default

$ docker volume ls
DRIVER              VOLUME NAME
...
local               compose01_db-volume
...
local               mi-volumen-externo
...
```



Para eliminar los volumenes definidos en *volumes:* debemos agregarle `-v` o `--volumes` (para probarlo, iniciemos los servicios antes):

```bash
$ docker-compose up -d
...

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
...
local               mi-volumen-externo
...
```

Como se puede ver los volumenes definidos como externos no son eliminados desde docker compose.





### Definición de Networks:

Por defecto, cuando desplegamos nuestro ambiente, el comando `docker-compose up`crea una única network, y agrega cada contenedor de un servicio a esta *default network*. Como consecuencia, todos los contenedores pueden conectarse entre ellos y además pueden descubrirse mediante su *hostname*.

```bash
$ docker-compose up -d
...
...

$ docker network ls
NETWORK ID          NAME                DRIVER              SCOPE
ecdf172b3adf        bridge              bridge              local
db68a213cd9c        compose01_default   bridge              local
4b6f37984b56        host                host                local
b9b7a573b4d0        none                null                local


$ docker attach backupserver 
root@03c3f705f7d1:/# 
root@03c3f705f7d1:/# apt-get update; apt-get install -y iputils-ping dnsutils
...
...

root@03c3f705f7d1:/# ping -c4 dbserver01
PING dbserver01 (172.26.0.2) 56(84) bytes of data.
64 bytes from dbserver01.compose01_default (172.26.0.2): icmp_seq=1 ttl=64 time=0.047 ms
64 bytes from dbserver01.compose01_default (172.26.0.2): icmp_seq=2 ttl=64 time=0.055 ms
64 bytes from dbserver01.compose01_default (172.26.0.2): icmp_seq=3 ttl=64 time=0.056 ms
64 bytes from dbserver01.compose01_default (172.26.0.2): icmp_seq=4 ttl=64 time=0.061 ms

--- dbserver01 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 2997ms
rtt min/avg/max/mdev = 0.047/0.054/0.061/0.010 ms

root@03c3f705f7d1:/# 
root@03c3f705f7d1:/# 
root@03c3f705f7d1:/# ping -c4 webserver01
PING web-server (172.26.0.4) 56(84) bytes of data.
64 bytes from webserver01.compose01_default (172.26.0.4): icmp_seq=1 ttl=64 time=0.071 ms
64 bytes from webserver01.compose01_default (172.26.0.4): icmp_seq=2 ttl=64 time=0.068 ms
64 bytes from webserver01.compose01_default (172.26.0.4): icmp_seq=3 ttl=64 time=0.058 ms
64 bytes from webserver01.compose01_default (172.26.0.4): icmp_seq=4 ttl=64 time=0.067 ms

--- web-server ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 2998ms
rtt min/avg/max/mdev = 0.058/0.066/0.071/0.004 ms
```



Si bien esto puede ser útil en un ambiente de prueba, en una ambiente en producción podría interesarnos restringir o segmentar esta conectividad, de modo que los contenedores puedan comunicarse únicamente con los que sea extrictamente necesario.

Dentro de la sección **networks:** del archivo *docker-compose.yml*, podemos modificar la red por defecto `default:`o bien crear nuestras propias redes, que es lo que vamos a hacer a continuación mediante los siguientes ejercicios.

Como vimos antes, nuestro *docker-compose.yml* crea los servicios *db-server*, *web-server*, y *backup-server*.  Supongamos que queremos que *db-server* se pueda comunicar con *web-server* y con *backup-server*, pero no queremos que *web-server* y *backup-server* se comuniquen entre si. Para esto vamos a crear dos redes en forma manual (*custom networks*) dentro del archivo *docker-compose.yml*. 



**Ejercicio 21:**

1. Primero bajemos nuestros servicios con `docker-compose down`. Si bien podemos dejarlos arriba y luego actualizarlos, será mas claro si lo hacemos de este modo, dado que de esta forma eliminamos la *default network*:



   ```bash
   $ docker network ls
   NETWORK ID          NAME                DRIVER              SCOPE
   ecdf172b3adf        bridge              bridge              local
   db68a213cd9c        compose01_default   bridge              local
   4b6f37984b56        host                host                local
   b9b7a573b4d0        none                null                local
   
   $ docker-compose down
   Stopping webserver01  ... done
   Stopping dbserver01   ... done
   Stopping backupserver ... done
   Removing webserver01  ... done
   Removing dbserver01   ... done
   Removing backupserver ... done
   Removing network compose01_default
   
   $ docker network ls
   NETWORK ID          NAME                DRIVER              SCOPE
   ecdf172b3adf        bridge              bridge              local
   4b6f37984b56        host                host                local
   b9b7a573b4d0        none                null                local
   
   ```




2. Editamos el *docker-compose.yml* y agregamos dos redes `prod-network` y `backup-network`. 

   ```bash
   version: '3'
   
   services:
     db-server:
       image: ubuntu
       container_name: "dbserver01"
       command: /bin/bash
       stdin_open: true
       tty: true
       volumes:
         - db-volume:/base
       networks:
         - prod-network
         - backup-network
   
     web-server:
       image: ubuntu
       container_name: "webserver01"
       command: /bin/bash
       depends_on:
         - db-server
       stdin_open: true
       tty: true
       volumes:
         - ./data:/mnt/data
       networks:
         - prod-network
   
     backup-server:
       image: ubuntu
       container_name: "backupserver"
       command: /bin/bash
       stdin_open: true
       tty: true
       restart: always
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



   De esta forma, la red `prod-network` conecta a los servicios *db-server* y *web-server*, mientras que `backup-network` conecta a *backup-server* y *db-server*; pero no hay ninguna red que conecte a *web-server* con *backup-server*.



3. Ahora despleguemos nuestro ambiente y veamos la comunicación entre los servicios:

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



   Podemos ver el detalle de cada una de las redes mediante el comando `docker network inspect`, por ejemplo para ver que contenedor se encuentra conectado a cada red.

   También podemos conectarnos a los contenedores y probar la comunicación entre ellos:

   ```bash
   $ docker attach backupserver 
   root@03c3f705f7d1:/# 
   root@03c3f705f7d1:/# apt-get update; apt-get install -y iputils-ping dnsutils
   ...
   ...
   
   root@f7397251a392:/# ping -c4 dbserver01
   PING dbserver01 (192.168.0.3) 56(84) bytes of data.
   64 bytes from dbserver01.compose01_backup-network (192.168.0.3): icmp_seq=1 ttl=64 time=0.056 ms
   64 bytes from dbserver01.compose01_backup-network (192.168.0.3): icmp_seq=2 ttl=64 time=0.054 ms
   64 bytes from dbserver01.compose01_backup-network (192.168.0.3): icmp_seq=3 ttl=64 time=0.055 ms
   64 bytes from dbserver01.compose01_backup-network (192.168.0.3): icmp_seq=4 ttl=64 time=0.058 ms
   
   --- dbserver01 ping statistics ---
   4 packets transmitted, 4 received, 0% packet loss, time 2997ms
   rtt min/avg/max/mdev = 0.054/0.055/0.058/0.009 ms
   
   root@f7397251a392:/# ping -c4 webserver01
   ping: webserver01: Name or service not known
   
   ```



Para terminar, en el ejemplo anterior si bien definimos las redes nosotros, dejamos que sea el engine de docker quien asigne la configuración de cada red, esto es, rango de direcciones ip, default gateway, dirección ip de cada servicio, etc. 

Si queremos, podemos indicar estos valores a mano en el archivo *docker-compose.yml*. También podemos utilizar redes externas, que se encuentren previamente definidas, con `external:  `.

```bash:
version: '3'

services:
  db-server:
    image: ubuntu
    container_name: "dbserver01"
    command: /bin/bash
    stdin_open: true
    tty: true
    volumes:
      - db-volume:/base
    networks:
      prod-network:
        ipv4_address: 172.16.0.3
      backup-network:

  web-server:
    image: ubuntu
    container_name: "webserver01"
    command: /bin/bash
    depends_on:
      - db-server
    stdin_open: true
    tty: true
    volumes:
      - ./data:/mnt/data
    networks:
      prod-network:
        ipv4_address: 172.16.0.4

  backup-server:
    image: ubuntu
    container_name: "backupserver"
    command: /bin/bash
    stdin_open: true
    tty: true
    restart: always
    volumes:
      - db-volume:/backup/base
      - mi-volumen-externo:/mi-volumen
    networks:
      - backup-network
      - mi-red-externa

volumes:
  db-volume:
  mi-volumen-externo:
    external: true

networks:
  prod-network:
    driver: bridge
    ipam:
      driver: default
      config:
        - subnet: 172.16.0.0/24
  backup-network:
    driver: bridge
  mi-red-externa:
    external: true
```



---



| [<-- Volver](20170807-Networking.md) |



# 

