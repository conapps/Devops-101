
## Reutilización del código

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
