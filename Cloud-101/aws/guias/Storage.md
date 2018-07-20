Amazon Simple Storage Service (Amazon S3)
===


*Fuentes:*
- [Documentación oficial](https://aws.amazon.com/es/documentation/s3/)
- [Página de AWS S3](https://aws.amazon.com/es/s3/)
- [Precios de AWS S3](http://aws.amazon.com/s3/pricing/)


¿Qué es Amazon S3?      
---

Amazon S3 es un **almacenamiento de objetos** creado para almacenar 
y recuperar cualquier cantidad de datos desde cualquier ubicación: 
sitios web y aplicaciones móviles, aplicaciones corporativas y datos de
sensores o dispositivos IoT.

Permite recopilar, almacenar y analizar datos de forma cómoda y sencilla, 
independientemente de su formato y a escala masiva. Es durable, seguro
y altamente escalable. Puede ser accedido desde la interface web, 
desde la línea de comando (Amazon CLI), desde APIs y/o SDKs. 
Puede utilizarse en forma aislada como un repositorio de datos, 
o en forma integrada con otros servicios de AWS.

**Características:**
* Fácil de usar
* Bajo costo (falta agregar costo aprox)
* Disponible (cuatro 9s)
* Durable (once 9s)
* Seguro (AWS IAM)
* Encriptación
* Escalable
* Integrado con otros servicios AWS


**Casos de uso:**
* Backup & Archive
* Almacenar y distribuir contenido (fotos, videos, etc.)
* Static Website Hosting
* Big Data & Analytics
* Almacenamiento de nube híbrida (AWS Store Gateway)
* Datos de aplicaciones Cloud-native
* Distaster recovery (AWS EBS Snapshoots)


Formas de acceso a S3
---

AWS S3, al igual que el resto de los servicios de Amazon, puede
accederse y utilizarse de diversas formas.

* **AWS Management Console**: es una consola web provista por 
Amazon para el acceso a todos sus servicios de AWS. 

* **AWS CLI**: permite acceder a S3 mediante una consola de línea de
 comando. Típicamente utilizando comandos construidos como *aws s3 
 <comando> <opciones>* o *aws s3api <acción> <opciones>*.
 
* **API Rest**: permite utilizar requests HTTPS estándar para crear, 
borrar *buckets* y escribir/acceder los objetos.
Utiliza las operaciones estándard de REST.



Conceptos Básicos
---

#### Buckets
Son los depósitos donde se almacenan los objetos en S3. Representan el nivel mas alto de jerarquía dentro del almacenamiento. Cada objeto encuentra dentro de un *bucket*.
Se pueden crear y utilizar hasta 100 *buckets* por cada cuenta por defecto, y cada *bucket* puede contener miles de objetos.

* El nombre del *bucket* debe ser único dentro de todos los existentes en Amazon S3 
(no solo dentro de mi cuenta).
 
* Debe tener entre 3 y 63 caracteres.

* No puede tener mayúsculas, ni espacios, ni caracteres especiales salvo guiones y puntos, entre otros.  

El nombre del *bucket* será visible en la URL que remite a los objetos almacenados
 en él. **Una vez creado, el nombre no puede ser modificado**.
 
#### Objetos

Los objetos podríamos decir que son los archivos almacenados en Amazon S3.
Es la información que nosotros subimos y accedemos en S3 (fotos, documentos, respaldos,
etc).

Un objeto puede contener cualquier tipo de datos en cualquier formato.
El tamaño máximo para un objeto es de 5TB, y un *bucket* puede contener una 
cantidad ilimitada de objetos.

Cada objeto consiste de *datos* (el archivo propiamente dicho) y *metadatos* (una serie
de información acerca del archivo).

