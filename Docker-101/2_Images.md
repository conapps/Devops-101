| [&lt;-- Volver](1_Docker.md) |
[Siguiente --&gt;](3_Storage.md) |

```

```

## Imágenes y contenedores

---

Hasta ahora hemos creado contenedores provenientes de imagenes creadas por terceros. Ahora vamos a explorar los pasos necesarios para crear nuestras propias imágenes.

### Docker commit

Supongamos que generamos un container a partir de la última imagen de ubuntu de la siguiente manera:

```bash
$ docker container run --name ejemplo_commit -it ubuntu bash
root@1dbc76e3acdb:/#
```

Esto nos deja posicionados dentro de este nuevo contenedor, gracias a las opciones `-it`. Podemos ver que estamos dentro del contenedor y no dentro de nuestra máquina `host` al observar el prompt, que pasa a ser del estilo `root@1dbc76e3acdb:/#`.

Supongamos ahora que queremos ejecutar un intérprete de Python:

```bash
root@1dbc76e3acdb:/# python3
bash: python3: command not found
```

El problema aquí es que Python no está instalado en el contenedor, dado que la imagen de `ubuntu` por defecto no lo trae. A continuación lo instalamos:

```bash
root@e6387986f32b:/# apt-get update && apt-get install -y python3
Get:1 http://security.ubuntu.com/ubuntu xenial-security InRelease [102 kB]
Get:2 http://archive.ubuntu.com/ubuntu xenial InRelease [247 kB]
Get:3 http://security.ubuntu.com/ubuntu xenial-security/universe Sources [43.0 kB]
Get:4 http://security.ubuntu.com/ubuntu xenial-security/main amd64 Packages [406 kB]
Get:5 http://archive.ubuntu.com/ubuntu xenial-updates InRelease [102 kB]
Get:6 http://security.ubuntu.com/ubuntu xenial-security/restricted amd64 Packages [12.8 kB]
Get:7 http://security.ubuntu.com/ubuntu xenial-security/universe amd64 Packages [187 kB]
Get:8 http://security.ubuntu.com/ubuntu xenial-security/multiverse amd64 Packages [2931 B]
----> SALIDA OMITIDA PARA MAYOR CLARIDAD <---
```

Una vez finalizado el proceso de instalación ya podemos utilizar Python:

```bash
root@e6387986f32b:/# python3
Python 3.10.6 (main, Nov  2 2022, 18:53:38) [GCC 11.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> exit()

root@e6387986f32b:/#
```

En este punto tenemos un contenedor completamente funcional que cumple con todas nuestras necesidades, en este caso únicamente Python.

Pero que sucede si ahora queremos utilizar este contenedor en producción fuera de nuestra máquina local. Esto de hecho es una de las fortalezas mas importantes de la tecnología de contenedores, la posibilidad de crear un ambiente en nuestra máquina local y luego exportar y utilizar dicho ambiente en producción con exactamente los mismos paquetes y dependencias instaladas que lo que tenemos localmente (lo que utilizamos para desarrollar).

El problema aquí es que, en Docker lo que se transporta no son los contenedores sino las imágenes,  y a partir de una imagen se pueden generar cualquier cantidad de contenedores idénticos. Dicho esto, si queremos transportar nuestro nuevo ambiente con Python instalado sobre una distribución Ubuntu, el desafío es generar una nueva imagen, dado que la imagen de la cual partimos no contiene Python.

Para esto utilizaremos el comando `docker container commit <contenedor> <nombre-de-la-nueva-imagen>`, por ejemplo:

```bash
$ docker container commit ejemplo_commit ambiente-produccion
sha256:c2a9520001342c424d141f05c6f13761a74d58edd336f11b7a971c1a1d2ed317

$ docker image ls
REPOSITORY                TAG                 IMAGE ID            CREATED             SIZE
ambiente-produccion       latest              c2a952000134        5 seconds ago       189.2 MB
```

Ahora que tengo una nueva imagen con mi ambiente, podría eliminar el contenedor y volver a regenerarlo, pero utilizando nuestra imagen `ambiente-produccion`. Como se puede ver, el nuevo contenedor ahora tiene Python instalado:

```bash
$ docker container rm ejemplo_commit
ejemplo_commit

$ docker container run --name contenedor_con_python -it ambiente-produccion bash
root@0f66ed1e694d:/# python3
Python 3.10.6 (main, Nov  2 2022, 18:53:38) [GCC 11.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 
>>> exit()

```

#### Ejercicio 4

1. Partiendo de la última imagen de `ubuntu`, generar un contenedor corriendo el proceso `bash` de forma interactiva.
2. Una vez dentro del contenedor, intentar ejecutar el editor de texto `nano` y verficar que no está instalado.
3. Instalarlo y verficar que se puede correr.
4. Utilizando `docker commit` generar una nueva imagen de `Ubuntu` con `nano` instalado.
5. A partir de la nueva imagen, generar un nuevo contenedor y verficiar que se puede correr `nano`.

<details>
    <summary>Solución</summary>

<pre>
   $ docker container run --name ejercicio4 -it ubuntu bash
   root@0f7e17479085:/# nano
   bash: nano: command not found 
</pre>

<pre>
   root@0f7e17479085:/# apt-get update && apt-get install -y nano
   Get:1 http://security.ubuntu.com/ubuntu jammy-security InRelease [110 kB]
   Get:2 http://archive.ubuntu.com/ubuntu jammy InRelease [270 kB]
   Get:3 http://archive.ubuntu.com/ubuntu jammy-updates InRelease [114 kB]
   (...)
   root@0f7e17479085:/#
   root@0f7e17479085:/# nano
   root@0f7e17479085:/# exit
</pre>

<pre>
   $ docker container ls -l
   CONTAINER ID   IMAGE     COMMAND   CREATED         STATUS                     PORTS     NAMES
   0f7e17479085   ubuntu    "bash"    4 minutes ago   Exited (0) 9 seconds ago             ejercicio4
   $
   $ docker container commit ejercicio4 ubuntu_con_nano
   sha256:84a9196c1c28041ee4ac976b28917539209f282025b5dc848f829e70b5822cf6
   $
   $ docker image ls
   REPOSITORY            TAG       IMAGE ID       CREATED          SIZE
   ubuntu_con_nano       latest    84a9196c1c28   8 seconds ago    118MB
</pre>

<pre>
   $ docker container run -it --name ejercicio4_nuevo ubuntu_con_nano
   root@88ebe0cb22f8:/# nano
   root@88ebe0cb22f8:/# exit
</pre>

</details>

### Dockerfile

El método anterior es útil para generar imágenes a partir de contenedores, pero tiene muchas desventajas a la hora de su uso en producción. Es poco flexible, y la imagen no está optimizada para versionarse al igual que hacemos con nuestro código. Profundicemos sobre este punto con un ejemplo.

Supongamos que nuestro ambiente de producción no incluye únicamente Python3, sino también `python3-pip, `
Pensemos en el proceso para armar un ambiente de este tipo; habría que generar un contenedor con Ubuntu, instalar todos estos paquetes y luego hacer un commit. Ahora, ¿qué pasaría si durante nuestro proceso de desarrollo decidimos explorar la posiblidad de cambiar nuestro motor de base de datos de MySQL a PostgreSQL? ¿Cómo haríamos para generar una nueva imágen? Podríamos intentar desinstalar MySQL e instalar PostgreSQL en su lugar, pero veamos que hay dependencias como mysql-connector que sólo tienen sentido si utilizamos MySQL y que deberían también ser desinstaladas para mantener "limpia" nuestra imagen que luego será utilzada en producción. Finalmente habría que instalar los módulos de Python correspondientes para trabajar con una base de datos PostgreSQL y hacer un commit para generar la nueva imagen.

Principales desventajas del enfoque anterior:

- Si la decisión de cambiar a PostgreSQL se toma varias semanas o meses luego de generada la primer imagen, probablemente no recuerde que existían las librerías de Python que Soportan MySQL (mysql-connector) dado que los paquetes que hay instalados en la imagen no quedan documentados en ningún sitio (en realidad se pueden ver con el comando `docker history` pero esto no es práctico).
- Los cambios en los ambientes de desarrollo pueden darse decenas de veces en el transcurso de un proyecto, la desinstalación de módulos y librerías que ya no son necesarias puede volverse una tarea tediosa.
- En general cada cambio en el ambiente de desarrollo viene acompañado por un cambio en el código fuente de nuestra aplicación, lo que nos gustaría poder hacer es versionar nuestro ambiente utilizando los mismos mecanismos (ej.: GIT) que utilizamos para versionar nuestro código. Pero cada nueva imagen generada con el método de `docker commit` pesa cientos de MB y no contiene información de los paquetes que hay instalados en ella.
- Si queremos reutilizar nuestro ambiente para otro desarrollo no tenemos visibilidad de qué software hay instalado en la imagen para poder adaptarlo a las necesidades del nuevo proyecto.
- En caso de que el proceso que necesitamos correr en nuestro contenedor no sea "bash", ni siquiera hay una forma sencilla y directa de generar el ambiente por medio de  `docker commit`.

La solución a los problemas planteados anteriormente es la utilización de un archivo `Dockerfile` para la construcción de nuestra imagen.

Un archivo `Dockerfile` es básicamente un archivo de texto que describe de forma unívoca cuál es el contenido de la imagen. Para entenderlo mejor, veamos como aplicaríamos esta técnica para la creación de la imagen del ejemplo anterior.

El contenido del archivo 'Dockerfile' sería el siguiente:

```dockerfile
FROM ubuntu
LABEL maintainer="cdh@conatel.com.uy"
RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN pip3 install --upgrade pip
RUN pip3 install requests
RUN pip3 install mysql-connector==2.2.9
RUN pip3 install django==1.10
RUN echo "mysql-server mysql-server/root_password password CursoDocker2022." | debconf-set-selections
RUN echo "mysql-server mysql-server/root_password_again password CursoDocker2022." | debconf-set-selections
RUN apt-get install -y mysql-server
RUN apt-get install -y tftpd-hpa
ENV TZ=America/Montevideo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get install -y openssh-server
RUN apt-get install -y nginx
CMD bash
```

Una vez que tenemos el archivo `Dockerfile` creado, lo único que debemos hacer para generar la imagen es guardarlo en un directorio vacío (el cuál se denomina `contexto`), y estando en ese mismo directorio ejecutar el comando `docker build` para crear la imagen:

```bash
$ mkdir prod-env
$ cd prod-env

~/prod-env$ nano Dockerfile
  <copiar el contenido del Dockerfily y grabar el archivo>

~/prod-env$ docker build -t prod-env:0.1 .
Sending build context to Docker daemon   2.56kB
Step 1/19 : FROM ubuntu
 ---> a8780b506fa4
Step 2/19 : LABEL maintainer="cdh@conatel.com.uy"
 ---> Using cache
 ---> 19ca15d6ebac
Step 3/19 : RUN apt-get update
(...)
Step 19/19 : CMD bash
 ---> Using cache
 ---> b7af7d942475
Successfully built b7af7d942475
Successfully tagged prod-env:0.1
```

Este proceso generará una imagen llamada `prod-env:0.1` a partir de la cual podrémos generar la cantidad de contenedores que necesítemos.

> 👉 El `:0.1` hace referencia al tag de la versión que le se asigna a la imagen que estoy creando, lo que me permite versionar diferentes ambientes o configuraciones. Si no lo especificamos, docker le asignará el tag por defecto, que es `:latest`

Este método tiene las siguientes ventajas:

- La especificación de la imagen (el archivo `Dockerfile`) ocupa apenas unos bytes por lo que se vuelve muy sencilla de transportar.
- El archivo `Dockerfile` contiene la información exacta de los paquetes que hay instalados en la imagen, lo que nos sirve de documentación.
- El archivo `Dockerfile` es totalmente versionable con un gestor de código como GIT.
- Si necesitamos hacer un cambio en nuestro ambiente sólo necesitamos modificar las líneas correspondientes del `Dockerfile` y volver a generar la imagen. No es necesario instalar y desinstalar paquetes manualmente.

Ahora, si quisiéramos generar un contenedor a partir de la imagen que construímos anteriormente, podemos ejecutar como siempre:

```bash
$ docker container run -it prod-env:0.1
root@08322e95d53c:/#
```

A continuación indicaremos los principales comandos que se utilizan dentro de un archivo `Dockerfile`:

#### `FROM`

Especifíca la imagen base a utilizar, sobre la cuál se construiría la nueva imagen. En el ejemplo estamos usando `ubuntu`.

