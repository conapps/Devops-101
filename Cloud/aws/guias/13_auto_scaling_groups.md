# Auto Scaling Groups

Un `Auto Scaling Group es una colección de instancias de EC2 que son tratadas como si fueran un único grupo logico. Habilitan la creación de chequeos de salud, y politicas de escalamiento, para controlar el estado y la cantidad de instancias dentro del grupo. 

Uno de los parámetros fundamentales en la configuración de un `Auto Scaling Group` es la cantidad de instancias deseadas. Al momento de lanzarlo, el `Auto Scaling Group` levantará todas las instancias necesarias para llegar a este número. Esta cantidad puede ser luego ajustada manualmente, o de forma automatica a través de políticas.

Un `Auto Scaling Group` realiza chequeos de salúd períodicos sobre las instancias. Cuando una es identificada como `Unhealthy`, la misma es eliminada, y una nueva instancia se crea para ocupar su lugar.

Cuando se cumple alguna de las políticas de escalamiento, el `Auto Scaling Group` comenzará a crea o destruir instancias de acuerdo a la misma. Se pueden configurar limites superiores e inferiores para controlar el número de instancias creadas o terminadas.

Múltiples zonas de disponibilidad se pueden configurar dentro de una `Auto Scaling Group` de manera que el distribuya las instancias de forma equitativa entre ellas. El `Auto Scaling Group` siempre mantrenrá las instancias balanceadas entre todas las zonas.

## Spot Instances 

> Las instancias de spot de Amazon EC2 le permiten aprovechar la capacidad de EC2 sin usar en la nube de AWS. Las instancias de spot están disponibles con un descuento de hasta el 90 % en comparación con los precios bajo demanda. Puede utilizar instancias de spot para diversas aplicaciones flexibles, sin estado y tolerantes a errores, como big data, cargas de trabajo en contenedores, CI/CD, servidores web, informática de alto rendimiento (HPC) y otras cargas de trabajo de prueba y desarrollo. Dado que las instancias de spot se integran perfectamente con otros servicios de AWS, incluidos Auto Scaling, EMR, ECS, CloudFormation, Data Pipeline y AWS Batch, puede elegir la manera de lanzar y mantener sus aplicaciones en ejecución en las instancias de spot.

> Además, puede combinar fácilmente las instancias de spot con instancias bajo demanda y RI para optimizar aún más el costo de la carga de trabajo con rendimiento. Gracias a la escala operativa de AWS, las instancias de spot pueden ofrecer escalado y ahorro de costos para ejecutar las cargas de trabajo de hiperescala. También tiene la opción de hibernar, detener o finalizar sus instancias de spot cuando EC2 reclama recuperar la capacidad con dos minutos de aviso. Solo AWS le ofrece un acceso sencillo a capacidad de cómputo sin usar a escala masiva; todo con un descuento de hasta el 90 %.  

[Source](https://aws.amazon.com/es/ec2/spot/)

Dentro de nuestros `Auto Scaling Group` podemos utilizar una combinación de instancias `spot` y `on-demand` para bajar costos. Tenemos varias variables que podemos modificar para combinar la cantidad de estas instancias que queremos que se levanten. El `Auto Scaling Group` se encargara de manejarlas por nosostros, e intentará levantar instanias `spot` siempre que pueda.

---

## 💻 DEMO #21 ~ Configurar un Auto Scaling Group <a name="demo020"></a>

Mostraremos como realizar este procedimiento desde la `cli`.

### Procedimiento (`cli`)

Las opciones de la `cli` de AWS pueden pasarse como JSON. Esto es especialmente útil cuando la cantidad de información que tenemos que configurar es tan grande que se vuelve complejo introducirla directo en la consola.

1. Obtenemos la `id` de nuestra imagen
  ```
  export AMI=$(aws ec2 describe-images \
    --filters Name=name,Values=ghost-cdh-2.0.0 \
    --query 'sort_by(Images, &CreationDate)[-1].[ImageId]' \
    --output json \
    | jq -r ".[0]" \
  ); echo "AMI=$AMI";
  ```
2. Obtenemos la `id` de nuestro `vpc`
  ```
  aws ec2 describe-vpcs \
    --query 'Vpcs[*].{Id:VpcId,Tags:Tags}' \
    --output json
  # Cargamos la variable `VPC` con el ID de nuestro VPC
  export VPC_ID=
  ```
3. Obtenemos las `id` de las `subnets` (las colocamos dentro de la variable `PRIVATE_SUBNETS` separadas por una coma `,`) de nuestro `vpc`
  ```
  aws ec2 describe-subnets \
    --filters Name=vpc-id,Values=$VPC_ID \
    --query 'Subnets[*].{Name:Tags[0].Value, Id:SubnetId}'
  export PRIVATE_SUBNETS=
  ```
4. Obtenemos el id de nuestro `Security Group`
  ```
  aws ec2 describe-security-groups \
    --filters Name=vpc-id,Values=$VPC_ID \
    --query 'SecurityGroups[*].{Name:GroupName, ID:GroupId}'
  # Cargamos la variable `SG_ID` con nuestro Security Group
  export SG_ID=
  ```
5. Obtenemos el nombre de la llave que queremos utilizar
  ```
  aws ec2 describe-key-pairs
  # Cargamos la variable `KEY` con el nombre de nuestra llave
  export KEY=
  ```
6. Obtenemos la `id` de la `AMI` que queremos utilizar
  ```
  export AMI=$(aws ec2 describe-images \
    --filters Name=name,Values=ghost-cdh-2.0.0 \
    --query 'sort_by(Images, &CreationDate)[-1].[ImageId]' \
    --output json \
    | jq -r ".[0]" \
  ); echo "AMI=$AMI";
  ```
7. Crear un archivo `launch_template_input.json` con la siguiente información:
  ```json
  {
    "LaunchTemplateName": "ghost-lt",
    "VersionDescription": "1",
    "LaunchTemplateData": {
      "NetworkInterfaces": [
        {
          "AssociatePublicIpAddress": false,
          "DeleteOnTermination": true,
          "DeviceIndex": 0,
          "Groups": [
            ""
          ]
        }
      ],
      "ImageId": "",
      "InstanceType": "t2.micro",
      "KeyName": "",
      "Monitoring": {
        "Enabled": true
      },
      "DisableApiTermination": false,
      "UserData": ""
    }
  } 
  ```
8. Escribimos las variables en el archivo JSON utilizando `jq`
  ```bash
  cat launch_template_input.json \
    | jq ".LaunchTemplateData.ImageId = \"$AMI\" | .LaunchTemplateData.KeyName = \"$KEY\" | .LaunchTemplateData.NetworkInterfaces[0].Groups = [\"$SG_ID\"]" \
    > .tmp && mv .tmp launch_template_input.json
  ```
9. Creamos el `Launch Template` pasando el archivo JSON como entrada:
  ```bash
  aws ec2 create-launch-template \
    --cli-input-json file://launch_template_input.json
  ```
10. Crear un archivo `auto_scaling_group_input.json` con la siguiente información:
  ```json
  {
    "AutoScalingGroupName": "ghost-asg",
    "MixedInstancesPolicy": {
      "LaunchTemplate": {
        "LaunchTemplateSpecification": {
          "LaunchTemplateName": "ghost-lt",
          "Version":  "1"
        },
        "Overrides": [
          { "InstanceType": "t2.micro" },
          { "InstanceType": "t2.small" },
          { "InstanceType": "t3.micro" },
          { "InstanceType": "t3.small" }
        ]
      },
      "InstancesDistribution": {
        "OnDemandBaseCapacity": 1,
        "OnDemandPercentageAboveBaseCapacity": 50,
        "SpotInstancePools": 2
      }
    },
    "MinSize": 1,
    "MaxSize": 5,
    "DesiredCapacity": 2,
    "VPCZoneIdentifier": "",
    "Tags": [{
      "Key": "Project",
      "Value": "cloud_101"
    }]
  }
  ```
11. Actualizamos el valor de `VPCZoneIdentifier` utilizando `jq`.
  ```bash
  cat auto_scaling_group_input.json \
    | jq ".VPCZoneIdentifier = \"$PRIVATE_SUBNETS\"" \
    > .tmp && mv .tmp auto_scaling_group_input.json
  ```
12. Levantamos el `Auto Scaling Group` de acuerdo a nuestra configuración.
```bash
aws autoscaling create-auto-scaling-group \
  --cli-input-json file://auto_scaling_group_input.json
