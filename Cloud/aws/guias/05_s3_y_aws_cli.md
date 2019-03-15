# S3

Amazon S3 es un servicio web que permite almacenar cualquier cantidad de información, desde cualquier parte de Internet, manteniendo un nivel de disponibilidad muy alto. Es un servicio que tiene múltiples años en el mercado y es utilizado por todo tipo de empresas para diversas aplicaciones: respaldos, hosting web, streaming, etc. 

Con los años ha adquirido una gran variedad de funcionalidades que lo hacen muy versatil. Entre ellas:

- Encriptación.
- Multiples niveles de disponibilidad.
- Ciclos de vida de archivos.
- Servidor Web.
- Etc.

Así como con otros servicios, hay múltiples formas de interactuar con este servicio pero por ahora nos concentraremos en usarlo desde la consola. 

Antes de empezar definiremos algunos recursos fundamentales para entender como funciona S3:

- `Buckets`: Funcionan como un `namespace` bajo el cual se almacenarán todos los objetos. Los `Buckets` son creados dentro de una región pero pueden ser migrados a otra de ser necesario. El nombre de los `Buckets` tiene que ser único dentro de todas las regiones. AWS S3 utiliza un sistema de nombre plano, similar al utilizado por `DNS`.
- `Objects`: Corresponden a los objetos que queremos almacenar dentro de S3. Puede ser cualquier tipo de archivo, de tamaños ente 0 y 5TB. Los `Objects` son almacenados dentro de un `Bucket`, sin existir un límite en la cantidad de `Objects` almacenados dentro de uno. Cada `Object` cuenta con ciertas propiedades para identificarlo y protegerlo. El atributo más importante de un `Object` es su `Key` o llave. La `Key` corresponde al nombre asignado al objeto, y es la dirección que debemos utilizar para recuperarlo.

S3 en el fondo funciona como un sistema de llave/valor con una capacidad casí infinita para almacenar objetos. Debido a este esquema es que S3 no permite editar objetos, **solo sustituirlos**. También soporta un sistema de versionado que permite mantener un historico del estado de cada `Object` de forma indefinida. 

> 🚨 El versionado de objetos se debe realizar sobre todo un `Bucket` no puede realizarse por objeto.

---

### 💻 DEMO #01 ~ Creación de un `Bucket` de S3 <a name="demo001"></a>

El nombre de un `Bucket` cuenta con ciertas restricciones que tenemos que cumplir, además de ser único dentro de AWS:

- Debe cumplir con las convenciones de DNS.
- Debe tener entre 3 y 63 carácteres.
- No debe contener mayusculas o guiones-bajo `_`.
- Debe comenzar con una letra mínuscula o un número.
- Debe estar compuesto de múltiples etiquetas separadas por un punto `.`.
- Cada etiqueta debe comenzar y terminar con un a letra mínuscula o un número.
- No debe tener la forma de una dirección `IP` (ej. `192.168.1.1`).

Para este ejemplo utilizaremos la siguiente convención:

`<apellido>.<nombre>.cloud.devops`

#### Procedimiento

1. Ir al Dashboard de S3.
2. Hacer click en `Create bucket`.
3. Ingresar el nombre del `Bucket`.
4. Hacer click en `Next`.
5. Hacer click en `Next`.
6. Deseleccionar todas las opciones (4).
7. Hacer click en `Next`.
8. Hacer click en `Create Bucket`.

#### FAQ

**¿Porque en la barra de la consola aparece `Global` en vez de la regíón donde estaba trabajando?**

S3 es un servicio Global, por más que los objetos estén almacenados en una región puntual. Como es servido sobre Internet, puedo acceder a los objetos almacenados en S3 desde cualquier otra región, sin necesidad de realizar ningún tipo de configuración adicional.

---

Haciendo click sobre el `Bucket` recientemente creado entramos a su consola de administración. Dentro de las opciones que nos presenta vamos a ver una que dice `Create folder`. Sin embargo, el concepto de una `folder` en S3 no es el mismo al que estamos acostrumbrados.

Como se menciono antes, S3 tiene una estructura plana en donde todos los objetos están almacenados dentro de un `Bucket`. Esta estructura puede ser dificil de manejar, sobretodo si tenemos una gran cantidad de objetos dentro del `Bucket`. Es por esto que S3 ofrece un sistema de jerarquía lógico que utiliza prefijos y delimitadores en las `Keys` para simular el funcionamiento de carpetas y subdirectorios. 

Por ejemplo, si guardamos un objeto dentro de nuesto `Bucket` con la `Key` `devops/cloud/ejemplo.txt`, la consola utilizará como delimitador la `/` y creara "carpetas" llamadas `devops` y `cloud` en donde se encontrará el archivo `ejemplo.txt`. Si no le colocamos un prefijo a la `Key` de nuestro objeto, el mismo será almacenado en la raiz del `Bucket`.

---

### 💻 DEMO #02 ~ Creación de un archivo dentro del `Bucket` <a name="demo002"></a>

Vamos a necesitar subir un archivo a `S3` para aprender como funciona. Pueden utilizar un archivo de su propiedad que ya este en su maquina o la siguiente imagen licenciada bajo la licencia `Creative Commons`.

