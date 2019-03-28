# App

Ahora que ya tenemos nuestro motor de bases de datos funcionando podemos pasar a configurar nuestra aplicación. En este caso, queremos poner en producción un blog personal, en particular [Ghost](https://ghost.org/es/).

Si vamos a la [documentación](https://docs.ghost.org/install/ubuntu/) de esta aplicación podemos ver los pasos que debemos seguir para su instalación. Siguiendo esta guía podemos configurar todos los parámetros de acuerdo a nuestas necesidades, partiendo de una `ami` de Ubuntu 18.04 por ejemplo. Una vez terminadas nuestras configuraciones principales, podríamos crear una nueva `ami` que incorpore todos los cambios que le realizamos a la `ami` inicial. De esta manera podremos levantar múltiples instancias con esta configuración, o hacer una restauración a fabrica si algo sale mal.

No realizaremos nínguna de estas acciones. En cambio, utilizaremos el **AWS Marketplace** para obtener una `ami` con todo lo que necesitamos instalado.

## AWS Marketplace

El AWS Marketplace es un catalogo digital de `ami` que permite acceder a `amis` desarrolladas por múltiples fabricantes, simplificando el proceso de instalación de nuevas aplicaciones. Algunas de las categorías de aplicaciones que se pueden encontrar son: Seguridad, Networking, Almacenamiento, Machine Learning, Business Intelligence, etc.

Todos los clientes pueden utilizar estas `ami` como punto de partida de sus instancias. Alguna de ellas cuentan con un licenciamiento adicional para su uso, el cual es mostrado al momento de levantar la instancia desde el portal web. Esta licencia es cobrada por AWS directamente, junto con el costo de la instancia. AWS luego le paga al proveedor de la AMI lo que corresponde a la licencia.

No solamente podemos utilizar el AWS Marketplace como consumidores, podemos utilizarlo para ofrecer nuestras propias AMI. Lo único que tenemos que hacer es subir la `ami` correspondiente, la cual sera analizada por AWS, y si todo sale bien, será públicada en todo el mundo.

Por último, existen las `AMI` de la comunidad que son `AMI` creadas por usuarios de AWS con permisos públicos para ser utilizados por otras cuentas. Esta claro que estas `AMI` no cuentan con el mismo nivel de seguridad que las mencionadas anteriormente dado que no son analizadas por un cuerpo validador. Tampoco podemos confiar de primera mano el software que viene pre-instalado en las maquina. Sin embargo, para aquellos casos en que conozcamos la fuente de la `AMI`, son una muy buena opción para simplificar la instalación de nuevos servicios.

---

### 💻 DEMO #01 ~ Levantar una instancia de Ghost <a name="demo001"></a>

Mostraremos como realizar este procedimiento desde la `cli`.

#### Procedimiento (`cli`)

Primero debemos obtener la `ImageId` de la `ami` de Ghost que queremos utilizar, dado que la `ImageId` depende de la región.

```
# Obtenemos la ImageId de la ami
aws ec2 describe-images \
--filters Name=name,Values=conatel_ghost_4.0.0 \
--query 'sort_by(Images, &CreationDate)[-1].[ImageId]'

# Obtenemos el id de nuestro VPC

aws ec2 describe-vpcs \
--filters Name=tag:Name,Values=<nombre_del_vpc> \
--query 'Vpcs[*].VpcId'

# Obtenemos la lista de subnets dentro de nuestro VPC
aws ec2 describe-subnets \
--filters Name=vpc-id,Values=<vpc_id> \
--query 'Subnets[*].{Name:Tags[0].Value, Id:SubnetId}'

# Obtenemos la id del `Security Group` previamente creado.
aws ec2 describe-security-groups \
--filters Name=vpc-id,Values=<vpc_id> \
--query 'SecurityGroups[*].{Name:GroupName, ID:GroupId}'

# Creamos la instancia
aws ec2 run-instances \
--instance-type t1.small \
--image-id <image_id> \
--subnet-id <private_subnet_id> \
--security-group-ids <security_group> \
--no-associate-public-ip-address  \
--private-ip-address <private_ip_address> \
--key-name <key_name>

```

Como son tantos comandos empieza a ser conveniente correlos como un `script`:

```bash
#!/bin/bash

VPC_NAME=<VPC_NAME>
SUBNET_NAME=<SUBNET_NAME>
GROUP_NAME=<GROUP_NAME>
KEY_NAME=<KEY_NAME>
PROFILE=<REGION>
INSTANCE_TYPE=t2.small
IMAGE_NAME=conatel_ghost_2.0.0
PRIVATE_IP='10.0.1.20'
REGION=us-east-1

# Obtiene la id de una ami según su nombre.
function image_id {
  aws ec2 describe-images \
    --filters Name=name,Values=$IMAGE_NAME \
    --query 'sort_by(Images, &CreationDate)[-1].{Id: ImageId}' \
    --region $REGION \
    --profile $PROFILE | jq -r .Id
}
# Obtiene la id de un VPC según su nombre.
function vpc_id {
  aws ec2 describe-vpcs \
    --filters Name=tag:Name,Values=$VPC_NAME \
    --query 'Vpcs[0].{Id: VpcId}' \
    --region $REGION \
    --profile $PROFILE | jq -r .Id
}
# Obtiene la id de una Subnet según su nombre.
function subnet_id {
  aws ec2 describe-subnets \
    --filters Name=tag:Name,Values=$SUBNET_NAME \
    --query 'Subnets[0].{Id: SubnetId}' \
    --region $REGION \
    --profile $PROFILE | jq -r .Id
}
# Obtiene la id de un Security Group según su nombre.
function security_group {
  aws ec2 describe-security-groups \
    --filters Name=group-name,Values=$GROUP_NAME \
    --query 'SecurityGroups[0].{Id: GroupId}' \
    --region $REGION \
    --profile $PROFILE | jq -r .Id
}
# Comando para crear la instancia de Ghost en EC2
aws ec2 run-instances \
  --instance-type $INSTANCE_TYPE \
  --image-id `image_id` \
  --subnet-id `subnet_id` \
  --security-group-ids `security_group` \
  --no-associate-public-ip-address \
  --private-ip-address $PRIVATE_IP \
  --key-name $KEY_NAME \
  --region $REGION \
  --profile $PROFILE | jq
```

#### FAQ

**¿Porque debo buscar la id de la `ami`?**

Las `ami` son únicas por region. Por lo tanto, debemos hallar la que corresponde a nuestra región en particular.

**¿Como obtengo las credenciales para acceder a la nueva instancia?**

Cada `ami` del marketplace tiene una página dentro del catalogo con la información de conexión. En este caso, es necesario dirigirse a [la siguiente](https://aws.amazon.com/marketplace/pp/B00NPHLY8W?ref=cns_1clkPro#pdp-pricing) dirección y dirigirse a la sección `Usage Information`.

En este caso, el usuario de `ssh` es `bitnami`.

---

Ahora que tenemos la instancia levantada, tenemos que configurarla para conectarla a nuestra base de datos.

---

### 💻 DEMO #02 ~ Levantar una instancia de Ghost <a name="demo002"></a>

Mostraremos como realizar este procedimiento desde la `cli`.

#### Procedimiento (`cli`)

Lo importante de este procedimiento no son las acciones puntuales para levanta la aplicación, las cuales son específicas para la demonstración. La idea es simplemente observar cual sería el procedimiento general para poner en producción nuestro ambiente dentro de nuestra infraestructura.

1. Establecer una conexión SSH con el bastion
    ```bash
    ssh -i <llave_privada_del_bastion> ec2-user@<ip_publica_del_bastion>
    ```
2. Establecer una conexión SSH con la instancia de Ghost desde el bastion.
    ```bash
    ssh -i <llave_privada_del_ghost> ubuntu@<ip_privada_del_ghost>
    ```
3. Realizar el siguiente procedimiento:
```bash
# Modificamos el archivo de configuración del ghost
cd /var/www/ghost
vim ./config.prod.json
# Es necesario modificar:
#  1. El host del motor de base de datos.
#  2. El usuario master del motor de base de datos.
#  3. La contraseña del usuario master del motor de base de datos.
# Reiniciamos la aplicación `ghost`.
ghost restart
```
4. Verificar el funcionamiento de la aplicación `ghost` con `curl` desde el bastión, o abriendo un túnel `ssh` entre su maquina local y el puerto 80 de la instancia `ghost` a través del bastión.
```bash
# Desde el bastion: curl [Respuesta 200 OK]
curl <ip_privada_del_ghost>

# Desde su maquina local: túnel ssh [en el browser abrir http://localhost:8080]
ssh -i <llave_privada_del_bastion> \
-L 8080:<ip_privada_del_ghost>:80 \
ec2-user@<ip_publica_del_bastion>
```
5. Creamos un snapshot de la instancia del ghost re-configurada.
6. Creamos una nueva `AMI` basandonos en la snapshot recien realizada.

**OBS: el dashboard de administración de la aplicación se encuentra en la dirección: `http://localhost:8080/admin` (abriendo previamente un túnel en el puerto 8080).**

#### FAQ

**¿Que es un túnel `ssh`?**

Es una funcionalidad que provee `ssh` para mover tráfico entre redes privadas sobre otra red. En este caso puntual, construímos un túnel entre nuestra maquina local y la instancia `ghost` a través del bastión sobre los puertos 8080 y 80.

**¿Porque creo una nueva `AMI` al finalizar el proceso de configuración?**

Porque ahora contamos con una imagen inicial de nuestra aplicación, preconfigurada para trabajar sobre nuestra infraestructura. Esto nos permite: poder volver atras en el tiempo; realizar una restauración de la aplicación; levantar múltiples ambientes basado en la misma maquina, etc.

---

La idea es que todo el estado de nuestra aplicación este almacenado en la base de datos, la cual sabemos esta configurada para escalar horizontalmente y cuenta con protección de datos, respaldos, etc. Por encima de la base de datos, levantaremos tantas instancias de nuestra aplicación como sea necesario para soportar el tráfico. El tamaño de cada una de ellas dependerá de la aplicación que estemos ejecutando. En general, podemos utilizar muchas instancias pequeñas cuando la necesidad de computo es baja, y los cuellos de botella suelen darse en la red. Si en cambio la necesidad de computo es muy alta utilizaremos instancias más grandes. No existe una formula que nos permita estimar a priori el timpo de instancia que más nos combiene, necesariamente vamos a tener que hacer algunas pruebas para llegar a la configuración óptima. Los servicios de `cloud` simplifican enormemente la realización de estas pruebas.

Un problema que tenemos cuando creamos una nueva `AMI` de esta manera, es que si queremos modificar la información de conexión de la base de datos, tenemos que crear una nueva `AMI`. Para este caso particular, los pasos que debemos realizar son muy faciles de realizar a través de un script. EC2 cuenta con una opción avanzada denominada `UserData` que permite pasar un script que será ejecutado una única vez al momento de creación de una instancia. Por ejemplo, podríamos usar algo así:

```bash
#!/bin/bash -v
# Configuramos un log del script
set -x
exec > >(tee /var/log/user-data.log|logger -t user-data ) 2>&1
echo BEGIN
date '+%Y-%m-%d %H:%M:%S'
# Nos movemos al directorio de Ghost
cd /var/www/ghost/
# Respaldamos la configuración inicial
mv config.production.json config.production.json.old
# Modificamos los campos de conexión a la base de datos.
cat config.production.json.old \
| jq -r '.database.connection.host="${Cloud101DatabaseAddress}"' \
| jq -r '.database.connection.user="${Cloud101DatabaseMasterUser}"' \
| jq -r '.database.connection.password="${Cloud101DatabaseMasterUserPassword}"' \
> config.production.json
# Volvemos asignar la propiedad del archivo de configuración al usuario ubuntu
chown ubuntu /var/www/ghost/config.production.json
# Reiniciamos ghost
su -c 'ghost restart --no-prompt --no-color --dir /var/www/ghost' - ubuntu
# ------
```

Algunas particularidades de este `script`:

1. Dentro de nuestra instancia podemos encontrar disponibles todos los logs generados durante su creación, incluidos aquellos generados durante la ejecución de nuestro `script`. Estos logs son muy extensos lo que hace dificil utilizarlos para encontrar errores al momento de debuguear. Por lo tanto, creamos nuestro propio archivos de  logs.
2. Este es un `script` de ejemplo, por lo que vamos a dejar fija la información de conexión a la base de datos. No es muy complejo modificarlo para poder obtener estos valores de forma dinamica.
3. El `script` sera ejecutado por el usuario `root` por defecto. Lo que significa que aquellos comandos que deban ser ejecutados por otro usuario deben ser identificados de forma explicita. Lo mismo sucede cuando modificamos un archivo.
