# 🌍 Proyecto REST Countries: Análisis y Visualización de Datos Geográficos y Demográficos  

## **Introducción**  
El **Proyecto REST Countries** es una solución modular desarrollada en Python que automatiza el procesamiento de datos geográficos y demográficos de 250+ países mediante la API pública [REST Countries](https://restcountries.com). Integra conceptos de las tres fases del curso de **Programación Básica en Python**, aplicando técnicas de adquisición de datos, análisis estadístico y visualización gráfica. Este proyecto elimina el trabajo manual repetitivo, permitiendo enfocarse en la interpretación de resultados.  

---

## **Descripción del Proyecto**  
### **Problema Resuelto**  
La API REST Countries proporciona datos estructurados, pero estos no están listos para análisis inmediato. Este proyecto automatiza:  
- Descarga de datos desde la API.  
- Estructuración de información en listas de diccionarios.  
- Filtrado avanzado con expresiones regulares.  
- Análisis estadístico (media, mediana, varianza).  
- Generación de gráficos (barras, líneas).  
- Exportación a formatos reutilizables (JSON, Excel).  

### **API REST Countries**  
La API REST Countries (v3.1) es una fuente gratuita de datos geográficos y demográficos actualizados. Su uso permite:  
- Acceso a datos estructurados (JSON).  
- Integración automática sin intervención manual.  
- Escalabilidad para análisis masivo.  

#### **Endpoints Clave**  
| **Endpoint** | **Descripción** |  
|--------------|------------------|  
| `https://restcountries.com/v3.1/all` | Obtiene todos los países |  
| `https://restcountries.com/v3.1/name/{nombre}` | Busca por nombre |  
| `https://restcountries.com/v3.1/independent?status=true` | Filtra por independencia |  

#### **Comparación con Otras APIs**  
| **API** | **Autenticación** | **Casos de Uso** |  
|---------|-------------------|--------------------|  
| **REST Countries** | No | Análisis geográfico, demográfico |  
| **Country API** | No | Búsquedas básicas |  
| **World Bank Data API** | No | Indicadores económicos |  

**Ventajas de REST Countries**:  
- Datos completos (nombre, población, área, idiomas, monedas).  
- Sin autenticación requerida.  

---

## **Estructura de Datos Utilizada**  
Los datos se almacenan en **listas de diccionarios** para facilitar su manipulación:  
```python
{
    "Nombre": str,
    "Población": int,
    "Área (km²)": int,
    "Densidad (hab/km²)": float,
    "Región": str,
    "Subregión": str,
    "Idiomas": str,
    "Monedas": str
}
```  

**Ejemplo de Salida**:  
```json
[
  {
    "Nombre": "Colombia",
    "Población": 50882891,
    "Área (km²)": 1141748,
    "Densidad (hab/km²)": 44.57
  }
]
```  

---

## **Funciones Principales (`PIA_Modulo.py`)**  
Este archivo contiene las funciones reutilizables que forman el núcleo del proyecto.  

### **1. `obtener_datos_paises()`**  
**Propósito**: Descargar datos crudos desde la API REST Countries.  
**Código**:  
```python
import requests

def obtener_datos_paises():
    url = "https://restcountries.com/v3.1/all"
    try:
        respuesta = requests.get(url, timeout=10)
        if respuesta.status_code == 200:
            return respuesta.json()
        else:
            print("Error: Fallo en la conexión")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None
```  
**Uso**:  
```python
from PIA_Modulo import obtener_datos_paises
datos_crudos = obtener_datos_paises()
```  

### **2. `estructurar_datos_paises(datos)`**  
**Propósito**: Convertir datos anidados en una lista de diccionarios con campos normalizados.  
**Código**:  
```python
def estructurar_datos_paises(datos):
    paises_estructurados = []
    for pais in datos:
        nombre = pais.get("name", {}).get("common", "N/A")
        poblacion = pais.get("population", 0)
        area = pais.get("area", 0)
        densidad = calcular_densidad(poblacion, area)
        paises_estructurados.append({
            "Nombre": nombre,
            "Población": poblacion,
            "Área (km²)": area,
            "Densidad (hab/km²)": densidad,
            "Región": pais.get("region", "N/A"),
            "Subregión": pais.get("subregion", "N/A"),
            "Idiomas": ", ".join(pais.get("languages", {}).values()) if pais.get("languages") else "N/A",
            "Monedas": ", ".join([f"{code} ({info['name']})" for code, info in pais.get("currencies", {}).items()]) if pais.get("currencies") else "N/A"
        })
    return paises_estructurados
```  
**Uso**:  
```python
from PIA_Modulo import estructurar_datos_paises
datos_estructurados = estructurar_datos_paises(datos_crudos)
```  

### **3. `calcular_densidad(poblacion, area)`**  
**Propósito**: Calcular la densidad poblacional (población / área).  
**Código**:  
```python
def calcular_densidad(poblacion, area):
    if area > 0:
        return round(poblacion / area, 2)
    return 0
```  
**Uso**:  
```python
densidad = calcular_densidad(50_882_891, 1_141_748)  # Colombia
```  

### **4. `guardar_datos_json(datos, nombre_archivo="datos_paises.json")`**  
**Propósito**: Guardar datos estructurados en un archivo JSON.  
**Código**:  
```python
import json

def guardar_datos_json(datos, nombre_archivo="datos_paises.json"):
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)
    print(f"Datos guardados en {nombre_archivo}")
```  
**Uso**:  
```python
from PIA_Modulo import guardar_datos_json
guardar_datos_json(datos_estructurados, "paises_filtrados.json")
```  

### **5. `filtrar_paises_con_regex(datos, patron_regex)`**  
**Propósito**: Filtrar países por patrones de texto (ej.: `^A` para nombres que empiezan con "A").  
**Código**:  
```python
import re

def filtrar_paises_con_regex(datos, patron_regex):
    regex = re.compile(patron_regex, re.IGNORECASE)
    return [pais for pais in datos if regex.search(pais["Nombre"])]
```  
**Uso**:  
```python
paises_filtrados = filtrar_paises_con_regex(datos_estructurados, "^A")
```  

### **6. `analizar_estadisticas(datos, campo="Población")`**  
**Propósito**: Calcular métricas como media, mediana y varianza para campos numéricos.  
**Código**:  
```python
import statistics

def analizar_estadisticas(datos, campo="Población"):
    valores = [pais[campo] for pais in datos if pais[campo] > 0]
    return {
        "Media": statistics.mean(valores),
        "Mediana": statistics.median(valores),
        "Moda": statistics.mode(valores),
        "Varianza": statistics.variance(valores),
        "Desviación Estándar": statistics.stdev(valores)
    }
```  
**Uso**:  
```python
estadisticas = analizar_estadisticas(datos_estructurados, campo="Área (km²)")
```  

### **7. `exportar_datos_excel(datos, nombre_archivo="datos_paises.xlsx")`**  
**Propósito**: Exportar datos a Excel para análisis posterior.  
**Código**:  
```python
import pandas as pd

def exportar_datos_excel(datos, nombre_archivo="datos_paises.xlsx"):
    df = pd.DataFrame(datos)
    df.to_excel(nombre_archivo, index=False, engine="openpyxl")
    print(f"Datos exportados exitosamente a {nombre_archivo}")
```  
**Uso**:  
```python
exportar_datos_excel(datos_estructurados, "paises_filtrados.xlsx")
```  

### **8. `graficar_datos(datos, tipo_grafico="barras", campo_x="Nombre", campo_y="Población")`**  
**Propósito**: Generar gráficos de barras o líneas para visualizar tendencias.  
**Código**:  
```python
import matplotlib.pyplot as plt

def graficar_datos(datos, tipo_grafico="barras", titulo="Gráfico", eje_x="X", eje_y="Y", campo_x="Nombre", campo_y="Población"):
    valores_x = [pais[campo_x] for pais in datos]
    valores_y = [pais[campo_y] for pais in datos]
    
    plt.figure(figsize=(12, 6))
    if tipo_grafico == "barras":
        plt.bar(valores_x, valores_y)
    elif tipo_grafico == "lineas":
        plt.plot(valores_x, valores_y, marker="o")
    
    plt.title(titulo)
    plt.xlabel(eje_x)
    plt.ylabel(eje_y)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{titulo}.png")
    plt.show()
```  
**Uso**:  
```python
graficar_datos(
    top_poblacion,
    tipo_grafico="barras",
    titulo="Top 10 Países por Población",
    eje_x="País",
    eje_y="Población"
)
```  

### **9. `interpretar_resultados(estadisticas, datos_originales=None, campo="Población")`**  
**Propósito**: Interpretar estadísticas en contexto geográfico/demográfico.  
**Código**:  
```python
def interpretar_resultados(estadisticas, datos_originales=None, campo="Población"):
    if not estadisticas:
        return "No hay estadísticas disponibles."
    
    mensaje = (
        f"Media: {estadisticas['Media']}\n"
        f"Mediana: {estadisticas['Mediana']}\n"
    )
    
    if datos_originales:
        pais_max = max(datos_originales, key=lambda x: x[campo])
        pais_min = min(datos_originales, key=lambda x: x[campo])
        mensaje += (
            f"País con mayor {campo}: {pais_max['Nombre']}\n"
            f"País con menor {campo}: {pais_min['Nombre']}"
        )
    return mensaje
```  
**Uso**:  
```python
interpretacion = interpretar_resultados(estadisticas, datos_estructurados, campo="Población")
print(interpretacion)
```  

---

## **Script Principal (`PIA_Script.py`)**  
Este archivo define el flujo completo del proyecto, integrando todas las funciones.  
**Código**:  
```python
# -*- coding: utf-8 -*-
from PIA_Modulo import (
    obtener_datos_paises,
    estructurar_datos_paises,
    guardar_datos_json,
    filtrar_paises_con_regex,
    analizar_estadisticas,
    exportar_datos_excel,
    graficar_datos,
    interpretar_resultados
)

if __name__ == "__main__":
    # 1. Descargar datos desde la API
    datos_crudos = obtener_datos_paises()
    
    # 2. Estructurar datos
    if datos_crudos:
        datos_estructurados = estructurar_datos_paises(datos_crudos)
        
        # 3. Guardar en JSON
        guardar_datos_json(datos_estructurados, "datos_paises.json")
        
        # 4. Filtrar países con regex
        patron = input("Ingrese un patrón de búsqueda (ej.: '^A' o 'land$'): ")
        paises_filtrados = filtrar_paises_con_regex(datos_estructurados, patron)
        
        # 5. Mostrar resultados del filtrado
        print(f"\nPaíses que coinciden con el patrón '{patron}':")
        for pais in paises_filtrados:
            print(f"- {pais['Nombre']} (Región: {pais['Región']}, Idiomas: {pais['Idiomas']})")
        
        # 6. Análisis estadístico de población
        print("\nAnálisis estadístico de población:")
        estadisticas = analizar_estadisticas(datos_estructurados, campo="Población")
        for clave, valor in estadisticas.items():
            print(f"{clave}: {valor}")
        
        # 7. Exportar datos a Excel
        exportar_datos_excel(datos_estructurados, "datos_paises.xlsx")
        if paises_filtrados:
            exportar_datos_excel(paises_filtrados, "paises_filtrados.xlsx")
        
        # 8. Visualizar datos
        print("\nVisualizando datos...")
        top_poblacion = sorted(datos_estructurados, key=lambda x: x["Población"], reverse=True)[:10]
        graficar_datos(
            top_poblacion,
            tipo_grafico="barras",
            titulo="Top 10 Países por Población",
            eje_x="País",
            eje_y="Población",
            campo_x="Nombre",
            campo_y="Población"
        )
        graficar_datos(
            paises_filtrados,
            tipo_grafico="lineas",
            titulo="Densidad Poblacional de Países Filtrados",
            eje_x="País",
            eje_y="Densidad (hab/km²)",
            campo_x="Nombre",
            campo_y="Densidad (hab/km²)"
        )
        
        # 9. Interpretar resultados
        print("\nInterpretación del análisis de población:")
        interpretacion = interpretar_resultados(estadisticas, datos_estructurados, campo="Población")
        print(interpretacion)
```  

---

## **Relación con los Apuntes de Programación Básica**  
| **Función** | **Fase del Curso** | **Apunte Relacionado** |  
|-------------|--------------------|------------------------|  
| `obtener_datos_paises()` | Fase III | "Automatización de tareas con APIs" |  
| `filtrar_paises_con_regex()` | Fase III | "Expresiones regulares para manipular texto" |  
| `analizar_estadisticas()` | Fase III | "Análisis de datos con estadísticas básicas" |  
| `graficar_datos()` | Fase III | "Generación de gráficos que comuniquen información" |  
| `estructurar_datos_paises()` | Fase II | "Uso de funciones y algoritmos" |  
| `exportar_datos_excel()` | Fase III | "Manipulación de hojas de cálculo" |  

---

## **Ejecución y Salida Esperada**  
### **Pasos para Ejecutar**  
1. **Instalar dependencias**:  
   ```bash
   pip install requests pandas matplotlib openpyxl
   ```  
2. **Ejecutar el script**:  
   ```bash
   python PIA_Script.py
   ```  
3. **Ingresar un patrón de búsqueda** (ej.: `^A`).  

### **Salida en Consola**  
```text
Países que coinciden con el patrón '^A':
- Australia (Región: Oceania, Idiomas: English)
- Afghanistan (Región: Asia, Idiomas: Dari, Pashto, Turkmen)
...

Análisis estadístico de población:
Media: 31361780.5
Mediana: 5026200.5
Moda: 53192
...
```  

### **Archivos Generados**  
- **JSON**: `datos_paises.json` (datos completos).  
- **Excel**: `datos_paises.xlsx` (tabla con campos normalizados).  
- **Gráficos**:  
  - `top_10_países_por_población.png` (barras).  
  - `densidad_poblacional_de_países_filtrados.png` (líneas).  

---

## **Estructura del Proyecto**  
```
REST-Countries-Project/
│
├── PIA_Modulo.py          # Módulos reutilizables (funciones)
├── PIA_Script.py          # Script principal que invoca los módulos
└── requirements.txt       # Lista de dependencias
```

**Contenido de `requirements.txt`**:  
```text
requests
pandas
matplotlib
openpyxl
```  

---

## **Conclusión**  
Este proyecto aplica los principios de las tres fases del curso:  
- **Fase I**: Fundamentos de Python (variables, ciclos, condicionales).  
- **Fase II**: Modularización y estructuras de datos anidadas.  
- **Fase III**: Integración con APIs, análisis estadístico y visualización gráfica.  

Al evitar dependencias de IDEs avanzados, se refuerza la disciplina en la programación, alineado con la metodología del curso de "construir soluciones inteligentes" desde cero.  

---

## **Referencias**  
- **CUADRO_APIs_PIA_G2.pdf**: Comparación técnica de APIs.  
- **PlanteamientoDelProblema.pdf**: Contexto académico y profesional.  
- **JustificacionDelTratamientoDeDatosAplicado.pdf**: Estrategias de filtrado y persistencia.  
- **Apuntes_Programación_básica_Python.pdf**: Fundamentos de Python, expresiones regulares, APIs y visualización.  

---

## **Fortalezas del Proyecto**  
- **Modularización**: Cada función tiene responsabilidad única, facilitando mantenimiento.  
- **Escalabilidad**: Agregar nuevos módulos (ej.: pruebas unitarias) es sencillo.  
- **Automatización**: Elimina tareas manuales repetitivas.  

---

## **Posibles Mejoras**  
1. **Validación de Entradas**: Asegurar que el patrón regex sea válido.  
2. **Interfaz Web**: Usar Flask o Streamlit para interactividad.  
3. **Pruebas Unitarias**: Validar funciones con `unittest`.  

---

## **Contribuciones y Donaciones**  
Este proyecto utiliza datos de la API REST Countries. Si lo usas en producción, considera donar en [Patreon](https://www.patreon.com/restcountries) o PayPal.  

--- 

## **Código Completo**  
- **Funciones**: Ver `PIA_Modulo.py`.  
- **Script Principal**: Ver `PIA_Script.py`.  
