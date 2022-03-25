
## Reutilización del código

A medida que querramos realizar tareas mas complejas, el contenido de nuestro playbook será mas extenso. Y si bien es posible escribir todo el playbook en un único archivo `.yml` grande, eventualmente vamos a querer partirlo en secciones mas pequeñas, que nos permitan no solo gestionarlo de mejor manera, sino además reutilizar código en otros playbooks, algo que a la larga nos resultará muy útil.

En Ansible, hay tres formas de hacer esto: `includes`, `imports`, and `roles`. 
Si bien mencionaremos como funcionan las tres, nos concentraremos en al utilización de `roles`.

Mediante `include` e `import` podemos dividir nuestro código complejo o largo, en múltiples archivos mas pequeños, con funciones específicas, y luego invocarlos desde otros playbooks, pudiendo así simplificar las escritura de los mismos y reutilizar nuestro código.

Los `roles` van mas lejos, dado que además del código, permiten incluir definiciones adicionales, como ser variables, handlers, modulos, plugins, etc. Los roles pueden además ser subidos y compartidos por medio de Ansible Galaxy (lo veremos mas adelante).

Es necesario entender primero que Ansible cuenta con dos modos de operación:
- `static`: Ansible pre-procesa todos los archivos y referencias antes de comenzar a ejecutar las taeas.
- `dynamic`: Ansible procesa los archivos durante la ejecución, es decir, a medida que va encontrando las tareas y leyendo los archivos.

Si queremos que Ansible funcione en modo `static` debemos referenciar los archivos por medio de `import`. Mientras si queremos que se comporte de forma dinámica, utilizaremos `include`.

Existen algunas limitaciones en el uso de `import` e `include` que es importante tener en cuenta:
- Loops solo pueden realizarse con comandos de `include`. 
- Las variables definidas a nivel de inventario no serán consumidas por un `import`.

Por ejemplo, podemos tener un `playbook` que instale una determinada aplicación:
```yaml
# webservers.yml
- hosts: app
  tasks:
    - name: Install apache2
      apt: 
        name: apache2
        state: latest
        update_cache: yes
```

y luego en otro `playbook` importarlo para poder ejecutarlo, sin necesidad de tener que reescribir el código:
```yaml        
# three_tier_app.yml
- import_playbook: webservers.yml
```

---

## Roles
Los roles son un elemento fundamental a la hora de escribir nuestro código en forma mas sencilla y estructurada, y poder además reutilizarlo e incluso compartirlo.

Los roles permiten importar de forma automática no solo las tareas a ejecutar, sino también variables, handlers, templates, y otros componentes, basado en una estructura de directorios especifica. Los roles puede ser luego utilizados en multiples `playbooks`, o compartidos a traves de Ansible Galaxy.

Los `roles` requieren cierta estructura de directorios definida para su funcionamiento. Para empezar, deben ubicarse siempre dentro del directorio `./roles` de nuestro proyecto.
Allí, se crea un directorio para cada `role` con el nombre que querramos darle, el cuál se referencia luego para su invocación desde el `playbook`. Dentro del rol se crea la siguiente estrucutura de directorios:

```
roles/
  nombre-de-mi-rol/
    defaults/
    files/
    handlers/
    meta/
    README.md
    tasks/
    templates/
    vars/
```

Al menos uno de estos directorios debe existir dentro de la carpeta del rol, sin embargo, no es necesario que existan todos. Para cada directorio que creemos dentro del rol, debe existir un archivo llamado `main.yml` en donde se encuentra la información por defecto correspondiente a ese directorio.

```
roles/
  nombre-de-mi-rol/
    tasks/
      main.yml
    vars/
      main.yml
```
Dentro del archivo `tasks/main.yml` se colocan las tareas a ejecutar por defecto para el rol, esto es, lo que queremos ejecutar. En caso de querer incluir múltiples tareas, podemos colocarlas en forma de lista:
```yaml
# tasks/main.yml
- tarea1
- tarea2
- tarea3
```

Dentro del archivo `vars/main.yml` se colocan las variables que queremos cargar por defecto cada vez que se invoque el rol.
Y así sucesivamente con el resto de los componentes/directorios del rol, y su archivo `main.yml` correspondiente.

Dentro del archivo `tasks/main.yml` podemos poner todo nuestro código de corrido, o bien podemos separarlo en varios archivos, y referenciarlos según corresponda, lo que nos permite simplificar la escritura en caso de roles complejos. 
Esto es usual, por ejemplo, cuando se quiere que un rol sea capaz de interactuar con multiples sistemas operativos, los cuales pueden requerir de la realización de distintas tareas y utilización de distintos módulos, para cumplir con un mismo objetivo final. 

En la documentación de Ansible se presenta el siguiente ejemplo para demostrar esta práctica:

```
roles/
  apache2/
    tasks/
      main.yml
      redhat.yml
      debian.yml
```

