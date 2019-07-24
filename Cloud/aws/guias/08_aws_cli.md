# AWS `cli`.

## Métodos de interacción con los servicios de AWS

En la consola de administración de AWS tenemos acceso a todos los servicios y a todas sus funcionalidades. El problema es que la interfaz web de la consola no se presta para realizar acciones de forma automática y no es la forma más rápida para interactuar con algunos servicios de AWS.

Para remediar esta situación, AWS ofrece múltiples formas de interactuar con sus servicios además de la consola. 

Ordenados en órden de complejidad estos son:

- `cli`: Aplicación de línea de comandos.
- `SDKs`: Kits de desarrollo para múltiples sistemas.
- `CloudFormation`: Servicio de AWS de `Infrastructure as Code`.
- `CDK`: Permite levantar servicios de AWS utilizando lenguajes de programación, y construir abstacciones sobre los mismos. Lenguajes soportados: Python, Typescript, Javascript, .NET, y Java.

Durante el curso interactuaremos los primeros tres métodos, haciendo enfasís en la `cli` y en `CloudFormation`.

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

> ❗❗️❗️<br/>Si esta trabajando desde una Mac es recomendable que realice la instalación con el siguiente comando, ya que existe un bug en una de sus dependencias.</br>❗❗️❗️

```
pip install aws-shell --upgrade --ignore-installed siz
```

### Configuración de la `cli`

> ❗❗️❗️<br/>Los siguientes ejemplos se realizarán sobre `aws-shell` sin embargo, todos los comandos pueden utilizarse de la misma manera sobre la `cli` sin modificaciones.</br>❗❗️❗️

---

### 💻 DEMO #15 ~ Configuración de la `cli` <a name="demo015"></a>

Las credenciales mencionadas en esta sección serán provistas por el moderador. Si por algún motivo no cuenta con estas credenciales, consulte con alguno de los ayudantes.

También se puede realizar los siguientes pasos con las credenciales de su cuenta personal.

**La primera vez que se ejecute `aws-shell` se generara el indice de `autocomplete` por lo que puede demorar unos minutos en iniciar.**

#### Procedimiento

0. Correr `aws-shell` (solamente si va a utilizar este programa).
1. Lanzar el comando `configure`.
2. Ingresar su AWS Access Key ID.
3. Ingresar su AWS Secret Access Key.
4. Seleccione su región (la misma que fue asignada anteriormente.)
5. Seleccione `table` como `Default output format`.

#### FAQ

**¿Como se que `string` corresponde a mi región?**

