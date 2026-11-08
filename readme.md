# Enterprise Inventory Management & Advanced Analytics System

> Sistema profesional de control de inventarios, analítica predictiva y Machine Learning desarrollado bajo principios estrictos de **Clean Architecture** (Arquitectura Limpia), optimizado para alta concurrencia de consultas y preparado para escalar a motores corporativos como PostgreSQL.

---

## Arquitectura y Estructura del Proyecto

El proyecto se encuentra estrictamente modularizado para garantizar el desacoplamiento de responsabilidades, alta testabilidad y un mantenimiento limpio:

```text
├── analytics/              # Módulos de Ciencia de Datos y Estadística Avanzada
│   ├── abc_analytics.py    # Clasificación ABC financiera de inventario
│   ├── anomaly_detection.py# Detección de anomalías operativas
│   ├── inventory_math.py   # Modelos matemáticos (Stock de seguridad y EOQ)
│   ├── kmeans_segmentation.py# Segmentación multicriterio por Aprendizaje No Supervisado
│   ├── kpis.py             # Motor de cálculo de indicadores clave de salud logística
│   ├── ml_forecasting.py   # Pronóstico de demanda con Machine Learning Tabular (LightGBM)
│   └── stock_forecast.py   # Proyecciones estadísticas de consumo
├── config/                 # Configuraciones globales del sistema y parámetros
│   └── settings.py         # Variables de entorno y rutas base
├── database/               # Capa de persistencia y motor de base de datos
│   ├── connection.py       # Gestor de conexiones optimizado con SQLite WAL
│   ├── migration.py        # Control de migraciones y esquemas iniciales
│   └── schema.sql          # Definición de tablas, índices y triggers relacionales
├── models/                 # Entidades de dominio y estructuras de datos
│   ├── movement.py         # Modelo de transacciones de inventario
│   ├── product.py          # Modelo de SKUs y atributos de productos
│   └── warehouse.py        # Modelo de gestión multialmacén/bodegas
├── repository/             # Patrón Repositorio (Abstracción de consultas a base de datos)
│   ├── inventory_repository.py # Consultas y operaciones atómicas de stock
│   └── movement_repository.py  # Registro de auditoría y excepciones (Kardex)
├── services/               # Lógica de negocio y orquestación de servicios
│   ├── analytics_service.py    # Orquestación de métricas de BI
│   ├── forecasting_service.py  # Cálculo de órdenes de compra sugeridas
│   ├── inventory_service.py    # Reglas de negocio para entradas y salidas
│   ├── movement_service.py     # Procesamiento de cargas masivas (Excel/CSV)
│   ├── pdf_report_service.py   # Generación de reportes ejecutivos en PDF
│   ├── validation_service.py   # Validaciones de integridad y stock
│   └── webhook_service.py      # Envío de alertas automatizadas (Telegram/Webhooks)
├── tests/                  # Suite de pruebas unitarias e integración
│   ├── test_analytics.py
│   ├── test_inventory.py
│   └── test_movements.py
├── ui/                     # Capa de presentación (Interfaz gráfica con Streamlit)
│   ├── alerts.py           # Vista de anomalías y alertas críticas
│   ├── dashboard.py        # Panel de indicadores generales y salud logística
│   ├── inventory.py        # Visualización de stock actual y bodegas
│   ├── movements.py        # Registro manual, carga masiva y pruebas de estrés
│   └── reports.py          # Reportes inteligentes, ML y exportación ejecutiva
├── .streamlit/             # Configuración y temas de la interfaz web
├── app.py                  # Punto de entrada principal (Orquestador de Streamlit)
├── requirements.txt        # Dependencias y librerías del sistema
└── README.md               # Documentación oficial del proyecto
```

⚡ Rendimiento, Concurrencia y Escalabilidad
Concurrencia con SQLite WAL (Write-Ahead Logging):

El sistema está configurado a nivel de conexión para operar con el modo WAL de SQLite (evidenciado en los archivos .db-wal y .db-shm del directorio). Esto permite múltiples consultas de lectura simultáneas sin bloquear las operaciones de escritura concurrentes, optimizando el rendimiento de la aplicación web en tiempo real.

Preparado para Escalar a PostgreSQL:

Gracias al diseño modular basado en el Patrón Repositorio (repository/), la transición desde SQLite hacia un motor relacional pesado como PostgreSQL es transparente, requiriendo únicamente la adaptación de la capa de conexión en database/connection.py para soportar infraestructuras corporativas masivas.

Capacidades Analíticas y Machine Learning
Pronóstico de Demanda Inteligente (ml_forecasting.py): Modelos tabulares basados en árboles de decisión (LightGBM) que procesan series temporales históricas para anticipar la demanda a 30 días por SKU.

Segmentación Multicriterio (kmeans_segmentation.py): Algoritmos de Aprendizaje No Supervisado (K-Means) que agrupan el inventario evaluando simultáneamente el valor financiero, la frecuencia y la volatilidad de la demanda.

Optimización Matemática del Inventario (inventory_math.py): Cálculo automatizado de Stock de Seguridad probabilístico basado en el Nivel de Servicio deseado y el Punto de Reorden dinámico.

Instalación y Configuración
1. Clonar el repositorio
Bash

git clone 

cd control_inventario


2. Crear y activar entorno virtual
Bash

python -m venv venv
# En Linux/macOS:
source venv/bin/activate
# En Windows:
venv\Scripts\activate

3. Instalar dependencias
Bash

pip install -r requirements.txt



Instala las dependencias necesarias mediante el gestor de paquetes de Python (omitiendo restricciones de entornos virtuales si prefieres instalación directa en el sistema):

Bash
pip install --break-system-packages -r requirements.txt
Ejecuta la aplicación web interactiva con Streamlit:

Bash
streamlit run app.py


video demo 

