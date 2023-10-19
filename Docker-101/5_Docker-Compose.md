| [&lt;-- Volver](4_Networking.md) |

Docker Compose
==============

Introducción
-------------

`Docker Compose` es una herramienta que permite definir y correr aplicaciones Docker multi-contentedor.

A medida que las aplicaciones son mas complejas, resulta necesario distribuirlas en múltiples contenedores. Por ej. aplicaciones basadas en microservicios son apropiadas para usar múltiples contenedores, un contenedor con una base de datos, otro con un servidor web, un sistema de mensajería en otro, etc., etc.

Crear estos contenedores en forma manual (`docker container run`) resultará poco práctico, y si tuvieramos que crear un ambiente con decenas de contenedores, ciertamente no es la mejor opción.

![alt text](Imagenes/microservicios.jpg "Arquitectura de Microservicios")

Con Docker Compose podemos definir nuestra aplicación multicontenedor utilizando un único archivo de configuración, que contiene las definiciones de todos los servicios (contenedores) que necesitamos, y con un único comando podemos iniciar todos los servicios, o bajarlos.

Este archivo de configuración, en formato `yaml`, no solo nos sirve para poder desplegar y eliminar todo nuestro ambiente, sino que también es útil como documentación, dado que incluye toda la información sobre sus contenedores, imágenes, volúmenes, networking, y el resto de las características configuradas.

## Instalando Docker Compose

> ⚠️ **Nota:** en los equipos que utilizamos para el laboratorio, `docker-compose` **ya se encuentra instalado**. Esta sección se coloca como referencia, pero puede saltearla en el curso.



Docker Compose se puede instalar de varias formas, recomendamos realizar la instalación mediante una de estas dos alternativas:

**Alternativa 1: Instalación mediante *curl***

```bash
$ sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

Para instalar la última versión, en el comando anterior debemos indicar cuál es el último release disponible (2.22.0). Esto lo podemos ver aquí: [Compose repository release page on GitHub](https://github.com/docker/compose/releases).

Luego de finalizada la instalación debemos aplicar permiso de ejecución al binario:

```bash
$ sudo chmod +x /usr/local/bin/docker-compose
```

**Alternativa 2: Instlación mediante *pip***

Si tenemos instalado `pip` (o lo instalamos), podemos usar esta alternativa:

```bash
$ sudo pip install docker-compose
```

**Verificación de la instalación:**

```bash
$ docker compose version
Docker Compose version v2.21.0

```

## Como funciona Docker Compose

Docker Compose se basa en la utilización de un archivo de configuración en formato *YAML*, donde indicamos los servicios que queremos desplegar. Esto incluye, entre otras cosas, que imagen de contenedor vamos a utilizar, su configuración, las dependencias con otros contenedores, los volúmenes de disco, la configuración de las redes, etc.

Las dependencias, por ejemplo, permiten no solo crear los contenedores en determinado orden, sino que además, si un contenedor depende de otro, el *contenedor hijo* no será creado hasta que el *contenedor padre* exista y esté corriendo.

Este archivo también podemos usarlo para eliminar (bajar) nuestro ambiente una vez que ya no lo necesitamos, y es una fuente de documentación muy precisa sobre el mismo.

## Desplegando los servicios

> 💡A partir de ahora es un buen momento para utilizar `Visual Studio Code`, y poder trabajar con los archivos YML de forma mas sencilla.

Para entender el contenido del archivo *docker-compose.yml* y como realizar el despliegue del mismo, realizaremos algunos ejercicios.

### Ejercicio 20:

En este ejercicio vamos a crear dos servicios simples, llamados *db-server* y *web-server*.

1. Crear un directorio para nuestro proyecto.

   Este directorio debe contener únicamente los elementos necesarios para el ambiente que vamos a desplegar. Aquí incluiremos el archivo *docker-compose.yml*, así como los Dockerfiles, etc. Esto nos permite contar con toda la documentación específica de nuestro proyecto.

   ```bash
   $ mkdir compose01
   $ cd compose01
   ```
2. Crear un archivo *Dockerfile* que utilizaremos para construir las imagenes a utilizar para los servicios, tal como lo hicimos anteriormente:

   ```bash
   FROM ubuntu
   LABEL maintainer="cdh@conatel.com.uy"
   RUN apt-get update
   RUN apt-get install -y net-tools
   RUN apt-get install -y dnsutils
   RUN apt-get install -y iputils-ping
   CMD bash
   ```

   Como ya vimos, este *Dockerfile* simplemente crea una imagen a partir de *ubuntu* a la cuál le instala algunos paquetes y ejecuta el shell `bash`.
   👉 Cree el Dockerfile pero no realice el build de la imagen en este punto.
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
4. Realizar el despliegue de los servicios, mediante el comando  `docker compose up -d`, parados en el directorio del proyecto:

```bash
~/compose01$ docker compose up -d
 => [db-server internal] load build definition from Dockerfile                                   0.1s
 => => transferring dockerfile: 218B                                                             0.0s
 => [db-server internal] load .dockerignore                                                      0.1s
 => => transferring context: 2B                                                                  0.0s   
 (...)
 (...)
 => => writing image sha256:b71290b9857fc86464021c3603df9a78cf105189a4644c28add883e01b9ea93a     0.0s
 => => naming to docker.io/library/compose01-web-server                                          0.0s
