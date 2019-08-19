# AWS Marketplace

_ami-0273150f1f5fefd92`_

Ahora que ya tenemos nuestro motor de bases de datos funcionando podemos pasar a configurar nuestra aplicación. En este caso, queremos poner en producción un blog personal, en particular [Ghost](https://ghost.org/es/).

Si vamos a la [documentación](https://docs.ghost.org/install/ubuntu/) de esta aplicación podemos ver los pasos que debemos seguir para su instalación. Siguiendo esta guía podemos configurar todos los parámetros de acuerdo a nuestas necesidades, partiendo de una `AMI` de Ubuntu 18.04 por ejemplo. Una vez terminadas nuestras configuraciones principales, podríamos crear una nueva `AMI` que incorpore todos los cambios que le realizamos a la `AMI` inicial. De esta manera podremos levantar múltiples instancias con esta configuración, o hacer una restauración a fabrica si algo sale mal.

No realizaremos nínguna de estas acciones. En cambio, utilizaremos el **AWS Marketplace** para obtener una `AMI` con todo lo que necesitamos instalado.

El AWS Marketplace es un catalogo digital de `AMI` que permite acceder a `AMI` desarrolladas por múltiples fabricantes, simplificando el proceso de instalación de nuevas aplicaciones. Algunas de las categorías de aplicaciones que se pueden encontrar son: Seguridad, Networking, Almacenamiento, Machine Learning, Business Intelligence, etc.

Todos los clientes pueden utilizar estas `AMI` como punto de partida de sus instancias. Alguna de ellas cuentan con un licenciamiento adicional para su uso, el cual es mostrado al momento de levantar la instancia desde el portal web. Esta licencia es cobrada por AWS directamente, junto con el costo de la instancia. AWS luego le paga al proveedor de la AMI lo que corresponde a la licencia.

No solamente podemos utilizar el AWS Marketplace como consumidores, podemos utilizarlo para ofrecer nuestras propias AMI. Lo único que tenemos que hacer es subir la `AMI` correspondiente, la cual sera analizada por AWS, y si todo sale bien, será públicada en todo el mundo.

Por último, existen las `AMI` de la comunidad que son `AMI` creadas por usuarios de AWS con permisos públicos para ser utilizados por otras cuentas. Esta claro que estas `AMI` no cuentan con el mismo nivel de seguridad que las mencionadas anteriormente dado que no son analizadas por un cuerpo validador. Tampoco podemos confiar de primera mano el software que viene pre-instalado en las maquina. Sin embargo, para aquellos casos en que conozcamos la fuente de la `AMI`, son una muy buena opción para simplificar la instalación de nuevos servicios.

---

## 💻 DEMO #19 ~ Levantar una instancia de Ghost <a name="demo001"></a>

Mostraremos como realizar este procedimiento desde la `cli`.

### Procedimiento (`cli`)

Primero debemos obtener la `ImageId` de la `AMI` de Ghost que queremos utilizar, dado que la `ImageId` depende de la región. Para simplificar la obtención de esta información vamos a utilizar el programa `jq` que permite manipular JSON. Lo podemos instalar haciendo `sudo yum install jq`.

```
# Obtenemos la ImageId de la ami
export AMI=$(aws ec2 describe-images \
  --filters Name=name,Values=ghost-cdh-2.0.0 \
  --query 'sort_by(Images, &CreationDate)[-1].[ImageId]' \
  --output json \
  | jq -r ".[0]" \
); echo "AMI=$AMI";

# Obtenemos el id de nuestro VPC
aws ec2 describe-vpcs \
  --query 'Vpcs[*].{Id:VpcId,Tags:Tags}' \
  --output json
# Cargamos la variable `VPC` con el ID de nuestro VPC
export VPC_ID=

# Obtenemos la lista de subnets dentro de nuestro VPC
aws ec2 describe-subnets \
  --filters Name=vpc-id,Values=$VPC_ID \
  --query 'Subnets[*].{Name:Tags[0].Value, Id:SubnetId}'
# Cargamos la variable `SUBNET_ID` con alguna de nuestas subnet privadas
export SUBNET_ID=

