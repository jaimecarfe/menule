# MenULE

**MenULE** es una aplicación de escritorio desarrollada como proyecto final de la asignatura Ingeniería del Software. Está diseñada para gestionar un sistema completo de reservas, menús y pagos en un comedor universitario.

## 🎯 Objetivos del proyecto
- Permitir la gestión de usuarios según roles: estudiante, profesor, visitante, personal de comedor, administrador.
- Facilitar la reserva de menús y pedidos diarios.
- Supervisar pagos, incidencias y estadísticas del servicio.
- Proveer interfaces diferenciadas por tipo de usuario.

## 🧱 Estructura del proyecto
```
src/
├── vista/              # Interfaces de usuario (.py y .ui)
├── controlador/        # Controladores por rol y vista
├── modelo/
│   ├── dao/            # Acceso a datos
│   ├── vo/             # Objetos de valor
│   └── BussinessObject.py  # Lógica de negocio central
└── main.py             # Punto de entrada principal
```

## 🧑‍💻 Roles y funcionalidades
| Rol               | Funcionalidades clave                          |
|------------------|-----------------------------------------------|
| Estudiante        | Reservar comida, historial, reportar errores |
| Profesor          | Reservar comida, historial                   |
| Visitante         | Hacer reservas rápidas sin cuenta           |
| Personal Comedor  | Procesar pedidos, gestionar stock           |
| Administrador     | Gestión de usuarios, menús, estadísticas    |

## 🛠 Tecnologías utilizadas
- Python 3.x
- PyQt5
- SQLite (MySQL compatible)
- MVC + DAO + VO como patrón de arquitectura

## 🚀 Cómo ejecutar
1. Clona el repositorio:
```bash
git clone https://github.com/tuusuario/menule.git
```
2. Instala las dependencias necesarias:
```bash
pip install -r requirements.txt
```
3. Ejecuta la aplicación:
```bash
python main.py
```

## 📌 Créditos
Proyecto desarrollado por el equipo de Ingeniería del Software - Curso 2024/2025.