[+] Running 3/3
 ✔ Network compose01_default  Created                                                            0.1s 
 ✔ Container dbserver01       Started                                                            0.1s 
 ✔ Container webserver01      Started                                                            0.0s 

```

La opción `-d` hace que el deploy corra en segundo plano (*detached*), ejecutando como servicio.
Si no ponemos esta opción el comando quedará en primer plano, y veremos los logs de todos los contenedores. Esto puede ser útil para diagnosticar algún problema, pero como contra, si lo cortamos (ctrl-c) detendrá la ejecución de todos los contenedores generados.

Como es la primera vez que generamos nuestra imagen, el deploy va a mostrar todo el proceso de creación de la misma, bajando la imagen de `ubuntu` desde Dockerhub, e instalando los paquetes que indicamos en el archivo Dockerfile. La próxima vez el deploy será mucho mas rápido, dado que la imagen ya estará creada.

>  👉 El formato de la salida de este comando puede variar dependiendo de la versión de `docker compose` instalada en el servidor `host`.
>       Asi mismo, hasta la versión 1.x el comando era `docker-compose` y a partir de la versión 2.x pasa a ser `docker compose`.


5. Una vez finalizado el despliegue, podemos verificar que los servicios están corriendo, mediante `docker-compose ps`

```bash
~/compose01$ docker compose ps
NAME          IMAGE                  COMMAND             SERVICE      CREATED         STATUS         PORTS
dbserver01    compose01-db-server    "/bin/sh -c bash"   db-server    8 minutes ago   Up 8 minutes   
webserver01   compose01-web-server   "/bin/sh -c bash"   web-server   8 minutes ago   Up 8 minutes   

```

   Y también podemos ver, como siempre, el estado de los contenedores:

```bash
~/compose01$ docker container ls
CONTAINER ID   IMAGE                  COMMAND             CREATED          STATUS          PORTS     NAMES
8d16f1dcd769   compose01-web-server   "/bin/sh -c bash"   11 minutes ago   Up 11 minutes             webserver01
6a6d6d5b9e75   compose01-db-server    "/bin/sh -c bash"   11 minutes ago   Up 11 minutes             dbserver01

