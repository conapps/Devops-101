## RESTConf - 2017 - RFC 8040

Soporta tanto XML como JSON.
![alt restconf_operations](imagenes/restconf_operations.png)

![alt restconf vs netconf](imagenes/restconf_vs_netconf_operations.png)





# Restconf en IOS-XE

Content-type/Accept-headers

`application/yang-data+json`

Si no especificamos nada viene en XML.

## Enabling restconf

``` cisco
restconf
!
username <username> privilege 15 secret <password> 
!
ip http server
ip http secure-server
```

## Verifying restconf

```cisco
show platform software yang-management process monitor
```

```
ip-172-31-93-76#show platform software yang-management process
confd            : Running 
nesd             : Running 
syncfd           : Running 
ncsshd           : Not Running  ! NETCONF-YANG is not configured, hence ncsshd process is in not running.
dmiauthd         : Running 
dmiauthd         : Running 
nginx            : Running ! nginx process is up due to the HTTP configuration, and it is restarted when RESTCONF is enabled.
ndbmand          : Running 
pubd             : Running
```

## Para identificar que modulos de YANG soporta el equipo

`GET https://hostname/restconf/data/ietf-yang-library:modules-state`

## Para construir la URI

![alt URI construction](imagenes/YANG_to_URI.jpg)

## URLs útiles

### Para traer la running completa

`https://hostname/restconf/data/Cisco-IOS-XE-native:native`

`https://hostname/restconf/data/Cisco-IOS-XE-native:native/ip`



## Request methods supported

### GET

### POST

### PUT

Cualquier cosa que pongamos en el body del request va a ser exactamente como se va a ver el objeto después. Declarativo por naturaleza.

Esto es muy poderoso porque me evita todos los `no` en la configuración cuando quiero borrar lo que estaba antes.

### PATCH

A diferencia del `PUT` el `PATCH` agrega lo que está en el body pero deja lo demás.

### DELETE

Cursos de RESTCONF

<https://learninglabs.cisco.com/lab/lab03-using-restconf-to-interface-with-networking-devices/step/1>

<https://learninglabs.cisco.com/lab/intro-restconf/step/1>