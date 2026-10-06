# creamos el acceso a esa herramienta asi como la referencia a ella
herramienta_sumar = {
    "type": "function",
    "function": {
        "name": "sumar",
        "description": "Suma dos numeros",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {
                    "type": "number",
                    "description": "Primer numero"
                },
                "b": {
                    "type": "number",
                    "description": "Segundo numero"
                }
            },
            "required": ["a", "b"]
        }
    }
}


herramienta_restar = {
    "type": "function",
    "function": {
        "name": "restar",
        "description": "Resta dos numeros",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {
                    "type": "number",
                    "description": "Primer numero"
                },
                "b": {
                    "type": "number",
                    "description": "Segundo numero"
                }
            },
            "required": ["a", "b"]
        }
    }
}


herramienta_leer = {
    "type": "function",
    "function": {
        "name": "leer",
        "description": "Lee y devuelve el contenido de un archivo de texto o código fuente. Acepta rutas relativas (ejemplo: 'mi_proyecto/index.html').",
        "parameters": {
            "type": "object",
            "properties": {
                "nombre": {
                    "type": "string",
                    "description": "El nombre o la ruta relativa del archivo a leer (ejemplo: 'index.html' o 'mi_proyecto/index.html')."
                }
            },
            "required": ["nombre"]
        }
    }
}


herramienta_escribir = {
    "type": "function",
    "function": {
        "name": "escribir",
        "description": "Escribe o crea un archivo de texto con el contenido especificado. Crea automáticamente las carpetas intermedias si el nombre del archivo incluye una ruta (ejemplo: 'mi_app/index.html').",
        "parameters": {
            "type": "object",
            "properties": {
                "nombre": {
                    "type": "string",
                    "description": "El nombre o la ruta relativa del archivo a crear (ejemplo: 'output.txt' o 'mi_proyecto/index.html')."
                },
                "contenido": {
                    "type": "string",
                    "description": "El texto o código fuente completo que se escribirá en el archivo."
                }
            },
            "required": ["nombre", "contenido"]
        }
    }
}



herramienta_archivo_cpp = {
    "type": "function",
    "function": {
        "name": "archivo_cpp",
        "description": "Crea o sobrescribe un archivo fuente de C++ (.cpp) con el código fuente proporcionado.",
        "parameters": {
            "type": "object",
            "properties": {
                "nombre": {
                    "type": "string",
                    "description": "El nombre del archivo .cpp a crear (ejemplo: 'solucion.cpp' o 'main')"
                },
                "contenido": {
                    "type": "string",
                    "description": "El código fuente completo de C++ que se guardará en el archivo (incluyendo los #include y la función main)."
                }
            },
            "required": ["nombre", "contenido"]
        }
    }
}


herramienta_crear_directorio = {
    "type":"function",
    "function":{
        "name":"crear_directorio",
        "description":"Crear una nueva carpeta en la ruta actual si no existe",
        "parameters":{
            "type":"object",
            "properties":{
                "nombre":{
                    "type":"string",
                    "description":"El nombre o ruta de la carpeta a crear (ejemplo: 'mi_landing_page')"
                }
            },
            "required":["nombre"]
        }
    }
}

herramienta_compilar_y_ejecutar = {
    "type": "function",
    "function": {
        "name": "compilar_y_ejecutar_cpp",
        "description": "Compila un archivo de C++ (.cpp) usando g++ y lo ejecuta pasando un archivo de entrada (por defecto input.txt). Retorna la salida del programa o el error de compilación.",
        "parameters": {
            "type": "object",
            "properties": {
                "archivo_cpp": {
                    "type": "string",
                    "description": "Nombre del archivo C++ a compilar (ejemplo: 'solucion.cpp')"
                },
                "entrada_txt": {
                    "type": "string",
                    "description": "Nombre del archivo de texto con la entrada del problema (ejemplo: 'input.txt')"
                }
            },
            "required": ["archivo_cpp"]
        }
    }
}


herramienta_buscar_en_pdf = {
    "type": "function",
    "function": {
        "name": "buscar_en_pdf",
        "description": "Busca y recupera los fragmentos de texto más relevantes almacenados en la base de datos del PDF para responder dudas sobre el documento.",
        "parameters": {
            "type": "object",
            "properties": {
                "consulta": {
                    "type": "string",
                    "description": "El tema, término o pregunta específica a buscar dentro del PDF."
                }
            },
            "required": ["consulta"]
        }
    }
}