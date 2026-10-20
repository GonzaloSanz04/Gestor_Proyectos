# Gestor de proyectos y tareas

API REST para gestionar proyectos con una jerarquía Proyecto > Épica > User Story > Tarea, con roles por proyecto y asignación de tareas a varios usuarios.

Proyecto personal de formación. El objetivo es practicar las funcionalidades habituales de un backend (API, base de datos, autenticación, tests, Docker, CI/CD) y documentar las decisiones tomadas por el camino.

## Estado del proyecto

- Fase actual: diseño del modelo de datos.
- Pendiente: definir el MVP, la estructura del repositorio e implementar registro y login.

## Stack

- Lenguaje: Python
- Framework: FastAPI
- Base de datos: PostgreSQL
- Previsto: SQLAlchemy (ORM), Alembic (migraciones), pytest, Docker Compose, GitHub Actions
- Frontend: por decidir

## Modelo de datos

### Entidades

**Usuario**
- id (PK), username (único), nombre, apellidos, correo (único), password_hash
- telefono (opcional, único), rol (USUARIO, ADMIN), activo
- fecha_alta, fecha_modificacion

**Proyecto**
- id (PK), creador_id (FK a Usuario), titulo, descripcion (opcional)
- estado (EN_CURSO, CERRADO, PLANIFICADO)
- fecha_creacion, fecha_modificacion

**Miembro_proyecto**
- usuario_id (FK), proyecto_id (FK), rol_en_proyecto (USUARIO, EDITOR), fecha_union
- PK compuesta (usuario_id, proyecto_id)

**Epica**
- id (PK), creador_id (FK), proyecto_id (FK), titulo, descripcion (opcional)
- estado, prioridad (ALTA, MEDIA, BAJA)
- fecha_creacion, fecha_modificacion

**User Story (US)**
- id (PK), creador_id (FK), epica_id (FK), titulo, descripcion (opcional)
- estado, prioridad
- fecha_creacion, fecha_modificacion

**Tarea**
- id (PK), creador_id (FK), proyecto_id (FK), us_id (FK), titulo, descripcion (opcional)
- estado, prioridad, fecha_limite (opcional)
- fecha_creacion, fecha_modificacion

**Asignacion_tarea**
- tarea_id (FK), usuario_id (FK), fecha_asignacion, asignado_por (FK a Usuario, opcional)
- PK compuesta (tarea_id, usuario_id)

El enum de estado (EN_CURSO, CERRADO, PLANIFICADO) es compartido por Proyecto, Épica, US y Tarea.

### Relaciones

- Usuario 1:N Proyecto (creador)
- Usuario N:M Proyecto (a través de Miembro_proyecto)
- Proyecto 1:N Épica
- Épica 1:N US
- US 1:N Tarea
- Usuario N:M Tarea (a través de Asignacion_tarea)
- Usuario 1:N Épica, US y Tarea (creador)

## Reglas de negocio

- El login se puede hacer con username o con correo.
- El carácter "@" no está permitido en el username (evita colisiones con correos).
- El creador de un proyecto entra automáticamente como EDITOR.
- El rol EDITOR actúa como administrador del proyecto (puede incluso borrarlo).
- No se puede cerrar una entidad con subentidades en estado distinto de CERRADO.
- No se puede asignar una tarea a un usuario que no sea miembro del proyecto.
- Las entidades cerradas no se reabren: se crea una nueva.
- Los usuarios no se borran, se desactivan (campo activo).

## Decisiones de arquitectura

### Tablas separadas para Épica, US y Tarea

Se elige una tabla por nivel en lugar de una tabla única con tipo y jerarquía.

- A favor: cada nivel tiene su esquema y sus claves foráneas.
- A favor: cada entidad tiene sus propios campos sin columnas nulas de relleno (por ejemplo, fecha_limite solo en Tarea).
- En contra: la lógica se repite (CRUD, estados, permisos) y las consultas transversales necesitan UNION o varias consultas.

Motivo: en este proyecto los tres niveles son fijos y se prioriza la integridad referencial y la claridad del esquema.

### Proyecto_id directo en Tarea

Se guarda el proyecto en la tarea para comprobar la pertenencia al proyecto sin recorrer US y Épica. Riesgo: que el proyecto de la tarea no coincida con el de su US. La forma de evitarlo está pendiente de decidir.

## Decisiones pendientes

- Tabla de permisos por rol (ADMIN global, EDITOR, USUARIO) para cada acción de la API.
- Renombrar los roles de proyecto para que no choquen con el rol global (USUARIO).
- Estado para descartar trabajo que ya no hace falta (por ejemplo CANCELADO).
- Si se puede crear una tarea dentro de una US cerrada.
- Transiciones de estado permitidas.
- Qué ocurre con las asignaciones de un usuario que sale del proyecto.
- Política de borrado en cascada por nivel (CASCADE o RESTRICT).
- Si un proyecto puede quedarse sin ningún editor.
- Idioma de los nombres en el código y las tablas.

## MVP

Por definir.

## Cómo ejecutarlo

Por definir.

## Hoja de ruta

- [ ] Cerrar el modelo de datos
- [ ] Definir el MVP y las historias de usuario
- [ ] Estructura del repositorio y entorno con Docker Compose
- [ ] Registro y login
- [ ] CRUD de proyectos, épicas, US y tareas
- [ ] Roles por proyecto y asignaciones
- [ ] Tests de integración y pipeline en GitHub Actions
- [ ] Documentación de la API (OpenAPI)
