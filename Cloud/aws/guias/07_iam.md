# IAM

AWS Identity and Access Management (IAM) es un servicio web que le ayuda a controlar de forma segura el acceso a los recursos de AWS. Puede 

- controlar quién está autenticado (ha iniciado sesión) 
- autorizar para utilizar recursos (tiene permisos) .

Cuando se crea por primera vez una cuenta de AWS, se comienza con una única identidad de inicio de sesión que tiene acceso completo a todos los servicios y recursos de AWS de la cuenta. Esta identidad recibe el nombre de AWS de la cuenta de usuario raíz y se obtiene acceso a ella iniciando sesión con la dirección de correo electrónico y la contraseña que utilizó para crear la cuenta. Le recomendamos que no utilice usuario raíz en sus tareas cotidianas, ni siquiera en las tareas administrativas. En lugar de ello, es mejor ceñirse a la práctica recomendada de utilizar exclusivamente usuario raíz para crear el primer usuario de IAM. A continuación, guarde las credenciales de usuario raíz en un lugar seguro y utilícelas únicamente para algunas tareas de administración de cuentas y servicios.

## Terminos importantes

- `User`
  - En lugar de compartir sus credenciales de usuario raíz con otras personas, puede crear usuarios de IAM individuales dentro de su cuenta para usuarios de su organización. Los usuarios de IAM no son cuentas separadas, sino que son usuarios dentro de su cuenta. Cada usuario puede tener su propia contraseña para obtener acceso a la Consola de administración de AWS. También puede crear una clave de acceso individual para cada usuario, de modo que el usuario puede realizar solicitudes programadas para trabajar con recursos de su cuenta. En la figura siguiente, se han agregado los usuarios Li, Mateo, DevApp1, DevApp2, TestApp1 y TestApp2 a una única cuenta de AWS. Cada usuario tiene sus propias credenciales.
- `Policies`
  - Los usuarios de IAM son identidades en el servicio. Cuando se crean usuarios de IAM, estos no pueden obtener acceso a ningún elemento de la cuenta hasta que se les conceda permiso. Para conceder permisos a un usuario se crea una política basada en identidad, que es una política que se asocia al usuario o a un grupo al que el usuario pertenece.
- `Groups`
  - Puede organizar a los usuarios de IAM en grupos de IAM y asociar una política a un grupo. En ese caso, los usuarios individuales siguen teniendo sus propias credenciales, pero todos los usuarios de un grupo tienen los permisos que se asocian al grupo. 
- `Roles`
  - Los usuarios federados y otros recursos no tiene identidades permanentes en su cuenta de AWS tal y como las tienen los usuarios de IAM. Para asignarles permisos, puede crear una entidad a la que se hace referencia como `role` y definir permisos para el `role`. Cuando un usuario federado inicia sesión en AWS, se asocia el usuario al rol y se le conceden los permisos que están definidos en el `role`.

  ---

## 💻 DEMO #13 ~ Obtener credenciales programatias de IAM <a name="demo013"></a>

Desde la consola web.

### Procedimiento

1. Ir al Dashboard de IAM.
2. Hacer click en `Users`.
3. Hacer click en `admin`.
4. Hacer click en la tab `Security Credentials`.
5. Hacer click en `Create access key`.
6. ❗Guardar en una ubicación segura la `Access key ID` y la `Secret access key`.
7. Hacer click en `Close`.

### ❗Atención

Las llaves secretas solo se muestran una sola vez. Desde el modal que se nos presenta las podemos descargar o copiar a un lugar seguro. Si las perdemos no las podemos recuperar desde la página. Tenemos que volver a generar un nuevo par.

### FAQ

**¿Que sucede si pierdo el par de llaves?**

No se podrá conectar más de forma programatica hasta que haya generado un nuevo par. Debe eliminar el para anterior para evitar problemas.

**¿Que puedo hacer con estas credenciales?**

Todo lo que el usuario dueño de las mismas tenga permisos. Por eso es importante mantenerlas seguras.

---