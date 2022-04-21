# Desafío final

## Contexto

El cliente ACME, quien tiene instalada una red WiFi Meraki provista por Conatel, sistemáticamente tiene problemas de falta de ancho de banda en sus enlaces.
Esto se debe a que los usuarios de la red están permanentemente utilizando aplicaciones no corporativas muy demandantes de ancho de banda.
Cuando se origina un incidente, el departamento de sistemas aplica un traffic-shapping a las aplicaciones detectadas, lo cual soluciona el inconveniente por un tiempo.
El problema es que de forma recurrente van surgiendo sitios y aplicaciones nuevas, lo que hace que la situación se repita una y otra vez.
Su objetivo es detectar de forma temprana cuando en su red aparece una aplicación muy demandante de ancho de banda para poder determinar si filtrarla o no.
El planteo del gerente de sistemas es que si bien el dashboard presenta esta información, él necesita entrar periódicamente para revisarlo, cosa que habitualmente olvida. Su intención es que el sistema le avise de forma proactiva cuando alguna de las aplicaciones en su red supere un umbral de tráfico definido para un período de tiempo particular. Pero el dashboard de Meraki no provee esta funcionalidad...

## Desafío

Desarrollar un script en Python que reciba como parámetro un umbral de tráfico (en Bytes), y que al correrlo analice el consumo en el ** último mes ** de las aplicaciones que cursaron tráfico en la red. Si alguna de las aplicaciones detectadas excedió dicho umbral (al sumar el tráfico recibido y el enviado), hay que enviar un mensaje a la sala de Webex del departamento de sistemas de ACME. A modo de ejemplo, el mensaje debe tener el siguiente formato:

```
Aplicaciones que han traficado mas de X Bytes en el último mes:

Dropbox:
  Enviado: 104567
  Recibido: 2345653
  Total: 2450220

Netflix:
  Enviado: 104566
  Recibido: 2345650
  Total: 2450224

Spotify:
  Enviado: 542356
  Recibido: 1234984
  Total: 1777340
```

Los técnicos de ACME se encargarán luego de configurar sus sistemas para que el script provisto por Conatel se corra todos los días de forma automática.

## Datos

#### Meraki

---

##### Clave para poder autenticar con la API de Meraki

MERAKI_KEY = "4e071834c19d13104776af28be360d297cc365fb"

##### Nombre de la organización que contiene la red para la cuál hay que obtener estadísticas

ORG_NAME = 'C008 - Preventa Conatel'

##### Nombre de la red para cuál hay que obtener estadísticas

NETWORK_NAME = 'X001 - LAB CONATEL'

#### Webex

---

##### Clave para poder autenticar con la API de Webex

WEBEX_KEY = "a definir el día del laboratorio"

##### Nombre de la sala donde hay que publicar las alarmas de tráfico

WEBEX_ROOM_NAME = "devnet_express_telefonica"
