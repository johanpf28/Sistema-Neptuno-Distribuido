# Sistema Distribuido Neptuno - Gestión de Productos

Este proyecto implementa un sistema distribuido basado en una **Arquitectura de 3 Capas** para la gestión de inventarios. Utiliza comunicación mediante Sockets TCP/IP entre un cliente de escritorio y un servidor en la nube.

## Arquitectura del Sistema
El sistema está diseñado siguiendo el modelo de capas para separar responsabilidades:

1.  **Capa de Presentación (Frontend):** Interfaz gráfica desarrollada en **Python** con Tkinter. Permite la entrada de datos del usuario y se ejecuta de forma local.
2.  **Capa de Negocio (Middleware):** Servidor desarrollado en **Java** encargado de recibir las conexiones, procesar la lógica de negocio y actuar como puente con la base de datos. Está alojado en **Google Cloud Platform (GCP)**.
3.  **Capa de Datos (Backend):** Base de datos relacional **MySQL** instalada en la instancia de GCP para la persistencia de la información de los productos.

---

## Detalles Técnicos y Requisitos

### Componentes de Red
* **Servidor (GCP):** `34.57.53.3`
* **Puerto de Escucha:** `5000`

### Tecnologías Utilizadas
* **Lenguajes:** Python 3.x, Java JDK 11+
* **Librerías:** Sockets (Python/Java), JDBC (MySQL Connector 8.0.28)
* **Infraestructura:** Google Compute Engine (VM Instance)

---

## Guía de Ejecución

Para un correcto funcionamiento, debe iniciarse primero el servidor y luego el cliente.

### 1. Iniciar el Middleware (En el Servidor GCP)
Accede a la terminal de tu instancia y ejecuta:
```bash
java -cp ".:mysql-connector-java-8.0.28.jar" MiddlewareNeptuno
