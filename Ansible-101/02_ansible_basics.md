
## Inventario
Ref: [How to build your inventory](https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html)

La lista de hosts sobre los cuales Ansible trabajará se almacenan en `inventarios`. Estos son archivos de texto escritos en formato `yaml` o `ini`, conteniendo las IPs o nombres de los hosts a administrar.

Por defecto, Ansible buscará el archivo de inventario en `/etc/ansible/hosts`, pero podemos especificar la ubicación del mismo durante la invocación a través del parámetro`-i <archivo_de_inventario>`.
O también se puede indicar la ubicación por defecto del inventario en la [configuración de ansible](https://docs.ansible.com/ansible/latest/reference_appendices/config.html), en un archivo `ansible.cfg`.

Ansible es capaz de tomar hosts de múltiples inventarios al mismo tiempo, y puede también construirlos de forma dinámica previo a la realización de las tareas, mediante la utilización de [inventarios dinámicos](https://docs.ansible.com/ansible/latest/user_guide/intro_dynamic_inventory.html).

En el inventario podemos crear grupos y subgrupos de equipos, lo cuál nos permitirá luego ejecutar tareas contra un grupo y que se realicen contra todos sus equipos. También podemos definir variables en el inventario, que apliquen a un host, o a grupos de hosts.

### DEMO Lab #2 - Crear un archivo de inventario

Los inventarios de Ansible pueden contener múltiples grupos, y cada host puede pertenecer a uno o más grupos.
En general, se comienza identificando un grupo llamado `all`  al cual pertenecerán todos los equipos y todos los demás grupos que definamos. 
Los equipos se definen como llaves de un objeto llamado `hosts`.

Vamos a definir entonces un archivo de inventario inicial.
Para esto, conectados al nodo `controller` de nuestro lab, dentro de la carpeta `/root/ansible/` vamos a crear un nuevo archivo llamado `inventory.yml` con el siguiente contenido:

```yaml
all:
  hosts:
    host01:
    host02:
    host03:
```
>OBS: puede usar el editor _vi_ o _nano_ para editar los archivos, aunque recomendamos conectarse en forma remota al equipo mediante el editor Visual Studio Code. 


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
# inventory.yml
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
ansible -i inventory.yml all -m ping
```

>OBS: el comando anterior utiliza el módulo ping de Ansible (no el comando ping), el cuál establece una conexión por ssh hacia cada hosts, por lo cual es muy útil para verificar que la autenticación ssh esté funcionando correctamente.

También podemos ejecutar un comando directamente en los hosts, mediante:
```bash
ansible -i inventory.yml all -a 'echo "Hello, World!"'
```

Es importante identificar las comillas que envuelven el comando que ejecutará ansible a través del flag `-a`, especialmente si se quieren utilizar variables de entorno dentro del comando (las comillas simples `'` no resuelven variables, solo la hacen las comillas dobles `"`). Otro punto a tener en cuenta es que el flag `-a` no soporta comandos concatenados con un pipe (`|`). Para hacer esto tenemos que utilizar el módulo `shell`.

```bash
ansible -i inventory.yml all -m shell -a 'ifconfig eth0 | grep "inet addr" | cut -d: -f2 | awk "{print $1}"'
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
    Para probar los grupos de hosts se puede utilizar el comando <code>ping</code> de la siguiente manera: <code>ansible -i inventory.yml app -m ping</code> o <code>ansible -i inventory.yml db -m ping</code>
</details>

<details>
    <summary>Solución</summary>
    <pre>
# inventory.yml
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
# ansible -i inventory.yml app -m ping
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
# ansible -i inventory.yml db -m ping
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
ansible -i inventory.yml app -m apt -a "name=jq state=present"

# YUM - CentOS
ansible -i inventory.yml app -m yum -a "name=jq state=present"
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
ansible -i inventory.yml all -m setup
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
  - `ansible-console -i inventory.yml all`
- `ansible-doc`.
  - Muestra información sobre los módulos de ansible instalados.
  - `ansible-doc ping`
  - `ansible-doc ping -s`
- `ansible-galaxy`.
  - Maneja roles compartidos en repositorios de terceros. Por defecto buscara los repositorios en [https://galaxy.ansible.com](https://galaxy.ansible.com).
- `ansible-inventory`.
  - Util para validar el inventario con el que estamos trabajando.
  - `ansible-inventory -i inventory.yml --list`
  - `ansible-inventory -i inventory.yml --graph`
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
- hosts: app
  name: Primer playbook
  tasks:
    - ping:
```

Para correr un `playbook` utilizamos el comando `ansible-playbook`, al cuál podemos pasarle el inventario queremos utilizar (luego veremos otra forma de especificar el inventario):

```bash
ansible-playbook -i inventory.yml playbook.yml
```

Si queremos comprobar que la sintaxis de nuestro `playbook` no tiene errores podemos utilizar el flag `--syntax-check`. Y, si queremos ver con más detalles las acciones que esta realizando Ansible para detectar errores (debug), podemos correrlo con el comando con el flag `--verbose`.


Ejecutemos entonces nuestro playbook:
```
# ansible-playbook -i inventory.yml primer-playbook.yml

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
- hosts: app
  name: Primer playbook
  tasks:
    - ping:
    - ansible.builtin.user:
        name: user1
```

Al ejecutarlo:
```bash
root@master> ansible-playbook -i inventory.yml primer-playbook.yml

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

### Estructura de directorios para las paybooks
A medida que los `playbooks` crecen en complejidad, es necesario crear una estructura de directorios que nos permita ubicar los diferentes componentes (tareas, roles, variables, inventarios, etc.) en forma ordenada.

Existen ejemplos de mejores prácticas para dicha estructura, como el que se  puede encontrar [aquí](
https://docs.ansible.com/ansible/latest/user_guide/sample_setup.html#sample-directory-layout).

En nuestro lab, comenzarmos por colocar los `playbooks` en el directorio `~/ansible`, e iremos creando las estructuras de directos necesarias a medida que avancemos.


### Variables
Ref: [Using Variables](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html)

Podemos utilizar variables para almacenar valores que se pueden consumir en los `Playbooks`. Ansible sustuye la variable por su valor al momento de ejecutar la tarea. Las variables se pueden definir en múltiples lugares, y dependiendo donde se haga, tendrán precedencia unas sobre las otras.

Las variables se definen en forma de clave-valor, por ej:
  ```yaml
  application_path: /opt/my_app
  ```
y se referencian colocando el nombre de la variable entre llaves dobles:
  ```yaml
  La aplicación se encuentra instalada en {{application_path}}
  ```

Las variables y sus valores se pueden definir en varios lugares: el inventario, archivos de variables, pasarlas desde línea de comandos, etc.

La práctica recomendada para proporcionar variables en el inventario es definirlas en archivos ubicados en dos directorios denominados `host_vars` y `group_vars`:

Por ejemplo, para definir variables para nuestro grupo de hosts `app`, creamos el archivo `group_vars/app.yml` con las definiciones de variables.
Si queremos en cambio definir variables que apliquen a un único host, por ej. al `host01`, lo hacemos creando el archivo `host_vars/host01.yml` con las definiciones de variables.

>OBS: las variables de `host` tienen prioridad sobre las variables de `group`, puede encontrar más infromación sobre la precedencia en la definición de variables [aquí](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#understanding-variable-precedence).


También es posible definir variables en forma general, que puedan ser utilizadas independientemente del `host`/`group` sobre el cuál se ejecute el playbook. 
Para esto, podemos crear un archivo por ejemplo: `vars/my_app.yml` y definir aquí todas las variables necesarias para mi aplicación.
```yaml
application_path: /opt/my_app
```

Luego, al momento de escribir el `playbook` puedo incluir estas variables para que puedan ser referenciadas, mediante `var_files`:

```yml
- name: Desplegar mi aplicación
  hosts: app
  gather_facts: yes
  vars_files:
    - ./vars/my_app.yml
  tasks:
    - name: Copiar archivos de configuración
      copy:
        src: '/home/my_app//*.cfg'
        dest: '{{application_path}}'
```


### Registros de salida

Todas las tareas emiten por defecto una salida, en donde se incluye información general sobre la ejecución de la misma, más el mensaje generado por el módulo durante su ejecución. Sin embargo, esta salida no puede ser accedida a menos que se indique específicamente, mediante la opción `register`:

```yaml
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
La opción `register` almacena la salida de la tarea `shell` en una variable de entorno llamada `result` (si bien este nombre de variable es típicamente utilizado con este fin, podemos usar cualquier nombre de variable que querramos). Luego, la siguiente tarea `debug:` despliega el contenido de dicha variable.


```bash
root@master> ansible-playbook segundo-playbook.yml

PLAY [Ejemplo de como utilizar la opción 'register'] *******************************************************************************************

TASK [shell] ***********************************************************************************************************************************
changed: [localhost]

TASK [debug] ***********************************************************************************************************************************
ok: [localhost] => {
    "result": {
        "changed": true,
        "cmd": "echo Hola",
        "delta": "0:00:00.002576",
        "end": "2022-03-21 19:09:35.570745",
        "failed": false,
        "msg": "",
        "rc": 0,
        "start": "2022-03-21 19:09:35.568169",
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

>OBS: notese que este playbook lo estamos ejecutando contra *localhost*, o sea, contra el mismo *controller host* de Ansible, y por tanto no necesitamos pasarle el inventario.

---
### Condicionales
Como comentamos antes, Ansible esta desarrollado sobre Python, pero las configuraciones se realizan a través de documentos escritos en YAML para simplificar su escritura. Sin embargo, el hecho de contar con Python trabajando detrás de escena, nos permite incorporar funcionalidades más avanzadas a nuestros `playbooks`. Los condicionales son uno de ellos.

Mediante la utilización de la opción `when` en la definición de una tarea, podemos hacer que solo se ejecute la misma cuando se cumpla una determinada condición. El contenido de la opción `when` es una sentencia condicional de Python valida, que puede referenciar variables definidas de forma dinámica o estática.

Por ejemplo, si queremos generalizar una tarea para que se ejecute tanto en servidores Ubuntu como en CentOS, podemos agregar un condicional `when`, de forma de poder invocar al módulo de ansible correcto dependiendo de cuál sea el sistema operativo del host.

```yaml
# OBS: la variable `ansible_os_family` es resuelta por Ansible previo a 
#      la ejecución de las tareas en el host.
# ---
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
```bash
root@master> ansible-playbook -i inventory.yml tercer-playbook.yml

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

Al ejecutarlo, podemos ver una tarea inicial llamada `[Gathering Facts]`. Esta tarea es ejecutada siempre por defecto (salvo que le indiquemos no hacerlo) para obtener información relevante de los `hosts`. Entre dicha información, se obtiene el tipo de sistema operativo del host, el cuál se devuelve en la variable `ansible_os_family`, que es la variable que utilizamos nosotros en la sentencia `when`. 

Luego de la ejecución, podemos ver que la tarea de instalación fue ejecutada para Ubuntu, pero fue salteada para CentOS (skipped=1), dado que ninguno de nuestros hosts tiene CentOS.

---
## Loops

También podemos incluir loops en el código utilizando las opciones `loop`.

La opción `loop` toma una lista de opciones y ejecuta la tarea para cada uno de los elementos de la lista. Podemos acceder a los elementos de la lista durante la ejecución a través de la variable `item`.

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

>OBS: No es conveniente definir variables con el nombre `item` porque la misma por defecto será reemplazada cuando se utilicen loops.

Los elementos de cada lista pueden ser valores más complejos, como objetos u otras listas. Por ejemplo:

```yaml
- name: Ejemplo de como utilizar loop en un playbook de Ansible
  hosts: localhost
  connection: local
  gather_facts: no
  tasks:
    - debug:
        msg: '{{item["name"]}}'
      loop:
        - { name: 'testuser1', groups: 'wheel' }
        - { name: 'testuser2', groups: 'root' }
```
En este caso, cada elemento del `loop` es una lista, que tiene dentro dos elementos (name y groups). Y cuando itero sobre los mismos, despliego únicamente el primero (name).

En el caso de que no se conozca de antemano la cantidad de iteraciones que se necesita se pueden realizar `do-until` loops.

```yaml
# OBS: La idea es que el comando utilizado en la tarea falle
#      para ver funcionar el loop.
# ...
- name: Ejemplo de como crear un do-until loop.
  hosts: localhost
  connection: local
  gather_facts: no
  tasks:
    - shell: /usr/bin/no-exite-este-comando
      register: result
      until: result.stdout.find('todo bien') != -1
      retries: 5
      delay: 1
    - debug:
        msg: '{{result}}'
```

_OBS: El comando anterior fallará. En la siguiente sección veremos como podemos remediar esta situación utilizando `blocks`._

En el comando anterior se intento capturar la salida de una tarea que trabaja dentro de un loop. Lo que en realidad quedará registrado en la variable de salida es una lista con todas las salidas parciales.


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
# db_playbook.yml
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
# db_playbook.yml
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

---



## Ansible Config
Ref: [Configuring Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_configuration.html)

Aunque podemos indicarle a Ansible donde buscar el inventario cada vez que ejecutamoso un `playbook`, este proceso se vuelve tedioso rapidamente. Además, existe un sinfin adicional de comportamientos de Ansible que podemos querer modificar, dependiendo del tipo de proyecto en el que estemos trabajando. 

Ansible expone un archivo de configuraciones donde podemos definir su comportamiento.
Por defecto, Ansible buscará el archivo de configuración de la siguiente manera, y con esta precedencia:

1. En base a la configuración de la variable de entorno `ANSIBLE_CONFIG`.
2. Dentro del directorio donde se esta ejecutando Ansible, en un archivo llamado `ansible.cfg`.
3. En el directorio del usuario que ejecuta Ansible, bajo el nombre `~/.ansible.cfg`.
4. En la ubicación `/etc/ansible/ansible.cfg`.

>OBS: Nosotros recomendamos acompañar todos los proyectos de Ansible con un archivo de configuración `ansible.cfg` en la raiz del proyecto. De esta manera podemos saber exactamente que configuraciones estamos modificando, y tener diferentes configuraciones para diferentes proyectos.



## Reutilización de `playbooks`

Dada la forma de configuración que provee Ansible, es útil poder reutilizar el codigo de cada tarea o `playbook`. En Ansible hay tres formas de reutilizar codigo: `includes`, `import`, y `roles`. A continuación, mencionaremos como funcionan las tres, pero nos concentraremos en al utilización de roles.

Ansible cuenta con dos modos de operación:

- `static`: Ansible pre-procesa todos los archivos y referencias antes de comenzar a trabajar.
- `dynamic`: Ansible procesa los archivos a medida que comienza a operar.

Esta distinción es fundamental para entender el funcionamiento de los comandos de `imports` y los comandos de `include`. Ambos son utilizados para separar `playbooks` complejos o largos en multiples archivos más pequeños, que pueden ser reutilizados con mayor facilidad.

Si queremos que Ansible funcione en modo `static` debemos referenciar los archivos  pertinentes utilizando comandos de `import*`. Y si queremos que se comporte de forma dinámica, utilizamos comandos de `include*`.

Existen algunas limitaciones en el uso de `imports` e `include` que es importante tener en cuenta:

- Loops solo pueden realizarse con comandos de `include`. 
- Las variables definidas a nivel de inventario no serán consumidas por un `import`.

```yaml
# webservers.yml
- hosts: app
  tasks:
    - name: Install apache2
      apt: 
        name: apache2
        state: latest
        update_cache: yes
        
# three_tier_app.yml
- import_playbook: webservers.yml
```

---

## Roles

Los roles permiten importar de forma automática: archivos de variables, tareas, y handlers, basado en una estructura de directorios. Estos roles puede ser compartido en multiples `playbooks` .

La estructura de directorios que se debe utilizar es la siguiente:

```
roles/
  role01/
    tasks/
    handlers/
    files/
    templates/
    vars/
    defaults/
    meta/
  role02/
    ...
...
```

Al menos uno de estos directorios debe existir dentro de la carpeta del rol, sin embargo, no es necesario que existan todos. Dentro de cada carpeta en uso debe existir un archivo llamado `main.yml` en donde se encuentra la información útil correspondiente a esa carpeta.

Dentro de los archivos `main.yml` podemos referencias otros archivos para simplificar su lectura. Esto es usual, por ejemplo, cuando se quiere que un rol sea capaz de interactuar con multiples sistemas operativos, los cuales pueden requerir de la realización de distintas tareas para cumplir con el mismo objetivo. En la documentación de Ansible se presenta el siguiente ejemplo para demostrar esta práctica:

```yaml
# roles/apache2/tasks/main.yml
- import_tasks: redhat.yml
  when: ansible_os_family|lower == 'redhat'
- import_tasks: debian.yml
  when: ansible_os_family|lower == 'debian'
# roles/apache2/tasks/redhat.yml
- yum:
    name: "httpd"
    state: present

# roles/apache2/tasks/debian.yml
- apt:
    name: "apache2"
    state: present
```

Una vez definido el rol, puede ser agregado a un `playbook` a través de la opción `roles` la consume una lista de `roles` a ejecutar.

---

### Ejercicio #4

<!--
EJERCICIO 4 Y 5 DUPLICADOS
 Cree un rol capaz de instalar `apache2` y otro capaz de instalar `sqlite3`. Luego cree un nuevo `playbook` que instale `apache2` en los servidores identificados como `app` e instale `sqlite3` en los servidores identificados como `db` utilizando los roles previamente creados. -->

Cree dos roles, uno llamado `apache2` y otro `sqlite3`, que instalen `apache` y `sqlite3` respectivamente. Luego, cree un `playbook` que aplique el rol `apache2` a los servidores del grupo `app` y el rol `sqlite3` a los servidores del grupo `db`.

<details>
	<summary>
		Pista #1
	</summary>
	Recuerde que los roles deben ser crados dentro de la carpeta `/roles`.
</details>
<details>
	<summary>
		Pista #2
	</summary>
	Las carpetas activas dentro de los roles, cuentan con un archivo llamado `main.yml`.
</details>
<details>
	<summary>
		Pista #3
	</summary>
	Las tareas dentro del archivo `tasks/main.yml` se definen dentro de una lista.
</details>

<details>
    <summary>Solución</summary>
    <pre>
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


[Siguiente >](./03_ansible_networking.md)