```

6. Para detener los servicios tenemos dos opciones:

   El comando `docker compose stop` detiene los servicios, sin eliminar los contenedores:

   ```bash
   ~/compose01$ docker compose stop
   [+] Stopping 2/2
    ✔ Container webserver01  Stopped                                                        10.2s 
    ✔ Container dbserver01   Stopped                                                        10.1s 

   ```

   El comando `docker compose down` no solo detiene los servicios, sino que además elimina los contenedores correspondientes (y las redes).

   ```bash
   $ docker compose down
   Stopping webserver01 ... done
   Stopping dbserver01  ... done
   Removing webserver01 ... done
   Removing dbserver01  ... done
   Removing network compose01_default

   ```

## Contenido del archivo *docker-compose.yml*

El nombre por defecto para el archivo de configuración es *docker-compose.yml* (o también *docker-compose.yaml).*

Si bien podemos utilizar otro nombre, tendremos que pasarselo como opción (-f) a cada uno de los comandos que ejecutemos, por lo cuál recomendamos utilizar siempre el nombre por defecto, y crear directorios particulares para cada proyecto (como hicimos en el ejemplo anterior).

Este archivo contiene **3 secciones principales**, las cuales son:

- **services:** contiene la configuración de cada uno de los servicios que vamos a levantar, esto es, cada contenedor y sus opciones.
- **volumes:** contiene la configuración de los volumenes de disco que vamos a utilizar. Si bien es posible declarar los volumenes de cada contenedor dentro de la sección *services:*, hacerlo aquí en *volumes:* nos permite crear volumenes con nombres, que puedan ser reutilizados y fácilmente referenciados desde múltiples servicios.
- **networks:** contiene la configuración de las redes que vamos a utilizar para los servivios. Si no definimos esta sección, se utilizará una única red por defecto para todos los servicios.

> ℹ️ recuerde que siempre puede acceder a la ayuda de los comandos, en este caso con `docker compose --help`

Veamos las opciones principales dentro de cada una de estas secciones.

### Definición de *services:*

En la sección **services:** es donde definimos todos los servicios que vamos a levantar en nuestro ambiente.

***service-name***: es un nombre que permite identificar el el servicio que estamos creando. Es un nombre arbitrario que seleccionamos nosotros, que nos permite diferenciar cada uno de los contenedores que vamos a levantar en nuestro ambiente, por ejemplo: *web-server*, *db-server*.

**container_name:** es el nombre que le va a dar al contenedor cuando levante el servicio. Es opcional, si no lo indicamos va a utilizar un nombre generado por defecto.

**build:** si vamos a construir nuestra imagen, aquí indicamos el directorio donde se encuentra el archivo *Dockerfile* que se utilizará para crear la misma (camino relativo).

**image:** si vamos a utilizar una imagen existente, aquí le indicamos cual es esa imagen. En caso de no encontrarla localmente la itentará bajar del repositorio de Dockerhub.

**command:** comando que le pasamos a la imagen para que corra al momento de ejecutar el contenedor.

**ports:** permite mapear puertos al contenedor, en formato `host_port:container_port `

**environment:** perminte pasarle variables de entorno al contenedor, en formato `VARIABLE=valor `

**depends_on:** indica dependencia con otro(s) contenedor(es). El contenedor no va a levantar si los contenedores de los cuales depende no se encuentran corriendo. Los contenedores son iniciados/bajados siguiendo el orden necesario de acuerdo a las dependencias establecidas.

**stdin_open** y **tty:** permiten dejar abierta `STDIN` y asigarle una terminal al mismo, de forma que tendremos acceso al shell para poder interactuar con el contenedor. Esto es análogo a correr el comando `docker container run -it` que vimos anteriormente.

**network**: indica las redes que va a utilizar el servicio (lo veremos mas adelante).

**volumes:** indica los volumenes de disco que vamos a acceder desde el servicio. Podemos definir los volumenes aquí dentro de *services:* o hacerlo preferentemente mas adelante, dentro de *volumes:*.

Veamos con un ejemplo como acceder a un directorio local del host (*bind mount*) desde un contenedor:

1. Iniciamos los servicios:

   ```bash
   ~/compose01$ docker compose up -d
    ✔ Network compose01_default  Created                                            0.1s 
    ✔ Container dbserver01       Started                                            0.1s 
    ✔ Container webserver01      Started                                            0.1s

   ~/compose01$ docker container ls
   CONTAINER ID   IMAGE                  COMMAND             CREATED          STATUS          PORTS     NAMES
   4b8726bc4a69   compose01-web-server   "/bin/sh -c bash"   53 seconds ago   Up 52 seconds             webserver01
   892cdfc29821   compose01-db-server    "/bin/sh -c bash"   53 seconds ago   Up 52 seconds             dbserver01

   ```
2. En el mismo directorio de nuestro proyecto, creamos un directorio `data` y un archivo dentro, que montaremos dentro de uno de los servicios:

   ```bash
   ~/compose01$ mkdir data
   $ touch data/test.txt
   ```
3. Editamos el archivo *docker-compose.yml* y agregamos la referencia a este directorio dentro del servicio *web-server*:

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

   De esta forma, vamos a montar el directorio local `./data` del host, en el direcotrio `/mnt/data` del contenedor `webserver01` que es creado para el servicio `web-server`.
4. Reflejamos los cambios en los servicios:

   ```bash
   ~/compose01$ docker compose up -d
   [+] Running 2/2
    ✔ Container dbserver01   Running                                                    0.0s 
    ✔ Container webserver01  Started                                                    10.2s
   ```

   👉 note que solo se recrea el servicio al cuál se realizaron cambios en su configuración, y el contenedor se reinicia.
5. Si nos conectamos al contenedor, podemos ver que el directorio local fue montado:

   ```bash
   $ docker container exec -it webserver01 bash
   root@e4be32bbc206:/#
   root@e4be32bbc206:/# ls -l /mnt/data
   total 0
   -rw-rw-r-- 1 1000 1000 0 Aug 21 23:17 test.txt
   ```

Esta configuracion dentro de la sección `services:` es análogo a utilizar un `bind mount` que vimos anteriormente. Podemos definir el acceso a disco de esta forma para cada uno de los servicios que lo requieran, pero en muchos casos, puede no ser la mejor opción.

Si quisieramos utilizar la opción de `volumes` de docker, y además poder accederlos desde múltiples servicios, es preferible definirlos utilizando la sección **volumes:**, como veremos a continuación.

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
Dicho volumen es utilizado por el servicio `db-server` existente, así como también por un nuevo servicio `backup-server` que estamos agregando. Ambos servicios utilizan el mismo volumen, pero lo montan internamente en diferentes ubicaciones de cada contenedor.

Refrescamos nuestros servicios (puede demorar algunos segundos):

```bash
~/compose01$ docker compose up -d
[+] Building 0.3s (9/9) FINISHED                                                                                                                docker:default
 => [backup-server internal] load build definition from Dockerfile                                             0.0s
 => => transferring dockerfile: 218B                                                                           0.0s
 => [backup-server internal] load .dockerignore                                                                0.0s
 => => transferring context: 2B                                                                                0.0s
 => [backup-server internal] load metadata for docker.io/library/ubuntu:latest                                 0.2s
 (...)
 => => writing image sha256:a4c75f8c7a55f6a1fdd5daf5d23a68a7ceae892492cde82bc35b334151a3b0cb                   0.0s
 => => naming to docker.io/library/compose01-backup-server                                                     0.0s
