# Gestor de proyectos y tareas

API REST para gestionar proyectos con una jerarquía Proyecto > Épica > User Story > Tarea, con roles por proyecto y asignación de tareas a un usuario.

Proyecto personal de formación. El objetivo es practicar las funcionalidades habituales de un backend (API, base de datos, autenticación, tests, Docker, CI/CD) y documentar las decisiones tomadas por el camino.

## Estado del proyecto

- Fase actual: persistencia (modelos hechos, migraciones con Alembic en curso).

## Stack

- Lenguaje: Python
- Framework: FastAPI
- Base de datos: PostgreSQL
- Previsto: SQLAlchemy (ORM), Alembic (migraciones), pytest, Docker Compose, GitHub Actions
- Frontend: por decidir

## Modelo de datos

### Entidades

**Usuario**
- id (PK), username (único), nombre, apellidos, email (único), password_hash
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
- id (PK), creador_id (FK), us_id (FK), titulo, descripcion (opcional)
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

### Borrado Mixto

El borrado en tablas intermedias y en la jerarquía: Proyecto > Épica > User Story > Tarea, será "CASCADE". Sin embargo, en creador_id y asignado_por será "RESTRICTED". 
Esto se ha decidido ya que si se elimina un proyecto se eliminará en consecuencia todo lo que hay debajo. Por otro lado, si el creador de una tarea se elimina, no tiene por qué eliminarse también la tarea.

### Tarea no guarda proyecto_id

El proyecto se obtiene por US y épica. Así no puede haber incoherencia entre la tarea y su US, a costa de joins.

## Decisiones pendientes

- Tabla de permisos por rol (ADMIN global, EDITOR, USUARIO) para cada acción de la API.
- Renombrar los roles de proyecto para que no choquen con el rol global (USUARIO).
- Qué ocurre con las asignaciones de un usuario que sale del proyecto.
- Si un proyecto puede quedarse sin ningún editor.
- Idioma de los nombres en el código y las tablas.

## MVP

Sistema para que equipos de trabajo desglosen el trabajo (proyecto, épica, user story y tarea), se repartan las tareas y avancen en una misma dirección. La primera versión incluye solo lo básico para que el sistema funcione, y se expone como API REST documentada con Swagger (sin frontend).

### Historias de usuario

- Como usuario quiero registrarme proporcionando username, correo, contraseña y mis datos personales.
- Como usuario quiero iniciar sesión con mi correo o con mi username.
- Como administrador quiero crear proyectos para distribuir el trabajo (solo los administradores pueden crearlos).
- Como usuario quiero conocer los proyectos a los que pertenezco.
- Como editor de un proyecto quiero crear épicas, user stories y tareas.
- Como editor de un proyecto quiero añadir usuarios (entran con rol USUARIO).
- Como editor de un proyecto quiero cambiar el rol de un miembro para hacerlo editor.
- Como usuario quiero ver la lista de tareas planificadas de un proyecto.
- Como usuario quiero asignarme tareas planificadas (pasan a EN_CURSO).
- Como usuario quiero listar mis tareas en curso de un proyecto para planificar mi trabajo.
- Como usuario quiero cambiar el estado de las tareas que tengo asignadas (incluido cerrarlas).
- Como editor quiero cerrar un proyecto cuando todas sus épicas estén cerradas.

### Ciclo de vida de una tarea

- Transiciones permitidas: PLANIFICADO a EN_CURSO, EN_CURSO a CERRADO y EN_CURSO a PLANIFICADO.
- No se puede pasar de PLANIFICADO a CERRADO directamente.
- Autoasignarse una tarea la pasa a EN_CURSO.
- Volver a PLANIFICADO elimina la asignación.
- CERRADO es un estado final: no se reabre, se crea una tarea nueva.
- Cada tarea tiene un único responsable en el MVP (restricción UNIQUE sobre tarea_id en la tabla de asignaciones).

### Reglas de negocio del MVP

- El primer administrador se crea mediante promoción manual en la base de datos.
- El creador de un proyecto entra automáticamente como EDITOR.
- Una US se cierra automáticamente cuando todas sus tareas están cerradas.
- Una épica se cierra automáticamente cuando todas sus US están cerradas.
- El cierre del proyecto es manual y solo es posible con todas las épicas cerradas.
- No se pueden crear elementos hijos dentro de un padre cerrado.
- Solo se puede asignar una tarea a miembros del proyecto.

### Fuera del MVP

- Invitaciones a otros usuarios para colaborar en tareas.
- Editar y borrar épicas, user stories y tareas (cambiar el estado sí está incluido).
- Borrar proyectos y quitar miembros.
- Frontend.
- Despliegue en cloud.

## Cómo ejecutarlo

- Crear venv -> python -m venv .venv
- pip install -r requirements.txt
- opiar .env.example a .env
- uvicorn src.main:app --reload

## Hoja de ruta

- [ ] Estructura del repositorio y entorno con Docker Compose
- [ ] Registro y login
- [ ] CRUD de proyectos, épicas, US y tareas
- [ ] Roles por proyecto y asignaciones
- [ ] Tests de integración y pipeline en GitHub Actions
- [ ] Documentación de la API (OpenAPI)
