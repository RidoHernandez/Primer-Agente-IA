from dotenv import load_dotenv
from openai import OpenAI
import os
import json

from funciones import sumar, restar, leer, escribir, crear_directorio, buscar_en_pdf
from herramientas import (
    herramienta_restar,
    herramienta_leer,
    herramienta_sumar,
    herramienta_escribir,
    herramienta_crear_directorio,
    herramienta_buscar_en_pdf
)

funciones = {
    "sumar": sumar,
    "restar": restar,
    "leer": leer,
    "escribir": escribir,
    "crear_directorio": crear_directorio,
    "buscar_en_pdf":buscar_en_pdf
}

cliente = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

mensajes = [
    {
        "role": "system", 
        "content": (
            "Eres un agente experto en programación. Tienes acceso a herramientas.\n"
            "REGLAS ESTRICTAS:\n"
            "1. Si necesitas usar herramientas, devuelve los objetos JSON correspondientes sin texto explicativo.\n"
            "2. Cuando recibas los resultados de las herramientas, analízalos. Si faltan tareas, ejecuta más herramientas.\n"
            "3. Si completaste todo, da tu respuesta final conversacional en español."
        )
    }
]

while True:
    pregunta = input("\nRido 117 : ")

    if pregunta == "FIN": break
    
    mensajes.append({"role": "user", "content": pregunta})

    while True:
        response = cliente.chat.completions.create(
            model="qwen2.5-coder:7b", 
            messages=mensajes,
            tools=[herramienta_sumar, herramienta_restar, herramienta_leer, herramienta_escribir, herramienta_crear_directorio, herramienta_buscar_en_pdf],
            tool_choice="auto",
            temperature=0.1,   
            max_tokens=2000  
        )
        
        mensaje_respuesta = response.choices[0].message
        
        if mensaje_respuesta.tool_calls:
            print("\n[!] El modelo decidió usar herramientas (nativo)...")
            mensajes.append(mensaje_respuesta)
            
            for tool_call in mensaje_respuesta.tool_calls:
                nombre_funcion = tool_call.function.name
                print(f"Ejecutando: {nombre_funcion}")
                
                funcion_a_llamar = funciones[nombre_funcion]
                argumentos = json.loads(tool_call.function.arguments)
                
                resultado = funcion_a_llamar(**argumentos)
                print(f"Salida de la función: {resultado}")
                
                mensajes.append({
                    "role": "tool",               
                    "tool_call_id": tool_call.id, 
                    "content": str(resultado)     
                })            
        
        else:
            texto = mensaje_respuesta.content
            if not texto: texto = ""
            texto = texto.strip()
            
            decoder = json.JSONDecoder()
            pos = 0
            herramientas_encontradas = []

            while pos < len(texto):
                inicio_json = texto.find('{', pos)
                if inicio_json == -1:
                    break
                try:
                    obj, cant_caracteres = decoder.raw_decode(texto[inicio_json:])
                    if isinstance(obj, dict) and "name" in obj and "arguments" in obj:
                        herramientas_encontradas.append(obj)
                    pos = inicio_json + cant_caracteres
                except json.JSONDecodeError:
                    pos = inicio_json + 1

            if herramientas_encontradas:
                mensajes.append({"role": "assistant", "content": texto})
                resultados_acumulados = []

                for datos_tool in herramientas_encontradas:
                    nombre_funcion = datos_tool["name"]
                    argumentos = datos_tool.get("arguments", {})

                    print(f"\n[Fallback] Ejecutando herramienta: {nombre_funcion}")

                    if nombre_funcion in funciones:
                        funcion_a_llamar = funciones[nombre_funcion]
                        resultado = funcion_a_llamar(**argumentos)
                        print(f"Salida: {resultado}")
                        resultados_acumulados.append(f"Resultado de {nombre_funcion}: {resultado}")
                    else:
                        print(f"Error: La función '{nombre_funcion}' no existe.")

                mensaje_parada = (
                    "\n".join(resultados_acumulados) + "\n"
                    "Si necesitas usar otra herramienta para continuar, devuelve el JSON. "
                    "Si ya terminaste la tarea, responde en texto conversacional normal para concluir."
                )
                mensajes.append({"role": "user", "content": mensaje_parada})

            else:
                print("\nRespuesta del modelo:\n", texto)
                mensajes.append({"role": "assistant", "content": texto})
                break
            