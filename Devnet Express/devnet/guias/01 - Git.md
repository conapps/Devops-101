# Git

_Fuentes:_

- [Cisco Git Lab](https://learninglabs.cisco.com/lab/git-intro/step/1)
- [Instalación de Git](https://git-scm.com/book/es/v2/Inicio---Sobre-el-Control-de-Versiones-Instalaci%C3%B3n-de-Git)\*
- [What a branch is](https://git-scm.com/book/en/v1/Git-Branching-What-a-Branch-Is)
- [Git reference](http://gitref.org/basic/)
- [What is a git "snapshot"](http://stackoverflow.com/questions/4964099/what-is-a-git-snapshot)

## Sistema de control de versiones.

Los sistemas de control de versiones de archivo existen desde la invención del desarrollo de software. Algunas de sus funciones principales son:

- Almacenar versiones incrementales de los cambios realizados a los documentos que componen el proyecto.
- Permitir compartir proyectos entre múltiples usuarios.
- Brindar un metodo para "unir" el código desarrollado por múltiples individuos, minimizando la introducción de errores en el codigo.
- Mantener una base de datos de cambios en el codigo.
- Brindar herramientas para encontrar y solucionar bugs dentro del código.
- Etc.

`git` es el sistema de control de versiones más popular en el mundo, desarrollado por Linus Torvalds, quien es el el fundador del kernel de linux. Es importante no confundir `git` con "Github". El último es una compania popular que utiliza el protocolo `git` para compartir bases de codigo entre múltiples usuarios, brindando herramientas adicionales para construir comunidades en torno al codigo.

## Instalación de Git

### Ubuntu

Puede que ya este instalado. Sino se puede instalar a travez de `apt-get`.

```
apt-get install git
```

También se puede compilar directamente a partir del codigo fuente.

**Solo siga estas instrucciones si se siente comodo con la línea de comandos de Linux.**

```
// Se necesitan las siguientes dependencias
apt-get install libcurl4-gnutls-dev libexpat1-dev gettext libz-dev libssl-dev wget

// Luego descargamos la versión más reciente (2.11.0 al día de redacción de este texto).
wget https://www.kernel.org/pub/software/scm/git/git-2.11.0.tar.xz

// Por último compilamos e instalamos el software
tar -zxf git-2.0.0.tar.gz
cd git-2.0.0
make configure
./configure --prefix=/usr
make all doc info
sudo make install install-doc install-html install-info
```

Futuras actualizaciones de git pueden realizarse utilizando propiamente `git`.

```
git clone git://git.kernel.org/pub/scm/git/git.git
```

### Windows

Se puede instalar el paquete `git-scm` o "Github para Windows". Recomendamos la segunda opción.

- [git-scm](http://git-scm.com/download/win)
- [Github para Windows](https://desktop.github.com/)
- [Git Reference](http://gitref.org/basic/)

## Configuración de Git

Una vez instalado debemos configurar nuestras credenciales para obtener el credito (o la culpa) de nuestros aportes al código. Para eso utilizaremos el comando `git config` con nuestra cuenta de correo.

**Sustituir el texto entre corchetes por sus valores**

```
git config --global user.name ["Su nombre"]
git config --global user.email [Su mail]
```

## Inicializar un repositorio (repo)

Un repositorio (o "repo") es simplemente el directorio raiz de nuestro proyecto, el cual sera monitoreado por `git`.

Para iniciar un repositorio, debemos it a la carpeta de nuestro proyecto y correr el comando `git init`. En este ejemplo crearemos una carpeta llamada `intro` y correremos el comando mencionado.

**El signo de moneda ($) al comienzo de ciertas lineas indica comandos que debemos ingresar en la consola. Las líneas que no cuenten con este caracter al inicio corresponden a las salidas de los comandos ingresados.**

```
$ mkdir intro && cd intro
$ git init
Initialized empty Git repository in /src/.git/
```

Si revisamos el contenido de la carpeta de nuestro proyecto, vamos a ver que `git` creo una nueva carpeta llamada `.git`, donde almacenara toda la información referente a nuestro proyecto.

```
$ ls -a
total 1M
drwxrwxr-x  3 user user 1M ene 24 10:25 .
drwxr-xr-x 22 user root 1M ene 24 10:25 ..
drwxrwxr-x  7 user user 1M ene 24 10:25 .git
```

Todas las interacciones con `git` serán a través de la linea de comandos. Nunca vamos a tener que realizar ninguna modificación a los archivos encontrados dentro de la carpeta `.git`. Podemos olvidarnos de la existencia de la misma y seguir adelante.

## Registrando cambios

Para que `git` comienze a registrar los cambios en nuestro archivos tenemos que indicarle los archivos a seguir. Esto lo hacemos con el comando `git add`. Si realizamos el proceso de inicialización del proyecto en un directorio vació, `git` no va a tener nada para seguir. Podemos veríficar el estado de `git` en cualquier momento utilizando el comando `git status`.

```
$ git status
On branch master

Initial commit

nothing to commit (create/copy files and use "git add" to track)
```

Para comenzar a entender el resultado de este comando tenemos que conocer el significado de un "commit" y "branch".

Un "commit" es el termino que usamos para referir al proceso de almacenamiento de los cambios realizados. `git` no almacena por defecto todas las modificaciones realizadas en nuestro proyecto. Cada modificación se registra en un índice en estado de "staging" (presentación). Es responsabilidad del desarrolador definir cuales de estos cambios queremos almacenar. Debemos realizar un "commit" para guardar los cambios en el sistema de control. Esto permite ordenar la forma en que se almacenarán los cambios, independientemente de como los realizamos.

Por otro lado, para entender el concepto de "branch", debemos entender como es que `git` almacena la información de los cambios. Uno podría suponer que los cambios son guardado de forma incremental. Esto es incorrecto. `git` almacena los cambios como "snapshots", osea, el estado de los archivos que `git` esta siguiendo en algún punto en el tiempo. Cuando uno realiza un "commit", esta generando un puntero que apunta hacia una "snapshot" en particular; el autor que realizo los cambios; metadata correspondiente al commit; y relaciones con otros "commits" realizados anteriormente en el tiempo. A medida que vamos realizando "commits" dentro de nuestro proyecto vamos generando una cadena o árbol donde cada "commit" esta vinculado por al menos otro "commit" (menos nuestro "commit" inicial). Un "branch" corresponde a una cadena de "commits". Durante el proyecto podemos construir "branches" adicionales y comenzar una nueva cadena de "commits". A este proceso se le conoce como "branching" y basicamente lo que permite es trabajar en bases de codigo paralelas que cuenten con un "commit" ancestro en común. Cada "branch" cuenta con un nombre distinto que los identifica. La "branch" `master` es creada de forma automatica por `git` al inicar el proyecto. Las "branches" pueden "unirse" entre sí, combinando los "commits" realizados en cada uno de ellos de forma paralela.

Volviendo al resultado del comando `git status`, ahora podemos identificar que nos encontramos trabajando en las "branch" `master`, que el último "commit" fue registrado con el mensaje "Intiial commit" y que no se está siguiendo níngun archivo, ni se ha seleccionado uno para almacenar sus cambios a través de un nuevo "commit".

Agreguemos un nuevo archivo para ver como evoluciona el proceso.

```
$ touch test.txt
$ git status
On branch master

Initial commit

Untracked files:
  (use "git add <file>..." to include in what will be committed)

	test.txt

nothing added to commit but untracked files present (use "git add" to track)
```

Vemos que `git` reconocio que se ha creado un nuevo archivo en el proyecto pero por defecto no se están siguiendo sus cambios. Para poder registrar sus cambios debemos pasarlo a la fase de "stage" utilizando el comando `git add`. La fase de "staging" permite ordenar como se van a almacenar los cambios.

```
$ git add test.txt
$ git status
On branch master

Initial commit

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)

	new file:   test.txt
```

Ahora si el archivo `test.txt` esta en la fase de "stage" listo para ser incluido en nuestro proximo "commit". El comando para realizar un "commit" es `git commit`. Usualmente se le agrega el flag `-m` más un mensaje entre comillas indicando de que se compone el "commit". La formalidad del mensaje a incluir varía entre proyecto, pero usualmente es una buena practica indicar de forma concisa los cambios efectuados.

```
$ git commit -m "creación del archivo test.txt"
[master (root-commit) 358eace] creación del archivo test.txt
 1 file changed, 0 insertions(+), 0 deletions(-)
 create mode 100644 test.txt
```

La salida del comando `git commit` indica la "branch" donde se registo el "commit" y un detalle sobre las modificaciones realizadas en este "commit". Además, la salida del comando comparte un código que referencia al "commit". En este caso: `358eace`. Este valor varía entre "commits" y se utiliza para referenciar los distintos "commits". El codigo es el resultado de aplicar el algoritmo de hashing SHA1 sobre los cambios realizados. Por lo tanto, todos los codigos de los "commits" serán distintos uno del otro.

Si volvemos a realizar el comando `git status` verificamos que los cambios han sido guardados de forma exitosa.

```
$ git status
On branch master
nothing to commit, working directory clean
```

## Modificaciones

En el ejemplo anterior creamos un nuevo archivo vacío y guardamos esta acción en `git`. Veamos el mismo proceso pero ahora realizando una modificación a un archivo.

```
$ echo "Agregamos una línea a nuestro archivo de prueba" >> test.txt
$ git status
On branch master
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git checkout -- <file>..." to discard changes in working directory)

	modified:   test.txt

no changes added to commit (use "git add" and/or "git commit -a")
```

`git` reconocio que se ha realizado un cambio en un archivo. Sin embargo, este cambio no esta listo para ser almacenado. Debemos seguir el mismo procedimiento que realizamos anteriormente.

**OBS: Si queremos agregar todos los archivos que modificamos de una sola vez podemos utilizar el comando `git add --all`. Esto evita agregar cada archivo de forma individual.**

```
$ git add --all
$ git commit -m "agregado de nueva línea a test.txt"
[master 4ebfe80] agregado de una nueva línea a test.txt
 1 file changed, 1 insertion(+)
```

## Corrección de errores

La mejor forma de correjir errores en el codigo es realizando un nuevo "commit" despues de haber correjido el problema. Por ejemplo, en el caso anterior nos olvidamos de terminar la oración con un punto.

```
$ echo "Agregamos una línea a nuestro archivo de prueba." > test.txt
$ git add --all && git commit -m "bug fix - punto agregado al final de la línea"
[master 6cf0e7a] bug fix - punto agregado al final de la línea
 1 file changed, 1 insertion(+), 1 deletion(-)
```

## Log de cambios

Hay veces en que es importante entender que cambios se realizaron en el proyecto de forma reciente. Algo muy común cuando trabajamos con una base de código de otra persona, o volvemos a un proyecto despues de haber transcurrido un tiempo. Para ver esta información historica usamos el comando `git log`.

```
commit 6cf0e7a335050f854ecb328a9914f6a1271e2130
Author: User <user@example.com>
Date:   Tue Jan 24 11:51:27 2017 -0300

    bug fix - punto agregado al final de la línea

commit 4ebfe80c1c84dace951979e2f92a1cdb8f5d706e
Author: User <user@example.com>
Date:   Tue Jan 24 11:39:18 2017 -0300

    agregado de una nueva línea a test.txt

commit 358eace44e54faed0a6c3cf038271ad52c1cbcd4
Author: User <user@example.com>
Date:   Tue Jan 24 11:24:26 2017 -0300

    creación del archivo test.txt
```

**OBS: En la salida del comando `git log` podemos ver el hash completo de nuestro commit. El que devuelve el comando `git commit` es el resultado de los primeros 7 carácteres del hash completo.**

## Diferencia entre "commits"

Además de poder ver el historial de "commits" realizados, podemos comparar dos "commits" entre si para ver los cambios realizados. Para esto utilizamos el comando `git diff`, ingresando los valores de los "commits" que queremos comparar. Primer el "commit" anterior y luego el que queremos comparar.

```
$ git diff 4ebfe80 6cf0e7a
diff --git a/test.txt b/test.txt
index d1962cd..8ff8579 100644
--- a/test.txt
+++ b/test.txt
@@ -1 +1 @@
-Agregamos una línea a nuestro archivo de prueba
+Agregamos una línea a nuestro archivo de prueba.
```

Otra forma de referenciar los commits es utilizando el valor: `HEAD`. Este valor es manejado internamente por `git` y representa el último "commit" sobre el que estamos trabajando. Podemos utilizarlo para simplificar la llamada a `git diff`. Realicemos un nuevo cambio para que el ejemplo sea más claro.

```
$ echo "Agregamos otra línea al archivo test.txt" >> test.txt
$ git add --all && git commit -m "agregamos otra linea a test.txt"
[master 64ae80d] agregamos otra linea a test.txt
 1 file changed, 1 insertion(+)
$ git diff 4ebfe80 HEAD
diff --git a/test.txt b/test.txt
index d1962cd..ffe9678 100644
--- a/test.txt
+++ b/test.txt
@@ -1 +1,2 @@
-Agregamos una línea a nuestro archivo de prueba
+Agregamos una línea a nuestro archivo de prueba.
+Una nueva línea
```

## Crear un nuevo "branch"

Un "branch" (como referencia su nombre en ingles) es una rama del árbol de commits que construye `git` para almacenar las modificaciones realizadas sobre el proyecto. Crear múltiples "branches" dentro de un proyecto puede ser beneficioso en alguna instancias. Por ejemplo, buenas prácticas indican que la "branch" `master` contenga el cofigo de producción, mientras que el desarrollo de nuevas funcionalidades se realiza en "branches" paralelas. Una vez que este codigo construido paralelamente es testeado y aprobado para entrar en producción se realiza un "branch merge" (una "union").

Para crear una nueva "branch" usamos el comando `git branch` seguido por un nombre que se le asignara a la nueva "branch". Una vez creada, podemos pasarnos a esta nueva "branch" utilizando el comando `git checkout` más el nombre de la "branch" objetivo. Los "commits" realizados en esta nueva "branch" no serán aplicados en las otras "branches". Esto nos permite compartemizar el proyecto en instancias aisladas.

**OBS: Es importante tener presente que si se realiza un `git checkout` y existen modificaciones que no fueron aplicadas a un commit en la "branch" actual, los mismos se transladarán a la otra "branch".**

Veamos el sistema en funcionamiento con un nuevo ejemplo. Crearemos una nueva "branch" llamada "desarrollo". Luego pasaremos a trabajar en esta nueva "branch", crearemos un nuevo archivo y guardaremos los cambios aplicando un nuevo "commit" en la "branch" de desarrollo. Luego compararemos el estado de ambas "branches" y terminaremos mostrando como combinar los "commits" de ambas.

Primero veríficamos que estamos trabajando en la "branch" `master`.

```
$ git branch
* master
```

El comando `git branch` sin incluir el nombre devuelve todas las "branches" del proyecto e indica la "branch" donde estamos trabajando utilizando un "\*".

Ahora crearemos la "branch" de desarrollo.

```
$ git branch desarrollo
$ git branch
  desarrollo
* master
```

La nueva "branch" aparece en la lista. Utilizemos el comando `git checkout` para pasarnos a la nueva "branch".

```
$ git checkout desarrollo
Switched to branch 'desarrollo'
$ git branch
* desarrollo
  master
```

**OBS: Los comandos `git branch <branch>` y `git checkout <branch>` se pueden combinar utilizando el comando `git checkout -b <branch>`.**

Ahore crearemos un nuevo archivo en la "branch" de desarrollo, realizaremos un nuevo "commit" y verificaremos que no se encuentra si nos pasamos a la "branch" `master`.

```
$ touch nuevo.txt
$ git add --all && git commit -m "creación de nuevo archivo"
[desarrollo 88c2543] creación de nuevo archivo
 1 file changed, 0 insertions(+), 0 deletions(-)
 create mode 100644 nuevo.txt
$ ls
-rw-rw-r-- 1 user user 0M ene 24 12:25 nuevo.txt
-rw-rw-r-- 1 user user 1M ene 24 11:57 test.txt
$ git checkout master
Switched to branch 'master'
$ ls
-rw-rw-r-- 1 user user 1M ene 24 11:57 test.txt
```

Por lo tanto, podemos realizar todos los cambios que queramos en la branch de desarrollo sin problemas por que contamos con el codigo funcionando en otra "branch", a nuestro alcance cuando lo necesitemos. Por ejemplo, si queremos comenzar a trabajar en otro nuevo feature, podemos volver a la "branch" master, crear una nueva a partir de la misma y comenzar a trabajar en la misma. Sin tocar las "branches" de desarrollo o producción. Esta práctica es muy común a la hora de solucionar "bugs" en el codigo.

Combinemos los "commits" de ambas branches utilizando el comando `git merge`.

```
$ git branch
  desarrollo
* master
$ git merge desarrollo
Updating 64ae80d..88c2543
Fast-forward
 nuevo.txt | 0
 1 file changed, 0 insertions(+), 0 deletions(-)
 create mode 100644 nuevo.txt
$ ls
-rw-rw-r-- 1 user user 0M ene 24 12:32 nuevo.txt
-rw-rw-r-- 1 user user 1M ene 24 11:57 test.txt
```

Ahora la "branch" `master` cuenta con los "commits" realizados en la "branch" de desarrollo. Si no quicieramos trabajar más con la misma, podemos usar el comando `git branch` con el flag `d` para eliminarla.

```
$ git branch -d desarrollo
Deleted branch desarrollo (was 88c2543).
```

**OBS: Si la "branch" a eliminar contara con cambios sin guardar, un mensaje de advertencia será emitido. Se puede forzar la elminación de la "branch" de todas maneras utilizando el flag `-f`.**

## Almacenar repositorio en GitHub

Una forma de compartir y almacenar nuestro codigo es a través de servicios como GitHub. Para poder sincronizar nuestro codigo en GitHub, debemos crear un repositorio en GitHun y luego agregar el endpoint que nos proveen en la carpeta local de nuestro proyecto. Esto lo hacemos utilizando el comando `git remote`. La comunicación con GitHub puede realizarse a través de SSH o HTTPS. La primera es más segura pero requiere de la creación de una clave RSA que debe ser cargada en GitHub, mientras que para usar HTTPS solo debemos utilizar nuestras credenciales cada vez que queramos comunicarnos con GitHub, ya sea para subir o descargar archivos.

En la carpeta de nuestro proyecto debemos registrar el endpoint de GitHub. Usualmente lo denominamos como "origin" para identificarlo.

```
$ git remote add origin https://github.com/<usuario de GitHub>/<nombre de repo>
```

Luego podemos subir archivos a este repositorio utilizando el comando `git push`, indicando el "endpoint" que queremos contactar y que "branch" queremos empujar. Por ejemplo:

```
$ git push origin master
```

El comando `git pull` funciona de manera similar pero descara la "branch" indicada del "endpoint" indicado. Es importante tener en cuenta que este comando no creara una nueva "branch" con el mismo nombre que la importada, sino que combinara los cambios con los encontrados en la "branch" local activa.

```
$ git pull origin master
```

## Git Backpack & Git Kraken

GitHub ofrece un servicio llamado [Git Backpack](https://education.github.com/pack) con beneficios para nuevos desarrolladores. Hay acceso a páginas con cursos como Pluralsight, y licencias de software. Entre ellas, podemos encontrar una licencia de uso profesional de un software llamado Git Kraken. El mismo abstrae los comandos explicados anteriormente (y más) en un interfaz gráfica donde podemos controlar el estado de nuestro proyecto.

Se puede descargar para Linux, Windows o Mac.

**OBS: Todas las funcionalidades ofrecidas por Git Kraken también están disponibles en la línea de comandos de `git`.**

---

## Setup del proyecto

Se puede descargar el repositorio del curso a la máquina local ejecutando el siguiente comando:

```bash
git clone https://github.com/conapps/Devops-101.git
```