[+] Running 4/4
 ✔ Volume "compose01_db-volume"  Created                                                                       0.0s 
 ✔ Container dbserver01          Started                                                                      10.2s 
 ✔ Container backupserver        Started                                                                       0.1s 
 ✔ Container webserver01         Started                                                                      10.2s 


~/compose01$ docker container ls
CONTAINER ID   IMAGE                     COMMAND             CREATED          STATUS         PORTS     NAMES
4e67b073af90   compose01-web-server      "/bin/sh -c bash"   20 seconds ago   Up 8 seconds             webserver01
803e0e6580e1   compose01-db-server       "/bin/sh -c bash"   30 seconds ago   Up 9 seconds             dbserver01
3a2ac58f8470   compose01-backup-server   "/bin/sh -c bash"   30 seconds ago   Up 9 seconds             backupserver

```

Podemos ver que además de crear el nuevo servicio `backupserver`, se crea también un volumen:

```bash
$ docker volume ls
DRIVER              VOLUME NAME
local               compose01_db-volume
```

Nuevamente, podemos conectarnos a ambos contenedores y acceder al volumen en el punto de montaje correspondiente:

```bash
$ docker container exec -it dbserver01 bash
root@6dae219d5ac6:/# 
root@6dae219d5ac6:/# cd /base
root@6dae219d5ac6:/base# touch archivo1.txt
root@6dae219d5ac6:/base# ls -l
total 0
-rw-r--r-- 1 root root 0 Aug 22 01:06 archivo1.txt
root@6dae219d5ac6:/base# exit


$ docker container exec -it backupserver bash
root@94f5d5cb6abb:/# 
root@94f5d5cb6abb:/# ls -l /backup/base/
total 0
-rw-r--r-- 1 root root 0 Aug 22 01:06 archivo1.txt
root@94f5d5cb6abb:/# exit

```

#### Accediendo a volumenes mediante driver específico

Si vemos nuevamente el *docker-compose.yml* dentro de la sección `volumes:`, la entrada `db-volume:` que creamos se encuentra vacía. Por lo cual para acceder a dicho volumen se va a utilizar el driver por defecto del Docker Engine, que como ya vimos, generalmente es el driver `local`.

```bash
volumes:
  db-volume:
```

Podemos en cambio especificar que driver queremos utilizar, así como pasarle las opciones necesarias al mismo.
Por ejemplo, podemos utilizar el driver *sshfs* que ya vimos anteriormente [aquí](https://github.com/conapps/Devops-101/blob/master/Docker-101/3_Storage.md#volumenes-con-drivers-creados-por-los-usuarios), para montar un volumen desde un servidor ssh.

```bash
volumes:
  ssh-volume:
    driver: vieux/sshfs:latest
    driver_opts:
      sshcmd: "ubuntu@sshserver.labs.conatest.click:/home/ubuntu/docker101"
      password: "conatel_docker101"
