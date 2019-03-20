# Amazon RDS

Servicio de AWS diseñado para crear, operar, y escalar bases de datos relacionales. Este servicio se encarga de:

- Escalar de forma independiente CPU, RAM, almacenamiento, e IOPS.
- Administrar la gestión de respaldos, actualización de software, detección de fallos, y disaster recovery.
- Oculta el acceso a áreas sensibles de la base de datos.
- Capacidad de crear snapshots de las instancias.
- Alta disponibilidad a través de instancias sincronas secundarias.
- Read replicas para MariaDB, MySQL, o PosgreSQL.
- Productos soportados: MySQL, MariaDB, PostgreSQL, Oracle, Microsoft SQL Server.
- Control de acceso a través de IAM.

## Instancias

El componente principal de RDS son las instancias. Dentro de cada instancia corre un motor de bases de datos independiente, sobre el cual se pueden levantar múltiples bases de datos con las herramientas que estmos acostumbrados a utilizar para cada producto. 

Las capacidades de cada instancia son determinadas en base a su clase. Dependiendo de la demanda del motor de bases de datos que se necesite, es la clase de instancia que se deberá configurar. Con respecto al almacenamiento, se pueden elegir entre tres tecnologías: Magneticos, SSD de proposito general, o IOPS a medida. Cada una de ellas varía en precio y rendimiento. 

Las instancias de RDS pueden correr dentro de un VPC, desde donde se puede controlar el acceso a la misma desde el resto de nuestra red. Tal como con las instancias de EC2, las instancias de RDS cuentan con `Security Groups` que ayudan a limitar el acceso a la misma.

---

### 💻 DEMO #01 ~ Creación de una instancia de RDS <a name="demo001"></a>

Mostraremos como realizar este procedimiento desde la consola de administración y la `cli`.

#### Procedimiento (Web)

1. Ir al Dashboard de RDS.
2. Hacer click en `Create database`.
3. Hacer click en `Next`.
4. Seleccionar `Dev/Test - MySQL`.
5. Hacer click en `Next`.
6. En el cuadro `Free tier` seleccionar la opción que dice `Only enable options eligible for RDS Free Usage Tier`.
7. En la sección `Settings` colocar:
   1. Un identificador único para su base. Por ejemplo: `mydbinstance`.
   2. Un usuario master. Por ejemplo: `conatel`.
   3. Una contraseña para el usuario master.
8. Hacer click en `Next`.
9. Seleccionar el `VPC` con el cual estabamos trabajando.
10. Seleccionar la `subnet` privada con la cual estamos trabajando.
11. Seleccionar `No` en `Public accessibility`.
12. Seleccionar `Choose existing VPC security groups` en la sección `VPC security groups`.
13. Seleccionar un `Security Group` existente.
14. Ingresar un nombre para la base de datos por defecto. Por ejemplo: `conatel`.
15. Configurar el tiempo de retención del Backup en `0` días.
16. Hacer click en `Create database`.
17. Hacer click en `View DB Instance details`.

#### Procedimiento (`cli`)

La lista de clases de instancia de RDS se encuentra [en esta dirección](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.DBInstanceClass.html). Utilizaremos la clase `db.t2.micro` en esta instancia.

```
# Obtenemos la lista de VPCs para identificar el ID de nuestro VPC
aws ec2 describe-vpcs --query 'Vpcs[*].[VpcId, Tags[*]]'

# Obtenemos la lista de subnets dentro de nuestro VPC
aws ec2 describe-subnets \
--filters Name=vpc-id,Values=<vpc_id> \
--query 'Subnets[*].[SubnetId]'

# Creamos un subnet group
aws rds create-db-subnet-group \
--db-subnet-group-name <nombre_de_subnet_group> \
--db-subnet-group-description <descripcion_del_subnet_group>
--subnet-ids <lista_de_subnet_ids>

# Creamos una instancia de RDS asociada al nuevo subnet group
aws rds create-db-instance \
--allocated-storage 20 \
--db-instance-class db.t2.micro \
--engine mysql \
--storage-type standard \
--no-publicly-accesible \
--no-multi-az \
--db-subnet-group-name <nombre_del_subnet_group_prviamente_creado> \
--db-instance-identifier <identificador_de_su_instancia> \
--master-username <usuario_master> \
--master-user-password <password_de_usuario_master>

# Listamos las instancias de RDS
aws rds describe-db-instances \
--query 'DBInstances[*].{ID: DBInstanceIdentifier}'
```

#### FAQ

**¿Que es un `Subnet Group`?**

Un `Subnet Group` es una colección de `subnets` utilizada para asignar una instancia de `RDS` a un `VPC`. Esta lista de `subnets` más una selección de la zona de disponibilidad preferida, será utilizada por RDS para asignar una dirección IP dentro del `VPC`.

**¿Como hago para modificar la configuración de mi instancia de RDS?**

Dentro del dashboard de administración de la instancia hay una opción llamada `Modify` que permite ajustar todos los parámetros de configuración. También puede realizar estas modificaciones desde la `cli`. Prácticamente todas las opciones de la base de datos pueden ser modificadas luego de su creación.

---