Puede utilizar [este link](https://docs.aws.amazon.com/general/latest/gr/rande.html) como referencia.

**¿Que pasa si no tengo credenciales de acceso programatico?**

No podrá utilizar ninguna de las interfaces de gestión de AWS programaticas.

**¿Como consigo credenciales de acceso programatico?**

El administrador de la cuenta de AWS puede crear usuarios desde el servicio `IAM`. Estos usuarios cuentan con múltiples tipos de credenciales para acceder a la cuenta de AWS, entre ellos, credenciales de acceso a la consola Web y credenciales de acceso prográmatico. Solamente un administrador de la cuenta puede crear credenciales para otros usuarios. Además, un usuario puede recrear sus credenciales de acceso prográmatico si siente que pueden haberse comprometido las anteriores, siempre y cuando tenga los permisos suficientes para realizar esta acción.

**¿Tengo que correr el comando `configure` cada vez que quiero usar la `cli`?**

No. El comando `configure` crea un archivo en la carpeta `~/.aws` llamado `credentials` en donde almacena las credenciales. Dentro de este archivo se pueden cargar múltiples credenciales, de múltiples cuentas de AWS. Luego al momento de utilizar la `cli` se puede indicar que credencial utilizar mediante la opción `--profile` seguida del nombre del perfil a utilizar.

---

La `cli` es llamada desde la consola a través del comando `aws` seguido del servicio/comando que queremos realizar y luego el subcomando y sus parámetros necesarios. Se pueden pasar opciones antes del comando/servicio, principalemente para modificar la salida de los datos.

```
aws [options] <command> <subcommand> [parameters]
```

Por ejemplo, en el siguiente ejemplo estamos realizando el comando `describe-regions` sobre el servicio `ec2`, configurando la salida en formato `json`.

```
aws ec2 --color="on" --output="json" describe-regions
```

Para obtener información sobre los subcomandos utilizamos la opción `help`.

```
aws s3 ls help
```

Se nos desplegara una `man page` en la consola con toda su información. Por ejemplo, para el comando `ls` de `s3` la salida es algo así:

```
NAME
       ls -

DESCRIPTION
       List  S3  objects and common prefixes under a prefix or all S3 buckets.
       Note that the --output and --no-paginate arguments are ignored for this
       command.

       See 'aws help' for descriptions of global parameters.

SYNOPSIS
            ls
          <S3Uri> or NONE
          [--recursive]
          [--page-size <value>]
          [--human-readable]
          [--summarize]
          [--request-payer <value>]
```

Reproduciremos los mismos pasos que realizamos sobre la consola web de S3 pero en la `cli`.

---

### 💻 DEMO #15 ~ Configuración de la `cli` <a name="demo015"></a>

#### Procedimiento

Comenzaremos por obtener la lista de `Buckets` disponibles en nuestra cuenta.

```
aws s3api list-buckets
```

Dentro de la lista existirá el `Bucket` que creamos en la demo anterior. Ahora listaremos todos los objetos que existan dentro de dicho `Bucket`.

```
aws s3 ls s3://<apellido>.<nombre>.cloud.devops
```

Ahora eliminaremos y volveremos a subir los mismos archivos que subimos anteriormente.

```
aws s3 rm s3://<apellido>.<nombre>.cloud.devops/<ruta_al_archivo>
aws s3 cp <ruta_del_archivo_a_subir> s3://<apellido>.<nombre>.cloud.devops/<ruta_del_archivo_en_s3>
```

El proceso de descargar la imagen es el mismo que utilizamos para subirla pero invirtiendo el orden de las rutas. La interfaz de la `cli` de S3 intenta simular el funcionamiento tradicional del `fs`.

#### FAQ

**¿Como se cual es el nombre del servicio que tengo que utilizar?**

El comando `aws help` devuelve la lista entera de servicios disponible. Combinando la salida con `grep` se puede obtener rapidamente el nombre buscado.

**¿Como se cuales son los subcomandos disponibles que tengo para realizar dentro del servicio?**

El comando `aws <command> help` devuelve la información de todos los subcomandos disponibles.

**¿Cuando es mejor configurar servicios desde la `cli`?**

La `cli` es especialmente útil cuando tengo que automatizar la creación de recursos; cuando tengo que crear múltiples recursos; o cuando quiero probar algo rápidamente. Además, hay ciertas acciones que son más faciles de realizar desde la `cli` que desde la consola web, como la carga y descarga de archivos.

---

Practicamente todos los servicios y todas sus funcionalidades están disponibles a través de la `cli`. Es una herramienta muy potente. Sin embargo, algunos de los subcomandos requieren de una gran cantidad de parámetros a configurar para funcionar, lo que los hace poco prácticos para tipear directo en la consola. Una opción para minimizar esto es a través de scripts. 

A continuación hay un ejemplo de un script que lanza una nueva instancia de la imagen "Amazon Linux 2", permitiendo solo la configuración del tipo de instancia y su IP privada.

> ❗❗️❗️<br/>Para probar este script desde sus maquinas en sus cuentas, deben modificar las variables encontradas bajo el comentario "CONSTANTES" con los recursos de su cuenta. Para encontrar estos valores utilice los siguientes comandos, u obtengalos desde la consola web.</br>❗❗️❗️

```bash
# Obtener el ID del Security Group
aws ec2 describe-security-groups \
    --query "SecurityGroups[*].{Name:GroupName,ID:GroupId}"

# Obtener el ID de la Private Subnet
aws ec2 describe-subnets \
    --query "Subnets[*].{Id:SubnetId}" \
    --output table --filters Name=tag:Name,Values=private_subnet
```

```bash
#!/bin/bash

usage() {
    echo "Uso: $0 [-t <tipo_de_instancia>] [-i <direccion_ip>]" 1>&2;
    exit 1;
}

### CONSTANTES
SECURITY_GROUP_ID=<security_group_id>
SUBNET_ID=<subnet_id>
###

while getopts ":t:i:" o; do
    case "${o}" in
        t)
            t=${OPTARG}
            ;;
        i)
            i=${OPTARG}
            ;;
        *)
            usage
            ;;
    esac
done
shift $((OPTIND-1))

if [ -z "${t}" ] || [ -z "${i}" ]; then
    usage
fi

echo
echo "Running new instance"
aws ec2 run-instances \
    --instance-type "${t}" \
    --private-ip-address "${i}" \
    --image-id ami-0de53d8956e8dcf80 \
    --subnet-id ${SUBNET_ID} \
    --security-group-ids ${SECURITY_GROUP_ID} \
    --no-associate-public-ip-address
echo
echo "Done"
```

Antes de poder correr este `script` debemos darle permisos de ejecución:

```bash
chmod +x ./script.sh
```

Con `scripts` y la `cli` de AWS podemos automatizar y simplificar todas las acciones queramos realizar sobre los recursos de AWS. Sin embargo, no es fácil mantener actualizado la lista de `script`; es díficil mantener una base de `scripts` común; y usualmente no son faciles de _debuggear_. Es por esto que existen otras formas de automatizar los recursos de la nube.

En este curso veremos dos de ellos:

- SDKs (boto)
- CloudFormation.

Mediante el uso de `SDK` podemos simplificar la interacción con los recursos de la nube y podemos tomar provecho de las funcionalidades que ofrecen los nuevos lenguajes de programación. Existen `SDK` para prácticamente todos los lenguajes más populares del momento, así como extensiva documentación de su uso.

Los `SDK` brindados son excelentes para extender el funcionamiento de nuestra aplicación con tecnologías de nube, manteniendo el acceso a nuestra cuenta de forma segura.

Utilizar un `SDK` no es suficiente mara mitigar todos los problemas mencionados anteriormente. Por más que utilizemos lenguajes más complejos, sigue siendo nuestra responsabilidad mantenerlos libres de _bugs_, extensibles, y fáciles de entender por el resto del equipo. El problema principal, es que estos `scripts` no representan nuestra arquitectura como código.

### ¿Que es `Infraestructure as Code` o `IaC`?

> [...el proceso de administrar y aprovisionar recursos computacionales en centros de datos a través de la definición de archivos, en vez de a través de configuración de hardware o a través de interfacez de configuración interactivas.]
> 
> ***Traducido del ingles de [Wikipedia](https://en.wikipedia.org/wiki/Infrastructure_as_code).**

Osea, es la capacidad de definir la infraestructura de nuestro sistema mediante la modificación de archivos de texto. Estos archivos son procesados por algún tipo de sistema, que los transforma en configuración y aprovisionamiento de servicio. De esta manera, conseguimos ser más declarativos en como definimos y configuramos nuestra infraestructura, _enfocandonos en el resultado, y no en el camino._

Administrar nuestros sistemas de esta manera tiene varias ventajas:

- **Auto-documentación**: Los archivos de texto mencionados describen completamente el estado de nuestra arquitectura, por lo que no necesitamos herramientas adicionales para describirla.
- **Homogeneidad**: Todos los recursos de nuestra red son configurados exactamente de la misma manera, ya sean recursos de red, sistemas, bases de datos, o aplicaciones. Esto simplifica su mantenimiento y entendimiento por parte del resto del equipo.
- **Idempotencia**: La aplicación del mismo juego de configuraciones múltiples veces no modifica las configuraciones. Esta característica es díficil de conseguir en nuestros propios scripts.
- **Mejor mantenimiento**: Una vez definida nuestra arquitectura, es fácil identificar que archivo tenemos que modificar para realizar cambios en la misma.

No todos los sistemas de `IaC` consiguen implementar todas estas carácteristicas completamente, pero de a poco tienden a ellas. Por otro lado, los archivos mencionados pueden resultar muy verbosos lo que puede dificultar su lectura.

`CloudFormation` es el servicio de `IaC` que brinda AWS a sus usuarios. Con el, se pueden configurar todos los servicios de su nube a través de archivos `yaml` o `json`. Cada juego de configuraciones, o `stack`, puede mantenersa aislado del otro, lo que permite construir arquitecturas multi-tenant con facilidad o múltiples ambientes de desarrollo. La eliminación de un `stack` lanzará la eliminación de todos los recursos creados por el, lo que simplifica enormemente las tareas de limpieza y mantenimiento de servicios, y evita gastos innecesarios en la cuenta.

Veremos como utilizar ambas herramientas más adelante.