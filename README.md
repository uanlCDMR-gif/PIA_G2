# 🌍 Proyecto REST Countries: Análisis y Visualización de Datos Geográficos y Demográficos  

## **Descripción del Proyecto**  
### **Propósito y Objetivos**  
El **Proyecto REST Countries** es una solución modular desarrollada en Python que integra conceptos de programación básica para interactuar con la API pública [REST Countries](https://restcountries.com), extraer datos geográficos, demográficos y económicos, y transformarlos en información útil mediante análisis estadístico, visualización gráfica y exportación estructurada (JSON/Excel).  

#### **Problema Resuelto**  
La API REST Countries proporciona datos estructurados de 250+ países, pero estos no están listos para análisis inmediato. Este proyecto automatiza:  
- Descarga de datos desde la API.  
- Estructuración de información en listas de diccionarios.  
- Filtrado avanzado con expresiones regulares.  
- Análisis estadístico (media, mediana, varianza).  
- Generación de gráficos (barras, líneas).  
- Exportación a formatos reutilizables (JSON, Excel).  

Este enfoque elimina el trabajo manual repetitivo, permitiendo enfocarse en la interpretación de resultados.  

---

## **Desarrollo y Lógica Detallada de Módulos**  
### **1. `PIA_Modulo.py` - Funcionalidades Principales**  
#### **Módulo 1: Conexión a la API**  
```python
def obtener_datos_paises():
    url = "https://restcountries.com/v3.1/all"
    respuesta = requests.get(url, timeout=10)
    return respuesta.json()
```
- **Dependencias**: `requests` (instalado con `pip install requests`).  
- **Fase del Curso**: **Fase III** (aplicación de APIs y estructuras JSON).  
- **Propósito**: Descargar datos crudos desde la API REST Countries.  

#### **Módulo 2: Estructuración de Datos**  
```python
def estructurar_datos_paises(datos):
    paises_estructurados = []
    for pais in datos:
        paises_estructurados.append({
            "Nombre": pais["name"]["common"],
            "Población": pais.get("population", 0),
            "Área (km²)": pais.get("area", 0),
            "Densidad (hab/km²)": calcular_densidad(poblacion, area),
            "Región": pais.get("region", "N/A"),
            "Idiomas": ", ".join(pais.get("languages", {}).values()) or "N/A"
        })
    return paises_estructurados
```
- **Dependencias**: `statistics` (librería estándar).  
- **Fase del Curso**: **Fase II** (funciones, estructuras de datos).  
- **Propósito**: Transformar datos crudos en un formato tabular legible.  

#### **Módulo 3: Manejo de Archivos y Expresiones Regulares**  
```python
def filtrar_paises_con_regex(datos, patron_regex):
    regex = re.compile(patron_regex, re.IGNORECASE)
    return [pais for pais in datos if regex.search(pais["Nombre"])]
```
- **Dependencias**: `re` (librería estándar).  
- **Fase del Curso**: **Fase III** (manipulación de texto con regex).  
- **Propósito**: Filtrar países por patrones personalizados (ej.: `^A`, `land$`).  

#### **Módulo 4: Análisis Estadístico**  
```python
def analizar_estadisticas(datos, campo="Población"):
    valores = [pais[campo] for pais in datos if pais.get(campo, 0) > 0]
    return {
        "Media": round(statistics.mean(valores), 2),
        "Mediana": statistics.median(valores),
        "Varianza": round(statistics.variance(valores), 2)
    }
```
- **Dependencias**: `statistics` (librería estándar).  
- **Fase del Curso**: **Fase III** (análisis de datos).  
- **Propósito**: Calcular métricas clave para campos numéricos.  

#### **Módulo 5: Visualización Gráfica**  
```python
def graficar_datos(datos, tipo_grafico="barras", campo_x="Nombre", campo_y="Población"):
    valores_x = [pais[campo_x] for pais in datos]
    valores_y = [pais[campo_y] for pais in datos]
    plt.bar(valores_x, valores_y) if tipo_grafico == "barras" else plt.plot(...)
```
- **Dependencias**: `matplotlib` (instalado con `pip install matplotlib`).  
- **Fase del Curso**: **Fase III** (generación de gráficos).  
- **Propósito**: Mostrar tendencias en datos (ej.: top 10 países por población).  

#### **Módulo 6: Exportación a Excel**  
```python
def exportar_datos_excel(datos, nombre_archivo="datos_paises.xlsx"):
    df = pd.DataFrame(datos)
    df.to_excel(nombre_archivo, index=False, engine="openpyxl")
```
- **Dependencias**: `pandas`, `openpyxl` (`pip install pandas openpyxl`).  
- **Fase del Curso**: **Fase III** (manipulación de hojas de cálculo).  
- **Propósito**: Persistir datos estructurados en archivos Excel.  

#### **Módulo 7: Interpretación de Resultados**  
```python
def interpretar_resultados(estadisticas, datos_originales=None, campo="Población"):
    if not estadisticas: return "No hay estadísticas disponibles."
    # Interpreta media, mediana y dispersión
```
- **Dependencias**: Ninguna (usa lógica nativa de Python).  
- **Fase del Curso**: **Fase II** (estructuras condicionales).  
- **Propósito**: Relacionar estadísticas con contexto geográfico/demográfico.  

---

## **Creación del Entorno Virtual**  
### **Pasos para Configuración**  
1. **Crear Entorno Virtual**:  
   ```bash
   python -m venv venv
   ```
2. **Activar Entorno**:  
   - Windows:  
     ```bash
     venv\Scripts\activate
     ```
   - Linux/macOS:  
     ```bash
     source venv/bin/activate
     ```
3. **Instalar Dependencias**:  
   ```bash
   pip install requests pandas matplotlib openpyxl
   ```
4. **Generar `requirements.txt`**:  
   ```bash
   pip freeze > requirements.txt
   ```

### **Dependencias Instaladas**  
```text
requests==2.28.1
pandas==1.5.3
matplotlib==3.6.3
openpyxl==3.0.10
```

---

## **Estructura del Proyecto**  
```
REST-Countries-Project/
│
├── venv/                  # Entorno virtual
├── PIA_Modulo.py          # Módulos reutilizables (funciones)
├── PIA_Script.py          # Script principal que invoca los módulos
└── requirements.txt       # Lista de dependencias
```

---

## **Ejemplos de Uso desde la Terminal**  
### **1. Ejecutar Script Principal**  
```bash
python script.py
```
- **Entrada Esperada**:  
  ```text
  Ingrese un patrón de búsqueda (ej.: '^A' o 'land$'): ^A
  ```
- **Salida**:  
  ```text
  Datos guardados en datos_paises.xlsx
  Gráfico guardado como top_10_países_por_población.png
  ```

### **2. Ejecutar Módulos Individuales**  
#### **Obtener Datos desde la API**  
```python
from PIA_Modulo import obtener_datos_paises
datos = obtener_datos_paises()
print(f"Descargados {len(datos)} países.")
```

#### **Filtrar con Expresiones Regulares**  
```python
from PIA_Modulo import filtrar_paises_con_regex
paises_filtrados = filtrar_paises_con_regex(datos_estructurados, "^A")
print([p["Nombre"] for p in paises_filtrados])
```

#### **Exportar a Excel**  
```python
from PIA_Modulo import exportar_datos_excel
exportar_datos_excel(datos_estructurados, "datos_paises.xlsx")
```

---

## **Análisis del Script Principal (`script.py`)**  
### **Fortalezas**  
- **Modularización**: Cada función tiene responsabilidad única, facilitando mantenimiento.  
- **Escalabilidad**: Agregar nuevos módulos (ej.: análisis de correlación entre área y densidad) es sencillo.  

### **Posibles Mejoras**  
1. **Validación de Entradas**:  
   - Asegurar que `patron_regex` sea válido antes de ejecutar `filtrar_paises_con_regex`.  
   - Validar que `campo` en `analizar_estadisticas` exista en los datos.  
2. **Interfaz Web**:  
   - Usar Flask o Streamlit para una aplicación interactiva.  
3. **Pruebas Unitarias**:  
   - Agregar tests con `unittest` para validar funciones críticas.  
4. **Optimización de Gráficos**:  
   - Usar `seaborn` para gráficos más estilizados.  

---

## **Flujo Completo de Ejecución**  
### **1. Configuración Inicial**  
```bash
# Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate  # En Linux/macOS
pip install requests pandas matplotlib openpyxl
```

### **2. Ejecutar Script**  
```bash
python script.py
```
- **Pasos Internos**:  
  1. **Descarga de Datos**:  
     - `obtener_datos_paises()` → Datos en formato JSON.  
  2. **Estructuración**:  
     - `estructurar_datos_paises()` → Conversión a tabla.  
  3. **Análisis y Visualización**:  
     - `analizar_estadisticas()` → Media, mediana, moda.  
     - `graficar_datos()` → Gráfico de barras.  
  4. **Persistencia**:  
     - `guardar_datos_json()` → Archivo local.  
     - `exportar_datos_excel()` → Hoja de cálculo.  

### **3. Resultados Esperados**  
- **Archivo JSON**: `datos_paises.json` con campos como `Nombre`, `Población`, `Región`.  
- **Archivo Excel**: `datos_paises.xlsx` con los mismos datos, listo para análisis.  
- **Gráficos**:  
  - `top_10_países_por_población.png` (barras).  
  - `densidad_poblacional_de_países_filtrados.png` (líneas).  
- **Salida en Consola**:  
  ```text
  Países que coinciden con el patrón '^A':
  - Afghanistan, Albania, Algeria, Andorra, Argentina...

  Análisis estadístico de población:
  Media: 39378755.88
  Mediana: 6888660.0
  ```

---

## **Conexión con los Apuntes de Programación Básica**  
| **Módulo**                | **Fase del Curso** | **Apunte Relacionado**                          |
|---------------------------|--------------------|------------------------------------------------|
| `obtener_datos_paises()`  | Fase III           | "Automatización de tareas con APIs"            |
| `filtrar_paises_con_regex()` | Fase III         | "Expresiones regulares para manipular texto"    |
| `analizar_estadisticas()` | Fase III           | "Análisis de datos con estadísticas básicas"    |
| `graficar_datos()`       | Fase III           | "Generación de gráficos que comuniquen información" |
| `estructurar_datos_paises()` | Fase II         | "Uso de funciones y algoritmos"               |
| `exportar_datos_excel()` | Fase III           | "Manipulación de hojas de cálculo"            |

---

## **Conclusión**  
Este proyecto aplica los principios de las tres fases del curso:  
- **Fase I**: Uso de variables, ciclos y condicionales para procesar datos.  
- **Fase II**: Modularización, funciones reutilizables y estructuras anidadas.  
- **Fase III**: Integración con APIs, análisis estadístico y visualización gráfica.  

Al evitar dependencias de IDEs avanzados, se refuerza la disciplina en la programación, alineado con la metodología del curso de "construir soluciones inteligentes" desde cero.   
¡Ya formas parte del mundo de la programación! 🚀