```

### FAQ

**¿Cual es la diferencia entre `min`, `max`, y `desired` capacity?**

Las tres son utilizadas para determinar la cantidad de instancias que el `Auto Scaling Group` va a crear por nosotros. `min` y `max` son simples de explicar; corresponden a los límites de instancias que se podrán crear o terminar. `desired` es la cantidad de instancias que el `Auto Scaling Group` debe intentar mantener. Una vez fijado por el administrador, este valor puede variar entre `min` y `max` de acuerdo a las politicas definidas.

**¿Porque tengo que crear un `Launch Template` para crear un `Auto Scaling Group`?**

Es una forma efectiva de garantizar que todas las instancias que levante al `Auto Scaling Group` se realicen de la misma manera. Por otro lado, uno puede necesitar de múltiples `Auto Scaling Groups` que sean lanzadas de formas similares.

---

Si vamos a la consola de instancias de EC2, veremos las instancias creadas por nuestro `Auto Scaling Group`, corriendo nuestra aplicación. Veamos que sucede si terminamos una instancia. Si no recuerda como hacerle, refierase a la guía de `04_ec2.md`.

Cuando el `Auto Scaling Group` detecta la caída de una instancia, inmediatemente comienza el procedimiento para volverla a levantar. Si ya no necestiamos el `Auto Scaling Group` podemos eliminarlo. 

> ❗❗️❗️<br/>Todas las instancias creadas por el `Auto Scaling Group` serán eliminadas junto con el.<br/>❗❗️❗️

---

## 💻 DEMO #21 ~ Eliminar un `Auto Scaling Group` y un `Launch Template` <a name="demo020"></a>

Mostraremos como realizar este procedimiento desde la consola web.

### Procedimiento para eliminar `Auto Scaling Group` (`web`)

1. Acceder al dashboard de EC2.
2. Hacer click en `Auto Scaling Group`.
3. Seleccionar el `Auto Scaling Group` deseado.
4. Hacer click en `Actions > Delete`.
5. Hacer click en `Close`.

### Procedimiento para eliminar `Launch Template` (`web`)

1. Acceder al dashboard de EC2.
2. Hacer click en `Launch Templates`.
3. Seleccionar el `Launch Template` deseado.
4. Hacer click en `Actions > Delete launch template`.
5. Hacer click en `Close`.

---

Los `Auto Scaling Group` son excelentes para mantener la disponibilidad de nuestras aplicaciones, pero todavía no tenemos una forma de balancear el tráfico sobre ellos. Por otro lado, los pasos necesarios para levantar esta infraestructura se están volviendo cada vez más complejos. Por más que podemos generar `scripts` que nos ayuden a levantar la infraestructura, es dificil mantenerlos actualizados y libres de `bugs`. Tampoco tenemos níngun tipo de documentación respecto a nuestra infra. Cualquier cambio adicional empeorara la situación. Necesitamos otra forma de levantar nuestros servicios.

Vamos a ver como podemos solucionar la creación de un balanceador y documentar nuestro sistema con `CloudFormation`. 