# Obtenemos la id del `Security Group` previamente creado.
aws ec2 describe-security-groups \
  --filters Name=vpc-id,Values=$VPC_ID \
  --query 'SecurityGroups[*].{Name:GroupName, ID:GroupId}'
# Cargamos la variable `SG_ID` con nuestro Security Group
export SG_ID=

# Obtenemos la lista de llaves disponibles
aws ec2 describe-key-pairs
# Cargamos la variable `KEY` con el nombre de nuestra llave
export KEY=

# Confirmamos que tenemos todas las variables de entorno cargadas correctamente
echo "AMI       = $AMI" ;\
echo "VPC_ID    = $VPC_ID" ;\
echo "SUBNET_ID = $SUBNET_ID" ;\
echo "SG_ID     = $SG_ID" ;\
echo "KEY       = $KEY"

# Creamos la instancia
aws ec2 run-instances \
  --instance-type t3.small \
  --image-id $AMI \
  --subnet-id $SUBNET_ID \
  --security-group-ids $SG_ID \
  --no-associate-public-ip-address  \
  --key-name $KEY
```

Como son tantos comandos empieza a ser conveniente correlos como un `script`:

```bash
#!/bin/bash

clear

echo "Seleccion de la AMI"
echo "-------------------"
echo
read -p "¿Cual es el nombre de la AMI que quiere levantar? [ghost-cdh-2.0.0]: " AMI_NAME
AMI_NAME=${AMI_NAME:-ghost-cdh-2.0.0}

AMI=$(aws ec2 describe-images \
  --filters Name=name,Values=$AMI_NAME \
  --query 'sort_by(Images, &CreationDate)[-1].[ImageId]' \
  --output json \
  | jq -r ".[0]" \
);

clear

echo "Seleccion del VPC"
echo "-----------------"
echo
aws ec2 describe-vpcs \
  --query 'Vpcs[*].{Id:VpcId,Tags:Tags}' \
  --output json
read -p "¿Que VPC quiere utilizar? (vpc-...): " VPC_ID

clear

echo "Seleccion de Subnet"
echo "-------------------"
echo
aws ec2 describe-subnets \
  --filters Name=vpc-id,Values=$VPC_ID \
  --query 'Subnets[*].{Name:Tags[0].Value, Id:SubnetId}'
read -p "Que subnet quiere utilizar? (subnet-0...): " SUBNET_ID

clear

echo "Seleccion del Security Group"
echo "----------------------------"
echo
aws ec2 describe-security-groups \
  --filters Name=vpc-id,Values=$VPC_ID \
  --query 'SecurityGroups[*].{Name:GroupName, ID:GroupId}'
read -p "Que Security Group quiere utilizar? (sg-...): " SG_ID

clear

echo "Seleccion de llave privada"
echo "--------------------------"
echo
aws ec2 describe-key-pairs
read -p "Que llave privada quier utilizar? (KeyName): " KEY

clear

echo "Verifique sus valores"
echo "---------------------"
echo
echo "AMI       = $AMI" ;\
echo "VPC_ID    = $VPC_ID" ;\
echo "SUBNET_ID = $SUBNET_ID" ;\
echo "SG_ID     = $SG_ID" ;\
echo "KEY       = $KEY"
read -p "Desea continuar creando la instancia con estos valores? [Y/n]: " CONTINUE
CONTINUE=${CONTINUE:-Y}

if [[ $CONTINUE != "Y" ]]; then
    echo "No se creara la instancia. Muchas gracias."
    exit
fi

clear

echo "Crendo la instancia"
echo "==================="
echo
aws ec2 run-instances \
  --instance-type t3.small \
  --image-id $AMI \
  --subnet-id $SUBNET_ID \
  --security-group-ids $SG_ID \
  --no-associate-public-ip-address  \
  --key-name $KEY
