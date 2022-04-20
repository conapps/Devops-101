

## Networking con Ansible

Como mencionamos antes, Ansible puede utilizarse para configurar más que servidores. En esta sección nos concentraremos en la configuración de equipos de red, específicamente, trabajando con routers Cisco. Sin embargo, todo lo que veamos puede trasladarse a equipos de otras marcas.

:point_right: Dentro de la lista de módulos que tiene Ansible para interactuar con otros sistemas, existe una categoría exclusiva para networking, que puede ver [aquí](https://docs.ansible.com/ansible/2.9/modules/list_of_network_modules.html).

La lista es extensa y contiene módulos para la mayoría de los vendors más importantes del mercado. Sin embargo, es posible que algún módulo en particular no exista. En este caso podemos desarrollar nostros nuestro propio módulo, y si queremos, ofrecerlo luego al resto de la comunidad. Esta es una de las ventajas que tiene el software de código abierto.

Nosotros nos concentraremos en los módulos para [Cisco IOS](https://www.cisco.com/c/en/us/products/ios-nx-os-software/index.html), que puede encontrar [aquí](https://docs.ansible.com/ansible/2.9/modules/list_of_network_modules.html#ios).


### Ambiente de Laboratorio de Networking
Para los laboratorios de esta parte del curso, utilizaremos los siguientes equipos:
![Diagrama de Lab](./imagenes/ansible_013.png)

Cada Pod cuenta con 3 routers configurados Hub & Spoke. El `hub` se encuentra en la red de `management` y es el único que puede ser accedido directamente a través de Internet. Aunque recomendamos conectarse al mismo desde nuestro equipo `controller`, que utilizamos para Ansible. Los dos equipos `spoke` se encuentran en redes privadas, y conseguiremos acceder a ellos a medida que avanzamos con el laboratorio. 

:point_right: La idea de esta parte del curso es realizar las configuraciones de los routers a través de `Ansible`, y no con la `cli` conectado a la consola. Sin embargo, puede resultar útil conectarse a la consola para ver como se aplican los cambios, verificar configuraciones, etc.

Para **conectarnos al router `hub` recomendamos hacerlo desde el equipo `controller`**, dado que ya tenemos preconfigurado para conectarnos por nombre (la X corresponde al número de POD asignado):
```bash
$ ssh hub-X.labs.conatest.click

ip-10-X-254-254#
```

Al conectarse al router queda parado en la consola de configuración en modo `EXEC`. Podemos verificar que nos encontramos en un router CISCO utilizando el comando `show version`:

```
ip-10-X-254-254# show version
Cisco IOS XE Software, Version 16.12.06
Cisco IOS Software [Gibraltar], Virtual XE Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 16.12.6, RELEASE SOFTWARE (fc3)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2021 by Cisco Systems, Inc.
Compiled Sun 05-Sep-21 00:37 by mcpre

(...)
```

También podemos **conectarnos a los routers `spoke1` y `spoke2` desde `controller`** de forma similar (la X corresponde al número de POD asignado):
```bash
$ ssh spoke1-X.labs.conatest.click

ip-10-X-201-253#
```
```bash
$ ssh spoke2-X.labs.conatest.click

ip-10-X-202-253#
```



Si queremos **conectarnos a los routers directamente por internet**, debemos incluir opciones adicionales al ssh:
```bash
$ ssh -i devops101-labs.pem -o KexAlgorithms=diffie-hellman-group-exchange-sha1 ec2-user@hub-X.labs.conatest.click
```
> OBS: Si al intentar conectarnos nos tira para afuera sin nungún mensaje, puede deberse a que el router busca el certificado ssh en la lista de hosts conocidos de nuestra máquina, la cuál puede ver con: `ssh-add -l`. Si este es el caso, intente agregar el certificado a la lista de host conocidos mediante `ssh-add devops101-lab.pem` y vuelva a probar. Si el problema persiste, recomendamos conectarse desde el equipo `controller` que ya se encuentra preconfigurado para facilitar la conexión.


Para poder **establecer la conexión a los routers a través de Ansible** tenemos que realizar algunos pasos previos, los cuales haremos en el siguiente **Demo Lab**.

>OBS: si lo prefiere, en lugar de modificar los archivos que venimos utilizando de los labs anteriores, puede crear un nuevo directorio para comenzar desde cero, y trabajar en el mismo creando un nuevo archivo de inventario, nuevos directorios según sean requeridos, etc. También puede reinicial el ambiente desde cero, borrando su contenido, como vimos [aqui](https://github.com/conapps/Devops-101/blob/master/Ansible-101/01_ansible.md#demo-lab-1---lanzar-el-laboratorio).


### Demo Lab #3 - Configurar el ambiente requerido para Ansible

Lo primero que debemos hacer es agregar nuestros equipos de Networking al inventario.

```yaml
# ./inventory/hosts.yml
all:
  children:
    routers:
      hosts:
        10.X.254.254:
```

La mayoría de los equipos de red no cuentan con una interfaz programática para interactuar con ellos. En general, solamente podemos configurarlos a través de una consola. Además, tampoco permiten correr scripts de python a través de ssh, que es lo que realizamos con Ansible en los ejemplos anteriores. Por lo tanto, debemos indicarle a Ansible como debe interactuar con estos equipos. 
Comenzaremos por configurar las siguientes variables que aplican a todos los `routers` del inventario:

```yaml
# ./inventory/hosts.yml
all:
  children:
    routers:
      vars:
        # Nombre de usuario
        ansible_user: ec2-user
        # Llave privada a utilizar
        ansible_ssh_private_key_file: ~/.ssh/devops101-labs.pem
        # Sistema operativo a utilizar
        ansible_network_os: ios
        # Permitir elevación de permisos
        ansible_become: yes
        # Comando a utilizar para elevar permisos
        ansible_become_method: enable
        # Tipo de conexión
        ansible_connection: network_cli
      hosts:
        10.X.254.254:
```

Además, en el `ansible.cfg` del proyecto, configuramos las siguientes opciones:

```yml
# ./ansible.cfg
[defaults]
inventory = ./inventory/hosts.yml      
#vault_password_file = /root/secret/vault-password   # estaba de antes, podemos comentarla por ahora
host_key_checking = False
retry_files_enabled = False
```

Para verificar que todo funcine correctamente, hacemos un `ansible ping` al grupo `routers`, siempre trabajando desde el `controller`:

```
# ansible routers -m ping
10.1.254.254 | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```

Ahora que sabemos que la conectividad funciona, agreguemos los routers `spoke` al inventario, separándolos en dos grupos `hub` y `spokes`. Podemos mejorar un poco nuestro inventario y asignarle nombre a los routers, para no tener que hacerle referencia por la dirección IP, ademas de agregar un grupo para los `spokes`.
En caso que estemos usando el mismo inventario que habíamos definido antes, movamos los servidores linux a otro grupo `servers` con sus propias variables definidas dentro.

```yaml
# archivo de inventario ./inventory/hosts.yml
all:
  children:
    routers:
      vars:
        ansible_user: ec2-user
        ansible_ssh_private_key_file: ~/.ssh/devops101-labs.pem
        ansible_network_os: ios
        ansible_become: yes
        ansible_become_method: enable
        ansible_connection: network_cli
      hosts:
          hub:
            ansible_host: 10.1.254.254
          spoke01:
            ansible_host: 10.1.201.253
          spoke02:
            ansible_host: 10.1.202.253
      children:
        spokes:
          hosts:
            spoke01:
            spoke02:
    servers:
      vars:
        ansible_ssh_common_args: '-o StrictHostKeyChecking=no'
        ansible_ssh_private_key_file: '~/ansible/master_key'
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
---

### `ios_config`

Uno de los módulos más comunes para utilizar con equipos `ios` es `ios_config`, cuya documentación puede ver [aquí](https://docs.ansible.com/ansible/latest/modules/ios_config_module.html).

El primer `playbook` que vamos a crear permitira almacenar un respaldo de las configuraciones de los `routers` en un directorio que indicamos:

```yaml
# ---
# routers-backup-config.yml
#
# Crea un respaldo de las configuraciones de los equipos IOS
# ---
- name: Respaldo de configuraciones IOS
  hosts: routers
  connection: local
  gather_facts: no
  tasks:
    - name: Comandos para respaldar las configuraciones
      ios_config:
        backup: yes
        backup_options:
          dir_path: ./respaldo-routers
```
Pruebe de correr el `playbook` y verificar que se realizó el respaldo.

---

### Ejercicio #8

Cree un `playbook` que le permita modificar el `hostname` de los `routers`, solo en el caso de que la variable `hostname` este definida para cada host.

<details>
    <summary>Pista #1</summary>
    El módulo <code>ios_config</code> permite ejecutar lineas de configuración definidas en la opción <code>lines</code>. Revise la documentación del módulo y los ejemplos allí incluidos.
</details>

<details>
    <summary>Pista #2</summary>
    El comando para cambiar el <code>hostname</code> en <code>ios</code> es: <code>hostname nombre_del_host</code>
</details>

<details>
    <summary>Pista #3</summary>
    Recuerde utilizar la opción <code>when</code> dentro de una <code>task</code> para ejecutarla sólo cuando se cumpla determinada condición. En este caso, la condición que deberá evaluar es, que exista la variable <code>hostname</code> definida para el host.
</details>

<details>
    <summary>Pista #4</summary>
    Recuerde definir la variable <code>hostname</code>, la cuál debe tener el nombre que quiere asignarle al <code>router</code>. Recuerde que hay varios lugares donde puede definir dicha variable.
</details>

<details>
    <summary>Verificación</summary>
    Conectese al <code>router</code> y verifique que el <code>prompt</code> se modificó con el <code>hostname</code> establecido, por ej:.
<pre class="language-yaml" lang="yaml">
(controller) # ssh hub-1.labs.conatest.click
hub#
</pre>
<pre class="language-yaml" lang="yaml">
(controller) # ssh spoke1-1.labs.conatest.click
spoke1#

</pre>
</details>

<details>
    <summary>Solución</summary>
<pre class="language-yaml" lang="yaml">
# ./inventory/group_vars/routers.yml
hostname: '{{inventory_hostname}}'
</pre>

<pre class="language-yaml" lang="yaml">
# ./inventory/hosts.yml
# archivo de inventario ./inventory/hosts.yml
all:
  children:
    routers:
      vars:
        ansible_user: ec2-user
        ansible_ssh_private_key_file: ~/.ssh/devops101-labs.pem
        ansible_network_os: ios
        ansible_become: yes
        ansible_become_method: enable
        ansible_connection: network_cli
      hosts:
          hub:
            ansible_host: 10.1.254.254
          spoke01:
            ansible_host: 10.1.201.253
          spoke02:
            ansible_host: 10.1.202.253
      children:
        spokes:
          hosts:
            spoke01:
            spoke02:
</pre>

<pre class="language-yaml" lang="yaml">
# routers-update-hostnames.yml
#
# Modifica el hostname de los routers de acuerdo al valor definido
# en la variable `hostname`, solo si la misma se encuentra definida.
# ---

- name: Ejercicio 8 - Modificar hostname de los routers
  hosts: routers
  connection: local
  gather_facts: no
  tasks:
    - name: Modificar el hostname
      ios_config:
        lines: 'hostname {{hostname}}'
      when: hostname is defined
</pre>

Referencias:
- special variable <code>inventory_hostname</code>: https://docs.ansible.com/ansible/latest/reference_appendices/special_variables.html
- inventory aliases <code>ansible_host</code>:
https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html#inventory-aliases

</details>

---

### Auditoría de configuraciones
Una de las tareas que se realizan comúnmente a nivel de red es auditar las configuraciones de los dispositivos, de forma de garantizar de que todos ellos están configurados de la misma manera, o que cumplen con los estándares de la organización. El módulo `ios_config` cuenta con algunas opciones para realizar esta tarea.

A través de la opción `diff_against` podemos indicarle al módulo `ios_config` contra que configuración buscar las diferencias. El comando acepta tres opciones:

- `running`: el sistema retornará la configuración antes y después de realizarle cambios.
- `startup`: si se corre el `playbook` bajo el flag `—diff` retornará la diferencia entre la `startup` config y la `running` config.
- `intended`: verificará las diferencias entre la `running` config y aquella que se indique en la opción `intended_config`.


> OBS: el flag `—diff` le indica a Ansible, en terminos generales, que nos indique que acciones se ejecutarían en caso de correr el `playbook` sin este flag.

Por ejemplo, si corremos el siguiente `playbook` veremos las diferencias entre la configuración de `startup` del router y el cambio que realizamos al `hostname`.

:warning: Debe correrlo con la opción `--diff`.

```yaml
# ---
# routers-running-vs-startup-config.yml
#
# Muestra las diferencias entre la running y startup config.
# Obs: Este playbook debe ser ejecutado con el flag `--diff`.
# ---

- name: Running vs. Startup configuration diff (simple)
  hosts: hub
  connection: local
  gather_facts: no
  tasks:
    - name: Comando para hallar las diferencias
      ios_config:
        diff_against: startup
```

Para la salida del router `hub` deberíamos ver algo similar a:
```
(controller) # ansible-playbook --diff routers-running-vs-startup-config.yml

PLAY [Running vs. Startup configuration diff (simple)] *****************************************************************************************

TASK [Comando para hallar las diferencias] *****************************************************************************************************
--- before
+++ after
@@ -6,7 +6,7 @@
 platform qfp utilization monitor load 80
 platform punt-keepalive disable-kernel-core
 platform console virtual
-hostname ip-10-1-254-254
+hostname hub
(...)
(...)
```

### `ios_facts`

Existen otros módulos que también se pueden utilizar para obtener información de los dispositivos.
Por ejemplo `ios.facts`, cuya documentación puede ver [aquí](https://docs.ansible.com/ansible/latest/collections/cisco/ios/ios_facts_module.html)



```yaml
# ---
# routers-get-facts.yml
# 
# Obtiene la configuración de routers Cisco IOS
# 
# ...
- name: Get routers facts
  hosts: hub
  connection: local
  gather_facts: no
  tasks:
    - ios_facts:
      register: result 

    - debug:
        var: result.ansible_facts

```

:point_right: el módulo `debug:` de Ansible permite desplegar información como parte de la salida del playbook. Podemos desplegar el contenido de una variable con `var:`, o el mensaje que querramos con `msg:`. Puede ver la documentación del módulo [aquí](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/debug_module.html).


Podemos ejecutar el `playbook` anterior sobre `spoke01` y ver la salida que devuelve:

```
ansible-playbook router-get-facts.yml 

PLAY [Get routers facts] ***********************************************************************************************************************

TASK [ios_facts] *******************************************************************************************************************************
ok: [hub]

TASK [debug] ***********************************************************************************************************************************
ok: [hub] => {
    "result.ansible_facts": {
        "ansible_net_all_ipv4_addresses": [
            "10.1.254.254",
            "10.1.201.254",
            "10.1.202.254",
            "192.168.35.101"
        ],
        "ansible_net_all_ipv6_addresses": [],
        "ansible_net_api": "cliconf",
        "ansible_net_filesystems": [
            "bootflash:"
        ],
        "ansible_net_filesystems_info": {
            "bootflash:": {
                "spacefree_kb": 5370036.0,
                "spacetotal_kb": 6138880.0
            }
        },
        "ansible_net_gather_network_resources": [],
        "ansible_net_gather_subset": [
            "default",
            "interfaces",
            "hardware"
        ],
        "ansible_net_hostname": "hub",
        "ansible_net_image": "bootflash:packages.conf",
        "ansible_net_interfaces": {
            "GigabitEthernet1": {
                "bandwidth": 1000000,
                "description": null,
                "duplex": "Full",
                "ipv4": [
                    {
                        "address": "10.1.254.254",
                        "subnet": "24"
                    }
                ],
                "lineprotocol": "up",
                "macaddress": "0e82.88ee.e7c5",
                "mediatype": "Virtual",
                "mtu": 1500,
                "operstatus": "up",
                "type": "CSR vNIC"
            },
            "GigabitEthernet2": {
                "bandwidth": 1000000,
                "description": "ConexiC3n con Red Spoke1",
                "duplex": "Full",
                "ipv4": [
                    {
                        "address": "10.1.201.254",
                        "subnet": "24"
                    }
                ],
                "lineprotocol": "up",
                "macaddress": "0e56.310b.fd49",
                "mediatype": "Virtual",
                "mtu": 1500,
                "operstatus": "up",
                "type": "CSR vNIC"
            },
            "GigabitEthernet3": {
                "bandwidth": 1000000,
                "description": "ConexiC3n con Red Spoke1",
                "duplex": "Full",
                "ipv4": [
                    {
                        "address": "10.1.202.254",
                        "subnet": "24"
                    }
                ],
                "lineprotocol": "up",
                "macaddress": "0e42.6241.25d3",
                "mediatype": "Virtual",
                "mtu": 1500,
                "operstatus": "up",
                "type": "CSR vNIC"
            },
            "VirtualPortGroup0": {
                "bandwidth": 750000,
                "description": null,
                "duplex": null,
                "ipv4": [
                    {
                        "address": "192.168.35.101",
                        "subnet": "24"
                    }
                ],
                "lineprotocol": "up",
                "macaddress": "001e.4976.14bd",
                "mediatype": null,
                "mtu": 1500,
                "operstatus": "up",
                "type": "Virtual Port Group"
            }
        },
        "ansible_net_iostype": "IOS-XE",
        "ansible_net_memfree_mb": 1831399.328125,
        "ansible_net_memtotal_mb": 2076700.96875,
        "ansible_net_model": "CSR1000V",
        "ansible_net_neighbors": {},
        "ansible_net_python_version": "3.8.10",
        "ansible_net_serialnum": "9LIAS8D01DX",
        "ansible_net_system": "ios",
        "ansible_net_version": "16.12.06",
        "ansible_network_resources": {}
    }
}

PLAY RECAP *************************************************************************************************************************************
hub                        : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

```

---


### `ios_user`
Otro módulo que nos puede resultar útil para configurar equipos con IOS, es el módulo `ios_user`, que permite gestionar usuarios de forma más sencilla que haciendolo con los comandos individuales.
Puede encontrar la documentación del módulo [aquí](https://docs.ansible.com/ansible/latest/collections/cisco/ios/ios_user_module.html).

---

### Ejercicio #9

Construya un `playbook` llamado `routers-create-user.yml` que agregue un usuario en todos los routers, con las siguientes credenciales:

- User: conatel
- Pass: conatel
- Privilege: 15

<details>
<summary>Solución</summary>

<pre class="language-yaml" lang="yaml">
#./ansible.cfg
[defaults]
inventory = ./inventory/hosts.yml
vault_password_file = /root/secret/vault-password
host_key_checking = False
retry_files_enabled = False
</pre>

<pre class="language-yaml" lang="yaml">
(controller) # ansible-vault encrypt_string 'conatel' --name 'user_name' 
user_name: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          66333730356638333435623631346335313161616566663139353734623539343430623637646430
          6565633435323435353935663961613861666530316561350a333437633037323539353737306330
          34653234373136386534353365633931346332326136653331363462373761343737633235376138
          6339656261363235310a356136623730643733336165663737323033303263613237633632396333
          3233
Encryption successful

(controller) # ansible-vault encrypt_string 'conatel' --name 'user_password' 
user_password: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          66646162333038643832336130653635366362616334366566383135313330623532316235623738
          6663373235323830393462633633623161656133383535310a326231386638663531303034346136
          38613761643466303833653363646165626164613639633561613138363736333932623663313033
          6631313138373532380a626662326434373839393839303334616265653731343130616435623439
          3937
Encryption successful
</pre>

<pre class="language-yaml" lang="yaml">
#./inventory/group_vars/routers.yml
hostname: '{{inventory_hostname}}'
user_name: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          66333730356638333435623631346335313161616566663139353734623539343430623637646430
          6565633435323435353935663961613861666530316561350a333437633037323539353737306330
          34653234373136386534353365633931346332326136653331363462373761343737633235376138
          6339656261363235310a356136623730643733336165663737323033303263613237633632396333
          3233
user_password: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          66646162333038643832336130653635366362616334366566383135313330623532316235623738
          6663373235323830393462633633623161656133383535310a326231386638663531303034346136
          38613761643466303833653363646165626164613639633561613138363736333932623663313033
          6631313138373532380a626662326434373839393839303334616265653731343130616435623439
          3937
user_privilege: 15
</pre>


<pre class="language-yaml" lang="yaml">
# ---
# routers-create-user.yml
#
# Crea un usuario en routers Cisco IOS
# ---

- name: Ejercicio 9 - Crear usuario en Cisco IOS
  hosts: routers
  connection: local
  gather_facts: no
  tasks:
    - name: Crear el usuario
      ios_user:
        name: '{{user_name}}'
        configured_password: '{{user_password}}'
        privilege: '{{user_privilege}}'
        state: present
        update_password: always
      no_log: true
</pre>
</details>

---

### `ios_command`
Como ya vimos, existen múltiples módulos para configurar equipos de red, que permiten realizar configuraciones específicas. Pero puede ocurrir que necesitemos realizar cierta configuración, y no contemos con un módulo específico para esto.
En ese caso, podemos recurrir al módulo `ios_command` que nos permite ejecutar comandos directamente como si los estuvieramos escribiendo en la consola del equipo.

Puede encontrar la documentación de este módulo [aquí](https://docs.ansible.com/ansible/latest/collections/cisco/ios/ios_command_module.html).



### Cambios a varios dispositivos
Como ya vimos, es sencillo realizar configuraciones en múltiples equipos utilizando Ansible. Alcanza con aplicar el mismo `playbook` a múltiples `hosts` y Ansible se encarga de ejecutar las tareas sobre todos ellos.

Los routers del laboratorio ya están configurados para poder comunicarse entre sí. Sin embargo, no podemos llegar a los equipos `slave1` y `slave2` desde `controller`:
```
(controller) # ping slave1-1.labs.conatest.click
PING slave1-1.labs.conatest.click (10.1.1.100) 56(84) bytes of data.
^C
--- slave1-1.labs.conatest.click ping statistics ---
6 packets transmitted, 0 received, 100% packet loss, time 5106ms
```

Esto se debe a que las interfaces `GigabitEthernet2` de los routers `spokes`, que conectan a los equipos `slaves`, no están configuradas. Esto podemos verlo, por ejemplo, si corremos el playbook `router-get-facts.yml` contra los `spokes`, que devuelve algo como esto:
```
    "GigabitEthernet2": {
        "bandwidth": 1000000,
        "description": null,
        "duplex": "Full",
        "ipv4": [],
        "lineprotocol": "down",
        "macaddress": "0ebb.5df9.2ec3",
        "mediatype": "Virtual",
        "mtu": 1500,
        "operstatus": "administratively down",
        "type": "CSR vNIC"
    },
```

Nuevamente, para configurar las interfaces del router utilizamos el módulo `ios_config`, cuya documentación se encuentra [aquí](https://docs.ansible.com/ansible/latest/collections/cisco/ios/ios_config_module.html). Revise los detalles del módulo y los ejemplos de configuración.

---

Veamos entonces como solucionarlo.

### Ejercicio #10
Cree un nuevo rol llamado `configure_interfaces` que configure las interfaces de los routers, a partir de una `lista` de `interfaces`, con las siguiente estructura:

```yml
interfaces:
  - interface: GigabitEhernet1
    ip_address: x.x.x.x
    netmask: -.-.-.-
    description: <descripción de la interface 1>
  - interface: GigabitEthernet2
    ip_address: y.y.y.y
    netmask: -.-.-.-
    description: <descripción de la interface 2>
    (...)
```
Tenga en cuenta que los diferentes routers, tienen diferentes cantidad de interfaces (los `spoke` tiene dos interfaces, `hub` tiene tres inferfaces, etc.) por lo cual el rol ebe poder manejar una cantidad indefinida de items en esta la lista. 

:point_right: recuerde grabar la configuración si realiza cambios en los routers.

El rol luego será llamado a través del siguiente `playbook`:
```yaml
# ---
# routers-configure-interfaces.yml
#
# Configura las interfaces de un router Cisco IOS
# ---

- name: Configuración de interface
  hosts: <equipos a configurar>
  connection: local
  gather_facts: no
  roles:
    - configure_interfaces
```


:warning: Tenga especial cuidado si realiza cambios de configuración en el router `hub` porque podría perder la conectividad a todos los equipos del lab.


<details>
<summary>Pista #1</summary>
Recuerde que los roles requieren de una determinada estructura de directorios, tal como vimos antes.
</details>

<details>
<summary>Pista #2</summary>
Debe definir (como variable) la lista de <code>interfaces</code> con la información de configuración para cada uno de los routers, siguiendo el formato de lista solicitado en el ejercicio.
Esto puede definirlo en diversos lugares del código (host_vars/group_vars/inventory vars/etc.). 
Ejemplo:
<pre>
interfaces:
  - interface: GigabitEthernet1
    ip_address: 10.xxx.xxx.xxx
    netmask: 255.255.255.0
    description: Conexion con red xxxx
  - interface: GigabitEthernet2
    ip_address: 10.xxx.xxx.xxx
    netmask: 255.255.255.0
    description: Conexión con red xxxx
</pre>
</details>

<details>
<summary>Pista #3</summary>
Tenga en cuenta que la lista <code>interfaces</code> de cada router tendrá una cantidad variable de ítems (algunos routers pueden tener dos interfaces, otros tres, cinco, etc.). Para referenciar los valores de configuración, deberá iterar sobre la lista de <code>interfaces</code>, por ejemplo utilizando <code>loop:</code>.

Para probar que la iteración funciona correctamente, utilice primero el módulo <code>debug:</code> para desplegar los diferentes items de la lista de <code>interfaces</code>, en lugar de directamente hacer el cambio en la configuración del router con <code>ios_config</code>. De esta forma evita "quedar afuera" en caso de que le erre a la configuración.
</details>


<details>
<summary>Pista #4</summary>
Utilice la opción <code>save_when:</code> del módulo <code>ios_config</code> para grabar la configuración de los routers cuando se realicen cambios.
</details>

<details>
<summary>Pista #5</summary>
Utilice el módulo <code>ios_config</code> para configurar las interfaces del router. Por ejemplo:
<pre class="language-yaml" lang="yaml">
- ios_config:
    lines:
      - description "Conexión con Red Tunnel 01"
      - ip address 10.X.201.254 255.255.255.0
      - no shutdown
    parents: interface GigabitEthernet2

Vea como se le indica cual es el `parent` sobre el cual se realizan los comandos, en este caso, la `interface GigabitEthernet2`. Y básicamente, escribimos las líneas que ingresaríamos en la consola del router, para aplicar la configuración sobre dicha interface.
</details>

<details>	
<summary>Solución</summary>

<pre class="language-yaml" lang="yaml">
# ./inventory/hosts.yml
all:
  children:
    routers:
      vars:
        ansible_user: ec2-user
        ansible_ssh_private_key_file: ~/.ssh/devops101-labs.pem
        ansible_network_os: ios
        ansible_become: yes
        ansible_become_method: enable
        ansible_connection: network_cli
      hosts:
          hub:
            ansible_host: 10.X.254.254
          spoke01:
            ansible_host: 10.X.201.253
          spoke02:
            ansible_host: 10.X.202.253
      children:
        spokes:
          hosts:
            spoke01:
            spoke02:
</pre>

<pre class="language-yaml" lang="yaml">
# ./inventory/host_vars/spoke01.yml
hostname: spoke01
interfaces:
  - interface: GigabitEthernet1
    ip_address: 10.X.201.253
    netmask: 255.255.255.0
    description: Conexion con red Tunnel-01
  - interface: GigabitEthernet2
    ip_address: 10.X.1.253
    netmask: 255.255.255.0
    description: Conexión con red Spoke-01
</pre>

<pre class="language-yaml" lang="yaml">
# ./inventory/host_vars/spoke02.yml
hostname: spoke02
interfaces:
  - interface: GigabitEthernet1
    ip_address: 10.X.202.253
    netmask: 255.255.255.0
    description: Conexion con red Tunnel-02
  - interface: GigabitEthernet2
    ip_address: 10.X.2.253
    netmask: 255.255.255.0
    description: Conexión con red Spoke-02
</pre>


<pre class="language-yaml" lang="yaml">
# ./roles/configure_interfaces/tasks/main.yml
#
# Tareas para configurar la interfaz de un equipo.
# ---
- name: 'Configuro interfaces de router Cisco IOS'
  ios_config:
    lines:
      - 'description {{ item.description }}'
      - 'ip address {{ item.ip_address }} {{ item.netmask }}'
      - no shutdown
    parents: 'interface {{ item.interface }}'
  save_when: modified
  loop: '{{ interfaces }}'
</pre>

<pre class="language-yaml" lang="yaml">
# ./routers-configure-interfaces.yml
#
# Configura interfaces de los routers Cisco IOS
# 
# OBS: se debe definir una lista con los valores a configurar para el router:
#   interfaces:
#     - interface: GigabitEthernet1
#       ip_address: '1.2.3.4'
#       netmask: '255.255.255.0'
#       description: Conexión con red-1
# ...
- name: Ejercicio 10 - Configurar interfaces de los routers
  hosts: spokes
  connection: local
  gather_facts: no
  roles:
    - configure_interfaces
</pre>
</details>



---