#### `LABEL`

Permite agregar metadata de forma arbitraria a la imagen (opcional). Esto puede utilizarse con múltiples propósitos, en este caso particular se está utilizando para indicar el correo del "dueño" de la imagen. Esta medatada puede consultarse luego, cuando el contenedor esté creado, con el comando `docker inspect`.

```bash
$ docker image inspect prod-env:0.1
...
...
"Labels": {
    "maintainer": "cdh@conatel.com.uy"
}
...
...
```

#### `ADD`

Permite agregar un archivo (o directorio) a la imagen que estoy creando. Puede utilizarse por ejemplo, para incluir archivos con datos de configuración que requiera nuestra aplicación.

La sintaxis es `ADD <source> <destination>` siendo `<source>` la ubicación (path) del archivo dentro del directorio `contexto` del equipo host, y `<destination>` la ubicación donde quiero colocar el archivo dentro del contenedor.

Para definir `<source>` se pueden utilizar wildcards. Por ejemplo `ADD configuracion?.txt /data/` agregará al directorio `/data` del contenedor todos los archivos del contexto que comiencen con `configuracion` que luego tengan exactamente un caracter y que terminen con la extensión `.txt`

#### `RUN`

Ejecuta un comando, por defecto con el shell `/bin/sh -c`, agregando el resultado del comando a la imagen que se está construyendo (en una nueva capa).

#### `ENV`

Define una variable de entorno que será disponibilizada dentro del contenedor cuando éste se encuentre corriendo.

#### `CMD`

Indica cuál es el comando que el contenedor va a ejecutar por defecto cuando se ejecute, en caso de que el usuario al crear el contenedor (`docker container run`) no indique un comando específico. Esta línea en general se colocal al final del archivo `Dockerfile.`

#### Ejercicio 5

1. Crear un directorio y navegar hacia él:

```bash
$ mkdir contexto
$ cd contexto
~/contexto$
```

2. Dentro del nuevo directorio crear 3 archivos vacíos, con el comando `touch`, de la siguiente manera:

```bash
~/contexto$ touch archivo1.cfg archivo2.cfg archivo3.cfg
```

3. Dentro del mismo directorio crear un archivo `Dockerfile` con las siguientes líneas:

```dockerfile
FROM ubuntu
ADD <completar>
```

Donde dice `<completar>` se debe escribir, en una única línea, el comando necesario para agregar al directorio `/data` de la imagen los tres archivos creados en el paso 2.

4. Construir una imagen a partir del Dockerfile:

```bash
~/contexto$ docker build -t ejercicio5 .
```

5. Crear un contenedor a partir de la nueva imagen y verificar que los 3 archivos están presentes en `/data`

<details>
    <summary>Solución</summary>
<pre>
   ~/contexto$ cat Dockerfile
   FROM ubuntu
   ADD archivo?.cfg /data/
</pre>
<pre>
   ~/contexto$ docker build -t ejercicio5 .
   Sending build context to Docker daemon  3.584kB
   Step 1/2 : FROM ubuntu
   ---> a8780b506fa4
   Step 2/2 : ADD archivo?.cfg /data/
   ---> 2db5ac716d3d
   Successfully built 2db5ac716d3d
   Successfully tagged ejercicio5:latest
</pre>
<pre>
   ~/contexto$ docker container run -it --rm ejercicio5
   root@f69759d29668:/# cd /data
   root@f69759d29668:/data# ls -la
   total 8
   drwxr-xr-x 2 root root 4096 Nov  7 17:17 .
   drwxr-xr-x 1 root root 4096 Nov  7 17:17 ..
   -rw-rw-r-- 1 root root    0 Nov  7 17:16 archivo1.cfg
   -rw-rw-r-- 1 root root    0 Nov  7 17:16 archivo2.cfg
   -rw-rw-r-- 1 root root    0 Nov  7 17:16 archivo3.cfg
   root@f69759d29668:/data# exit
</pre>
</details>

#### Ejercicio 6

1. Modificar el `Dockerfile` construido en el ejercicio anterior para que tenga una sentencia `RUN` que instale Python de la siguiente manera `apt-get update && apt-get install -y python3 `
2. Volver a construir la imagen.
3. Crear un contenedor a partir de la imagen y verificar que Python está instalado de la siguiente manera:

