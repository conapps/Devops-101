# Cloud 101 - Definiciones

## ¿Que queremos decir con tecnologías de nube o `cloud computing`?

> "...internet-based computing in which groups of remote servers are networked to allow the centralized data storage, and online access to computer services and resources."
> 
> **Definición de `cloud computing` según Wikipedia.-**

Esta definición es demasiado vaga, aunque es la más utilizada. 

El "National Institute of Standards and Technology" o [NIST](#)(https://www.nist.gov/) en cambio, la define de la siguiente manera:

> "Cloud computing is a model for enabling ubiquitous, convenient, on-demand network access to a _shared pool of configurable computing resources_ (e.g., networks, servers, storage, applications, and services) that can be rapidly provisioned and released with minimal management effort or service provider interaction. This cloud model is composed of _five essential characteristics, three service models, and four deployment models._"
> 
> **Definición de `cloud computing` según NIST.-**

**Características esenciales**

Veamos que a qué hacen referencia cada una de estas características escenciales.

- **On-demand self-service**: El consumidor puede aprovisionar servicios de computo sin necesidad de interactuar con otra persona para realizarlo.
- **Broad network access**: Se debe poder acceder a los servicios a través de una red utilizando mecanismos estandar.
- **Resource pooling**: Los recursos son compartidos por varios consumidores dentro de un modelo multi-tenant, y son distribuidos y re-asignados de acuerdo a la demanda de los consumidores. Los consumidores por su parte, no saben exactamente qué recurso físico esta sirviendo a su aplicación. Como máximo contará con algún nivel de abstracción que le permita identificar de que país, ciudad, o datacenter quiere se le asignen los recursos.
- **Rapid elasticity**: Las funcionalidades de los servicios pueden ser aprovisionadas y liberadas de forma elástica, de forma manual o automática, de acuerdo a la demanda del consumidor. Desde su punto de vista, el consumidor debe percibir que esta trabajando con un pool de recursos ilimitados que puede consumir en cualquier momento.
- **Measured service**: Todos los servicios cuentan con algún sistema de medición que permite llevar la cuenta de su uso. Esta información debe estar disponible al consumidor, y es la utilizada para cobrarle el uso del servicio.

Las servicios de `cloud` cuentan además con otras cualidades adicionales a estas, como: `alta disponibilidad`, `escalabilidad`, `seguridad`, `robustez`, etc.

**Modelos de servicio**

Definiciones desarrolladas por NIST.

- **Infraestructure as a Service (_IaaS_)**: The capability provided to the consumer is to provision processing, storage, networks, and other fundamental computing resources where the consumer is able to deploy and run arbitrary software, which can include operating systems and applications. The consumer does not manage or control the underlying cloud infrastructure but has control over operating systems, storage, and deployed applications; and possibly limited control of select networking components (e.g., host firewalls).
- **Platform as a Service (_PaaS_)**: The capability provided to the consumer is to deploy onto the cloud infrastructure consumer-created or acquired applications created using programming languages, libraries, services, and tools supported by the provider.The consumer does not manage or control the underlying cloud infrastructure including network, servers, operating systems, or storage, but has control over the deployed applications and possibly configuration settings for the application-hosting environment.
- **Software as a Service (_SaaS_)**: The capability provided to the consumer is to use the provider’s applications running on a cloud infrastructure. The applications are accessible from various client devices through either a thin client interface, such as a web browser (e.g., web-based email), or a program interface. The consumer does not manage or control the underlying cloud infrastructure including network, servers, operating systems, storage, or even individual application capabilities, with the possible exception of limited user-specific application configuration settings.

![](https://raw.githubusercontent.com/conapps/Devops-101/master/Cloud/aws/imagenes/001.png "IaaS, PaaS, SaaS")

**Tipos de nubes**

Los tipos de nubes se determinan en base a _quien_ es el consumidor del servicio y no en base a quién lo administra. Por ejemplo, una _private cloud_ es aquella que existe para dar servicio a una organización, pero puede estar administrada por un tercero, y no por la propia organización.

Los tipos de `cloud` más populares son:

- _Private Clouds_
- _Community Clouds_
- _Public Clouds_
- _Hybrid Clouds_

[Referencia](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-145.pdf): Peter MellTimothy Grance. “NIST SP 800-145, The NIST Definition of Cloud Computing.” Apple Books.

## ¿Qué aplicaciones pueden implementarse en la nube?

Cualquier tipo de aplicación puede migrarse a la nube, sin embargo, hay ciertas aplicaciones que pueden aprovechar de mejor manera los recursos de la nube. Por ejemplo:

- Aplicaciones con grandes variaciones de tráfico.
- Aplicaciones de streaming.
- Pruebas de concepto.
- Aplicaciones multimedia.
- Aplicaciones con grandes volúmenes de datos.
- Aplicaciones de escala mundial.

## ¿Cuales son los beneficios de utilizar tecnología cloud?

Los beneficios son muchos y dependen del tipo de servicio que utilicemos. De todas maneras, muchos de ellos caen dentro de los siguiente:

- **La nube esta diseñada para escalar.** A diferencia de nuestros sistemas internos, las tecnologías `cloud` ya tienen todo lo necesario para soportar cualquier tipo de demanda. No tenemos que predecir lo que necesitamos de antemano, ni incluir en el diseño de nuestro proyecto los pasos a seguir para escalar la plataforma. Podemos suponer que cuando sea necesario, lo vamos a poder hacer, sin importar los requerimientos.
- **Automatización.** Las mayoría de los servicios `cloud` (públicos o privados) cuentan con numerosas herramientas que permiten automatizar cualquier tipo de tarea.
- **Disaster Recovery**. Diseñar una aplicación robusta es más sencillo en la nube. Porque en general, contamos con múltiples regiones, zonas de disponibilidad, y recursos a utilizar. Además, si utilizamos servicios `PaaS` o `SaaS` el diseño se hace todavía más sencillo, porque podemos utilizar los `SLA` que nos brinda el proveedor.
- **Procesamiento en paralelo.** Es mucho más sencillo desarrollar aplicaciones que escalen horizontalmente, o que puedan tomar provecho de realizar acciones en paralelo. Especialmente importante en aplicaciones de analítica de datos, o en aplicaciones con grandes consumos de ancho de banda (streaming). Los anchos de banda de los servicios `cloud`, sobre todo aquellos de cara a Internet, son mucho más potentes que los que usualmente contamos en nuestros data centers.
- **Rendimiento**. Si nuestras aplicaciones tienen `SLA` muy exigentes es complicado estimar la cantidad de requerimientos que necesitamos para cumplirlos. Especialmente si la demanda de estas aplicaciones varía con el tiempo. En estos casos es usual tener qué comprar equipamiento para soportar los picos, lo que deja un montón de computo inutilizado durante los períodos de uso promedio.

---
<div style="width: 100%">
  <div style="float: left"><a href="../guias/00_introduccion.md">⬅️00 - Introducción</a></div>
  <div style="float: right"><a href="../guias/02_aws.md">02 - AWS ➡️</a></div>
</div>