```

#### Accediendo a volumenes externos

En los casos anteriores, el comando `docker compose up` se encarga de crear el volumen que definimos dentro de la sección `volumes:` del archivo `docker-compose.yml`. Esto lo verificamos al hacer un `docker volume ls`. Pero si ya tuvieramos un volumen previamente definido e intentáramos accederlo de esta forma, vamos a obtener un error.

Para esto, podemos acceder a volumenes externos que hayan sido definidos previamente, en cuyo caso el comando `docker-compose up` no intentará crear el volumen, sino que buscará el volumen ya creado y lo montará en el servicio. Claro que, en caso de que el volumen no exista, el deploy terminará con error.

Para definir un volumen como externo en `docker-compose.yml` le agregamos la opción `external: true`

```bash
volumes:
  mi-volumen-externo: 
    external: true
```

En este caso buscará  un [volumen](https://github.com/conapps/Devops-101/blob/master/Contenedores/3_Storage.md#volumenes) ya definido previamente con nombre `mi-volumen-externo`.

#### Eliminación de volumenes

Si bajamos el ambiente con `docker compose down`, por defecto los volumenes creados en la sección `volumes:` **no son eliminados.** Este es el comportamiento por defecto, para evitar una posible perdida de datos accidental. Si queremos forzar su eliminación debemos agregarle la opción  `-v` o `--volumes`.

> ⚠️ tenga en cuenta que esto eliminará todos los datos contenidos en el volumen.

```bash
~/compose01$ docker compose down --volumes
[+] Running 5/5
 ✔ Container backupserver      Removed                                                                       10.2s 
 ✔ Container webserver01       Removed                                                                       10.3s 
 ✔ Container dbserver01        Removed                                                                       10.1s 
 ✔ Volume compose01_db-volume  Removed                                                                        0.0s 
 ✔ Network compose01_default   Removed                                                                        0.1s
 

~/compose01$ docker volume ls
DRIVER               VOLUME NAME
local                mi-volumen-externo