```bash
root@08f5d92ad130:/# python3
Python 3.5.2 (default, Nov 23 2017, 16:37:01)
[GCC 5.4.0 20160609] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> exit()
root@08f5d92ad130:/#
```

<details>
    <summary>Solución</summary>
<pre>
   ~/contexto$ cat Dockerfile
   FROM ubuntu
   ADD archivo?.cfg /data/
   RUN apt-get update && apt-get install -y python3
</pre>
<pre>
   ~/contexto$ docker build -t ejercicio6 .
   (...)
   Successfully tagged ejercicio6:latest
</pre>
<pre>
   ~/contexto$ docker container run -it --rm ejercicio6
   root@cf9cc50371d9:/# python3
   Python 3.10.6 (main, Nov  2 2022, 18:53:38) [GCC 11.3.0] on linux
   Type "help", "copyright", "credits" or "license" for more information.
   >>> exit()
   root@cf9cc50371d9:/# exit
   exit
</pre>

</details>

#### Ejercicio 7

En este ejercicio haremos que, por defecto, los contenedores creados a partir de nuestra nueva imagen corran python en lugar de `bash`

1. En el Dockerfile que utilizamos en los ejercicios anteriores, agregar una línea al final de la siguiente manera: `CMD python3`.
2. Volver a construir la imagen.
3. Crear un contenedor a partir de la nueva imagen, pero no especificar un comando a ejecutar.
4. Verificar que al crearse, el contenedor nos deja posicionados en el interprete de Python.

<details>
    <summary>Solución</summary>
<pre>
   ~/contexto$ cat Dockerfile
   FROM ubuntu
   ADD archivo?.cfg /data/
   RUN apt-get update && apt-get install -y python3
   CMD python3
</pre>
<pre>
   ~/contexto$ cat Dockerfile
   FROM ubuntu
   ADD archivo?.cfg /data/
   RUN apt-get update && apt-get install -y python3
   CMD python3
</pre>

</details>

#### Ejercicio 8

En este ejercicio exploraremos como utilizar las variables de entorno cambiando el directorio "home" del contenedor.

1. Partiendo del Dockerfile utilizado anteriormente, agregar la siguiente líne `ENV HOME /mi_casa`
2. Luego vamos a crear el directorio `mi_casa` dentro de la imagen agregando al Dockerfile la siguiente línea `RUN mkdir $HOME`
3. Volver a construir la imagen.
4. A partir de la nueva imagen, crear un contenedor y verficiar que al tipear `cd ~` quedamos posicionados dentro del directorio `mi_casa`. (recuerde que en el ejercicio anterior modificó el comando por defecto del contenedor, por lo que ahora para ejecutar `bash` hay que hacerlo explicitamente, o bien volver a colocar bash como comando por defecto en el Dockerfile).

<details>
    <summary>Solución</summary>
<pre>
   ~/contexto$ cat Dockerfile
   FROM ubuntu
   ADD archivo?.cfg /data/
   RUN apt-get update && apt-get install -y python3
   ENV HOME /mi_casa
   RUN mkdir $HOME
   CMD python3
</pre>
<pre>
   ~/contexto$ docker build -t ejercicio8 .
   (...)
   Successfully tagged ejercicio8:latest
</pre>
<pre>
~/contexto$ docker container run -it --rm ejercicio8 /bin/bash
root@2b1b88794be8:/# cd $HOME
root@2b1b88794be8:~# pwd
/mi_casa
</pre>
</details>

### Optimización de la construcción de imágenes

Antes de aprender como escribir nuestro archivo Dockerfile para generar nuestras imágenes de forma mas eficiente, es necesario entender como funciona el proceso de construcción de una imagen a bajo nivel.
Cuando creamos una imagen a partir de un archivo `Dockerfile` con el comando `docker build`, lo que hace básicamente docker es tomar la imagen base especificada en la directiva `FROM` e ir ejecutando de forma secuencial cada uno de los comandos especificados en las directivas `RUN`, y haciendo implícitamente un `docker commit` luego de cada comando, almacenando la imagen resultante en cache local.
Por lo que, al final del día, tendremos almacenada nuestra imagen final y todas las imágenes intermedias que se fueron creando paso a paso para llegar a la misma. Esta estructura de capas puede verse al ejecutar el siguiente comando:

```bash
$ docker history prod-env:0.1
IMAGE          CREATED       CREATED BY                                      SIZE      COMMENT
b7af7d942475   3 hours ago   /bin/sh -c #(nop)  CMD ["/bin/sh" "-c" "bash…   0B      
2f302e662771   3 hours ago   /bin/sh -c apt-get install -y nginx             8.6MB   
1bf221cf985c   3 hours ago   /bin/sh -c apt-get install -y openssh-server    41.6MB  
f235654227fa   3 hours ago   /bin/sh -c ln -snf /usr/share/zoneinfo/$TZ /…   57B     
66aa9c29608d   3 hours ago   /bin/sh -c #(nop)  ENV TZ=America/Montevideo    0B      
b6cc71a365cd   3 hours ago   /bin/sh -c apt-get install -y tftpd-hpa         2.86MB  
2d05553c8655   3 hours ago   /bin/sh -c apt-get install -y mysql-server      559MB   
73da17ec04de   3 hours ago   /bin/sh -c echo "mysql-server mysql-server/r…   1.67MB  
f7366ecbdc7d   3 hours ago   /bin/sh -c echo "mysql-server mysql-server/r…   1.67MB  
91ead6360f5b   3 hours ago   /bin/sh -c pip3 install django==1.10            28.8MB  
8aa8822284d1   3 hours ago   /bin/sh -c pip3 install mysql-connector==2.2…   13.8MB  
0e02ba792d59   3 hours ago   /bin/sh -c pip3 install requests                2.68MB  
961f3c1c8028   3 hours ago   /bin/sh -c pip3 install --upgrade pip           13.8MB  
2f2b52bf5a8e   3 hours ago   /bin/sh -c apt-get install -y python3-pip       319MB   
cc2aeaf7390c   3 hours ago   /bin/sh -c apt-get install -y python3           30.3MB  
321b1b0fd8da   3 hours ago   /bin/sh -c DEBIAN_FRONTEND=noninteractive ap…   4.13MB  
85937b63b384   3 hours ago   /bin/sh -c apt-get update                       39.4MB  
19ca15d6ebac   3 hours ago   /bin/sh -c #(nop)  LABEL maintainer=cdh@cona…   0B      
a8780b506fa4   5 days ago    /bin/sh -c #(nop)  CMD ["bash"]                 0B      
<missing>      5 days ago    /bin/sh -c #(nop) ADD file:29c72d5be8c977aca…   77.8MB 
```

El objetivo de la estructura de capas almacenadas en cache es optimizar el tiempo de construcción de las imagenes y el espacio en disco que consumen los contenedores, mas sobre esto

