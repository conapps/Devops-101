| [&lt;-- Volver](2_Images.md) |
[Siguiente --&gt;](4_Networking.md) |

## Storage

---

### Espacio en disco ocupado por un contenedor

Es bastante difícil poder calcular el tamaño exacto que ocupa un contenedor.

Si ejecutamos el comando `docker container ls -s` vamos a ver que en la columna `SIZE` aparecen dos valores, el primero hace referencia al tamaño de la capa read-write de ese contenedor en particular y el `virtual size` que hace referencia al tamaño de la imagen a partir de la cual se generó el contenedor + el tamaño de la capa RW del contenedor.

```bash
$ docker container ls -s
CONTAINER ID   IMAGE     COMMAND                  CREATED         STATUS         PORTS     NAMES             SIZE
6da23ebd22d4   nginx     "/docker-entrypoint.…"   5 seconds ago   Up 4 seconds   80/tcp    competent_elion   1.09kB (virtual 187MB)

```

El `virtual size` constituye el tamaño total que ocupa un contenedor en el disco.

Algunas consideraciones importantes a tener en cuenta a la hora de estimar cuanto espacio ocupan los contenedores:

- En escenarios donde tengo varios contenedores derivados de la misma imagen, tengo que sumar el `virtual size` una única vez.
- Es posible que dos imagenes distintas compartan algunas capas, por lo que en este escenario, si corremos dos contenedores uno derivado de cada imagen, tampoco sería correcto sumar los `virtual size` de ambos.
- Además de su capa read-write, los contenedores pueden escribir datos en volúmenes externos (lo veremos mas adelante). En tal caso, el espacio que ocupan estos volúmenes no figura en la salida de este comando.

#### Ejercicio 10

En este ejercicio autoguiado vamos a explorar el `size` y el `virtual size` de un contenedor, y a verficar que el segundo es la suma del tamaño de la imagen y del primero.

1. A partir del siguiente Dockerfile generemos una imagen llamada `imagen_de_prueba`.

```Dockerfile
FROM ubuntu
RUN apt update && apt install -y nano
```


```
~/ejercicio10$ docker build -t imagen_de_prueba .
(...)
 => => writing image sha256:7ad73c48793cee7ff5371c13b451501efcc9f6046348f2ba3e60c11349be3393                   0.0s 
 => => naming to docker.io/library/imagen_de_prueba                                                            0.0s
```

2. Verifiquemos las capas que componen la imagen:

```bash
$ docker image history imagen_de_prueba:latest 
IMAGE          CREATED         CREATED BY                                      SIZE      COMMENT
7ad73c48793c   2 minutes ago   RUN /bin/sh -c apt update && apt install -y …   45.9MB    buildkit.dockerfile.v0
<missing>      2 weeks ago     /bin/sh -c #(nop)  CMD ["/bin/bash"]            0B    
<missing>      2 weeks ago     /bin/sh -c #(nop) ADD file:194c886b88876c180…   77.8MB  
<missing>      2 weeks ago     /bin/sh -c #(nop)  LABEL org.opencontainers.…   0B    
<missing>      2 weeks ago     /bin/sh -c #(nop)  LABEL org.opencontainers.…   0B    
<missing>      2 weeks ago     /bin/sh -c #(nop)  ARG LAUNCHPAD_BUILD_ARCH     0B    
<missing>      2 weeks ago     /bin/sh -c #(nop)  ARG RELEASE                  0B

```

3. Ahora vamos a crear un contenedor, corriendo en segundo plano, a partir de dicha imagen:

```bash
$ docker container run -itd --rm --name contenedor_de_prueba imagen_de_prueba bash
```

4. Verfiquemos el tamaño de dicho contenedor:

```bash
$ docker container ls -s
CONTAINER ID   IMAGE              COMMAND   CREATED         STATUS         PORTS     NAMES                  SIZE
109a4567197c   imagen_de_prueba   "bash"    16 seconds ago  Up 15 seconds            contenedor_de_prueba   0B (virtual 124MB)
```

5. Ahora ingresamos al contenedor, y creamos dentro del mismo un archivo de 35M:

