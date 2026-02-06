Plataforma de Estandarización y Gobernanza de Proyectos

1. 🧭 Visión del Producto

Construir una plataforma interna para PMs y equipos técnicos que permita:

Crear nuevos proyectos de software bajo estándares técnicos obligatorios

Automatizar tareas repetitivas de configuración

Imponer buenas prácticas de ingeniería desde el primer commit

Asegurar calidad, gobernanza y consistencia entre repositorios

La plataforma será el punto único de creación y configuración de proyectos dentro de la organización.

2. 🎯 Objetivos

Objetivos principales

Estandarizar la arquitectura base de los proyectos

Reducir errores humanos en configuraciones iniciales

Garantizar reglas de calidad y revisión de código

Automatizar la integración con GitLab

No objetivos (por ahora)

No gestionará releases ni hotfixes desde el dashboard

No incluirá métricas de calidad (Sonar, cobertura, etc.)

No reemplaza GitLab, lo orquesta

3. 👥 Usuarios

Rol Qué puede hacer
PM Crear proyectos y visualizar estado
Admin Control total

4. 🏗️ Arquitectura General

Backend

Python + FastAPI

API REST

Servicios que orquestan GitLab

Frontend

Dashboard web

Creación y visualización de proyectos

Selección de miembros desde la API de GitLab

Integración externa

GitLab Self-Hosted API

5. 🚀 Flujo Principal — Creación de Proyecto

Cuando un usuario crea un proyecto desde el dashboard:

Paso 1 — Crear proyecto en GitLab

Se crea dentro de un grupo definido

Visibilidad privada

Paso 2 — Primer commit automático

Se sube un template generado por el backend que incluye:

Estructura base del proyecto

.gitlab-ci.yml

.pre-commit-config.yaml

CODEOWNERS

README

Configuración base de FastAPI

Paso 3 — Crear ramas base (GitFlow)
Rama Base Propósito
main — Producción
develop main Integración
Paso 4 — Proteger ramas
main

No push directo

Merge solo Maintainers

MR obligatorio

develop

No push directo

Merge vía MR

release/_ y hotfix/_

Protegidas por wildcard

Solo Maintainers pueden mergear

Paso 5 — Configurar reglas de Merge Request

Para main y develop:

Pipeline debe pasar

Aprobaciones obligatorias

Requiere revisión de Code Owners

No self-approval

Paso 6 — CODEOWNERS

Archivo incluido en el primer commit:

Define responsables de áreas críticas

Protege CI/CD y configuración

Paso 7 — Agregar miembros al repositorio

Desde selección hecha en el frontend, el backend:

Obtiene usuarios desde GitLab API

Los asigna al proyecto con roles:

Rol plataforma Rol GitLab
Developer Developer
Tech Lead Maintainer
PM Reporter 6. 🌳 Estrategia de ramas oficial — GitFlow
Tipo Patrón Merge hacia
Feature feature/_ develop
Release release/_ main + develop
Hotfix hotfix/\* main + develop

La plataforma no crea automáticamente ramas feature/release/hotfix, solo define reglas.

7. 🔐 Seguridad y Gobernanza

Todas las ramas críticas protegidas

CODEOWNERS obligatorio

Cambios a CI requieren aprobación

Solo la plataforma crea repos iniciales

8. 📌 Endpoint principal
   POST /projects

Crea un proyecto completo con gobernanza aplicada.

Request
{
"name": "payments-api",
"members": [
{ "gitlab_user_id": 12, "role": "maintainer" },
{ "gitlab_user_id": 44, "role": "developer" }
]
}

Response
{
"repo_url": "git@gitlab:group/payments-api.git"
}

10. 🧠 Resultado esperado

Cada proyecto creado desde la plataforma:

✅ Tiene arquitectura estándar
✅ Tiene CI/CD configurado
✅ Usa GitFlow
✅ Tiene ramas protegidas
✅ Exige revisiones y aprobaciones
✅ Tiene responsables definidos
✅ Tiene equipo asignado correctamente

11. 🗺️ Roadmap futuro (fuera de este PRD)

Integración con Sonar

Integracion con Logfire

Métricas de calidad en dashboard

Health score de proyectos