```

Los volumenes definidos como externos nunca son eliminados desde docker compose (y tampoco las redes externas).


### Definición de Networks:

Por defecto, cuando desplegamos nuestro ambiente el comando `docker compose up` crea una única network de tipo `bridge,` y agrega cada contenedor del compose file a la misma (en nuestro ejemplo `compose01_default).`

```bash
$ docker network ls
NETWORK ID          NAME                DRIVER              SCOPE
ecdf172b3adf        bridge              bridge              local
db68a213cd9c        compose01_default   bridge              local
4b6f37984b56        host                host                local
b9b7a573b4d0        none                null                local
```

Como consecuencia, todos los contenedores pueden conectarse entre si, y además pueden descubrirse por DNS utilizando su nombre:

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

Si bien esto puede ser muy útil, en una ambiente en producción podría ser necesario restringir o segmentar esta conectividad, de modo que cada servicio pueda comunicarse únicamente con aquellos otros servicios que sea estrictamente necesario.

Para esto, dentro de la sección **networks:** del compose file podemos crear nuestras propias redes, y así definir nosotros la conectividad entre los servicios.

**Ejercicio 21:**

Como vimos antes, nuestro *docker-compose.yml* crea los servicios `db-server`, `web-server`, y `backup-server`. En este ejercicio queremos modificar la conectividad, de forma que `db-server` se pueda comunicar con `web-server` y `backup-server`, pero, no queremos que `web-server` y `backup-server` se comuniquen entre si.

Para esto vamos a crear dos redes en forma manual (*custom networks*):

1. Primero bajemos nuestros servicios con `docker compose down`.
   Si bien podemos dejarlos arriba y luego actualizarlos, será mas claro si lo hacemos de este modo, y aprovechamos a eliminar la default network:

   ```bash
   ~/compose01$ docker compose down
   [+] Running 4/3
    ✔ Container webserver01      Removed                                                                                 10.3s 
    ✔ Container backupserver     Removed                                                                                 10.3s 
    ✔ Container dbserver01       Removed                                                                                 10.1s 
    ✔ Network compose01_default  Removed                                                                                  0.1s 

   ```
2. Editamos el *docker-compose.yml* y en la sección *networks:* agregamos dos redes llamadas `prod-network` y `backup-network`.
   Y dentro de la configuración de cada servicio, colocamos la *networks:* a las cuales queremos que el servicio acceda.

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

   Ambas redes las definimos con el driver `bridge` (el cuál vimos [aqui](https://github.com/conapps/Devops-101/blob/master/Docker-101/4_Networking.md#bridge)), y dado que no estamos indicando ninguna configuración adicional, es el Docker Engine quien asignará los rangos de direcciones IP a las redes, y las direcciones IP específicas a los servicios por DHCP.

   De esta forma, la red `prod-network` conecta únicamente los servicios `db-server` y `web-server`, mientras que la red `backup-network` conecta a `backup-server` y `db-server`; pero no hay ninguna red que conecte a `web-server` con `backup-server` por lo cual estos dos servicios no podrán comunicarse entre si.
3. Ahora despleguemos nuestro ambiente, y verifiquemos la comunicación entre los servicios:

   ```bash
   ~/compose01$ docker compose up -d
   [+] Running 5/5
    ✔ Network compose01_prod-network    Created                                                                                                              0.1s 
    ✔ Network compose01_backup-network  Created                                                                                                              0.1s 
    ✔ Container dbserver01              Started                                                                                                              0.1s 
    ✔ Container backupserver            Started                                                                                                              0.1s 
    ✔ Container webserver01             Started                                                                                                              0.1s 


   ~/compose01$ docker network ls
   NETWORK ID     NAME                       DRIVER    SCOPE
   d48e5d4b5c06   bridge                     bridge    local
   4a05c8ae4c7d   compose01_backup-network   bridge    local
   7ad6c8fb38fb   compose01_prod-network     bridge    local
   c380168e50b7   host                       host      local
   97fb097f7b1f   none                       null      local

   ```

   Podemos ver el detalle de cada una de las redes mediante el comando `docker network inspect`, y así saber por ejemplo que contenedor se encuentra conectado a cada red.

   También podemos conectarnos a los contenedores y probar la comunicación entre ellos:

   ```bash
   $ docker container exec -it backupserver bash
   root@f7397251a392:/#
   root@f7397251a392:/# ping dbserver01
   PING dbserver01 (192.168.0.3) 56(84) bytes of data.
   64 bytes from dbserver01.compose01_backup-network (192.168.0.3): icmp_seq=1 ttl=64 time=0.056 ms
   64 bytes from dbserver01.compose01_backup-network (192.168.0.3): icmp_seq=2 ttl=64 time=0.054 ms
   ^C

   root@f7397251a392:/# ping webserver01
   ping: webserver01: Temporary failure in name resolution

   ```

#### Configuración de *custom networks*:

Dentro de la sección **networks:** también podemos establecer configuraciones adicionales para las redes que definimos. Por ej. especificar que rangos de direcciones IP queremos utilizar para cada red:

```bash
networks:
  prod-network:
    driver: bridge
    ipam:
      driver: default
      config:
        - subnet: 172.16.0.0/24   
```

Y en la sección **services:**, podemos configurar determinadas opciones de red para los servicios, por ej. asignarle una dirección IP específica:

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

#### Accediendo a redes externas:

Si ya tenemos una red previamente definida en docker (algo que vimos [aqui](https://github.com/conapps/Devops-101/blob/master/Docker-101/4_Networking.md#redes-definidas-por-el-usuario)) y queremos utilizarla para nuestros servicios, podemos referenciarla de la siguiente manera:

```bash
networks:
  mi-red-externa: 
    external: true
```

#### Eliminación de *custom networks*:

Si bajamos el ambiente con `docker compose down`, las *custom network* que definimos dentro del *docker-compose.yml* serán eliminadas por defecto:

```bash
$ docker-compose down
Stopping webserver01  ... done
Stopping backupserver ... done
Stopping dbserver01   ... done
Removing webserver01  ... done
Removing backupserver ... done
Removing dbserver01   ... done
Removing network compose01_prod-network
Removing network compose01_backup-network

```

Pero como indicamos antes, **ni las redes externas ni los volúmenes externos son eliminados por defecto** cuando bajamos nuestros servicios con `docker compose down`.

---

**Referencias:**

* Overview of Docker Compose: [https://docs.docker.com/compose/](https://docs.docker.com/compose/)
* Compose file version 3 reference: [https://docs.docker.com/compose/compose-file/](https://docs.docker.com/compose/compose-file/)
* docker-compose command options: [https://docs.docker.com/compose/reference/](https://docs.docker.com/compose/reference/)

---

| [&lt;-- Volver](4_Networking.md) |
