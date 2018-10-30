# Modelos de datos

## Introducción

Los modelos de datos son una forma de modelar la información disponible en los dispositivos. A modo de ejemplo, se puede modelar la información de estado de una interface especificando una entidad llamada "interface-state", este proceso de modelado especifíca que datos podemos obtener y en que unidades a partir de dicha entidad. De esta forma, se podría definir que la entidad "interface-state" tendrá los siguientes campos:

**"interface-state"**

- "name" (que se almacenará como un string)
- "state" (que se almacenará como un booleano)
- "ifIncounter" (que se almacanará como un entero)
- "ifOutcounter" (que se almacanará como un entero)

A este proceso se le llama modelar los datos. En el ejemplo anterior, el modelado de los datos se expresó en el texto a través de viñetas, hecho que obviamente no es de ninguna utilidad en la realidad.

Para poder describir los modelos de datos (que no son mas que abstracciones conceptuales) de forma práctica y escalable existen distintos lenguajes de modelado.  `JSD` y `XSD` son ejemplos de este tipo de lenguajes. Para el caso del equipamiento de comunicaciones, la IETF definió, a través de la RFC 6020, un lenguaje de modelado diseñado específicamente para contemplar las particularidades que surgen al intentar modelar la información en este tipo de equipamiento. Este lenguaje, llamado YANG (Yet Another Next Generation), es lo que se ha establecido en la industria como el estándar de facto.

La figura a continuación muestra, de izquierda a derecha, como ha sido la evolución a lo largo del tiempo hasta llegar a lo que hoy definimos como "model driven programmability"



![alt data_models](imagenes/data_models.png)

> Nota: Originalmente, los Nexus 7000 usaban xsd en lugar de Yang

El objetivo último detrás del paradigma "model driven programmability" es poder generar abstracciones conceptuales (modelos de datos) que apliquen a todos los dispositivos del mismo tipo, un router por ejemplo, sin importar cual sea su fabricante.

