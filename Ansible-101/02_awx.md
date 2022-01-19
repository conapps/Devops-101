# Ansible Tower: AWX
_Fuentes:_

- [Documentación oficial](https://docs.ansible.com/ansible_community.html)

Ansible Tower (la version open suource es  'AWX') es una solución con un fronted web para admiinstrar la ejecucion de Ansible. Está diseñado para ser el centro de todas las tareas de automatización de una organización y que estas puedan ser ejecutadas graficamente de forma interactiva ó programar su ejecución.
 
## Dashboard 

En el dashboad se puede ver un estado general de las organizcciones procyectos, host, etc.

## Usuarios y perfiles

Son los usuarios que podran ejecutar las playbookm....


## Inventario

El inventario es el conjunto de host a los cuales vamos a ejecutar las playbooks programadas, este puede dividirse en grupos para ejecutar en determinado conjunto de hosts.

## Proyectos

Es el proyecto donde se encuentan nuestras playbooks y roles, es necesario para luego crear los templates apartir de las playbooks

## Templates

El template es una planilla de configuracion asociada a un playbook, contiene la configuracion apra la ejecucion de la misma como credenciales necesarias, programacion de ejecucion, inventario a apicar, permismos de usuario, etc-

En particular, es intereante el uso de encuestas, para la cual se pueden crear formualrios 

