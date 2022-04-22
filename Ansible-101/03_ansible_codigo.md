
## Reutilización del código
Ref: [Re-using Ansible Artifacts](https://docs.ansible.com/ansible/latest/user_guide/playbooks_reuse.html)

A medida que queremos realizar tareas mas complejas, el contenido de nuestro playbook será mas extenso. Y si bien es posible escribir todo el playbook en un único archivo `.yml` grande, eventualmente vamos a querer partirlo en secciones mas pequeñas, que nos permitan no solo gestionarlo de mejor manera, sino además reutilizar código en otros playbooks, algo que a la larga nos resultará muy útil.

En Ansible, hay tres formas de reutilizar código: `includes`, `imports`, and `roles`. 
- Con `includes` o `imports` podemos dividir nuestro código en múltiples archivos mas pequeños, con funciones específicas, y luego invocarlos desde otro playbook.
- Los `roles` van bastante más lejos, dado que además del código, permiten incluir definiciones adicionales, como ser variables, handlers, templates, plugins, etc. Los roles pueden además ser subidos y compartidos por medio de [Ansible Galaxy](https://galaxy.ansible.com/).

#### Static & Dynamic

Es necesario entender primero que Ansible cuenta con dos modos de operación:
- `static`: Ansible pre-procesa todos los archivos (ej. playbooks) y sus referencias, antes de comenzar a ejecutar las taeas en los hosts.
- `dynamic`: Ansible procesa los archivos durante la ejecución, es decir, a medida que va encontrando las tareas, leyendo los archivos y ejecutandolas en los hosts.

Si queremos que Ansible funcione en modo `static` debemos referenciar los archivos de nuestro código por medio de `import`. Mientras si queremos que se comporte de forma dinámica, utilizaremos `include`.

Existen algunas limitaciones en el uso de `import` e `include` que es importante tener en cuenta:
- Solo podemos realizar `Loops` en modalidad `dinámica`, esto es, con `include`. 
- Las variables definidas a nivel de inventario no serán consumidas en modalidad `estática`, con `import`.

#### `import_playbook:`

Por ejemplo, podemos tener un `playbook` que instale una determinada aplicación:
```yaml
# deploy_webservers.yml
- hosts: web-server
  tasks:
    - name: Install apache2
      apt: 
        name: apache2
        state: latest
        update_cache: yes
```

```yaml
# deploy_db.yml
- hosts: db-server
  tasks:
    - name: Install SQLite
      apt: 
        name: sqlite3 
        state: latest
        update_cache: yes
```

y luego desde otro `playbook` importar el anterior, para poder ejecutarlo:
```yaml        
# mi_playbook_principal.yml
- hosts: localhost
  tasks:
    - debug:
        msg: Este es mi playbook principal

- name: "Instalar el web-server"
  import_playbook: ./deploy_webservers.yml

# ESTO FALLA!! pues no puedo importar un playbook dentro de un play
- name: "Instalar el db-server"
  hosts: db-server
  tasks:
    import_playbook: /deploy_db.yml
```


#### `import_tasks` & `include_tasks:`
Ref: [include_tasks module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/include_tasks_module.html) | [import_tasks module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/import_playbook_module.html)


Importar un `playbook` completo no es lo más común. En general solemos importar `tareas` que realizan funciones específicas, y que tenemos escritas en archivos .yml independientes. Esto nos permite reutilizar nuestro código de forma mas eficiente.

```yaml
# deploy_webservers.yml
- name: Install apache2
  apt: 
    name: apache2
    state: latest
    update_cache: yes
```

```yaml
# deploy_db.yml
- name: Install SQLite
  apt: 
    name: sqlite3 
    state: latest
    update_cache: yes
```

y luego llamamos estas tareas en nuestro `playbook`:
```yaml        

# mi_playbook_principal.yml
- hosts: localhost
  tasks:
    - debug:
        msg: Este es mi playbook principal

- name: "Instalar el web-server"
  hosts: web-server
  tasks:
    import_tasks: ./deploy_webservers.yml

- name: "Instalar el db-server"
  hosts: database-server
  tasks:
    include_tasks: /deploy_db.yml

```

Pero la forma más eficiente y potente de reutilizar nuestro código es mediante el uso de `roles`.

---

## Ansible Roles
[Ref: Ansible Roles](https://docs.ansible.com/ansible/latest/user_guide/playbooks_reuse_roles.html)

Los roles son un elemento fundamental a la hora de escribir nuestro código en forma mas sencilla y estructurada, y poder además reutilizarlo e incluso compartirlo.

Los roles permiten importar no solo las tareas a ejecutar, sino que también incluyen variables, handlers, templates, y otros componentes. Los roles puede ser luego utilizados en multiples `playbooks`, o incluso compartirlo, por ejemplo mediante Ansible Galaxy.

Los `roles` requieren cierta estructura de directorios despecífica para su funcionamiento. Para empezar, deben ubicarse siempre dentro del directorio `./roles` de nuestro proyecto. Allí, se crea un directorio para cada `role` que definamos, cuyo nombre se referenciará luego para su invocación desde el `playbook`. 

El `rol` tiene la siguiente estrucutura de directorios:
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

Al menos uno de estos directorios debe existir dentro de la carpeta del rol, sin embargo, no es necesario que existan todos estos directorios. En general se utiliza siempre el directorio `tasks` que contiene las tareas que vamos a ejecutar. Y típicamente, se utilizan ademas los directorios `defaults` o `vars` que contiene las variables predefinidas para el rol. También podemos tener el directorio `templates` (cuya utilidad veremos más adelante), y `files`.

:point_right: Es buena práctica utilizar un archivo de `README.md` que explique el funcionamiento y requerimientos del rol.

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
:point_right: Cuando invoquemos al `rol` desde el `playbook`, Ansible ejecutará automáticamente todas las tareas que se encuentren en este archivo `tasks/main.yml`.

Aquí también podemos escribir todo nuestro código de corrido en `tasks/main.yml`, o separarlo en varios archivos e invocarlos según los necesitemos, simplificando la escritura en caso de roles más complejos. 

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

#### `roles:`
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

#### `include_role:` & `import_role:`
Ref: [include_role](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/include_role_module.html) | [import_role](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/import_role_module.html)

En nuestro playbook, podemos también invocar los roles desde nuestra lista de `tasks:`, por medio de `include_role:` (en forma dinámica) o `import_role:` (en forma estática).  En general es mucho más común hacerlo de esta forma, en lugar de invocarlos mediante `roles:` como vimos antes. 
```yaml
# playbook.yml
- name: install apache2 
  hosts: web
  tasks:
    - import_role:
        name: apache2
```

También podemos utilizar `loops` en la llamda a nuestros roles, siempre que usemos `include_role:`. Vea el siguiente ejemplo, similar al que se encuentra en la documentación del módulo:
```yaml
- name: Use role in loop
  include_role:
    name: my-role
  vars:
    some_role_variable: '{{ loop_var }}'
  loop:
    - '{{ roleinput1 }}'
    - '{{ roleinput2 }}'
  loop_control:
    loop_var: loop_var

```
:point_right: note que en lugar de usar la variable por defecto `item` para iterar sobre el loop, en este caso lo cambia por otra variable, llamada `loop_var`. Entiende por que puede ser necesario hacer esto??
<details>
<summary> Respuesta </summary>
  Si dentro de código de <code>my-role</code> se ejecuta algún <code>loop:</code>, seguramente utilice la variable por defecto <code>item:</code>. Y si también utilizo la misma variable <code>item:</code> al llamar al role, la estaría sobreescribiendo, lo que podría causar inconsistencias durante la ejecución de las tareas del role.
</details>


#### `tasks_from:`
Como vimos antes, cuando se llama a un rol desde un playbook Ansible ejecutará por defecto las tareas que se encuentren en el archivo `./task/main.yml`. Pero puede suceder que en realidad querramos ejecutar tareas que se encuentren en otro archivo `.yml`. Esto podemos hacerlo utilizando la sentencia `tasks_from:`

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

#### variables dentro del role:
El primer lugar donde un rol va a buscar la definición de una variable es dentro de `./defaults/main.yml`. Este es además, el lugar que tiene la menor precedencia posible, en cuanto a la definición de variables. Por lo cuál es una buena práctica definir ahí todas las variables que utilice el rol, con sus valores por defecto, para que la ejecución del rol no falle por falta de una variable.

Luego, dentro de `./vars/main.yml` podemos definir variables particulares que necesitemos para la ejecución del rol en determinado ambiente. De esta forma podemos reutilizar el código, en diferentes ambientes, simplemente modificando los valores de ciertas variables. Las variables aquí definidas, sobreescribiran a las definidas en `./defaults/main.yml`. 

Y también, podemos pasarle variables al rol al momento de su invocación, utilizando la sentencia `vars:`. Estas tendrán mayor precedencia que las dos opciones anteriores, por lo cual las sobreescribirán. Por ejemplo:


```yaml
# ./roles/apache2/defaults/main.yml
webserver_document_root: "/var/www/html"

# ./instalar-apache-playbook.yml
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
instalar-apache-playbook.yml
```
En el caso anterior, la variable `webserver_document_root` tomará el valor `/home/apache/main/html` definido a nivel del playbook, el cual sobreescribirá el valor por defecto definido en el rol. 

:point_right: Esto se debe a la forma en que Ansible maneja la [precedencia de variables](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#understanding-variable-precedence) de acuerdo al lugar donde éstas se definan.

Si luego necesito instalar apache2 en otro equipo, pero con el `document_root` en otra ubicación, no necesito modificar el código del rol. Simplemente alcanza con modificar la variable al invocar al rol.

:warning: Es importante tomar en cuenta este tipo de cosas a la hora de construir nuestros roles, como escribir nuestro código de forma de poder luego reutilizarlo en diferentes ambientes. Los `templates` es algo que también pueden ayudarnos mucho a esto.

---
## Templates
Ref: [Templating (jinja2)](https://docs.ansible.com/ansible/latest/user_guide/playbooks_templating.html)

[Jinja2](https://jinja.palletsprojects.com/en/3.1.x/) es un lenguaje de templating desarrollado sobre python. El mismo se utiliza en varios frameworks importantes de Python como Django para crear páginas web por ejemplo, sin embargo, se puede usar para crear todo tipo de archivos.

Ansible utiliza `Jinja2` para modificar archivos en forma dinámica antes de que estos sean distrubuidos a los `hosts`, siendo una herramienta muy utilizada, que nos ayuda a reutilizar nuestro código. 

Por ejemplo, podemos crear un `template` para un archivo de configuración que necesitemos aplicar . Y, por medio de un playbook, desplegar ese archivo de configuración a múltiples hosts, pero modificando algunas partes del mismo al momento de copiarlo, para poder colocarle la información correcta de cada host (como dirección IP, hostname, etc.). 
De esta forma evitamos tener que escribir un archivo de configuración específico para cada host (solo porque cambia la dirección IP o el hostname), y reutilizamos el `template`, modificando su contenido en forma dinámica por medio de variables.

La conversión del `template` se realiza en el Ansible controller, antes de que la tarea sea enviada y ejecutada en el host. Esto evita la necesidad de tener instalado `jinja2` en el host destino, y el mismo solo es requerido en el controller, es decir, donde corre Ansible.

Los templates son archivos con extensión `.j2`. Pueden ubicarse dentro del directorio `./templates` de nuestro proyecto, o en caso de ser parte de un rol, deben estar dentro de `./roles/nombre-del-rol/templates`.

:point_right: `jinja2` es una librería de Python y por tanto se instala con el comando `pip3`. En nuestro laboratorio ya se encuentra instalado en el nodo `contoller`, puede verificarlo con `pip3 freeze | grep -i jinja2`. 


### Demo Lab: Templates
A modo de ejemplo, tomemos la funcionalidad de poder desplegar un mensaje de bienvenida en Linux cuando un usuario se conecta al mismo, algo conocido como [motd](https://manpages.ubuntu.com/manpages/trusty/man5/motd.5.html) (message of the day). Para esto, es necesario crear un archivo con el texto que queremos desplegar, y ubicarlo en `/etc/motd` dentro del host.

Pero supongamos que queremos colocar en el mensaje de bienvendia, información específica del host donde se está corriendo como el nombre del host, distribución de linux, etc.

Creamos entonces el archivo de template:
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

#### `template:`
Para copiar un template a los hosts, y que su contenido sea modificado dinámicamente, utilizamos el módulo `template:`, cuya documentación puede encontrar [aquí](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/template_module.html#template-module).

En este caso indicamos cuál es el archivo de template a copiar (*motd.j2*), a que directorio del `host` lo vamos a copiar (*/etc*), con que nombre de archivo (*motd*), y que permisos le vamos a asignar al archivo (*root.root -rw-r--r--*).

Luego corremos el playbook (ya deberíamos saber como hacer esto!), y confirmamos que los cambios fueron realizados. Y cuando nos conectemos a alguno de nuestros `hosts` mediante `ssh` deberíamos ver nuestro nuevo mensaje como parte del mensaje de bienvenida de linux:
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

Como podemos ver, las variables del `template` son sustituidas por su valor al momento de ejecutar el playbook, y el archivo ya "viaja" modificado al host remoto. De hecho, si se conecta por ssh a uno de los hosts y hace un `cat /etc/motd` verá el archivo con los valores finales.

El `template` que creamos mas arriba consume la variable `course_name` desde el propio playbook. Pero el resto de las variables no las definimos nosotros en ningún lado, sino que son cargadas por Ansible en forma automática para cada uno de los `hosts`, gracias a la ejecución del modulo `gather_facts:`.

#### `gather_facts:`

El módulo `gather_facts:`, cuya documentación se encuentra [aquí](https://docs.ansible.com/ansible/2.9/modules/gather_facts_module.html), se conecta a los `hosts:` antes de comenzar a ejecutar las tareas del playbook. Recaba información específica del `host` y la devuelve en determinadas variables que nosotros luego podemos consumir como parte de nuestras tareas. 

Puede ver las variables que devuelve este módulo ejecutando el siguiente comando add-hoc `ansible <nombre-del-host> -m gather_facts`, o también en la documentación que se encuentra [aquí](https://docs.ansible.com/ansible/latest/user_guide/playbooks_vars_facts.html). 

Por defecto, Ansible siempre ejecutará el `gather_facts:`, salvo que nosotros le indiquemos que no lo haga, mediante la sentencia `gather_facts: no` a nivel del `playbook`.

```yml
- name: Este playbook no hace gather_facts 
  hosts: all
  gather_facts: no
  tasks:
    - xxxx
```

---

### Ejercicio #5 - Templates

Tomando como base el [Ejercicio #4](#ejercicio-4) modifique el rol `apache2` para que cambie el contenido de la página web por defecto del servidor, dependiendo en que `host` se encuentre ejecutando. El servidor web deberá desplegar una página similar a la siguiente:
```bash
  Este sitio web se encuentra corriendo en el nodo <host01|host02>.
  Este es el ambiente de <produccion|desarrollo>!!
```

<details>
  <summary>
Aquí puede verlo en formato HTML
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
Utilice un `template` para modificar el contenido de la página, según se encuentre en `host01 | produccion` o `host02 | desarrollo`, de forma de no tener que escribir el contenido de la página a mano dos veces.

Recuerde que ya instalamos Apache previamente en el ejercicio 4, por lo cuál no es necesario volver a instalarlo. 

Tenga en cuenta que debe iniciar los servicios de Apache en cada host para que el servidor web responda, dado que por defecto éstos se encuentran detenidos. Incluya este paso como parte del rol, para no tener que hacerlo en forma manual en cada `host`. 

El comando `service apache2 restart` inicia los servicios de apache en el equipo, pero mejor busque si no existe un módulo de Ansible específico para hacer esto!



<details>
<summary> Pista #1 </summary>
El directorio <code>document root</code> del servidor web Apache se encuentra ubicado en <code>/var/www/html/</code>, y tiene dentro el archivo <code>index.html</code>, el cuál se carga por defecto al acceder al servidor con un navegador web.
</details>

<details>
<summary> Pista #2 </summary>
Recuerde que puede definir las <code>variables</code> a utilizar en múltiples lugares del proyecto, incluyendo un archivo específico de variables, en el inventario dentro de <code>host_vars/group_vars</code>, en los directorios <code>./defaults ./vars</code> del rol, entre otros.  
</details>

<details>
<summary>Pista #3</summary>
Recuerde que es posible definir tareas dentro de un rol, en otros archivos por fuera del <code>tasks/main.yml</code>. Luego puede invocar estas tareas direcamente, mediante la opción <code>tasks_from:</code> de <code>include_role:</code> o <code>import_role:</code>.  
</details>

<details>
<summary>Pista #4</summary>
Google es (como siempre) el mejor aliado para buscar módulos específicos de Ansible, para usar en lugar de comandos de Linux. Busque algo como <code>linux service command ansible module</code> y seguro lo encontrará facilmente.  
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

## Ansible Galaxy

[Ansibe Galaxy](https://galaxy.ansible.com/) es un sitio gratuito mantenido por Red Hat que permite descargar roles desarrollados por la comunidad. Es una excelente forma de simplificar nuestros `playbooks` y poder reutilizar nuestro código, o cófigo de terceros.

Utilizando el comando `ansible-galaxy` podemos:
- Descargar roles.
- Construir templates para armar nuestros propios roles.
- Buscar roles.

Aunque es posible buscar por roles desde la consola utilizando `ansible-galaxy`, es mucho más sencillo cuando realizamos la búsqueda a través de la web.

Por ejemplo el siguiente rol instala docker en Linux: https://galaxy.ansible.com/geerlingguy/docker
Dentro del sitio podemos ver los detalles de como instalarlo. Y en `Read Me`, en general se indica información detallada del rol, como usarlo, si requiere definir variables, si tiene dependencias, etc.

Una vez que encontremos el rol, lo podemos instalar a través del comando `ansible-galaxy install`:
```
# ansible-galaxy install geerlingguy.docker
```

:point_right: Por defecto los roles descargados desde `ansible-galaxy` se instalarán en `~/.ansible/roles`. Sin embargo, podemos cambiar el directorio donde queremos que se instale utilizando la opción `-p`.

Para usar el rol en nuestra `playbook` alcanza con invocarlo como cualquier otro rol que hayamos escrito nosotros:
```yml
- hosts: all
  roles:
    - geerlingguy.docker
```


---
### Ejercicio #6: Ansible Galaxy

Tomando como base el [Ejercicio #4](#ejercicio-4) instale MySQL en el grupo de hosts `db`, utilizando un rol existente de [Ansibe Galaxy](https://galaxy.ansible.com/).


<details>
	<summary> Pista #1 </summary>
	La cantidad de roles disponibles en Ansible Galaxy es enorme. Cuando realice una busqueda en el sitio web puede utilizar los filtros disponibles (por ej. para buscar solo dentro de roles), o ingresar palabras claves adicionales para acotar la busqueda. 

  Por ejemplo en este caso pruebe de buscar: <code>mysql install role ubuntu</code>. 
  En la lista de roles que aparecen como resultado, puede ver la cantidad de veces que se descargó cada rol o el puntaje que tiene asignado, estos datos pueden ser utiles al momento de elegir cual de ellos usar. También puede seleccionar roles de determinado usuario, como por ejemplo `geerlingguy`, quien es muy conocido en la comunidad y cuyos roles hemos usado nosotros frecuentemente, en este caso: https://galaxy.ansible.com/geerlingguy/mysql
</details>

<details>
	<summary> Pista #2 </summary>
	Recuerde que debe instalar el <code>rol</code> antes de poder usarlo. Revise la documentación del rol para saber como utilizarlo, y verificar si tiene requerimientos previos como definición de variables, dependencias con otros roles, etc.
</details>

<details>
	<summary> Pista #3 </summary>
	Para invocar un <code>rol</code> descargado de Ansible Galaxy en nuestro <code>playbook</code>, puede usar los mismos módulos que utilizamos con roles escritos por nosotros mismos, como ser: <code>roles:</code>, <code>include_role:</code>, o <code>import_role:</code>.

  Verifique en la documentación del rol si requiere escalar los privilegios de usuario, aunque recuerde que en nuestro caso ya estamos corriendo todas las tareas con el usuario <code>root</code>, por lo cuál esto no sería necesario.
</details>

<details>
	<summary> Verificación </summary>
	Puede verificar si <code>mySQL</code> fue instalado correctamente en el host, conectandose al mismo con el comando <code>mysql</code>:
  <pre>
(host03) # mysql
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 9
Server version: 8.0.28-0ubuntu0.20.04.3 (Ubuntu)

Copyright (c) 2000, 2022, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
4 rows in set (0.01 sec)

mysql> quit;

</pre>


</details>

<details>
    <summary>Solución</summary>
<pre>
# ansible-galaxy install geerlingguy.mysql
Starting galaxy role install process
- downloading role 'mysql', owned by geerlingguy
- downloading role from https://github.com/geerlingguy/ansible-role-mysql/archive/3.3.2.tar.gz
- extracting geerlingguy.mysql to /root/.ansible/roles/geerlingguy.mysql
- geerlingguy.mysql (3.3.2) was installed successfully
</pre>

<pre>
# ./ejer6-playbook.yml 
- name: "Ejercicio 6 - Ansible Galaxy"
  hosts: db
  gather_facts: yes
  #become: yes           # no es necesario porque estamos corriendo como root
  tasks:
    - name: Install mysql using ansible-galaxy role 
      include_role:
        name: geerlingguy.mysql
</pre>
</details>




---
## Ansible Vault
Ref: [Encrypting content with Ansible Vault](https://docs.ansible.com/ansible/2.8/user_guide/vault.html)

A medida que creamos `playbooks` mas complejos, y comenzamos a interactuar con múltiples sistemas ya sea locales o en la nube, nos damos cuenta que comenzamos a almacenar en nuestros archivos un montó de información sensible, como usuarios, contraseñas, claves de acceso a la nube, información sensible de nuestras aplicaciones, etc.

También, es lógico y súmamente útil, comenzar a utilizar repositorios de control de versiones para nuestro código, tales como [Github](https://github.com/) que almacenan nuestro código en la nube. Pero que, dependiendo de como tengamos configurados nuestros repositorios, podrían brindar acceso público a los mismos, exponiendo así nuestra información.

Para poder resguardar la información sensible de nuestro código, Ansible nos provee de Ansible Vault, que permite cifrar nuestros archivos y así protegerlos. El comando `ansible-vault` gestiona el contenido encriptado en Ansible, y nos permite encriptar inicialmente un archivo, así como luego poder verlo, editarlo o incluso desencriptarlo.

#### Utilizando ansible-vault
Para **crear un archivo nuevo encriptado** utilizamos la opción `create` y el nombre del archivo.
Nos pedirá una contraseña, y luego nos abrirá el editor que tengamos configurado por defecto, para que ingresemos el contenido del archivo:
```
# ansible-vault create archivo-encriptado.yml
New Vault password: 
Confirm New Vault password:
```
En el editor, ingresamos un texto y salimos del mismo grabando su contenido, por ejemplo:
```
--- editor de texto ---------------------
Esta información se encuentra encriptada.
-----------------------------------------
```

Si luego intentamos ver el contenido del archivo, en encontraremos con algo del estilo:
```
# cat archivo-encriptado.yml 
$ANSIBLE_VAULT;1.1;AES256
37613739316533623030323435616439333433616161666163343730316561393535666235646665
3766653961633035363432653664373234616637636538310a623333633035353439346339623065
30343165303136326236643638646163336431653166303032616531396266653962336534636564
6464393762343665320a396333656663393062346136626333363434396539333365313738303064
37383632346363643236663062306235616231363265666333366532333237386338646138373730
3939313166353033343530323837616434336630623938346339
```

Para poder **ver el contenido** real del archivo, debemos usar la opción `view`:
```
# ansible-vault view archivo-encriptado.yml
Vault password: 
Este contenido se encuentra encriptado
```

Y para **editar el contenido**, usamos `edit` el cuál nuevamente nos abre el editor de texto por defecto para que podamos modificarlo:
```
# ansible-vault edit archivo-encriptado.yml
Vault password: 

--- editor de texto ---------------------
Este contenido se encuentra encriptado.
Le agrego otra línea.
-----------------------------------------
```

También tenemos la posibilidad de **cambiar la contraseña** de encriptación de un archivo, mediante `rekey`:
```
# ansible-vault rekey archivo-encriptado.yml
Vault password: 
New Vault password:
Confirm New Vault password:
Rekey successful
```

Para **desencriptarlo**, podemos usar la opción `decrypt`:
```
# ansible-vault decrypt archivo-encriptado.yml
Vault password: 
Decryption successful

# cat archivo-encriptado.yml
Este contenido se encuentra encriptado.
Le agrego otra línea.
```

:warning: Esto es algo que normalmente no haremos, pues deja el contenido del archivo visible nuevamente. Para ver o editar el contenido de un archivo encriptado debemos utilizar las opciones `view` o `edit` que vimos antes.

Y por último, podemos **encriptar un archivo existente**, mediante la opción `encrypt`
```
# ansible-vault encrypt archivo-encriptado.yml
New Vault password: 
Confirm New Vault password: 
Encryption successful
```



#### Utilizando archivos encriptados en nuestros playbooks
Ahora bien, hemos visto como encriptar nuestros archivos, pero como hacemos para ejecutar un `playbook` y que Ansible pueda desencriptarlo y leer su contenido? Tenemos varias opciones para esto.

La primera es **ingresando la contraseña a mano** al momento de ejecutar el `playbook`.
Esto lo hacemos agregando la opción `--ask-vault-pass` al comando `ansible-playbook`. 

Por ejemplo, el siguiente playbook copia nuestro `archivo-encriptado.yml` a los hosts `app`:
```bash
# ./vault_playbook.yml 
- name: Ejemplo de Ansible Vault
  hosts: app
  gather_facts: no
  tasks:
    - name: Copiar archivo encriptado
      ansible.builtin.copy:
        src: ~/ansible/archivo-encriptado.yml
        dest: /root/
        owner: root
        group: root
        mode: '0600'
```

Pero si intentamos ejecutarlo como siempre, nos va a dar un error, pues Ansible se da cuenta que el archivo se encuentra encriptado, y no tiene forma de abrirlo:
```
# ansible-playbook vault_playbook.yml 

PLAY [Ejemplo de Ansible Vault] ****************************************************************************************************************

TASK [Copiar archivo encriptado] ***************************************************************************************************************
fatal: [host01]: FAILED! => {"msg": "A vault password or secret must be specified to decrypt /root/ansible/archivo-encriptado.yml"}
fatal: [host02]: FAILED! => {"msg": "A vault password or secret must be specified to decrypt /root/ansible/archivo-encriptado.yml"}

PLAY RECAP *************************************************************************************************************************************
host01                     : ok=0    changed=0    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0   
host02                     : ok=0    changed=0    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0   
```

Para poder ejecutarlo, le agregamos la opción `--ask-vault-pass`, y nos pedirá que ingresemos la contraseña antes de ejecutarlo:
```
# ansible-playbook --ask-vault-pass vault_playbook.yml 
Vault password: 

PLAY [Ejemplo de Ansible Vault] ****************************************************************************************************************

TASK [Copiar archivo encriptado] ***************************************************************************************************************
changed: [host02]
changed: [host01]

PLAY RECAP *************************************************************************************************************************************
host01                     : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
host02                     : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   


```

:point_right: Tenga en cuenta que todos los archivos que utilice el `playbook` deberán estar encriptados con la misma contraseña.
.

#### Almacenando la contraseña en un archivo
Para evitar tener que ingresar a mano nuestra contraseña cada vez que utilizamos el comando `ansible-vaul`, podemos crear un archivo que contenga la misma.

:warning: El archivo con la contraseña quedará legible y en texto plano, por lo que debemos ubicarlo fuera de nuestro proyecto, y con permisos que restringan su acceso:

```
# mkdir /root/secret
echo "micontraseña" > /root/secret/vault-password
chmod 600 /root/secret/vault-password
```

:point_right: El nombre y la ubicación del archivo puede ser la que nosotros querramos. Pero el archivo debe contener únicamente la contraseña a utilizar, y solo una, si usamos varias contraseñas debemos tener varios archivos separados.

Luego podemos **pasar la ubicación del archivo de contraseña** desde línea de comando, con la opción `--vault-password-file`: 

```
# ansible-vault encrypt --vault-password-file /root/secret/vault-password archivo-encriptado.yml 
Encryption successful

# ansible-vault view --vault-password-file /root/secret/vault-password archivo-encriptado.yml 
Este contenido se encuentra encriptado
Le agrego otra línea
```

Y al momento de ejecutar nuestro `playbook`:
```
# ansible-playbook --vault-password-file=/root/secret/vault-password vault_playbook.yml 

PLAY [Ejemplo de Ansible Vault] ****************************************************************************************************************

TASK [Copiar archivo encriptado] ***************************************************************************************************************
ok: [host02]
ok: [host01]

PLAY RECAP *************************************************************************************************************************************
host01                     : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
host02                     : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```

Otra alternativa es **establecer la ubicación del archivo de contraseña en la configuración de ansible**, indicándolo en el archivo `ansible.cfg` de nuestro proyecto con la opción `vault_passord_file`:
```ìni
[defaults]
inventory = ./inventory/hosts.yml
vault_password_file = /root/secret/vault-password
```

De esta forma Ansible sabrá donde encontrar la contraseña por defecto, y no será necesario ingresarla ni referenciar el archivo a mano:
```
# ansible-vault view archivo-encriptado.yml 
Este contenido se encuentra encriptado
Le agrego otra línea
```

```
# ansible-playbook vault_playbook.yml 

PLAY [Ejemplo de Ansible Vault] ****************************************************************************************************************

TASK [Copiar archivo encriptado] ***************************************************************************************************************
ok: [host02]
ok: [host01]

PLAY RECAP *************************************************************************************************************************************
host01                     : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
host02                     : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```


También es posible pasarle a Ansible la ubicación del archivo de contraseña, **exportando una variable de entorno** de linux `ANSIBLE_VAULT_PASSWORD_FILE` con la ubicación del mismo. Por ejemplo con el comando `export ANSIBLE_VAULT_PASSWORD_FILE=/root/secret/vault-password`.



#### Encriptando variables
Cuando desplegamos una aplicación o servicio, suele ser necesario definir ciertas variables requeridas, con información sensible como ser nombres de usuarios, contraseñas, etc. 

Para encriptar estas variables, podemos por ejemplo **colocar la definición de las variables en un archivo de variables encriptadas** por separado, y encriptar todo ese archivo. Esto nos permite asegurar su contenido, pero tiene como contra que a la hora de leer nuestro código perdemos la referencia a estas variable. Es decir, como nuestro achivo de variables estará encriptado, no podremos ver fácilmente que variables hay definidas, y mucho menos cual es su valor. 

Esta opción es totalmente válida y utilizable. Solo debemos ser claros en nuestro código para indicar que esas variables son requeridas y se encuentran encriptadas. Podemos aprovechar la precedencia de variables que maneja Ansible, definir variables genéricas por ej. en nuestro `role/defaults/` para saber que las mismas existen, y definir los valores reales que utilizamos en nuestro archivo encriptado, por ejemplo en `role/vars`, que sobreescribirán a las primeras.

Recuerde que también es posible tener mas de un archivo con definición de variables, por ej., uno con las variables encriptadas, y otro con variables en texto plano cuyo contenido no es sensible.

:point_right: si trabajamos con un editor como Visual Studio Code podemos instalar una extensión que desencripta el contenido de un archivo y nos muestra el contenido legible directamente en el editor. Por ejemplo: [ansible-vault vscode](https://marketplace.visualstudio.com/items?itemName=dhoeric.ansible-vault), mediante la combinación de teclas `ctrl-alt-0` nos permite desencriptar (o encriptar) un archivo utilizando `ansible-vault` por detrás. 

Si queremos mantener el mismo archivo de variables, y colocar allí las que están encriptadas y las que no, podemos **encriptar solamente el contenido de la variable**. De esta forma, queda visible el nombre de la variable, pero no el contenido. Esto nos permite leer nuestro código de forma más facil, pero, debemos tener en cuenta que estamos igual dejando en texto plano el nombre de la variable, y asegurarnos que ese nombre no tenga información sensible.

Esto lo hacemos encriptando el contenido de la variable con `ansible-vault encrypt_string`, y luego cuando definimos la variable debempos preceder el valor encriptado con la opción `!vault`.

Por ejemplo, para definir una variable `username: root` con el contenido encriptado, hacemos:
```
# ansible-vault encrypt_string 'root' --name 'username'
username: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          30643737653162623734663334613434353063636336356234336663396136306465623031633139
          3335333161386235313166313832633337376434663135640a623063393964613334383861633439
          31653439653034643931373566313732653830653733383562343634363832653739343130313063
          3435383633333338350a306632343934363363343534663336613935653333636565346633376162
          3932
Encryption successful
```

Y luego en el archivo `.yml` donde definimos las variables, la misma se define así:
```
username: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          37303037366239653137663731636565623337653164306631363861663137623865623731393865
          6530623534653135663738613863343334626464636638320a373664633635386336373236383835
          34643938373036636266356364663831336137666336313664653466373739663166343966383738
          3635363861616463350a363664336264316330653935343939333935386434613262616533336666
          3635

```

:point_right: puede tener varias variables definidas en el mismo archivo, algunas encriptadas y otras en texto plano, según se desee. Y como siempre, dependiendo donde se definan, se aplica la precedencia de variables de Ansible, como con cualquier otra variable.

---
### Ejercicio #7  - Ansible Galaxy 

Tomando como base el [Ejercicio #6](#ejercicio-6-ansible-galaxy) configure MySQL para que solicite usuario y contraseña al intentar acceder con el comando `mysql`. 
Ni el nombre de usuario ni la contraseña deben estar visibles en nuestro código.

:point_right: Debe configurar el usuario de MySQL estableciéndole una contraseña, y configurarle como plugin de autenticación: `mysql_user_password`. Para esto puede utilizar el módulo `mysql_user` de Ansible, cuya documentación se encuentra [aquí](https://docs.ansible.com/ansible/latest/collections/community/mysql/mysql_user_module.html). 

<details>
	<summary>
		Pista #1
	</summary>
	Recuerde definir y encriptar las variables que va a utilizar, tanto para el nombre de usuario como para la contraseña. Decida si va a encriptar solo el contenido de la variables o todo el archivo con la definición de las mismas.
</details>

<details>
	<summary>
		Pista #2
	</summary>
	Cuando instaló <code>MySQL</code> se creó por defecto el usuario <code>root</code>. Debe asingarle una contraseña y cambiar el plugin de autenticación, utilizando el módulo de ansible:
  <pre>
    mysql_user:
      name: root
      password: contraseña
      plugin: mysql_native_password
      state: present
  </pre>
</details>

<details>
	<summary>
		Verificación
	</summary>
	Intente acceder a <code>mySQL</code> como hicimos antes y debería darle error: <code>Access denied</code>. 
<pre>
(host03) # mysql
ERROR 1045 (28000): Access denied for user 'root'@'localhost' (using password: YES)
</pre>

Para poder ingresar tiene que especificar usuario y contraseña:
<pre>
(host3) # mysql -u root -p
Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 17
Server version: 8.0.28-0ubuntu0.20.04.3 (Ubuntu)
(...)
</pre>
</details>

<details>
    <summary>Solución</summary>
<pre>
# ansible-vault encrypt_string 'root' --name 'mysql_user_name'
mysql_user_name: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          63373062383835633935646331356334333261316332646365353032613038613736623564613661
          3731363362396262643266353035326364646465363038330a373562336262643933663665666232
          32623334623465623339393062646366383635653939653166663534376666393164643165623230
          3161306436383831390a396534336365663962346532636531646234343434353261616461666130
          3830
Encryption successful
</pre>

<pre>
# ansible-vault encrypt_string 'nuevapass' --name 'mysql_user_password'
mysql_user_password: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          38613237613736633031373265363838383038633330333336613761373966376438616133346362
          3339303739313663376262373738396230353164303964630a323336346137623135633834666663
          31353062336164366366613430366339373764313637343165356130353764396233336464393831
          3139313035636230340a633763336538383266346536313361653562393966663161366633623761
          3065
Encryption successful
</pre>

<pre>
# ./inventory/group_vars/db.yml
mysql_user_name: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          63373062383835633935646331356334333261316332646365353032613038613736623564613661
          3731363362396262643266353035326364646465363038330a373562336262643933663665666232
          32623334623465623339393062646366383635653939653166663534376666393164643165623230
          3161306436383831390a396534336365663962346532636531646234343434353261616461666130
          3830

mysql_user_password: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          38613237613736633031373265363838383038633330333336613761373966376438616133346362
          3339303739313663376262373738396230353164303964630a323336346137623135633834666663
          31353062336164366366613430366339373764313637343165356130353764396233336464393831
          3139313035636230340a633763336538383266346536313361653562393966663161366633623761
          3065
</pre>

<pre>
- name: "Ejercicio 7 - Ansible Vault"
  hosts: db
  tasks:
      - name: configure mysql authentication
        mysql_user:
          name: '{{mysql_user_name}}'
          password: '{{mysql_user_password}}'
          plugin: mysql_native_password
          state: present

</pre>
</details>

---

[Siguiente >](./04_ansible_networking.md)