Hoy en día existe una entidad que trabaja en pos de lograr este objetivo. 
[Openconfig](http://www.openconfig.net/) es una asociación que está desarrollando modelos de datos agnósticos a los fabricantes. Según su propia descripción.

> ### What is OpenConfig?
>
> OpenConfig is an informal working group of network operators sharing the goal of moving our networks toward a more dynamic, programmable infrastructure by adopting software-defined networking principles such as declarative configuration and model-driven management and operations.
>
> Our initial focus in OpenConfig is on compiling a consistent set of vendor-neutral data models (written in YANG) based on actual operational needs from use cases and requirements from multiple network operators.

Algunos de los principales contribuyentes a Openconfig son:

- Alibaba
- Apple
- AT&T
- British Telecom
- Deutsche Telekom
- Facebook
- Google
- Microsoft
- Oracle
- Telefónica
- Yahoo!

## YANG - 2010 - RFC 6020

Definido en la RFC 6020, originalmente diseñado para NETCONF (esto quiere decir que fue inicialmente diseñado para modelar equipos de networking). Ahora también lo utiliza RESTCONF. 
Como se comentó anteriormente, sirve para modelar configuración e información de estado. Provee sintáxis y semántica. Utiliza estructuras de datos re-utilizables.

Tipos de YANG modules en dispositivos Cisco:

- Industry strandard
- Cisco common
- Cisco platform specific

Una lista muy amplia de modelos de datos escritos en YANG, tanto de organizaciones como IETF o IEEE así como de vendors como Cisco, Huawei o Juniper pueden encontrarse en Github en el siguiente repositorio:

`https://github.com/YangModels/yang`

### Sintáxis de YANG

Para comenzar, veámos YANG en acción con un ejemplo sencillo. En este ejemplo vamos a modelar a la población de Uruguay. Lo que generaremos en nuestro modelo es una lista de personas con una serie de atributos que las definen. En este ejemplo, los atributos serán el nombre, la edad y de que equipo de fútbol es hincha la persona.

```yang
// module name
module personas-uruguay {

    yang-version "1";
    namespace "https://conatel.cloud/personas-uruguay";

    prefix "personas-uruguay";

    identity EQUIPO {
        description "De que equipo es hincha";
    }

    identity NACIONAL {
        base EQUIPO;
        description "Hincha de Nacional";
    }

    identity PENAROL {
        base EQUIPO;
        description "Hincha de Penarol";
    }

    // nuevo tipo de datos
    typedef edad {
        type uint16 {
            range 1..100;
        }
    }

    // este agrupamiento de datos contiene todos los datos de una persona
    grouping datos-personales {
        leaf nombre {
            type string;
        }
        leaf edad {
            type edad;
        }
        leaf EQUIPO {
            type identityref {
                base personas-uruguay:EQUIPO;
            }
        }
    }

    // objeto raiz definido en el modelo
    container poblacion {
        list persona {
            // identificador unico de cada individuo
            key "nombre";

            // los datos correspondientes a cada individuo seran los definidos en el grouping datos-personales
            uses datos-personales;
        }
    }
}
```

Como se puede ver, cuando modelamos utilizando YANG lo hacemos a través de módulos, por lo que, en este caso,  la población de Uruguay será un módulo definido mediente la sentencia `module <nombre-del-modulo>`.

Una de las potencias del lenguaje es que permite definir tipos de datos arbitrarios, esto se hace a través de la sentencia `typedef`, en este caso definimos un tipo de datos llamado `edad` a la que restringimos a tomar valores de entre 0 y 100. Si bien esto es algo bastante simple, el lenguaje permite definir estructuras arbitrarias, tan complejas como se quiera. Por ejemplo se puede definir un tipo de datos que restrinja sus posibles valores a direcciones IP válidas.

Utilizando los distintos tipos de datos, ya sea nativos del lenguaje o definidos por el usuario, se pueden armar agrupaciones lógicas utilizando la sentencia `grouping`. En el ejemplo, se definió un `grouping` llamado `datos-personales` que contiene la información de `edad`, `nombre` y `EQUIPO`.

Hasta ahora hemos definido tipos de datos y agrupaciones de campos de información con sus respectivos tipos de datos (groupings), ahora avanzaremos con el modelado de la población. Para hacer esto, YANG dispone de la sentencia `container`  dentro de la cual, en el ejemplo definimos que habrá una lista de personas a la que llamamos `persona`. Cada elemento de esta lista será una persona, representada por sus datos personales, con la particularidad de que no podrá haber personas repetidas dentro de dicha lista. Se consideran como repetidas a todas aquellas personas con el mismo nombre. Esto se logra mediante la definición de un identificador único a través de la sentencia `key` , que en este caso define al `nombre` como dicho identificador.

### Yang tools

#### Yang validator

www.yangvalidator.com

Se sube el modelo de Yang y la página yangvalidator valida la sintaxis. Además se muestra el modelo en un formato entendible para humanos.

>  Nota: la herramienta no valida correctamente algunos modelos de vendors, si funciona correctamente con modelos estándar.

Por detrás se utiliza Pyang.

#### pyang

Una de las principales utilidades de modelar la información, es que los desarrolladores podemos conocer de antemano la estructura de los datos y por tanto escribir código que los procese con facilidad. Si bien YANG es un lenguaje muy potente para realizar el modelado, la realidad es que no es nada sencillo de leer cuando nuestro objetivo es, de un vistazo, entender la estructura con la que tendrá que trabajar nuestro código. Para ello, en Python existe una herramienta muy útil llamada `pyang`. 

`pyang` permite partir de uno o varios módulos de YANG y generar una representación del modelo de datos en forma de árbol que es muy sencilla de leer.

A continuación podemos ver como con `pyang` generamos una visualización en formato de árbol (`-f tree`) del modelo de datos `personas-uruguay.yang`

```bash
$ pyang -f tree personas-uruguay.yang
module: personas-uruguay
  +--rw poblacion
     +--rw persona* [nombre]
        +--rw nombre    string
        +--rw edad?     edad
        +--rw EQUIPO?   identityref
```

Allí podemos ver rápidamente como los campos dependen jerárquicamente unos de otros y cuales son de lectura y/o escritura.

### Ejercicio 5

Buscar dentro del repositorio `https://github.com/YangModels/yang/tree/master/vendor/cisco/xe/1681` el modelo `ietf-interfaces.yang` . Descargarlo y analizar su estructura utilizando `pyang`

<details>

<summary>Solucion</summary>

<code>

```bash
$ pyang -f tree ietf-interfaces.yang 
module: ietf-interfaces
  +--rw interfaces
  |  +--rw interface* [name]
  |     +--rw name                        string
  |     +--rw description?                string
  |     +--rw type                        identityref
  |     +--rw enabled?                    boolean
  |     +--rw link-up-down-trap-enable?   enumeration {if-mib}?
  +--ro interfaces-state
     +--ro interface* [name]
        +--ro name               string
        +--ro type               identityref
        +--ro admin-status       enumeration {if-mib}?
        +--ro oper-status        enumeration
        +--ro last-change?       yang:date-and-time
        +--ro if-index           int32 {if-mib}?
        +--ro phys-address?      yang:phys-address
        +--ro higher-layer-if*   interface-state-ref
        +--ro lower-layer-if*    interface-state-ref
        +--ro speed?             yang:gauge64
        +--ro statistics
           +--ro discontinuity-time    yang:date-and-time
           +--ro in-octets?            yang:counter64
           +--ro in-unicast-pkts?      yang:counter64
           +--ro in-broadcast-pkts?    yang:counter64
           +--ro in-multicast-pkts?    yang:counter64
           +--ro in-discards?          yang:counter32
           +--ro in-errors?            yang:counter32
           +--ro in-unknown-protos?    yang:counter32
           +--ro out-octets?           yang:counter64
           +--ro out-unicast-pkts?     yang:counter64
           +--ro out-broadcast-pkts?   yang:counter64
           +--ro out-multicast-pkts?   yang:counter64
           +--ro out-discards?         yang:counter32
           +--ro out-errors?           yang:counter32
```

</code>

</details>

### Como extender los modelos

Una posibiliad que ofrece YANG es la de extender los modelos de datos para agregar información o funcionalidades que no estaban previstas en el modelo original. Una particularidad de como funciona este proceso con YANG es que no es necesario modificar (ni ser el autor) del módulo original para poder extenderlo. Dicho en otras palabras, no es necesario hacer un "fork" de un módulo para para poder extenderlo. Esto nos permite partir de un módulo de un tercero, aumentarlo, y si en un futuro el tercero realiza una actualización del mismo poder seguir adelante de forma transparente.

Veremos a continuación como podemos extender el modelo anterior `personas-uruguay.yang` para agregar información adicional mismo. Mas específicamente, agregaremos la posibilidad de ser hincha del Barcelona así como información sobre la situación laboral de la persona.

``` yang
module personas-uruguay-extended {

    yang-version "1";
    namespace "https://conatel.cloud/personas-uruguay-extended";

    prefix "personas-uruguay-extended";

    // Importamos el modelo anterior
    import personas-uruguay { prefix personas-uruguay; }

    // Nuevo equipo de futbol
    identity BARCELONA {
        base personas-uruguay:EQUIPO;
        description "Para los hijos de la globalizacion";
    }

    // Este grouping contiene nueva informacion para extender el modelo anterior
    grouping datos-personales-extendidos {
        leaf ocupacion {
            type enumeration {
                enum ACTIVO {
                    description "Activo en el mercado laboral";
                }
                enum DESOCUPADO {
                    description "En búsqueda activa de una ocupacion";
                }
                enum RETIRADO {
                    description "Retirado del mercado laboral";
                }

            }
        }
    }

    // Aqui es donde especificamos que parte del modelo anterior queremos extender
    augment "/personas-uruguay:poblacion/personas-uruguay:persona" {
        uses datos-personales-extendidos;
    }
}
```

Como puede verse en el snippet anterior, utilizamos la expesión `ìdentity` tomando como base a `personas-uruguay:EQUIPO`

Por otro lado, generamos un nuevo `grouping` llamado `datos-personales-extendidos` donde, utilizando el tipo de datos nativo de YANG `enumeration`, definimos la posibilidad de que la perona esté en estado laboral `ACTIVO`,  `DESOCUPADO` o `RETIRADO`

Finalmente, utilizamos el nuevo módulo para extender el módulo anterior indicando exactamente donde debe ubicarse el primero dentro del último. Esto lo definimos mediante la sentencia:

``` yang
augment "/personas-uruguay:poblacion/personas-uruguay:persona" {
        uses datos-personales-extendidos;
}
```

Podemos visualizar el modelo extendido mediante Pyang de la siguiente manera:

``` bash
$ pyang -f tree personas-uruguay.yang personas-uruguay-extended.yang 
module: personas-uruguay
  +--rw poblacion
     +--rw persona* [nombre]
        +--rw nombre                                 string
        +--rw edad?                                  edad
        +--rw EQUIPO?                                identityref
        +--rw personas-uruguay-extended:ocupacion?   enumeration
```

### Ejercicio 6

En este ejercicio vamos a explorar como utilizar `pyang` para generar una página Web con la documentación del modelo.

Para hacerlo, podemos encontrar los modelos presentados en el ejemplo anterior en la carpeta `dia_1/data_models`. 

La sintáxis para generar un archivo `html` con la documentación de los modelos es la siguiente:

``` bash
$ pyang -f jstree <modelo-1.yang> --- <modelo-N.yang> -o <nombre-del-archivo.html>
```

Generar un archivo HTML con la documentación del modelo extendido `personas-uruguay-extended.yang`

<details>

<summary>Solucion</summary>

<code>

`[link](https://s3.amazonaws.com/adv-network-programmability/personas-uruguay.html)`

</code>

</details>









