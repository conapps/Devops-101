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

## 💻 DEMO #1 ~ Crear un `ALB` con `CloudFormation` <a name="demo020"></a>

Vamos a realizar estas tareas desde la `web`.

### Procedimiento (`web`)

1. Acceder al dashboard de EC2.
2. Hacer click en `Load Balancers`.
3. Hacer click en `Create Load Balancer`.
4. Dentro de la sección `Application Load Balancer` hacer click en `Create`.
5. Asignar un nombre al `ALB`.
6. Seleccionarlo como `internet-facing`.
7. ❗️Seleccionar `HTTP` como protocolo y el puerto `80`.
8. ❗️Seleccionar la `VPC` donde se encuentran las instancias del `Auto Scaling Group`.
9. ❗️Seleccionar al menos tres zonas de disponibilidad y las redes públicas de cada una de ellas.
10. Hacer click en `Next: Configure Security Groups`. Si se le presenta un cartel de advertencia, omitalo haciendo click nuevamente en el boton `Next: Configure Security Groups`.
11. Seleccionar el `Security Group` creado previamente. El mismo debe permitir el tráfico entrante al puerto 80.
12. Hacer click en `Next: Configure Routing`.
13. Seleccionar `New Target Group` en la opción `Target Group`.
14. Asignele un nombre al `Target Group`.
15. Configure `HTTP` como protocolo y `8080` como puerto.
16. En la sección de `Health checks` configure `HTTP` como protocolo y `8080` como puerto.
17. Haga click en `Next: Register Targets`.
18. Haga click en `Next: Review`.
19. Haga click en `Create`.
20. Haga click en `Close`.

### ❗️Atención

En producción se recomienda utilizar HTTPS como protocolo para públicar nuestras aplicaciones en el puerto 443. El `ALB` se puede encargar de terminar el tráfico `HTTPS` por nuesto motor de aplicaciones. Se pueden utilizar certificados externos, o generados por el servicio de certificados de AWS.

Es importante que tenga precaución al momento de realizar la configuración del `ALB` con el `VPC`. Debe seleccionar el `VPC` donde se encuentran las instancias con nuestra aplicación, y las `Subnets` publicas. Si selecciona las `Subnet` privadas, el balanceador no podrá recibir tráfico de Internet.

### FAQ

**¿Que diferencia hay entre los distintos tipos de balanceadores?**

En [esta página](https://aws.amazon.com/elasticloadbalancing/features/#compare) se pueden ver todas las diferencias entre ellos.

**¿Que pasa si no configuro el puerto 8080 en el `Target Group`?**

Si esta mal configurado este puerto el `ALB` enviara los requests a un puerto incorrecto y la aplicación no funcionara. Además, los chequeos de salud no funcionarán, por lo que las instancias activas serán eliminadas del `Auto Scaling Group`.

---

Durante el proceso anterior generamos los siguientes recursos, además del `ALB`:

1. `Listener`: Configura el puerto, el protocolo, y el objetivo.
2. `ListenerRule`: Reglas que indican como distribuir el tráfico HTTP.
3. `TargetGroup`: Definen el conjunto de recursos que recibirán las consultas. También definen los chequeos de salud necesarios para identificar las instancias con errores.

Lo único que nos resta hacer es configurar nuestro `Auto Scaling Group` a nuesto balanceador.

---

## 💻 DEMO #2 ~ Configuración del Auto Scaling Group <a name="demo025"></a>

Vamos a configurar nuestro `Auto Scaling Group` para que registre las instancias en el `Target Group` de nuestro `ALB`. De esta manera, cada modificación en las instancias administradas por el `Auto Scaling Group` será reflejada en los `Targets` a los que les enviara los mensajes el `ALB`.

### Procedimiento (`web`)

1. Vamos a la consola de `EC2`.
2. Hacemos click en `Auto Scaling Groups`.
3. Seleccionamos nuestro grupo.
4. Hacemos click en `Actions`.
5. Hacemos click en `Edit`.
6. Bajamos hasta encontrar el camop `Target Groups`. Seleccionamos el `Target Group` en la demo anterior.
7. Hacemos click en `Save`.

---

Para acceder a nuestro sistema tenemos que obtener la dirección DNS por la cual AWS esta sirviendo nuestra aplicación. Podemos encontrar este valor en la página principal de nuesto `ALB`.

---
<div style="width: 100%">
  <div style="float: left"><a href="../guias/13_auto_scaling_groups.md">⬅️13 - Auto Scaling Groups</a></div>
  <div style="float: right"><a href="../guias/15_desafio_final.md">15 - Desafío Final ➡️</a></div>
</div>