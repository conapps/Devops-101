---

Ansible además de permitirnos utilizar opciones especiales para expresar el comportamiento de las tareas (`loops`, `when`, etc.), ofrece otras estructuras que permiten la manipulación de variables y de salidas de otras tareas. Por ejemplo, nos permiten manipular documentos `JSON` directamente desde nuestro `playbook`, lo que agrega una gran potencia a nuestros `playbooks`.

Estas herramientas son: 

- Ansible Filters
- Ansible Plugins
- Templates de Jinja2
- El módulo `set_fact`.

El módulo `set_fact` es particularmente útil porque nos permite configurar variables durante la ejecución del `playbook` de forma dínamica. Explotaremos esta característica de este módulo para manipular nuestros documentos `JSON`. Las demás herramientas las veremos en la siguiente sección.

### Ansible Filters, Plugins, y Jinja2

Jinja2 es un lenguaje de templating desarrollado sobre python. El mismo se utiliza en varios frameworks importantes de Python como Django para crear páginas web por ejemplo. Sin embargo, se puede usar para crear todo tipo de documentos.

Ansible utiliza Jinja2 por debajo para la construcción de los scripts que se terminan ejecutando el los hosts remotos o localmente y además expone ciertas funcionalidades para ser utilizadas dentro de la definición de tareas. Por ejemplo, podemos utilizar Jinja2 para manipular variables declaradas en el inventario, en la configuración del rol, o al momento de correr el playbook. 

Cuando estamos configurando una tarea, y queremos configurar una determinada opción con una variable, utilizamos la sintaxis de Jinja2, e incluimos la variable que queremos referenciar

```yaml
- hosts: all
  vars:
    ejemplo: 'Hola Mundo!'
  tasks:
    - name: Imprimimos el valor de la variable 'ejemplo' en la consola
      debug:
      	msg: '{{ ejemplo }}'
```

En Jinja2, utilizamos los corchetes dobles `{{}}` para indicarle al sistema que dentro del mismos vamos a estar trabajando con variables y filtros. Además, tenemos que _escapar_ estas sentencias con comillas simples `''` o dobles `""` para que `YAML` no se las confunda con declaraciones de objetos de `JSON`.

Los filtros de Ansible se usan para manipular datos dentro de una expresión. Ansible expone una gran variedad de filtros para interactuar con nuestras variables. Un filtro no es más que un pequeño script de Python, que manipula valores almacenados en variables. Por lo tanto, podemos crear nuestros propios filtros para utilizarlos dentro de nuestros `playbooks`. Sin embargo, la creación de estos scripts escapa el alcance de este curso.

Dentro de los filtros más comunes tenemos:

- Filtros para formatear datos.
- Filtros para redefinir variables.
- Filtros para definir valores por defecto.
- Filtros para manipular listas
- Etc.

La lista completa de filtros se encuentra en el siguiente [link](https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters.html).

Por último, Ansible nos brinda Plugins. Los Plugins, son también scripts de Python pero que exponen una función capaz de realizar tareas más complejas que no tienen porque trabajar necesariamente sobre variables. Ansible provee varios filtros, y también permite la creación de nuevos plugins. 

Tampoco indicaremos en este curso como desarrollar nuestros propios plugins, simplemente utilizaremos algunos de los que Ansible provee por defecto, en particular el plugin `lookup`. El mismo permite buscar dentro del `filesystem` del host por archivos, que podemos cargar luego en una variable para interactuar con sus contenidos.

Veamos como podemos manipular un documento JSON utilizando todos estos componentes.


### Ejercicio #11

Cree un playbook llamado `interfaces.yml` que configure las interfaces de los routers spokes, si se cumplen las siguientes condiciones:

Las interfaces a configurar deben ser `GigabiEthernet`, estar con el protocolo `down` y `sin descripcion`.

Si se cumple eso configuro lo siguiennte:

- shutdown
- description No link Up

 
<details>
<summary>Pista #1</summary>

