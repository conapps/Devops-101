# Netconf - 2006 - RFC 4741 (updated in 2011)

Netconf es un protocolo IETF pensado como una evolución de SNMP. Usa ssh, SOAP, o TLS como transporte. En este curso utilizaremos únicamente ssh.

La arquitectura es cliente-servidor, donde el router es el servidor y la notebook (o sistema de gestión) es el cliente.

**A diferencia de REST (que es stateless), Netconf es basado en transacciones.**

Las configuraciones de los equipos se guardan en "datastores".
NetConf prevee que los equipos puedan soportar tres tipos de datastore:

- candidate
- running
- startup

No obstante, el único data-store mandatorio es el de la running-config. Los equipos Cisco típicamente soportan `running-config` y `startup-config`  en todos los modelos y la `candidate-config` en algunos modelos selectos como los que corren IOS-XR.

Cuando un cliente establece una conexión con un servidor, este le responde enviando sus "capabilites". En el contexto de este curso las "capabilites" se corresponden a modelos de YANG, aunque esto no necesariamente tiene que ser así; de hecho antes de existir YANG, los routers modelaban sus estructuras de datos con XSD y utilizaban Netconf como transporte. Acto seguido el cliente debe respoder con sus propias "capabilites"; una vez hecho esto está listo para enviar peticiones al servidor. En Netconf las peticiones son conocidas como "Remote  Procedure Call (RPC)" . El diagrama a continuación muestra este procedimiento de forma resumida.



![alt netconf handshake](imagenes/netconf_handshake.png)



Si analizamos Netconf mas en profundidad podremos ver que dentro de los mensajes RPCs se envían operaciones, un concepto muy similar a los métodos de HTTP y finalmente dentro de las operaciones se envian los datos, (en caso de que corresponda). Tanto los mensajes, como los métodos que van dentro de estos, como los datos que van dentro de los propios métodos, se codifican utilizando XML. La figura a continuación resume esto último de forma gráfica.



![alt netconf overview](imagenes/para_agregar_2.png)



Dado que Netconf es orientado a transacciones, cada mensaje RPC tiene un identificador único que identifica a la transacción. De esta forma, el cliente, o Manager figura en la imágen a continuación, puede distinguir a que RPC corresponde una respuesta determinada.



![alt rpc](imagenes/para_agregar_3.png)



Cómo se mencionó anteriormente, de forma muy similar a como lo hace HTTP con sus métodos, Netconf define una serie de operaciones que le indican al servidor la naturaleza del pedido realizado. La lista a continuación muestra algunas de las operaciones existentes y su significado.



![alt netconf actions](imagenes/netconf_actions.png)



Dado que Netconf utiliza ssh como transporte, en teoría podríamos realizar cualquier operación únicamente con una consola (aunque obviamente no sería demasiado práctico). De cualquier forma, como una primera aproximación al protocolo, veremos como funciona el intercambio de capabilites de esta manera para introducir luego una metodología mas práctica de acceso. 

Antes de poder trabajar con NetConf es necesaro habilitar dicha funcionalidad en los equipos.
Para ello, el procedimiento es el siguiente:



## Ejercicio 7

Ejectuar el siguiente comando para conectarnos al router:

```bash
$ ssh -i cert.pem -p 830 usuario@hostname 
```

Una vez conecados deberíamos poder ver el mensaje de `<hello>` del router donde comunica sus capabilites. El mensaje debería ser algo parecido al siguiente:

```bash
<?xml version="1.0" encoding="ISO-8859-1"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:xml:ns:netconf:base:1.0</capability>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
    <capability>urn:ietf:params:netconf:capability:validate:1.0</capability>
    <capability>urn:ietf:params:netconf:capability:writable-running:1.0</capability>
    <capability>urn:ietf:params:netconf:capability:url:1.0?scheme=file</capability>
    <capability>urn:ietf:params:netconf:capability:rollback-on-error:1.0</capability>
    <capability>urn:ietf:params:netconf:capability:candidate:1.0</capability>
    <capability>urn:ietf:params:netconf:capability:confirmed-commit:1.0</capability>
    ... salida omitida para mayor claridad
  </capabilities>
  <session-id>21992</session-id>
</hello>
]]>]]>
```

Para establecer una conexión exitosa, en necesario que el cliente envie su propio `<hello>`, indicando sus "capabilites".  Haremos esto de la siguiente forma:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <capabilities>
        <capability>urn:ietf:params:netconf:base:1.0</capability>
    </capabilities>
</hello>]]>]]>
```

Ahora estamos listos para enviar pedidos (RPCs) al router. Enviaremos un RPC con una operación `get-config` pidiendo por la configuración de la datastore `running`. Si todo sale bien, el router debería respondernos con su running-config en formato XML.

```xml
<rpc xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="534">
    <get-config>
        <source>
            <running/>
        </source>
    </get-config>
</rpc>]]>]]>
```

> Nota: al enviar los mensajes no olvidar incluir el `]]>]]>` esto es lo que indica el fin del mensaje.

### Netconf ncclient

ACA EXPLICAMOS ncclient Y HACEMOS ALGUNOS EJERCICIOS.

Ej 1) Mostrar Netconf capabilities exchange.

```xml
cisco@cisco:~$ ssh cisco@nxosv -s netconf
User Access Verification
cisco@nxosv's password: 
<?xml version="1.0" encoding="ISO-8859-1"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:xml:ns:netconf:base:1.0</capability>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
    <capability>urn:ietf:params:netconf:capability:validate:1.0</capability>
    <capability>urn:ietf:params:netconf:capability:writable-running:1.0</capability>
    <capability>urn:ietf:params:netconf:capability:url:1.0?scheme=file</capability>
    <capability>urn:ietf:params:netconf:capability:rollback-on-error:1.0</capability>
    <capability>urn:ietf:params:netconf:capability:candidate:1.0</capability>
    <capability>urn:ietf:params:netconf:capability:confirmed-commit:1.0</capability>
  </capabilities>
  <session-id>21992</session-id>
</hello>
]]>]]><?xml version="1.0" encoding="ISO-8859-1"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:xml:ns:netconf:base:1.0</capability>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
    <capability>urn:ietf:params:netconf:capability:validate:1.0</capability>
    <capability>urn:ietf:params:netconf:capability:writable-running:1.0</capability>
    <capability>urn:ietf:params:netconf:capability:url:1.0?scheme=file</capability>
    <capability>urn:ietf:params:netconf:capability:rollback-on-error:1.0</capability>
    <capability>urn:ietf:params:netconf:capability:candidate:1.0</capability>
    <capability>urn:ietf:params:netconf:capability:confirmed-commit:1.0</capability>
  </capabilities>
</hello>
]]>]]>
```

Estas capabilities muestran las versiones de Netconf soportadas, hoy en día las dos versiones disponibles son `1.0` y `1.1`

`urn:ietf:params:netconf:base:1.0`

`urn:ietf:params:netconf:base:1.1`

Para entender las capabilities que se devuelven:

![alt understand_netconf_capabilities](imagenes/netconf_understand_capabilites.png)





## 



## 