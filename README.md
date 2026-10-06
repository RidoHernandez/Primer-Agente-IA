# Agente IA Local con Ollama y Python

Un agente de inteligencia artificial modular y local diseñado para la programación, gestión de proyectos y análisis avanzado de documentos mediante RAG (Retrieval-Augmented Generation), operando completamente en local sin dependencias externas ni servicios de pago.

## Stack Tecnológico

- **Modelo Principal:** `qwen2.5-coder:7b` (a través de Ollama) como el cerebro del agente.
- **Embeddings:** `nomic-embed-text` para la vectorización de texto.
- **Base de Datos Vectorial:** ChromaDB para el almacenamiento y búsqueda semántica local.
- **Procesamiento de PDF:** PyMuPDF (`fitz`) para la extracción de texto.
- **Lenguaje:** Python con entorno virtual (`.venv`).

## Herramientas Disponibles (Tools)

El agente cuenta con un parser multi-herramienta capaz de ejecutar acciones de manera autónoma:

### Gestión de Archivos y Directorios
- **`crear_directorio`**: Crea nuevas carpetas en la estructura del proyecto.
- **`escribir`**: Crea o modifica archivos con contenido de texto o código.
- **`leer`**: Lee el contenido de archivos locales existentes.

### Lógica y Matemáticas
- **`sumar`**: Realiza operaciones aritméticas de suma.
- **`restar`**: Realiza operaciones aritméticas de resta.

### Recuperación de Información (RAG)
- **`buscar_en_pdf`**: Realiza búsquedas semánticas vectoriales sobre los documentos PDF ingestados en la base de datos local (`chroma_db`), permitiendo consultar múltiples archivos simultáneamente mediante similitud geométrica y mapeo de conceptos.

## Estructura del Proyecto

- `coder.py`: Bucle principal del agente y gestión de llamadas a herramientas.
- `funciones.py`: Implementación lógica de cada función o tool.
- `herramientas.py`: Definición de los esquemas JSON para el funcionamiento del LLM.
- `ingestar_pdf.py`: Script encargado de procesar, fragmentar (*chunking*), vectorizar e indexar PDFs en ChromaDB.
