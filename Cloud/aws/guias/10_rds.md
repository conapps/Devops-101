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

## 💻 DEMO #1 ~ Creación de una instancia de RDS <a name="demo018"></a>

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
aws ec2 describe-vpcs \
  --query 'Vpcs[*].{Id:VpcId,Tags:Tags}' --output json

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

**¿Que es Amazon Aurora?**

Es una base de dato relacional completamente administrada por AWS, compatible con MySQL y PostgreSQL. AWS expresa que es capaz de manejar hasta 5 veces más throughput que MySQL y hasta 3 veces más que PostgreSQL. El producto ofrece alta disponibilidad, escalabilidad, y alto rendimiento por defecto. 

**¿Como puedo comprobar que la base esta funcionando?**

Desde una instancia dentro de nuestro `VPC` podemos instalar `mysql` a través de `yum`.

```bash
sudo yum install mysql
```

Una vez instalado usamos el siguiente comando para conectarnos:

```
mysql -h <url_de_la_instancia_de_rds> -u <master_user> -p
```

**Segui los pasos anteriores pero no puedo conectarme, ¿cual es el problema?**

Verífique que el `security group` que tenga asignado a su instancia de `RDS` cuente con reglas que permitan la conexión de su instancia de `EC2`. El puerto por defecto en el que esta publicado `mysql` es `3306`.

---

Podemos veríficar que la base de datos esta funcionando utilizando el cliente de `mysql`.

```bash
# Instalamos el clente de mysql
sudo yum install mysql

# Obtenemos la dirección de la instancia de RDS
aws rds describe-db-instances \
  --query 'DBInstances[*].Endpoint'

# Nos conectamos a la base utilizando el cliente de mysql
mysql -h <rds_host> -u <master_username> -p
```

Si todo funciona bien veremos un prompt similar a: `MySQL [(none)]>`.

Utilice los siguientes comandos para crear una nueva base de datos y una tabla dentro de la misma.

```sql
CREATE DATABASE conatel;
USE conatel;
CREATE TABLE people (id SERIAL NOT NULL, name VARCHAR(30));
INSERT INTO people (name) VALUES ('John Doe'), ('Jane Doe');
SELECT * FROM people;

+----+--------------+
| id | name         |
+----+--------------+
|  1 | John Doe     |
|  2 | Jane Doe     |
+----+--------------+
```

---
<div style="width: 100%">
  <div style="float: left"><a href="../guias/09_aws_cli.md">⬅️09 - AWS `cli`</a></div>
  <div style="float: right"><a href="../guias/11_marketplace.md">11 - Marketplace ➡️</a></div>
</div>