```

### FAQ

**¿Porque debo buscar la id de la `AMI`?**

Las `AMI` son únicas por region. Por lo tanto, debemos hallar la que corresponde a nuestra región en particular.

**¿Como obtengo las credenciales para acceder a la nueva instancia?**

Cada `AMI` del marketplace tiene una página dentro del catalogo con la información de conexión. En este caso, es necesario dirigirse a [la siguiente](https://aws.amazon.com/marketplace/pp/B00NPHLY8W?ref=cns_1clkPro#pdp-pricing) dirección y dirigirse a la sección `Usage Information`.

En este caso, el usuario de `ssh` es `ec2-user`.

---

Cuanto más recuros tenemos, más compleja es la logica para levantar nuestro ambiente.

Ahora que tenemos la instancia levantada, tenemos que configurarla para conectarla a nuestra base de datos.

---

## 💻 DEMO #20 ~ Configurar la nueva instancia de Ghost <a name="demo002"></a>

Mostraremos como realizar este procedimiento desde la `cli`.

### Procedimiento (`cli`)

Lo importante de este procedimiento no son las acciones puntuales para levantar la aplicación, las cuales son específicas para la demonstración. La idea es simular la puesta en producción de una aplicación.

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
    cd /srv/ghost
    # Editamos el archivo de configuración
    sudo vim .env
    # o con nano
    sudo nano .env

    # Es necesario modificar:
    #  1. El host del motor de base de datos.
    #  2. El usuario master del motor de base de datos.
    #  3. La contraseña del usuario master del motor de base de datos.

    # Reiniciamos el servicio de Ghost
    sudo systemctl stop ghost.service
    sudo systemctl start ghost.service
    ```
4. Verificar el funcionamiento de la aplicación `ghost` con `curl` desde el bastión, o abriendo un túnel `ssh` entre su maquina local y el puerto 80 de la instancia `ghost` a través del bastión.
    ```bash
    # Desde el bastion: curl [Respuesta 200 OK]
    curl http://<ip_privada_del_ghost>:8080 -I

    # Desde su maquina local: túnel ssh [en el browser abrir http://localhost:8080]
    ssh -i <llave_privada_del_bastion> \
      -L 8080:<ip_privada_del_ghost>:8080 \
      ec2-user@<ip_publica_del_bastion>
    ```

> OBS: el dashboard de administración de la aplicación se encuentra en la dirección: `http://localhost:8080/admin` (abriendo previamente un túnel en el puerto `8080`).

### FAQ

**¿Que es un túnel `ssh`?**

Es una funcionalidad que provee `ssh` para mover tráfico entre redes privadas sobre otra red. En este caso, construímos un túnel entre nuestra maquina local y la instancia `ghost` a través del bastión haciendo que todo nuestro tráfico al puerto `8080` sea enviado al puerto `8080` de la instancia del `ghost`.

---

Ahora tenemos una aplicación conectada a la base de datos, pero:

1. No pudeo accer a través de Internet a la misma.
2. No cuenta alta disponibilidad
3. No cuento con níngun procedimiento de Disaster Recovery

Idealmente, nos gustaría tener más de una instancia sirviendo a la aplicación; conectada a una base de datos robusta y escalable; y contar con un balanceador de tráfico que termine las conexiones de los clientes y las distribuya a las instancias de la aplicación. Además, necesitamos un metodo para reconstruir las instancias en caso de errores, y para escalarlas horizontalmente si la demanda de conexiones aumenta. El tamaño de cada una de ellas dependerá de la aplicación que estemos ejecutando. En general, podemos utilizar muchas instancias pequeñas cuando la necesidad de computo es baja, y los cuellos de botella suelen darse en la red. Si en cambio la necesidad de computo es muy alta utilizaremos instancias más grandes. No existe una formula que nos permita estimar a priori el timpo de instancia que más nos combiene, necesariamente vamos a tener que hacer algunas pruebas para llegar a la configuración óptima. Basicamente, queremos que la cantidad de instancias que estén sirviendo nuestra aplicación se elastica. Que se adapte a los requerimientos de forma dínamica.

Para conseguir esto vamos a ver como funcionan los `Auto Scaling Groups`.

---
<div style="width: 100%">
  <div style="float: left"><a href="../guias/11_rds.md">⬅️11 - RDS</a></div>
  <div style="float: right"><a href="../guias/13_auto_scaling_groups.md">13 - Auto Scaling Groups ➡️</a></div>
</div>
