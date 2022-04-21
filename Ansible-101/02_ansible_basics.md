
## Inventario
Ref: [How to build your inventory](https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html)

La lista de hosts sobre los cuales Ansible trabajará se almacenan en `inventarios`. Estos son archivos de texto escritos en formato `yaml` o `ini`, conteniendo las IPs o nombres de los hosts a administrar.

Por defecto, Ansible buscará el archivo de inventario en `/etc/ansible/hosts`, pero podemos especificar la ubicación del mismo durante la invocación a través del parámetro`-i <archivo_de_inventario>`.
O también se puede indicar la ubicación por defecto del inventario en la [configuración de ansible](https://docs.ansible.com/ansible/latest/reference_appendices/config.html), en un archivo `ansible.cfg`.

Ansible es capaz de tomar hosts de múltiples inventarios al mismo tiempo, y puede también construirlos de forma dinámica previo a la realización de las tareas, mediante la utilización de [inventarios dinámicos](https://docs.ansible.com/ansible/latest/user_guide/intro_dynamic_inventory.html).

En el inventario podemos crear grupos y subgrupos de equipos, lo cuál nos permitirá luego ejecutar tareas contra un grupo y que se realicen contra todos sus equipos. También podemos definir variables en el inventario, que apliquen a un host, o a grupos de hosts.

### DEMO Lab #2 - Crear un archivo de inventario

Los inventarios de Ansible pueden contener múltiples grupos, y cada host puede pertenecer a uno o más grupos.
En general, se comienza identificando un grupo llamado `all`  al cual pertenecerán todos los equipos y todos los demás grupos que definamos. Los equipos se definen como llaves de un objeto llamado `hosts`.

Vamos a definir entonces un archivo de inventario inicial para nuestro **lab**.

>Nota: puede usar el editor _vi_ o _nano_ para editar los archivos que iremos creando en el laboratorio, aunque recomendamos conectarse en forma remota al equipo `controller` mediante el editor Visual Studio Code utilizando la extensión *Remote SSH* o similar . 

En el nodo `controller` de nuestro lab, dentro de la carpeta `~/ansible/` vamos a crear nuestro archivo de inventario llamado `hosts.yml`, con el siguiente contenido:

```yaml
# archivo de inventario hosts.yml
all:
  hosts:
    host01:
    host02:
    host03:
```
>OBS: el nombre del archivo puede ser cualquiera, e incluso podemos tener multiples archivos de inventarios. Pero como mejor práctica se recomienda utilizar el nombre `hosts.yml`, y es el que utilizaremos nosotros en nuestro lab.

Cada host, o grupo, puede contar con variables especificas definidas a nivel de inventario, que pueden o bien modificar el comportamiento de Ansible o ser utilizadas luego como parte de nuestros playbooks.

Por ejemplo, vamos a agregar una variable que aplique a todos los hosts, para evitar que Ansible verifique si el host al que nos estamos conectando esta identificado como un host conocido (known_host) cuando se conecta por ssh:

```yaml
all:
  vars:
    ansible_ssh_common_args: '-o StrictHostKeyChecking=no'
  hosts:
    host01:
    host02:
    host03:
```
> OBS: tenga en cuenta la correcta indentación del archivo.

Ahora, cada vez que Ansible se quiera comunicar con cualquiera de los hosts (del grupo `all`) utilizará el argumento definido en la variable `ansible_ssh_common_args`.

La lista de variables que podemos configurar para modificar el comportamiento de Ansible se encuentran en el siguiente [link](https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html#connecting-to-hosts-behavioral-inventory-parameters).

Las variables se pueden configurar a nivel global, por grupo, o por host; y siempre se terminará aplicando la más específica.

Una de las variables que es importante tener en cuenta es `ansible_connection`. La misma especifica que método de conexión utilizará Ansible para interactuar con el host. Por defecto, intentara comunicarse a través de SSH, aunque otros métodos de conexión interesantes pueden ser por ej: `local` y `docker`.

---

### Ejercicio #1

Para conseguir realizar la conexión por SSH hacia los hosts debemos configurar el método de autenticación necesario. En este caso vamos a utilizar una llave privada de ssh, que se encuentra disponible en `~/ansible/master_key` del nodo `controller`.

Configure el inventario para que Ansible utilize la llave privada almacenada en `./master_key` para todos los hosts. 

<details>
<summary>Pista #1</summary>
El nombre de la variable a configurar es <code>ansible_ssh_private_key_file</code>.
</details>

<details>
    <summary>Solución</summary>
    <pre>
# Archivo de inventario: hosts.yml
all:
  vars:
    ansible_ssh_common_args: '-o StrictHostKeyChecking=no'
    ansible_ssh_private_key_file: './master_key'
  hosts:
    host01:
    host02:
    host03:
    </pre>
</details>

---

Para probar que efectivamente tenemos acceso a los hosts definidos en el inventario vamos a utilizar comandos `ad-hoc`. 

---

## Comandos ad-hoc
Ref: [Introduction to ad hoc commands](https://docs.ansible.com/ansible/latest/user_guide/intro_adhoc.html)

Estos son comandos sencillos, de una sola línea, que no necesitan de un archivo individual para contenerlos, o que no tenemos intención de salvarlos para el futuro. Por ejemplo: `ping`, `echo`, etc.

Los comandos `ad-hoc` se llaman a través del flag `-m` seguidos del módulo de ansible que queremos utilizar, o bien, a través del flag `-a` seguidos del comando que queremos lanzar en los hosts remotos.

Con el siguiente comando podemos realizar un ping sobre todos los hosts detallados en el inventario:
```bash
ansible -i hosts.yml all -m ping
```

>OBS: el comando anterior utiliza el módulo ping de Ansible (no el comando ping), el cuál establece una conexión por ssh hacia cada hosts, por lo cual es muy útil para verificar que la autenticación ssh esté funcionando correctamente.

También podemos ejecutar un comando directamente en los hosts, mediante:
```bash
ansible -i hosts.yml all -a 'echo "Hello, World!"'
```

Es importante identificar las comillas que envuelven el comando que ejecutará ansible a través del flag `-a`, especialmente si se quieren utilizar variables de entorno dentro del comando (las comillas simples `'` no resuelven variables, solo la hacen las comillas dobles `"`). Otro punto a tener en cuenta es que el flag `-a` no soporta comandos concatenados con un pipe (`|`). Para hacer esto tenemos que utilizar el módulo `shell`.

```bash
ansible -i hosts.yml all -m shell -a 'ifconfig eth0 | grep inet | awk "{print \$2}" '
```

El comando anterior devuelve la dirección IP de la interfaz `eth0` de cada host.

---

### Ejercicio #2

Modifique el inventario actual de manera de que cuente con dos nuevos grupos: `app` y `db`. Dentro del grupo `app` se deben incluir los hosts `host01` y `host02`. En el grupo `db` se debe incluir únicamente el host `host03`.

Verificar la configuración de inventario utilizando el módulo `ping`.

ref: [Inventory basics: formats, hosts, and groups](https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html#inventory-basics-formats-hosts-and-groups)

<details>
    <summary>Pista #1</summary>
    Utilice la llave <code>children</code> para definir subgrupos.
</details>

<details>
    <summary>Pista #2</summary>
    Para probar los grupos de hosts se puede utilizar el comando <code>ping</code> de la siguiente manera: <code>ansible -i hosts.yml app -m ping</code> o <code>ansible -i hosts.yml db -m ping</code>
</details>

<details>
    <summary>Solución</summary>
    <pre>
# archivo de inventario hosts.yml
all:
  vars:
    ansible_ssh_common_args: '-o StrictHostKeyChecking=no'
    ansible_ssh_private_key_file: './master_key'
  hosts:
    host01:
    host02:
    host03:
  children:
    app:
      hosts:
        host01:
        host02:
    db:
      hosts:
        host03:
  </pre>
  </details>
<details>
  <summary>Verificación</summary>
  <pre>
# ansible -i hosts.yml app -m ping
host02 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}
host01 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}
</pre>
<pre>
# ansible -i hosts.yml db -m ping
host03 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}
</pre>
</details>

---

Utilizando los comandos `ad-hoc` podemos realizar una gran cantidad de tareas sobre múltiples hosts en simultáneo. Por ejemplo, utilizando el módulo `file` podemos compartir archivos, o podemos instalar aplicaciones utilizando los módulos `apt` o `yum` según la distribución de linux que utilicemos.

```
# APT - Ubuntu
ansible -i hosts.yml app -m apt -a "name=jq state=present"

# YUM - CentOS
ansible -i hosts.yml app -m yum -a "name=jq state=present"
```

Otros posibles usos son:
- Creación de usuarios
- Clonar repositorios utilizando `git`
- Administrar servicios remotos
- Lanzar operaciones
- Apagar o reiniciar equipos
- Recopilar información

Este último es particularmente útil, podemos ejecutarlo mediante el siguiente comando:
```bash
ansible -i hosts.yml all -m setup
```


## Aplicaciones

Por ahora solo hemos utilizado la aplicación `ansible`, sin embargo, no es la única disponible, tenemos otras como:

- `ansible`
  - Herramienta simple para correr una tarea en múltiples hosts remotos.
- `ansible-config`.
  - Herramienta para configurar Ansible.
  - `ansible-config list`
- `ansible-console`.
  - Un REPL para ejecutar múltiples tareas sobre un grupo de hosts.
  - `ansible-console -i hosts.yml all`
- `ansible-doc`.
  - Muestra información sobre los módulos de ansible instalados.
  - `ansible-doc ping`
  - `ansible-doc ping -s`
- `ansible-galaxy`.
  - Maneja roles compartidos en repositorios de terceros. Por defecto buscara los repositorios en [https://galaxy.ansible.com](https://galaxy.ansible.com).
- `ansible-inventory`.
  - Util para validar el inventario con el que estamos trabajando.
  - `ansible-inventory -i hosts.yml --list`
  - `ansible-inventory -i hosts.yml --graph`
- `ansible-playbook`.
  - Aplicación capaz de ejecutar Ansible `playbooks`.
- `ansible-pull`.
  - Invierte el proceso de ejecución de `push` a `pull`.
- `ansible-vault`.
  - Aplicación capaz de encriptar cualquier estructura de datos a utilizar por ansible.
  - `ansible-vault create secret.yml`
  - `ansible-vault edit secret.yml`
  - `ansible-vault encrypt sin_encriptar.yml`

Durante el resto del curso nos enfocaremos en `ansible-playbook` y mencionaremos alguna de las otras aplicaciones cuando corresponda, por ej.`ansible-vault`.

## Ansible playbooks
Ref: [Intro to playbooks](https://docs.ansible.com/ansible/latest/user_guide/playbooks_intro.html)


Si bien los comandos ad-hoc son útiles para operaciones simples, no son adecuados para escenarios mas complejos, como ser tareas de configuración de equipos, deploy de nuevos sericios, orquestación en la nube, etc. Para estos casos utilizaremos `playbooks`.

Los `playbooks` son archivos que describen lo que queremos hacer, es decir, las tareas que queremos ejecutar sobre los hosts administrados. Además de declarar configuraciones, los `playbooks` se pueden utilizar para orquestar cambios masivos en múltiples equipos de forma ordenada. 

El objetivo del `playbook` es el de mapear un grupo de hosts con los módulos de ansible que queremos ejecutar, a través de una lista de tareas. Cada una de estas uniones dentro de un `playbook` se denomina `play`. Una `task` es la mínima acción que se puede ejecutar sobre el host, esto es en general, la llamada a un módulo de ansible.

Un `playbook` puede contener múltiples `plays`, y un `play` puede contener múltiples `tasks`.

Los `playbooks` se escriben en archivos en formato `yaml` como una lista de `plays`. Cada `play` debe tener al menos una `task` y debe especificar el grupo o la lista de hosts sobre el cual Ansible deberá trabajar.

A continuación podemos ver un ejemplo de un `playbook`, que cuenta con dos `plays`. El primero se aplicará sobre los `hosts: webservers` y el segundo sobre los `hosts: databases`. Cada `play` tiene un conjunto de `tasks`, que son en definitiva, las operaciones que se ejecutarán sobre los `hosts`.
```yaml
- name: Update web servers
  hosts: webservers
  remote_user: root

  tasks:
  - name: Ensure apache is at the latest version
    ansible.builtin.yum:
      name: httpd
      state: latest
  - name: Write the apache config file
    ansible.builtin.template:
      src: /srv/httpd.j2
      dest: /etc/httpd.conf

- name: Update db servers
  hosts: databases
  remote_user: root

  tasks:
  - name: Ensure postgresql is at the latest version
    ansible.builtin.yum:
      name: postgresql
      state: latest
  - name: Ensure that postgresql is started
    ansible.builtin.service:
      name: postgresql
      state: started

```
### Tareas

Las tareas dentro del `playbook` son ejecutadas en el orden en que se definieron, de a una, contra todos los sistemas especificados en la lista de `hosts`. Si alguno de los `plays` falla para un host, el mismo se elimina de la lista para las siguientes tareas. Una vez corregido el error, se puede lanzar el `playbook` de nuevo, y Ansible se encargará de realizar las modificaciones en aquellos hosts que fallaron.

Se sugiere que cada tarea tenga un nombre, especificado bajo la clave `name`. Estos nombres aparecerán en la consola durante la ejecución del `playbook` y ayudan a debuguear su funcionamiento. 

Si no nos importa que algún comando falle podemos configurar la opción `ignore_error`. 


### Variables del `play`
Podemos setear ciertas variables a nivel del play, para modificar el comportamiento del mismo.

Una de las variables que es usual configurar es el nombre del usuario remoto con el cual se ejecutarán las tareas en el host. Esto se define con la variable `remote_user:`

```yaml
- hosts: all
  remote_user: ubuntu
  tasks:
    # ...
```

En nuestro caso utilizaremos el usuario `root`, que es además el valor por defecto que utiliza Ansible.

Si las tareas que queremos realizar necesitan de permisos elevados, podemos utilizar la opción `become`. Esta opción, en conjunto con la opción `become_user`,  permite cambiar de usuario durante la ejecución de la tarea. Para especificar el método con el cual necesitamos escalar los permisos lo hacemos con la opción `become_method`.

```yaml
- hosts: all
  become: yes
  become_user: root
  become_method: su
  tasks:
    # ...
```



### Creando el primer playbook
Comencemos creando un playbook muy simple, que hace un `ping` al grupo de hosts `app` que tenemos definido en nuestro inventario.

Para esto, crear un archivo `primer-playbook.yml` con el siguiente contenido:
```yaml
# primer_playbook.yml
- name: Primer playbook
  hosts: app
  tasks:
    - ping:
```

Para correr un `playbook` utilizamos el comando `ansible-playbook`, al cuál podemos pasarle el inventario queremos utilizar (luego veremos otra forma de especificar el inventario):

```bash
ansible-playbook -i hosts.yml playbook.yml
```

Si queremos comprobar que la sintaxis de nuestro `playbook` no tiene errores podemos utilizar el flag `--syntax-check`. Y, si queremos ver con más detalles las acciones que esta realizando Ansible para detectar errores (debug), podemos correrlo con el comando con el flag `--verbose`.


Ejecutemos entonces nuestro playbook:
```
# ansible-playbook -i hosts.yml primer-playbook.yml

PLAY [Primer playbook] ****************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************************************
ok: [host02]
ok: [host01]

TASK [ping] ************************************************************************************************************************************
ok: [host02]
ok: [host01]

PLAY RECAP *************************************************************************************************************************************
host01                     : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
host02                     : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

```

Si observamos la salida, podemos ver que la tarea se ejecutó en `host01`y `host02`lo cuál es correcto de acuerdo a nuestro inventario. Y sobre el final podemos ver un resumen de la ejecución, donde indica que se realizaron 2 tareas en forma correcta en cada equipo (ok=2), no se realizaron cambios en los equipos (changed=0), y no hubo errores (failed=0), además información adicional.

En el caso de que queramos correr múltiples tareas en un mismo `play`, podemos hacerlo, dado que el comando `tasks` consume una lista de tareas:
```yaml
# primer_playbook.yml
- name: Primer playbook
  hosts: app
  tasks:
    - ping:
    - ansible.builtin.user:
        name: user1
```

Al ejecutarlo:
```
# ansible-playbook -i hosts.yml primer-playbook.yml

PLAY [Primer playbook] ****************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************************************
ok: [host01]
ok: [host02]

TASK [ping] ************************************************************************************************************************************
ok: [host02]
ok: [host01]

TASK [ansible.builtin.user] ********************************************************************************************************************
changed: [host02]
changed: [host01]

PLAY RECAP *************************************************************************************************************************************
host01                     : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
host02                     : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
 
```

En este caso podemos ver que se realizaron cambios en los hosts (changed=1) dado que se creó el usuario *user1*.

Dentro de cada tarea se pueden configurar opciones adicionales que modifican su comportamiento como: condicionales, loops, registros de salida, etc. A continuación mencionaremos algunas de las más importantes.


## Estructura de directorios para las paybooks
A medida que los `playbooks` crecen en complejidad, es necesario crear una estructura de directorios que nos permita ubicar los diferentes componentes (tareas, roles, variables, inventarios, etc.) en forma ordenada.

Existen ejemplos de mejores prácticas para dicha estructura, como el que se  puede encontrar [aquí](
https://docs.ansible.com/ansible/latest/user_guide/sample_setup.html#sample-directory-layout).

En nuestro **lab**, comenzarmos por colocar los `playbooks` en el directorio `~/ansible`, e iremos creando las estructuras de directos necesarias a medida que avancemos. A medida que vayamos avanzando lo iremos indicando.

``` bash
# estructura del lab en ~/ansible
primer_playbook.yml
```

## Ansible Config
Ref: [Configuring Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_configuration.html)

Aunque podemos indicarle a Ansible donde buscar el inventario cada vez que ejecutamoso un `playbook`, este proceso se vuelve tedioso rapidamente. Además, existe un sinfin adicional de comportamientos de Ansible que podemos querer modificar, dependiendo del tipo de proyecto en el que estemos trabajando. 

Ansible expone un archivo de configuración donde podemos definir su comportamiento, como por ejemplo, la ubicación del inventario, y así no tener que pasarselo por línea de comando.

Por defecto, Ansible buscará el archivo de configuración de la siguiente manera, y con esta precedencia:
1. En base a la configuración de la variable de entorno `ANSIBLE_CONFIG`.
2. Dentro del directorio donde se esta ejecutando Ansible, en un archivo llamado `ansible.cfg`.
3. En el directorio del usuario que ejecuta Ansible, bajo el nombre `~/.ansible.cfg`.
4. En la ubicación `/etc/ansible/ansible.cfg`.

>OBS: Recomendamos acompañar todos los proyectos de Ansible con un archivo de configuración `ansible.cfg` en el directorio raiz del proyecto. De esta manera podemos saber exactamente que configuraciones estamos aplicando, y tener diferentes configuraciones para diferentes proyectos.


Para nuestro **lab** creamos entonces el archivo `ansible.cfg` en nuestro directorio raiz `~/ansible`, con el siguiente contenido:
```YML
# archivo de configuración ansible.cfg
[defaults]
inventory = ./inventory/hosts.yml
```

Y creamos la siguiente estructura de directorios:
``` bash
# estructura del lab en ~/ansible
inventory/
  hosts.yml
ansible.cfg
primer_playbook.yml
```

<details>
    <summary>Comandos linux</summary>
    <pre>
# cd ~/ansible
# mkdir inventory
# mv hosts.yml inventory
  </pre>
  </details>

Ahora, cuando ejecutemos nuestro `primer_playbook.yml` no será necesario pasarle el inventario con el flag `-i`, sino que por defecto lo tomará desde `./inventory/hosts.yml`.

```
# ansible-playbook primer-playbook.yml

PLAY [Primer playbook] ****************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************************************
ok: [host01]
ok: [host02]

TASK [ping] ************************************************************************************************************************************
ok: [host02]
ok: [host01]

TASK [ansible.builtin.user] ********************************************************************************************************************
ok: [host02]
ok: [host01]

PLAY RECAP *************************************************************************************************************************************
host01                     : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
host02                     : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```

En el archivo `ansible.cfg` podemos definir muchas configuraciones que afectan el comportamiento de Ansible.
A modo de ejemplo, algunas que nosotros solemos utilizar (aunque esto depende de cada proyecto) son:

```
[defaults]
inventory = ./inventory/hosts.yml
host_key_checking = False
command_warnings = False
deprecation_warnings = False
remote_tmp = ~/.ansible/tmp
display_skipped_hosts = False
stdout_callback = yaml
callback_whitelist  = profile_tasks
```


### Variables
Ref: [Using Variables](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html)

Algo muy útil y potente es poder utilizar variables para almacenar valores que luego sean consumidos en nuestros `Playbooks`. Ansible sustuye la variable por su valor al momento de ejecutar la tarea. Las variables se pueden definir en múltiples lugares, y dependiendo donde se haga, tendrán precedencia unas sobre las otras.

Las variables se definen en forma de clave-valor, por ej:
  ```yaml
  mi_variable: valor
  ```
y se referencian colocando el nombre de la variable entre llaves dobles:
  ```yaml
  Este es el contenido de {{mi_variable}}
  ```

Las variables y sus valores se pueden definir en múltiples lugares, por ejemplo: en el inventario, en archivos específicos de variables, dentro de los `roles` (lo veremos mas adelante), o incluso pasarlas por línea de comando al ejecutar `ansible-playbook`, etc.

>OBS: las variables pueden definirse en múltiples lugares, lo cual si bien brinda mucha flexibilidad a la hora de escribir los playbooks, en proyectos grandes puede generar complejidad a la hora de mantener el código o hacer debug de errores.

#### Variables definidas en un archivo específico
Una opción simple es utilizar un archivo de variables general, donde podamos definir todas las variables que necesitemos para nuestro proyecto.

``` bash
# estructura del lab en ~/ansible
inventory/
  hosts.yml
vars/
  variables.yml
ansible.cfg
primer_playbook.yml
```

```yaml
# Archivo ./vars/variables.yml
application_path: /opt/my_app
```

Y en  nuestro `playbook` incluimos este archivo mediante `var_files`:
```yaml
# primer_playbook.yml
- name: Primer playbook
  hosts: app
  vars_files:
    - ./vars/variables.yml
  tasks:
    - ping:
    - ansible.builtin.user:
        name: user1
    - debug:
        msg: "La aplicación se encuentra instalada en {{application_path}}"
```

:point_right: el módulo `debug:` de Ansible permite desplegar información como parte de la salida del playbook. Podemos desplegar el contenido de una variable con `var:`, o como en este caso, el mensaje que querramos con `msg:`. Puede ver la documentación del módulo [aquí](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/debug_module.html).


Al correr el playbook anterior, podemos ver que la variable `application_path` es sustituida por su valor `/opt/my_app`:
```
# ansible-playbook primer_playbook.yml 

PLAY [Primer playbook] *************************************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************************************
ok: [host01]
ok: [host02]

TASK [ping] ************************************************************************************************************************************
ok: [host01]
ok: [host02]

TASK [ansible.builtin.user] ********************************************************************************************************************
ok: [host01]
ok: [host02]

TASK [debug] ***********************************************************************************************************************************
ok: [host01] => {
    "msg": "La aplicación se encuentra instalada en /opt/my_app"
}
ok: [host02] => {
    "msg": "La aplicación se encuentra instalada en /opt/my_app"
}

PLAY RECAP *************************************************************************************************************************************
host01                     : ok=4    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
host02                     : ok=4    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```



#### Variables definidas en el inventario
Podemos definir variables particulares para nuestros hosts o grupos, dentro del propio archivo de inventario.

```yml
# archivo de inventario ./inventory/hosts.yml
all:
  vars:
    ansible_ssh_common_args: '-o StrictHostKeyChecking=no'
    ansible_ssh_private_key_file: './master_key'
  hosts:
    host01:
    host02:
    host03:
  children:
    app:
      vars:
        application_name: prod_app
      hosts:
        host01:
        host02:
    db:
      hosts:
        host03:
```

Pero, **la práctica recomendada para proporcionar variables en el inventario** es definirlas en archivos ubicados en dos directorios específicos, denominados `host_vars` y `group_vars`:

Por ejemplo, para definir variables para nuestro grupo de hosts `app`, creamos el archivo `group_vars/app.yml` con las definiciones de variables (notese que el nombre del archivo coincide con el nombre del grupo de hosts).
Si queremos en cambio definir variables que apliquen a un único host, por ej. al `host01`, lo hacemos creando el archivo `host_vars/host01.yml` con las definiciones de variables.

>OBS: las variables de `host` siempre tienen prioridad sobre las variables de `group`, puede encontrar más infromación sobre la precedencia en la definición de variables [aquí](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#understanding-variable-precedence).


Creamos los directorios `host_vars` y `group_vars` en nuestro proyecto, dentro de la carpeta `inventory`:
``` bash
# estructura del lab en ~/ansible
inventory/
  host_vars/
    host01.yml
  group_vars/
    app.yml
  hosts.yml
vars/
  variables.yml
ansible.cfg
primer_playbook.yml
```

```yaml
# Archivo ./host_vars/host01.yml
application_env: produccion
```

```yaml
# Archivo ./group_vars/app.yml
envirapplication_env: desarrollo
```

Y en  nuestro `playbook`:
```yaml
# primer_playbook.yml
- name: Primer playbook
  hosts: app
  vars_files:
    - ./vars/variables.yml
  tasks:
    - ping:
    - ansible.builtin.user:
        name: user1
    - debug:
        msg: 
          - "La aplicación {{application_name}} se encuentra instalada en {{application_path}}"
          - "El ambiente para este equipo es: {{application_env}}"
```

:point_right: la opción `msg:` del módulo `debug:` acepta una lista de mensajes a desplegar, puede verlo [aquí](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/debug_module.html).


Luego al correr el playbook, podemos ver la precedencia que se aplica de `host_vars` sobre `group_vars`:
```
ansible-playbook primer_playbook.yml 

PLAY [Primer playbook] *************************************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************************************
ok: [host01]
ok: [host02]

TASK [ping] ************************************************************************************************************************************
ok: [host02]
ok: [host01]

TASK [ansible.builtin.user] ********************************************************************************************************************
ok: [host01]
ok: [host02]

TASK [debug] ***********************************************************************************************************************************
ok: [host01] => {
    "msg": [
        "La aplicación prod_app se encuentra instalada en /opt/my_app",
        "El ambiente para este equipo es: produccion"
    ]
}
ok: [host02] => {
    "msg": [
        "La aplicación prod_app se encuentra instalada en /opt/my_app",
        "El ambiente para este equipo es: desarrollo"
    ]
}

PLAY RECAP *************************************************************************************************************************************
host01                     : ok=4    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
host02                     : ok=4    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

```


#### Variables definidas en el `playbook`
También podemos definir variables en diferentes lugares de nuestro `playbook`:

```yml
# primer_playbook.yml
- name: Primer playbook
  hosts: app
  vars_files:
    - ./vars/variables.yml
  vars:
    - application_owner: conatel
  tasks:
    - ping:
    - ansible.builtin.user:
        name: user1
    - set_fact:
        application_doc: "www.{{application_name}}.com/{{application_env}}/help"
    - debug:
        msg: 
          - "La aplicación {{application_name}} se encuentra instalada en {{application_path}}"
          - "El ambiente para este equipo es: {{application_env}}"
          - "El dueño de la aplicación es {{application_owner}} y corre en {{application_pod}}"
          - "Puede acceder a la documentación en: {{application_doc}}"
      vars:
        - application_pod: pod-1
```

En este caso estamos:
  - cargando el archivo de variables `./vars/variables.yml` a nivel del `playbook`
  - definiendo la variable `application_owner` también a nivel del `playbook`
  - definiendo la variable `application_doc` a nivel del `play`, utilizando el módulo `ansible_facts:`
  - definiendo la varialbe `application_pod` a nivel de la `task` final `debug:`

:point_right: también puede definir variables dentro del mismo código, utilizando el módulo `sect_facts:` cuya documentación se encuenta [aquí](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/set_fact_module.html#examples)




```
(controller) # ansible-playbook primer_playbook.yml 

PLAY [Primer playbook] *************************************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************************************
ok: [host01]
ok: [host02]

TASK [ping] ************************************************************************************************************************************
ok: [host02]
ok: [host01]

TASK [ansible.builtin.user] ********************************************************************************************************************
ok: [host02]
ok: [host01]

TASK [set_fact] ********************************************************************************************************************************
ok: [host01]
ok: [host02]

TASK [debug] ***********************************************************************************************************************************
ok: [host01] => {
    "msg": [
        "La aplicación prod_app se encuentra instalada en /opt/my_app",
        "El ambiente para este equipo es: produccion",
        "El dueño de la aplicación es conatel y corre en pod-1",
        "Puede acceder a la documentación en: www.prod_app.com/produccion/help"
    ]
}
ok: [host02] => {
    "msg": [
        "La aplicación prod_app se encuentra instalada en /opt/my_app",
        "El ambiente para este equipo es: desarrollo",
        "El dueño de la aplicación es conatel y corre en pod-1",
        "Puede acceder a la documentación en: www.prod_app.com/desarrollo/help"
    ]
}

PLAY RECAP *************************************************************************************************************************************
host01                     : ok=5    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
host02    
```

### Registros de salida
Todas las tareas que ejecuta Ansible, emiten por defecto una salida, en donde se incluye información general sobre la ejecución de la misma, más el mensaje generado por el módulo durante su ejecución. Sin embargo, esta salida no puede ser accedida a menos que se indique específicamente, mediante la opción `register`.

```yaml
# segundo_playbook.yml
- name: Ejemplo de como utilizar la opción 'register'
  hosts: localhost
  connection: local
  gather_facts: no
  tasks:
    - shell: echo Hola
      register: result
    - debug:
        var: result
```
La opción `register` almacena la salida de la tarea `shell` en una variable de entorno llamada `result`. Si bien este nombre de variable es típicamente utilizado con este fin, podemos usar cualquier otro nombre de variable que querramos. 

Luego, usamos el módulo `debug:` pero ahora con la opción `var:`, que despliega el contenido de dicha variable.


```
# ansible-playbook segundo-playbook.yml

PLAY [Ejemplo de como utilizar la opción 'register'] *******************************************************************************************

TASK [shell] ***********************************************************************************************************************************
changed: [localhost]

TASK [debug] ***********************************************************************************************************************************
ok: [localhost] => {
    "result": {
        "changed": true,
        "cmd": "echo Hola",
        "delta": "0:00:00.002527",
        "end": "2022-03-25 13:40:48.141851",
        "failed": false,
        "msg": "",
        "rc": 0,
        "start": "2022-03-25 13:40:48.139324",
        "stderr": "",
        "stderr_lines": [],
        "stdout": "Hola",
        "stdout_lines": [
            "Hola"
        ]
    }
}

PLAY RECAP *************************************************************************************************************************************
localhost                  : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```

:point_right: Note que este playbook lo estamos ejecutando contra `localhost`, o sea, contra el mismo nodo *controller* y por tanto no está utilizando el inventario que tenemos definido.

Guardar la salida resultante de la ejecución de un módulo puede ser necesario en muchos casos. Por ejemplo, si está utilizando un playbook para desplegar una máquina virtual en la nube, el módulo le devolverá información que seguramente necesite mas adelante, como la dirección IP que le asignó a la misma. 

Pero aunque muchas veces es necesario o recomendable almacenar esta información, no siempre es necesario desplegarla, para evitar sobrecargar la salida standard de nuestro `playbook` a pantalla.

---

### Debug

Guardar la salida resultante de la ejecución de un módulo puede ser útil también cuando estamos haciendo debug de nuestro código. Dado que nos permite ver información adicional que nos ayude a encontrar un problema.

Otra opción que tenemos para hacer debug, es correr nuestro playbook en modo `verbose`, esto lo hacemos como se indica [aquí](https://docs.ansible.com/ansible/latest/cli/ansible-playbook.html#cmdoption-ansible-playbook-v). 

Pruebe de correr el playbook anterior de esta forma: `ansible-playbook primer-playbook.yml --verbose` y revise la salida que produce. Luego aumente el nivel de información con `-vv` o `-vvv` y vea las diferencias.



---
### Condicionales
Ref: [Conditionals](https://docs.ansible.com/ansible/latest/user_guide/playbooks_conditionals.html)

Como comentamos antes, Ansible esta desarrollado sobre Python, pero las configuraciones se realizan a través de documentos escritos en YAML para simplificar su escritura. Sin embargo, el hecho de contar con Python trabajando detrás de escena, nos permite incorporar funcionalidades más avanzadas a nuestros `playbooks`. Los condicionales son uno de ellos.
`
Mediante la utilización de la opción `when:` en la definición de una tarea, podemos hacer que solo se ejecute la misma cuando se cumpla una determinada condición. El contenido de la opción `when` es una sentencia condicional de Python valida, que puede referenciar variables definidas de forma dinámica o estática.

Por ejemplo, si queremos generalizar una tarea para que se ejecute tanto en servidores Ubuntu como en CentOS, podemos agregar un condicional `when:`, de forma de poder invocar al módulo de ansible correcto dependiendo de cuál sea el sistema operativo del host.

```yaml
# tercer_playbook.yml
# OBS: la variable `ansible_os_family` es resuelta por Ansible previo a 
#      la ejecución de las tareas en el host (Gathering Facts).
- name: Ejemplo, instalar `jq` con `apt` en Ubuntu y con `yum` en CentOS
  hosts: app
  tasks:
    - name: Instalar `jq` en Ubuntu con apt
      apt:
        name: jq
        update_cache: yes
      when: ansible_os_family == 'Debian'

    - name: Instalar `jq` en CentOS con yum
      yum:
        name: jq
        state: latest
      when: ansible_os_family == 'RedHat'
```

Ejecutamos el playbook:
```
# ansible-playbook tercer_playbook.yml

PLAY [Ejemplo, instalar `jq` con `apt` en Ubuntu y `yum` en CentOS] ****************************************************************************

TASK [Gathering Facts] *************************************************************************************************************************
ok: [host02]
ok: [host01]

TASK [Instalar `jq` en Ubuntu con apt] *********************************************************************************************************
ok: [host02]
ok: [host01]

TASK [Instalar `jq` en CentOS con yum] *********************************************************************************************************
skipping: [host01]
skipping: [host02]

PLAY RECAP *************************************************************************************************************************************
host01                     : ok=2    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0   
host02                     : ok=2    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0   


```

Al ejecutarlo, podemos ver una tarea inicial llamada `[Gathering Facts]`. 

Esta tarea es ejecutada siempre por Ansible (salvo que le indiquemos no hacerlo) para obtener información relevante de los `hosts` donde va a correr. Entre dicha información, se obtiene por ejemplo la familia de sistema operativo del host, la cuál la devuelve en la variable `ansible_os_family`. Esta es la variable que utilizamos nosotros luego en la sentencia `when` para chequear sobre que sistema operativo estamos ejecutando. 

Podemos ver entonces, que la tarea de instalación fue ejecutada para Ubuntu pero fue salteada (`skipping`) para CentOS, dado que ninguno de nuestros hosts del laborotorio tiene CentOS instalado.

---
### Iteraciones
Ref: [Loops](https://docs.ansible.com/ansible/latest/user_guide/playbooks_loops.html)

También podemos realizar iteraciones en el código utilizando la sentencia `loop`.

La opción `loop` toma una `lista` y ejecuta la tarea para cada uno de los elementos de la misma. Utilizamos la variable `item` para referenciar a los elementos de la lista durante la ejecución del loop.

```yaml
# ---
# Ejemplo de como utilizar loop en un playbook de Ansible
# ...
- name: Imprimir todos los elementos de la lista de a uno
  hosts: localhost
  connection: local
  gather_facts: no
  tasks:
    - debug:
        msg: '{{item}}'
      loop:
        - uno
        - dos
        - tres
```

:warning: no es conveniente definir nosotros variables con el nombre `item` porque la misma por defecto será reemplazada cuando se utilicen loops. Si es necesario, podemos indicarle al loop que utilice otra variable con diferente nombre, revise la documentación para ver como hacerlo.

Los elementos de cada lista pueden ser valores un poco más complejos, como otras listas o diccionarios. Por ejemplo:

```yaml
- name: Ejemplo de como utilizar loop en un playbook de Ansible
  hosts: localhost
  connection: local
  gather_facts: no
  tasks:
    - debug:
        msg: 'Nombre: {{item.name}} - Grupo: {{item.groups}}'
      loop:
        - { name: 'testuser1', groups: 'wheel' }
        - { name: 'testuser2', groups: 'root' }
```
En este caso, iteramos sobre una `lista` donde cada elemento es un `diccionario`, el cuál tiene dentro dos llaves (name y groups) con sus valores. En este caso, al iterar sobre el diccionario accedo al valor mediante `item.clave.

#### until loops
Ref: [Retrying a task until a condition is met](https://docs.ansible.com/ansible/latest/user_guide/playbooks_loops.html#retrying-a-task-until-a-condition-is-met)

Otro tipo de iteración que podemos realizar es `until` loops. Este tipo de loop es utilizado para reintentar una tarea hasta que se cumpla cierta condición.

Para utilizar este loop se necesitan básicamente tres argumentos en la tarea:
- `until`: condición que se debe cumplir para que el loop finalice. Ansible va a continuar ejecutando la tarea hasta que la expresión utilizada para evaluar el loop se cumpla: `true`.
- `retry`: cuantas veces queremos correr la tarea antes de que Ansible se rinda y la de por terminada (sin que se cumpla la condición anterior).
- `delay`: el tiempo de espera, en segundo,s entre cada reintento de la tarea.

Por ejemplo, la siguiente tarea va a consultar una aplicación en determinada URL, hasta que la misma responda con un código 200 (OK). Ansible va a realizar 10 intentos en total, con una demora de 1 segundo entre cada intento. Si dentro de esos intentos la aplicación responde con código 200, el loop finaliza y se continua con la siguiente tarea. Pero si luego de los 10 intentos la respuesta sigue sin ser "200", el loop finaliza con error y la tarea devolverá un `fail`.

```yaml
  - name: Wait until web app status is "READY"
    uri:
      url: "{{ app_url }}/status"
    register: result
    until: result.status = 200
    retries: 10
    delay: 1
```

>OBS: esta tarea se muestra a modo de ejemplo para explicar el uso de `loop`, no podrá ejecutarla en el laboratorio dado que no contamos con la aplicación (URL) que devuelva el `status` necesario.

### Ejercicio #3

Cree un playbook para instalar SQLite3 y su paquete de desarrollo en los hosts identificados como `db`.   

<details>
    <summary>Pista 1</summary>
    Los paquetes a instalar son: <code>sqlite3</code> y <code>libsqlite3-dev</code>
</details>
<details>
    <summary>Pista 2</summary>
    El módulo para instalar paquetes en Ubuntu es <code>apt</code>
</details>
<details>
    <summary>Solución</summary>
    <pre>
# ejer3_playbook.yml
- hosts: db
  tasks:
    - name: Install SQLite
      apt: 
        name: sqlite3 
        state: latest
        update_cache: yes
    - name: Install SQLite dev package
      apt:
        name: libsqlite3-dev
        state: latest
        update_cache: yes
</pre>
</details>

<details>
    <summary>Solución alternativa</summary>
    <pre>
# ejer3_playbook.yml
- hosts: db
  tasks:
    - name: Install software
      apt:
        name: '{{item}}'
        state: latest
        update_cache: yes
      loop:
        - sqlite3
        - libsqlite3-dev
</pre>
</details>

<details>
    <summary>Verificación</summary>
    <pre>
# ansible-playbook ejer3_playbook.yml 

PLAY [db] **************************************************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************************************
ok: [host03]

TASK [Install software] ************************************************************************************************************************
changed: [host03] => (item=sqlite3)
changed: [host03] => (item=libsqlite3-dev)

PLAY RECAP *************************************************************************************************************************************
host03                     : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
</pre>
</details>

---



[Siguiente >](./03_ansible_codigo.md)