```bash
$ docker container attach contenedor_de_prueba
root@e3173657fec9:/# fallocate -l 35M archivo_grande.txt

root@e3173657fec9:/# ls -lah
total 35912
drwxr-xr-x   1 root root     4.0K Aug  8 23:00 .
drwxr-xr-x   1 root root     4.0K Aug  8 23:00 ..
-rwxr-xr-x   1 root root        0 Aug  8 22:57 .dockerenv
-rw-r--r--   1 root root      35M Aug  8 23:00 archivo_grande.txt
(...)
```

6. Usando la secuencia de escape `ctl+p`,`ctl+q` salimos del contenedor y verificamos que ahora ambos tamaños, el `size` y el `virtual size` han aumentado en 35MB:

```bash
$ docker container ls -s
CONTAINER ID   IMAGE              COMMAND   CREATED         STATUS         PORTS     NAMES                  SIZE
109a4567197c   imagen_de_prueba   "bash"    3 minutes ago   Up 3 minutes             contenedor_de_prueba   36.7MB (virtual 160MB)

```

### Drivers de acceso a disco mas comúnes (aufs, overlay y overlay2)

Las lecturas y escrituras al filesystem que se genera para los contenedores a partir de las capas read-only y read-write, se realizan mediante algún _storage driver_, donde los mas comunes son `aufs`, `overlay` y `overlay2`. Para el caso de _Ubuntu_, que es el sistema operativo que usamos en nuestro `docker host` del laboratorio, el driver por defecto es `overlay2`. Sin embargo, el comportamiento que describiremos a continuación aplica también para los otros dos drivers mencionados.

Cada vez que un contedor quiere modificar un archivo de su filesystem, primero busca dicho archivo en las capas read-only, comenzando por la capa superior, y avanzando hacia abajo una capa a la vez. Al encontrar el archivo, detiene la búsqueda y realiza una copia del mismo en la capa superior (read-write). De ahora en adelante, cada vez que quiera acceder a este archivo el contenedor no tendrá acceso al archivo original, sino que usará siempre la copia que realizó en la capa superior.

Este comportamiento se repite también en la generación de imágenes, donde cada vez que una capa superior modifica un archivo realiza una copia del mismo, invalidando las copias que puedan existir en capas inferiores.

### Alternativas para la persistencia de datos

#### Capa read-write del contenedor

Como vimos en algunos de los ejercicios, es posible guardar información de forma persistente en la capa read-write de un contenedor. Sin embargo esto tiene varias desventajas:

- Los datos se perderán al borrar el contenedor.
- Los datos no se pueden exportar fácilmente fuera de la máquina _host_.
- La escritura a la capa read-write de los contenedores se hace mediante un _storage driver,_ lo que lo hace poco performante pensando en ambientes de producción.

⚠️ Recuerde que los contenedores son **efimeros** y deben poder eliminarse y crearse continuamente.

Lo correcto entonces, es no almacenar datos en el contenedor, sino almacenarlos directamente en el servidor `host`. Para esto, tenemos tres alternativas:

#### _bind mount_

En esta modalidad, lo que se hace es montar un directorio del servidor `host`, en un directorio interno del propio contenedor. Varios contenedores pueden montar el mismo directorio del `host,` pudiendo leer y escribir datos sobre el mismo de forma simultánea.

Este método presenta como ventajas principales:

- Es mucho mas performante que guardar los archivos en la capa read-write de los contenedores, dado que no utiliza el _storage driver_ del contenedor.
- Los datos persisten, aún cuando los contenedores se eliminan.
- Varios contenedores pueden acceder y modificar los mismos archivos de forma simultánea.

#### _volumes_

Esta modalidad es prácticamente igual a la anterior, con la diferencia que no es el usuario quien elige el directorio a montar, sino que es el propio Docker el que asigna un directorio de la máquina _host_ para manejar la persistencia de los datos. En general este método es recomendado sobre el uso de _bind mount,_ dado que presenta las siguientes ventajas:

- Permite migrar un contenedor de un _host_ a otro con mínimo impacto, dado que no es necesario conocer, ni administrar, la estructura de directorios del *host.*
- Permite desacoplar los comandos de Docker de la estructura de datos de la máquina _host_ donde este corre.
- Se pueden utilizar _volume plugins_ específicos que proveen funcionalidades adicionales, como por ejemplo, sincronizar los _volumes_ con proveedores de nube o con otros servicios de storage. Se puede encontrar mas detalle sobre esto [aquí](https://docs.docker.com/engine/extend/legacy_plugins/#volume-plugins).

#### _tmpfs mount_

Esta modalidad - que en realidad no mantiene la persistencia - coloca los datos dentro de _filesystems temporales_ que son almacenados en la memoria RAM del host. En este caso los datos se pierden al apagar el contenedor. Este método es ideal cuando no se necesitan los datos mas allá del tiempo de vida del contenedor, pero es necesaria una alta performance para la lectura/escritura de los mismos.



La imagen a continuación presenta un resumen de los tres tipos de persistencia de datos disponibles en el host:

![alt text](Imagenes/types-of-mounts.png "Tipos de persistencia de datos en el host")


### Capa read-write del contenedor

Exploremos esta estrategia de persistencia con un ejercicio.

#### Ejercicio 11

1. Utilizando un Dockerfile generar una imagen a partir de la imagen de Ubuntu, con el editor de texto `nano` pre-instalado.
2. Generar un contenedor corriendo `bash` en modo terminal interactiva, y asegurandose que no se elimine al apagarse.
3. Dentro del contenedor, utilizando `nano` crear un archivo de texto con contenido arbitrario al que llamaremos `testigo.txt`
4. Salir del contenedor utilizando `exit`, y verificar que al salir el contenedor se apagó.
5. Iniciar nuevamente el contenedor, conectarse al mismo y verificar que el archivo aún está presente.
6. Salir del contenedor nuevamente, y esta vez eliminarlo.
7. Generar un contenedor nuevamente a partir de la imagen, conectarse al mismo y verificar que el archivo no existe.

    `<details>`
    `<summary>`Solución`</summary>`

<pre>
    $ mkdir ejercicio11
    $ cd ejercicio11
    ~/ejercicio11$ nano Dockerfile
    FROM ubuntu
    RUN apt update && apt install -y nano
    CMD bash
</pre>

<pre>
    ~/ejercicio11$ docker build -t ejercicio11 .
    (...)
     => => naming to docker.io/library/ejercicio11                                  0.0s
</pre>

<pre>
    ~/ejercicio11$ docker container run -it --name contenedor11 ejercicio11
    root@77d732dae63f:/# nano testigo.txt
    Texto de prueba
  
    root@77d732dae63f:/# exit
    exit
  
   ~/ejercicio11$ docker container ls
    CONTAINER ID   IMAGE              COMMAND   CREATED       STATUS       PORTS     NAMES
</pre>

<pre>
    ~/ejercicio11$ docker container start contenedor11
    contenedor11

    ~/ejercicio11$ docker container ls
    CONTAINER ID   IMAGE         COMMAND             CREATED         STATUS         PORTS     NAMES
    77d732dae63f   ejercicio11   "/bin/sh -c bash"   4 minutes ago   Up 3 seconds             contenedor11

    ~/ejercicio11$ docker container attach contenedor11
    root@77d732dae63f:/# ls -la testigo.txt
    -rw-r--r--   1 root root   16 Nov  8 14:13 testigo.txt
    root@77d732dae63f:/# cat testigo.txt 
    Texto de prueba
    root@77d732dae63f:/# exit
    exit

    ~/ejercicio11$ docker container rm contenedor11
    contenedor11
</pre>

<pre>
    ~/ejercicio11$ docker container run -it --name contenedor11 -it ejercicio11
    root@ad5af9a9ad3b:/# ls -la testigo.txt
    ls: cannot access 'testigo.txt': No such file or directory
    root@ad5af9a9ad3b:/# exit
    exit
</pre>

</details>

### Bind Mounts

Para utilizar `bind mount` para almacenar datos, debemos indicarlo al momento de crear el contenedor, de la siguiente manera:

```bash
$ docker container run -it --mount type=bind,src=<direcotrio-del-host>,dst=<directorio-del-contenedor> ubuntu bash
```

Exploremos esto en el siguiente ejercicio.

#### Ejercicio 12

1. En el host, crear un directorio llamado `datos`, y dentro del mismo crear un archivo de texto llamado `testigo.txt`.
2. Utilizando la imagen del ejercicio 11 (con `nano` pre-instalado) crear un nuevo contenedor, pero esta vez montando la carpeta `/home/ubuntu/datos` del host en la carpeta `/data` del contenedor.
3. Una vez dentro del contenedor verficar que el archivo `testigo.txt` se encuentra dentro de `/data,` editarlo y agregarle información.
4. Todavía estando dentro del contenedor, crear un nuevo archivo `testigo2.txt` en el directorio `/data`
5. Salir del contenedor, y verificar en el directorio `datos` del `host` que el archivo `testigo1.txt` se encuentra modificado, y que ahora hay un nuevo archivo `testigo2.txt`.

<details>
    <summary>Solución</summary>
<pre>
    $ cd /home/ubuntu
    $ mkdir datos
    $ touch datos/testigo.txt
</pre>
<pre>
    $ docker container run -it --rm --mount type=bind,src=/home/ubuntu/datos,dst=/data ejercicio11 bash
</pre>
<pre>
    root@8fae21109d08:/# ls -la /data/testigo.txt
    -rw-rw-r-- 1 1000 1000 0 Nov  8 14:33 /data/testigo.txt
    root@8fae21109d08:/# nano /data/testigo.txt
    Agrego una linea al archivo.
    (Ctrl-X)
    root@8fae21109d08:/#
</pre>
<pre>
    root@8fae21109d08:/# touch /data/testigo2.txt
    exit
</pre>
<pre>
    $ cd datos
    ~/datos$ ls -la
    total 12
    drwxrwxr-x  2 ubuntu ubuntu 4096 Nov  8 14:36 .
    drwxr-xr-x 12 ubuntu ubuntu 4096 Nov  8 14:32 ..
    -rw-rw-r--  1 ubuntu ubuntu   29 Nov  8 14:34 testigo.txt
    -rw-r--r--  1 root   root      0 Nov  8 14:36 testigo2.txt
    ~/datos$ cat testigo.txt
    Agrego una linea al archivo.
</pre>
</details>

> **Bonus:** montar varios contenedores apuntando al mismo directorio del host, y verificar que cuando modificamos el contenido desde un contenedor, los cambios están disponibles automáticamente para todo el resto de los contenedores.

### Volumes

Veamos ahora como trabajar con `volumes` con nuestros contenedores.

##### **Crear un volumen**

```bash
$ docker volume create nombre-del-volumen
```

##### **Listar un volumen**

```bash
$ docker volume ls
DRIVER              VOLUME NAME
local               nombre-del-volumen
```

##### **Ver los detalles de un volumen**

```bash
$ docker volume inspect nombre-del-volumen
[
    {
        "Driver": "local",
        "Labels": {},
        "Mountpoint": "/var/lib/docker/volumes/nombre-del-volumen/_data",
        "Name": "nombre-del-volumen",
        "Options": {},
        "Scope": "local"
    }
]
```

👉 en la salida del comando anterior podemos ver el punto de montaje del volumen dentro el `host.`

##### **Eliminar un volumen**

```bash
$ docker volume rm nombre-del-volumen
```

⚠️ este comando elimina todo el contenido almacenado en el volumen.

##### Asociar un contenedor con un volumen

Al momento de la creación de un contenedor se le puede asociar un volumen. Si el volumen ya existe se asocia al contenedor, y si el volumen no existe el mismo es creado.

```bash
$ docker container run -d -it --name contenedor-con-volumen --mount source=mi-nuevo-volumen,target=/punto_de_montado ubuntu bash
```

Verifiquemos que el contenedor tiene el volumen asociado:

```bash
$ docker container inspect contenedor-con-volumen
<-- SALIDA OMITIDA PARA MAYOR CLARIDAD <--
    "Mounts": [
        {
           "Type": "volume",
           "Name": "mi-nuevo-volumen",
           "Source": "/var/lib/docker/volumes/mi-nuevo-volumen/_data",
           "Destination": "/punto_de_montado",
           "Driver": "local",
           "Mode": "z",
           "RW": true,
           "Propagation": ""
        }
    ],
<-- SALIDA OMITIDA PARA MAYOR CLARIDAD <--
```

Ahora vamos a crear datos para que queden almacenados en el volumen:

```bash
$ docker container attach contenedor-con-volumen
root@b5f618ef6d47:/# cd /punto_de_montado/
root@b5f618ef6d47:/punto_de_montado# touch testigo.txt
root@b5f618ef6d47:/punto_de_montado# ls -l
total 0
-rw-r--r--  1 root root    0 Aug 21 19:11 testigo.txt
root@b5f618ef6d47:/punto_de_montado# exit

```

Eliminemos el container y volvamos a crear otro para ver que los datos persisten. En este caso vamos a hacer que el nuevo contenedor tenga permisos de solo lectura sobre los datos del volumen:

```bash

$ docker container rm contenedor-de-prueba
contenedor-de-prueba

$ docker container run -it --name contenedor-con-volumen-ro --mount source=mi-nuevo-volumen,target=/nuevo_punto_de_montado,readonly ubuntu bash

root@65a9253f28c4:/# cd nuevo_punto_de_montado/
root@65a9253f28c4:/nuevo_punto_de_montado# ls -l
total 0
-rw-r--r--  1 root root    0 Aug 21 19:11 testigo.txt

root@65a9253f28c4:/nuevo_punto_de_montado# echo prueba > testigo.txt
bash: testigo.txt: Read-only file system

```

Notemos que si bien el archivo figura con permisos `rw` para el `owner`, el archivo igual no puede modificarse porque el filsystem es `ro`.
Eliminemos el contenedor y el volumen:

```bash
$ docker container stop contenedor-con-volumen-ro
$ docker container rm contenedor-con-volumen-ro
contenedor-con-volumen-ro

$ docker volume rm mi-nuevo-volumen
mi-nuevo-volumen
```

#### Ejercicio 13

1. Crear un volumen llamado `miVolumen`
2. Crear 3 contenedores `contenedor1`, `contenedor2` y `contenedor3`, cuya carpeta `/data` se encuentre montada sobre el volumen `miVolumen`.
3. Parados en el `contenedor1` modificar el contenido de la carpeta de alguna forma.
4. Verificar que la modificación realizada en el paso anterior se ve reflejada en los otros contenedores.
5. Eliminar los 3 contenedores.
6. Crear un nuevo contenedor montando `miVolumen` en una carpeta a elección dentro del contenedor y verificar que los datos persisten.

> **Bonus:** identificar en que directorio del *host*  se encuentran almacenados los datos.


<details>
    <summary>Solución</summary>
<pre>
    $ docker volume create miVolumen
    miVolumen
    $
    $ docker container run -itd --rm --name contenedor1 --mount source=miVolumen,target=/data ubuntu bash
    ca2c111487050a0e40b95377fee04d4b43e7274fcf1f070ab758880ba7f77bba
    $ docker container run -itd --rm --name contenedor2 --mount source=miVolumen,target=/data ubuntu bash
    0b25da2515c16128585eae17550009dde7941ca8596d0e19ba6a98c01b665ff0
    $ docker container run -itd --rm --name contenedor3 --mount source=miVolumen,target=/data ubuntu bash
    43c07e5ac42bcc17cc292d57f8166ed3ab93824745b38ff74d58cdbc161d9971
    $ 
    $ docker container attach contenedor1
    root@ca2c11148705:/# cd /data
    root@ca2c11148705:/data# touch archivo1.txt archivo2.txt
    root@ca2c11148705:/data# ls -l
    total 0
    -rw-r--r-- 1 root root 0 Nov  8 16:52 archivo1.txt
    -rw-r--r-- 1 root root 0 Nov  8 16:52 archivo2.txt
    root@ca2c11148705:/data# exit
    exit
    $
    $ docker container exec -it contenedor2 bash -c "ls -l /data"
    total 0
    -rw-r--r-- 1 root root 0 Nov  8 16:52 archivo1.txt
    -rw-r--r-- 1 root root 0 Nov  8 16:52 archivo2.txt
    $
    $ docker container exec -it contenedor3 bash -c "ls -l /data"
    total 0
    -rw-r--r-- 1 root root 0 Nov  8 16:52 archivo1.txt
    -rw-r--r-- 1 root root 0 Nov  8 16:52 archivo2.txt
    $
    $ docker container stop contenedor2 contenedor3
    contenedor2
    contenedor3
    $
    $ docker container ls -l
    CONTAINER ID   IMAGE         COMMAND             CREATED       STATUS                   PORTS     NAMES
    $
    $ docker container run -it --rm --name nuevo-contenedor --mount source=miVolumen,target=/misdatos ubuntu bash
    root@8ba5078b9d03:/# ls -la /misdatos
    total 8
    drwxr-xr-x 2 root root 4096 Nov  8 16:52 .
    drwxr-xr-x 1 root root 4096 Nov  8 16:56 ..
    -rw-r--r-- 1 root root    0 Nov  8 16:52 archivo1.txt
    -rw-r--r-- 1 root root    0 Nov  8 16:52 archivo2.txt
    $ exit
    exit
</pre>
</details>

### Volumenes con drivers creados por los usuarios.

Cuando creamos un volumen, por defecto este utilizará el driver `local` para el acceso al mismo. Sin embargo es posible crear drivers que extiendan la funcionalidad de los volúmenes para, por ejemplo, montar un filesystem alojado en un proveedor de nube. Estos drivers pueden instalarse en la forma de  `docker plugin` mediante un proceso muy sencillo. Puede encontrar una lista de dri

A continuación exploraremos este mecanismo con un par de ejemplos.

#### sshFS - volume plugin para montar un directorio remoto a través de ssh

Como mencionamos anteriormente, una de las principales ventajas de utilizar `volumes` por sobre `bind mounts`, es la posibilidad de montar storage externos al host.

En el siguiente ejercicio guiado, veremos como montar el directorio `/home/ubuntu/docker101` que se encuentra ubicado en forma remota en el servidor  `sshserver.labs.conatest.click` a través de ssh, para poder accederlo en uno o varios contenedores.

#### Ejercicio 14

Primero instalamos el plugin `vieux/sshfs`

```bash
$ docker plugin install --grant-all-permissions vieux/sshfs
latest: Pulling from vieux/sshfs
Digest: sha256:1d3c3e42c12138da5ef7873b97f7f32cf99fb6edde75fa4f0bcf9ed277855811
52d435ada6a4: Complete 
Installed plugin vieux/sshfs

```

Ahora creamos el volumen

```bash
$ docker volume create --driver vieux/sshfs \
  -o sshcmd=ubuntu@sshserver.labs.conatest.click:/home/ubuntu/docker101 \
  -o password=conatel_docker101 \
  sshvolume

$ docker volume ls
DRIVER               VOLUME NAME
vieux/sshfs:latest   sshvolume

```

Ya estamos listos para generar un contenedor con este volumen montado en algún lugar de su filesystem.

```bash
$ docker container run -it --rm --name test-container --mount source=sshvolume,target=/data ubuntu bash
root@ad2a828fcda3:/# cd /data
root@ad2a828fcda3:/data# ls
holaMundoSSH.txt
```

Si aparece el archivo `holaMundoSSH.txt` es porque todo está funcionando.

#### REX-Ray - Volume plugin para montar storage en la nube.

Otra de las posibilidades al utilizar `volumenes` es por ejemplo la de montar storage de proveedores de cloud. En el siguiente ejercicio guiado veremos como montar un bucket de AWS S3 en uno, o varios, contenedores utilizando el plugin de [REX-Ray](https://rexray.readthedocs.io/en/stable/user-guide/schedulers/docker/plug-ins/aws/#aws-s3fs).

#### Ejercicio 15

Primero instalamos el plugin:

```bash
$ docker plugin install rexray/s3fs \
  S3FS_ACCESSKEY=<se_proveera_en_la_capacitacion_presencial> \
  S3FS_SECRETKEY=<se_proveera_en_la_capacitacion_presencial>
```

Una vez instalado el plugin, este se encarga de generar un volumen por cada bucket que existe en la cuenta.
Podemos inspeccionar los volumenes disponibles con:

```bash
~$ docker volume ls
DRIVER               VOLUME NAME
rexray/s3fs:latest   clase-de-docker
<-- Salida omitida para mayor claridad -->
```

⚠️ Para este ejercicio utilizaremos el volumen llamado `clase-de-docker`.


Ya estamos listos para generar un contenedor con este volumen montado en algún lugar de su filesystem.

```bash
$ docker container run -it --rm --name test-container --mount source=clase-de-docker,target=/data ubuntu bash
root@ad2a828fcda3:/# cd /data
root@ad2a828fcda3:/data# ls
helloWorldFromS3.txt
```

Si aparece el archivo `helloWorldFromS3.txt` es porque todo está funcionando correctamente.

| [&lt;-- Volver](2_Images.md) |
[Siguiente --&gt;](4_Networking.md) |
