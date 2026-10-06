import pymupdf as fitz
import chromadb
from openai import OpenAI
import os

cliente_ollama = OpenAI(
    base_url="http://127.0.0.1:11434/v1",
    api_key="ollama"
)


chroma_client = chromadb.PersistentClient(path="./chroma_db")
coleccion = chroma_client.get_or_create_collection(name="documentos_pdf")


def extraer_texto_pdf(ruta_pdf):
    doc = fitz.open(ruta_pdf)
    texto_completo = []
    for num_pagina, pagina in enumerate(doc):
        texto = pagina.get_text()
        if texto.strip():
            texto_completo.append({"pagina": num_pagina + 1, "texto": texto})
    return texto_completo


def dividir_en_chunks(paginas_texto, nombre_archivo, tamano_chunk=600, solapamiento=100):
    chunks = []
    id_counter = 0

    for item in paginas_texto:
        pagina = item["pagina"]
        texto = item["texto"]

        inicio = 0
        while inicio < len(texto):
            fin = inicio + tamano_chunk
            chunk_texto = texto[inicio:fin]

            chunk_id = f"{nombre_archivo}_pag_{pagina}_chunk_{id_counter}"

            chunks.append({
                "id": chunk_id,
                "texto": f"[Archivo: {nombre_archivo} | Página {pagina}]: {chunk_texto}",
                "pagina": pagina,
                "fuente": nombre_archivo
            })
            id_counter += 1
            inicio += (tamano_chunk - solapamiento)

    return chunks


def obtener_embedding(texto):
    respuesta = cliente_ollama.embeddings.create(
        model="nomic-embed-text",
        input=texto
    )
    return respuesta.data[0].embedding


def ingestar_pdf(ruta_pdf):
    nombre_archivo = os.path.basename(ruta_pdf)
    print(f"1. Extrayendo texto de '{nombre_archivo}'...")
    paginas = extraer_texto_pdf(ruta_pdf)
    
    print("2. Dividiendo el texto en fragmentos (chunks)...")
    chunks = dividir_en_chunks(paginas, nombre_archivo)
    print(f"   -> Se generaron {len(chunks)} fragmentos.")

    print("3. Generando vectores e guardando en ChromaDB...")
    for i, chunk in enumerate(chunks):
        embedding_vector = obtener_embedding(chunk["texto"])
        
        coleccion.upsert(
            ids=[chunk["id"]],
            embeddings=[embedding_vector],
            documents=[chunk["texto"]],
            metadatas=[{"fuente": chunk["fuente"], "pagina": chunk["pagina"]}]
        )
        if (i + 1) % 10 == 0 or (i + 1) == len(chunks):
            print(f"   -> Procesados {i + 1}/{len(chunks)} fragmentos.")

    print(f"\n¡Éxito! '{nombre_archivo}' ha sido añadido a la base de datos.")


if __name__ == "__main__":
    archivo_pdf = "documento.pdf" 
    
    if os.path.exists(archivo_pdf):
        ingestar_pdf(archivo_pdf)
    else:
        print(f"Coloca el archivo '{archivo_pdf}' en la carpeta del proyecto.")