El módulo ios_command permite ejecutar lineas de configuración definidas en la opción commands.
Revise la documentación del módulo y los ejemplos aqui incluidos [link](https://docs.ansible.com/ansible/latest/collections/cisco/ios/ios_command_module.html)
</details>

<details>
<summary>Pista #2</summary>

Para extraer una o mas ocurrencias dentro de un string se puede usar el filtro `regex_findall`:

#### Ejemplos:

```yaml
Returns a list of all IPv4 addresses in the string
{{ 'Some DNS servers are 8.8.8.8 and 8.8.4.4' | regex_findall('\\b(?:[0-9]{1,3}\\.){3}[0-9]{1,3}\\b') }}
 => ['8.8.8.8', '8.8.4.4']

Returns all lines that end with "ar"
{{ 'CAR\ntar\nfoo\nbar\n' | regex_findall('^.ar$', multiline=True, ignorecase=True) }}
 => ['CAR', 'tar', 'bar']
```

Se puede chequear online las expresiones regulares [link](https://regexr.com/)

</details>
<details>
<summary>Pista #3</summary> 

## Expresiones regulares

Las expresiones regulares son algo muy útil cuando necesitamos interactuar con dispositivos pensados para ser utilizados por humanos, en contraposición a aquellos dispositivos que soportan "programabilidad orientada a modelos" (model driven programmability). Concretamente, estas nos permiten buscar patrones dentro del texto de forma de poder luego incorporar los datos obtenidos a partir de dichos patrones a las estructuras de datos del lenguaje de programmación. Veremos a continuación como funcionan las expresiones regulares a través de ejercicios, pero antes disponibilizamos una tabla con las expresiones mas comunes para poder utilizar como referencia.

### Special Characters

`^` | Matches the expression to its right at the start of a string. It matches every such instance before each `\n` in the string.

`$` | Matches the expression to its left at the end of a string. It matches every such instance before each `\n` in the string.

`.` | Matches any character except line terminators like `\n`.

`\` | Escapes special characters or denotes character classes.

`A|B` | Matches expression `A` or `B`. If `A` is matched first, `B` is left untried.

`+` | Greedily matches the expression to its left 1 or more times.

`*` | Greedily matches the expression to its left 0 or more times.

`?` | Greedily matches the expression to its left 0 or 1 times. But if `?` is added to qualifiers (`+`, `*`, and `?` itself) it will perform matches in a non-greedy manner.

`{m}` | Matches the expression to its left `m` times, and not less.

`{m,n}` | Matches the expression to its left `m` to `n` times, and not less.

`{m,n}?` | Matches the expression to its left `m` times, and ignores `n`. See `?` above.

### Character Classes (a.k.a. Special Sequences)

`\w` | Matches alphanumeric characters, which means `a-z`, `A-Z`, and `0-9`. It also matches the underscore, `_`.

`\d` | Matches digits, which means `0-9`.

`\D` | Matches any non-digits.

`\s` | Matches whitespace characters, which include the `\t`, `\n`, `\r`, and space characters.

`\S` | Matches non-whitespace characters.

`\b` | Matches the boundary (or empty string) at the start and end of a word, that is, between `\w` and `\W`.

`\B` | Matches where `\b` does not, that is, the boundary of `\w` characters.

`\A` | Matches the expression to its right at the absolute start of a string whether in single or multi-line mode.

`\Z` | Matches the expression to its left at the absolute end of a string whether in single or multi-line mode.

### Sets

`[ ]` | Contains a set of characters to match.

`[amk]` | Matches either `a`, `m`, or `k`. It does not match `amk`.

`[a-z]` | Matches any alphabet from `a` to `z`.

`[a\-z]` | Matches `a`, `-`, or `z`. It matches `-` because `\` escapes it.

`[a-]` | Matches `a` or `-`, because `-` is not being used to indicate a series of characters.

`[-a]` | As above, matches `a` or `-`.

`[a-z0-9]` | Matches characters from `a` to `z` and also from `0` to `9`.

`[(+*)]` | Special characters become literal inside a set, so this matches `(`, `+`, `*`, and `)`.

`[^ab5]` | Adding `^` excludes any character in the set. Here, it matches characters that are not `a`, `b`, or `5`.

### Groups

`( )` | Matches the expression inside the parentheses and groups it.

`(? )` | Inside parentheses like this, `?` acts as an extension notation. Its meaning depends on the character immediately to its right.

`(?PAB)` | Matches the expression `AB`, and it can be accessed with the group name.

`(?aiLmsux)` | Here, `a`, `i`, `L`, `m`, `s`, `u`, and `x` are flags:

- `a` — Matches ASCII only
- `i` — Ignore case
- `L` — Locale dependent
- `m` — Multi-line
- `s` — Matches all
- `u` — Matches unicode
- `x` — Verbose

`(?:A)` | Matches the expression as represented by `A`, but unlike `(?PAB)`, it cannot be retrieved afterwards.

`(?#...)` | A comment. Contents are for us to read, not for matching.

`A(?=B)` | Lookahead assertion. This matches the expression `A` only if it is followed by `B`.

`A(?!B)` | Negative lookahead assertion. This matches the expression `A` only if it is not followed by `B`.

`(?<=B)A` | Positive lookbehind assertion. This matches the expression `A` only if `B` is immediately to its left. This can only matched fixed length expressions.

`(?<!B)A` | Negative lookbehind assertion. This matches the expression `A` only if `B` is not immediately to its left. This can only matched fixed length expressions.

`(?P=name)` | Matches the expression matched by an earlier group named “name”.

`(...)\1` | The number `1` corresponds to the first group to be matched. If we want to match more instances of the same expresion, simply use its number instead of writing out the whole expression again. We can use from `1` up to `99` such groups and their corresponding numbers.

</details>

<details>
<summary>Pista #4</summary>

Se pueden combinar elementos provenientes de multiples listas usando el filtro zip [link](https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters.html#combining-items-from-multiple-lists-zip-and-zip-longest)

Luego se pueden transformar en un diccionario usando el constructor [dict](https://docs.ansible.com/ansible/latest/user_guide/complex_data_manipulation.html#create-dictionary-from-list)
</details>

<details>
<summary>Solución</summary>

```yaml
# ---
# interfaces.yml
#
# Configura intefaces down
# ---

- name: Configuro interfaces
  hosts: spokes
  connection: local
  gather_facts: no
  tasks:
    - name: Consulto show interfaces description | i down
      ios_command:
        commands: show interface description | i down 
      register: salida
  
    - name: Filtro las Interfaces
      set_fact:
        down: |
          {{ salida.stdout[0] |regex_findall('^(..[0-9]+)[ ]+(down|admin down)[ ]+(down)([ ]+|.*)(.*)', multiline=True) }} 

    - name: Listo salida
      debug:
        var: salida

    - name: Listo down
      debug:
        var: down

    - name: inicializo 
      set_fact:
        filtro: []

    - name: Keys  
      set_fact:
        keys: 
          - "Interface"
          - "Admin"
          - "Status"
          - "Space"
          - "Description"

    - name: Filtro
      set_fact:
        filtro: "{{ filtro + [dict(keys|zip(item))] }}"
      loop: 
        "{{ down }}"

    - name: Configuro interfaces
      ios_config:
        save_when: modified
        lines: 
          - description No link UP
          - shutdown
        parents: 'interface {{ item.Interface }}'
      when: 
        - item.Description == ""  
      loop:
        "{{ filtro }}"
```
</details>