![Photo by Jarylle Adriane Paloma on Unsplash](../imagenes/street.jpg)
Photo by Jarylle Adriane Paloma on Unsplash

#### Procedimiento

1. Ir al Dashboard de S3.
2. Hacer click en el `Bucket` donde queremos subir un objeto.
3. Hacer click en `Upload`.
4. Arrastrar el archivo o seleccionarlo haciendo click en `Add files`. Se pueden subir más de un archivo a la vez.
5. Hacer click en `Next`.
6. En la sección `Manage public permissions` seleccionar `Grant public read access to this object(s)`.
7. Hacer click en `Next`.
8. Seleccionar la clase de almacenamiento `Reduced Redundancy`.
9. Hacer click en `Next`.
10. Hacer click en `Upload`.

#### FAQ

**¿Que pasa si no configuro la opción para que sea público?**

El acceso al archivo estará determinado por `IAM`, otro servicios de AWS.

**¿Que pasa si no selecciono la clase de almacenamiento `Reduced Redundancy`?**

Las clases de almacenamiento disponible cuentan con distintos niveles de SLA en cuestiones de robustez y disponibilidad. Además, cada clase de almacenamiento tiene un costo distinto y número mínimo de días de almacenamiento. La clase de almacenamiento puede modificarse en cualquier momento de todas maneras.

---

Cargamos los archivos en modo público simplemente para poder veríficar que fueron cargados correctamente fácilmente. Podemos ver como este servicio puede ser útil para públicar cualquier tipo de objeto para descargar desde una web, un mail, etc.

## AWS `cli`.

### Métodos de interacción con los servicios de AWS

En la consola de administración de AWS tenemos acceso a todos los servicios y a todas sus funcionalidades. El problema es que la interfaz web de la consola no se presta para realizar acciones de forma automática y no es la forma más rápida para interactuar con los servicios de AWS.

Para remediar esta situación, AWS ofrece múltiples formas de interactuar con sus servicios además de la consola. 

Ordenados en órden de complejidad estos son:

- `cli`: Aplicación de línea de comandos.
- `SDKs`: Kits de desarrollo para múltiples sistemas.
- `CloudFormation`: Servicio de AWS de `Infrastructure as Code`.

Durante el curso interactuaremos con estos tres métodos, haciendo enfasís en la `cli` y con `CloudFormation`.

### Instalación de la `cli` de AWS

La línea de comandos de aws esta desarrollada sobre Python y corre sobre los sistemas operativos más comúnes: Windows, Mac, y Linux.

En Mac y Linux si ya contamos con `python` y `pip` instalado podemos instalar la `cli` con el siguiente comando: 

```
pip install awscli
```

Para Windows es necesario descargar el archivo de instalación correspondiente a su sistema: [64-bit](https://s3.amazonaws.com/aws-cli/AWSCLI64PY3.msi), o [32-bit](https://s3.amazonaws.com/aws-cli/AWSCLI32PY3.msi).

Además de la `cli` es recomendable instalar [`aws-shell`](https://github.com/awslabs/aws-shell), que es una consola interactiva que facilita la utilización de la `cli`. Para instalarla es necesario contar con `python` y `pip`. 

```
pip install aws-shell
```

**🚨 Si esta trabajando desde una Mac es recomendable que realice la instalación con el siguiente comando, ya que existe un bug en una de sus dependencias.**

```
pip install aws-shell --upgrade --ignore-installed siz
```

### Configuración de la `cli`

**🚨 Los siguientes ejemplos se realizarán sobre `aws-shell` sin embargo, todos los comandos pueden utilizarse de la misma manera sobre la `cli` sin modificaciones.**

---

### 💻 DEMO #03 ~ Configuración de la `cli` <a name="demo003"></a>

Las credenciales mencionadas en esta sección tienen que haber sido proveidas a través del mail de bienvenida al curso. Si por algún motivo no le llego el mail o no ve las credenciales, consulte con el moderador del curso.

También se puede realizar los siguientes pasos con las credenciales de su cuenta personal.

#### Procedimiento

0. Correr `aws-shell` (solamente si va a utilizar este programa).
1. Lanzar el comando `configure`.
2. Ingresar su AWS Access Key ID.
3. Ingresar su AWS Secret Access Key.
4. Seleccione su región (la misma que fue asignada anteriormente.)
5. Seleccione `JSON` como `Default output format`.

#### FAQ

**¿Como se que `string` corresponde a mi región?**

Puede utilizar [este link](https://docs.aws.amazon.com/general/latest/gr/rande.html) como referencia.

**¿Que pasa si no tengo credenciales de acceso programatico?**

No podrá utilizar ninguna de las interfaces de gestión de AWS programaticas.

**¿Como consigo credenciales de acceso programatico?**

El administrador de la cuenta de AWS puede crear usuarios desde el servicio `IAM`. Estos usuarios cuentan con múltiples tipos de credenciales para acceder a la cuenta de AWS, entre ellos, credenciales de acceso a la consola Web y credenciales de acceso prográmatico. Solamente un administrador de la cuenta puede crear credenciales para otros usuarios. Además, un usuario puede recrear sus credenciales de acceso prográmatico si siente que pueden haberse comprometido las anteriores, siempre y cuando tenga los permisos suficientes para realizar esta acción.

---
