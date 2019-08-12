# Application Load Balancers

Elastic Load Balancing admite tres tipos de balanceadores de carga: Application Load Balancers, Network Load Balancers y Classic Load Balancers. Nosotros nos concentraremos solo en los "Application Load Balancers".

Un balanceador de carga actúa como único punto de contacto para los clientes. El balanceador de carga distribuye el tráfico entrante de aplicaciones entre varios destinos, tales como instancias EC2, en varias zonas de disponibilidad. Esto aumenta la disponibilidad de la aplicación. Puede agregar uno o varios `Listeners` al balanceador de carga.

Un `Listener` comprueba las solicitudes de conexión de los clientes mediante el protocolo y el puerto que haya configurado; luego, reenvía las solicitudes a uno o más `Target Groups`, según las `Rules` que haya definido. Cada `Rule` especifica un `Target Group`, una condición y una prioridad. Cuando se cumple la condición, el tráfico se reenvía al `Target Group`. Debe definir una `Rule` predeterminada para cada `Listener` y agregar reglas que especifiquen diferentes `Target Groups` en función del contenido de la solicitud.

![Load Balancer](https://docs.aws.amazon.com/es_es/elasticloadbalancing/latest/application/images/component_architecture.png)

## Información General

Un `ALB` actúa como la capa de aplicación, es decir, la séptima capa del modelo de interconexión de sistemas abiertos (OSI). Una vez que el `ALB` ha recibido una solicitud, evalúa las `Rules` del `Listener` por orden de prioridad con el fin de determinar qué `Rule` se debe aplicar. Luego, selecciona un destino en el `Target Group` para la acción de la `Rule`. Puede configurar las `Rules` del `Listener` de tal forma que las solicitudes se direccionen a diferentes `Target Groups` en función del contenido del tráfico de aplicación. El direccionamiento se lleva a cabo de manera independiente para cada `Target Group`, aunque un destino se haya registrado en varios `Target Groups`.

Puede agregar y eliminar destinos del `ALB` en función de sus necesidades sin interrumpir el flujo general de solicitudes a la aplicación. Elastic Load Balancing escala el `ALB` a medida que cambia el tráfico dirigido a la aplicación y es capaz de adaptarse automáticamente a la mayoría de cargas de trabajo. Elastic Load Balancing puede escalarse automáticamente para adaptarse a la mayoría de las cargas de trabajo.

Puede configurar los `Health Checks`, que se utilizan para monitorizar el estado de los destinos registrados, de tal forma que el `ALB` solo pueda enviar solicitudes a los destinos en buen estado.

---

## 💻 DEMO #24 ~ Crear un `ALB` con `CloudFormation` <a name="demo020"></a>

Vamos a realizar estas tareas desde la `cli`.

### Procedimiento (`cli`)

1. Creamos el template `alb_template.yaml` con el siguiente contenido:
  ```yaml
  AWSTemplateFormatVersion: '2010-09-09'
  Description: Application Load Balancer
  Parameters:
    PrivateSubnet0:
      Description: Public Subnet 0
      Type: String
    PrivateSubnet1:
      Description: Public Subnet 1
      Type: String
    InstancesSecurityGroup:
      Description: Instance Security Group
      Type: String
  Resources:
    LoadBalancer:
      Type: 'AWS::ElasticLoadBalancingV2::LoadBalancer'
      Properties:
        IpAddressType: ipv4
        Name: ApplicationLoadBalancer
        Scheme: internet-facing
        SecurityGroups:
          - !Ref InstancesSecurityGroup
        Subnets:
          - !Ref PrivateSubnet0
          - !Ref PrivateSubnet1
        Type: application
  ```
2. Obtenemos los valores de los parámetros que necesitamos
  ```bash
  # Obtenemos el ID de nuestro VPC
  aws ec2 describe-vpcs \
    --query 'Vpcs[*].{Id:VpcId,Tags:Tags}' \
    --output json
  export VPC_ID=
  # Obtenemos el ID de nuestras redes privadas
  aws ec2 describe-subnets \
    --filters Name=vpc-id,Values=$VPC_ID \
    --query 'Subnets[*].{Name:Tags[0].Value, Id:SubnetId}'
  export SUBNET0_ID=
  export SUBNET1_ID=
  # Obtenemos el ID de nuestro Security Group
  aws ec2 describe-security-groups \
    --filters Name=vpc-id,Values=$VPC_ID \
    --query 'SecurityGroups[*].{Name:GroupName, ID:GroupId}'
  # Cargamos la variable `SG_ID` con nuestro Security Group
  export SG_ID=
  ```
3. Creamos el `stack` utilizando nuestro `template`
  ```bash
  aws cloudformation create-stack \
    --stack-name cloud-101-alb \
    --template-body file://alb_template.yaml \
    --parameters \
      ParameterKey=PrivateSubnet0,ParameterValue=$SUBNET0_ID \
      ParameterKey=PrivateSubnet1,ParameterValue=$SUBNET1_ID \
      ParameterKey=InstancesSecurityGroup,ParameterValue=$SG_ID
  ```
4. Podemos ver el estado de nuestro `stack` con el siguiente comando
  ```bash
  watch aws cloudformation describe-stack-events --stack-name cloud-101-alb --output json
  ```

---

El balanceador de carga en si mismo no nos aporta nada. Tenemos que conectarlo a nuestras instancias para que sirva nuestro contenido. Este proceso involucra la creación de los siguientes recursos:

1. `Listener`: Configura el puerto, el protocolo, y el objetivo.
2. `ListenerRule`: Reglas que indican como distribuir el tráfico HTTP.
3. `TargetGroup`: Definen el conjunto de recursos que recibirán las consultas. También definen los chequeos de salud necesarios para identificar las instancias con errores.

---

## 💻 DEMO #25 ~ Agregamos nuevos recursos al template de `CloudFormation` <a name="demo025"></a>

En vez de crear un nuevo `template`, vamos a extender el que ya tenemos. Luego vamos a crear un `Change Set`, y por último, aplicaremos los cambios. 

Vamos a realizar estas tareas desde la `cli`.

### Procedimiento (`cli`)

1. Editamos el archivo `alb_template.yaml` para que quede de la siguiente manera:

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: Application Load Balancer
Parameters:
  PrivateSubnet0:
    Description: Public Subnet 0
    Type: String
  PrivateSubnet1:
    Description: Public Subnet 1
    Type: String
  InstancesSecurityGroup:
    Description: Instance Security Group
    Type: String
  VPC:
    Description: VPC ID del proyecto
    Type: String
Resources:
  LoadBalancer:
    Type: 'AWS::ElasticLoadBalancingV2::LoadBalancer'
    Properties:
      IpAddressType: ipv4
      Name: ApplicationLoadBalancer
      Scheme: internet-facing
      SecurityGroups:
        - !Ref InstancesSecurityGroup
      Subnets:
        - !Ref PrivateSubnet0
        - !Ref PrivateSubnet1
      Type: application

  Listener:
    Type: AWS::ElasticLoadBalancingV2::Listener
    Properties:
      DefaultActions:
        - TargetGroupArn: !Ref TargetGroup
          Type: forward
      LoadBalancerArn: !Ref LoadBalancer
      Port: 80
      Protocol: HTTP

  ListenerRule:
    Type: AWS::ElasticLoadBalancingV2::ListenerRule
    Properties:
      Actions:
        - TargetGroupArn: !Ref TargetGroup
          Type: forward
      Conditions:
        - Field: path-pattern
          Values: 
            - '/*'
      ListenerArn: !Ref Listener
      Priority: 1

  TargetGroup:
    Type: AWS::ElasticLoadBalancingV2::TargetGroup
    Properties:
      HealthCheckIntervalSeconds: 30
      HealthCheckProtocol: HTTP
      HealthCheckPath: /
      HealthCheckTimeoutSeconds: 10
      HealthyThresholdCount: 4
      Matcher:
        HttpCode: 200
      Name: !Sub 'cloud-101-tg'
      Port: 8080
      Protocol: HTTP
      VpcId: !Ref VPC
```
2. Obtenemos los valores de los parámetros que necesitamos
  ```bash
  # Obtenemos el ID de nuestro VPC
  aws ec2 describe-vpcs \
    --query 'Vpcs[*].{Id:VpcId,Tags:Tags}' \
    --output json
  export VPC_ID=
  # Obtenemos el ID de nuestras redes privadas
  aws ec2 describe-subnets \
    --filters Name=vpc-id,Values=$VPC_ID \
    --query 'Subnets[*].{Name:Tags[0].Value, Id:SubnetId}'
  export SUBNET0_ID=
  export SUBNET1_ID=
  # Obtenemos el ID de nuestro Security Group
  aws ec2 describe-security-groups \
    --filters Name=vpc-id,Values=$VPC_ID \
    --query 'SecurityGroups[*].{Name:GroupName, ID:GroupId}'
  # Cargamos la variable `SG_ID` con nuestro Security Group
  export SG_ID=
  ---
3. Creamos un `Change Set` utilizando nuestro `template` editado
  ```bash
  aws cloudformation create-change-set \
    --change-set-name cloud-101-alb-change-set \
    --stack-name cloud-101-alb \
    --template-body file://alb_template.yaml \
    --parameters \
      ParameterKey=PrivateSubnet0,ParameterValue=$SUBNET0_ID \
      ParameterKey=PrivateSubnet1,ParameterValue=$SUBNET1_ID \
      ParameterKey=InstancesSecurityGroup,ParameterValue=$SG_ID \
      ParameterKey=VPC,ParameterValue=$VPC_ID
  ```
4. Analizamos los cambios a realizar en el `Change Set`.
  ```bash
  aws cloudformation describe-change-set \
    --change-set-name cloud-101-alb-change-set \
    --stack-name cloud-101-alb \
    --output json \
    | jq
  ```
5. Aplicamos los cambios
  ```bash
  aws cloudformation update-stack \
    --stack-name cloud-101-alb \
    --template-body file://alb_template.yaml \
    --parameters \
      ParameterKey=PrivateSubnet0,ParameterValue=$SUBNET0_ID \
      ParameterKey=PrivateSubnet1,ParameterValue=$SUBNET1_ID \
      ParameterKey=InstancesSecurityGroup,ParameterValue=$SG_ID \
      ParameterKey=VPC,ParameterValue=$VPC_ID \
    | watch -n 1 'aws cloudformation describe-stack-events --stack-name cloud-101-alb --output json'
  ```

---

Una vez que el `stack` termine de actualizar, contaremos con todos los recursos necesarios. Lo único que falta es conectar nuestro `Auto Scaling Group` a nuesto `ALB`. Esto es porque ambos recursos los creamos a través de distintos metodos, y la conexión entre ambos se realiza de forma indirecta utilizando nuestro `Target Group`. Los pasos a realizar son los siguientes:

---

## 💻 DEMO #26 ~ Conectamos los recursos creadso con `CloudFormation` con los recursos existentes <a name="demo025"></a>

Vamos a realizar estas tareas desde la consola `web`.

### Procedimiento (`cli`)

1. Vamos a la consola de `EC2`.
2. Hacemos click en `Auto Scaling Groups`.
3. Seleccionamos nuestro grupo.
4. Hacemos click en `Actions`.
5. Hacemos click en `Edit`.
6. Bajamos hasta encontrar el camop `Target Groups`. Seleccionamos el `Target Group` creado con `CloudFormation`.
7. Hacemos click en `Save`.

---

Para acceder a nuestro sistema tenemos que obtener la dirección DNS por la cual AWS esta sirviendo nuestra aplicación. Podemos encontrar este valor en la página principal de nuesto `ALB`.