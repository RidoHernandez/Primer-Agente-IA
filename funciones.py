def sumar(a, b):
    return a + b

def restar(a, b):
    return a - b

import os
def leer(nombre):
    try:
        if not os.path.exists(nombre):
            return f"Error: El archivo '{nombre}' no existe."
            
        with open(nombre, "r", encoding="utf-8") as archivo:
            contenido = archivo.read()
            return contenido if contenido else "El archivo está vacío."
    except Exception as e:
        return f"Error al leer el archivo: {str(e)}"

def escribir(nombre, contenido):
    try:
        directorio = os.path.dirname(nombre)
        if directorio:
            os.makedirs(directorio, exist_ok=True)
            
        with open(nombre, "w", encoding="utf-8") as archivo:
            archivo.write(contenido)
        return f"Éxito: Archivo '{nombre}' guardado correctamente."
    except Exception as e:
        return f"Error al escribir el archivo: {str(e)}"
    
    
def archivo_cpp(nombre, contenido):
    try:
        if not nombre.endswith(".cpp"):
            nombre += ".cpp"
        with open(nombre, "w", encoding="utf-8") as archivo:
            archivo.write(contenido)
        return f"Exito: Archivo C++ {nombre} guardado correctamente."
    except Exception as e:
        return f"Error al crear el archivo C++: {str(e)}"


import os 
def crear_directorio(nombre):
    try:
        os.makedirs(nombre, exist_ok=True)
        return f"Exito: La carpeta {nombre}  fue creada."
    except Exception as e:
        return f"Error no se pudo crear la carpeta {str(e)}."
    


import subprocess
def compilar_y_ejecutar_cpp(archivo_cpp, entrada_txt="input.txt"):
    try:
        if not archivo_cpp.endswith(".cpp"):
            archivo_cpp += ".cpp"
            
        ejecutable = archivo_cpp.replace(".cpp", ".exe")
        ruta_ejecutable = os.path.abspath(ejecutable)

        compilacion = subprocess.run(
            ["g++", archivo_cpp, "-o", ejecutable],
            capture_output=True, text=True, timeout=10
        )
        
        if compilacion.returncode != 0:
            return f"Error de Compilación:\n{compilacion.stderr}"

        if not os.path.exists(entrada_txt):
            return f"Error: No se encontró el archivo de entrada '{entrada_txt}'."

        with open(entrada_txt, "r", encoding="utf-8") as f_in:
            ejecucion = subprocess.run(
                [ruta_ejecutable],
                stdin=f_in, 
                capture_output=True, 
                text=True, 
                timeout=5
            )
        
        return f"Salida del Programa:\n{ejecucion.stdout}"
        
    except subprocess.TimeoutExpired:
        return "Error: El programa tardó demasiado en responder (posible bucle infinito o TLE)."
    except Exception as e:
        return f"Error durante la ejecución: {str(e)}"
    

import chromadb
from openai import OpenAI

cliente_ollama = OpenAI(
    base_url="http://127.0.0.1:11434/v1",
    api_key="ollama"
)

chroma_client = chromadb.PersistentClient(path="./chroma_db")
coleccion = chroma_client.get_or_create_collection(name="documentos_pdf")


def buscar_en_pdf(consulta, n_resultados=3):
    try:
        respuesta = cliente_ollama.embeddings.create(
            model="nomic-embed-text",
            input=consulta
        )
        query_vector = respuesta.data[0].embedding

        resultados = coleccion.query(
            query_embeddings=[query_vector],
            n_results=n_resultados
        )

        documentos = resultados.get("documents", [[]])[0]
        if not documentos:
            return "No se encontró información relevante en el PDF."

        contexto = "\n\n---\n\n".join(documentos)
        return f"Fragmentos extraídos del PDF:\n\n{contexto}"

    except Exception as e:
        return f"Error al buscar en el PDF: {str(e)}"