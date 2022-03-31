
## Reutilización del código

A medida que queremos realizar tareas mas complejas, el contenido de nuestro playbook será mas extenso. Y si bien es posible escribir todo el playbook en un único archivo `.yml` grande, eventualmente vamos a querer partirlo en secciones mas pequeñas, que nos permitan no solo gestionarlo de mejor manera, sino además reutilizar código en otros playbooks, algo que a la larga nos resultará muy útil.

En Ansible, hay tres formas de hacer esto: `includes`, `imports`, and `roles`. 
Si bien mencionaremos como funcionan las tres, nos concentraremos en al utilización de `roles`, que es sin dudas uno de los puntos fuertes de Ansible.

Mediante `include` e `import` podemos dividir nuestro código complejo o largo, en múltiples archivos mas pequeños, con funciones específicas, y luego invocarlos desde otros playbooks.

Los `roles` van mas lejos, dado que además del código, permiten incluir definiciones adicionales, como ser variables, handlers, templates, plugins, etc. Los roles pueden además ser subidos y compartidos por medio de [Ansible Galaxy](https://galaxy.ansible.com/).

Es necesario entender primero que Ansible cuenta con dos modos de operación:
- `static`: Ansible pre-procesa todos los archivos (ej. playbooks) y sus referencias, antes de comenzar a ejecutar las taeas en los hosts.
- `dynamic`: Ansible procesa los archivos durante la ejecución, es decir, a medida que va encontrando las tareas, leyendo los archivos y ejecutandolas en los hosts.

Si queremos que Ansible funcione en modo `static` debemos referenciar los archivos de nuestro código por medio de `import`. Mientras si queremos que se comporte de forma dinámica, utilizaremos `include`.

Existen algunas limitaciones en el uso de `import` e `include` que es importante tener en cuenta:
- Solo podemos realizar `Loops` en modalidad `dinámica`, esto es, con `include`. 
- Las variables definidas a nivel de inventario no serán consumidas en modalidad `estática`, con `import`.

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

y luego en otro `playbook` importar el anterior, para poder ejecutarlo:
```yaml        
# three_tier_app.yml
- import_playbook: webservers.yml
```

---

## Ansible Roles
[Ref: Ansible Roles](https://docs.ansible.com/ansible/latest/user_guide/playbooks_reuse_roles.html)

Los roles son un elemento fundamental a la hora de escribir nuestro código en forma mas sencilla y estructurada, y poder además reutilizarlo e incluso compartirlo.

Los roles permiten importar de forma automática no solo las tareas a ejecutar, sino también variables, handlers, templates, y otros componentes, basado en una estructura de directorios especifica. Los roles puede ser luego utilizados en multiples `playbooks`, o compartidos a traves de Ansible Galaxy.

Los `roles` requieren cierta estructura de directorios definida para su funcionamiento. Para empezar, deben ubicarse siempre dentro del directorio `./roles` de nuestro proyecto.
Allí, se crea un directorio para cada `role` con el nombre que querramos darle, el cuál se referenciará luego para su invocación desde el `playbook`. 

Dentro del rol se crea la siguiente estrucutura de directorios:

```
roles/
  nombre-del-rol/
    defaults/
    files/
    handlers/
    library/
    meta/
    tasks/
    templates/
    vars/
    README.md
```

Al menos uno de estos directorios debe existir dentro de la carpeta del rol, sin embargo, no es necesario que existan todos. Típicamente se utiliza por lo menos el directorio `tasks`, que contiene el código con las tareas a ejecutar, y `defaults` (o `vars`) que contiene las variables predefinidas para el rol.

Para cada directorio que creemos dentro del rol, debe existir un archivo llamado `main.yml`, en donde se encuentra la información por defecto que va ir a buscar Ansible para ese directorio. Los principales son:

- `tasks/main.yml`: contiene el código con las tareas a ejecutar por defecto para el rol.
- `defaults/main.yml`: contiene la definición de las variable utilizadas por defecto para el rol. Las variables que aquí se definan tienen la menor prioridad posible, y serán sobreescritas por cualquier definición de variable realizada en cualquier otro lugar de nuestro código.
- `vars/main.yml`: otras variables definidas para el rol, que tienen mayor precedencia a las definidas en el directorio anterior.
- `files/main.yml`: archivos que utilice el rol para su ejecución.
- `templates/main.yml`: templates que despliegue el rol.
- `meta/main.yml` - metadata para el rol, por ejemplo para definir dependencias con otros roles.


Dentro de `tasks/main.yml`, se encuentran las tareas a ejecutar por defecto para el rol, y en caso de querer incluir múltiples tareas podemos hacerlo en forma de lista:
```yaml
# ./roles/nombre-del-rol/tasks/main.yml
- tarea1
- tarea2
- tarea3
```

Podemos escribir todo nuestro código de corrido en `tasks/main.yml`, o bien podemos separarlo en varios archivos e invocarlos según los necesitemos, lo cual nos permite simplificar la escritura en caso de roles más complejos. 

Por ejemplo, cuando se quiere que un rol sea capaz de interactuar con multiples sistemas operativos, los cuales pueden requerir realizar distintas tareas y utilizar distintos módulos, para cumplir con un mismo objetivo final. En la documentación de Ansible se presenta un ejemplo similar al siguiente, para demostrar esta práctica:

```yml
# estructura de directorios
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

#### roles:
Una vez definido el rol, el mismo puede ser invocado desde un `playbook` a través de la sentencia `roles:`, la cuál consume una lista de roles a ejecutar:

```yml
# playbook.yml
- name: install apache2 
  hosts: web
  roles:
    - apache2
    - update-web-content
    - verify-web-services

# estructura de directorios
roles/
  apache2/
    tasks/main.yml
  update-web-content
    tasks/main.yml
  verify-web-services
    tasks/main.yml
```

---

### Ejercicio #4
Cree dos roles, uno llamado `apache2` y otro `sqlite3`, que instalen `apache` y `sqlite3` respectivamente. Luego, cree un `playbook` que aplique el rol `apache2` a los servidores del grupo `app` y el rol `sqlite3` a los servidores del grupo `db` de nuestro inventario.

<details>
	<summary>
		Pista #1
	</summary>
	Recuerde que los roles deben ubicarse dentro del directorio <code>/roles</code> del proyecto, comience por crear la estructura de directorios necesaria.
</details>
<details>
	<summary>
		Pista #2
	</summary>
	Las carpetas creadas para el rol deben contrar con el archivo <code>main.yml</code>, que es el que Ansible irá a buscar por defecto.
</details>
<details>
	<summary>
		Pista #3
	</summary>
	Debe crear dos roles diferentes, y luego en el playbook invocar un rol para el grupo de hosts <code>app</code> y otro rol para el grupo de hosts <code>db</code>.
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
ejer4_playbook.yml
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
# ejer4_playbook.yml
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

#### include_role: / import_role:
En nuestro playbook, podemos también invocar los roles desde nuestra lista de `tasks:`, por medio de `include_role:` (en forma dinámica) o `import_role:` (en forma estática).  En general es mucho más común hacerlo de esta forma, en lugar de invocarlos mediante `roles:` como vimos mas [arriba](#roles). 
```yaml
# playbook.yml
- name: install apache2 
  hosts: web
  tasks:
    - import_role:
        name: apache2
```


:point_right: Aquí puede ver la documentación oficial de los módulos [include_role](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/include_role_module.html) e [import_role](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/import_role_module.html).


####tasks_from:
Como vimos antes, cuando se llama a un rol desde un playbook Ansible ejecutará por defecto las tareas que se encuentren en el archivo `task/main.yml`. Pero puede suceder que en realidad querramos ejecutar tareas que se encuentren en otro archivo `.yml`. Esto podemos hacerlo utilizando la sentencia `tasks_from`:

```yaml
# playbook.yml
- name: install apache2 
  hosts: web
  tasks:
    - include_role:
        name: apache2
    - include_role:
        name: apache2
        tasks_from: update-web-content
    - include_role:
        name: apache2
        tasks_from: verify-web-services


# estructura de directorios
roles/
  apache2/
    tasks/
      main.yml
      update-web-content.yml
      verify-web-services.yml
```

Por defecto los roles consumiran siempre las variables que definamos dentro de `./defaults/main.yml`.

Pero si queremos, podemos pasarle variables al rol desde nuestro `playbook` en el momento de su invocación, utilizando la sentencia `vars:`. Esto hará que se sobreescriban los valores por defecto del rol, con los que pasemos a nivel del playbook:


```yaml
# roles/apache2/defaults/main.yml
webserver_document_root: "/var/www/html"

# playbook.yml
- name: install apache2 
  hosts: web
  tasks:
    - import_role:
        name: apache2
    - vars:
        webserver_document_root: "/home/apache/main/html"

# estructura de directorios
roles/
  apache2/
    defaults/main.yml
    tasks/main.yml
playbook.yml
```
En el caso anterior, la variable `webserver_document_root` tomará el valor `/home/apache/main/html` definido a nivel del playbook, el cual sobreescribirá el valor por defecto definido en el rol. Esto se debe a la forma en que Ansible maneja la [precedencia de variables](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#understanding-variable-precedence) de acuerdo al lugar donde éstas sean definidas.

>OBS: recordemos que las variables definidas en `./defaults/main.yml` siempre van a tener el `menor nivel de precedencia posible` respecto a variables definidas en cualquier otro lugar de nuestro código.

---
## Templates
Ref: [Ansible Templates (jinja2)](https://docs.ansible.com/ansible/latest/user_guide/playbooks_templating.html)

[Jinja2](https://jinja.palletsprojects.com/en/3.1.x/) es un lenguaje de templating desarrollado sobre python. El mismo se utiliza en varios frameworks importantes de Python como Django para crear páginas web por ejemplo, sin embargo, se puede usar para crear todo tipo de documentos.

Ansible utiliza `Jinja2` para modificar archivos antes de que estos sean distrubuidos a los `hosts`, siendo una de las herramientas más utilizadas para el manejo de templates. 

Por ejemplo, podemos crear un `template` para un archivo de configuración, y por medio de un playbook desplegar ese archivo de configuración a múltiples hosts, pero modificando algunas partes del mismo al momento de copiarlo, para poder colocarle la información correcta de cada host, como ser dirección IP, hostname, etc.
De esta forma evitamos tener que escribir un archivo de configuración específico para cada host, y reutilizamos el mismo código, modificando su contenido en forma dinámica por medio de variables.

La conversión del `template` se realiza en el Ansible controller, antes de que la tarea sea enviada y ejecutada en el host. Esto evita la necesidad de tener instalado `jinja2` en el host destino, sino que el mismo solo es requerido en el controller, es decir, donde corre Ansible.

Los templates pueden ubicarse dentro del directorio `./templates` de nuestro proyecto, o en caso de ser parte de un rol, dentro de `roles/nombre-del-rol/templates` y son archivos con extensión `.j2`.

### Demo Lab: Templates
A modo de ejemplo, tomemos la funcionalidad de poder desplegar un mensaje de bienvenida en Linux cuando un usuario se conecta, algo conocido como [motd](https://manpages.ubuntu.com/manpages/trusty/man5/motd.5.html) (message of the day). Para esto, es necesario crear un archivo con el texto que queremos desplegar, y ubicarlo en `/etc/motd` dentro del host.

Pero supongamos que queremos colocar información específica del host donde se está corriendo, dentro de ese mensaje, como ser su dirección IP y nombre del host, etc.

Creamos el archivo de template:
```yml
# ./templates/motd.j2

----------------------------------------------------------------------------------
Welcome to {{ course_name }} on {{ ansible_hostname }}.
Running {{ ansible_distribution }} {{ ansible_distribution_version}} on {{ ansible_architecture }} architecture.
Have a nice day!!
----------------------------------------------------------------------------------

```
Luego creamos nuestro `playbook` que copiará el `template` anterior a los hosts, sustituyendo las variables definidas de forma que quede customizado para cada uno.

```yml
# motd_playbook.yml
- name: Configurar message-of-the-day 
  hosts: all
  gather_facts: yes
  vars:
    - course_name: "Ansible-101"
  tasks:
    - template:
        src: motd.j2
        dest: /etc/motd
        owner: root
        group: root
        mode: 0644
```

:point_right: Puede encontrar la documentación del módulo `template` en el siguiente [link](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/template_module.html#template-module).

Luego corremos el playbook (ya deberíamos saber como hacerlo), y cuando nos conectemos a alguno de nuestros `hosts` mediante ssh vamos a ver nuestro mensaje como parte del mensaje de bienvenida:
```
(controller) # ssh host01
(...parte de la salida omitida para mayor claridad...)

----------------------------------------------------------------------------------
Welcome Ansible-101 on host01.
Running Ubuntu 20.04 on x86_64 architecture.
Have a nice day!!
----------------------------------------------------------------------------------
(...)
```

El `template` que creamos mas arriba consume la variable `course_name` desde el propio playbook.
El resto de las variables son cargadas por Ansible en forma automática previo a la ejecución de las tareas en cada uno de los `hosts`, gracias a la ejecución del modulo [gather_facts](https://docs.ansible.com/ansible/2.9/modules/gather_facts_module.html). Puede ver la información que este último trae, mediante el comando `ansible host01 -m gather_facts`, contra cualquiera de los hosts.

Las variables del `template` son sustituidas por su valor al momento de ejecutar el playbook, y antes de copiar el archivo al `host` remoto. De hecho, si se conecta por ssh a uno de los hosts y hace un `cat /etc/motd` verá el archivo modificado.

---

### Ejercicio #5 

Tomando como base el [Ejercicio #4](#ejercicio-4) modifique el rol `apache2`, para que cambie el contenido de la página web por defecto dependiendo en que `host` se encuentre. El servidor web deberá desplegar una página similar a la siguiente:
```bash
  Este sitio web se encuentra corriendo en el nodo <host01|host02>.
  Este es el ambiente de <produccion|desarrollo>!!
```

<details>
  <summary>
HTML
  </summary>
</html>
<pre>
&lt;html>
&lt;body>
  &lt;p> Este sitio web se encuentra corriendo en el nodo &lt;host01|host02>.
  &lt;p> Este es el ambiente de &lt;produccion/desarrollo>!!
&lt;/body>
&lt;/body>
&lt;/html>
</pre>
</details>


.
Utilice un `template` para modificar el contenido de esta página, según se encuentre en `host01 | produccion` o `host02 | desarrollo`. 

:warning: Tenga en cuenta que debe iniciar los servicios de Apache en cada host para que el servidor web responda, dado que por defecto se encuentra apagado. Esto puede hacerlo ejecutando el comando `service apache2 restart` en cada host. Pruebe de incluir este paso como una tarea más del rol, para no tener que realizarlo en forma manual. Puede utilizar el módulo `service:` de Ansible, cuya documentación se encuentra [aqui](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/service_module.html).



<details>
	<summary>
		Pista #1
	</summary>
	El directorio <code>document root</code> del servidor web Apache se encuentra ubicado en <code>/var/www/html/</code>, y tiene el archivo <code>index.html</code> que se carga por defecto al acceder al mismo con un navegador.
</details>

<details>
	<summary>
		Pista #2
	</summary>
	Recuerde que puede definir las <code>variables</code> a utilizar en múltiples lugares del proyecto, incluyendo un archivo específico de variables, en el inventario dentro de <code>host_vars/group_vars</code>, en los directorios <code>./defaults ./vars</code> del rol, entre otros.  
</details>

<details>
	<summary>
		Pista #3
	</summary>
	Recuerde que es posible definir tareas dentro del rol en otros archivos por fuera del <code>tasks/main.yml</code>. Luego puede invocar estas tareas, mediante <code>include_role:</code> o <code>import_role:</code> con la opción <code>tasks_from:</code>.  
</details>

<details>
	<summary>
		Verificación
	</summary>
	Puede acceder con un navegador web para verificar que la página es desplegada correctamente, mediante la url <code>http://pod-X.labs.conatest.click:8001/</code> para el <code>host01</code> y <code>http://pod-X.labs.conatest.click:8002/</code> para el <code>host02</code>, donde la <code>X</code> corresponde a su número de pod asignado.
</details>

<details>
    <summary>Solución</summary>
    <pre>
# estructura de directorios
inventory/
  group_vars/
    app.yml
  host_vars/
    host01.yml
  hosts.yml
roles/
  apache2/
    tasks/
      main.yml
      configure_web_server.yml
    templates/
      index.html.j2
ejer4_playbook.yml
ejer5_playbook.yml
</pre>

<pre>
# ./inventory/group_vars/app.yml
application_env: desarrollo
</pre>

<pre>
# ./inventory/host_vars/host01.yml
application_env: produccion
</pre>

<pre>
#./roles/apache2/tasks/configure_web_server.yml 
- name: Copy index.html template to web server document root folder 
  template:
        src: index.html.j2
        dest: /var/www/html/index.html
        owner: root
        group: root
        mode: 0644
        backup: yes        # opcional, resplada el archivo anterior

- name: Restart apache2 services
  service: 
    name: apache2
    state: restarted
</pre>

<pre>
# ./roles/apache2/templates/index.html.j2
&lt;html>
&lt;body>
  &lt;p> Este sitio web se encuentra corriendo en el nodo {{ ansible_hostname }}
  &lt;p> Este es el ambiente de {{ application_env }}!!
&lt;/body>
&lt;/body>
&lt;/html>
</pre>

<pre>
# ejer5_playbook.yml
- name: "Configurar los servidores web"
  gather_facts: yes
  hosts: app
  tasks:
    - include_role:
        name: apache2
        tasks_from: configure_web_server
</pre>
</details>




---

---
## CONTENIDO ACTUALIZADO HASTA ACA 
---


### Ansible Vault





---

## Ansible galaxy

[Ansibe Galaxy](https://galaxy.ansible.com/) es un sitio gratuito mantenido por Red Hat que permite descargar roles desarrollados por la comunidad. Es una excelente forma de simplificar la configuración de nuestros `playbooks`. 

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

### Ejercicio #?

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




[Siguiente >](./03_ansible_networking.md)