El objetivo de la estructura de capas almacenadas en cache es optimizar el tiempo de construcción de las imagenes y el espacio en disco que consumen los contenedores. Se puede obtener mas información sobre esto [aquí](https://docs.docker.com/engine/userguide/storagedriver/imagesandcontainers/#images-and-layers).

Este proceso funciona de la siguiente manera: al ejecutar `docker build -t <nombre-de-la-imagen> .`, lo que hace Docker es, antes de ejecutar cada directiva del archivo Dockerfile, fijarse si no hay en cache una imagen derivada de la directiva correspondiente y de todas las anteriores (comenzando por la directiva `FROM` que siempre es la primera).

En caso de que encuentre una imagen que se corresponda con dicha directiva, se saltea el paso de la generación de la misma (porque ya está generada) y pasa a la siguiente directiva. Este proceso se repite hasta que alguna de las imágenes no se encuentre en cache local, en tal caso Docker crea dicha imagen **y todas las sucesivas**. Dicho de otra forma, una imagen está compuesta por capas **read-only** que contienen los archivos resultantes de las directivas ejecutadas desde el archivo Dockerfile; estas capas se construyen una sobre otra, de forma incremental, agregando los archivos "delta" (sólo la diferencia) entre una capa y otra.

Dado que las capas son read-only, si una capa posterior modifica un archivo contenido en una capa anterior, es necesario copiar nuevamente el archivo completo en la capa posterior, siéndo esta última copia la que se utilizará. Esta forma de construir las imágenes como capas una sobre otra, tiene la implicancia de que si modificamos una capa "del medio", será necesario volver a generar todas las capas sucesivas, dado que las capas no son autocontenidas sino que se basan en su capa anterior incluyendo únicamente los "nuevos archivos".

👉 Entender esto es la clave para generar archivos Dockerfile mas eficientes; veámoslo con un ejercicio guiado como ejemplo.

#### `Ejercicio 9`

1. Ubicarse en el directorio `prod-env` que utilizamos previamente en el primer ejemplo.
   ```
   $ cd ~/prod-env
   ```

2. Dentro de este directorio, generar un archivo `config.txt`, el cuál simula ser por ejemplo, un archivo de configuración de nuestra aplicación.
   ```
   ~/prod-env$ touch config.txt
   ```
3. Editar el `Dockerfile` que habíamos utilizado antes, y agregar la sentencia `ADD` para incluir el archivo `config.txt` en nuestra imagen. Asegurarse de poner esta línea al inicio del `Dockerfile`, luego de `LABEL` por ejemplo.

```dockerfile
FROM ubuntu
LABEL maintainer="cdh@conatel.com.uy"
# Colocamos el ADD archivo config.txt al principio del Dockerfile
ADD config.txt /setting/config.txt
RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN pip3 install --upgrade pip
RUN pip3 install requests
RUN pip3 install mysql-connector==2.2.9
RUN pip3 install django==1.10
RUN echo "mysql-server mysql-server/root_password password CursoDocker2022." | debconf-set-selections
RUN echo "mysql-server mysql-server/root_password_again password CursoDocker2022." | debconf-set-selections
RUN apt-get install -y mysql-server
RUN apt-get install -y tftpd-hpa
ENV TZ=America/Montevideo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get install -y openssh-server
RUN apt-get install -y nginx
CMD bash
```

4. Construir la imagen, como una nueva versión, y notar lo largo que es este proceso.
```
   ~/prod-env$ docker build -t prod-env:0.2 .
   Sending build context to Docker daemon  3.072kB
   Step 1/20 : FROM ubuntu
   ---> a8780b506fa4
   Step 2/20 : LABEL maintainer="cdh@conatel.com.uy"
   ---> Using cache
   ---> 19ca15d6ebac
   Step 3/20 : ADD config.txt /setting/config.txt
   ---> 8e914ddf30a5
   Step 4/20 : RUN apt-get update
   (...)
   (...)
   Step 20/20 : CMD bash
   ---> Running in 76f68264dd28
   Removing intermediate container 76f68264dd28
   ---> 4867bf05acca
   Successfully built 4867bf05acca
   Successfully tagged prod-env:0.2
```

5. Modificar el contenido del archivo de configuración `config.txt`
```
   ~/prod-env$ nano config.txt
   Agrego una línea al archivo de configuración.
   <ctrl-X>
```

6. Construir la imagen, como una nueva versión, y observar el proceso.
   Se puede ver que todas las capas a partir del comando `ADD` son reconstruidas nuevamente, mientras que solo las primeras dos sentencias `FROM` y `LABEL` son tomadas del cache
   
```
   ~/prod-env$ docker build -t prod-env:0.3 .
Sending build context to Docker daemon  3.584kB
Step 1/20 : FROM ubuntu
 ---> a8780b506fa4
Step 2/20 : LABEL maintainer="cdh@conatel.com.uy"
 ---> Using cache
 ---> 19ca15d6ebac
Step 3/20 : ADD config.txt /setting/config.txt
 ---> f8683c095d87
Step 4/20 : RUN apt-get update
 ---> Running in 071898e91fbf
Get:1 http://security.ubuntu.com/ubuntu jammy-security InRelease [110 kB]
Get:2 http://archive.ubuntu.com/ubuntu jammy InRelease [270 kB]
(...)
(...)
Step 20/20 : CMD bash
 ---> Running in 5ca9e3a58636
Removing intermediate container 5ca9e3a58636
 ---> 68136fb7a822
Successfully built 68136fb7a822
Successfully tagged prod-env:0.3

```

7. Ahora repitamos estos pasos, pero moviendo la sentencia `ADD` para el final del `Dockerfile`, justo antes de la sentencia `CMD`:

```dockerfile
FROM ubuntu
LABEL maintainer="cdh@conatel.com.uy"
RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN pip3 install --upgrade pip
RUN pip3 install requests
RUN pip3 install mysql-connector==2.2.9
RUN pip3 install django==1.10
RUN echo "mysql-server mysql-server/root_password password CursoDocker2022." | debconf-set-selections
RUN echo "mysql-server mysql-server/root_password_again password CursoDocker2022." | debconf-set-selections
RUN apt-get install -y mysql-server
RUN apt-get install -y tftpd-hpa
ENV TZ=America/Montevideo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get install -y openssh-server
RUN apt-get install -y nginx
# Ahora colocamos el ADD del archivo config.txt al final del Dockerfile
ADD config.txt /setting/config.txt
CMD bash
```

y podemos volver a modificar el `config.txt` si lo deseamos (aunque no es realmente necesario):
```
   ~/prod-env$ nano config.txt
   Agrego una línea al archivo de configuración.
   Agrego una segunda línea al archivo de configuración.
   <ctrl-X>
```


8. Volvemos a construir la imagen, y esta vez vemos que el proceso es mucho mas rápido, y solo se construyen las últimas capas luego de la sentencia `ADD`, mientras que todas las capas anteriores son leidas desde el cache:

```
   ~/prod-env$ docker build -t prod-env:0.4 .
   Sending build context to Docker daemon  3.584kB
   Step 1/20 : FROM ubuntu
   ---> a8780b506fa4
   Step 2/20 : LABEL maintainer="cdh@conatel.com.uy"
   ---> Using cache
   ---> 19ca15d6ebac
   (...)
   (...)
   Step 18/20 : RUN apt-get install -y nginx
   ---> Using cache
   ---> 2f302e662771
   Step 19/20 : ADD config.txt /setting/config.txt
   ---> ce9dffd6293f
   Step 20/20 : CMD bash
   ---> Running in 1b1d30f03abc
   Removing intermediate container 1b1d30f03abc
   ---> a01d2e15cd79
   Successfully built a01d2e15cd79
   Successfully tagged prod-env:0.4

```
Este ejemplo sencillo muestra la importancia de armar en forma correcta el `Dockerfile`.
En los primeros casos, cuando construímos las imagenes `prod-env:0.2` y `prod-env:0.3`, como la sentencia `ADD` se encuentra al principio del archivo, Docker se ve obligado a volver a generar todas las capas posteriores a dicha sentencia generando de cero todas las imágenes correspondientes, desde la linea 4 en adelante. Si por el contrario nuestro archivo de configuración, que en este caso podría ser lo único que se modifique frecuentemente de nuestra imagen, se encuentra en el último lugar del Dockerfile, el proceso de reconstrucción de nuestra imagen es mucho mas rápido y eficiente, teniedo que modificar solo las últimas capas.

### Contenedores vs Imágenes

Si bien conceptualmente las diferencias entre contenedores e imágenes son importantes, la realidad es que si análizamos uno y otro a bajo nivel, tienen una estructura casí idéntica. De hecho en realidad la imagen es parte del contenedor; veamos esto en mas detalle. 

Un contenedor es una imagen a la que se le agrega una capa adicional con permisos de escritura. Esta capa contendrá todos los archivos que se generen en el contenedor mientras el mismo se encuentre corriendo. Esta capa, que es la única con permiso de escritura, permanecerá en nuestro sistema haciendo persistentes los datos contenidos en ella mientras el contenedor exista. Cuando borramos un contenedor de nuestro sistema con el comando `docker container rm <nombre-del-contenedor>` lo que en realidad estamos haciendo es borrar esa última capa, eliminando claro los datos que ésta contenía. 

El siguiente diagrama muestra gráficamente la estructura de capas explicada anteriormente:

![alt text](Imagenes/container-layers.jpg "Estructura de capas de un contenedor")


La forma en que están estructurados los contenedores presenta un beneficio muy importante. 
Si corremos varios conenedores derivados de una misma imagen, el espacio que ocupará cada uno de los contenedores en disco será unicamente la sumatoria de todas las capas superiores (capas de contenedor), más la imagen en sí, que se sumará una única vez. El diagrama a continuación muestra este concepto gráficamente:

![alt text](Imagenes/sharing-layers.jpg "Varios contenedores utilizando una imagen")



| [<-- Volver](1_Docker.md) | [Siguiente -->](3_Storage.md) |
