# Docker

_Fuentes:_

- [Documentación oficial](https://docs.docker.com/)
- [Página de Docker](https://www.docker.com/)

## Indice.

---

- [Introducción](#introduccion)
- [Imágenes y contenedores](2_Images.md)
- [Storage](3_Storage.md)
- [Networking](4_Networking.md)
- [Docker compose](5_Docker-Compose.md)

## Introduccion

---

## ¿Qué es Docker?

Docker es la implementación líder de una tecnología llamada Linux containers. Los desarrolladores utilizan contenedores para eliminar los conflictos que se originan al trabajar en la máquina propia mientras colaboran con otros desarrolladores.
Los contenedores también facilitan la puesta en producción y la operación de las aplicaciones.

Mas específicamente, los contenedores son una tecnología, similar a las máquinas virtuales, que permiten automatizar el seteo de un ambiente de desarrollo para el programador. De esta forma, el programador ya no tiene que pasar horas customizando el sistema operativo e instalando dependencias, sino que puede utilizar uno o varios contenedores que ya tienen toda la customización necesaria. Una ventaja adicional es que los contenedores nos permiten experimentar libremente sin preocuparnos por "romper" nuestra máquina.

Los contenedores se han vuelto extremadamente populares porque son ideales para implementar aplicaciones con una arquitectura de microservicios. A diferencia de la arquitectura monolítica tradicional donde hay una base única de código para toda la aplicación, la arquitectura de microservicios implementa varios servicios diferentes, que resuelven pequeños problemas y que cada uno tiene base de código distinta. Una aplicación hoy en día puede estar compuesta por decenas de microservicios que se comunican entre sí.

![alt text](Imagenes/microservicios.jpg "Arquitectura de Microservicios")

## Terminología.

**imagen:** una imagen es un archivo (técnicamente son varios) que contiene todo lo necesario para correr un contenedor. Para quien esté familiarizado con la tecnología de máquinas virtuales esto es similar a un .ova/.ovf

**contenedor** un contenedor es una instancia viva de una imagen. Haciendo una analogía con la tecnología de máquinas virtuales esto sería algo similar a una máquina virtual propiamente dicha. Un contenedor corre un comando o un script nativamente sobre el Kernel del sistema operativo (compartido para todos los contenedores del host), a diferencia de la tecnología de máquinas virtules donde se implementa un sistema operativo completo para cada una. Por tal motivo los contenedores son mucho mas "livianos" que las máquinas virtuales.

## Contenedores vs Máquinas virtuales

### Arquitectura de máquinas virtuales.

![alt text](Imagenes/VM_Architecture.png "Arquitectura de máquinas virtuales")

### Arquitectura de contenedores.

![alt text](Imagenes/Container_Architecture.png "Arquitectura de contenedores")

La diferencia principal entre los contenedores y las máquinas virtuales es que las máquinas virtuales corren un sistema operativo completo cada una, mientras que los contenedores comparten el kernel del host. La única información necesaria en una imagen de Docker es la aplicación misma y sus dependencias. Por este motivo, las imagenes de docker son órdenes de magnitud mas pequeñas que un archivo ovf/ova.

### Ventajas principales

- Uso mas eficiente de recursos (CPU, Memoria).
- Menor consumo de disco.
- Levantan mucho mas rápido.
- Fácilmente automatizables.
- Ideales para arquitectura de microservicios.
- Se puede tratar la infraestructura como código.

## Contenedores y Máquinas virtuales

Cómo vimos anteriormente y como veremos también mas adelante, los contenedores presentan muchas ventajas respecto de las máquinas virtuales pero también algunas limitantes (aunque cada vez menos).

Por otro lado, ¿que sucede si quiero utilizar contenedores pero toda mi infraestructura se encuentra virtualizada mediante virtualización tradicional?

![alt contenedores_y_vms](Imagenes/containers-vms-together.png "Contenedores y VMs juntos")

Como se ve en el diagrama mas arriba, no existe ningún inconveniente en que co-existan la virtualización mediante contenedores y la virtualización tradicional, de hecho es posible que en algunos escenarios esto sea lo recomendado.

## Docker engine

El motor de Docker, tal como se instala típicamente, consiste de tres componentes:

- Server (`dockerd`)
- REST API
- Client o "docker cli" (`docker`)

![alt docker_engine](Imagenes/engine-components-flow.png)

El **Server** es el demonio de Docker propiamente dicho, podremos verlo como un proceso llamado `dockerd` dentro del sistema. Este es quien se encarga de crear y gestionar "objetos" de Docker como ser **imágenes, contenedores, redes y volúmenes**.

El **server** dispone de una API REST para recibir instrucciones y brindar información a otras piezas de software.

El **client** o **docker cli**, es una línea de comandos disponible para el usuario. Esta recibe las instrucciones del usuario a través de comandos y las traduce a mensajes HTTP a ser enviados a la API REST. En otras palabras, oculta al usuario la complejidad (del servidor y su API) presentando un conjunto de comandos a través de los cuales gestionar Docker.

## Instalación

En caso de querer instalar Docker, (`dockerd`, API y `docker`), en la máquina local se pueden seguir estas [instrucciones](https://docs.docker.com/install/). Para este curso no utilizaremos Docker localmente sino que accederemos a un ambiente en la nube donde tendremos Docker pre-instalado.

## DockerHub

[DockerHub](http://dockerhub.com) es un repositorio, típicamente público, aunque también puede ser privado, de imágenes de contenedores Docker. En DockerHub hay mas de 100.000 imágenes públicas, desarrolladas por la comunidad que están disponibles para bajar. Dentro de estas imagenes se encuentran las aplicaciones mas comunes que utilizaremos cuando estemos desarrollando como ser: NGINX, MySQL, PostgreSQL, Ubuntu, Python, Node.js, haproxy, etc.

DockerHub está integrado de forma nativa dentro de Docker, por lo que al instalar este último ya tendremos acceso de forma automática a las imágenes públicas de DockerHub, aún sin tener una cuenta registrada.

## Acceso al ambiente de trabajo

Como se mencionó anteriormente, en esta capacitación no trabajaremos directamente sobre las notebooks, sino que cada estudiante tendrá acceso a un servidor en la nube desde donde se realizarán los laboratorios.

Los servidores disponibles (del 1 al N depeniendo de la cantidad de estudiantes) siguen la siguiente convención de nombres:

```
servernum1.labs.conatest.click
servernum2.labs.conatest.click
...
servernumN.labs.conatest.click
```

Cada estudiante accederá únicamente al servidor asignado (la asignación la hará el instructor al momento de la capacitación).

Previo al inicio del curso, debe haber recibido por mail los certificados para conectarse al equipo. Estos son `devops101-labs.pem` el cuál se utiliza directamente con ssh, y `devops101-labs.ppk` el cual se utiliza con el cliente Putty (en Windows). En caso de no haberlo recibido, consulte al instructor.

#### Como acceder desde Linux/MacOS

Para acceder al servidor de trabajo desde linux o Mac, se debe descargar el certificado (.pem) y colocarle permisos de solo lectura únicamente para el usuario. Esto se hace de la siguiente manera:

```bash
$ chmod 400 devops101-labs.pem
```

Luego se utiliza el comando `ssh` para acceder al servidor, sustituyendo la X por el número de POD asignado, de acuerdo al mail recibido.

```bash
$ ssh -i devops101-labs.pem ubuntu@servernumX.labs.conatest.click
```

#### Como acceder desde Windows

Desde Windows, se puede acceder de dos formas.

La primera es utilizando `Windows Power Shell`:

- Descargar a la notebook el certificado (.pem) recibido y coloclarlo en una carpeta de fácil acceso.
- Abrir la aplicación `Windows Power Shell`, y ubicarse en dicha carpeta.
- Utilizar el comando `ssh` tal como lo haríamos para Linux en el caso anterior:
  ```bash
  > ssh -i devops101-labs.pem ubuntu@servernumX.labs.conatest.click
  ```

La segunda opción es utilizando la herramienta `Putty`:

- Descargar a la notebook el certificado (.ppk) recibido.
- Instalar [Putty](https://www.chiark.greenend.org.uk/~sgtatham/putty/) y abrirlo.
- Dentro del panel "Category" elegir "Session" y luego completar los siguientes campos:

  ```bash
  hostname: ubuntu@servernumX.labs.conatest.click
  connection-type: ssh
  port: 22
  ```
- Dentro de "Category" --> "Connection" --> "SSH" --> "Auth" seleccionar "Browse" y elegir el certificado `devops101-labs.ppk`
- Opcional: puede grabar la configuración de la sesión mediante "Save" para poder volver a utilizarla luego.
- Seleccionar "Open" para conectarse, y luego "Accept" para aceptar la Security Alert.

## Docker cli

Docker se controla a nivel local mediante una interfaz de línea de comandos (cli), que por debajo interactúa con el Docker daemon a traves de la API.

### Standalone Commands vs Management Commands

Debido a su desarrollo y evolución, la `docker cli` cuenta con dos tipos de comandos diferentes, que permiten realizar las mismas tareas de dos formas.
En las primeras versiones, la `cli` contaba con una serie de comandos independientes (que siguen siendo válidos) denominados `Standalone Commands`. Suelen ser comandos de tipo "verbos", como por ejemplo `docker run`, `docker pull`, `docker build`, que en general realizan una acción específica. Sin embargo, a medida que la plataforma crecía y se agregaban nuevas funcionalidades, resultaba cada vez mas difícil encontrar "verbos" adecuados para poder reflejar las mismas.

A partir de la versión 1.13+, la `docker cli` evolucionó, para incluir un nuevo conjunto de comandos denominados `Management Commands`,  con el objetivo es agrupar los comandos para que puedan adecuarse a las nuevas funcionalidades y sean mas sencillos de recordar. Los `Management Commands` suelen comenzar con "sustantivos" que se asocian con los diversos componentes de la plataforma, por ejemplo `docker container` o `docker image` seguidos de subcomandos en forma de "verbos", que se asocian a la acción que se realiza, por ejemplo `docker container run` o `docker image ls`.

A lo largo de esta guía trataremos de utilizar en la mayoría de los casos los relativamente nuevos `Management Commands`, pero como la misma también ha ido evolucionando desde las primeras versiones del curso hace varios años, es posible que en algunos lugares todavía se haga referencia al antiguo set de Standalone Commands, los cuales de todas formas siguen siendo válidos.

Simplementa a modo de ejemplo, si quisieramos listar los contenedores que están corriendo actualmente, utilizando los `Management commands` ejecutaríamos:

```bash
$ docker container ls
```

mientras que con los Standalone Commands sería:

```bash
$ docker ls
```


### Ayuda: `docker help`

Una de las fuentes importantes de referencia es la propia ayuda que proporciona la propia cli, al ejecutar el comando `docker help`:

```bash
$ docker help
(...)

Management Commands:
  config      Manage Docker configs
  container   Manage containers
  image       Manage images
(...)

Commands:
  attach      Attach local standard input, output, and error streams to a running container
  build       Build an image from a Dockerfile
  commit      Create a new image from a container's changes
  cp          Copy files/folders between a container and the local filesystem
  create      Create a new container
  diff        Inspect changes to files or directories on a container's filesystem
  events      Get real time events from the server
  exec        Run a command in a running container
(...)
 

```



Y podemos también obtener detelles específicos de un Management Command, por ejemplo:

```bash
$ docker container --help
Usage:  docker container COMMAND

Manage containers

Commands:
  attach      Attach local standard input, output, and error streams to a running container
  commit      Create a new image from a container's changes
  cp          Copy files/folders between a container and the local filesystem
  create      Create a new container
  diff        Inspect changes to files or directories on a container's filesystem
  exec        Run a command in a running container
  export      Export a container's filesystem as a tar archive
  inspect     Display detailed information on one or more containers
(...)
```



O bajar mas de nivel a un comando específico, por ejemplo:


```
$ docker container ls --help
Usage:  docker container ls [OPTIONS]

List containers

Aliases:
  ls, ps, list

Options:
  -a, --all             Show all containers (default shows just running)
  -f, --filter filter   Filter output based on conditions provided
      --format string   Pretty-print containers using a Go template
  -n, --last int        Show n last created containers (includes all states) (default -1)
  -l, --latest          Show the latest created container (includes all states)
      --no-trunc        Don't truncate output
  -q, --quiet           Only display container IDs
  -s, --size            Display total file sizes
```




Comencemos por conocer los comandos mas comunes disponibilizados por Docker a través de su **cli**.


### Cómo crear un contenedor: `docker run`

> Genera un contenedor a partir de una imagen y lo pone a correr.

La forma genérica del comando es `docker run` + `argumentos (opcional)` + `nombre de la imagen` + `comando a correr (opcional)`. En caso de no proporcionar el comando a correr se correrá el comando por defecto de la imagen en cuestión, mas sobre esto mas adelante.

Aquí hay que tener cuidado en no dejarse engañar por el nombre del comando, si bien el mismo se llama `run`, no se utiliza para poner a correr un contenedor sino que se utiliza para crearlo.

> **Nota:** al ejecutar `docker run`, por defecto, además de ser creado, el contenedor se pone a correr. De hecho la mejor forma de pensar la utilidad de este comando es que sirve para: "correr un comando en un **nuevo contenedor**"

El comando `docker run` primero busca la imagen localmente y en caso de no encontrarla va a buscarla a un registro de imágenes, por defecto DockerHub.

#### Ejemplo:

```bash
$ docker run hello-world
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
9db2ca6ccae0: Pull complete
Digest: sha256:4b8ff392a12ed9ea17784bd3c9a8b1fa3299cac44aca35a85c90c5e3c7afacdc
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/engine/userguide/

```

Como se puede apreciar en la primera línea de la salida del comando, dado que la imagen `hello-world:latest` no se encuentra localmente, el demonio de Docker la descarga desde [dockerhub](https://hub.docker.com/)

> **Nota:** cada imagen tiene una etiqueta asignada que sirve para que el creador de dicha imagen pueda identificar diferentes versiones de la misma. La etiqueta se especifica colocando `:` inmediatamente después del nombre de la imagen, seguido de la etiqueta en si misma de la siguiente forma `nombredelaimagen:etiqueta`.
>
> En caso de que se omita el nombre de la etiqueta, Docker utiliza `latest`.

#### Opciones de `docker run`

El comando `docker run ` acepta varias opciones, a continuación repasaremos las mas comunes.

##### Opción `-it`

El comando `docker run` tiene un par de opciones que usualmente se utilizan en conjunto, estas son `-i` y `-t`. La opción `-i` (`--interactive`) mantiene `STDIN` abierto para el contenedor, lo que se traduce en que podremos utilizar nuestro teclado para enviarle comandos. Por otro lado, la opción `-t` (`--tty`) asigna una `tty` al contenedor, lo que en otras palabras quiere decir que tendremos acceso a una terminal de linux cuando vayamos a interactuar a través de `STDIN, STDOUT, STDERR` con el contenedor.

##### Ejercicio 1

Partiendo de la imagen llamada `ubuntu` levantar un contenedor que corra una terminal de bash (`/bin/bash`) en modo interactivo.

##### Opción `-d`

La opción `-d` (`--detach`) indica a Docker que el contenedor debe de correr en segundo plano, como si fuese un servicio. Esto es útil cuando el contenedor que estamos creando no necesita interacción por parte del administrador y fue creado para correr en background sirviendo requests de clientes, por ejemplo un servidor Web, DNS, DHCP, etc.

El siguiente ejemplo muestra como correr un servidor web NGINX en segundo plano:

```bash
$ docker run -d nginx
9a95e5d34baa8af84eec14569a4966cb40690cafe0c0b28034eb5c9c1d829fd2
$
```

##### Opción `--name`

Esta opción permite darle un nombre al contenedor que estamos creando. En caso de que no se le brinde un nombre, Docker asignará uno generado randómicamente. El nombre permite ejecutar diferentes acciones sobre el contenedor de forma nemotécnica. Lo veremos en detalle mas adelante.

##### Opción `--rm`

Esta opción le indica a Docker que el contedor debe ser eliminado una vez que se detenga. Por defecto los contenedores permanecen en el sistema una vez apagados.

##### Opción `-p`

Esta opción mapea un puerto del contenedor a un puerto del equipo host. Se utiliza cuando se necesita publicar externamente el servicio que proporciona el contenedor. Si por ejemplo tuvieramos un contenedor corriendo un servidor web esuchando en el puerto 8080 y quisieramos publicar dicho servicio en la máquina `host` utilizando el puerto 80, agregaríamos la opción `-p 80:8080`. Veremos la opción `-p` en mas detalle en la sección [Networking](4_Networking.md)

##### Opción `-e`

Esta opción mapea un puerto del contenedor a un puerto del equipo host. Se utiliza cuando se necesita publicar externamente el servicio que proporciona el contenedor. Si por ejemplo tuvieramos un contenedor corriendo un servidor web esuchando en el puerto 8080 y quisieramos publicar dicho servicio en la máquina `host` utilizando el puerto 80, agregaríamos la opción `-p 80:8080`. Veremos la opción `-p` en mas detalle en la sección [Networking](4_Networking.md)

### Cómo listar los contenedores: `docker ps`

El comando:

```bash
$ docker ps
```

lista los contenedores que están corriendo, por lo tanto, si lo ejecutamos con un contenedor corriendo deberíamos ver algo así:

```bash
$ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS      NAMES
7ed9736d1ec5        nginx               "docker-entrypoint.s…"   3 minutes ago       Up 3 minutes        80/tcp     friendly_bartik
```

Como puede verse, cada contenedor tiene un ID autogenerado, así como un nombre (autogenerado o asignado con la opción `--name`).
Estos campos son fundamentales dado que los utilizaremos en cada vez que nos querramos referir a un contenedor para ejecutar alguna acción.

Para listar todos los contenedores del sistema, estén corriendo o no, se agrega la opción `-a` de la siguiente manera:

```bash
$ docker ps -a
```





Cómo apagar un contenedor: `docker stop`

Para apagar un contenedor que está corriendo se puede ejecutar `docker stop` seguido del nombre o el id del contenedor. Por ejemplo:

```bash
$ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS      NAMES
7ed9736d1ec5        nginx               "docker-entrypoint.s…"   3 minutes ago       Up 3 minutes        80/tcp     friendly_bartik

$ docker stop friendly_bartik
friendly_bartik

$ docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES

```


> **Nota:** asignar nombres nemotécnicos a los contenedores nos evita tener que listarlos previamente para obtener su ID o su nombre autogenerado para poder ejecutar comandos sobre el mismo, como por ejemplo apagarlo.

### Cómo encender un contenedor que se encuentra apagado: `docker start`

Para prender un contenedor que se encuentra apagado podemos ejecutar `docker start` seguido del nombre del contenedor o su ID.

##### Ejemplo

```bash
$ docker ps -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              	PORTS   NAMES
7ed9736d1ec5        nginx               "docker-entrypoint.s…"   3 minutes ago       xited (0) 2 minutes ago    	friendly_bartik

$ docker start 7ed9736d1ec5
7ed9736d1ec5

$ docker container ls
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS          NAMES
7ed9736d1ec5        nginx               "docker-entrypoint.s…"   4 minutes ago       Up 1 second         80/tcp   	friendly_bartik
```


> **Nota:** asignar nombres nemotécnicos a los contenedores nos evita tener que listarlos previamente para obtener su ID o nombre autogenerado para poder apagarlos.



### Cómo borrar un contenedor: `docker rm`

Ya vimos como prender y apagar un contenedor, pero ¿qué sucede cuando ya no lo necesitamos?. Los contenedores pueden eliminarse del sistema con el comando `$ docker rm <nombre-del-contenedor/id-del-contenedor>`. Esto elimina el container por completo por lo que al ejecutar `$ docker ps -a` tampoco lo veremos:

```bash
$ docker rm 7ed9736d1ec5
7ed9736d1ec5

$ docker ps -a
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
```

> **Nota:** Es importante notar que este comando elimina el contenedor pero no la imagen de la cual el contenedor proviene. Esto quiere decir que si nosotros quisieramos volver a correr el contenedor, la imagen se encuentra almacenada localmente y por tanto no es necesario descargarla nuevamente.

De esta forma, si volvieramos a crear un contenedor previamente eliminado, a diferencia de la primera vez donde `dockerd` tuvo que descargar la imagen, el contenedor se crearía de forma prácticamente instantánea. Veámos un ejemplo:

1. Creo un contenedor cuya imagen no se encuentra localmente

```bash
docker run -d -it ubuntu
Unable to find image 'ubuntu:latest' locally
latest: Pulling from library/ubuntu
124c757242f8: Pull complete
2ebc019eb4e2: Pull complete
dac0825f7ffb: Pull complete
82b0bb65d1bf: Pull complete
ef3b655c7f88: Pull complete
Digest: sha256:72f832c6184b55569be1cd9043e4a80055d55873417ea792d989441f207dd2c7
Status: Downloaded newer image for ubuntu:latest
d83cb28ee25cc1abda77f8f45248d3f80e4c42f93ddde9cd5338739498e9e66e

```

2. Listo el contenedor y luego apago y lo elimino

```bash
ubuntu@serverNum1:~$ docker container ls
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
d83cb28ee25c        ubuntu              "/bin/bash"         3 seconds ago       Up 2 seconds                            pedantic_bell

ubuntu@serverNum1:~$ docker container stop pedantic_bell
pedantic_bell

ubuntu@serverNum1:~$ docker container rm pedantic_bell
pedantic_bell
```

3. Vuelvo a crear el contenedor, lo cuál esta vez es inmediato, dado que la imagen ya se encuentra presente de forma local

```bash
ubuntu@serverNum1:~$ docker container run -d -it ubuntu
b1332396d3fbfe3629a3c3fe5d829995e9d9fd8642bfd234b929e887fb7a81ed


```

4. Listo el nuevo contenedor

Notemos que al ejecutar `$ docker ps` que el ID ahora es diferente dado que se trata de otro contenedor.

```bash

ubuntu@serverNum1:~$ docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
b1332396d3fb        ubuntu              "/bin/bash"         4 seconds ago       Up 3 seconds                            relaxed_lichterman
```



### Cómo conectarse a un contenedor corriendo en segundo plano: `docker attach`

Cuando un contenedor está corriendo en segundo plano podemos conectar nuestra `STDIN, STDOUT Y STDERR` al mismo, utilizando el comando `docker attach`.

```bash
$ docker container run -itd --rm --name ejemplo_attach ubuntu top
7e0da3c794cb1f64ce0ed20dce277741965dfb1ee96a2990dde9ebeb16b9667d

$ docker container attach ejemplo_attach
root@33c2899ecb9e:/#
top - 20:40:11 up 7 days, 22:10,  0 users,  load average: 1.14, 1.02, 0.98
Tasks:   1 total,   1 running,   0 sleeping,   0 stopped,   0 zombie
%Cpu(s):  5.5 us,  1.8 sy,  0.0 ni, 92.4 id,  0.1 wa,  0.0 hi,  0.3 si,  0.0 st
KiB Mem : 12190548 total,   710936 free,  6855016 used,  4624596 buff/cache
KiB Swap: 12475900 total, 12384984 free,    90916 used.  3590716 avail Mem

  PID USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM     TIME+ COMMAND
    1 root      20   0   36640   3104   2676 R   0.0  0.0   0:00.03 top
```

Una vez "dentro" del contenedor, para desconectarnos debemos ejecutar la combinación de teclas `ctrl+p`, `ctrl+q`. Esto permitirá volver a la máquina `host` y que el contendor siga corriendo. 

##### Ejercicio 2

1. Ejecutar el siguiente comando:

```bash
$ docker run -it -d --name ejercicio2 --rm ubuntu /bin/bash
```

2. Verificar que el contenedor se encuentra corriendo.
3. Conectarse a la consola del contenedor.
4. Una vez dentro de la consola ejecutar el comando `exit`.
5. En el equipo `host`, ejecutar el comando `docker ps` y revisar la salida del mismo. Que puede notar?
6. Volver a ejecutar el paso 1.
7. Conectarse una vez mas a la consola del contenedor.
8. Volver a la consola del equipo `host` pero ahora sin apagar el contenedor.
9. Verificar mediante `docker ps` que el contenedor sigue encendido.
10. Estando en el equipo `host` apagar el contenedor.

### Cómo listar las imágenes: `docker images`

```bash
$ docker images
```

o bien:

```bash
$ docker image ls
```

Muestra las imagenes que hay en el equipo `host` local:

```bash
$ docker images
REPOSITORY                TAG                 IMAGE ID            CREATED             SIZE
nginx                     latest              c246cd3dd41d        5 weeks ago         107.5 MB
hello-world               latest              1815c82652c0        6 weeks ago         1.84 kB
ismaa10/devnetcontainer   latest              d00246b829df        7 weeks ago         488.9 MB
conatel/config-backup     latest              32dde64fc2ca        12 weeks ago        706.8 MB
conatel/config-backup     <none>              fc4791bcc292        3 months ago        706.8 MB
conatel/config-backup     <none>              a2186fa14acc        3 months ago        706.8 MB

```

> **Nota:** estudiaremos las imágenes mas en profundidad el la sección [Imágenes y contenedores](2_Images.md),

### Ejercicio 3

Este ejercicio tiene como objetivo experimentar de primera mano la potencia de los contenedores a la hora de simplificar la puesta en producción de un servicio. Nos referimos mas concretamente al hecho de que una vez que la aplicación fue "contenerizada" tendremos la certeza absoluta que correrá sin problemas en cualquier plataforma que soporte Docker.

Concretamente, el objetivo del ejercicio es poner en producción una aplicación, llamada Ghost, que permite registrarse y publicar Blogs al público en general. Esta plataforma ya fue "contenerizada" y su imagen está diponible públicamente en Dockerhub, bajo el nombre `ghost`.

Cuando corremos un contenedor a partir de dicha imagen, por defecto éste queda "escuchando" en el puerto 2368. Pero para simplificar el acceso de los clientes a la aplicación, el `host` deberá estar escuchando en el puerto `80`.

Para finalizar, presentamos una lista de los requerimientos considerados necesarios para dar por resuelto el ejercicio. Algunos ya fueron mencionados anteriormente, pero se dejan en la lista para facilitar la referencia:

- La imagen a utilizar se llama `ghost.`
- El contendor debe tener un nombre específico, definido por el administrador, en este caso: `ejercicio3`
- El contenedor no debe ser eliminado al apagarse.
- El servicio debe estar publicado al exterior en el puerto 80 (el puerto original es 2368)
- El contenedor debe correr en segundo plano.
- El comando a utilizar es el que viene por defecto con la imagen.

#### Verificación:

- Mediante un navegador acceder a [http://servernumX.labs.conatest.click](http://servernumX.labs.conatest.click), y deberá ver el servicio publicado.
- Apagar el contenedor utilizando `docker stop` y verificar que el servicio ya no está accesible.
- Encender el contenedor utilizando `docker start` y verificar que el servicio vuelve a estar online.


<details>
<summary>Pista #1</summary>
La opción para mapear el puerto del contenedor al host es <code>-p:<puerto_contenedor>:<puerto_host></code>.
</details>

<details>
    <summary>Solución</summary>
    <pre>
# Archivo de inventario: hosts.yml
all:
  vars:
    ansible_ssh_common_args: '-o StrictHostKeyChecking=no'
    ansible_ssh_private_key_file: './master_key'
  hosts:
    host01:
    host02:
    host03:
    </pre>
</details>


### Cómo borrar una imagen: `docker rmi`

Anteriormente vimos como puede eliminarse un contenedor, pero ¿que sucede si además del contenedor quiero eliminar la copia local de la imagen de la cual proviene?
El comando `docker rmi <id-de-la-imagen/nombre-de-la-imagen>` cumple precisamente esta función. Es importante notar que esta operación no puede realizarse mientras haya un contenedor que esté usando esta imagen, aún cuando el mismo esté apagado:

```bash
$ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
7a950a434a1c        ghost               "docker-entrypoint.sh"   4 minutes ago       Up 4 minutes        0.0.0.0:8080->2368/tcp   primer-prueba

$ docker stop primer-prueba
primer-prueba

$ docker rmi ghost
Error response from daemon: conflict: unable to remove repository reference "ghost" (must force) - container 7a950a434a1c is using its referenced image b8fb2fac700b
```

Si queremos borrar una imagen lo correcto es primero eliminar el contenedor y luego la imagen.
En caso de que se quiera borrar la imagen pero mantener el contenedor se puede "forzar" el borrado de la siguiente manera:

```bash
$ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
7a950a434a1c        ghost               "docker-entrypoint.sh"   4 minutes ago       Up 4 minutes        0.0.0.0:8080->2368/tcp   primer-prueba

$ docker rmi ghost --force
b8fb2fac700b
```

[Siguiente--&gt;](2_Images.md)
