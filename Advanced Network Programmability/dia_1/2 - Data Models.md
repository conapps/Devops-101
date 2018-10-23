## Data models

Los modelos de datos describen un set de datos con restricciones en la forma de un leguaje para "schemas".

![alt data_models](/home/ialmandos/Dropbox/CodeProjects/network_programmability/imagenes/data_models.png)

Originalmente los Nexus 7000 usaban xsd en lugar de Yang modules, no se si lo siguen haciendo.



EXPLICAR LA DIFERENCIA ENTRE LOS DATOS, EL MODELADO DE LOS DATOS, EL FORMATO ELEGIDO PARA TRANSMITIR LA INFORMACION Y EL PROTOCOLO UTILIZADO PARA HACERLO.

### YANG - 2010 - RFC 6020

Definido en la RFC 6020, originalmente diseñado para NETCONF (esto quiere decir que fue inicialmente diseñado para modelar equipos de networking). Ahora también lo utiliza RESTCONF. Sirve para modelar configuración e información de estado. Provee sintáxis y semántica. Utiliza estructuras de datos re-utilizables.



Tipos de YANG modules:

- Industry strandard
- Cisco common
- Cisco platform specific

[Openconfig](http://www.openconfig.net/) es una asociación que está desarrollando modelos de datos agnósticos a los fabricantes. Según su propia descripción.

> ### What is OpenConfig?
>
> OpenConfig is an informal working group of network operators sharing the goal of moving our networks toward a more dynamic, programmable infrastructure by adopting software-defined networking principles such as declarative configuration and model-driven management and operations.
>
> Our initial focus in OpenConfig is on compiling a consistent set of vendor-neutral data models (written in YANG) based on actual operational needs from use cases and requirements from multiple network operators.



## Yang sintax



## Yang tools

### Yang validator

www.yangvalidator.com

Se sube el modelo de Yang y la yangvalidator valida la sintaxis. Además se muestra el modelo en un formato entendible para humanos.

Hasta donde pude ver sirve para validar modelo estándar, no de vendors.

Por detrás esta herramienta utiliza Pyang

### pyang

Options:

-f: format - acá utilizamos habitualmente `tree` . Otras opciones incluyen `sample-xml-skeleton` esto sirve para ver la representación XML de un modelo. Este output es lo que tenemos que mandar si estamos usando Netconf. Otra opción es `jstree`, esta genera un archivo html que nos permite navegar a estructura de los modelos. Un ejemplo de como se ejecutaría sería:

```bash
pyang -f jstree -p /path/archivo.yang > output.html
```

-p: path al modelo - acá va el path al archivo.yang



### ydk

### Yang explorer

https://github.com/CiscoDevNet/yang-explorer

Es una herramienta gráfica para navegar modelos de Yang y que permite además generar requests, tanto para Netconf como para Restconf.



> Nota: no está soportado en Windows.