```yaml
# ./roles/apache2/tasks/main.yml
- import_tasks: redhat.yml
  when: ansible_os_family|lower == 'redhat'
- import_tasks: debian.yml
  when: ansible_os_family|lower == 'debian'

# ./roles/apache2/tasks/redhat.yml
- yum:
    name: "httpd"
    state: present

# ./roles/apache2/tasks/debian.yml
- name: Update apt repository cache 
  apt:
    update_cache: yes 
- name: Install apache2
  apt:
    name: "apache2"
    state: present
```

Una vez definido el rol, puede ser invocado desde una `playbook` a través de la opción `roles`, la cuál consume una lista de `roles` a ejecutar.

```yml
# playbook.yml
- name: install apache2 
  hosts: web
  roles:
    - apache2
    - update-web-content
    - xxx
```

---

### Ejercicio #4
Cree dos roles, uno llamado `apache2` y otro `sqlite3`, que instalen `apache` y `sqlite3` respectivamente. Luego, cree un `playbook` que aplique el rol `apache2` a los servidores del grupo `app` y el rol `sqlite3` a los servidores del grupo `db` de nuestro inventario.

<details>
	<summary>
		Pista #1
	</summary>
	Recuerde que los roles deben ser crados dentro del directorio <code>/roles</code> del proyecto.
</details>
<details>
	<summary>
		Pista #2
	</summary>
	Las carpetas creadas para el rol, deben contrar al menos con un archivo llamado <code>main.yml</code> , que es el que Ansible va a ir a buscar por defecto.
</details>
<details>
	<summary>
		Pista #3
	</summary>
	Las tareas a ejecutar por defecto para el rol, se definen dentro del archivo <code>tasks/main.yml</code> .
</details>

<details>
    <summary>Solución</summary>
    <pre>
# estructura de directorios
inventory/
  hosts.yml
roles/
  apache2/
    tasks/
      main.yml
  sqlite3/
    tasks/
      main.yml
ejer4-playbook.yml
</pre>
<pre>
# ./roles/apache2/tasks/main.yml
- apt:
    name: apache2
    state: present
    update_cache: yes
</pre>
<pre>
# ./roles/sqlite3/tasks/main.yml
- apt:
    name: sqlite3
    state: present
    update_cache: yes
</pre>
<pre>
# ejer4-playbook.yml
- name: "Instalar los servidores web"
  hosts: app
  roles:
    - apache2
- name: "Instalar los servidores de bases de datos"
  hosts: db
  roles:
    - sqlite3
</pre>
</details>

---

_OBS: También se puede correr un rol desde una tarea a través del comando `import_role`_

Por defecto, cuando indiquemos el rol solo por su nombre, Ansible buscara la carpeta del rol en la siguiente ubicación `./roles/<nombre_de_rol>`. En caso de que el rol al cual queramos hacer referencia se encuentre en otra ubicación, podemos utilizar una dirección al directorio en vez de su nombre. La única diferencia es que tenemos que utilizar la llave `role` dentro de la lista de roles.

```yaml
- hosts: webservers
  roles:
    - role: ~/ansible/roles/apache2
```

Los roles puedes consumir variables definidas dentro del `playbook` a través de la opción `vars`. Las variables definidas de esta manera sobreescribirán los valores por defecto que se hayan configurado dentro del rol.






---
---

---

## Ansible galaxy

[Ansibe galaxy](https://galaxy.ansible.com/) es un sitio gratuito mantenido por Red Hat que permite descargar roles desarrollados por la comunidad. Es una excelente forma de simplificar la configuración de nuestros `playbooks`. 

Utilizando la aplicación `ansible-galaxy` podemos:

- Descargar roles.
- Construir templates para armar nuestros propios roles.
- Buscar roles.

Aunque es posible buscar por roles desde la consola utilizando `ansible-galaxy`, es mucho más sencillo cuando lo realizamos la búsqueda a través de la aplicación web.

Una vez que encontremos el rol que queremos usar, lo podemos importar a la aplicación a través del comando `ansible-galaxy install`.

Por ejemplo, el siguiente comando instala un rol capaz de interactuar con dispositivos CISCO que utilicen IOS como sistema operativo:

```bash
ansible-galaxy install ansible-network.cisco_ios
```

Por defecto los roles descargados desde `ansible-galaxy` se instalarán en `~/.ansible/roles`. Sin embargo, podemos cambiar el directorio donde queremos que se instale el rol utilizando la opción `-p`.

---

### Ejercicio #5

Construya el mismo `playbook` que en el ejercicio 4 pero utilizando roles obtenidos de `ansible-galaxy`.

_OBS: para evitar problemas de permisos, configuren la opción `ansible_become` como `false` en las variables del inventario. Esto es necesario porque estamos accediendo a los servidores como `root` y muchos `roles` online presuponen que por defecto los usuarios con los cuales se van a ejecutar las tareas no tienen este rol._

<details>
    <summary>Solución</summary>
    <pre>
- name: "Instalar los servidores web"
  hosts: app
  roles:
    - role: asianchris.apache2
- name: "Instalar sqlite"
  hosts: db
  roles:
	- manala.sqlite    
  </pre>
</details>

---


## Templates
https://github.com/ansible/workshops/tree/devel/exercises/ansible_rhel/1.6-templates


[Siguiente >](./03_ansible_networking.md)
