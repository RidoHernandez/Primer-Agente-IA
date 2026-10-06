from dotenv import load_dotenv
from openai import OpenAI
import os
import json

from funciones import sumar, restar, leer, escribir
from herramientas import (
    herramienta_restar,
    herramienta_leer,
    herramienta_sumar,
    herramienta_escribir
)

funciones = {
    "sumar": sumar,
    "restar": restar,
    "leer": leer,
    "escribir": escribir
}

cliente = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

mensajes = [{"role": "system", "content": "Eres un experto en programación competitiva. Responde SIEMPRE en español de manera clara y breve."}]

while True:
    pregunta = input("\nRido 117 : ")

    if pregunta == "FIN": break
    
    mensajes.append({"role": "user", "content": pregunta})

    while True:
        response = cliente.chat.completions.create(
            model="qwen2.5-coder:7b", 
            messages=mensajes,
            tools=[herramienta_sumar, herramienta_restar, herramienta_leer, herramienta_escribir],
            tool_choice="auto",
            temperature=0.1,
            max_tokens=2000  
        )
        
        mensaje_respuesta = response.choices[0].message
        
        if mensaje_respuesta.tool_calls:
            print("\n[!] El modelo decidió usar herramientas...")
            
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
            respuesta_final = mensaje_respuesta.content
            print("\nRespuesta del modelo:", respuesta_final)
            
            mensajes.append({"role": "assistant", "content": respuesta_final})
            break
