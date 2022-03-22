# Ansible Tower: AWX
_Fuentes:_

- [Documentación oficial](https://docs.ansible.com/ansible_community.html)
- [Pagina de redhat](https://www.redhat.com/en/resources/awx-and-ansible-tower-datasheet)
<!-- - [Usuarios oficial](https://docs.ansible.com/ansible-tower/latest/html/userguide/users.html) -->

Ansible Tower (la version open suource es  'AWX') es una solución con un fronted web para administrar la ejecución de Ansible. Está diseñado para ser el centro de todas las tareas de automatización de una organización y que estas puedan ser ejecutadas gráficamente de forma interactiva ó programar su ejecución.
 

## Dashboard 

En el dashboad se puede ver un estado general de las organizaciones proyectos, host, etc.

Se ve información general y total de equipos con ejecuciones fallidas.

## Inventario

El inventario es el conjunto de host a los cuales vamos a ejecutar las playbooks programadas, este puede dividirse en grupos para ejecutar en determinado conjunto de hosts.

## Proyectos

Es el proyecto donde se encuentran nuestras playbooks y roles, es necesario para luego crear los templates a partir de las playbooks

## Templates/Plantillas

El template es una plantilla de configuración asociada a un playbook, contiene la configuración para la ejecución de la misma como credenciales necesarias, programación de ejecución, inventario a aplicar, permisos de usuario, etc.

En particular, es interesante el uso de encuestas, para la cual se pueden crear formularios que generan interacción con el operador.

## Usuarios y tipos

Los usuarios que tienen acceso al frontend de Awx tanto para administrar el Awx como para ejeutar playbook a nivel de operador. 

Los tipos son:

- Normal: Tienen acceso de lectura y escritura limitado a los recursos (como inventario, proyectos y plantillas de trabajo) para los que se le han otorgado los roles y privilegios apropiados a ese usuario, por ejemplo, a nivel de template se agregan estos usuarios con el permiso que corresponde en el mismo(ejecutar, lectura,admin).

- Auditor de sistema: Tienen solo permisos de lectura para todos los objetos del Awx.

- Administrador de sistema(también conocido como superusuario): tiene todos los privilegios de administración, similar al usuario root de linux.


<!-- ## Organizaciones

Las organizaciones reprensentarian una orgnazación a administrar, para la cual se pueden asociar proyectos, usuarios, inventarios, plantillas etc. -->

## Ejercicio #11

Cree un proyecto con el ejercicio 9 y 10 e importe el inventario para correr las playbooks de estos ejercicios.


## Ejercicio #12
Genere templates con encuesta para ejecutar el ejerció 9 y 10 desde awx.

Para el caso del ejerció 9, harcodee privilege en 15 y en la encuesta solicite el nombre usuario y contraseña(para esta usar un campo de contraseña para que no se muestre al ingresar).

Para el caso del ejercicio 10, generar un formulario que permita ingresar el `room_name` y el `message`.

